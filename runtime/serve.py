#!/usr/bin/env python3
"""Tiny stdlib static server for the NOESIS Cutout tool.

Serves this folder on http://127.0.0.1:8788 (localhost only), auto-opens the
browser, and sends CORS/isolation headers that allow the @imgly ESM CDN import
to load its WASM/ONNX assets:

  Cross-Origin-Opener-Policy:   same-origin
  Cross-Origin-Resource-Policy: cross-origin

We deliberately do NOT set Cross-Origin-Embedder-Policy (require-corp), because
COEP would block the cross-origin CDN module. HTML is served no-cache so edits
show up immediately.

Background removal itself always runs client-side in the browser (WASM/ONNX,
see index.html) -- images never leave the machine to be processed. The one
server route this file exposes is:

  POST /zip   multipart/form-data, one or more "image" parts (already
              background-removed PNGs from the browser). Packs them into an
              in-memory ZIP_STORED archive and returns it as application/zip.
              Used by the batch "Download ZIP" button in index.html; mirrors
              the same in-memory zipfile pattern as NOESIS-Slicer/serve.py.

No third-party dependencies — Python 3 standard library only.
"""

import io
import json
import os
import re
import sys
import webbrowser
import zipfile
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional
from urllib.parse import urlparse

HOST = "127.0.0.1"
# Fixed app port. Do not silently move to another port: users rely on this address.
PORT = 8788
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Batch-zip safety caps: a typo or a runaway client should never be able to
# hang the server or exhaust memory building the archive.
MAX_BATCH_FILES = 300
MAX_BATCH_BYTES = 300 * 1024 * 1024  # 300 MB total request body

_INVALID_NAME_CHARS = re.compile(r"[^A-Za-z0-9_\-. ]+")


# --------------------------------------------------------------------------
# Minimal multipart/form-data parser (stdlib only, no cgi module) -- mirrors
# the same approach used by NOESIS-Slicer/serve.py, extended to collect every
# part that repeats the same field name (one request can carry N images).
# --------------------------------------------------------------------------


def _extract_boundary(content_type: str) -> Optional[bytes]:
    match = re.search(r'boundary=(?:"([^"]+)"|([^;]+))', content_type)
    if not match:
        return None
    boundary = (match.group(1) or match.group(2)).strip()
    return boundary.encode("utf-8")


def _parse_multipart_files(body: bytes, boundary: bytes, field_name: str = "image") -> list:
    """Return every file part named `field_name`, in submission order, as
    [{"filename": str, "content": bytes}, ...]. Parts without a filename
    (plain form fields) are ignored -- this endpoint only cares about the
    uploaded image parts.
    """
    delimiter = b"--" + boundary
    files = []
    for raw_part in body.split(delimiter):
        part = raw_part.strip(b"\r\n")
        if not part or part == b"--":
            continue
        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            continue
        header_text = part[:header_end].decode("utf-8", errors="replace")
        content = part[header_end + 4:]
        if content.endswith(b"\r\n"):
            content = content[:-2]
        name_match = re.search(r'name="([^"]*)"', header_text)
        if not name_match or name_match.group(1) != field_name:
            continue
        filename_match = re.search(r'filename="([^"]*)"', header_text)
        filename = filename_match.group(1) if filename_match else None
        if not filename:
            continue
        files.append({"filename": filename, "content": content})
    return files


def _sanitize_zip_name(name: str, used: set) -> str:
    """Sanitize an untrusted client-supplied filename into a safe, unique zip
    entry name: strip any directory component (no path traversal), replace
    disallowed characters, force a .png extension, and dedupe collisions.
    """
    base = os.path.basename(name.replace("\\", "/"))
    cleaned = _INVALID_NAME_CHARS.sub("_", base).strip("._") or "image"
    if not cleaned.lower().endswith(".png"):
        cleaned += ".png"
    stem, ext = os.path.splitext(cleaned)
    candidate = cleaned
    n = 2
    while candidate in used:
        candidate = "{}_{}{}".format(stem, n, ext)
        n += 1
    used.add(candidate)
    return candidate


def _build_zip(files: list) -> bytes:
    buf = io.BytesIO()
    used: set = set()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_STORED) as zf:
        for f in files:
            name = _sanitize_zip_name(f["filename"], used)
            zf.writestr(name, f["content"])
    return buf.getvalue()


class Handler(SimpleHTTPRequestHandler):
    """Serve from the script's own directory with CDN-friendly headers."""

    def translate_path(self, path):
        # Resolve every request against ROOT, not the process CWD.
        rel = super().translate_path(path)
        cwd = os.getcwd()
        return os.path.join(ROOT, os.path.relpath(rel, cwd))

    def end_headers(self):
        # crossOriginIsolation enables multi-threaded WASM (fast inference).
        # Everything is vendored locally now, so we can safely turn it on.
        # COEP=credentialless (not require-corp) isolates WITHOUT breaking the
        # cross-origin Google Fonts <link> (require-corp would block them).
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cross-Origin-Resource-Policy", "cross-origin")
        # no-store on EVERYTHING: a local dev tool must never serve a stale
        # cached index.html/module (that is what caused an old publicPath to
        # keep pointing at a CDN -> "Failed to fetch"). Vendored assets are on
        # local disk, so re-fetching every load is instant.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  [srv] " + (fmt % args) + "\n")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/zip":
            self.send_error(404)
            return
        try:
            self._handle_zip()
        except Exception as exc:  # top-level request guard: always answer the client
            self._send_json_error(str(exc))

    def _handle_zip(self):
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            raise ValueError("expected multipart/form-data")
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            raise ValueError("empty request body")
        if length > MAX_BATCH_BYTES:
            raise ValueError("upload too large")
        body = self.rfile.read(length)

        boundary = _extract_boundary(content_type)
        if boundary is None:
            raise ValueError("missing multipart boundary")
        files = _parse_multipart_files(body, boundary, field_name="image")
        if not files:
            raise ValueError("no images received")
        if len(files) > MAX_BATCH_FILES:
            raise ValueError("too many images in one batch (max {})".format(MAX_BATCH_FILES))

        zip_bytes = _build_zip(files)

        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", 'attachment; filename="noesis-cutout-batch.zip"')
        self.send_header("Content-Length", str(len(zip_bytes)))
        self.end_headers()
        self.wfile.write(zip_bytes)

    def _send_json_error(self, message, status=400):
        payload = json.dumps({"error": message}).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class _Server(ThreadingHTTPServer):
    # SO_REUSEADDR so a socket lingering in TIME_WAIT (the usual cause of
    # "address already in use" right after a restart) does not block rebinding.
    allow_reuse_address = True


def _make_server():
    """Bind the application to its one documented port."""
    try:
        return _Server((HOST, PORT), Handler), PORT
    except OSError as exc:
        raise RuntimeError(
            "NOESIS Cut-Out port {} is busy. Close the other Cut-Out server or "
            "choose a different documented port before starting it.".format(PORT)
        ) from exc


def main():
    os.chdir(ROOT)
    httpd, port = _make_server()
    url = "http://{}:{}/".format(HOST, port)

    print("=" * 56)
    print("  NOESIS Cutout  ·  Background Remover")
    print("  Serving:  " + ROOT)
    print("  Open:     " + url)
    print("  (Ctrl+C to stop)")
    print("=" * 56)

    # Browser launch is intentionally disabled; users open the printed URL manually.

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.server_close()


if __name__ == "__main__":
    main()

# NOESIS Cut-Out

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-76B900.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-76B900.svg)](#portability)
[![Mode: Local](https://img.shields.io/badge/mode-local-111827.svg)](#privacy-and-security)
[![Port: 8788](https://img.shields.io/badge/port-8788-111827.svg)](#quick-start)

> **Remove the background. Keep the subject.**
>
> A focused local tool for turning ordinary images into clean transparent PNG assets.

NOESIS Cut-Out is a portable Windows application for removing image backgrounds locally. It is designed for product images, profile pictures, icons, thumbnails and other assets where the subject should remain visible and the background should become transparent.

## At a glance

| Item | Details |
|---|---|
| Primary task | Local image background removal |
| Input | PNG, JPG and WEBP images |
| Output | Transparent PNG |
| Interface | Local browser UI |
| Default state | English language, dark theme |
| Server | `127.0.0.1:8788` |
| License | Apache-2.0 |

## Why use it

Cut-Out keeps the workflow short: choose an image, remove the background, inspect the result and export a PNG. Once the local assets are available, image processing happens on the computer instead of sending the image to a remote web service.

The interface uses the common NOESIS visual system: the same dark background, typography, language selector, flags, theme controls and interaction patterns as the other four applications.

## Highlights

- **Local processing:** the image remains in the local application workflow.
- **Common NOESIS shell:** English and dark mode are the first-run defaults.
- **Practical formats:** PNG, JPG and WEBP input with transparent PNG export.
- **Preview-first workflow:** inspect the result before saving it.
- **Portable layout:** launch from the extracted folder without a system-wide install.

## Quick start

1. Extract the complete application folder. Do not move files out of their subfolders.
2. Double-click `START.bat`.
3. Open `http://127.0.0.1:8788/` manually when the console prints the address.
4. Add an image, select **Remove background**, review the preview and download the PNG.

The server does **not** open a browser automatically. Port `8788` is fixed for Cut-Out. If the port is already in use, close the other Cut-Out server before starting this one.

## How the workflow works

The local server delivers the HTML interface and bundled assets. The browser loads the local processing components, runs background removal and displays the result. The final PNG is generated in the local session and downloaded by the browser.

| Stage | What happens |
|---|---|
| 1. Select | Choose or drop an image into the upload area. |
| 2. Process | The local background-removal pipeline separates the subject from the background. |
| 3. Review | Check the transparent preview and touch up the result when the interface offers that option. |
| 4. Export | Download a transparent PNG to the location selected by Windows. |

## Portability

`START.bat` performs preflight checks for the portable runtime, disk space, fixed-port availability and protected-file integrity. Heavy runtime components are intentionally not stored in the public Git repository; a complete private distribution or bootstrap step may be required before first use.

The application folder should remain writable during setup and while saving generated files. It is safe to place the folder on another local drive, provided the full directory tree is copied together.

## Privacy and security

The local server binds to `127.0.0.1`, so it is intended for use on the same computer. Do not publish private images, generated output, cookies, tokens, logs or local caches. The repository excludes local state and heavy runtime payloads through `.gitignore`.

## Troubleshooting

If the page does not load, confirm that `START.bat` completed preflight, that the complete folder was extracted and that port `8788` is free. If processing fails, confirm that the required local assets are present and that the application folder is writable. If the browser shows an older shell, reload the page without cache.

For the technical start sequence and distribution rules, see [`docs/README.md`](docs/README.md).

## License and third-party components

NOESIS application code is licensed under the [Apache License 2.0](LICENSE). Bundled fonts, background-removal libraries, ONNX Runtime assets and model files remain subject to their own licenses and notices.

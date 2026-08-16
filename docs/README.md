# NOESIS Cut-Out — technical notes

## Start sequence

`START.bat` validates the local portable runtime, verifies the integrity manifest, checks disk space and checks the fixed port. The local server listens on `127.0.0.1:8788`. The launcher intentionally does not call `webbrowser.open`; the user opens the printed URL manually.

## Runtime model

The web shell is served by the local Python runtime in `runtime/`. UI styles, language data, flags and fonts are served from `vendor/`. Image processing stays on the local machine.

## Distribution rules

Do not publish user output, cookies, logs, cache folders, model downloads, embedded Python payloads or local diagnostics. The root `.gitignore` is the publication baseline. If a runtime file changes, recalculate `runtime/preflight_manifest.json` before distribution.

## Troubleshooting

If the page does not load, confirm that `START.bat` completed preflight, that port 8788 is free and that the complete folder was extracted. If the server starts but processing fails, confirm that the required local model/runtime assets are present and that the application folder is writable.

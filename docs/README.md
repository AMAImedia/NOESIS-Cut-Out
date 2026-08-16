# NOESIS Cut-Out — local guide

This document explains the Cut-Out workflow in plain language. The shorter project overview is in [`../README.md`](../README.md).

## What this application does

Cut-Out removes the background from an image and lets you save the result as a transparent PNG. It is useful for product pictures, avatars, icons, thumbnails and simple design assets.

## Start the application

1. Copy or extract the complete `NOESIS-Cut-Out` folder.
2. Do not move `START.bat` away from the folder and do not rename the subfolders.
3. Double-click `START.bat`.
4. Wait until the console reports that the local server is ready.
5. Open `http://127.0.0.1:8788/` manually in the browser you prefer.

The application intentionally does not open a browser by itself. Port `8788` is fixed. If another Cut-Out instance is already using it, close that instance first.

## Use the interface

Choose an image or drop it into the upload area. Start **Remove background** and wait for the preview. If touch-up controls are available, use them to correct small missed or removed regions. Download the final transparent PNG when the preview looks correct.

The image is processed through the local application workflow. The browser is only the interface; the local server provides the application assets and processing route.

## What happens before startup

`START.bat` checks the portable runtime, required files, SHA-256 integrity, free disk space and port availability. A failed preflight is a safety stop: read the console message rather than launching a different Python installation manually.

Heavy model and runtime payloads are not stored in the public Git repository. A complete private portable package or the project bootstrap process may be required before processing works on a new computer.

## Common problems

| Symptom | What to check |
|---|---|
| Page does not open | Confirm preflight completed, the folder is complete and port 8788 is free. |
| Background removal fails | Confirm local model/runtime assets are present and the folder is writable. |
| Old design is visible | Reload the page without cache after confirming the server is the current instance. |
| Export does not save | Check Windows download permissions and free disk space. |

## Safe distribution

Do not publish private images, generated PNG files, cookies, tokens, logs, cache folders or downloaded model/runtime payloads. The root `.gitignore` is the publication baseline. If a protected runtime file changes, regenerate `runtime/preflight_manifest.json` before distributing the folder.

## File map

| Location | Purpose |
|---|---|
| `START.bat` | User-facing launcher. |
| `index.html` | User-facing application shell. |
| `runtime/` | Local server, preflight and startup helpers. |
| `vendor/` | UI styles, language data, fonts and local browser assets. |
| `docs/` | Human-readable local documentation. |

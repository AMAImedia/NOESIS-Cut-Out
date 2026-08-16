# NOESIS Cut-Out

Local image background removal for Windows portable workflows. NOESIS Cut-Out runs a local web interface and produces transparent PNG images without uploading user images to a remote service.

## Features

The application supports PNG, JPG and WEBP input, multiple-image selection, local U2-Net background removal, preview, touch-up and PNG export. Its interface uses the shared AMAImedia/NOESIS visual shell with English as the first-run language and dark mode as the first-run theme.

## Run

1. Extract the complete application folder.
2. Double-click `START.bat`.
3. Open `http://127.0.0.1:8788/` manually when the console prints the address.
4. Drop an image into the upload area, choose **Remove background**, and download the PNG.

The application does not open a browser automatically. Port `8788` is fixed for this application. If it is already occupied, close the other Cut-Out server before starting this one.

## Portability

The launcher checks the embedded Python runtime, disk space, port availability and SHA-256 integrity before starting. Lightweight UI assets, fonts and local web model assets are kept inside the application tree. Heavy runtime components are downloaded or restored by the bootstrap process when they are not included in a public distribution.

## Privacy and security

The server binds to `127.0.0.1` only. Images are processed locally by the application. Do not place private cookies, tokens, personal files or generated output inside a public repository clone.

## Repository layout

The public root contains only the user-facing entrypoints and publication files. Runtime helpers are under `runtime/`; local assets are under `vendor/`; user output and downloaded components are excluded by `.gitignore`.

## License

The NOESIS application code is licensed under the Apache License 2.0. See [LICENSE](LICENSE). Third-party assets remain subject to their own licenses and notices.

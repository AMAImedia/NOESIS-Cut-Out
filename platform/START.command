#!/bin/bash
cd "$(dirname "$0")"
echo
echo "  NOESIS Cut-Out"
echo "  ================================================"
echo "  Свой Python в папке. Системный не нужен."
echo "  ================================================"
echo
ARCH=$(uname -m)
case "$ARCH" in
  arm64) TGZ="vendor/python-macos/aarch64.tar.gz" ;;
  x86_64) TGZ="vendor/python-macos/x86_64.tar.gz" ;;
  *) echo "  Неизвестная архитектура: $ARCH"; read -r _; exit 1 ;;
esac
PYDIR="vendor/python-macos/python"
if [ ! -x "$PYDIR/bin/python3" ]; then
  if [ ! -f "$TGZ" ]; then echo "  [Ошибка] Нет $TGZ"; read -r _; exit 1; fi
  echo "  Распаковываю Python для macOS ($ARCH)..."
  mkdir -p vendor/python-macos
  tar -xzf "$TGZ" -C vendor/python-macos
fi
if [ ! -x "$PYDIR/bin/python3" ]; then echo "  [Ошибка] Python не распаковался"; read -r _; exit 1; fi
exec "$PYDIR/bin/python3" serve.py

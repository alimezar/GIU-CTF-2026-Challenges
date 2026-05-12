#!/usr/bin/env bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 file.sage"; exit 1
fi

HOST_DIR="$(pwd -W)"   # Windows-style path for Docker on Windows
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL="*" \
docker run --rm -it \
  -v "$HOST_DIR":/work \
  -w /work sagemath/sagemath:latest sage "$1"
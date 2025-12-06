#!/usr/bin/env bash
# generate sha256 for data and screenshots originals
set -e
echo "Generating checksums sha256 for data and screenshots originals"
find data screenshots/originals -type f -print0 | sort -z | xargs -0 sha256sum > ../checksums.sha256
echo "checksums saved to checksums.sha256 in repo root"

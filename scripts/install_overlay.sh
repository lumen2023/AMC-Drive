#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/navsim_v1" >&2
  exit 2
fi

TARGET_ROOT="$1"
PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$TARGET_ROOT/navsim" ]]; then
  echo "Target does not look like a NAVSIM v1 devkit: $TARGET_ROOT" >&2
  exit 2
fi

rsync -a "$PACKAGE_ROOT/navsim_v1_overlay/" "$TARGET_ROOT/"
echo "Installed AMC-Drive overlay into $TARGET_ROOT"

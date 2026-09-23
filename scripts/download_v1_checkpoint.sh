#!/usr/bin/env bash
set -euo pipefail

REPO_ID="${AMC_DRIVE_HF_REPO:-Lumen-SEU/AMC-Drive-NAVSIM-v1-0919}"
REMOTE_PATH="${AMC_DRIVE_HF_CKPT_PATH:-checkpoints/AMC-Drive_navsimv1_pdms93.9.ckpt}"
EXPECTED_SHA="2fc81a59e7bb183069403a2c9cc204f29cd86d4b71e4ddba4da8ba5dbb9e4047"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/checkpoints"
OUT_FILE="$OUT_DIR/AMC-Drive_navsimv1_pdms93.9.ckpt"
mkdir -p "$OUT_DIR"

if [[ -f "$OUT_FILE" ]]; then
  echo "Checkpoint already exists: $OUT_FILE"
else
  if command -v huggingface-cli >/dev/null 2>&1; then
    huggingface-cli download "$REPO_ID" "$REMOTE_PATH" \
      --local-dir "$ROOT" \
      --local-dir-use-symlinks False
  else
    python - <<PY
from huggingface_hub import hf_hub_download
from pathlib import Path
repo_id = "$REPO_ID"
filename = "$REMOTE_PATH"
root = Path("$ROOT")
path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=root)
print(path)
PY
  fi
fi

if [[ ! -f "$OUT_FILE" ]]; then
  echo "Checkpoint was not found at $OUT_FILE after download." >&2
  exit 1
fi

ACTUAL_SHA="$(sha256sum "$OUT_FILE" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "SHA-256 mismatch for $OUT_FILE" >&2
  echo "expected: $EXPECTED_SHA" >&2
  echo "actual:   $ACTUAL_SHA" >&2
  exit 1
fi

echo "Checkpoint verified: $OUT_FILE"

#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/navsim_v1" >&2
  exit 2
fi

TARGET_ROOT="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECKPOINT="$ROOT/checkpoints/AMC-Drive_navsimv1_pdms93.9.ckpt"
EXPECTED_SHA="2fc81a59e7bb183069403a2c9cc204f29cd86d4b71e4ddba4da8ba5dbb9e4047"

require_path() {
  local path="$1"
  local label="$2"
  if [[ ! -e "$path" ]]; then
    echo "Missing $label: $path" >&2
    exit 1
  fi
}

require_path "$TARGET_ROOT/navsim" "NAVSIM package directory"
require_path "$TARGET_ROOT/data/8192.npy" "NAVSIM anchor file"
require_path "$ROOT/navsim_v1_overlay/navsim/agents/amc_drive/amc_drive_agent.py" "AMC agent"
require_path "$ROOT/navsim_v1_overlay/navsim/planning/script/config/common/agent/amc_drive_agent.yaml" "AMC agent config"
require_path "$ROOT/scripts/install_overlay.sh" "overlay installer"
require_path "$ROOT/scripts/create_navsimv1_submission.sh" "submission script"
require_path "$ROOT/checkpoints/SHA256SUMS" "checkpoint checksum manifest"

if [[ ! -x "$ROOT/scripts/install_overlay.sh" || ! -x "$ROOT/scripts/create_navsimv1_submission.sh" ]]; then
  echo "Release scripts must be executable." >&2
  exit 1
fi

if [[ ! -f "$CHECKPOINT" ]]; then
  echo "Checkpoint missing: $CHECKPOINT" >&2
  echo "Run: bash scripts/download_v1_checkpoint.sh" >&2
  exit 1
fi

ACTUAL_SHA="$(sha256sum "$CHECKPOINT" | awk '{print $1}')"
if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "Checkpoint SHA-256 mismatch." >&2
  echo "expected: $EXPECTED_SHA" >&2
  echo "actual:   $ACTUAL_SHA" >&2
  exit 1
fi

PRIVATE_RE="${HOME}|Navsim""_Data|Drive-JEPA-""official-v2"
if rg -n "$PRIVATE_RE" "$ROOT" \
  --glob '!checkpoints/*.ckpt' \
  --glob '!*.pyc' \
  --glob '!.git/**' >/tmp/amc_drive_private_paths.txt; then
  echo "Private/local source paths found:" >&2
  cat /tmp/amc_drive_private_paths.txt >&2
  exit 1
fi

echo "AMC-Drive V1 release verification passed."

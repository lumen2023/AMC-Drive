#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/navsim_v1" >&2
  exit 2
fi

NAVSIM_DEVKIT_ROOT="$1"
AMC_DRIVE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -z "${PYTHON_BIN:-}" ]]; then
  CONDA_BASE="$(conda info --base 2>/dev/null || true)"
  CONDA_NAVSIM_PYTHON="${CONDA_BASE:+$CONDA_BASE/envs/navsim/bin/python}"
  if [[ -n "$CONDA_NAVSIM_PYTHON" && -x "$CONDA_NAVSIM_PYTHON" ]]; then
    PYTHON_BIN="$CONDA_NAVSIM_PYTHON"
  else
    PYTHON_BIN="python"
  fi
fi
export NAVSIM_DEVKIT_ROOT
export AMC_DRIVE_ROOT
export PYTHONPATH="$NAVSIM_DEVKIT_ROOT${PYTHONPATH:+:$PYTHONPATH}"

TEAM_NAME="${TEAM_NAME:-AMC-Drive}"
AUTHORS="${AUTHORS:-Yongzhi Liu}"
EMAIL="${EMAIL:-230268037@seu.edu.cn}"
INSTITUTION="${INSTITUTION:-Southeast University}"
COUNTRY="${COUNTRY:-China}"
TRAIN_TEST_SPLIT="${TRAIN_TEST_SPLIT:-navtest}"
EXPERIMENT_NAME="${EXPERIMENT_NAME:-AMC-Drive_navsimv1_submission}"
EXTRA_ARGS=()
if [[ -n "${CHECKPOINT_PATH:-}" ]]; then
  EXTRA_ARGS+=(agent.checkpoint_path="$CHECKPOINT_PATH")
fi

"$AMC_DRIVE_ROOT/scripts/install_overlay.sh" "$NAVSIM_DEVKIT_ROOT"

cd "$NAVSIM_DEVKIT_ROOT"
"$PYTHON_BIN" navsim/planning/script/run_create_amc_drive_submission_pickle.py \
  train_test_split="$TRAIN_TEST_SPLIT" \
  agent=amc_drive_agent \
  experiment_name="$EXPERIMENT_NAME" \
  team_name="$TEAM_NAME" \
  authors="$AUTHORS" \
  email="$EMAIL" \
  institution="$INSTITUTION" \
  country="$COUNTRY" \
  "${EXTRA_ARGS[@]}"

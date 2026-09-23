# AMC-Drive

## How Many Futures Are Enough?

**Learning Redundancy-Aware Effective Multimodality for End-to-End Autonomous
Driving with Action-Conditioned Predictive Representations**

AMC-Drive is a Drive-JEPA-lineage, proposal-based end-to-end driving planner.
Drive-JEPA provides the proposal-based driving foundation. AMC-Drive calibrates
fixed-budget proposal organization in consequence space. The deployed interface
remains a standard `K=32` proposal-based planner: the model generates 32
candidate trajectories, scores them, and selects one trajectory for NAVSIM.

GitHub stores the code, release metadata, scripts, and reproducibility
documents. Hugging Face stores the large V1 checkpoint.

中文简述：AMC-Drive 是基于 Drive-JEPA 主线的固定预算多模态规划器。V1
保持 `K=32` 的 NAVSIM v1 proposal planner 部署接口，同时公开
consequence-aware effective multimodality 的代码、文档和迁移协议。

## V1 Status

| Component | Status |
| --- | --- |
| NAVSIM v1 proposal-based planner | `AVAILABLE` |
| V1 checkpoint | `AVAILABLE via Hugging Face` |
| V1 submission script | `AVAILABLE` |
| NAVSIM v1 score package | `AVAILABLE` |
| NAVSIM v2 full release | `TODO: V2` |
| HUGSIM full training/release | `TODO: HUGSIM` |
| Diffusion Policy adapter | `INTERFACE / PROTOCOL READY` |
| Flow Matching adapter | `INTERFACE / PROTOCOL READY` |
| Robot policy adapter | `INTERFACE / PROTOCOL READY` |
| Full cross-domain benchmark | `TODO: matched validation` |

AMC-Drive is released first as a verified automotive V1 implementation. Its
consequence-aware interface is organized to support later migration to
diffusion, flow-matching, and robot-policy decoders. Those migrations are
staged as explicit adapters with endpoint validation rather than being
conflated with the V1 NAVSIM result.

## Headline

The V1 release package records the following NAVSIM v1 evidence:

- NAVSIM v1 local full-navtest PDMS: `0.939443730214`
- NAVSIM v1 submission-pickle rescore: `0.939443730121`
- Public score label: `93.9 PDMS`
- Prediction count: `12146`
- Component summary: `NC 98.7`, `DAC 98.6`, `EP 92.2`, `C 99.8`, `TTC 95.8`

The V2 and HUGSIM values are roadmap items for later release packages unless
their full checkpoints, evaluator manifests, and reproduction scripts are added
to this repository.

## Architecture

```text
camera input
-> camera / BEV feature construction
-> ego-state encoding
-> K=32 proposal embeddings
-> shared trajectory refinement
-> proposal scorer
-> score aggregation
-> argmax
-> one selected trajectory
```

The proposal count, trajectory horizon, selected-trajectory API, and NAVSIM
submission format stay Drive-JEPA-compatible. AMC-Drive's scientific layer is
the fixed-budget consequence-aware view of how the 32 slots are organized.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Repository Layout

```text
navsim_v1_overlay/          AMC-Drive NAVSIM v1 overlay
scripts/                    install, checkpoint download, submission, verify
checkpoints/                SHA-256 manifest and downloaded checkpoint target
evidence/                   V1 score summary
docs/                       paper mainline, reproduction, roadmap, lineage
docs/migration/             DM/FM/robot migration protocol notes
extensions/transfer_contracts/
                            decoder-agnostic interface contracts
```

## Installation

Prepare a standard NAVSIM v1 / Drive-JEPA-style environment first. The target
devkit should contain:

```text
/path/to/navsim_v1/navsim/
/path/to/navsim_v1/data/8192.npy
```

Typical environment variables follow the NAVSIM / Drive-JEPA convention:

```bash
export NUPLAN_MAP_VERSION="nuplan-maps-v1.0"
export NUPLAN_MAPS_ROOT="$HOME/navsim_workspace/dataset/maps"
export NAVSIM_EXP_ROOT="$HOME/navsim_workspace/exp"
export NAVSIM_DEVKIT_ROOT="$HOME/navsim_workspace/navsim_v1"
export OPENSCENE_DATA_ROOT="$HOME/navsim_workspace/dataset"
```

Install dependencies according to the Drive-JEPA / NAVSIM v1 environment,
including PyTorch, NAVSIM, nuPlan, MMCV, MMDetection, and the packages listed
in the upstream Drive-JEPA requirements.

## Download the V1 Checkpoint

```bash
bash scripts/download_v1_checkpoint.sh
```

Expected checkpoint:

```text
checkpoints/AMC-Drive_navsimv1_pdms93.9.ckpt
sha256: 2fc81a59e7bb183069403a2c9cc204f29cd86d4b71e4ddba4da8ba5dbb9e4047
```

The checkpoint is intentionally ignored by Git. The download script verifies
the SHA-256 hash after download.

## Verify the Release

```bash
bash scripts/verify_v1_release.sh /path/to/navsim_v1
```

The verifier checks the target NAVSIM v1 devkit, the checkpoint hash, script
permissions, overlay files, and release metadata.

## Create a NAVSIM v1 Submission

```bash
TEAM_NAME="AMC-Drive" \
AUTHORS="Yongzhi Liu" \
EMAIL="230268037@seu.edu.cn" \
INSTITUTION="Southeast University" \
COUNTRY="China" \
bash scripts/create_navsimv1_submission.sh /path/to/navsim_v1
```

The script installs the overlay into the target NAVSIM v1 devkit and runs the
normal NAVSIM submission-pickle creation script. It does not modify this
source tree.

## Roadmap

- `V1`: NAVSIM v1 proposal-based planner, checkpoint, deployment script.
- `V2`: NAVSIM v2 full release with checkpoint, evaluator manifest, and script.
- `HUGSIM`: full training/release package with no-HUGSIM-specific-fine-tuning
  provenance and evaluator manifest.
- `DM/FM/Robot`: decoder-specific adapters and endpoint validation.

AMC-Drive exposes a decoder-agnostic migration interface and validation
protocol. Full DM/FM/robot implementations are scheduled as subsequent
releases.

## Citation

If you use AMC-Drive, please cite this repository and the upstream systems that
make it possible. See [CITATION.cff](CITATION.cff).

## Acknowledgements

AMC-Drive is built on the Drive-JEPA / NAVSIM ecosystem. We thank the authors
and maintainers of Drive-JEPA, NAVSIM, nuPlan, V-JEPA 2, BEVFormer, MMCV,
MMDetection, TransFuser, Bench2Drive, and related open-source projects. See
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for details.

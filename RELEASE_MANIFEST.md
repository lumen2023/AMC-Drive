# AMC-Drive V1 Release Manifest

- Package name: `AMC-Drive`
- Release line: `V1 NAVSIM proposal-based planner`
- Branch policy: `main` contains the automotive NAVSIM v1 proposal planner.
- Method title: `How Many Futures Are Enough? Learning Redundancy-Aware
  Effective Multimodality for End-to-End Autonomous Driving with
  Action-Conditioned Predictive Representations`
- Author: `Yongzhi Liu`
- Contact email: `230268037@seu.edu.cn`
- Institution: `Southeast University`
- Hugging Face namespace: `Lumen-SEU`
- Target model repo: `Lumen-SEU/AMC-Drive-NAVSIM-v1-0919`
- NAVSIM agent config: `amc_drive_agent`
- Agent class: `navsim.agents.amc_drive.amc_drive_agent.AMCDriveAgent`
- Model class: `navsim.agents.amc_drive.amc_drive_model.AMCDriveModel`
- Checkpoint target: `checkpoints/AMC-Drive_navsimv1_pdms93.9.ckpt`
- Checkpoint storage: `Hugging Face`, not Git history
- Public score label: `NAVSIM v1 PDMS 93.9`
- Local submission-pickle rescore: `0.939443730121`

## Release Boundary

This V1 package contains NAVSIM v1 inference/deployment code and release
metadata. NAVSIM v2, HUGSIM, Diffusion Policy, Flow Matching, and robot-policy
releases are documented as roadmap or interface-level extensions unless their
future checkpoints and evaluator manifests are added explicitly.

## Integrity

The V1 checkpoint hash is recorded in `checkpoints/SHA256SUMS`. The checkpoint
file itself is ignored by Git and must be downloaded separately.

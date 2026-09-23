# NAVSIM v1 Reproduction

## 1. Prepare NAVSIM v1

Install the NAVSIM v1 devkit and data following the NAVSIM / Drive-JEPA setup.
The target path must contain:

```text
/path/to/navsim_v1/navsim/
/path/to/navsim_v1/data/8192.npy
```

## 2. Download the V1 Checkpoint

```bash
bash scripts/download_v1_checkpoint.sh
```

## 3. Verify the Release

```bash
bash scripts/verify_v1_release.sh /path/to/navsim_v1
```

## 4. Create the Submission Pickle

```bash
TEAM_NAME="AMC-Drive" \
AUTHORS="Yongzhi Liu" \
EMAIL="230268037@seu.edu.cn" \
INSTITUTION="Southeast University" \
COUNTRY="China" \
bash scripts/create_navsimv1_submission.sh /path/to/navsim_v1
```

## 5. Expected Evidence

The V1 release records:

```text
Prediction count: 12146
Local full-navtest PDMS: 0.939443730214
Submission-pickle rescore: 0.939443730121
Public label: NAVSIM v1 PDMS 93.9
```

The exact output path is controlled by the NAVSIM/Hydra configuration and
`NAVSIM_EXP_ROOT`.

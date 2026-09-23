# AMC-Drive V1 Architecture

AMC-Drive V1 is a NAVSIM v1 proposal-based planner with a fixed deployment
budget of `K=32` candidate trajectories. It preserves the Drive-JEPA-style
proposal and scorer interface while organizing the candidate set under a
consequence-aware effective-multimodality view.

## Runtime Data Flow

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

The deployed model does not emit more than 32 proposals and does not deploy an
oracle trajectory. It emits the scorer-selected candidate trajectory.

## Core Classes

- `AMCDriveAgent`: NAVSIM agent wrapper, sensor contract, feature builders,
  checkpoint loading, loss path, and optimizer path.
- `AMCDriveModel`: image/BEV encoder, ego-state encoding, proposal embeddings,
  shared trajectory refinement, proposal scorer, and final argmax.
- `AMCDriveConfig`: fixed `K=32`, trajectory horizon, model dimensions, and
  auxiliary regularizer switches.
- `AMCDriveFeatureBuilder`: camera, BEV, and ego-state feature construction.

## Fixed-Budget Interpretation

The method distinguishes:

```text
K_generated = 32
K_effective = consequence-distinct opportunity represented by those slots
```

Two models can both perform 32-to-1 selection and still differ because the
candidate set before the final argmax may contain different opportunity
structure. AMC-Drive studies that structure without changing the deployment
API.

## Consequence-Aware Calibration

The scientific interface is:

```text
candidate actions -> frozen predictive representation -> pairwise affinity
-> effective multimodality / topology statistics -> auxiliary calibration
```

The frozen predictive representation is a calibration coordinate system. It is
not treated as a ground-truth oracle. Endpoint quality is measured separately
through NAVSIM/PDM-style evaluation.

## Selected-vs-Oracle Boundary

For a scene:

```text
S = selected candidate score
O = best-of-32 oracle candidate score
G = O - S
```

Therefore:

```text
S = O - G
```

This identity separates candidate opportunity from scorer conversion. V1
deployment uses `S`, not `O`.

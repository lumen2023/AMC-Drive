# Drive-JEPA Lineage

AMC-Drive is intentionally close to Drive-JEPA. This makes the comparison
interpretable and keeps the deployable interface familiar to NAVSIM users.

Drive-JEPA contributes the proposal-based driving foundation:

```text
scene features
-> fixed trajectory proposal set
-> scorer
-> selected trajectory
```

AMC-Drive contributes a fixed-budget consequence-aware calibration view:

```text
K=32 proposal set
-> consequence affinity
-> effective multimodality / topology
-> capacity calibration
-> selected trajectory through the usual scorer
```

## What Stays Compatible

- Candidate count: `K=32`.
- Trajectory horizon and coordinate convention.
- Proposal refinement and scorer-style selection.
- NAVSIM agent and submission-pickle interface.

## What AMC-Drive Adds

- A paper-facing interpretation of proposal slots as capacity.
- Consequence-aware effective multimodality.
- Migration contracts for non-Drive-JEPA decoders.
- A release boundary that separates V1 automotive deployment from future
  V2/HUGSIM/DM/FM/robot releases.

## Required Attribution

Users should cite both AMC-Drive and Drive-JEPA when using this repository.
Drive-JEPA remains the direct architecture and implementation lineage for V1.

# AMC-Drive Paper Mainline

## Title

How Many Futures Are Enough? Learning Redundancy-Aware Effective
Multimodality for End-to-End Autonomous Driving with Action-Conditioned
Predictive Representations

## Core Question

Drive-JEPA demonstrates that a fixed-budget proposal planner can be very
strong. AMC-Drive asks a deeper structural question:

```text
When a planner must emit K=32 proposals, how much consequence-distinct
future opportunity do those 32 slots actually represent?
```

中文：AMC-Drive 不问“能不能输出 32 条轨迹”，而问“这 32 个固定 slot
到底表达了多少有用且后果不同的未来”。

## From Drive-JEPA to AMC-Drive

Drive-JEPA provides:

```text
visual / BEV features
-> fixed proposal generation
-> proposal scoring
-> one selected trajectory
```

AMC-Drive keeps that deployment interface and adds:

```text
candidate action
-> action-conditioned predictive representation
-> consequence affinity
-> effective multimodality
-> topology-aware capacity calibration
```

## Fixed K and Effective Multimodality

The physical proposal budget is fixed:

```text
K_generated = 32
```

The effective opportunity represented by those proposals can be smaller or
better organized:

```text
K_effective != K_generated
```

The contribution is not variable-cardinality planning. The contribution is a
principled way to reason about the internal organization of a fixed candidate
set.

## Consequence-Aware Capacity Calibration

For each candidate action or trajectory, a frozen action-conditioned predictive
representation provides a coordinate for comparing possible futures. Pairwise
affinity in that space exposes redundancy amount and redundancy topology.

This representation is an operational calibration view, not a ground-truth
semantic oracle. Endpoint performance must still be measured with the selected
trajectory under the task evaluator.

## Opportunity-to-Decision Interface

For each scene:

```text
S = selected endpoint score
O = best-of-32 oracle score
G = O - S
S = O - G
```

This identity separates proposal opportunity from scorer conversion. AMC-Drive
can be useful when it increases or better organizes opportunity and the scorer
can convert that opportunity into the selected trajectory.

## Benchmark and Release

V1 reports NAVSIM v1 PDMS `93.9` through the release package:

```text
local full-navtest PDMS: 0.939443730214
submission-pickle rescore: 0.939443730121
prediction count: 12146
```

NAVSIM v2 and HUGSIM are planned as later release packages with separate
checkpoint and evaluator manifests.

## Migration Interface

The same fixed-budget question appears in other multimodal generators:

- diffusion policies;
- flow-matching decoders;
- robot action-chunk policies.

AMC-Drive exposes a decoder-agnostic interface, but every new decoder family
requires its own representation validation and endpoint audit.

## ICLR Positioning

The ICLR-level contribution is:

```text
fixed proposal budget
-> effective multimodality
-> consequence-aware topology
-> explicit opportunity-to-decision conversion
```

The paper should be positive and ambitious while remaining reviewer-safe:

```text
AMC-Drive does not change how many proposals a planner emits; it changes how
much consequence-distinct opportunity those fixed proposals can represent, and
it provides the mathematical interface required to convert that opportunity
into a selected decision.
```

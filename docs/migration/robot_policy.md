# Robot Policy Migration

Robot policies can use the AMC-Drive interface when they generate a fixed set
of candidate action chunks or end-effector trajectories.

## Interface

```text
robot observation
-> K candidate action chunks
-> task-aware consequence representation
-> redundancy relation
-> fixed-budget capacity calibration
-> selected robot action
```

## Endpoint Replacement

NAVSIM/PDM metrics must be replaced by robot-task endpoints such as:

- task success rate;
- collision or constraint violation;
- final distance to goal;
- smoothness or control cost;
- recovery or robustness under perturbation.

## Validation Gate

Before claiming robot transfer:

- keep the action budget fixed;
- compare matched policies with and without AMC calibration;
- report selected endpoint metrics;
- audit failure modes for safety-critical tasks;
- separate interface compatibility from benchmark improvement.

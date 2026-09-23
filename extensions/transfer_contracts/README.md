# Transfer Contracts

This directory contains lightweight interfaces for migrating AMC-Drive's
fixed-budget consequence-aware view to other decoder families.

The contracts are intentionally framework-neutral. They do not import NAVSIM,
Drive-JEPA, PyTorch, or robot-specific packages.

## Minimal Pipeline

```python
candidate = decoder.sample(condition, budget=K)
representation = consequence_encoder(condition, candidate)
relation = redundancy_relation(representation)
loss = capacity_calibration(candidate, relation, endpoint_context)
selected = selector(candidate, score)
```

## Status

These contracts are public V1 migration scaffolding. They are not by
themselves evidence of completed DM/FM/robot endpoint performance.

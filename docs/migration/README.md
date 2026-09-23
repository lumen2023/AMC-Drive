# Migration Roadmap

AMC-Drive V1 is a NAVSIM v1 automotive release. The migration package explains
how the same fixed-budget consequence-aware interface can be adapted to other
decoder families without claiming that those adaptations are already fully
benchmarked in V1.

The common interface is:

```python
candidate = decoder.sample(condition, budget=K)
representation = consequence_encoder(condition, candidate)
relation = redundancy_relation(representation)
loss = capacity_calibration(candidate, relation, endpoint_context)
selected = selector(candidate, score)
```

## Status

| Target | V1 status |
| --- | --- |
| Diffusion Policy | `INTERFACE / PROTOCOL READY` |
| Flow Matching | `INTERFACE / PROTOCOL READY` |
| Robot Policy | `INTERFACE / PROTOCOL READY` |
| End-to-end matched benchmark | `TODO` |

## Rule

Do not claim transfer performance until the target decoder has:

1. a candidate adapter;
2. a validated consequence representation;
3. fixed-budget matched baseline;
4. endpoint metric;
5. selected-vs-oracle or equivalent conversion audit.

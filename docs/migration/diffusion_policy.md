# Diffusion Policy Migration

Diffusion policies naturally generate multiple action samples, but raw noise
vectors or noisy intermediate states are not automatically valid
consequence-redundancy representations.

## Interface

```text
condition
-> diffusion sampler at fixed budget K
-> clean action / trajectory candidates
-> consequence encoder
-> relation matrix
-> capacity calibration
-> endpoint validation
```

## Required Adapter

The adapter must expose clean candidate actions:

```python
candidate = diffusion_adapter.sample_clean(condition, budget=K)
```

It must not treat diffusion noise alone as the consequence relation unless an
invariance or endpoint-predictiveness test supports that choice.

## Validation Gate

Before claiming a diffusion transfer result:

- compare against the same diffusion policy without AMC calibration;
- keep the candidate budget fixed;
- report selected endpoint quality;
- audit whether oracle opportunity and selector conversion align;
- document the sampler, timestep schedule, checkpoint, and evaluator.

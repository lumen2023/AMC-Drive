# Flow Matching Migration

Flow Matching models a probability transport path through a learned vector
field. For AMC-Drive migration, the important object is not the vector field by
itself, but the fixed set of decoded candidate actions that enter the endpoint
selector.

## Interface

```text
condition
-> flow-matching sampler at fixed budget K
-> decoded candidate actions
-> consequence representation
-> pairwise relation
-> capacity calibration
-> endpoint validation
```

## Adapter Requirements

The adapter must record:

- integration horizon;
- solver settings;
- sampling budget;
- decoded clean action tensor shape;
- whether candidate identities are persistent slots or stochastic samples.

## Validation Gate

A Flow Matching transfer claim requires a model-family-specific validation. Do
not reuse AC-JEPA assumptions without checking whether the flow representation
predicts endpoint-relevant consequence differences.

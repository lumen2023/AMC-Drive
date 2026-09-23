# AMC-Drive Release Status

| Module | Status |
| --- | --- |
| NAVSIM v1 proposal-based planner | `AVAILABLE` |
| V1 checkpoint | `AVAILABLE via Hugging Face` |
| V1 submission script | `AVAILABLE` |
| NAVSIM v1 score package | `AVAILABLE` |
| NAVSIM v2 full release | `TODO: V2` |
| HUGSIM full training/release | `TODO: HUGSIM` |
| Diffusion Policy adapter | `INTERFACE / PROTOCOL READY` |
| Flow Matching adapter | `INTERFACE / PROTOCOL READY` |
| Robot policy adapter | `INTERFACE / PROTOCOL READY` |
| Full cross-domain benchmark | `TODO: matched validation` |

## Public V1 Boundary

V1 is a NAVSIM v1 release. It includes an inference/deployment overlay,
submission script, checkpoint checksum, and score evidence.

V1 does not claim that all future migration targets are already fully trained
or benchmarked. Migration targets are exposed as interfaces and validation
protocols so that later releases can add implementation and evidence without
rewriting the V1 planner.

## Positive but Safe Wording

Use:

```text
AMC-Drive is released first as a verified automotive V1 implementation.
Its consequence-aware interface is organized to support later migration to
diffusion, flow-matching, and robot-policy decoders.
Those migrations are staged as explicit adapters with endpoint validation
rather than being conflated with the V1 NAVSIM result.
```

Avoid:

```text
AMC-Drive has already solved DM/FM/robot transfer.
AMC-Drive universally improves every planner endpoint.
The frozen representation is a ground-truth consequence oracle.
```

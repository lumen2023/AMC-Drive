# V1 Scope and TODO

## Included in V1

- NAVSIM v1 proposal-based AMC-Drive planner.
- Fixed `K=32` candidate trajectory interface.
- NAVSIM v1 overlay for standard devkit installation.
- Pretrained V1 checkpoint distribution via Hugging Face.
- NAVSIM v1 submission-pickle generation script.
- V1 score summary and checkpoint checksum.
- Decoder-agnostic migration contracts for later DM/FM/robot releases.

## Not Included in V1

- NAVSIM v2 full checkpoint and evaluator manifest.
- HUGSIM full training and model-release process.
- End-to-end Diffusion Policy adapter benchmark.
- End-to-end Flow Matching adapter benchmark.
- Robot-policy benchmark results.
- Git-tracked large checkpoint binaries.

## TODO

- Add NAVSIM v2 release package with checkpoint, evaluator, and exact command.
- Add HUGSIM release package with no-fine-tuning provenance and evaluator hash.
- Add model-family-specific adapter implementations for Diffusion Policy and
  Flow Matching.
- Add robot-policy endpoint validation on task success, collision, constraint,
  and control-cost metrics.
- Add cross-domain matched validation before claiming transfer performance.

# Migration Validation Protocol

Use this protocol before claiming AMC-Drive works in a new decoder family.

## 1. Candidate Contract

The adapter must return explicit fixed-budget candidates:

```text
[B, K, T, D]
```

`K` must be fixed across the matched baseline and AMC variant.

## 2. Representation Contract

The consequence representation must be candidate-conditioned and endpoint
relevant. A representation is not valid merely because it exists inside the
decoder.

## 3. Relation Contract

The relation matrix must compare candidates within the same condition only:

```text
[B, K, K]
```

Cross-scene or cross-time leakage invalidates the redundancy measurement.

## 4. Endpoint Contract

Report the selected endpoint, not only oracle or proxy metrics. If possible,
report:

```text
selected score
oracle score
gap = oracle - selected
```

## 5. Claim Labels

Use:

```text
INTERFACE_READY
ADAPTER_READY
ENDPOINT_SMOKE_PASS
MATCHED_TRANSFER_SUPPORTED
```

Avoid:

```text
TRANSFER_SOLVED
UNIVERSAL_IMPROVEMENT
ORACLE_DEPLOYED
```

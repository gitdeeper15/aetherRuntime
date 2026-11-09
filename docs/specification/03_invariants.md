# AetherRuntime v2.0.0 — Invariants Specification

**Version:** 2.0.0
**Status:** Operational Specification
**Basis:** AetherRuntime v0.1.0 (DOI: 10.5281/zenodo.24078477)
**Date:** 2026-11-09

---

## Overview

This document defines the **47 invariants** that AetherRuntime must preserve. Each invariant is a property that must hold in all valid states of the system. The invariants are the basis for the 60 tests (see `05_test_design.md`).

**Scope:** 47 invariants — 35 structural, 7 operational, 5 cross-cutting.

**Convention:** An invariant is violated if there exists any reachable state in which it does not hold.

---

## Part 1 — Structural Invariants (35)

### Identity (I1–I8)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I1** | `agent_id` is unique across the ecosystem | Monitoring | T01 |
| **I2** | `public_key` is a valid Ed25519 public key (32 bytes, valid curve point) | Monitoring | T02 |
| **I3** | `status` is one of: `idle`, `running`, `anomalous`, `contained`, `halted`, `recovering` | Monitoring | T03 |
| **I4** | `telemetry_id` is unique across the ecosystem | Monitoring | T04 |
| **I5** | `value` is finite (not NaN, not Inf) | Monitoring | T05 |
| **I6** | `timestamp` is monotonic per agent (strictly increasing) | Monitoring | T06 |
| **I7** | `sample_count >= 10` for every `Baseline` | Detection | T07 |
| **I8** | `parameters` contains all required keys for `model_type` | Detection | T08 |

### Detection (I9–I13)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I9** | `confidence` ∈ [0.0, 1.0] for every `AnomalyAlert` | Detection | T09 |
| **I10** | `telemetry_id` refers to an existing `TelemetryRecord` | Detection | T10 |
| **I11** | `level` is one of: `L1_throttle`, `L2_isolate`, `L3_quarantine`, `L4_freeze` | Containment | T11 |
| **I12** | `expiry > created_at` for every `ContainmentPolicy` | Containment | T12 |
| **I13** | `restrictions` contains all required keys for `level` | Containment | T13 |

### Halt (I14–I20)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I14** | `proposer_signature` verifies against `proposer`'s public key | Halt | T14 |
| **I15** | `quorum_threshold` ∈ [0.5, 1.0] | Halt | T15 |
| **I16** | `enforced_at` is set iff `approvals` count / total ≥ `quorum_threshold` | Halt | T16 |
| **I17** | `Δt_window = enforced_at - created_at > 0` (Proposition 2) | Halt | T17 |
| **I18** | `signature` verifies against `approver`'s public key | Halt | T18 |
| **I19** | `approval_id` is unique across the ecosystem | Halt | T19 |
| **I20** | An approver cannot approve the same halt twice | Halt | T20 |

### Recovery (I21–I26)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I21** | `verification_result` is `True` before agent is marked `running` | Recovery | T21 |
| **I22** | `snapshot_id` refers to an existing `Snapshot` | Recovery | T22 |
| **I23** | `reauthorized_by` is an authorized agent (via AetherGovern) | Recovery | T23 |
| **I24** | `hash` matches SHA-256 of `state` for every `Snapshot` | Recovery | T24 |
| **I25** | `stored_at` refers to an existing AetherGit record | Recovery | T25 |
| **I26** | `snapshot_id` is unique across the ecosystem | Recovery | T26 |

### Configuration (I27–I29)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I27** | `anomaly_threshold > 0` | Configuration | T27 |
| **I28** | `halt_quorum` ∈ [0.5, 1.0] | Configuration | T28 |
| **I29** | `telemetry_rate_hz > 0` | Configuration | T29 |

### Cross-Entity (I30–I35)

| ID | Invariant | Layer | Test |
|:-:|---|---|:-:|
| **I30** | Every `AnomalyAlert` references an existing `Agent` and `TelemetryRecord` | Detection | T30 |
| **I31** | Every `ContainmentPolicy` references an existing `AnomalyAlert` | Containment | T31 |
| **I32** | Every `HaltOrder` has at least one `HaltApproval` before enforcement | Halt | T32 |
| **I33** | Every `RecoveryRecord` follows a `HaltOrder` | Recovery | T33 |
| **I34** | Every `Agent` has at least one `Baseline` before detection | Detection | T34 |
| **I35** | Every `HaltOrder` enforces across all honest nodes (Proposition 1) | Halt | T35 |

---

## Part 2 — Operational Invariants (7)

These invariants concern the operations themselves.

| ID | Invariant | Operation | Test |
|:-:|---|---|:-:|
| **O1** | `collect` produces a `TelemetryRecord` with a unique `telemetry_id` | `collect` | T36 |
| **O2** | `update_baseline` requires `window_size >= 10` and `sample_count >= window_size` | `update_baseline` | T37 |
| **O3** | `detect` is deterministic (Proposition 1) — the verdict depends only on local state | `detect` | T38 |
| **O4** | `contain` requires `confidence >= threshold` and `expiry > created_at` | `contain` | T39 |
| **O5** | `propose_halt` requires `proposer_signature` to verify | `propose_halt` | T40 |
| **O6** | `approve_halt` cannot be performed twice by the same approver for the same halt | `approve_halt` | T41 |
| **O7** | `recover` requires `verification_result = True` before resumption | `recover` | T42 |

---

## Part 3 — Cross-Cutting Invariants (5)

These invariants span multiple layers.

| ID | Invariant | Layers | Test |
|:-:|---|---|:-:|
| **X1** | Every admitted action has a traceable authority chain (via AetherGovern) | Halt, Recovery | T43 |
| **X2** | Every halt order has `Δt_window > 0` (Proposition 2) | Halt | T44 |
| **X3** | Every detection verdict is reproducible from the local state (Proposition 1) | Detection | T45 |
| **X4** | Every recovery produces a `RecoveryRecord` with `verification_result = True` | Recovery | T46 |
| **X5** | Every containment policy is reversible (expiry or manual reversal) | Containment | T47 |

---

## Invariant Classification

### By Category

| Category | Count | IDs |
|---|:-:|---|
| Identity | 8 | I1–I8 |
| Detection | 5 | I9–I13 |
| Halt | 7 | I14–I20 |
| Recovery | 6 | I21–I26 |
| Configuration | 3 | I27–I29 |
| Cross-Entity | 6 | I30–I35 |
| Operational | 7 | O1–O7 |
| Cross-Cutting | 5 | X1–X5 |
| **Total** | **47** | |

### By Layer

| Layer | Count | IDs |
|---|:-:|---|
| Monitoring | 8 | I1–I8 |
| Detection | 6 | I9–I10, I30, I34, O3, X3 |
| Containment | 5 | I11–I13, I31, X5 |
| Halt | 10 | I14–I20, I32, I35, X2 |
| Recovery | 8 | I21–I26, I33, X1 |
| Configuration | 3 | I27–I29 |
| Operational | 7 | O1–O7 |
| **Total** | **47** | |

### By Testability

| Type | Count | IDs |
|---|:-:|---|
| Structural (unit test) | 35 | I1–I35 |
| Operational (integration test) | 7 | O1–O7 |
| Cross-cutting (system test) | 5 | X1–X5 |
| **Total** | **47** | |

---

## Invariant Interactions

Some invariants are **independent**, some are **dependent**.

### Dependencies

| Invariant | Depends on |
|---|---|
| I10 | I4 (telemetry_id unique) |
| I16 | I15 (quorum_threshold valid) |
| I17 | I16 (enforced_at set) |
| I21 | I22, I23 (snapshot, reauthorizer valid) |
| I32 | I16, I17 (halt quorum and window) |
| I35 | I16, I17, X2 (halt enforcement) |
| X1 | I23, O7 (reauthorizer valid) |
| X2 | I17, I32 (halt window > 0) |
| X3 | O3 (detect deterministic) |
| X4 | I21, O7 (recovery verified) |

### Conflicts

No conflicts identified. All 47 invariants are consistent.

---

## Verification Strategy

Each invariant is verified by at least one test:

| Verification Type | Count | Tests |
|---|:-:|---|
| Unit test | 35 | T01–T35 |
| Integration test | 7 | T36–T42 |
| System test | 5 | T43–T47 |
| **Total** | **47** | |

**Coverage:** 100% of invariants have at least one test.

---

## Formal Statement

For each invariant `I`, the system `S` satisfies `I` if:

```

∀ state ∈ Reachable(S): I(state) = True

```

An invariant is **violated** if:

```

∃ state ∈ Reachable(S): I(state) = False

```

The test suite `T` is **complete** if:

```

∀ I ∈ Invariants: ∃ t ∈ T: t verifies I

```

---

## Implementation Notes

### For `src/aetherruntime/`

Each invariant is checked by:
1. **Precondition checks** at the start of each operation.
2. **Postcondition checks** at the end of each operation.
3. **Invariant checks** in a `verify()` function (CLI: `aetherruntime verify`).

### For `tests/`

Each invariant is tested by:
- **Unit test** for structural invariants (I1–I35).
- **Integration test** for operational invariants (O1–O7).
- **System test** for cross-cutting invariants (X1–X5).

---

## Next Document

- `04_interfaces.md` — Interfaces with Aether family
- `05_test_design.md` — Test design for 60 tests

---

**Document Status:** Complete
**Version:** 2.0.0
**Date:** 2026-11-09

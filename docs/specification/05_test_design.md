# AetherRuntime v2.0.0 — Test Design

**Version:** 2.0.0
**Status:** Operational Specification
**Basis:** AetherRuntime v0.1.0 (DOI: 10.5281/zenodo.24078477)
**Date:** 2026-11-09

---

## Overview

This document specifies the **60 tests** that verify AetherRuntime's implementation against the 47 invariants (see `03_invariants.md`). Each test has a defined input, expected output, success condition, and the invariant it verifies.

**Scope:** 60 tests across 7 files.

---

## Test Files

| # | File | Tests | Scope |
|:-:|---|:-:|---|
| 1 | `test_models.py` | 10 | Structural invariants (I1–I10) |
| 2 | `test_monitoring.py` | 8 | Monitoring (I1–I8, O1–O2) |
| 3 | `test_detection.py` | 8 | Detection (I9–I10, I30, I34, O3, X3) |
| 4 | `test_containment.py` | 8 | Containment (I11–I13, I31, X5) |
| 5 | `test_halt.py` | 8 | Halt (I14–I20, I32, I35, O5–O6, X2) |
| 6 | `test_recovery.py` | 8 | Recovery (I21–I26, I33, O7, X1) |
| 7 | `test_simulation.py` | 10 | Simulation (integration) |
| **Total** | **7** | **60** | |

---

## Test 1–10: `test_models.py` (Structural)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T01 | `test_agent_id_unique` | I1 | Two agents with same `agent_id` | `ValueError` | Raises |
| T02 | `test_public_key_valid` | I2 | Invalid Ed25519 key (16 bytes) | `ValueError` | Raises |
| T03 | `test_status_enum` | I3 | Agent with `status="unknown"` | `ValueError` | Raises |
| T04 | `test_telemetry_id_unique` | I4 | Two telemetry records with same `telemetry_id` | `ValueError` | Raises |
| T05 | `test_value_finite` | I5 | Telemetry with `value=float("nan")` | `ValueError` | Raises |
| T06 | `test_timestamp_monotonic` | I6 | Two records with `t2 < t1` | `ValueError` | Raises |
| T07 | `test_baseline_sample_count` | I7 | Baseline with `sample_count=5` | `ValueError` | Raises |
| T08 | `test_baseline_parameters` | I8 | Baseline with missing `mean` | `ValueError` | Raises |
| T09 | `test_alert_confidence` | I9 | Alert with `confidence=1.5` | `ValueError` | Raises |
| T10 | `test_alert_telemetry_ref` | I10 | Alert with non-existent `telemetry_id` | `ValueError` | Raises |

---

## Test 11–18: `test_monitoring.py` (Monitoring)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T11 | `test_collect_creates_record` | O1 | Valid telemetry input | `TelemetryRecord` | Record created |
| T12 | `test_collect_agent_not_running` | E2 | Agent in `idle` state | `AgentNotRunning` | Raises |
| T13 | `test_update_baseline_window` | O2 | `window_size=5` | `InvalidWindowSize` | Raises |
| T14 | `test_update_baseline_insufficient` | E6 | 5 records, `window_size=10` | `InsufficientTelemetry` | Raises |
| T15 | `test_baseline_mean_std` | I8 | 10 records | Baseline with mean/std | Computed |
| T16 | `test_baseline_zscore` | I8 | 10 records | Baseline with mean/std | Computed |
| T17 | `test_telemetry_metadata` | — | Record with metadata | Preserved | ✅ |
| T18 | `test_telemetry_categories` | — | All 5 categories | Accepted | ✅ |

---

## Test 19–26: `test_detection.py` (Detection)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T19 | `test_detect_anomaly` | O3 | Telemetry > threshold | `AnomalyAlert` | Created |
| T20 | `test_detect_no_anomaly` | O3 | Telemetry < threshold | `None` | No alert |
| T21 | `test_detect_deterministic` | X3 | Same input twice | Same verdict | ✅ |
| T22 | `test_detect_no_baseline` | E9 | No baseline | `BaselineNotFound` | Raises |
| T23 | `test_alert_confidence_range` | I9 | Confidence 0.0–1.0 | Accepted | ✅ |
| T24 | `test_alert_references_valid` | I30 | Alert with valid refs | Accepted | ✅ |
| T25 | `test_agent_has_baseline` | I34 | Detect without baseline | `BaselineNotFound` | Raises |
| T26 | `test_detect_multiple_categories` | — | 5 categories | 5 alerts (or none) | ✅ |

---

## Test 27–34: `test_containment.py` (Containment)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T27 | `test_contain_l1` | I11 | Level L1 | Policy created | ✅ |
| T28 | `test_contain_l4` | I11 | Level L4 | Policy created | ✅ |
| T29 | `test_contain_invalid_level` | E12 | Level L5 | `InvalidLevel` | Raises |
| T30 | `test_contain_expiry_future` | I12 | `expiry > created_at` | Accepted | ✅ |
| T31 | `test_contain_expiry_past` | E13 | `expiry < created_at` | `ExpiryInPast` | Raises |
| T32 | `test_contain_restrictions` | I13 | All required keys | Accepted | ✅ |
| T33 | `test_contain_missing_restrictions` | I13 | Missing `cpu` | `ValueError` | Raises |
| T34 | `test_contain_reversible` | X5 | Apply then lift | Reverted | ✅ |

---

## Test 35–42: `test_halt.py` (Halt)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T35 | `test_propose_halt` | O5 | Valid signature | `HaltOrder` | Created |
| T36 | `test_propose_halt_invalid_sig` | E17 | Invalid signature | `InvalidSignature` | Raises |
| T37 | `test_approve_halt` | O6 | Valid approval | `HaltApproval` | Created |
| T38 | `test_approve_halt_twice` | I20 | Same approver twice | `ValueError` | Raises |
| T39 | `test_halt_quorum_threshold` | I15 | Quorum 0.67 | Accepted | ✅ |
| T40 | `test_halt_quorum_invalid` | I15 | Quorum 0.3 | `ValueError` | Raises |
| T41 | `test_halt_enforced_at` | I16 | Quorum reached | `enforced_at` set | ✅ |
| T42 | `test_halt_window_positive` | I17 | Enforced | `Δt_window > 0` | ✅ |

---

## Test 43–50: `test_recovery.py` (Recovery)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T43 | `test_recover_valid` | O7 | Valid halt + snapshot | `RecoveryRecord` | Created |
| T44 | `test_recover_not_halted` | E19 | Agent in `running` | `AgentNotHalted` | Raises |
| T45 | `test_recover_snapshot_invalid` | E20 | Non-existent snapshot | `SnapshotNotFound` | Raises |
| T46 | `test_recover_unauthorized` | E21 | Unauthorized reauthorizer | `UnauthorizedReauthorizer` | Raises |
| T47 | `test_recover_verification` | I21 | Verification passes | `True` | ✅ |
| T48 | `test_recover_verification_fail` | E22 | Verification fails | `VerificationFailed` | Raises |
| T49 | `test_snapshot_hash` | I24 | Snapshot created | `hash` matches | ✅ |
| T50 | `test_snapshot_stored_at` | I25 | Snapshot stored | Valid ref | ✅ |

---

## Test 51–60: `test_simulation.py` (Simulation)

| # | Test | Invariant | Input | Expected | Success |
|:-:|---|---|---|---|---|
| T51 | `test_network_creation` | — | 10 nodes | `Network` created | ✅ |
| T52 | `test_node_creation` | — | Valid agent | `Node` created | ✅ |
| T53 | `test_testbed_run` | — | 10 nodes, 10 steps | Completed | ✅ |
| T54 | `test_convergence` | I35 | 10 nodes, same input | Same verdict | ✅ |
| T55 | `test_halt_propagation` | X2 | Halt order broadcast | All nodes halted | ✅ |
| T56 | `test_quarantine` | — | L3 containment | Agent quarantined | ✅ |
| T57 | `test_freeze` | — | L4 containment | Agent frozen | ✅ |
| T58 | `test_network_partition` | — | Partition | Stated behavior | ✅ |
| T59 | `test_halt_quorum_partition` | — | Partition + quorum | Correct | ✅ |
| T60 | `test_recovery_after_halt` | — | Halt + recover | Agent resumed | ✅ |

---

## Test Coverage Summary

### By File

| File | Tests | Invariants Covered |
|---|:-:|---|
| `test_models.py` | 10 | I1–I10 |
| `test_monitoring.py` | 8 | I1–I8, O1–O2 |
| `test_detection.py` | 8 | I9–I10, I30, I34, O3, X3 |
| `test_containment.py` | 8 | I11–I13, I31, X5 |
| `test_halt.py` | 8 | I14–I20, I32, I35, O5–O6, X2 |
| `test_recovery.py` | 8 | I21–I26, I33, O7, X1 |
| `test_simulation.py` | 10 | Integration |
| **Total** | **60** | **47 invariants** |

### By Invariant Type

| Type | Tests | Invariants |
|---|:-:|---|
| Structural (I) | 35 | I1–I35 |
| Operational (O) | 7 | O1–O7 |
| Cross-cutting (X) | 5 | X1–X5 |
| Integration | 13 | CI1–CI5, E1–E22 |
| **Total** | **60** | **47** |

---

## Test Execution Plan

### Phase 1: Unit Tests (T01–T50)

**Run:** `pytest tests/test_models.py tests/test_monitoring.py tests/test_detection.py tests/test_containment.py tests/test_halt.py tests/test_recovery.py -v`

**Expected:** 50 passed in ~5 seconds.

### Phase 2: Integration Tests (T51–T60)

**Run:** `pytest tests/test_simulation.py -v`

**Expected:** 10 passed in ~30 seconds.

### Phase 3: Coverage Report

**Run:** `pytest --cov=src/aetherruntime --cov-report=html`

**Expected:** Coverage ≥ 80%.

---

## Test Fixtures (`conftest.py`)

The following fixtures are used across tests:

| Fixture | Purpose |
|---|---|
| `mock_agent` | A mock Agent with valid `agent_id`, `public_key` |
| `mock_telemetry` | A mock TelemetryRecord |
| `mock_baseline` | A mock Baseline with 10 samples |
| `mock_alert` | A mock AnomalyAlert |
| `mock_halt_order` | A mock HaltOrder with 1 approval |
| `mock_snapshot` | A mock Snapshot with valid hash |
| `mock_network` | A mock Network with 10 nodes |

---

## Test Design Principles

1. **One assertion per test** — Each test verifies one invariant.
2. **Deterministic** — No randomness; use seeds.
3. **Fast** — Unit tests < 100ms; integration < 5s.
4. **Independent** — No test depends on another.
5. **Descriptive names** — `test_<invariant>_<scenario>`.

---

## Expected Test Outcomes

| Phase | Tests | Expected |
|---|:-:|---|
| Unit | 50 | 50 passed |
| Integration | 10 | 10 passed |
| **Total** | **60** | **60 passed** |

**Pass rate:** 100% required for v2.0.0 release.

---

## Test → Invariant Mapping

| Invariant | Test(s) |
|---|---|
| I1–I10 | T01–T10, T23 |
| I11–I13 | T27–T34 |
| I14–I20 | T35–T42 |
| I21–I26 | T43–T50 |
| I27–I29 | T01–T10 |
| I30–I35 | T24, T32, T41, T49 |
| O1–O7 | T11–T13, T19–T20, T35–T37, T43 |
| X1–X5 | T21, T34, T42, T47, T55 |

**Coverage:** 100% of invariants have at least one test.

---

## Next Steps

1. Implement `src/aetherruntime/` (15 modules) — see `01_entities.md` and `02_operations.md`.
2. Implement `tests/` (60 tests) — see this document.
3. Run `pytest` — expect 60 passed.
4. Run experiments — see `experiments/`.
5. Write `REPORTS/v2.0.0/report.md`.

---

**Document Status:** Complete
**Version:** 2.0.0
**Date:** 2026-11-09

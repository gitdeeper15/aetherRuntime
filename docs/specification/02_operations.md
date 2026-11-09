# AetherRuntime v2.0.0 — Operations Specification

**Version:** 2.0.0
**Status:** Operational Specification
**Basis:** AetherRuntime v0.1.0 (DOI: 10.5281/zenodo.24078477)
**Date:** 2026-11-09

---

## Overview

This document defines the **seven operations** that AetherRuntime performs. Each operation is a function with defined inputs, outputs, preconditions, postconditions, and error conditions. The operations correspond to the five-layer architecture (Monitoring, Detection, Containment, Halt, Recovery).

**Scope:** 7 operations, 28 inputs, 19 error conditions.

---

## Operation 1 — `collect`

**Layer:** Monitoring (Layer 1)

**Purpose:** Collect a telemetry record from a running agent.

**Signature:**
```

collect(agent_id, category, value, timestamp, metadata?) → TelemetryRecord

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `agent_id` | string | ✅ | Target agent |
| 2 | `category` | enum | ✅ | One of: cpu, memory, network, syscall, action |
| 3 | `value` | float | ✅ | Numeric value |
| 4 | `timestamp` | ISO 8601 | ✅ | Logical time of observation |
| 5 | `metadata` | dict | ❌ | Optional metadata |

**Outputs:**
- `TelemetryRecord` — The created record.

**Preconditions:**
- P1: Agent exists and is in state `running`.
- P2: `value` is finite.
- P3: `timestamp` is monotonic per agent.

**Postconditions:**
- Q1: A new `TelemetryRecord` is created with a unique `telemetry_id`.
- Q2: The record is appended to the agent's telemetry log.
- Q3: I5 and I6 hold.

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E1 | `AgentNotFound` | `agent_id` does not exist |
| E2 | `AgentNotRunning` | Agent status ≠ `running` |
| E3 | `InvalidValue` | `value` is NaN or Inf |
| E4 | `NonMonotonicTimestamp` | `timestamp` < previous timestamp |

---

## Operation 2 — `update_baseline`

**Layer:** Monitoring (Layer 1)

**Purpose:** Update the baseline model for an agent's telemetry category.

**Signature:**
```

update_baseline(agent_id, category, model_type, window_size) → Baseline

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `agent_id` | string | ✅ | Target agent |
| 2 | `category` | enum | ✅ | Telemetry category |
| 3 | `model_type` | enum | ✅ | One of: mean_std, zscore, moving_average, seasonal |
| 4 | `window_size` | int | ✅ | Number of recent telemetry records to use |

**Outputs:**
- `Baseline` — The updated baseline.

**Preconditions:**
- P1: Agent exists.
- P2: `window_size >= 10`.
- P3: At least `window_size` telemetry records exist for the (agent, category) pair.

**Postconditions:**
- Q1: A new `Baseline` is created (or the existing one is updated).
- Q2: I7 and I8 hold.
- Q3: `computed_at` is set to current timestamp.

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E5 | `AgentNotFound` | `agent_id` does not exist |
| E6 | `InsufficientTelemetry` | Fewer than `window_size` records |
| E7 | `InvalidWindowSize` | `window_size < 10` |

---

## Operation 3 — `detect`

**Layer:** Detection (Layer 2)

**Purpose:** Compare a telemetry record against the baseline and flag deviations.

**Signature:**
```

detect(telemetry_id, baseline_id?) → AnomalyAlert | None

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `telemetry_id` | string | ✅ | Telemetry record to evaluate |
| 2 | `baseline_id` | string | ❌ | Baseline to use (auto-selected if omitted) |

**Outputs:**
- `AnomalyAlert` — If anomaly detected.
- `None` — If no anomaly.

**Preconditions:**
- P1: `telemetry_id` exists.
- P2: A baseline exists for the (agent, category) pair.
- P3: The anomaly predicate is deterministic (Proposition 1).

**Postconditions:**
- Q1: If anomalous, a new `AnomalyAlert` is created.
- Q2: I9 and I10 hold.
- Q3: The verdict is a deterministic function of the local state (Proposition 1).

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E8 | `TelemetryNotFound` | `telemetry_id` does not exist |
| E9 | `BaselineNotFound` | No baseline for the (agent, category) pair |
| E10 | `NonDeterministic` | Anomaly predicate depends on non-local state |

---

## Operation 4 — `contain`

**Layer:** Containment (Layer 3)

**Purpose:** Apply a containment policy to an anomalous agent.

**Signature:**
```

contain(alert_id, level, restrictions, expiry) → ContainmentPolicy

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `alert_id` | string | ✅ | Reference to `AnomalyAlert` |
| 2 | `level` | enum | ✅ | One of: L1_throttle, L2_isolate, L3_quarantine, L4_freeze |
| 3 | `restrictions` | dict | ✅ | Resource limits |
| 4 | `expiry` | ISO 8601 | ✅ | When containment expires |

**Outputs:**
- `ContainmentPolicy` — The applied policy.

**Preconditions:**
- P1: `alert_id` exists and has `confidence >= threshold`.
- P2: `expiry > created_at`.
- P3: Agent is not already contained at a higher level.

**Postconditions:**
- Q1: A new `ContainmentPolicy` is created.
- Q2: I11, I12, I13 hold.
- Q3: The agent's status is updated to `contained`.

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E11 | `AlertNotFound` | `alert_id` does not exist |
| E12 | `InvalidLevel` | `level` not in {L1, L2, L3, L4} |
| E13 | `ExpiryInPast` | `expiry <= created_at` |
| E14 | `AlreadyContained` | Agent already contained at higher level |

---

## Operation 5 — `propose_halt`

**Layer:** Halt (Layer 4)

**Purpose:** Propose a halt order for a compromised agent.

**Signature:**
```

propose_halt(agent_id, reason, proposer_signature) → HaltOrder

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `agent_id` | string | ✅ | Target agent |
| 2 | `reason` | string | ✅ | Human-readable reason |
| 3 | `proposer_signature` | bytes | ✅ | Ed25519 signature (64 bytes) |

**Outputs:**
- `HaltOrder` — The proposed halt order.

**Preconditions:**
- P1: Agent exists.
- P2: Proposer is authorized (via AetherGovern).
- P3: `proposer_signature` verifies.

**Postconditions:**
- Q1: A new `HaltOrder` is created with `enforced_at = None`.
- Q2: The halt order is broadcast to all authorized nodes.
- Q3: I14, I15, I16 hold.

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E15 | `AgentNotFound` | `agent_id` does not exist |
| E16 | `UnauthorizedProposer` | Proposer is not authorized |
| E17 | `InvalidSignature` | `proposer_signature` does not verify |

---

## Operation 6 — `approve_halt`

**Layer:** Halt (Layer 4)

**Purpose:** Approve a halt order, contributing to the quorum.

**Signature:**
```

approve_halt(halt_id, approver_signature) → HaltApproval

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `halt_id` | string | ✅ | Reference to `HaltOrder` |
| 2 | `approver_signature` | bytes | ✅ | Ed25519 signature (64 bytes) |

**Outputs:**
- `HaltApproval` — The approval record.

**Preconditions:**
- P1: `halt_id` exists.
- P2: Approver is authorized.
- P3: Approver has not already approved this halt.
- P4: `approver_signature` verifies.

**Postconditions:**
- Q1: A new `HaltApproval` is created.
- Q2: If approvals count / total ≥ `quorum_threshold`, `enforced_at` is set.
- Q3: I17, I18, I19, I20 hold.
- Q4: `Δt_window = enforced_at - created_at > 0` (Proposition 2).

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E18 | `HaltNotFound` | `halt_id` does not exist |
| E19 | `InvalidSignature` | `approver_signature` does not verify |

---

## Operation 7 — `recover`

**Layer:** Recovery (Layer 5)

**Purpose:** Recover a halted agent to a known-good state.

**Signature:**
```

recover(agent_id, halt_id, snapshot_id, reauthorized_by) → RecoveryRecord

```

**Inputs:**
| # | Name | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `agent_id` | string | ✅ | Target agent |
| 2 | `halt_id` | string | ✅ | Reference to `HaltOrder` |
| 3 | `snapshot_id` | string | ✅ | Reference to `Snapshot` |
| 4 | `reauthorized_by` | string | ✅ | Agent re-authorizing recovery |

**Outputs:**
- `RecoveryRecord` — The recovery record.

**Preconditions:**
- P1: Agent is in state `halted`.
- P2: `halt_id` exists and is enforced.
- P3: `snapshot_id` exists.
- P4: `reauthorized_by` is authorized (via AetherGovern).

**Postconditions:**
- Q1: A new `RecoveryRecord` is created.
- Q2: `verification_result = True` before agent is marked as `running`.
- Q3: I21, I22, I23 hold.
- Q4: Agent status is updated to `recovering`, then `running` (if verified).

**Error conditions:**
| ID | Error | Cause |
|---|---|---|
| E19 | `AgentNotHalted` | Agent status ≠ `halted` |
| E20 | `SnapshotNotFound` | `snapshot_id` does not exist |
| E21 | `UnauthorizedReauthorizer` | `reauthorized_by` not authorized |
| E22 | `VerificationFailed` | Recovered state does not match spec |

---

## Operation Summary

| # | Operation | Layer | Inputs | Errors |
|:-:|---|---|:-:|:-:|
| 1 | `collect` | Monitoring | 5 | 4 |
| 2 | `update_baseline` | Monitoring | 4 | 3 |
| 3 | `detect` | Detection | 2 | 3 |
| 4 | `contain` | Containment | 4 | 4 |
| 5 | `propose_halt` | Halt | 3 | 3 |
| 6 | `approve_halt` | Halt | 2 | 2 |
| 7 | `recover` | Recovery | 4 | 4 |
| **Total** | **7** | **5** | **24** | **23** |

---

## Input Count Summary

| Operation | Inputs |
|---|:-:|
| `collect` | 5 |
| `update_baseline` | 4 |
| `detect` | 2 |
| `contain` | 4 |
| `propose_halt` | 3 |
| `approve_halt` | 2 |
| `recover` | 4 |
| **Total** | **24** |

---

## Error Count Summary

| Operation | Errors |
|---|:-:|
| `collect` | 4 |
| `update_baseline` | 3 |
| `detect` | 3 |
| `contain` | 4 |
| `propose_halt` | 3 |
| `approve_halt` | 2 |
| `recover` | 4 |
| **Total** | **23** |

---

## Cross-Operation Invariants

- O1: Every operation respects the layer ordering: collect → update_baseline → detect → contain → propose_halt → approve_halt → recover.
- O2: Every operation produces a record that satisfies the structural invariants (I1–I35).
- O3: Every halt operation has `Δt_window > 0` (Proposition 2).
- O4: Every recovery operation has `verification_result = True` before resumption.
- O5: Every detection operation is deterministic (Proposition 1).

---

## Next Document

- `03_invariants.md` — Full invariant list
- `04_interfaces.md` — Interfaces with Aether family
- `05_test_design.md` — Test design for 60 tests

---

**Document Status:** Complete
**Version:** 2.0.0
**Date:** 2026-11-09

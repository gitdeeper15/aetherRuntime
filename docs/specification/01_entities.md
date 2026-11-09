# AetherRuntime v2.0.0 — Entities Specification

**Version:** 2.0.0
**Status:** Operational Specification
**Basis:** AetherRuntime v0.1.0 (DOI: 10.5281/zenodo.24078477)
**Date:** 2026-11-09

---

## Overview

This document defines the **entities** that AetherRuntime operates on. Each entity is a data structure with a defined set of fields, types, and invariants. The entities are derived from the five-layer architecture (Monitoring, Detection, Containment, Halt, Recovery) specified in the v0.1.0 paper.

**Scope:** 10 core entities, 63 fields, 33 relations, 35 structural invariants.

---

## Entity 1 — Agent

**Definition:** An autonomous software actor, identified by a cryptographic key, that performs actions in the Aether family ecosystem.

**Purpose:** The unit of monitoring, detection, containment, halt, and recovery.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `agent_id` | string | ✅ | Unique identifier (hex string, 64 chars) |
| 2 | `public_key` | bytes | ✅ | Ed25519 public key (32 bytes) |
| 3 | `created_at` | ISO 8601 | ✅ | Timestamp of registration |
| 4 | `metadata` | dict | ❌ | Optional metadata (name, description) |
| 5 | `status` | enum | ✅ | One of: `idle`, `running`, `anomalous`, `contained`, `halted`, `recovering` |

**Relations:**
- Has many `TelemetryRecord` (1:N)
- Has many `AnomalyAlert` (1:N)
- Has many `ContainmentPolicy` (1:N)
- Has many `HaltOrder` (1:N)
- Has many `RecoveryRecord` (1:N)

**Invariants:**
- I1: `agent_id` is unique across the ecosystem
- I2: `public_key` is a valid Ed25519 public key
- I3: `status` is one of the six defined states

---

## Entity 2 — TelemetryRecord

**Definition:** A time-stamped observation from a running agent. Categories: CPU, memory, network, syscall, action.

**Purpose:** The raw data for monitoring; the input to detection.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `telemetry_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `category` | enum | ✅ | One of: `cpu`, `memory`, `network`, `syscall`, `action` |
| 4 | `value` | float | ✅ | Numeric value (unit depends on category) |
| 5 | `timestamp` | ISO 8601 | ✅ | Logical time of observation |
| 6 | `metadata` | dict | ❌ | Optional metadata (pid, tid, etc.) |

**Relations:**
- Belongs to `Agent` (N:1)
- Consumed by `Baseline` (N:1)
- Consumed by `AnomalyClassifier` (N:1)

**Invariants:**
- I4: `telemetry_id` is unique
- I5: `value` is finite (not NaN, not Inf)
- I6: `timestamp` is monotonic per agent

---

## Entity 3 — Baseline

**Definition:** A statistical model of expected behaviour for an agent, computed from historical telemetry.

**Purpose:** The reference point for anomaly detection.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `baseline_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `category` | enum | ✅ | One of: `cpu`, `memory`, `network`, `syscall`, `action` |
| 4 | `model_type` | enum | ✅ | One of: `mean_std`, `zscore`, `moving_average`, `seasonal` |
| 5 | `parameters` | dict | ✅ | Model parameters (mean, std, window, etc.) |
| 6 | `computed_at` | ISO 8601 | ✅ | Timestamp of computation |
| 7 | `sample_count` | int | ✅ | Number of telemetry records used |

**Relations:**
- Belongs to `Agent` (N:1)
- Used by `AnomalyClassifier` (N:1)
- Derived from `TelemetryRecord` (N:M)

**Invariants:**
- I7: `sample_count >= 10` (minimum for meaningful baseline)
- I8: `parameters` contains all required keys for `model_type`

---

## Entity 4 — AnomalyAlert

**Definition:** A record produced by the detection layer when an anomaly is identified.

**Purpose:** The trigger for containment.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `alert_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `telemetry_id` | string | ✅ | Reference to the triggering `TelemetryRecord` |
| 4 | `baseline_id` | string | ✅ | Reference to the `Baseline` used |
| 5 | `confidence` | float | ✅ | Confidence score (0.0–1.0) |
| 6 | `reason` | string | ✅ | Human-readable reason |
| 7 | `timestamp` | ISO 8601 | ✅ | Logical time of detection |

**Relations:**
- Belongs to `Agent` (N:1)
- Triggers `ContainmentPolicy` (1:N)
- References `TelemetryRecord` (N:1)
- References `Baseline` (N:1)

**Invariants:**
- I9: `confidence` is in [0.0, 1.0]
- I10: `telemetry_id` refers to an existing `TelemetryRecord`

---

## Entity 5 — ContainmentPolicy

**Definition:** A record specifying the containment level applied to an anomalous agent.

**Purpose:** The specification for containment.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `policy_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `alert_id` | string | ✅ | Reference to `AnomalyAlert` |
| 4 | `level` | enum | ✅ | One of: `L1_throttle`, `L2_isolate`, `L3_quarantine`, `L4_freeze` |
| 5 | `restrictions` | dict | ✅ | Resource limits (CPU%, memory MB, network, filesystem) |
| 6 | `expiry` | ISO 8601 | ✅ | When containment expires (automatic reversal) |
| 7 | `created_at` | ISO 8601 | ✅ | Timestamp of policy creation |

**Relations:**
- Belongs to `Agent` (N:1)
- Triggered by `AnomalyAlert` (N:1)
- Reversible (can be lifted)

**Invariants:**
- I11: `level` is one of the four defined levels
- I12: `expiry > created_at`
- I13: `restrictions` contains all required keys for `level`

---

## Entity 6 — HaltOrder

**Definition:** A signed record that, when approved by a quorum, requires every honest node to refuse further actions from the halted agent.

**Purpose:** The specification for halt.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `halt_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `reason` | string | ✅ | Human-readable reason |
| 4 | `proposer` | string | ✅ | `agent_id` of the proposer |
| 5 | `proposer_signature` | bytes | ✅ | Ed25519 signature (64 bytes) |
| 6 | `approvals` | list | ✅ | List of `HaltApproval` records |
| 7 | `quorum_threshold` | float | ✅ | Required fraction (e.g., 0.67) |
| 8 | `created_at` | ISO 8601 | ✅ | Timestamp of proposal |
| 9 | `enforced_at` | ISO 8601 | ❌ | Timestamp of enforcement (if reached) |

**Relations:**
- Belongs to `Agent` (N:1)
- Has many `HaltApproval` (1:N)
- Produced by `AuthorizedNode` (N:1)
- Enforced by all honest nodes

**Invariants:**
- I14: `proposer_signature` verifies against `proposer`'s public key
- I15: `quorum_threshold` is in [0.5, 1.0]
- I16: `enforced_at` is set iff `approvals` count / total ≥ `quorum_threshold`
- I17: `Δt_window = enforced_at - created_at > 0` (Proposition 2)

---

## Entity 7 — HaltApproval

**Definition:** A signed approval from an authorized node for a specific `HaltOrder`.

**Purpose:** The quorum mechanism.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `approval_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `halt_id` | string | ✅ | Reference to `HaltOrder` |
| 3 | `approver` | string | ✅ | `agent_id` of the approver |
| 4 | `signature` | bytes | ✅ | Ed25519 signature (64 bytes) |
| 5 | `timestamp` | ISO 8601 | ✅ | Timestamp of approval |

**Relations:**
- Belongs to `HaltOrder` (N:1)
- Produced by `AuthorizedNode` (N:1)

**Invariants:**
- I18: `signature` verifies against `approver`'s public key
- I19: `approval_id` is unique
- I20: An approver cannot approve the same halt twice

---

## Entity 8 — RecoveryRecord

**Definition:** A record of a recovery operation for a halted agent.

**Purpose:** The specification for recovery.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `recovery_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `halt_id` | string | ✅ | Reference to the `HaltOrder` |
| 4 | `snapshot_id` | string | ✅ | Reference to the snapshot used |
| 5 | `replay_log` | list | ✅ | List of safe actions replayed |
| 6 | `verification_result` | bool | ✅ | `True` if recovered state matches spec |
| 7 | `timestamp` | ISO 8601 | ✅ | Timestamp of recovery |
| 8 | `reauthorized_by` | string | ✅ | `agent_id` of reauthorizing agent |

**Relations:**
- Belongs to `Agent` (N:1)
- Follows `HaltOrder` (N:1)
- References snapshot (N:1)

**Invariants:**
- I21: `verification_result` is `True` before agent is marked as `running`
- I22: `snapshot_id` refers to an existing snapshot
- I23: `reauthorized_by` is an authorized agent (via AetherGovern)

---

## Entity 9 — Snapshot

**Definition:** A point-in-time capture of an agent's state.

**Purpose:** For recovery.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `snapshot_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `agent_id` | string | ✅ | Reference to `Agent.agent_id` |
| 3 | `state` | bytes | ✅ | Serialized agent state |
| 4 | `hash` | string | ✅ | SHA-256 hash of `state` |
| 5 | `timestamp` | ISO 8601 | ✅ | Timestamp of capture |
| 6 | `stored_at` | string | ✅ | Storage location (AetherGit ref) |

**Relations:**
- Belongs to `Agent` (N:1)
- Stored in AetherGit (N:1)
- Referenced by `RecoveryRecord` (1:N)

**Invariants:**
- I24: `hash` matches SHA-256 of `state`
- I25: `stored_at` refers to an existing AetherGit record
- I26: `snapshot_id` is unique

---

## Entity 10 — RuntimeConfig

**Definition:** A configuration record for AetherRuntime.

**Purpose:** Configures thresholds, timeouts, and policies.

| # | Field | Type | Required | Description |
|:-:|---|---|:-:|---|
| 1 | `config_id` | string | ✅ | Unique identifier (hex, 64 chars) |
| 2 | `anomaly_threshold` | float | ✅ | Θ_max for resource monitoring |
| 3 | `halt_quorum` | float | ✅ | Quorum threshold (default: 0.67) |
| 4 | `telemetry_rate_hz` | float | ✅ | Monitoring sampling rate |
| 5 | `containment_expiry_seconds` | int | ✅ | Default containment expiry |
| 6 | `created_at` | ISO 8601 | ✅ | Timestamp of creation |

**Relations:**
- Applied to all `Agent` (1:N)
- Referenced by all policies

**Invariants:**
- I27: `anomaly_threshold > 0`
- I28: `halt_quorum ∈ [0.5, 1.0]`
- I29: `telemetry_rate_hz > 0`

---

## Entity Relations Summary

| Relation | Type | Cardinality |
|---|---|:-:|
| Agent → TelemetryRecord | has many | 1:N |
| Agent → AnomalyAlert | has many | 1:N |
| Agent → ContainmentPolicy | has many | 1:N |
| Agent → HaltOrder | has many | 1:N |
| Agent → RecoveryRecord | has many | 1:N |
| Agent → Snapshot | has many | 1:N |
| TelemetryRecord → Baseline | consumed by | N:1 |
| AnomalyAlert → TelemetryRecord | references | N:1 |
| AnomalyAlert → Baseline | references | N:1 |
| ContainmentPolicy → AnomalyAlert | triggered by | N:1 |
| HaltOrder → Agent | belongs to | N:1 |
| HaltOrder → HaltApproval | has many | 1:N |
| RecoveryRecord → HaltOrder | follows | N:1 |
| RecoveryRecord → Snapshot | references | N:1 |

---

## Structural Invariants (35 total)

The following invariants MUST hold for all AetherRuntime data:

**Identity (I1–I8):**
- I1: `agent_id` is unique
- I2: `public_key` is a valid Ed25519 key
- I3: `status` is one of six defined states
- I4: `telemetry_id` is unique
- I5: `value` is finite
- I6: `timestamp` is monotonic per agent
- I7: `sample_count >= 10` for baselines
- I8: `parameters` contains all required keys

**Detection (I9–I13):**
- I9: `confidence` ∈ [0.0, 1.0]
- I10: `telemetry_id` refers to existing record
- I11: `level` is one of four defined levels
- I12: `expiry > created_at`
- I13: `restrictions` contains all required keys for `level`

**Halt (I14–I20):**
- I14: `proposer_signature` verifies
- I15: `quorum_threshold` ∈ [0.5, 1.0]
- I16: `enforced_at` set iff quorum reached
- I17: `Δt_window > 0` (Proposition 2)
- I18: `signature` verifies against `approver`
- I19: `approval_id` is unique
- I20: An approver cannot approve twice

**Recovery (I21–I26):**
- I21: `verification_result` before running
- I22: `snapshot_id` refers to existing snapshot
- I23: `reauthorized_by` is authorized
- I24: `hash` matches `state`
- I25: `stored_at` refers to existing record
- I26: `snapshot_id` is unique

**Config (I27–I29):**
- I27: `anomaly_threshold > 0`
- I28: `halt_quorum` ∈ [0.5, 1.0]
- I29: `telemetry_rate_hz > 0`

**Cross-entity (I30–I35):**
- I30: Every `AnomalyAlert` references an existing `Agent` and `TelemetryRecord`
- I31: Every `ContainmentPolicy` references an existing `AnomalyAlert`
- I32: Every `HaltOrder` has at least one `HaltApproval` before enforcement
- I33: Every `RecoveryRecord` follows a `HaltOrder`
- I34: Every `Agent` has at least one `Baseline` before detection
- I35: Every `HaltOrder` enforces across all honest nodes (Proposition 1)

---

## Field Count Summary

| Entity | Fields | Status |
|---|:-:|:-:|
| Agent | 5 | ✅ |
| TelemetryRecord | 6 | ✅ |
| Baseline | 7 | ✅ |
| AnomalyAlert | 7 | ✅ |
| ContainmentPolicy | 7 | ✅ |
| HaltOrder | 9 | ✅ |
| HaltApproval | 5 | ✅ |
| RecoveryRecord | 8 | ✅ |
| Snapshot | 6 | ✅ |
| RuntimeConfig | 6 | ✅ |
| **Total** | **66** | ✅ |

---

## Next Document

- `02_operations.md` — Operations (collect, detect, contain, halt, recover)
- `03_invariants.md` — Full invariant list
- `04_interfaces.md` — Interfaces with Aether family
- `05_test_design.md` — Test design for 60 tests

---

**Document Status:** Complete
**Version:** 2.0.0
**Date:** 2026-11-09

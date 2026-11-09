# AetherRuntime v2.0.0 — Interfaces Specification

**Version:** 2.0.0
**Status:** Operational Specification
**Basis:** AetherRuntime v0.1.0 (DOI: 10.5281/zenodo.24078477)
**Date:** 2026-11-09

---

## Overview

This document defines the **five interfaces** between AetherRuntime and the other five functional dimensions of the Aether family. Each interface specifies what AetherRuntime **requires** from the other dimension and what it **provides** to it.

**Scope:** 5 interfaces, 20 requirements, 15 provisions, 5 coupling ratings.

---

## Interface 1 — AetherGit (Storage)

**Dimension:** Storage and versioning
**DOI:** [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896)
**Coupling:** Low–medium

### What AetherRuntime requires from AetherGit

| # | Requirement | Purpose |
|:-:|---|---|
| R1 | A storage schema in which `TelemetryRecord` can be stored as an append-only record | Persist monitoring data |
| R2 | A storage schema in which `Snapshot` can be stored as a content-addressed record | Persist agent state |
| R3 | A storage schema in which `RecoveryRecord` can be stored as an append-only record | Persist recovery history |
| R4 | A reference mechanism (`git_ref`) to link records to AetherGit commits | Trace records to versions |

### What AetherRuntime provides to AetherGit

| # | Provision | Purpose |
|:-:|---|---|
| P1 | A `Snapshot` mechanism that AetherGit can use to checkpoint an agent's state | State capture |
| P2 | A `RecoveryRecord` that AetherGit can use to roll back to a known-good state | State rollback |

### Coupling risk

**Low–medium.** AetherRuntime can function with a minimal AetherGit (append-only records + content-addressing). The coupling is low because AetherRuntime does not require AetherGit to change its schema.

---

## Interface 2 — AetherFlow (Integration)

**Dimension:** Integration and operational verification
**DOI:** [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129)
**Coupling:** Medium–high

### What AetherRuntime requires from AetherFlow

| # | Requirement | Purpose |
|:-:|---|---|
| R5 | An event stream from AetherFlow's operational verification | Correlate telemetry with post-merge checks |
| R6 | A hook at the merge stage where AetherRuntime can inspect the agent's state | Detect anomalies during integration |
| R7 | A halt signal that AetherFlow can consume to reject further actions from a halted agent | Enforce halt at integration |

### What AetherRuntime provides to AetherFlow

| # | Provision | Purpose |
|:-:|---|---|
| P3 | A `HaltOrder` that AetherFlow can consume to reject actions | Enforce halt |
| P4 | A `ContainmentPolicy` that AetherFlow can apply to integration | Restrict resources |
| P5 | A `TelemetryRecord` that AetherFlow can use for post-hoc analysis | Forensic evidence |

### Coupling risk

**Medium–high.** This is the closest coupling. If AetherFlow's operational verification is extended to cover runtime monitoring, F1 may be falsified for that part. The case for a separate dimension rests on the layers beyond the minimal interface.

---

## Interface 3 — AetherProof (Verification)

**Dimension:** Specification and formal evidence
**DOI:** [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124)
**Coupling:** Medium

### What AetherRuntime requires from AetherProof

| # | Requirement | Purpose |
|:-:|---|---|
| R8 | A designation of which specifications are runtime-checkable | Know what to verify at runtime |
| R9 | A proof obligation for each runtime predicate (e.g., the anomaly predicate must be deterministic) | Formalize runtime predicates |
| R10 | A mechanism to verify the `RecoveryRecord` against the specification | Verify recovery correctness |

### What AetherRuntime provides to AetherProof

| # | Provision | Purpose |
|:-:|---|---|
| P6 | A `TelemetryRecord` stream that AetherProof can use as evidence | Runtime evidence |
| P7 | A `RecoveryRecord` with `verification_result = True` that AetherProof can attest | Recovery attestation |
| P8 | A runtime predicate (anomaly detection) that AetherProof can formalize | Formalization target |

### Coupling risk

**Medium.** AetherRuntime can function without AetherProof (by using informal verification). The coupling is medium because AetherProof provides the formal basis for Proposition 1 (determinism).

---

## Interface 4 — AetherMesh (Distribution)

**Dimension:** Distribution and eventual consistency
**DOI:** [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038)
**Coupling:** High

### What AetherRuntime requires from AetherMesh

| # | Requirement | Purpose |
|:-:|---|---|
| R11 | Delta replication of `TelemetryRecord` and `HaltOrder` | Replicate across nodes |
| R12 | A determinism-compatible predicate for admission | Preserve AetherMesh's convergence (Proposition 1) |
| R13 | A gossip layer for `HaltOrder` propagation | Disseminate halt orders |
| R14 | A `revocation_frontier`-like mechanism for halt orders | Ensure monotonicity (Proposition 2) |

### What AetherRuntime provides to AetherMesh

| # | Provision | Purpose |
|:-:|---|---|
| P9 | A `MonitoringPredicate` that satisfies AetherMesh's determinism requirement (Proposition 1) | Admission |
| P10 | A `HaltPredicate` that satisfies monotonicity (Proposition 2) | Halt |
| P11 | A `HaltOrder` that replicates as a delta | Replication |
| P12 | A `HaltApproval` that replicates as a delta | Quorum |

### Coupling risk

**High.** This is the highest coupling. AetherRuntime depends on AetherMesh for:
- Delta replication
- Gossip propagation
- Determinism compatibility

If AetherMesh changes its assumptions (A1–A6), AetherRuntime must adapt.

---

## Interface 5 — AetherGovern (Governance)

**Dimension:** Authority and policy
**DOI:** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
**Coupling:** High

### What AetherRuntime requires from AetherGovern

| # | Requirement | Purpose |
|:-:|---|---|
| R15 | Authority to halt an agent | Define who may halt |
| R16 | Authority to contain an agent | Define who may contain |
| R17 | Authority to reauthorize recovery | Define who may recover |
| R18 | A definition of which nodes are authorized to sign a halt order | Halt quorum |

### What AetherRuntime provides to AetherGovern

| # | Provision | Purpose |
|:-:|---|---|
| P13 | Runtime evidence for accountability | Accountability |
| P14 | A `HaltOrder` that AetherGovern can use for revocation | Revocation |
| P15 | A `ContainmentPolicy` that AetherGovern can use for policy enforcement | Enforcement |

### Coupling risk

**High.** AetherRuntime depends on AetherGovern for:
- Halt authority
- Containment authority
- Recovery authority

**Circularity risk:** If halting requires authorization, and authorization is defined by governance, then runtime assurance is partly downstream of governance. This is the crux of F3.

---

## Interface Summary

| # | Dimension | Requires | Provides | Coupling |
|:-:|---|---|:-:|:-:|
| 1 | AetherGit | R1–R4 | P1–P2 | Low–medium |
| 2 | AetherFlow | R5–R7 | P3–P5 | Medium–high |
| 3 | AetherProof | R8–R10 | P6–P8 | Medium |
| 4 | AetherMesh | R11–R14 | P9–P12 | High |
| 5 | AetherGovern | R15–R18 | P13–P15 | High |

**Totals:** 18 requirements, 15 provisions.

---

## Minimal Interface

The **minimal interface** consists of four artifacts and one rule:

1. **Telemetry schema** — How telemetry records are structured.
2. **Baseline model** — How baselines are computed.
3. **Halt-order record** — How halt orders are structured.
4. **Halt-approval record** — How approvals are structured.
5. **Determinism rule** — The halt predicate must satisfy Proposition 1.

**If the minimal interface is all that is needed:**
- The whole contribution might be an extension of AetherFlow's operational verification.
- The case for a standalone dimension rests on the layers beyond the minimal interface.

**That is a hypothesis for which the paper has no evidence.**

---

## Full Interface

The **full interface** adds:

- Policy lifecycle messages (to/from AetherGovern)
- Accountability queries (to/from AetherGovern)
- Dispute and escalation messages (to/from AetherGovern)
- Governed-specification designation (for AetherProof)
- Remediation-authority rule (for AetherFlow)

---

## Interface Testing

Each interface is tested by:

| # | Interface | Test |
|:-:|---|---|
| 1 | AetherGit | T48 |
| 2 | AetherFlow | T49 |
| 3 | AetherProof | T50 |
| 4 | AetherMesh | T51 |
| 5 | AetherGovern | T52 |

---

## Cross-Interface Invariants

- **CI1:** Every interface preserves the determinism requirement (Proposition 1).
- **CI2:** Every interface preserves the monotonicity requirement (Proposition 2).
- **CI3:** Every interface is compatible with AetherMesh's assumption A6.
- **CI4:** Every interface respects AetherGovern's authority model.
- **CI5:** Every interface provides evidence for AetherProof's verification.

---

## Next Document

- `05_test_design.md` — Test design for 60 tests

---

**Document Status:** Complete
**Version:** 2.0.0
**Date:** 2026-11-09

# AetherRuntime v2.0.0 — Evaluation Report

**Version:** 2.0.0
**Date:** 2026-11-09
**Record ID:** AETHERRUNTIME-02
**Paper version:** 0.1.0 (DOI: [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477))
**OSF Registration:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
**Figshare:** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)

---

## 1. Summary

AetherRuntime v2.0.0 is the **reference implementation** of the operational specification derived from the AetherRuntime v0.1.0 hypothesis. It provides:

- A working implementation of the 10 entities, 7 operations, and 47 invariants of v0.1.0.
- A test suite of **60 tests** (pytest), all passing.
- **3 reproducible experiments** (M1/M2, M5, M6).

**Status:** Reference implementation. Preliminary results. The v0.1.0 hypothesis (F1–F5) is **not falsified** by the implementation or the experiments, but it is also **not confirmed**. The final project structure (single, dual, triple, or quadruple project) remains **undetermined**.

---

## 2. What v2.0.0 Adds to v0.1.0

| v0.1.0 (hypothesis) | v2.0.0 (this) |
|---|---|
| Formal architecture specified | Reference implementation built |
| Two propositions (proof sketches) | Implemented local anomaly detection and monotonic halt |
| Five failure conditions (F1–F5) | Evaluated against M1–M6 (simulation) |
| No implementation, no tests, no experiments | 15 modules, 60 tests, 3 experiments |
| No PyPI package | PyPI package `aetherruntime` (planned for v2.0.1) |

**The v0.1.0 hypothesis remains the authoritative record.** v2.0.0 does not modify the hypothesis; it adds an implementation and an empirical evaluation alongside it.

---

## 3. Implementation Status

| Module | Files | Lines | Purpose |
|---|:-:|:-:|---|
| `models.py` | 1 | ~480 | 10 entities, 4 enums |
| `monitoring/` | 2 | ~490 | `collect`, `update_baseline` |
| `detection/` | 2 | ~450 | `detect`, `AlertRegistry` |
| `containment/` | 2 | ~530 | `contain`, `IsolationManager` |
| `halt/` | 2 | ~530 | `propose_halt`, `approve_halt` |
| `recovery/` | 2 | ~490 | `create_snapshot`, `recover` |
| `simulation/` | 3 | ~900 | `Network`, `Node`, `Testbed` |
| `cli.py` | 1 | ~306 | CLI (`info\|verify\|simulate\|experiment`) |
| `__version__.py` | 1 | ~40 | Version info |
| `__init__.py` | 1 | ~314 | Public API (117 exports) |
| **Total** | **16** | **~4,520** | |

**Test suite:** 60 tests across 7 files:
- `test_models.py`: 10 tests
- `test_monitoring.py`: 8 tests
- `test_detection.py`: 8 tests
- `test_containment.py`: 8 tests
- `test_halt.py`: 8 tests
- `test_recovery.py`: 8 tests
- `test_simulation.py`: 10 tests

**Test result:** ✅ **60/60 passed** in 1.38s.

---

## 4. Experimental Results

### 4.1 Experiment 1 — Detection Accuracy (M1, M2)

From `experiments/detection_accuracy/results.json`:

| Scenario | mean_anomalies |
|---|---:|
| S1 (Resource Exhaustion) | 20.33 |
| S2 (Action Drift) | 20.33 |
| S3 (Network Anomaly) | 20.33 |
| S4 (Privilege Escalation) | 20.33 |
| S5 (Byzantine Agent) | 28.33 |
| S6 (False Positive) | 7.33 |

**Reading:**
- **M1 (S1–S5 total anomalies):** 109.67
- **M2 (S6 false positives):** 7.33
- **Detection ratio M1/M2:** ≈ 15:1
- **False positive rate:** 7.33 / (5 nodes × 36 readings) ≈ **4%**

**Caveat:** This is a **simulation result**. It uses a simplified network model (no real latency, packet loss, or adversarial conditions). The false positive rate is consistent with real-world anomaly detection (typical: 5–15%).

### 4.2 Experiment 2 — Halt Window (M5)

From `experiments/halt_window/results.json`:

| Trial | Approvals | Window (s) | Enforced |
|:-:|:-:|---:|:-:|
| 1 | 4 | 0.000389 | ✅ |
| 2 | 4 | 0.000228 | ✅ |
| 3 | 4 | 0.000223 | ✅ |
| 4 | 4 | 0.000218 | ✅ |
| 5 | 4 | 0.000249 | ✅ |
| 6 | 4 | 0.000283 | ✅ |
| 7 | 4 | 0.000211 | ✅ |
| 8 | 4 | 0.000206 | ✅ |
| 9 | 4 | 0.000205 | ✅ |
| 10 | 4 | 0.000213 | ✅ |

**Summary:**
- **Enforced:** 10/10
- **Mean window:** 0.000243s
- **Median window:** 0.000220s

**Reading:** All halts were enforced with a quorum of 4 approvals (out of 5 nodes = 80% > 67% threshold). The window is consistently positive and small (~0.2 ms). This is a **simulation-only** result; it does not measure real network latency.

**Caveat:** The 0.2 ms figure is a property of the simulation's time step, not a measurement of a real system. In a real network, the halt window would depend on gossip dissemination time, network latency, and node churn.

### 4.3 Experiment 3 — Recovery Correctness (M6)

From `experiments/recovery_correctness/results.json`:

| Trial | Verification | Final Status |
|:-:|:-:|---|
| 1–10 | ✅ verified | running |

**Summary:**
- **M6 (recovery correctness):** **1.0000** (10/10)
- All recovered states matched ground truth.
- All final statuses were `running`.

**Reading:** Every recovery operation produced a `RecoveryRecord` with `verification_result = True`, and the agent was resumed correctly. This is the expected result (M6 = 1.0).

**Caveat:** The ground truth is defined by the simulator, so M6 = 1.0 is a **ceiling** on real recovery quality, not a lower bound. In a real system, a Byzantine node could corrupt state during recovery.

---

## 5. What v2.0.0 Does Not Change

| Aspect | Status |
|---|---|
| v0.1.0 hypothesis | **Unchanged.** Still the authoritative record. |
| v0.1.0 failure conditions F1–F5 | **Unchanged.** F1–F4 are not falsified; F5 is untested. |
| v0.1.0 propositions P1–P2 | **Unchanged.** Still proof sketches, not machine-checked. |
| v0.1.0 limitations | **Unchanged.** All still apply. |
| Real-world deployment | **Still not evaluated.** |

---

## 6. What v2.0.0 Enables

- **Reproducibility:** Anyone can run `pytest` and `experiments/*/run.py`.
- **Extension:** The `src/aetherruntime/` package can be imported and extended.
- **Falsifiability:** The 60 tests make specific claims checkable.
- **PyPI:** The package is planned for v2.0.1.

---

## 7. Known Limitations of v2.0.0

| # | Limitation |
|:-:|---|
| 1 | **Simulation only.** No real-world deployment has been evaluated. |
| 2 | **Simplified network model.** No real latency distributions, packet loss, NAT, or adversarial network conditions. |
| 3 | **Simplified Byzantine model.** Limited to malformed certificates; colluding, equivocating, withholding, and Sybil adversaries are not tested. |
| 4 | **Root registry is centralized.** In v2.0.0, roots are passed explicitly. A decentralized root registry is future work. |
| 5 | **No ablation.** The contribution of each layer is not isolated. |
| 6 | **No mechanized proofs.** P1–P2 remain proof sketches. |
| 7 | **Tests cover the specification, not the implementation's edge cases.** Some edge cases (schema evolution, network partitions during revocation) are not tested. |
| 8 | **No performance benchmarks.** The simulation does not measure latency, throughput, or resource consumption in a real system. |

---

## 8. Reproducibility

```bash
# Install (development mode)
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# Run tests
python3 -m pytest tests/ -v

# Run experiments
python3 experiments/detection_accuracy/run.py
python3 experiments/halt_window/run.py
python3 experiments/recovery_correctness/run.py

# CLI
python3 -m aetherruntime.cli info
python3 -m aetherruntime.cli verify
python3 -m aetherruntime.cli simulate --scenario S1 --nodes 5 --runs 3
```

---

9. Comparison with AetherGovern v2.0.0

Aspect AetherGovern v2.0.0 AetherRuntime v2.0.0
Paper 33 pages 33 pages
Modules 15 16
Tests 60 60
Coverage (not measured) (not measured)
Experiments 3 3
PyPI ✅ aethergovern 2.0.0 ⏳ aetherruntime (planned)
Real-world ❌ ❌
Peer-reviewed ❌ ❌

---

10. Contact

· Author: Samir Baladi
· ORCID: 0009-0003-8903-0029
· Email: gitdeeper@gmail.com
· Zenodo DOI: 10.5281/zenodo.24078477
· Figshare: 10.6084/m9.figshare.34955746
· OSF: 10.17605/OSF.IO/KZU7P
· GitHub: gitdeeper15/aetherruntime

---

End of Evaluation Report (v2.0.0).

<div align="center">

# 🎯 AetherOrchestrate

### A Falsification-First Investigation of Decentralized Orchestration in the Aether Family

*Goal Decomposition, Task Assignment, Scheduling, Dependency Tracking, and Routing in Multi-Agent Software Ecosystems*

<br>

[![DOI Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.24095399.svg)](https://doi.org/10.5281/zenodo.24095399)
[![DOI Figshare](https://img.shields.io/badge/DOI%20Figshare-10.6084%2Fm9.figshare.34963687-blue)](https://doi.org/10.6084/m9.figshare.34963687)
[![License: MIT + CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--4.0-crimson.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![Release](https://img.shields.io/badge/Release-v2.0.0-green)](https://github.com/gitdeeper15/aetherorchestrate/releases/tag/v2.0.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)

[![PyPI](https://img.shields.io/badge/PyPI-2.0.0%20(pending)-gold?logo=pypi&logoColor=white)](https://pypi.org/project/aetherorchestrate/)
[![Tests](https://img.shields.io/badge/Tests-39%20passed-brightgreen)](tests/)
[![Experiments](https://img.shields.io/badge/Experiments-3%2F3-brightgreen)](experiments/)

[![Zenodo](https://img.shields.io/badge/Zenodo-Published-blue)](https://doi.org/10.5281/zenodo.24095399)
[![Figshare](https://img.shields.io/badge/Figshare-Published-blue)](https://doi.org/10.6084/m9.figshare.34963687)
[![OSF](https://img.shields.io/badge/OSF-Published-blue)](https://doi.org/10.17605/OSF.IO/2F7TZ)
[![Record ID](https://img.shields.io/badge/Record%20ID-AETHERORCHESTRATE--02-informational)](https://doi.org/10.5281/zenodo.24095399)
[![Website](https://img.shields.io/badge/Website-aetherorchestrate.netlify.app-00C7B7?logo=netlify&logoColor=white)](https://aetherorchestrate.netlify.app)
[![Aether Family](https://img.shields.io/badge/Aether%20Family-7%20dimensions-purple)](https://aetherorchestrate.netlify.app)

<br>

**[📄 Paper (Zenodo)](https://doi.org/10.5281/zenodo.24095399)** ·
**[📑 Preprint (Figshare)](https://doi.org/10.6084/m9.figshare.34963687)** ·
**[📋 OSF Registration](https://doi.org/10.17605/OSF.IO/2F7TZ)** ·
**[🌐 Website](https://aetherorchestrate.netlify.app)** ·
**[📦 Releases](https://github.com/gitdeeper15/aetherorchestrate/releases)** ·
**[📖 Citation](#-citation)**

</div>

---

> [!WARNING]
> **Status: v2.0.0 — Reference Implementation.**
> A reference implementation is built (`src/aetherorchestrate/`, 7 modules, 39 tests) and 3 experiments are executed.
> **Experiments use simulated data; no real-world deployment is evaluated.**
> The v0.1.0 hypothesis (F1–F5) is **not falsified** by the implementation or the experiments, but it is also **not confirmed**.
> F5 (observable benefit) remains **untested**.
> See [Threats to Validity](#️-threats-to-validity) and the [Research Status Statement](#-research-status-statement).

> *"AetherOrchestrate is a candidate, not a result."*

---

## 📑 Table of Contents

- [Overview](#-overview)
- [v2.0.0 at a Glance](#-v200-at-a-glance)
- [Seven-Phase Methodology](#-seven-phase-methodology)
- [The Central Question](#-the-central-question)
- [The Seven Functional Dimensions](#️-the-seven-functional-dimensions)
- [The Falsification-First Methodology](#-the-falsification-first-methodology)
- [Failure Conditions F1–F5](#-failure-conditions-f1f5)
- [Requirements R1–R6](#-requirements-r1r6)
- [AetherOrchestrate: Architecture](#️-aetherorchestrate-architecture)
- [Propositions P1–P2](#-propositions-p1p2)
- [Interfaces with the Aether Family](#-interfaces-with-the-aether-family)
- [Evaluation Design and v2.0.0 Results](#-evaluation-design-and-v200-results)
- [Threats to Validity](#️-threats-to-validity)
- [Open Questions Q1–Q20](#-open-questions-q1q20)
- [Research Status Statement](#-research-status-statement)
- [Platforms & Mirrors](#-platforms--mirrors)
- [Project Structure](#️-project-structure)
- [Version History](#-version-history)
- [Citation](#-citation)
- [Author](#-author)
- [License](#️-license)

---

## 🔭 Overview

**AetherOrchestrate** is the **seventh functional dimension (provisional)** of the Aether family — a candidate architecture for **goal decomposition, task assignment, scheduling, dependency tracking, and routing** of work in multi-agent software ecosystems.

The Aether family currently comprises **six foundational dimensions**, each published as a preprint on Zenodo (**not peer-reviewed**):

| Dimension | Focus | Question |
|---|---|---|
| **AetherGit** | Storage and versioning | How are agent-generated changes stored, signed, and versioned? |
| **AetherFlow** | Integration and post-merge verification | How are changes integrated into a shared trunk and verified? |
| **AetherProof** | Specification and evidence | How are claims specified and how is evidence for them recorded? |
| **AetherMesh** | Distribution and consistency | How is state synchronized without a central coordinator? |
| **AetherGovern** | Authority and policy | Who is authorized to do what, under which policy, and how is authority revoked? |
| **AetherRuntime** | Monitoring and assurance | What are agents doing while they run, and how are anomalies contained? |

AetherOrchestrate asks whether a **seventh dimension** is needed:

> **What should agents do next, and how is work decomposed, assigned, scheduled, ordered, and routed without a central coordinator?**

The investigation follows a **falsification-first methodology**: before describing the candidate, it states **five failure conditions (F1–F5)** whose satisfaction would show that the candidate does not deserve to exist as a separate dimension.

| Release | What it adds |
|---|---|
| **v0.1.0** | The hypothesis and the falsification-first methodology (paper only) |
| **v2.0.0** | Reference implementation (`src/aetherorchestrate/`): 7 modules, 39 tests, 3 experiments |

---

## 📊 v2.0.0 at a Glance

| Dimension | Status |
|---|---|
| Manuscript (v0.1.0) | ✅ Complete (36 pages) |
| Definitions / Propositions / Layers | 4 / 2 (proof sketches) / 5 |
| Implementation | ✅ Built (`src/aetherorchestrate/`, 7 modules) |
| Tests | ✅ 39 passed |
| Experiments | ✅ 3/3 completed (simulated data) |
| PyPI package | ⏳ Publishing in progress |
| Real-world deployment | ❌ Not evaluated |
| Causal claims | None (argument only) |

<p align="center">
  <img src="docs/figures/Fig1_Seven_Dimensions.png"
       alt="AetherOrchestrate — The Seven Functional Dimensions of the Aether Family"
       width="100%">
</p>

<p align="center">
  <em>Figure 1 — The Seven Functional Dimensions of the Aether Family. The seventh dimension (AetherOrchestrate) is a hypothesis under investigation, not a confirmed dimension.</em>
</p>

### Contributions

| # | Contribution | Kind |
|:-:|---|---|
| 1 | A falsification-first procedure with five failure conditions and a decision rule, stated before the candidate is described | Methodology |
| 2 | A formal framework: four definitions (goal decomposition, task-assignment predicate, dependency graph, coordination window) | Analysis |
| 3 | Two propositions with proof sketches: determinism of local decomposition (P1); irreducible coordination window (P2) | Analysis |
| 4 | A five-layer architectural hypothesis: decomposition, assignment, scheduling, dependency tracking, routing | Specification (hypothesis) |
| 5 | **A reference implementation** (v2.0.0) with 7 modules, 39 tests, and 3 experiments | Implementation |
| 6 | An evaluation design: nine metrics, five baselines, six scenarios, a protocol | Design (partly executed in v2.0.0) |
| 7 | Twenty open questions (Q1–Q20) | Catalogue |

---

## 🪜 Seven-Phase Methodology

v2.0.0 was built through a seven-phase methodology. Each phase is documented in a separate file.

| Phase | Deliverable | File | Status |
|:-:|---|---|:-:|
| 1 | Architectural Specification | `SPECIFICATION.md` (431 lines) | ✅ |
| 2 | Invariant Definition | `INVARIANTS.md` (285 lines) | ✅ |
| 3 | Test Design | `TESTS.md` (312 lines) | ✅ |
| 4 | Simulator Implementation | `src/aetherorchestrate/` (7 modules, ~561 lines) | ✅ |
| 5 | Test Execution | `tests/` (39 tests, 39 pass) | ✅ |
| 6 | Experiments | `experiments/` (3 experiments) | ✅ |
| 7 | Release | `RELEASE.md` (101 lines) | ✅ |

**Why seven phases?** To avoid building ~1,100 lines of Python based on untested assumptions, then discovering that the architecture itself needs to change. Each phase constrains the next.

**What is not assumed:** CRDT, gossip, BFT, or AetherMesh.

---

## ❓ The Central Question

> **Is there a set of requirements for goal decomposition, task assignment, scheduling, dependency tracking, and routing in multi-agent software systems that (i) is not already specified by the six existing dimensions, (ii) does not reduce to verification or to governance, (iii) can be specified without reintroducing a central authority, and (iv) yields an observable benefit over existing mechanisms?**

The four clauses correspond to failure conditions **F1**, **F2 and F3**, **F4**, and **F5**. A negative answer to any clause is sufficient to reject the candidate as a separate dimension.

---

## 🗺️ The Seven Functional Dimensions

| # | Dimension | Focus | DOI |
|:-:|---|---|---|
| 1 | **AetherGit** | Storage and versioning | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| 2 | **AetherFlow** | Integration and operational verification | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| 3 | **AetherProof** | Specification and evidence | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| 4 | **AetherMesh** | Distribution and consistency | [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038) |
| 5 | **AetherGovern** | Authority and policy | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) |
| 6 | **AetherRuntime** | Monitoring and runtime assurance | [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477) |
| 7 | **AetherOrchestrate** *(hypothesis)* | Orchestration | [10.5281/zenodo.24095399](https://doi.org/10.5281/zenodo.24095399) |

<p align="center">
  <img src="docs/figures/Fig5_Orchestrate_vs_Flow.png"
       alt="AetherOrchestrate — Orchestration versus Integration (AetherFlow)"
       width="100%">
</p>

<p align="center">
  <em>Figure 5 — Orchestration compared with integration and verification (AetherFlow) in the Aether family. Whether the two are distinct is tested by the failure conditions.</em>
</p>

---

## 🔬 The Falsification-First Methodology

A typical architecture paper begins from a conviction that a component is needed and then specifies it. The risk is circular. AetherOrchestrate adopts a falsification-first methodology:

1. **No prior assumption** that the gap exists.
2. **No prior assumption** that AetherOrchestrate should be a separate project.
3. **Every claim** is tested against failure conditions (F1–F5).
4. The **final structure** (single, dual, triple, quadruple, or integration protocol) is determined *after* comparison.

---

## 🧭 Failure Conditions F1–F5

| ID | Claim under test | Status |
|:-:|---|:-:|
| **F1** | Non-redundancy | 🟡 Not falsified (R2, R4, R6 partly covered) |
| **F2** | Orthogonality to verification | 🟡 Not falsified (narrowly) |
| **F3** | Boundary with governance | 🟡 Not falsified (decentralized setting) |
| **F4** | Decentralizability | 🟡 Not falsified (with residuals) |
| **F5** | Observable benefit | 🔴 Untested |

> [!NOTE]
> **"Not falsified" is a weaker status than "confirmed". No condition is confirmed.**

---

## 📋 Requirements R1–R6

| ID | Requirement |
|:-:|---|
| **R1** | Goal decomposition: a goal can be decomposed into a DAG of tasks |
| **R2** | Task assignment: each task can be assigned to a capable agent |
| **R3** | Scheduling: tasks can be ordered in time respecting dependencies |
| **R4** | Dependency tracking: the task DAG can be maintained under concurrent updates |
| **R5** | Routing: each task can be delivered to its executor without a central router |
| **R6** | Partition tolerance: decomposition, assignment, scheduling, and routing remain possible when nodes are disconnected |

---

## 🏛️ AetherOrchestrate: Architecture

> [!NOTE]
> All of this is **hypothesis**: a design-level description offered so that the failure conditions can be applied to something concrete. The five layers are implemented in `src/aetherorchestrate/`.

### The Five Layers

<p align="center">
  <img src="docs/figures/Fig2_Orchestrate_Layers.png"
       alt="AetherOrchestrate — The Five Layers"
       width="100%">
</p>

<p align="center">
  <em>Figure 2 — The five layers of AetherOrchestrate.</em>
</p>

| Layer | Question | Module | Status |
|:-:|---|---|:-:|
| **L1 — Decomposition** | How is a goal broken into tasks? | `decomposition/` | ✅ Implemented |
| **L2 — Assignment** | Which agent executes each task? | `assignment/` | ✅ Implemented |
| **L3 — Scheduling** | When does each task run? | `scheduling/` | ✅ Implemented |
| **L4 — Dependency Tracking** | What are the dependencies between tasks? | `dependencies/` | ✅ Implemented |
| **L5 — Routing** | How is each task routed to its executor? | `routing/` | ✅ Implemented |

<p align="center">
  <img src="docs/figures/Fig3_Task_DAG.png"
       alt="AetherOrchestrate — Task DAG"
       width="100%">
</p>

<p align="center">
  <em>Figure 3 — A goal decomposed into a DAG of tasks.</em>
</p>

<p align="center">
  <img src="docs/figures/Fig4_Assignment_Challenge.png"
       alt="AetherOrchestrate — The Assignment Challenge"
       width="100%">
</p>

<p align="center">
  <em>Figure 4 — The assignment challenge in a decentralized setting.</em>
</p>

<p align="center">
  <img src="docs/figures/Fig6_Centralization_Spectrum.png"
       alt="AetherOrchestrate — The Centralization Spectrum"
       width="100%">
</p>

<p align="center">
  <em>Figure 6 — The centralization spectrum of orchestration designs.</em>
</p>

### Monotone vs. non-monotone functions

The paper separates orchestration functions that can be realized **without agreement** (monotone functions, or deterministic functions of monotone state) from those that **cannot** (for example, enforcing at-most-one executor). This partition is the core of **F4**.

---

## 📜 Propositions P1–P2

> [!NOTE]
> *Status: Stated with proof sketches; **not machine-checked**.*

| # | Proposition | Status |
|:-:|---|:-:|
| **P1** | Determinism of Local Decomposition | Proof sketch |
| **P2** | Irreducible Coordination Window | Proof sketch |

**P1 (restated).** If admission of a decomposition delta is a deterministic function of the delta and its causal closure, decomposition deltas are inflationary additions to `S`, and each node selects the canonical decomposition by a deterministic rule, then (1) admission satisfies assumption A6 of [AetherMesh](https://doi.org/10.5281/zenodo.24038038) and (2) once all deltas are delivered, every honest node selects the same canonical decomposition.

**P2.** In any decentralized coordination protocol, the coordination window at an honest node is bounded below by the time to form the corrective record, propagate it, and verify it. The window is strictly positive.

---

## 🔗 Interfaces with the Aether Family

| Dimension | Requires | Provides | Coupling |
|---|---|---|:-:|
| **AetherGit** | Append-only store; result hashes | Goal, decomposition, claim, completion records | Low–medium |
| **AetherFlow** | Verification outcomes; remediation signals | Plans and expected structure of work | Medium–high |
| **AetherProof** | Specifications; evidence; certificates | Acceptance predicates; plan certificates | Medium |
| **AetherMesh** | Convergent propagation; A6 | Orchestration deltas; materialization functions | High |
| **AetherGovern** | Authorization; revocation | Takeover triggers; authority-rank use | High |
| **AetherRuntime** | Liveness telemetry; anomaly observations | Re-planning signals | Medium–high |

---

## 📊 Evaluation Design and v2.0.0 Results

> [!IMPORTANT]
> In the v0.1.0 paper **no evaluation was performed**. The v2.0.0 experiments are **simulations** covering a subset of the proposed metrics.

| ID | Metric | Direction |
|:-:|---|:-:|
| **M1** | Decomposition accuracy | Higher is better |
| **M2** | False-positive rate | Lower is better |
| **M3** | Decomposition latency | Lower is better |
| **M4** | Assignment fairness | Higher is better |
| **M5** | Schedule feasibility | Higher is better |
| **M6** | Dependency-tracking accuracy | Higher is better |
| **M7** | Routing overhead | Lower is better |
| **M8** | Coordination window | Lower is better |
| **M9** | Convergence preservation | Must be zero |

**Baselines B1–B5:** no orchestration, centralized orchestrator, hierarchical orchestrator, consensus-based scheduling, market-based allocation.

**Scenarios S1–S6:** network partition, coordinator failure, agent churn, concurrent decompositions, compromised assignee, dependency-update storm.

### v2.0.0 Experimental Results

*From `experiments/*/results.json`.*

| # | Experiment | Metric | Result |
|:-:|---|:-:|---|
| 1 | Decomposition Accuracy | M1 | 10 goals; mean task count = 1.00; all acyclic ✅ |
| 2 | Assignment Fairness | M4 | Jain index = 0.8803 (expected 0.9174; 4% deviation) |
| 3 | Coordination Window | M8 | 5 scenarios; all positive; min 0.008 s, max 7.5 s |

> [!IMPORTANT]
> These are **simulation results**. No generalization beyond simulation is claimed. Baselines B1–B5 and scenarios S1–S6 are **not** evaluated in v2.0.0.

---

## ⚠️ Threats to Validity

Seven threats are listed (T1–T7), each with a stated planned mitigation:

| ID | Threat |
|:-:|---|
| T1 | Construct validity |
| T2 | Internal validity |
| T3 | External validity |
| T4 | Baseline strength |
| T5 | Scenario selection |
| T6 | Author bias |
| T7 | Model assumptions |

---

## ❓ Open Questions Q1–Q20

| Range | Area |
|---|---|
| Q1–Q3 | Decomposition |
| Q4–Q7 | Assignment |
| Q8–Q10 | Scheduling |
| Q11–Q13 | Dependency tracking |
| Q14–Q16 | Routing |
| Q17–Q18 | Interfaces |
| Q19–Q20 | Methodology |

Full statements are in Section 10 of the [paper](https://doi.org/10.5281/zenodo.24095399).

---

## 📋 Research Status Statement

| Item | Status |
|---|---|
| Document type | Research article + reference implementation |
| Version / record | 2.0.0, November 2026 · AETHERORCHESTRATE-02 · DOI 10.5281/zenodo.24095399 |
| Implementation | ✅ Built (`src/aetherorchestrate/`, 7 modules) |
| Tests | ✅ 39 passed |
| Experiments | ✅ 3/3 completed (simulated data) |
| PyPI package | ⏳ Publishing in progress |
| Real-world deployment | None; no deployed system has been benchmarked |
| Propositions P1–P2 | Proof sketches; not machine-checked |
| Review status | Not peer reviewed |

### Deferred from v2.0.0

- **I3′ — Strong exclusivity:** requires bounded agreement; not implemented.
- **I5 — Completion readiness:** requires verification layer; not implemented.
- **I7 — Canonical convergence under full delivery:** requires full-delivery simulation; not implemented.
- **CRDT, gossip, BFT:** not assumed, not implemented.
- **Real-world deployment:** not evaluated.

---

## 🌍 Platforms & Mirrors

| Platform | URL | Role | Status |
|---|---|---|:-:|
| **GitHub** | [gitdeeper15/aetherorchestrate](https://github.com/gitdeeper15/aetherorchestrate) | Source code, issues, PRs | ✅ Active |
| **GitLab** | [gitlab.com/gitdeeper15/aetherorchestrate](https://gitlab.com/gitdeeper15/aetherorchestrate) | Mirror repository | ✅ Active |
| **Codeberg** | [codeberg.org/gitdeeper15/aetherorchestrate](https://codeberg.org/gitdeeper15/aetherorchestrate) | Mirror repository | ✅ Active |
| **Bitbucket** | [bitbucket.org/gitdeeper15/aetherorchestrate](https://bitbucket.org/gitdeeper15/aetherorchestrate) | Mirror repository | ✅ Active |
| **PyPI** | [pypi.org/project/aetherorchestrate](https://pypi.org/project/aetherorchestrate/) | Python package (`2.0.0`) | ⏳ Publishing |
| **Zenodo** | [10.5281/zenodo.24095399](https://doi.org/10.5281/zenodo.24095399) | Citable DOI, paper archive | ✅ Published |
| **Figshare** | [10.6084/m9.figshare.34963687](https://doi.org/10.6084/m9.figshare.34963687) | Preprint archive | ✅ Published |
| **OSF** | [10.17605/OSF.IO/2F7TZ](https://doi.org/10.17605/OSF.IO/2F7TZ) · [project](https://osf.io/8beur) | Registration | ✅ Published |
| **Website** | [aetherorchestrate.netlify.app](https://aetherorchestrate.netlify.app) | Live documentation | ✅ Active |
| **ORCID** | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) | Author identity | ✅ Active |

---

## 🗂️ Project Structure

<details>
<summary><b>Click to expand the repository tree</b></summary>

```text
AetherOrchestrate/
├── src/
│   └── aetherorchestrate/                # Reference implementation (v2.0.0, 7 modules)
│       ├── __init__.py
│       ├── __version__.py
│       ├── models.py
│       ├── cli.py
│       ├── decomposition/
│       ├── assignment/
│       ├── scheduling/
│       ├── dependencies/
│       ├── routing/
│       └── simulation/
├── tests/                                # 39 tests
├── experiments/                          # 3 experiments
│   ├── decomposition_accuracy/
│   ├── assignment_fairness/
│   └── coordination_window/
├── docs/
│   ├── figures/                          # 6 figures (Fig1–Fig6)
│   │   ├── Fig1_Seven_Dimensions.png
│   │   ├── Fig2_Orchestrate_Layers.png
│   │   ├── Fig3_Task_DAG.png
│   │   ├── Fig4_Assignment_Challenge.png
│   │   ├── Fig5_Orchestrate_vs_Flow.png
│   │   └── Fig6_Centralization_Spectrum.png
│   └── specification/                    # 5 specification files
│       ├── 01_entities.md
│       ├── 02_operations.md
│       ├── 03_invariants.md
│       ├── 04_interfaces.md
│       └── 05_test_design.md
├── PUBLICATION/
│   ├── AetherOrchestrate_Research_Paper.pdf
│   └── v2.0.0/                           # (planned) v2.0.0 report
├── SPECIFICATION.md                      # Phase 1
├── INVARIANTS.md                         # Phase 2
├── TESTS.md                              # Phase 3
├── SIMULATOR.md                          # Phase 4
├── RESULTS.md                            # Phase 5–6
├── RELEASE.md                            # Phase 7
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── INVENTORY.md
├── LICENSE
├── PROJECT_SUMMARY.txt
├── README.md
├── VERSION                               # 2.0.0
├── manifest.json
├── netlify.toml
└── scientific_state.json
```

</details>

---

## 🕓 Version History

| Version | Release | Focus | Status |
|---|---|---|:-:|
| **v2.0.0** | 2026-11-10 ([release](https://github.com/gitdeeper15/aetherorchestrate/releases/tag/v2.0.0)) | Reference implementation: 7 modules, 39 tests, 3 experiments | ✅ Released |
| **v0.1.0** | 2026-11-09 ([release](https://github.com/gitdeeper15/aetherorchestrate/releases/tag/v0.1.0)) | Formal architecture proposal (no implementation) | ✅ Released |
| *(planned)* | 2027+ | Real-world evaluation; comparison against baselines B1–B5 | ⏳ Not executed |

---

## 📖 Citation

### Paper — AetherOrchestrate v0.1.0

```bibtex
@techreport{baladi2026aetherorchestrate,
  author       = {Baladi, Samir},
  title        = {AetherOrchestrate: A Falsification-First Investigation of Decentralized Orchestration in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24095399},
  url          = {https://doi.org/10.5281/zenodo.24095399},
  note         = {Formal Architecture Proposal --- No implementation claimed.}
}
```

### Software — AetherOrchestrate v2.0.0

```bibtex
@software{baladi2026aetherorchestrate_v2,
  author       = {Baladi, Samir},
  title        = {{AetherOrchestrate} v2.0.0: Reference Implementation of the Falsification-First Orchestration Architecture},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24095399},
  url          = {https://pypi.org/project/aetherorchestrate/},
  note         = {Reference implementation. Available via pip install aetherorchestrate.}
}
```

---

### OSF Preregistration — AetherOrchestrate v0.1.0

```bibtex
@misc{baladi2026aetherorchestrate_osf,
  author       = {Baladi, Samir},
  title        = {{AetherOrchestrate: A Falsification-First Investigation of Decentralized Orchestration in the Aether Family}},
  year         = {2026},
  month        = nov,
  day          = {10},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/2F7TZ},
  url          = {https://doi.org/10.17605/OSF.IO/2F7TZ},
  note         = {OSF Preregistration. Associated project: https://osf.io/8beur}
}
```

---

## 👤 Author

**Samir Baladi**
*Interdisciplinary AI Researcher — Ronin Institute / Rite of Renaissance*

| | |
|---|---|
| **Research Area** | Distributed Systems / Software Engineering / Multi-Agent Coordination |
| **Research Domain** | Orchestration, Task Decomposition, Assignment, Scheduling, Dependency Tracking, Routing |
| **Research Type** | Architectural Hypothesis + Reference Implementation |
| 📧 **Email** | [gitdeeper@gmail.com](mailto:gitdeeper@gmail.com) |
| 🔗 **ORCID** | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) |
| 🐙 **GitHub** | [gitdeeper15/aetherorchestrate](https://github.com/gitdeeper15/aetherorchestrate) |
| 📄 **Figshare** | [10.6084/m9.figshare.34963687](https://doi.org/10.6084/m9.figshare.34963687) |
| 🌐 **Official Site** | [aetherorchestrate.netlify.app](https://aetherorchestrate.netlify.app) |

---

## ⚖️ License

| Scope | License |
|---|---|
| **Code** | [MIT License](LICENSE) — Copyright © 2026 Samir Baladi |
| **Documentation, manuscript, and figures** | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode) |

<details>
<summary><b>MIT License — full text</b></summary>

```text
MIT License

Copyright (c) 2026 Samir Baladi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

</details>

---

<div align="center">

**AetherOrchestrate — Program Manuscript v2.0.0 (Reference Implementation)**

© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)

[Zenodo](https://doi.org/10.5281/zenodo.24095399) ·
[Figshare](https://doi.org/10.6084/m9.figshare.34963687) ·
[OSF](https://doi.org/10.17605/OSF.IO/2F7TZ) ·
[Website](https://aetherorchestrate.netlify.app) ·
[GitHub](https://github.com/gitdeeper15/aetherorchestrate)

</div>

# AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family

---

**Registration DOI:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 9, 2026, 10:21 AM
**Date Registered:** Nov 9, 2026, 10:21 AM
**Associated Project:** [https://osf.io/ft7ez](https://osf.io/ft7ez)
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `AetherRuntime_Research_Paper.md` (v0.1.0, 33 pages, 8,861 words)
- `AetherRuntime_Research_Paper.pdf` (placeholder for archival PDF)
- `README.md`
- `AUTHORS.md`
- `CHANGELOG.md`
- `CITATION.cff`
- `CONTRIBUTING.md`
- `INVENTORY.md`
- `LICENSE`
- `PROJECT_SUMMARY.txt`
- `VERSION`
- `manifest.json`
- `requirements.txt`
- `scientific_state.json`
- 6 figures (Fig1–Fig6) in `docs/figures/`

---

## Overview

### Research questions or hypotheses

**Central question (definition):**
Is there a body of monitoring, detection, containment, halt, and recovery requirements for multi-agent software ecosystems that (i) is not already specified by the five existing dimensions, (ii) is not reducible to verification or to governance, (iii) can be specified without reintroducing a central authority, and (iv) yields an observable benefit over existing mechanisms?

**Hypotheses (five failure conditions):**
- **F1 (Non-redundancy):** Some runtime-assurance requirement among R1–R6 is not met by the specified mechanisms of the five existing dimensions, even with one bounded, localized extension to a single dimension.
- **F2 (Orthogonality to verification):** Runtime-assurance decisions cannot be reduced to proof obligations in AetherProof without loss.
- **F3 (Boundary with governance):** In a decentralized setting, runtime assurance is distinct from governance.
- **F4 (Decentralizability):** Runtime assurance can be specified without a trusted central authority and without violating AetherMesh's determinism requirement (assumption A6).
- **F5 (Observable benefit):** There exist scenario classes in which the family with runtime assurance outperforms the family without it on a pre-specified metric.

**Propositions (stated with proof sketches, not machine-checked):**
- **P1:** If each node evaluates anomaly predicates against a local baseline and the anomaly predicates are deterministic functions of the local state, then the anomaly-detection layer preserves AetherMesh's determinism requirement (assumption A6).
- **P2:** Any decentralized halt protocol leaves a window Δt_window = t_halt_enforced − t_detect during which a compromised agent may continue to act.

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

No empirical data exists for this registration (v0.1.0). The manuscript is a specification-level investigation of an architectural hypothesis. No implementation is claimed. No real-world deployment has been evaluated. No experiment has been run. The five failure conditions (F1–F5) are definitions (proposed test criteria), not results. Propositions P1–P2 are proof sketches, not machine-checked.

The only "data" that exists is the argument-level analysis of the five failure conditions, which is reported in the manuscript. To manage the risk of unintended influences:

1. The failure conditions (F1–F5) and decision rule were stated before the candidate was described (Section 3 of the manuscript).
2. The decision rule explicitly states that "not falsified" is never promoted to "confirmed" on the basis of argument.
3. The requirement list (R1–R6) is a hypothesis, not a fixed set.
4. The evaluation design (Section 7) specifies thresholds and metrics in advance, so that future results cannot be reinterpreted.
5. The manuscript states explicitly that the final project structure (single, dual, triple, or quadruple) is undetermined.

Future empirical work (v1.0.0) will be pre-registered separately, with its own DOI, before any simulation is run.

---

## Research Design

### Study type

**Other:** AetherRuntime is a falsification-first investigation, not an empirical study.

### Intention for causal interpretation

**No causal relationship inferred:** This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Additional blinding during research or analysis

No blinding is required for this study. The investigation is a specification-level argument. The failure conditions (F1–F5) and decision rule were stated before the candidate was described (Section 3 of the manuscript). The decision rule explicitly states that "not falsified" is never promoted to "confirmed" on the basis of argument. This pre-commitment is the methodological safeguard, not blinding.

### Study design

This is a falsification-first investigation, not an empirical study.

**Stage 1 — Failure conditions.** Five failure conditions (F1–F5) and a decision rule are stated before the candidate is described. The conditions are stated as falsifiable tests, with explicit admissible evidence for each.

**Stage 2 — Comparison.** Three candidate capabilities are compared: orchestration (AetherOrchestrate), governance (AetherGovern), and runtime assurance (AetherRuntime). The comparison is qualitative and structural, not empirical.

**Stage 3 — Specification.** A five-layer runtime architecture is specified: monitoring, detection, containment, halt, recovery. Each layer is a hypothesis, not a result.

**Stage 4 — Propositions.** Two propositions are stated with proof sketches: (P1) local anomaly detection preserves AetherMesh's determinism requirement; (P2) any decentralized halt protocol leaves an irreducible halt window. The sketches are not machine-checked.

**Stage 5 — Evaluation design.** A future evaluation is specified in advance: metrics M1–M9, baselines B1–B5, scenarios S1–S6, thresholds. No evaluation is performed in v0.1.0.

The design is between-subjects at the conceptual level: each candidate capability is evaluated independently against F1–F5. There is no repeated-measures component. There is no counterbalancing (no empirical treatments).

A PDF of the full manuscript is attached separately as the primary artifact.

---

## Sampling

### Data collection procedures

No empirical data is collected in v0.1.0. This is a specification-level investigation of an architectural hypothesis.

The "data" that exists is the argument-level analysis of five failure conditions (F1–F5), which is reported in the attached manuscript (33 pages). No sampling frame, no recruitment, no inclusion/exclusion criteria, and no data collection procedure apply.

For the proposed future evaluation (v1.0.0), six scenario classes (S1–S6) are defined:
- **S1:** resource exhaustion
- **S2:** action-set drift
- **S3:** network anomaly
- **S4:** privilege escalation attempt
- **S5:** Byzantine agent
- **S6:** false positive

Sampling for these scenarios will be defined in a separate pre-registration before any simulation is run. No simulation is performed in v0.1.0.

### Sample size

N/A — No empirical sample exists in v0.1.0. The study is a specification-level investigation. No subjects, no units of analysis, no conditions, no treatments, and no clusters are involved.

For the proposed future evaluation (v1.0.0), sample size will depend on the number of nodes simulated (e.g., 10, 50, 100, 250, 500 nodes) and the number of runs per configuration (e.g., 30 runs per scenario). These will be defined in a separate pre-registration.

### Sample size rationale

N/A — No empirical sample in v0.1.0.

For the proposed future evaluation (v1.0.0), a power analysis will be performed to determine the minimum sample size needed to detect a difference between full runtime assurance and baselines B1–B5 on metrics M1–M9. This analysis will be reported in the separate pre-registration.

The current v0.1.0 study has no sample size because it makes no empirical claims. The specification is complete as written; there is no "sample" to justify.

### Starting and stopping rules

N/A — No data collection is performed in v0.1.0. There is no pilot testing, no data collection start, and no data collection termination.

For the proposed future evaluation (v1.0.0), starting and stopping rules will be defined in the separate pre-registration. Proposed rules:
- **Start:** after the simulation testbed is validated against AetherMesh's published results.
- **Stop:** when the pre-specified number of runs per configuration is reached, or when a pre-specified effect size is detected with the pre-specified confidence level.

No such rules apply to v0.1.0.

---

## Variables

### Manipulated variables

None. No variables are manipulated in v0.1.0. This is a specification-level investigation of an architectural hypothesis. There are no treatment arms, no conditions, no randomization, and no empirical manipulation.

For the proposed future evaluation (v1.0.0), the following would be manipulated:
- **Runtime assurance configuration:** full (five layers) vs. baselines B1–B5 (no runtime, static thresholds, centralized monitor, AetherFlow-only, minimal runtime).
- **Network size:** 10, 50, 100, 250, 500 nodes.
- **Scenario class:** S1–S6.

These will be defined in a separate pre-registration before any simulation is run.

### Measured variables

No empirical variables are measured in v0.1.0. The study is a specification-level investigation.

For the proposed future evaluation (v1.0.0), nine measured variables are defined:
- **M1:** Anomaly detection rate (fraction of true anomalies detected)
- **M2:** False-positive rate (fraction of benign actions flagged as anomalous)
- **M3:** Detection latency (time from anomaly onset to alert)
- **M4:** Containment time (time from alert to containment)
- **M5:** Halt window (time from detection to halt enforcement)
- **M6:** Recovery correctness (fraction of recovered states that match ground truth)
- **M7:** Monitoring overhead (added CPU/memory/network per agent)
- **M8:** Halt quorum latency (time to reach quorum for a halt order)
- **M9:** Convergence preservation (count of runs in which honest nodes diverge)

Each metric is defined in Section 7.1 of the attached manuscript.

### Indices

No indices are computed in v0.1.0. No empirical data exists to combine.

For the proposed future evaluation (v1.0.0), the following derived variables could be computed:
- **Detection efficiency:** (M1 × (1 − M2)) / M3 — a combined measure of detection quality and speed.
- **Containment efficiency:** M4 / M5 — ratio of containment time to halt window.
- **Recovery reliability:** M6 × (1 − M2) — recovery correctness adjusted for false-positive rate.
- **Monitoring cost-effectiveness:** (M1 × (1 − M2)) / M7 — detection quality per unit overhead.

These indices are proposals. They will be finalized in the separate pre-registration before any simulation is run.

---

## Analysis Plan

### Statistical models

No statistical models are used in v0.1.0. The study is a specification-level investigation of an architectural hypothesis. No data is collected, no variables are measured, and no statistical inference is performed.

For the proposed future evaluation (v1.0.0), the following statistical models are proposed:

- **Primary analysis:** For each metric M1–M9, compare the full runtime assurance configuration against baselines B1–B5 using a linear mixed-effects model with:
  - Fixed effects: configuration (6 levels: full, B1–B5), network size (5 levels: 10, 50, 100, 250, 500 nodes), scenario class (6 levels: S1–S6)
  - Random effects: run (30 runs per configuration)
  - Interaction: configuration × network size
- **Secondary analysis:** For each metric, compute 95% confidence intervals for the difference between full runtime assurance and each baseline.
- **Convergence check (M9):** Report the count of runs where honest nodes diverge; if M9 > 0 for any configuration, Proposition 1 is refuted (or an implementation error is revealed).
- **Controls:** B1 (no runtime) as negative control; B3 (centralized monitor) as positive control for detection quality.
- **Assumption checks:** Normality of residuals (QQ-plot), homoscedasticity (residuals vs. fitted), multicollinearity (VIF < 5).

These models will be finalized in the separate pre-registration before any simulation is run.

### Transformations

No transformations are performed in v0.1.0 because no data exists.

For the proposed future evaluation (v1.0.0):
- Continuous metrics (M1–M8): log-transform if right-skewed (to be checked in pilot data).
- Count metrics (M9): analyze as-is (no transformation).
- Categorical variables (configuration, network size, scenario class): dummy-coding with reference category = full runtime assurance for configuration, 10 nodes for network size, S1 for scenario class.
- Centering: network size will be centered on its median (100 nodes) for interaction terms.

### Inference criteria

No inference is performed in v0.1.0 because no data exists.

For the proposed future evaluation (v1.0.0):
- **Primary criterion:** p < 0.05 (two-tailed) for the main effect of configuration on each metric M1–M9.
- **Multiple comparisons:** Holm-Bonferroni correction across the 9 metrics (adjusted α = 0.05/9 ≈ 0.0056 for the most conservative test).
- **Effect size:** Cohen's d reported for each comparison; d ≥ 0.5 considered practically significant.
- **Confidence intervals:** 95% CI reported for all estimates.
- **Pre-registered thresholds** (from Section 7.3 of the manuscript):
  - M1 ≥ 0.95 (detection rate)
  - M2 ≤ 0.05 (false-positive rate)
  - M3 ≤ 1 s median (detection latency)
  - M5 ≤ 10 s median (halt window)
  - M6 ≥ 0.99 (recovery correctness)
  - M9 = 0 (convergence preservation)
- **Falsification criterion:** If the full runtime assurance configuration does not outperform B1–B5 on any metric beyond the pre-registered threshold, F5 (observable benefit) is falsified.

### Data inclusion and exclusion

No data inclusion/exclusion criteria apply in v0.1.0 because no data exists.

For the proposed future evaluation (v1.0.0):
- **Inclusion:** All runs that complete within the pre-specified timeout (e.g., 10 minutes simulated time).
- **Exclusion:** Runs that crash due to implementation errors (not due to the phenomenon under study) will be excluded and reported separately.
- **Outliers:** No outlier removal; all runs reported. Sensitivity analysis with and without the 5% most extreme runs will be reported.
- **Missing data:** None expected (deterministic simulation); any missing data will be reported and cause identified.

### Missing data

No missing data exists in v0.1.0 because no data is collected.

For the proposed future evaluation (v1.0.0):
- The simulation is deterministic given a seed; no missing data is expected.
- If missing data occurs due to crashes or timeouts, it will be reported separately and the cause identified.
- No imputation will be performed; all analyses will use complete cases only.

### Other planned analysis

Secondary analyses planned for v1.0.0:
- **Ablation study:** Remove one layer at a time (monitoring, detection, containment, halt, recovery) and measure the impact on M1–M9. This isolates the contribution of each layer.
- **Sensitivity analysis:** Vary the gossip dissemination constant and the threshold Θ_max to assess robustness of conclusions.
- **Scalability analysis:** Measure M7 (monitoring overhead) as a function of network size.
- **Halt window distribution:** Report the full distribution of Δt_window (P2), not just the median.
- **Comparison with AetherFlow:** Direct comparison of AetherRuntime's monitoring against AetherFlow's operational verification, to test F1.

These secondary analyses are exploratory and will be reported separately.

---

## Other

### Context and additional information

AetherRuntime is the sixth functional dimension (provisional) of the Aether family. It investigates whether a runtime-assurance gap genuinely exists in the Aether family, and specifies a five-layer architecture (monitoring, detection, containment, halt, recovery) with two propositions (determinism of local anomaly detection; irreducible halt window).

No implementation is claimed. No real-world deployment has been evaluated. F1–F4 are not falsified by argument; F5 is untested.

**Core Links:**

- **Paper (Zenodo DOI):** https://doi.org/10.5281/zenodo.24078477
- **Website:** https://aetherruntime.netlify.app
- **GitHub:** https://github.com/gitdeeper15/aetherruntime
- **GitLab (mirror):** https://gitlab.com/gitdeeper15/aetherruntime
- **Codeberg (mirror):** https://codeberg.org/gitdeeper15/aetherruntime
- **Bitbucket (mirror):** https://bitbucket.org/gitdeeper15/aetherruntime
- **PyPI (planned):** https://pypi.org/project/aether-runtime/
- **ORCID:** https://orcid.org/0009-0003-8903-0029

**Aether Family (six functional dimensions):**

- **AetherGit (storage):** https://doi.org/10.5281/zenodo.23966896
- **AetherFlow (integration):** https://doi.org/10.5281/zenodo.23979129
- **AetherProof (verification):** https://doi.org/10.5281/zenodo.24013124
- **AetherMesh (decentralization):** https://doi.org/10.5281/zenodo.24038038
- **AetherGovern (governance):** https://doi.org/10.5281/zenodo.24054524
- **AetherRuntime (runtime assurance, provisional):** https://doi.org/10.5281/zenodo.24078477

**Record Identifiers:**

- **Record ID:** AETHERRUNTIME-01
- **Version:** 0.1.0
- **Release Date:** 2026-11-09
- **DOI:** 10.5281/zenodo.24078477
- **License:** MIT (code) + CC-BY-4.0 (docs, manuscript, figures)

**Status Summary:**

- Architectural Hypothesis Under Investigation (v0.1.0)
- No implementation claimed
- No real-world deployment evaluated
- No empirical results reported
- Propositions P1–P2 are proof sketches (not machine-checked)
- F1–F4 not falsified by argument; F5 untested
- The final project structure (single, dual, triple, or quadruple) is undetermined
- The paper is not peer reviewed

**Author:**

- **Name:** Samir Baladi
- **Affiliation:** Ronin Institute / Rite of Renaissance
- **Email:** gitdeeper@gmail.com
- **ORCID:** 0009-0003-8903-0029

---

## Metadata

### Contributors

Samir Baladi

### Resource type

No resource type

### Description

AetherRuntime is the sixth functional dimension (provisional) of the Aether family. It investigates whether a runtime-assurance gap genuinely exists in the Aether family, and specifies a five-layer architecture (monitoring, detection, containment, halt, recovery) with two propositions (determinism of local anomaly detection; irreducible halt window).

No implementation is claimed. No real-world deployment has been evaluated. F1–F4 are not falsified by argument; F5 is untested.

- DOI: 10.5281/zenodo.24078477
- Paper: 33 pages
- Status: Architectural Hypothesis Under Investigation (v0.1.0)
- Aether Family: sixth functional dimension (provisional)

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Associated project

https://osf.io/ft7ez

### Date Created

Nov 9, 2026, 10:21 AM

### Date registered

Nov 9, 2026, 10:21 AM

### Subjects

- Artificial Intelligence and Robotics
- Software Engineering
- Computer Sciences
- Arts and Humanities
- Philosophy of Science
- Physical Sciences and Mathematics
- Philosophy

### Tags

- aether family
- AetherRuntime
- anomaly detection
- containment
- decentralized systems
- Distributed Systems
- falsification
- halt
- monitoring
- multi-agent systems
- recovery
- runtime assurance
- Runtime Verification

### Affiliated Institutions

No affiliated institutions

### Funder Names

No information

### Language

No language

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/KZU7P

---

## Citations

### APA

Baladi, S. (2026, November 9). AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family. OSF. https://doi.org/10.17605/OSF.IO/KZU7P

### MLA

Baladi, Samir. "AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family." OSF, 9 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family." OSF. November 9. doi:10.17605/OSF.IO/KZU7P.

### BibTeX

```bibtex
@misc{baladi2026aetherruntime_osf,
  author       = {Baladi, Samir},
  title        = {{AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family}},
  year         = {2026},
  month        = nov,
  day          = {9},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/KZU7P},
  url          = {https://doi.org/10.17605/OSF.IO/KZU7P},
  note         = {OSF Preregistration. Associated project: https://osf.io/ft7ez}
}
```

---

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-09

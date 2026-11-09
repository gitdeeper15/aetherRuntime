# AetherRuntime — Changelog

All notable changes to this research project will be documented in this file.

## [2.0.0] — 2026-11-09

### Reference Implementation

First reference implementation of the AetherRuntime architecture
specified in v0.1.0.

**Published:**
- **Zenodo DOI:** [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477)
- **Figshare DOI:** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)
- **OSF Registration:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
- **PyPI:** `aether-runtime 2.0.0` (planned)
- **Website:** [aetherruntime.netlify.app](https://aetherruntime.netlify.app)

### Added — Operational Specification

- `docs/specification/01_entities.md` — entities for runtime assurance
- `docs/specification/02_operations.md` — operations
- `docs/specification/03_invariants.md` — invariants
- `docs/specification/04_interfaces.md` — interfaces with the Aether family
- `docs/specification/05_test_design.md` — test design

### Added — Source Code

- `src/aetherruntime/` package (15 modules):
  - `models.py` — core entities
  - `monitoring/` — `telemetry`, `baseline`
  - `detection/` — `classifier`, `alert`
  - `containment/` — `policy`, `isolation`
  - `halt/` — `order`, `quorum`
  - `recovery/` — `snapshot`, `replay`
  - `simulation/` — `Network`, `Node`, `Testbed`
  - `cli.py` — CLI (`aetherruntime info|verify`)

### Added — Tests

- `tests/` package (8 files, **60 tests**):
  - `test_models.py` — 10
  - `test_monitoring.py` — 8
  - `test_detection.py` — 8
  - `test_containment.py` — 8
  - `test_halt.py` — 8
  - `test_recovery.py` — 8
  - `test_simulation.py` — 10

### Added — Experiments

- `experiments/detection_accuracy/` — M1, M2 (detection rate, false positives)
- `experiments/halt_window/` — M5 (halt window)
- `experiments/recovery_correctness/` — M6 (recovery correctness)
- All three experiments reproducible via `python experiments/*/run.py`

### Added — Reports

- `REPORTS/v2.0.0/report.md` — full evaluation report

### Added — Packaging

- `pyproject.toml` — PEP 621 build config
- `upload_aetherruntime.py` — PyPI uploader
- `src/aetherruntime/py.typed` — PEP 561 marker

### Changed

- `VERSION`: 0.1.0 → 2.0.0
- `CITATION.cff`: 0.1.0 → 2.0.0
- `manifest.json`: 0.1.0 → 2.0.0
- `scientific_state.json`: 0.1.0 → 2.0.0
- `PROJECT_SUMMARY.txt`: 0.1.0 → 2.0.0
- `INVENTORY.md`: 0.1.0 → 2.0.0
- `README.md`: added v2.0.0 section
- `AUTHORS.md`: updated status to v2.0.0
- `CONTRIBUTING.md`: updated to v2.0.0
- `netlify.toml`: updated to v2.0.0
- `pyproject.toml`: updated to v2.0.0
- `requirements.txt`: updated to v2.0.0

### Related Identifiers

- **Zenodo DOI:** [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477)
- **Figshare DOI:** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)
- **OSF Registration:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
- **PyPI:** `aether-runtime 2.0.0` (planned)

### Status

| Dimension | Status |
|---|---|
| Manuscript (v0.1.0) | Complete (33 pages) |
| Implementation | ✅ Built (`src/aetherruntime/`, 15 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed |
| PyPI Package | ⏳ Not yet published |
| Real-world deployment | ❌ Not evaluated |
| Peer review | ❌ Not reviewed |

---

## [0.1.0] — 2026-11-09

### Architectural Hypothesis Under Investigation

First public release of AetherRuntime: a structured investigation of
whether a runtime-assurance gap genuinely exists in the Aether family.

**Published:**
- **Zenodo DOI:** [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477)
- **Figshare DOI:** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)
- **OSF Registration:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
- **Website:** [aetherruntime.netlify.app](https://aetherruntime.netlify.app)

### Added — Manuscript

- `PUBLICATION/AetherRuntime_Research_Paper.md` — 33-page research article (8,861 words)
- 6 figures (Fig1–Fig6) in `docs/figures/`
- `PAPER_PARTS/` — 17 paper sections (Markdown)

### Added — Methodology

- Falsification-first approach
- Five failure conditions (F1–F5)
- Five runtime layers (Monitoring, Detection, Containment, Halt, Recovery)
- Two propositions with proof sketches
- Twenty open questions (Q1–Q20)

### Added — Documentation

- `README.md`, `AUTHORS.md`, `CONTRIBUTING.md`, `INVENTORY.md`,
  `PROJECT_SUMMARY.txt`, `CITATION.cff`, `manifest.json`,
  `scientific_state.json`, `OSF_REGISTRATION.md`

### Related Identifiers

- **Zenodo DOI:** [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477)
- **Figshare DOI:** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)
- **OSF Registration:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)
- **PyPI:** Not published (v0.1.0 claims no implementation)

---

**Last Updated:** 2026-11-09
**Current Version:** 2.0.0

# AetherRuntime — Complete Inventory

**Version:** 2.0.0 (Reference Implementation)
**Release Date:** 2026-11-09
**Author:** Samir Baladi
**Email:** gitdeeper@gmail.com
**ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
**License:** MIT (code) · CC-BY-4.0 (docs, manuscript, figures)
**Status:** Reference Implementation with Reproducible Experiments
**Record ID:** AETHERRUNTIME-02
**DOI (Zenodo):** [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477)
**DOI (Figshare):** [10.6084/m9.figshare.34955746](https://doi.org/10.6084/m9.figshare.34955746)
**OSF:** [10.17605/OSF.IO/KZU7P](https://doi.org/10.17605/OSF.IO/KZU7P)

---

## Research Status

| Item | Status |
|---|---|
| Document type | Research article + reference implementation |
| Paper (v0.1.0) | Complete (33 pages) |
| Implementation (v2.0.0) | ✅ Built (`src/aetherruntime/`, 16 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed |
| PyPI package | ✅ Published (`aetherruntime-arch` 2.0.0) |
| Real-world deployment | None; no deployed system has been benchmarked |
| Propositions 1–2 | Stated with proof sketches; not machine-checked |
| Review status | Not peer reviewed |

---

## Repository Links

| Platform | URL | Role | Status |
|----------|-----|------|--------|
| GitHub | https://github.com/gitdeeper15/aetherruntime | Primary | ✅ Active |
| GitLab | https://gitlab.com/gitdeeper15/aetherruntime | Mirror | ✅ Active |
| Codeberg | https://codeberg.org/gitdeeper15/aetherruntime | Mirror | ✅ Active |
| Bitbucket | https://bitbucket.org/gitdeeper15/aetherruntime | Mirror | ✅ Active |
| PyPI | https://pypi.org/project/aetherruntime-arch/ | Python package | ✅ Published |
| Zenodo | https://doi.org/10.5281/zenodo.24078477 | DOI (v0.1.0 paper) | ✅ Published |
| Figshare | https://doi.org/10.6084/m9.figshare.34955746 | Preprint archive | ✅ Published |
| OSF | https://doi.org/10.17605/OSF.IO/KZU7P | Registration | ✅ Published |
| Website | https://aether-runtime.netlify.app | Live documentation | ✅ Active |
| ORCID | https://orcid.org/0009-0003-8903-0029 | Identity | ✅ Active |

---

## Manuscript Artifact (v0.1.0)

| File | Pages | Status |
|---|---|---|
| `PUBLICATION/AetherRuntime_Research_Paper.md` | 33 | ✅ Complete (8,861 words) |
| `PUBLICATION/AetherRuntime_Research_Paper.pdf` | 33 | ⚠️ Placeholder (reserved) |

---

## Root Files

| File | Purpose | Status |
|------|---------|:-:|
| `.gitignore` | Git ignore rules | ✅ |
| `AUTHORS.md` | Contributors | ✅ Updated |
| `CHANGELOG.md` | Version history (v0.1.0 + v2.0.0) | ✅ Updated |
| `CITATION.cff` | Citation metadata (v2.0.0) | ✅ Updated |
| `CONTRIBUTING.md` | Contribution guidelines | ✅ Updated |
| `INVENTORY.md` | This file | ✅ Updated |
| `LICENSE` | MIT + CC-BY-4.0 | ✅ |
| `PROJECT_SUMMARY.txt` | One-page summary (v2.0.0) | ✅ Updated |
| `README.md` | Main documentation (v2.0.0) | ✅ Updated |
| `VERSION` | `2.0.0` | ✅ Updated |
| `manifest.json` | Project manifest (v2.0.0) | ✅ Updated |
| `scientific_state.json` | Scientific state record (v2.0.0) | ✅ Updated |
| `netlify.toml` | Netlify configuration | ✅ Updated |
| `pyproject.toml` | PEP 621 build config (v2.0.0) | ✅ |
| `requirements.txt` | Python dependencies (v2.0.0) | ✅ Updated |
| `upload_aetherruntime.py` | PyPI uploader | ✅ |

---

## Directories

| Directory | Contents | Status |
|-----------|----------|:-:|
| `src/aetherruntime/` | Reference implementation (16 modules) | ✅ |
| `tests/` | Test suite (7 files, 60 tests) | ✅ |
| `experiments/` | 3 reproducible experiments | ✅ |
| `docs/specification/` | 5 operational specification files | ✅ |
| `docs/figures/` | 6 figures (Fig1–Fig6) | ✅ |
| `PUBLICATION/` | Paper (MD + PDF placeholder) + Netlify site | ✅ |
| `PAPER_PARTS/` | 17 markdown files (paper sections) | ✅ |
| `REPORTS/v2.0.0/` | Evaluation report | ✅ |
| `DATA/` | (empty) | — |
| `ANALYSIS/` | (empty) | — |
| `EXTERNAL_REVIEW/` | (empty) | — |
| `VALIDATION/` | (empty) | — |

---

## Source Code (`src/aetherruntime/`)

| Module | Files | Purpose |
|---|:-:|---|
| `models.py` | 1 | 10 entities, 4 enums |
| `__version__.py` | 1 | Version info |
| `__init__.py` | 1 | Public API (117 exports) |
| `cli.py` | 1 | CLI (`info\|verify\|simulate\|experiment`) |
| `monitoring/telemetry.py` | 1 | `collect` |
| `monitoring/baseline.py` | 1 | `update_baseline` |
| `detection/classifier.py` | 1 | `detect` |
| `detection/alert.py` | 1 | `AlertRegistry` |
| `containment/policy.py` | 1 | `contain` |
| `containment/isolation.py` | 1 | `IsolationManager` |
| `halt/order.py` | 1 | `propose_halt` |
| `halt/quorum.py` | 1 | `approve_halt` |
| `recovery/snapshot.py` | 1 | `create_snapshot` |
| `recovery/replay.py` | 1 | `recover` |
| `simulation/network.py` | 1 | `Network` |
| `simulation/node.py` | 1 | `Node` |
| `simulation/testbed.py` | 1 | `Testbed` |

**Total:** 16 modules, ~4,520 lines.

---

## Test Suite (`tests/`)

| File | Tests |
|---|:-:|
| `test_models.py` | 10 |
| `test_monitoring.py` | 8 |
| `test_detection.py` | 8 |
| `test_containment.py` | 8 |
| `test_halt.py` | 8 |
| `test_recovery.py` | 8 |
| `test_simulation.py` | 10 |
| **Total** | **60** |

**Result:** ✅ **60/60 passed**.

---

## Experiments (`experiments/`)

| # | Directory | Metrics | Results |
|:-:|---|---|:-:|
| 1 | `detection_accuracy/` | M1, M2 | ✅ `results.json` |
| 2 | `halt_window/` | M5 | ✅ `results.json` |
| 3 | `recovery_correctness/` | M6 | ✅ `results.json` |

---

## Figures (`docs/figures/`)

| File | Figure | Description |
|---|:-:|---|
| `Fig1_Six_Dimensions.png` | Fig 1 | Six functional dimensions |
| `Fig2_Runtime_Layers.png` | Fig 2 | Five runtime layers |
| `Fig3_Runtime_Lifecycle.png` | Fig 3 | Runtime lifecycle |
| `Fig4_Anomaly_Detection.png` | Fig 4 | Anomaly detection challenge |
| `Fig5_Runtime_vs_Verification.png` | Fig 5 | Runtime vs verification |
| `Fig6_Runtime_State_Machine.png` | Fig 6 | Runtime state machine |

---

## Companion Works

AetherRuntime is the **sixth functional dimension** (provisional) of the Aether family:

| # | System | Dimension | DOI |
|:-:|---|---|---|
| 1 | AetherGit | Storage | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| 2 | AetherFlow | Integration | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| 3 | AetherProof | Verification | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| 4 | AetherMesh | Decentralization | [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038) |
| 5 | AetherGovern | Governance | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) |
| 6 | **AetherRuntime** (provisional) | **Runtime Assurance** | [10.5281/zenodo.24078477](https://doi.org/10.5281/zenodo.24078477) |

---

## Citation

### Paper (v0.1.0)

```bibtex
@techreport{baladi2026aetherruntime,
  author       = {Baladi, Samir},
  title        = {AetherRuntime: A Falsification-First Investigation of
                  Runtime Assurance in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24078477},
  url          = {https://doi.org/10.5281/zenodo.24078477}
}
```

Software (v2.0.0)

```bibtex
@software{baladi2026aetherruntime_v2,
  author       = {Baladi, Samir},
  title        = {{AetherRuntime} v2.0.0: Reference Implementation of the
                  Runtime Assurance Architecture},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24078477},
  url          = {https://pypi.org/project/aetherruntime-arch/},
  note         = {Reference implementation. Available via pip install aetherruntime-arch.}
}
```

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24078477
· Figshare DOI: 10.6084/m9.figshare.34955746
· OSF: 10.17605/OSF.IO/KZU7P
· Website: aether-runtime.netlify.app
· GitHub: gitdeeper15/aetherruntime

---

Last Updated: 2026-11-09
Current Version: 2.0.0

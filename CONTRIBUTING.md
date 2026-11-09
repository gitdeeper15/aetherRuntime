# Contributing to AetherRuntime

**AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family**

---

## Status

This project is an **architectural hypothesis under investigation** (`v0.1.0`) of the AetherRuntime runtime-assurance architecture.

**No implementation is claimed.** No real-world deployment has been evaluated. F1–F4 are not falsified by argument; F5 is untested. Propositions P1–P2 are stated with proof sketches, not machine-checked. The final project structure (single, dual, triple, or quadruple) remains undetermined.

Contributions at this stage are welcome in:

- **Implementation:** Bug fixes, new features, or improved modularity.
- **Formal analysis:** Encoding attempts for F2, model checks for Proposition 1.
- **Figures:** Redrawn or improved diagrams.
- **Documentation:** Examples, tutorials, or improved explanations.
- **Review:** Independent review of F1–F5, the requirement list R1–R6, and the thresholds.

**Not accepted at this stage:**

- Empirical claims presented as findings (no implementation has been built).
- Claims that "not falsified" means "confirmed" — it does not.
- Changes to the failure conditions, requirements, or propositions without a documented rationale.
- Claims that an implementation exists (none does).

For extensions, open an issue first to discuss scope.

---

## Reporting Issues

Open an issue with:

- A one-sentence description.
- The affected section (e.g., Section 5.7.1, Proposition 1).
- A minimal reproduction or screenshot.
- Expected vs. actual behavior.
- For scientific claims: cite the specific failure condition (`F*`), requirement (`R*`), or proposition (`P*`) affected.

---

## Submitting Changes

```bash
git checkout -b feature/short-description
# make changes
git commit -m "feat: short description"
git push origin feature/short-description
```

Then open a pull request. Each PR should address one concern.

---

Standards

Language Standard
Python PEP 8, line length 100, ruff (when implementation is added)
Markdown markdownlint (MD013 disabled)
YAML yamllint
JSON valid JSON (verify with python3 -m json.tool)
TOML valid TOML (verify with python3 -c "import tomllib; ...")

---

Scientific Integrity Requirements

Because this is a research record with a published DOI, contributions must preserve:

1. Evidentiary status. No claim may be strengthened beyond what the manuscript supports. "Not falsified by argument" must never be read as "confirmed". Propositions 1–2 must remain labeled as proof sketches.
2. Failure condition transparency. Any claim that bears on F1–F5 must state which condition it bears on and what evidence would falsify it.
3. Limitation disclosure. Contributions that add results must also add the corresponding threats to validity.
4. Negative commitments. The following must remain explicit in all derived documents:
   · No implementation is claimed.
   · No real-world deployment has been evaluated.
   · F5 (observable benefit) is untested.
   · The final project structure (single, dual, triple, or quadruple) is undetermined.
   · The paper is not peer reviewed.
5. No silent corrections to published records. The Zenodo DOI 10.5281/zenodo.24078477 archives the v0.1.0 manuscript. Corrections must be issued as a new version with its own DOI.

---

Review Process

· All changes are reviewed by the maintainer (Samir Baladi).
· Changes to the specification, failure conditions, or propositions require explicit documentation in CHANGELOG.md with rationale.
· Changes that affect the published manuscript must be coordinated with a new Zenodo version, not a silent edit.

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24078477
· Website: aetherruntime.netlify.app
· GitHub: gitdeeper15/aetherruntime

---

Thank you for helping improve the falsification-first investigation of runtime assurance in the Aether family.

# LLM Threat Modeling Framework — Release Manifest

**Release:** v1.7 correction pass
**Date:** 2026-06-24
**Status:** Pilot candidate pending team-specific assessment and sign-off

## Purpose

This manifest records the coherent corpus state after the red-team correction pass. It is the release pointer for teams deciding which synthesis files belong together.

## Included synthesis files

| File | Version / state | Role |
|---|---|---|
| `synthesis/framework.md` | v1.7 | Umbrella framework, release history, regulatory baseline |
| `synthesis/threat-taxonomy.md` | v1.7 | Master threat taxonomy and evidence calibration |
| `synthesis/risk-matrix.md` | v1.7 | Machine-checkable base/elevated risk scores and corrected regulatory mapping |
| `synthesis/defense-playbook.md` | v1.7 | Defense controls, effectiveness notes, operational gaps, interaction analysis |
| `synthesis/assessment-template.md` | v1.7 | Engineering worksheet and residual-risk scoring rubric |
| `synthesis/quick-reference.md` | v1.7 | One-page operator reference |
| `synthesis/attack-surface-catalog.md` | v1.3 | Attack surface inventory; ISC references synced in prior pass |
| `synthesis/asset-inventory.md` | v1.0 | Protected assets inventory |
| `synthesis/assumptions.md` | v1.0 | Explicit assumptions and deployment boundaries |
| `synthesis/attack-trees.md` | v1.2 | Attack trees and kill-chain diagrams |

## Correction pass summary

- Residual-risk math now reduces risk only when preventive controls are actually implemented.
- EU AI Act mappings now distinguish Articles 9, 10, 13, 14, 15, and 17 correctly.
- Risk matrix separates `Base Score`, `Elevation Condition`, and `Elevated Score`.
- Assessment worksheet includes `SC-DEF-4`, `DET-DEF-1`, and `DET-DEF-2` handling.
- Defense-playbook malformed tables were normalized.
- ISC quick-reference wording uses attacker-controlled or attacker-shaped harness execution as the applicability gate.
- Evidence-provenance rule remains active: primary/corroborated sources carry Wild_vs_Theory; press/community narratives are context only.

## Pilot caveat

This release is suitable as a pilot candidate only after the assessing team fills out the worksheet for its actual deployment. The framework does not certify a deployment safe by itself.

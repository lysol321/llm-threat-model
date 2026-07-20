# LLM Threat Modeling Framework — Release Manifest

**Release:** v1.9 agentic trust-boundary integration
**Date:** 2026-07-20
**Status:** Pilot candidate pending team-specific assessment and sign-off

## Purpose

This manifest is the canonical pointer for the coherent v1.9 corpus. Component versions are independent; the table below identifies the exact versions that belong to this release.

## Included synthesis files

| File | Version / state | Role |
|---|---|---|
| `synthesis/framework.md` | v1.9 | Umbrella framework, release history, and operational architecture |
| `synthesis/threat-taxonomy.md` | v1.8 | Master taxonomy with canonical agentic subtype IDs and evidence calibration |
| `synthesis/risk-matrix.md` | v1.9 | Machine-checkable base/elevated scores, Wild_vs_Theory gates, and regulatory mapping |
| `synthesis/defense-playbook.md` | v1.8 | Defense controls, ownership, limitations, and assurance gaps |
| `synthesis/assessment-template.md` | v1.9 | Engineering worksheet, routing, control ratings, and residual-risk workflow |
| `synthesis/quick-reference.md` | v1.8 | Operator triage and decision gates |
| `synthesis/attack-surface-catalog.md` | v1.4 | Classical and agentic trust-boundary surface inventory |
| `synthesis/attack-trees.md` | v1.5 | Three canonical chains plus scoped agentic branches with canonical metadata and node IDs |
| `synthesis/asset-inventory.md` | v1.1 | Protected assets, including durable memory, skills, identity, relay, and provenance |
| `synthesis/assumptions.md` | v1.1 | Explicit behavior, deployment, identity, and trust-boundary assumptions |

## Operational and generated artifacts

| Artifact | Release state | Validation |
|---|---|---|
| `evaluation/scenario-suite.json` | 25 scenarios; nine v1.9 agentic cases | `python scripts/test_scenario_suite.py` |
| `threat-model-data.json` | Structured source v1.9 | `python scripts/test_corpus_coherence.py` |
| `llm-threat-model.html` | Generated from structured source and current Markdown | `python scripts/build-html.py --check` |
| `research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md` | Evidence note; June 4 source labeled pre-window corroboration | Citation and corpus checks |
| `review/red-team-2026-07-20-agentic-update.md` | Adversarial review that drove v1.9 | Findings preserved as review history |

## v1.9 release changes

- Added canonical subtypes T01-SESSION, T03-SKILL, T05-CAPABILITY, T09-MEMORY, T09-IDENTITY, T10-CUA, T10-REPRESENTATION, and T11-RELAY without creating new top-level categories.
- Calibrated agentic overlays to Wild_vs_Theory 1–2 and base/elevated scores 4–10. No new overlay is HIGH without evidence meeting the framework gate.
- Integrated MEM-DEF-1, SKILL-DEF-1, MA-DEF-3, CUA-DEF-1, RELAY-DEF-1, DET-DEF-3, and REP-DEF-1 into worksheet routing, PARTIAL definitions, and residual-risk lookup.
- Added executable scenarios for memory, skill retrieval, skill update/rug pull, agent identity, computer use, session contamination, relay tampering, representation confusion, and capability disclosure.
- Distinguished relay accountability from upstream authorization. Without a direct trusted path or provider-authenticated response, the assurance gap remains unresolved.
- Added durable memory, skill registry, agent identity credentials, relay transcripts, provider trust anchors, and representation provenance to the foundation assets and assumptions.
- Synchronized the structured data source and generated HTML.

## Evidence caveats

- Response-path relay tampering remains provisional at Wild_vs_Theory 1/5 pending independent replication.
- Representation confusion remains monitored at Wild_vs_Theory 1/5 and must be reproduced in the assessed conversion pipeline before elevation.
- Vendor red-team reporting and controlled benchmarks support inclusion but do not establish widespread in-wild exploitation.
- The Microsoft June 4 source is outside the strict June 20–July 20 scan window and is retained only as pre-window corroboration.

## Pilot caveat

The corpus is suitable as a pilot candidate only after the assessing team completes the v1.9 worksheet for its actual deployment. The framework does not certify a deployment safe by itself.

## Release validation

Run from the repository root:

```bash
python scripts/citation_drift_detector.py
python scripts/test_scenario_suite.py
python scripts/test_corpus_coherence.py
python scripts/build-html.py --check
```

The release is coherent only when all four commands pass and `git diff --check` reports no errors.
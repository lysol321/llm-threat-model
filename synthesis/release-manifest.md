# LLM Threat Modeling Framework — Release Manifest

**Release:** v1.12 September threat-model review and evidence update
**Date:** 2026-09-19
**Status:** Pilot candidate pending team-specific assessment and sign-off

## Purpose

This manifest is the canonical pointer for the coherent v1.12 corpus. Component versions are independent; the table below identifies the exact versions that belong to this release.

## Included synthesis files

| File | Version / state | Role |
|---|---|---|
| `synthesis/framework.md` | v1.12 | Umbrella framework, release history, and operational architecture |
| `synthesis/threat-taxonomy.md` | v1.11 | Master taxonomy with canonical agentic subtype IDs and evidence calibration |
| `synthesis/risk-matrix.md` | v1.12 | Machine-checkable base/elevated scores, Wild_vs_Theory confidence, and regulatory mapping |
| `synthesis/defense-playbook.md` | v1.11 | Defense controls, ownership, limitations, and assurance gaps |
| `synthesis/assessment-template.md` | v1.12 | Engineering worksheet, routing, control ratings, and residual-risk workflow |
| `synthesis/quick-reference.md` | v1.11 | Operator triage and decision gates |
| `synthesis/attack-surface-catalog.md` | v1.7 | Classical and agentic trust-boundary surface inventory |
| `synthesis/attack-trees.md` | v1.8 | Three canonical chains plus scoped agentic branches with canonical metadata and node IDs |
| `synthesis/asset-inventory.md` | v1.3 | Protected assets, including durable memory, skills, identity, relay, and provenance |
| `synthesis/assumptions.md` | v1.4 | Explicit behavior, deployment, identity, and trust-boundary assumptions |

## Operational and generated artifacts

| Artifact | Release state | Validation |
|---|---|---|
| `evaluation/scenario-suite.json` | 39 documented tabletop scenarios; includes monitor, compaction, cleanup and configuration regressions | `python scripts/test_scenario_suite.py` |
| `threat-model-data.json` | Structured source v1.12 | `python scripts/test_corpus_coherence.py` |
| `llm-threat-model.html` | Generated from structured source and current Markdown | `python scripts/build-html.py --check` |
| `research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md` | Evidence note; June 4 source labeled pre-window corroboration | Citation and corpus checks |
| `review/red-team-2026-07-20-agentic-update.md` | Adversarial review that drove v1.9 | Findings preserved as review history |

## September 19 research integration

`research/sources/Latest-Development-Integration-2026-09-19.md` records adoption of four scoped recommendations and deferred/backfill items. `research/sources/Latest-Development-Evidence-2026-09-19.json` preserves the source/claim ledger. `review/research-integration-2026-09-19.md` records verification and deliberate-defect checks. The research does not establish new field prevalence; required deployment tests are not claimed as executed.

## September 19 corrections

`review/corrections-2026-09-19.md` records the six findings, completed assessment records and negative controls. The new evidence note is `research/sources/Review-Corrections-2026-09-19.md`.

## September 15 corrections

Read `framework.md` v1.10 revision notes and `review/red-team-2026-09-15.md` for the corrected findings and follow-up review. `research/sources/Landscape-Update-2026-09.md` separates new publications from older incidents; `review/verification-2026-09-15.md` records checks and limitations.

## Retained July coverage

- Added canonical subtypes T01-SESSION, T03-SKILL, T05-CAPABILITY, T09-MEMORY, T09-IDENTITY, T10-CUA, T10-REPRESENTATION, and T11-RELAY without creating new top-level categories.
- In July, calibrated agentic overlays to Wild_vs_Theory 1–2 and base/elevated scores 4–10. These are baseline scores; higher reachable-chain or documented deployment scores take precedence. Evidence confidence does not cap risk.
- Integrated MEM-DEF-1, SKILL-DEF-1, MA-DEF-3, CUA-DEF-1, RELAY-DEF-1, DET-DEF-3, and REP-DEF-1 into worksheet routing, PARTIAL definitions, and residual-risk lookup.
- Added structured tabletop scenarios for memory, skill retrieval, skill update/rug pull, agent identity, computer use, session contamination, relay tampering, representation confusion, and capability disclosure.
- Distinguished relay accountability from upstream authorization. Without a direct trusted path or provider-authenticated response, the assurance gap remains unresolved.
- Added durable memory, skill registry, agent identity credentials, relay transcripts, provider trust anchors, and representation provenance to the foundation assets and assumptions.
- Synchronized the structured data source and generated HTML.

## September evidence update

- Category 1/2 confidence is 4/5 for field AI-wrapper key theft; EchoLeak remains 3/5 individually.
- T03-SKILL is 4/5 for malicious distribution, T09-MEMORY 3/5 broadly and InjecMEM 2/5 specifically. Baseline scores are not evidence-based ceilings.
- Existing controls now cover MCP version/authorization/cache/approval boundaries, build/runtime packages, memory ingestion, protected enforcement artifacts and independent logs.

## Evidence caveats

- Response-path relay tampering remains provisional at Wild_vs_Theory 1/5 pending independent replication.
- Representation confusion remains monitored at Wild_vs_Theory 1/5 and must be reproduced in the assessed conversion pipeline before elevation.
- Vendor red-team reporting and controlled benchmarks support inclusion but do not establish widespread in-wild exploitation.
- The Microsoft June 4 source is outside the strict June 20–July 20 scan window and is retained only as pre-window corroboration.

## Pilot caveat

The corpus is suitable as a pilot candidate only after the assessing team completes the v1.12 worksheet for its actual deployment. The framework does not certify a deployment safe by itself.

## Release validation

Run from the repository root:

```bash
python scripts/citation_drift_detector.py
python scripts/test_scenario_suite.py
python scripts/test_corpus_coherence.py
python scripts/build-html.py --check
```

The release is coherent only when all four commands pass and `git diff --check` reports no errors.

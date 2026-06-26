# AGENTS.md

## What this repo is

A research + synthesis project for LLM threat modeling. Pure markdown — no build system, no app code. The output is a versioned framework corpus in `synthesis/`.

## Directory structure

- `synthesis/` — The framework (umbrella, taxonomy, risk matrix, defense playbook, attack trees, assessment template, quick reference). This is the primary deliverable.
- `research/` — Source material: concepts, entities, sources, questions. Research foundation behind the framework.
- `review/` — Adversarial review rounds (rounds 1–18). Red-team critique history.
- `evaluation/` — Scenario suite (`scenario-suite.json`) and results. Validation of the framework against 16 deployment scenarios.
- `scripts/` — One test file: `test_scenario_suite.py`. Validates scenario suite integrity.
- `tmp/` — Working files (HTML content/design, review drafts). Not part of the corpus.

## Evidence-provenance rule

The framework's credibility depends on sourced claims. When editing synthesis or research files:

- **Primary/corroborated sources** carry Wild_vs_Theory ratings and risk claims.
- **Press/community narratives** are context only — they do not carry risk ratings.
- Every major conclusion in scenario evaluations must cite `synthesis/` file + line range.

If you can't verify a claim against a source in the corpus, don't write it.

## Versioning

Framework docs are versioned independently. Check version headers at the top of each synthesis file. `release-manifest.md` is the canonical pointer for which synthesis files belong to a release.

When updating framework documents, bump the version in the file header and add a revision note to `framework.md` if the change is substantive (new threats, revised risk scores, structural changes).

## Running tests

```bash
python scripts/test_scenario_suite.py
```

No dependencies. Pure stdlib. Validates that `evaluation/scenario-suite.json` has exactly 16 scenarios, 9 pass/fail criteria, required capability coverage, and all scenarios pass.

## Citation drift

`scenario-suite.json` evidence citations (`source` + `lines` + `quote`) must stay in sync with synthesis files. When synthesis documents change, citations can drift.

**Tools:**
- `scripts/citation_drift_detector.py` — detect and fix citation drift
- `scripts/test_scenario_suite.py` — CI gate for citation validity

**Workflow:**

```bash
# Detect drift
python scripts/citation_drift_detector.py

# Fix: auto-refresh line ranges where quote text still exists verbatim
python scripts/citation_drift_detector.py --fix

# If quotes are also drifted (text edited, not just moved):
# 1. Extract candidate verbatim quotes from current content
python scripts/citation_drift_detector.py --requote
# 2. Batch-update all 98 quotes to verbatim extracts
python scripts/citation_drift_detector.py --batch-requote

# Verify
python scripts/test_scenario_suite.py
```

**Two drift types:**
- **Range drift**: content moved to different lines → `--fix` updates line numbers
- **Quote drift**: quote text was edited → `--batch-requote` replaces with verbatim extract

`test_scenario_suite.py` runs three citation checks: range bounds, quote match, and CI gate. `test_quotes_match_cited_lines` fails when a quote is not verbatim inside its cited range. `test_no_drifted_citations` fails when any citation is not fully valid.

## Key conventions

- **Wild_vs_Theory scale** (1–5): Grounds claims in observed-in-wild vs theoretical. 1 = purely theoretical, 5 = widespread in production. Embedded in threat-taxonomy.md and defense-playbook.md.
- **Attack chain vocabulary**: Chains A/B/C are defined in `attack-trees.md`. Use their node names when referencing chains elsewhere.
- **Defense ownership tags**: [DEV], [OPS], [PROV] on every defense in `defense-playbook.md`.
- **Control type distinction**: Infrastructure-enforced vs alignment-based. Confusing these is a documented threat (Category 13).
- **Assessment template**: `assessment-template.md` is the engineering worksheet. Scoring rubric appendix is included.

## Scope boundary

This framework addresses **LLM-as-target** threats (attacks on the LLM system). It does not fully cover **LLM-as-attack-vector** misuse (using LLMs for phishing, disinformation). Don't blur this boundary when editing.

## Framework reading order

If you need to understand the framework, follow the order in `framework.md` § Architecture: assumptions → assets → attack surfaces → quick reference → assessment template → threat taxonomy → defense playbook → risk matrix.

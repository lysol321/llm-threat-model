# Threat-model corrections — 2026-09-19

**Release:** v1.11
**Scope:** Correct the six findings from the current threat-model review; preserve existing working-tree changes and historical review records.

## Finding dispositions

| Finding | Correction | Primary artifacts |
|---|---|---|
| P1: PI-DEF-4 omitted enforcement at output consumers | Added browser/Markdown/email, database, command/code/filesystem, and HTTP/broker controls; enforce before first render, execution or disclosure. Schema and semantic checks alone do not satisfy this control. | `synthesis/defense-playbook.md`, worksheet, quick reference; SCN-34-OUTPUT |
| P1: No tools or trusted users could incorrectly imply LOW | Removed the no-tools/direct-only LOW shortcuts; assess every answer, renderer, query and tool consumer. Trusted users narrow only direct attacker assumptions. | `synthesis/assessment-template.md`, `synthesis/assumptions.md`, Chain A; SCN-26-NO-TOOLS |
| P2: Poisoned facts were conflated with instruction injection | Added DATA-DEF-1 and a separate data-integrity path covering writer authority, independent factual checks, provenance/change tracking and recovery of derived artifacts. PI defenses alone earn no prevention credit for false facts. | Playbook, taxonomy, matrix, surfaces, attack trees, worksheet; SCN-35-FACTS |
| P2: Scenario PASS records lacked actual assessments | Completed all 33 existing records and added two regressions. Each includes explicit hypothetical assumptions, rated controls, risk arithmetic, decision, action, owner and evidence. Rebuilt the results and updated the worked example. | `evaluation/scenario-suite.json`, results, walkthrough; `scripts/test_scenario_suite.py` |
| P2: EU AI Act duties were conflated | Added classification and role applicability gates separating high-risk system requirements, provider/deployer duties, GPAI-provider duties, systemic-risk duties and transparency obligations. Unresolved classification requires a legal owner, not a compliance claim. | Worksheet, assumptions, matrix, framework, quick reference |
| P2: README release and evidence claims were stale | Synchronized release, scenario count and all 14 evidence ratings with the structured source. Distinguished the individual EchoLeak demonstration from broader field evidence. | `README.md`, release manifest, `threat-model-data.json`, generated HTML; coherence check |

Substantive synthesis documents have independent version bumps recorded in the release manifest. The framework revision notes describe this release. No dependencies were added.

The source basis is recorded in `research/sources/Review-Corrections-2026-09-19.md`: OWASP LLM04/LLM05, the consolidated EU AI Act and Cato's EchoLeak analysis. This correction does not introduce new observed-in-the-wild ratings or measured control-efficacy claims.

## Verification

The following checks passed on the corrected corpus:

| Command | Result |
|---|---|
| `python -B scripts/test_scenario_suite.py` | PASS: 35 documented tabletop assessments, including recorded control ratings, arithmetic, action/owner and evidence checks |
| `python -B scripts/test_corpus_coherence.py` | PASS: 14 coherence checks |
| `python -B scripts/citation_drift_detector.py` | 316 checked, 316 matched, zero drift |
| `python -B scripts/build-html.py --check` | PASS: generated artifact matches its sources |

The checks below were exercised by changing a disposable copy of the corpus, invoking the named check, requiring its failure, and restoring the original bytes. All 23 injected defects were rejected. The full release checks passed after restoration. Existing unchanged checks were run but were not newly negative-controlled in this pass; earlier verification remains in the historical review records.

## Deliberate-defect results

| Check | Injected defect | Observed rejection |
|---|---|---|
| `test_recorded_assessments` | Delete SCN-01 assessment | `SCN-01: incomplete assessment context` |
| `test_recorded_assessments` | Empty SCN-01 risk list | `SCN-01: no recorded risks` |
| `test_recorded_assessments` | Delete SCN-01 residual | `SCN-01/Chain A: missing scoring fields ['residual']` |
| `test_recorded_assessments` | Remove SCN-01 action | `SCN-01/Chain A: missing decision inputs or action/owner` |
| `test_recorded_assessments` | Invalid control rating | `SCN-01/Chain A: invalid control rating/type/reason` |
| `test_recorded_assessments` | Use logging as primary prevention | `SCN-01/Chain A: invalid primary preventive controls` |
| `test_recorded_assessments` | Likelihood 6 with consistent base 30 | `SCN-01/Chain A: invalid likelihood/impact/base` |
| `test_recorded_assessments` | Use unsupported mitigation 0.5 | `SCN-01/Chain A: invalid factors` |
| `test_recorded_assessments` | Give prevention credit to factual-poisoning case | `SCN-35-FACTS/RAG Context Poisoning: unsupported preventive credit` |
| `test_recorded_assessments` | Discount all-NO primary controls | `SCN-35-FACTS/RAG Context Poisoning: unsupported preventive credit` |
| `test_recorded_assessments` | Claim all-infrastructure credit for mixed partial controls | `SCN-12/Contained official-model evaluation: unsupported preventive credit` |
| `test_recorded_assessments` | Ignore PARTIAL agency multiplier | `SCN-01/Chain A: agency factor disagrees with scope/control` |
| `test_recorded_assessments` | Record residual 20 instead of 21 | `SCN-01/Chain A: recorded residual 20 != computed 21` |
| `test_recorded_assessments` | Label critical residual LOW | `SCN-01/Chain A: tier/decision disagrees with residual` |
| `test_recorded_assessments` | Add nonexistent risk evidence | `SCN-01/Chain A: missing or unknown risk evidence` |
| `test_recorded_assessments` | Use a base absent from cited framework row | `SCN-01/Chain A: framework score unsupported by cited row` |
| `test_recorded_assessments` | Rate open renderer disclosure LOW | `SCN-26-NO-TOOLS: open disclosure path cannot receive LOW` |
| `test_readme_matches_current_release` | Revert README release | `README release disagrees with structured source` |
| `test_readme_matches_current_release` | Revert README scenario count | `README scenario count disagrees with suite` |
| `test_readme_matches_current_release` | Inflate README ISC rating | `README threat evidence ratings disagree with structured source` |
| `test_readme_matches_current_release` | Restore README EchoLeak field claim | `README EchoLeak evidence is stale` |
| `test_scenario_suite_covers_new_attack_paths` | Remove factual-poisoning regression ID | `required scenarios missing: ['SCN-35-FACTS']` |
| `test_canonical_ids_are_threaded_through_operational_docs` | Remove DATA-DEF-1 from triage | `DATA-DEF-1` |

## Limits of the evidence

These are hypothetical tabletop assessments, not deployment observations. Added control states and deployment conditions are explicit assumptions. PASS establishes a complete, internally checked record; a scenario can correctly PASS while its risk decision is CRITICAL/BLOCK. The selected risk records are scoped examples, not exhaustive deployment inventories.

Citation checks establish a matching location, not semantic entailment. Arithmetic and consistency checks cannot establish factual truth, control effectiveness or legal applicability. No exploit was run against a deployed system, no production controls were verified, and no browser interaction or visual verification is claimed. Generated HTML content was checked against its sources; UI behavior was unchanged. Deployment evidence and responsible team sign-off remain necessary.

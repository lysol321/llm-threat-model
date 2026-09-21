# Research integration verification — September 19, 2026

**Release:** v1.12. **Scope:** Integrate the approved research recommendations into existing threat categories and controls; retain evidence limitations and existing base scores/Wild_vs_Theory ratings.

## Implemented changes

- REP-DEF-1/DET-DEF-3 now address trusted live-monitor framing and relevant history; PI-DEF-4/SC-DEF-2/AGENCY-DEF-2 bind delayed execution to approved immutable code/dependencies or reauthorization after mutation.
- MEM-DEF-1 applies to ephemeral compaction/resume even without durable storage; summaries cannot create user authority or erase genuine denials.
- DOS-DEF-1 covers retained state and cleanup after rejection, cancellation, abort and timeout, including pre-scheduling failures in distributed inference.
- Material watermark/logit/sampling and monitor/compactor changes require paired denied and legitimate case revalidation. Independently demonstrated infrastructure controls retain their evidence; configuration change alone is not proof of compromise.
- Added SCN-36-MONITOR, SCN-37-COMPACTION, SCN-38-CLEANUP and SCN-39-CONFIG. Each has control ratings, explicit hypothetical assumptions, deployment score rationale, residual decision/action/owner, and cited adversarial/legitimate deployment plans marked NOT_RUN.
- Updated the worksheet's main applicability/routing/rating gates, operator triage, assets, surfaces, path variants, assumptions, taxonomy, scoring guidance, worked example, release manifest, README, structured navigation and generated HTML. Navigation now checks component versions and scenario counts, including the manifest entry.
- Preserved the source/claim ledger and added a bounded evidence note. Provider notices' September 16 dates are recorded as updates, not unverified original publication dates. MCP backfill and CaMeLoT watch status do not raise evidence ratings.

## Release checks

The four release commands passed against the integrated corpus: `test_scenario_suite.py` (39 scenarios), `test_corpus_coherence.py` (14 checks), `citation_drift_detector.py` (362 matching citations; zero drift), and `build-html.py --check` (generated artifact matches). `git diff --check` is also required when applying to the repository. All commands use the existing Python stdlib tools; no dependencies or application/UI logic were added.

## Deliberate-defect checks

All 13 mutations below were applied only to a disposable staging copy, required to fail with the indicated assertion, and restored byte-for-byte. Each targeted check passed before injection and after restoration. Unchanged checks were run normally; earlier negative-control evidence remains in prior review records.

| Check | Injected defect | Observed rejection |
|---|---|---|
| `test_scenario_suite_covers_new_attack_paths` | Remove SCN-36-MONITOR | `required scenarios missing: ['SCN-36-MONITOR']` |
| `test_scenario_suite_covers_new_attack_paths` | Remove SCN-37-COMPACTION | `required scenarios missing: ['SCN-37-COMPACTION']` |
| `test_scenario_suite_covers_new_attack_paths` | Remove SCN-38-CLEANUP | `required scenarios missing: ['SCN-38-CLEANUP']` |
| `test_scenario_suite_covers_new_attack_paths` | Remove SCN-39-CONFIG | `required scenarios missing: ['SCN-39-CONFIG']` |
| `test_scenario_suite_covers_new_attack_paths` | Remove the monitor deployment plan | `SCN-36-MONITOR: missing or misrepresented deployment plan` |
| `test_scenario_suite_covers_new_attack_paths` | Claim an unexecuted configuration test passed | `SCN-39-CONFIG: missing or misrepresented deployment plan` |
| `test_scenario_suite_covers_new_attack_paths` | Remove the legitimate compaction case | `SCN-37-COMPACTION: missing adversarial or legitimate case` |
| `test_scenario_suite_covers_new_attack_paths` | Erase the cleanup expected result | `SCN-38-CLEANUP: incomplete deployment case` |
| `test_scenario_suite_covers_new_attack_paths` | Use nonexistent monitor-plan evidence | `SCN-36-MONITOR: unknown deployment-case evidence` |
| `test_release_versions_are_authoritative` | Revert framework navigation version | `navigation component versions disagree with release` |
| `test_release_versions_are_authoritative` | Revert manifest navigation version | `navigation component versions disagree with release` |
| `test_release_versions_are_authoritative` | Revert scenario navigation count/release | `navigation scenario counts or release are stale` |
| `test_recorded_assessments` | Miscalculate configuration residual | `SCN-39-CONFIG/Unvalidated generation-change output behavior: recorded residual 13 != computed 12` |

## Limits

These checks establish record structure, arithmetic, selected consistency rules, citation location and generated-output synchronization. They do not prove semantic entailment, exploitability, deployed control effectiveness, or legal compliance. New deployment verification plans remain NOT_RUN; no exploit was executed, no provider control was certified, and no browser interaction/visual verification is claimed. The monitor study's malign-agent precondition, endogenous training events, open upstream PR, single-vendor watermarking results and unverified advisory details remain explicitly bounded in the source note. No new incident frequency, affected-version range or released fix is inferred.

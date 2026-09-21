# Verification — 2026-09-15

## Scope

33 structured tabletop cases. No deployment exploit execution or empirical control-effectiveness measurement. Citation checks establish verbatim location, not semantic entailment; conclusions also received adversarial review.

## Injected-defect checks

Each mutation below changed a real source file, ran the named check, restored the original bytes in `finally`, then reran that check successfully. Existing checks outside this table were run normally; they did not receive a new negative-control experiment in this revision.

| Check | Injection | Result | Exact finding |
|---|---|---|---|
| test_relay_scores_agree | Relay worksheet 4/8 → 5/10 | RED → restored PASS | `AssertionError: relay worksheet [5, 10] != matrix [4, 8]` |
| test_relay_scores_agree | SCN23 base4 → base5 | RED → restored PASS | `AssertionError: SCN-23-RELAY expected base != matrix 4` |
| test_risk_addendum_is_calibrated_and_machine_checkable | Memory overlay product8 →9 | RED → restored PASS | `AssertionError: Persistent memory poisoning: base score != likelihood * impact` |
| test_risk_addendum_is_calibrated_and_machine_checkable | Likelihood6 with consistent product24 | RED → restored PASS | `AssertionError: Persistent memory poisoning: invalid axes` |
| test_risk_addendum_is_calibrated_and_machine_checkable | Memory elevated10 →11 (not grid product) | RED → restored PASS | `AssertionError: Persistent memory poisoning: invalid elevated score` |
| test_residual_rounding_and_bands | Round floor instead of ceil | RED → restored PASS | `AssertionError: residual formula drift` |
| test_residual_rounding_and_bands | Remove score6 from residual bands | RED → restored PASS | `AssertionError: residual bands overlap or leave gaps` |
| test_residual_rounding_and_bands | Delete example for minimum score1 | RED → restored PASS | `AssertionError: rounding boundary cases missing` |
| test_residual_rounding_and_bands | First worked base9 →12 without updating expected7 | RED → restored PASS | `AssertionError: residual example expected 7, computed 9` |
| test_residual_rounding_and_bands | Score7 mislabeled LOW | RED → restored PASS | `AssertionError: residual 7: tier MEDIUM != LOW` |
| test_every_scenario_has_evidence_and_passes | Unknown evidence ID on SCN01 | RED → restored PASS | `AssertionError: SCN-01: unknown evidence reference` |
| test_canonical_ids_are_threaded_through_operational_docs | Remove the quota control route from quick reference | RED → restored PASS | `AssertionError: DOS-DEF-1` |
| test_quotes_match_cited_lines | Corrupt a verbatim citation | RED → restored PASS | `  quote: 'INJECTED MISSING QUOTE'...` |
| test_scenario_suite_covers_new_attack_paths | Rename required SCN30 to an unknown ID | RED → restored PASS | `AssertionError: required scenarios missing: ['SCN-30-MCP']` |

## Generated-artifact negative control

Renamed the generated `CONTROLS` declaration. `python scripts/build-html.py --check` rejected it:

```text
ERROR: C:\Users\cthza\Projects\llm-threat-model\llm-threat-model.html is stale; run python scripts/build-html.py
```

Restored the original bytes; the same command returned PASS.

## Release gate

| Command | Observed result |
|---|---|
| python scripts/citation_drift_detector.py | 248 checked; 248 OK; 0 drifted |
| python scripts/test_scenario_suite.py | PASS; 33 tabletop scenarios |
| python scripts/test_corpus_coherence.py | PASS (12 coherence checks) |
| python scripts/build-html.py --check | PASS: generated output matches |
| git diff --check | PASS after removing one trailing blank line |

Fifteen injected defects were rejected: fourteen focused corpus/scenario mutations plus the generated-artifact mutation. This verifies the named check behavior, not security effectiveness of a deployed LLM system.

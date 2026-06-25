#!/usr/bin/env python3
"""Regression tests for the scenario evaluation suite.

These tests define the quality bar before the scenario pack exists:
- exactly sixteen realistic scenarios, including six foreign-model deployment scenarios
- every major framework capability is covered
- every scenario uses the same pass/fail criteria
- every scenario records evidence and passes all checks
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = ROOT / "evaluation" / "scenario-suite.json"

REQUIRED_CAPABILITIES = {
    "assumption_boundary_validation",
    "asset_inventory",
    "attack_surface_mapping",
    "threat_taxonomy_classification",
    "attack_chain_mapping",
    "risk_scoring_and_elevation",
    "defense_control_evaluation",
    "residual_risk_remediation",
    "regulatory_mapping",
    "evidence_provenance_calibration",
    "worksheet_workflow",
    "quick_reference_triage",
    "foreign_model_posture",
}

REQUIRED_FOREIGN_DISTRIBUTION_MODES = {
    "foreign_lab_hosted_api",
    "foreign_lab_official_open_weights",
    "foreign_lab_official_weights_self_hosted",
    "foreign_open_weights_quantized_distribution",
    "foreign_open_weights_unofficial_finetune",
    "foreign_open_weights_lora_adapter",
}

REQUIRED_CHECKS = {
    "deployment_boundary_defined",
    "assets_and_surfaces_identified",
    "threats_and_chains_mapped",
    "risk_rating_calibrated",
    "defenses_evaluated",
    "residual_actions_defined",
    "regulatory_obligations_noted",
    "evidence_cited",
    "pass_fail_recorded",
}


def load_suite() -> dict:
    return json.loads(SUITE_PATH.read_text(encoding="utf-8"))


def test_suite_exists_and_uses_pass_fail_method() -> None:
    suite = load_suite()
    assert suite["metadata"]["evaluation_method"] == "uniform_pass_fail"
    assert suite["metadata"]["same_conditions"]
    assert len(suite["scenarios"]) == 16
    assert suite["metadata"]["n_scenarios"] == 16


def test_foreign_llm_scenario_series_covers_required_distribution_modes() -> None:
    suite = load_suite()
    foreign = [
        scenario for scenario in suite["scenarios"]
        if "foreign_model_posture" in scenario["capabilities"]
    ]
    assert len(foreign) >= 6
    modes = {scenario.get("foreign_distribution_mode") for scenario in foreign}
    assert REQUIRED_FOREIGN_DISTRIBUTION_MODES <= modes
    for scenario in foreign:
        assert "foreign" in scenario["deployment"].lower(), scenario["id"]
        assert "EV-ASSUME-FOREIGN-WEIGHTS" in {
            evidence["id"] for evidence in scenario["evidence"]
        }, scenario["id"]


def test_success_criteria_are_consistent_for_every_scenario() -> None:
    suite = load_suite()
    expected = [criterion["id"] for criterion in suite["success_criteria"]]
    assert set(expected) == REQUIRED_CHECKS
    for scenario in suite["scenarios"]:
        actual = [check["criterion_id"] for check in scenario["checks"]]
        assert actual == expected, scenario["id"]


def test_every_major_capability_is_covered() -> None:
    suite = load_suite()
    covered = set()
    for scenario in suite["scenarios"]:
        covered.update(scenario["capabilities"])
    assert REQUIRED_CAPABILITIES <= covered


def test_every_scenario_has_evidence_and_passes() -> None:
    suite = load_suite()
    for scenario in suite["scenarios"]:
        assert scenario["overall_result"] == "PASS", scenario["id"]
        assert scenario["evidence"], scenario["id"]
        for evidence in scenario["evidence"]:
            assert evidence["source"].startswith("synthesis/"), scenario["id"]
            assert evidence["lines"], scenario["id"]
        for check in scenario["checks"]:
            assert check["result"] == "PASS", f"{scenario['id']}::{check['criterion_id']}"
            assert check["evidence_refs"], f"{scenario['id']}::{check['criterion_id']}"


def test_failure_log_is_empty_after_corrections() -> None:
    suite = load_suite()
    assert suite["rerun_history"]
    assert suite["open_failures"] == []
    assert suite["final_complete_rerun"]["result"] == "PASS"


if __name__ == "__main__":
    failures = []
    for name, func in sorted(globals().items()):
        if name.startswith("test_") and callable(func):
            try:
                func()
            except Exception as exc:  # noqa: BLE001 - tiny dependency-free runner
                failures.append(f"{name}: {exc}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        raise SystemExit(1)
    print("PASS")

#!/usr/bin/env python3
"""Regression tests for the scenario evaluation suite.

These tests define the quality bar for an extensible scenario pack:
- at least 25 realistic scenarios, including six foreign-model and nine agentic scenarios
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
    assert len(suite["scenarios"]) >= 25
    assert suite["metadata"]["n_scenarios"] == len(suite["scenarios"])
    for scenario in suite["scenarios"]:
        assert scenario["same_conditions_applied"] == suite["metadata"]["same_conditions"]


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
            assert evidence["quote"].strip(), f"{scenario['id']}::{evidence['id']} has an empty quote"
        for check in scenario["checks"]:
            assert check["result"] == "PASS", f"{scenario['id']}::{check['criterion_id']}"
            assert check["evidence_refs"], f"{scenario['id']}::{check['criterion_id']}"


def test_failure_log_is_empty_after_corrections() -> None:
    suite = load_suite()
    assert suite["rerun_history"]
    assert suite["open_failures"] == []
    assert suite["final_complete_rerun"]["result"] == "PASS"


# --- citation validation helpers (mirrored from citation_drift_detector.py) ---

def _check_citation(source: str, lines: str, quote: str) -> tuple[str, str]:
    """Returns (status, reason). Mirrors citation_drift_detector.check_citation."""
    if not quote.strip():
        return "INVALID_QUOTE", "quote is empty"
    path = ROOT / source
    if not path.exists():
        return "FILE_NOT_FOUND", f"{source} does not exist"
    content = path.read_text(encoding="utf-8")
    all_lines = content.splitlines()
    try:
        start, end = map(int, lines.split("-"))
    except ValueError:
        return "INVALID_RANGE", f"cannot parse lines: {lines}"
    if start < 1 or end < start:
        return "INVALID_RANGE", f"start={start} end={end}"
    if end > len(all_lines):
        return "DRIFTED", f"end={end} exceeds file length {len(all_lines)}"
    cited_text = "\n".join(all_lines[start - 1 : end])
    if quote not in cited_text:
        return "DRIFTED", "quote not found in cited range"
    return "OK", ""


def check_citation(source: str, lines: str, quote: str) -> tuple[str, str]:
    return _check_citation(source, lines, quote)


def test_citation_ranges_valid() -> None:
    """Every evidence citation points to a line range within the file."""
    suite = load_suite()
    for scenario in suite["scenarios"]:
        for evidence in scenario["evidence"]:
            path = ROOT / evidence["source"]
            assert path.exists(), (
                f"{scenario['id']}/{evidence['id']}: {evidence['source']} does not exist"
            )
            all_lines = path.read_text(encoding="utf-8").splitlines()
            start, end = map(int, evidence["lines"].split("-"))
            assert 1 <= start <= end <= len(all_lines), (
                f"{scenario['id']}/{evidence['id']}: lines {evidence['lines']} "
                f"out of bounds for {len(all_lines)}-line file {evidence['source']}"
            )


def test_quotes_match_cited_lines() -> None:
    """The quoted text appears verbatim inside the cited line range."""
    suite = load_suite()
    for scenario in suite["scenarios"]:
        for evidence in scenario["evidence"]:
            path = ROOT / evidence["source"]
            all_lines = path.read_text(encoding="utf-8").splitlines()
            start, end = map(int, evidence["lines"].split("-"))
            cited_text = "\n".join(all_lines[start - 1 : end])
            assert evidence["quote"] in cited_text, (
                f"{scenario['id']}/{evidence['id']}: quote not found in "
                f"{evidence['source']}:{evidence['lines']}\n"
                f"  quote: {evidence['quote'][:80]!r}..."
            )


def test_no_drifted_citations() -> None:
    """Fail if any citation has drifted (see citation_drift_detector.py).

    This is the CI gate: when synthesis files are edited, run:
        python scripts/citation_drift_detector.py --fix
    to refresh ranges, then re-run this test.
    """
    suite = load_suite()
    for scenario in suite["scenarios"]:
        for evidence in scenario["evidence"]:
            status, _ = check_citation(
                evidence["source"], evidence["lines"], evidence["quote"]
            )
            assert status == "OK", (
                f"{scenario['id']}/{evidence['id']}: citation drifted — "
                f"run: python scripts/citation_drift_detector.py --fix"
            )


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

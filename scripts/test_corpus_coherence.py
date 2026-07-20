#!/usr/bin/env python3
"""Coherence checks for the v1.9 agentic threat-model release."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "synthesis"

REQUIRED_CONTROL_IDS = {
    "MEM-DEF-1",
    "SKILL-DEF-1",
    "MA-DEF-3",
    "CUA-DEF-1",
    "RELAY-DEF-1",
    "DET-DEF-3",
    "REP-DEF-1",
}
REQUIRED_SUBTYPE_IDS = {
    "T01-SESSION",
    "T03-SKILL",
    "T05-CAPABILITY",
    "T09-MEMORY",
    "T09-IDENTITY",
    "T10-CUA",
    "T10-REPRESENTATION",
    "T11-RELAY",
}
REQUIRED_SCENARIOS = {
    "SCN-17-MEMORY",
    "SCN-18-SKILL-RETRIEVAL",
    "SCN-19-SKILL-UPDATE",
    "SCN-20-IDENTITY",
    "SCN-21-COMPUTER-USE",
    "SCN-22-SESSION",
    "SCN-23-RELAY",
    "SCN-24-REPRESENTATION",
    "SCN-25-DISCLOSURE",
}
EXPECTED_COMPONENT_VERSIONS = {
    "framework.md": "1.9",
    "threat-taxonomy.md": "1.8",
    "risk-matrix.md": "1.9",
    "defense-playbook.md": "1.8",
    "assessment-template.md": "1.9",
    "quick-reference.md": "1.8",
    "attack-surface-catalog.md": "1.4",
    "attack-trees.md": "1.5",
    "asset-inventory.md": "1.1",
    "assumptions.md": "1.1",
}


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_release_versions_are_authoritative() -> None:
    manifest = text("synthesis/release-manifest.md")
    assert "**Release:** v1.9 agentic trust-boundary integration" in manifest
    assert "**Date:** 2026-07-20" in manifest
    for filename, version in EXPECTED_COMPONENT_VERSIONS.items():
        content = text(f"synthesis/{filename}")
        assert content.startswith(f"# "), filename
        assert f"**Version:** {version}" in "\n".join(content.splitlines()[:6]), filename
        assert f"`synthesis/{filename}` | v{version}" in manifest, filename
    assert "post-release" not in manifest.lower()


def test_no_post_footer_fragments_or_mid_document_versions() -> None:
    for filename in EXPECTED_COMPONENT_VERSIONS:
        content = text(f"synthesis/{filename}")
        lines = content.splitlines()
        version_lines = [i for i, line in enumerate(lines, 1) if line.startswith("**Version:**")]
        assert version_lines == [3], (filename, version_lines)
        last_updated = [i for i, line in enumerate(lines, 1) if line.startswith("**Last updated:**")]
        assert len(last_updated) <= 1, (filename, last_updated)
        if last_updated:
            tail = lines[last_updated[0]:]
            assert not any(line.startswith("## ") for line in tail), filename


def test_canonical_ids_are_threaded_through_operational_docs() -> None:
    taxonomy = text("synthesis/threat-taxonomy.md")
    for subtype_id in REQUIRED_SUBTYPE_IDS:
        assert subtype_id in taxonomy, subtype_id
    assessment = text("synthesis/assessment-template.md")
    playbook = text("synthesis/defense-playbook.md")
    quick = text("synthesis/quick-reference.md")
    matrix = text("synthesis/risk-matrix.md")
    for control_id in REQUIRED_CONTROL_IDS:
        assert control_id in playbook, control_id
        assert f"| {control_id} |" in assessment, control_id
        assert control_id in quick, control_id
        assert control_id in matrix, control_id


def test_foundations_cover_new_assets_and_trust_boundaries() -> None:
    assets = text("synthesis/asset-inventory.md").lower()
    assumptions = text("synthesis/assumptions.md").lower()
    for phrase in (
        "durable memory",
        "skill registry",
        "agent identity credential",
        "relay transcript",
        "representation provenance",
    ):
        assert phrase in assets, phrase
    assert "authenticated transport does not prove agent identity" in assumptions
    assert "self-asserted" in assumptions


def test_risk_addendum_is_calibrated_and_machine_checkable() -> None:
    matrix = text("synthesis/risk-matrix.md")
    assert "Starting score" not in matrix
    assert "July 2026 Provisional Risk Addendum" not in matrix
    assert "| Threat overlay | Wild_vs_Theory | Likelihood | Impact | Base Score | Elevation Condition | Elevated Score |" in matrix
    for score in ("15",):
        for threat in (
            "Persistent memory poisoning",
            "Skill lifecycle compromise",
            "Inter-agent trust escalation",
            "Computer-use visual attack",
            "Session contamination / incremental escalation",
        ):
            row = next(line for line in matrix.splitlines() if f"| {threat} |" in line)
            assert f"| {score} |" not in row, row
    relay_row = next(line for line in matrix.splitlines() if "Response-path relay tampering" in line)
    assert "provisional" in relay_row.lower()
    assert "| 1/5 |" in relay_row


def test_relay_control_does_not_claim_unavailable_upstream_assurance() -> None:
    playbook = text("synthesis/defense-playbook.md")
    relay = playbook.split("### RELAY-DEF-1", 1)[1].split("### ", 1)[0]
    assert "Relay authentication alone does not prove upstream authorization" in relay
    assert "provider-authenticated" in relay
    assert "unresolved assurance gap" in relay.lower()


def test_scenario_suite_covers_new_attack_paths() -> None:
    suite = json.loads(text("evaluation/scenario-suite.json"))
    assert suite["metadata"]["n_scenarios"] == len(suite["scenarios"])
    assert len(suite["scenarios"]) >= 25
    validator = text("scripts/test_scenario_suite.py")
    assert 'len(suite["scenarios"]) >= 25' in validator
    assert 'n_scenarios"] == len(suite["scenarios"])' in validator
    assert "v1.9 corpus" in suite["metadata"]["same_conditions"]
    ids = {scenario["id"] for scenario in suite["scenarios"]}
    assert REQUIRED_SCENARIOS <= ids
    for scenario in suite["scenarios"]:
        if scenario["id"] in REQUIRED_SCENARIOS:
            assert scenario["overall_result"] == "PASS"
            assert scenario["evidence"]
            assert len(scenario["checks"]) == 9

    results = text("evaluation/scenario-suite-results.md")
    assert "against the same v1.9 corpus" in results
    assert "**PASS** (25 passed, 0 failed)" in results


def test_structured_source_and_html_include_new_contract() -> None:
    data = json.loads(text("threat-model-data.json"))
    assert data["_meta"]["version"] == "1.9"
    assert data["_meta"]["date"] == "2026-07-20"
    serialized = json.dumps(data)
    html = text("llm-threat-model.html")
    assert "const CONTROLS =" in html
    for identifier in REQUIRED_CONTROL_IDS | REQUIRED_SUBTYPE_IDS:
        assert identifier in serialized, identifier
        assert identifier in html, identifier


def test_source_window_labels_pre_window_evidence_honestly() -> None:
    source = text("research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md")
    assert "### Microsoft AI Red Team — June 4, 2026 (pre-window corroboration)" in source
    assert "outside the strict 30-day window" in source


def test_final_verifier_blockers_remain_fixed() -> None:
    html = text("llm-threat-model.html")
    assert "<title>LLM Threat Model v1.9</title>" in html
    assert "LLM Threat Model — v1.9" in html
    assert '<span class="badge">v1.9</span>' in html
    assert "Updated 2026-07-20" in html
    assert "3 canonical attack chains plus scoped agentic branches" in html
    builder = text("scripts/build-html.py")
    assert '"--check" in sys.argv' in builder

    risk = text("synthesis/risk-matrix.md")
    relay_row = next(line for line in risk.splitlines() if "Response-path relay tampering" in line)
    assert "| 1/5 | 1 | 4 | **4** |" in relay_row
    assert "| **8** |" in relay_row

    trees = text("synthesis/attack-trees.md")
    for marker in (
        "**Branch severity:**",
        "**Mission goal:**",
        "**Prerequisites:**",
        "T11-RELAY-N1",
        "T10-CUA-N1",
    ):
        assert marker in trees, marker

    defenses = text("synthesis/defense-playbook.md")
    assert "a *** authenticated relay" not in defenses


def main() -> int:
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:  # noqa: BLE001 - standalone test runner
            failures.append(f"{test.__name__}: {exc}")
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS ({len(tests)} coherence checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

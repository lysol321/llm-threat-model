#!/usr/bin/env python3
"""Coherence checks for the v1.12 agentic threat-model release."""
from __future__ import annotations

import json
import re
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "synthesis"

REQUIRED_CONTROL_IDS = {
    "DOS-DEF-1",
    "DATA-DEF-1",
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
RESEARCH_SCENARIOS = {"SCN-36-MONITOR", "SCN-37-COMPACTION", "SCN-38-CLEANUP", "SCN-39-CONFIG"}
REQUIRED_SCENARIOS = {
    *RESEARCH_SCENARIOS,
    "SCN-34-OUTPUT", "SCN-35-FACTS",
    "SCN-26-NO-TOOLS", "SCN-27-QUOTA", "SCN-28-SIGNED-BUILD",
    "SCN-29-INTERMEDIARY", "SCN-30-MCP", "SCN-31-MEMORY-INPUT",
    "SCN-32-ENFORCEMENT", "SCN-33-EVIDENCE",
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
    "assessment-template.md": "1.12",
    "asset-inventory.md": "1.3",
    "assumptions.md": "1.4",
    "attack-surface-catalog.md": "1.7",
    "attack-trees.md": "1.8",
    "defense-playbook.md": "1.11",
    "framework.md": "1.12",
    "quick-reference.md": "1.11",
    "risk-matrix.md": "1.12",
    "threat-taxonomy.md": "1.11"
}


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_release_versions_are_authoritative() -> None:
    manifest = text("synthesis/release-manifest.md")
    assert "**Release:** v1.12 September threat-model review and evidence update" in manifest
    assert "**Date:** 2026-09-19" in manifest
    for filename, version in EXPECTED_COMPONENT_VERSIONS.items():
        content = text(f"synthesis/{filename}")
        assert content.startswith(f"# "), filename
        assert f"**Version:** {version}" in "\n".join(content.splitlines()[:6]), filename
        assert f"`synthesis/{filename}` | v{version}" in manifest, filename
    assert "post-release" not in manifest.lower()
    data = json.loads(text("threat-model-data.json"))
    navigation = {Path(item["file"]).name: item.get("version") for item in data["synthesis"]}
    expected_navigation = {**EXPECTED_COMPONENT_VERSIONS, "release-manifest.md": data["_meta"]["version"]}
    assert all(navigation.get(name) == version for name, version in expected_navigation.items()), "navigation component versions disagree with release"
    suite = json.loads(text("evaluation/scenario-suite.json"))
    expected = f"{len(suite['scenarios'])}-scenario v{data['_meta']['version']} tabletop"
    assert all(expected in item["desc"] for item in data["evaluation"] if "scenario-suite" in item["file"]), "navigation scenario counts or release are stale"


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
    for row in matrix.splitlines():
        cells = [cell.strip().replace("**", "") for cell in row.split("|")[1:-1]]
        if len(cells) >= 7 and re.fullmatch(r"[1-5]/5", cells[1]):
            likelihood, impact, score, elevated = map(int, (cells[2], cells[3], cells[4], cells[6]))
            assert score == likelihood * impact, f"{cells[0]}: base score != likelihood * impact"
            assert 1 <= likelihood <= 5 and 1 <= impact <= 5, f"{cells[0]}: invalid axes"
            assert elevated in {a*b for a in range(1,6) for b in range(1,6)} and elevated >= score, f"{cells[0]}: invalid elevated score"
    relay_row = next(line for line in matrix.splitlines() if "Response-path relay tampering" in line)
    assert "provisional" in relay_row.lower()
    assert "| 1/5 |" in relay_row


def test_relay_control_does_not_claim_unavailable_upstream_assurance() -> None:
    playbook = text("synthesis/defense-playbook.md")
    relay = playbook.split("### RELAY-DEF-1", 1)[1].split("### ", 1)[0]
    assert "Relay authentication alone does not prove upstream authorization" in relay
    assert "provider-authenticated" in relay
    assert "unresolved assurance gap" in relay.lower()


def test_relay_scores_agree() -> None:
    """Negative controls recorded in review/verification-2026-09-15.md."""
    row = next(line for line in text("synthesis/risk-matrix.md").splitlines()
               if line.startswith("| Response-path relay tampering"))
    cells = [cell.strip().replace("**", "") for cell in row.split("|")[1:-1]]
    baseline, elevated = int(cells[4]), int(cells[6])
    lookup = next(line for line in text("synthesis/assessment-template.md").splitlines()
                  if line.startswith("| Response-path relay tampering *(provisional)* |"))
    scores = [int(number) for number in re.findall(r"\d+", lookup)]
    assert scores == [baseline, elevated], f"relay worksheet {scores} != matrix {[baseline, elevated]}"
    suite = json.loads(text("evaluation/scenario-suite.json"))
    scenario = next(item for item in suite["scenarios"] if item["id"] == "SCN-23-RELAY")
    expected = re.search(r"base (?:score )?(\d+)", scenario["expected_assessment"])
    assert expected and int(expected[1]) == baseline, f"SCN-23-RELAY expected base != matrix {baseline}"


def test_scenario_suite_covers_new_attack_paths() -> None:
    suite = json.loads(text("evaluation/scenario-suite.json"))
    assert suite["metadata"]["n_scenarios"] == len(suite["scenarios"])
    assert len(suite["scenarios"]) >= 25
    validator = text("scripts/test_scenario_suite.py")
    assert 'len(suite["scenarios"]) >= 25' in validator
    assert 'n_scenarios"] == len(suite["scenarios"])' in validator
    assert "v1.12 corpus" in suite["metadata"]["same_conditions"]
    ids = {scenario["id"] for scenario in suite["scenarios"]}
    assert REQUIRED_SCENARIOS <= ids, f"required scenarios missing: {sorted(REQUIRED_SCENARIOS - ids)}"
    for scenario in suite["scenarios"]:
        if scenario["id"] in REQUIRED_SCENARIOS:
            assert scenario["overall_result"] == "PASS"
            assert scenario["evidence"]
            assert len(scenario["checks"]) == 9
        if scenario["id"] in RESEARCH_SCENARIOS:
            plan = scenario.get("verification_plan", {})
            assert plan.get("status") == "NOT_RUN" and plan.get("owner"), f"{scenario['id']}: missing or misrepresented deployment plan"
            cases = plan.get("cases", [])
            assert {"adversarial", "legitimate"} <= {c.get("kind") for c in cases}, f"{scenario['id']}: missing adversarial or legitimate case"
            evidence_ids = {e["id"] for e in scenario["evidence"]}
            for case in cases:
                assert all(isinstance(case.get(k), str) and case[k].strip() for k in ("case", "expected")), f"{scenario['id']}: incomplete deployment case"
                assert case.get("evidence_refs") and set(case["evidence_refs"]) <= evidence_ids, f"{scenario['id']}: unknown deployment-case evidence"


    results = text("evaluation/scenario-suite-results.md")
    assert "against the same v1.12 corpus" in results
    assert f"**PASS** ({len(suite['scenarios'])} passed, 0 failed)" in results


def test_residual_rounding_and_bands() -> None:
    worksheet = text("synthesis/assessment-template.md")
    assert "max(1, ceil(min(25, BASE_RISK × MITIGATION_FACTOR × AGENCY_FACTOR)))" in worksheet, "residual formula drift"
    bands = [(int(a), int(b), label) for a, b, label in
             re.findall(r"\| (\d+)–(\d+) \((CRITICAL|HIGH|MEDIUM|LOW)\) \|", worksheet)]
    assert sorted(n for a, b, _ in bands for n in range(a, b+1)) == list(range(1,26)), "residual bands overlap or leave gaps"
    examples = json.loads(text("evaluation/scenario-suite.json"))["scoring_examples"]
    assert {example["expected"] for example in examples} >= {1,6,7,13,21,25}, "rounding boundary cases missing"
    for example in examples:
        raw = Decimal(example["base"]) * Decimal(example["mitigation"]) * Decimal(example["agency"])
        score = max(1, int(min(Decimal(25), raw).to_integral_value(rounding=ROUND_CEILING)))
        assert score == example["expected"], f"residual example expected {example['expected']}, computed {score}"
        tier = next(label for a, b, label in bands if a <= score <= b)
        assert tier == example["tier"], f"residual {score}: tier {tier} != {example['tier']}"


def test_structured_source_and_html_include_new_contract() -> None:
    data = json.loads(text("threat-model-data.json"))
    assert data["_meta"]["version"] == "1.12"
    assert data["_meta"]["date"] == "2026-09-19"
    serialized = json.dumps(data)
    html = text("llm-threat-model.html")
    assert "const CONTROLS =" in html
    for identifier in REQUIRED_CONTROL_IDS | REQUIRED_SUBTYPE_IDS:
        assert identifier in serialized, identifier
        assert identifier in html, identifier


def test_briefing_preserves_evidence_ratings() -> None:
    """Negative controls: review/html-briefing-verification-2026-09-15.md."""
    data = json.loads(text("threat-model-data.json"))
    taxonomy = text("synthesis/threat-taxonomy.md")
    for threat in data["threats"]:
        for field in ("plain_title", "applies_when", "business_impact", "defender_action", "evidence_summary"):
            assert threat.get(field, "").strip(), f"T{threat['num']}: missing {field}"
        assert threat["evidence_score"] == int(threat["wild"][0]), f"T{threat['num']}: badge disagrees with evidence text"
        section = taxonomy.split(f"### Category {int(threat['num'])}:", 1)[1].split("\n### ", 1)[0]
        score = re.search(r"\*\*Wild_vs_Theory: ([1-5])/5", section)
        if score:
            assert threat["evidence_score"] == int(score[1]), f"T{threat['num']}: briefing rating disagrees with taxonomy"
    briefing = text("llm-threat-model.html").split("// ── DATA_START", 1)[0]
    assert "Research: 5/5" not in briefing, "briefing labels research as widespread field evidence"


def test_readme_matches_current_release() -> None:
    """Negative controls: review/corrections-2026-09-19.md."""
    readme = text("README.md")
    data = json.loads(text("threat-model-data.json"))
    scenarios = json.loads(text("evaluation/scenario-suite.json"))["scenarios"]
    assert f"**Release v{data['_meta']['version']}**" in readme.splitlines()[2], "README release disagrees with structured source"
    assert f"{len(scenarios)} documented tabletop scenarios" in readme, "README scenario count disagrees with suite"
    rows = {int(n): int(score) for n, score in re.findall(r"^\| (\d+) \|.*\| ([1-5])/5 \|$", readme, re.M)}
    expected = {int(threat["num"]): threat["evidence_score"] for threat in data["threats"]}
    assert rows == expected, "README threat evidence ratings disagree with structured source"
    assert "EchoLeak individually is **3/5**" in readme and "confirmed zero-click in-wild exploitation" not in readme, "README EchoLeak evidence is stale"


def test_source_window_labels_pre_window_evidence_honestly() -> None:
    source = text("research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md")
    assert "### Microsoft AI Red Team — June 4, 2026 (pre-window corroboration)" in source
    assert "outside the strict 30-day window" in source


def test_final_verifier_blockers_remain_fixed() -> None:
    html = text("llm-threat-model.html")
    assert "<title>LLM Threat Model v1.12</title>" in html
    assert "LLM Threat Model — v1.12" in html
    assert '<span class="badge">v1.12</span>' in html
    assert "Updated 2026-09-19" in html
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

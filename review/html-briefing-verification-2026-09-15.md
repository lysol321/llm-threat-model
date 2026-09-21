# HTML briefing verification — 2026-09-15

## Audience and scope

The HTML now leads with evidence strength for defenders and non-technical leadership. It preserves the 1–5 Wild vs Theory scale, distinguishes category and subtype evidence, and explains applicability, business impact and defensive action. No new threat category or risk score was introduced. The stale Category 4 HTML evidence score was aligned with the existing taxonomy (3/5).

The stale hand-written risk table was replaced by the current embedded risk-matrix document behind a defender-detail disclosure. This prevents separate HTML scores from drifting away from the corpus. Existing research documents remain reference material, with the evidence limits stated in the main briefing.

## Browser checks

Chrome DevTools used real clicks, keyboard input and typing. The edited page was foregrounded, verified against changed copy, and inspected at desktop and 390px mobile widths.

- Overview evidence button selects four field-observed categories.
- Research filter plus “validator” returns only ISC, visibly rated 2/5.
- Cards expand with evidence limits, applicability, business impact and defensive action.
- Unmatched search returns zero results and a reset prompt; reset restores all fourteen.
- Evidence button opens the taxonomy in the document viewer.
- Mobile inspection exposed the old sidebar covering the content; references now start collapsed and inert, with an explicit toggle.
- No horizontal overflow in the inspected mobile overview; no runtime console errors during the main interaction checks.
- Expanded mobile threat cards and the canonical scoring tables also remained within the viewport. The evidence link placed the relevant Category 14 heading below the sticky navigation.
- Reference toggle correctly changed visibility, inert state and expanded state. Switching back to the briefing cleared the stale document URL fragment.

## Final checks

- `python scripts/test_corpus_coherence.py`: PASS (13 checks).
- `python scripts/test_scenario_suite.py`: PASS.
- `python scripts/build-html.py --check`: PASS; HTML matches its structured source.
- `git diff --check`: PASS.

Browser verification covered the main briefing, filters, search/reset, disclosure cards, source navigation, scoring disclosure and reference toggle. PDF pagination was not reviewed.

## Negative controls

Each mutation changed a real file, ran `test_briefing_preserves_evidence_ratings`, and restored the original bytes before a passing rerun.

| Injection | Exact failure | Restoration |
|---|---|---|
| Missing business impact | `AssertionError: T01: missing business_impact` | Restored PASS |
| Badge differs from its evidence text | `AssertionError: T01: badge disagrees with evidence text` | Restored PASS |
| ISC promoted from research to field evidence | `AssertionError: T14: briefing rating disagrees with taxonomy` | Restored PASS |
| Stale research label returns | `AssertionError: briefing labels research as widespread field evidence` | Restored PASS |

# HTML Content Integration — LLM Threat Model

**Goal:** Integrate synthesis doc content into the HTML until architecture is satisfied. Stop at 3 straight no-change passes.

---

## Corpus state at entry

- HTML: 979 lines, 69.3KB, single self-contained file (architecture complete per htmldesign log Pass 15)
- Synthesis docs: v1.8 release (threat-model-review log converged at Pass 10)
- Architecture is solid; this session closes content gaps between the reviewed synthesis and the HTML

---

## Pass log

### Pass 1 — Changes (committed)

| Finding | Fix |
|---|---|
| Stat cards wrong (4C/9H/8M/4L vs actual 3C/3H/7M/1L) | `renderStats()` computes from THREATS array |
| Version v1.7 in title/badge/h2 | Updated to v1.8 throughout |
| DET-DEF-1/DET-DEF-2 missing from defense table | Added with `ctrl-detect` badge + production cost rows |

### Pass 2 — Changes (committed)

| Finding | Fix |
|---|---|
| Defense Investment Guidance absent | Added Tier 1/2/3 + Conditional ISC table (from framework.md) |
| Comparable Frameworks absent | Added 7-framework table to OWASP tab (from framework.md v1.8) |

### Pass 3 — Changes (committed)

| Finding | Fix |
|---|---|
| ISC/Category 14 had no Overview key insight | Added 5th insight card about harness attacks bypassing PI detectors |
| SC-GAP-1 not surfaced | Added warning note to SC-DEF-1: AIBOM doesn't detect behavioral backdoors |

### Pass 4 — Changes (committed)

| Finding | Fix |
|---|---|
| MA-DEF-1 "HIGH if enforced" overstated for LangGraph default | Added LangGraph ToolCallWrapper caveat note + updated effectiveness label |
| Threat 09 missing source note + Slow-Burn subtype | Added update field + Slow-Burn as 5th subtype |

### Pass 5 — Changes (committed)

| Finding | Fix |
|---|---|
| ISC-DEF-2 in investment guidance but not in defense table | Added ISC-DEF-2 (agentic loop visibility) to defense table + investment Tier 2 |

### Pass 6 — NO CHANGES [no-change pass #1]

Comprehensive sweep of all remaining synthesis content:
- PI-DEF-3 (Input Filtering): SECONDARY; cost table already mentions "Input filtering". Not adding.
- PI-DEF-4 (Output Validation): SECONDARY; cost table already mentions "Output validation". Not adding.
- SC-DEF-3 (Model Registry Controls): SECONDARY. Not adding (scope creep for quick-ref tool).
- Tool Call Budgeting [OPS]: SECONDARY. Not adding.
- ISC-DEF-3 (Deployment-Level ISC Scanning): Provider-side only; deployers mark N/A. Not adding.
- Tier 4 Lower Risks: audio injection (score 3), covert channel (score 4), align regression (score 6), JaaS (score 4) — all already shown in risk matrix grid cells. ✓
- Asset inventory / assumptions / attack surface catalog: detailed reference docs, appropriate to leave in synthesis. Not suitable for quick-ref HTML.
- Regulatory detail (EU AI Act 3%/€15M for documentation vs 6%/€30M for violations): HTML uses max penalty. Intentional simplification for quick reference. ✓
- Research/evaluation content: not for HTML. ✓

**State: 1 no-change pass completed. Need 2 more to stop.**

---

## Final state (after Pass 6)

| Component | Status |
|---|---|
| Version | v1.8 ✓ |
| Stat cards | Dynamic from THREATS (3C/3H/7M/1L) ✓ |
| 14 Threats | All entries match taxonomy; update fields current ✓ |
| Attack Chains | All 4 chains (A/B/C/ISC) correct ✓ |
| Risk Matrix | Base scores + elevation conditions match ✓ |
| Defense Table | 11 controls (incl. ISC-DEF-2, DET-DEF-1/2) + SC-GAP-1 + MA-DEF-1 caveat ✓ |
| Defense Investment Guidance | Tier 1/2/3 + Conditional ISC ✓ |
| Decision Tree | 4 questions matching quick-reference ✓ |
| OWASP Mapping | LLM01-LLM10 correct ✓ |
| Regulatory Reference | EU AI Act / GDPR / FTC ✓ |
| Comparable Frameworks | 7 frameworks (v1.8 addition) ✓ |
| 5 Key Insights | Incl. ISC harness attack insight ✓ |

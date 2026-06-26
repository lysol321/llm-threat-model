# HTML Content Integration — LLM Threat Model

**Goal:** Integrate synthesis doc content into the HTML until architecture is satisfied. Stop at 3 straight no-change passes.

---

## Corpus state at entry

- HTML: 979 lines, 69.3KB, single self-contained file (architecture complete per htmldesign log Pass 15)
- Synthesis docs: v1.8 release (threat-model-review log converged at Pass 10)
- Architecture is solid; this session closes content gaps between the reviewed synthesis and the HTML

---

## Pass log

### Pass 1 — Content audit (findings)

| # | Severity | Finding |
|---|---|---|
| 1 | HIGH | Stat cards hardcoded as 4C/9H/8M/4L; actual THREATS array is 3C/3H/7M/1L. Clicking "4 Critical" filter shows only 3 threats — visible mismatch. |
| 2 | MEDIUM | Version: HTML title + h2 say v1.7; release manifest is v1.8. |
| 3 | MEDIUM | DET-DEF-1 (Audit Logging) and DET-DEF-2 (Anomaly Detection) absent from defenses table. The defense-playbook has them as a full "Detection and Response" layer. |
| 4 | LOW | Production cost annotations table doesn't include DET-DEF-1/DET-DEF-2 (will fix alongside #3) |

**Verified correct (no change):**
- THREATS data (14 entries) matches threat-taxonomy.md priority/content
- OWASP table matches quick-reference.md exactly
- Regulatory table: EU AI Act 6% turnover/€30M, GDPR 4%/€20M — both correct
- Risk matrix values match risk-matrix.md base scores
- Elevation conditions table matches risk-matrix.md Tier 2 elevation conditions
- Attack chains match attack-trees content
- Decision tree matches quick-reference.md decision tree shortcut
- Defense table controls (PI-DEF-1/2, AGENCY-DEF-1/2, SC-DEF-1/2, MA-DEF-1, ISC-DEF-1) match defense-playbook.md

---

### Pass 1 — Changes planned

1. **Stat cards**: Compute counts dynamically from THREATS array in `renderStats()` called at init
2. **Version**: v1.7 → v1.8 in `<title>` and Overview h2
3. **DET-DEF-1/DET-DEF-2**: Add to defenses table with `ctrl-detect` type + production cost entries
4. **CSS**: Add `.ctrl-detect` badge style for detection control type

---

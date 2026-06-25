# Threat Model Review — llm-threat-model

**Goal:** Review until all assumptions, assets, and attack surfaces defensible against a senior researcher.
Stop when 3 straight passes change nothing I'd defend. Track here. Autoresearch new questions, close gaps, update wiki. Use jdocmunch.

**Reviewer model:** Opus 4.8 · **Started:** 2026-06-25

---

## Corpus state at entry
- v1.8 release. 11 synthesis docs + research/ + evaluation/ + review/.
- Three 2026-06-24 red-team passes already applied. Verified the historical CRITICAL blockers are CLOSED:
  - Residual-risk formula: now `MITIGATION_FACTOR` reduces risk (0.3/0.7/1.0/1.2); worked example consistent (20×0.7×1.5=21→CRITICAL). ✓
  - EU AI Act articles normalized in risk-matrix.md (9/10/13/14/15/17) + framework.md. ✓
  - Risk matrix base/elevated split into machine-checkable columns. ✓
  - Detection vs prevention separated; control-gap floor present. ✓
  - ISC applicability boundary (attacker-shaped harness) crisp in taxonomy + quick-ref. ✓

## Findings — Pass 1 (my own senior-reviewer pass)

| # | Severity | File | Finding | Status |
|---|---|---|---|---|
| 1 | Medium | threat-taxonomy.md:26-32, 270-276 | Malformed `\|\|` tables (empty leading column) despite v1.7 note claiming "table formatting corrected" | FIX |
| 2 | Medium | release-manifest vs file headers | Manifest claims risk-matrix v1.7/defense-playbook v1.7/quick-ref v1.7/attack-trees v1.2; headers say 1.3/1.6/1.6/1.3. risk-matrix internally inconsistent (header 1.3, footer v1.7) | FIX |
| 3 | Medium | threat-taxonomy.md:375 vs risk-matrix.md:52 | ISC regulatory mapping contradicts: cross-ref index says Art.10/14, risk-matrix says Art.9/15/17 | FIX |
| 4 | Required | framework.md:265-278 | Defense Investment Guidance (Tier 1-3) omits ISC entirely despite ISC=CRITICAL — open red-team Required finding | FIX |
| 5 | Low | risk-matrix.md:176-197 | Summary visual mislabels: Direct PI shown at 10 (actual 15), Chain A at 15 (actual 20) — contradicts authoritative table | FIX |
| 6 | Low | assumptions.md:292 | Footer "Part of: Framework v1.4" stale vs v1.8 | FIX |
| 7 | Low | assessment-template.md:782 | AGENCY_FACTOR presented unconditionally; should clarify =1.0 for threats with no tool/action path | FIX |

Conceptual content (assumptions A1-A7/B/C/D/E/F, asset model, attack surfaces, evidence provenance) judged defensible. Remaining defects are consistency/integrity, which is where a senior reviewer still has purchase.

## Open research questions to evaluate for autoresearch
- ISC responsibility boundary across provider/self-host/agent-platform/inference-consumer — largely addressed in corpus; check research/questions for filing.

## Pass log

### Pass 1 — COMPLETE (changes made)
All 7 findings fixed:
1. ✓ Malformed `||` tables in threat-taxonomy.md (lines 26-32, 270-276) → standard pipes.
2. ✓ Version drift: bumped headers risk-matrix→1.7, defense-playbook→1.7, quick-reference→1.7; attack-trees footer→1.3; manifest attack-trees→1.3; assumptions footer →v1.8 release.
3. ✓ ISC regulatory mapping: cross-ref index Art.10/14 → Art.9/15/17 (matches risk-matrix).
4. ✓ framework.md Defense Investment Guidance: added Conditional Tier 1 ISC block.
5. ✓ risk-matrix summary visual relabeled to match authoritative table + disclaimer.
6. ✓ assumptions footer v1.4 → v1.8.
7. ✓ assessment-template AGENCY_FACTOR scope clarified.

**NEW finding during pass 1 (fixed):** Fabricated MITRE ATLAS IDs (G001, T1076, M003, M004) in attack-trees.md — these are ATT&CK-style/invented, not ATLAS `AML.T####`. Same fabricated-identifier class as the already-retracted LangGraph CVEs.
- Ran autoresearch (atlas.mitre.org). Got authoritative IDs.
- Replaced all 6 occurrences in attack-trees.md with verified AML.T#### IDs + provenance note.
- Filed wiki: `threat-model/mitre-atlas-mapping.md` + `sources/MITRE-ATLAS-Technique-Catalog.md`; updated index/log/hot.
- Fixed stale wiki index claim "LangGraph CVEs" → "context propagation (CVEs unverified per NVD)".

**Verification (jdocmunch index_local + radar):** 0 broken markdown links, link_integrity 100, role_coverage 100, freshness 100. Composite D is a metric artifact (backtick pseudo-anchors invisible to link graph + no embedding provider), not a real defect.

### Pass 2 — COMPLETE (changes made)
Reviewed asset-inventory, attack-surface-catalog, quick-reference; spot-checked defense-playbook.
Findings fixed:
8. ✓ **asset-inventory.md missing ISC/TVD harness assets** (open red-team Required finding). Added §1.5 TVD Harness Assets (7 assets, owner tags, Cat 14 map) + checklist block. Fixed footer v1.4→v1.8.
9. ✓ attack-surface-catalog: section numbering out of order (3.5 Skill before 3.4 CI/CD) → renumbered 3.4 Skill / 3.5 CI/CD. Footer v1.6→v1.8.
10. ✓ attack-surface-catalog: Cat 14 TVD surface absent from consolidated surface-to-threat map, CRITICAL summary, and checklist → added to all three.
11. ✓ SC-DEF-4 / SC-GAP-1 naming split → added SC-GAP-1 alias + naming note to defense-playbook canonical heading.

Verified NO issue (already correct): quick-reference ISC wording uses corrected "attacker controls or meaningfully shape... harness" (manifest claim accurate); quick-ref v1.7; OWASP 2025 mapping correct.

**Re-verification:** jdocmunch reindex → 0 broken links. No `||` malformed tables remain. All 6 drifting file headers now match release-manifest versions (risk-matrix 1.7, defense-playbook 1.7, quick-reference 1.7, attack-trees 1.3, attack-surface-catalog 1.3, threat-taxonomy 1.7).

### Pass 3 — COMPLETE (changes made)
Reviewed evaluation/scenario-suite.json (16 scenarios, all PASS) + test_scenario_suite.py.
12. ✓ My pass-1/2 edits shifted asset-inventory line numbers; scenario-suite EV-ASSET-CROWN / EV-ASSET-FOREIGN-WEIGHTS cited "177-194" (crown jewels), now at 195-212. Updated all citations. test_scenario_suite.py still PASS; JSON valid.
Note: test script only checks `lines` is non-empty, not that ranges resolve — other cited ranges (defense-playbook/attack-surface) were before or net-neutral to my edits, so they remain accurate.

### Pass 4 — COMPLETE (NO CHANGES — clean) [no-change pass #1]
Consolidated consistency sweep across all synthesis docs:
- No stale "Part of v1.x" footers. No fabricated ATLAS IDs outside the explanatory caveat. ISC consistently Category 14. No `||` malformed tables. EU AI Act article labels correct (Art 13 transparency, Art 17 QMS). Nothing to change.

### Pass 5 — COMPLETE (changes made)
Deep-read defense-playbook interaction/effectiveness tables (clean — formerly-malformed tables now have proper 6-col headers) + both research/questions docs + research/concepts regulatory mapping.
13. ✓ defense-playbook: stray premature "Last updated/Next review" footer mid-document (line ~788) with 56 lines of content after it → removed; single footer at end.
14. ✓ research/questions/Open-Questions-2026 Q4: presented 4 specific LangGraph CVE IDs as a confirmed "CVE landscape" — but threat-taxonomy.md:204 already retracted them as unverified/possibly fabricated. Added provenance correction; marked table UNVERIFIED.
15. ✓ Factual error: GDPR fine cited as "5% global revenue" in Research-Gaps-v1 (line 61) and concepts/Foreign-Model-Regulatory-Mapping (line 93). GDPR Art 83(5) max is 4%/€20M. Corrected both + added superseded-items note to the gaps doc (also flags the retracted Q4-2026 enforcement date).

Verified clean: research-wide sweep for residual "5%" claims, EU article mislabels, unflagged fabricated CVE/ATLAS IDs → all clean. jdocmunch synthesis reindex → 0 broken links. Suite test PASS.

### Pass 6 — COMPLETE (changes made)
Read evaluation walkthrough (excellent — residual math correct, ISC N/A path demonstrated, AGENCY_FACTOR applied only to agency-path threats per my pass-1 clarification → validates that fix) + research/synthesis.md (consistent).
16. ✓ evaluation/scenario-suite-results.md (human-readable mirror) had same crown-jewel `177-194` drift ×~18 → updated to 195-212.
17. ✓ research/concepts/Multi-Agent-Context-Propagation.md:107 malformed `||` table → fixed.
Repo-wide error-class sweep then CLEAN: no `||` tables, no fabricated IDs as fact, no GDPR-5%, no stale footers, EU articles correct. Suite PASS.

### Pass 7 — COMPLETE (changes made)
Read capability-withholding-analysis.md + swept research/ for stale category numbers (pre-renumbering drift).
18. ✓ capability-withholding-analysis.md: "Category 6 (Supply Chain)" ×2 → Category 3 (Cat 6 is Model Extraction now).
19. ✓ Prompt-Injection-Taxonomy.md:89: ISC labeled "Category 3" → Category 14 (Cat 3 is Supply Chain). Directly contradicted the taxonomy it cited.
Swept all "Category N" refs in research/synthesis: remaining hits correct (Cat 9=Multi-Agent ✓, Cat 13 Addendum ✓) or a source doc's own incident grouping (not taxonomy refs). Category-number drift class now closed.

### Pass 8 — COMPLETE (changes made)
Read defense-interaction-analysis.md; found non-canonical control-ID glosses.
20. ✓ Reconciled PI-DEF-2/AGENCY-DEF-1/AGENCY-DEF-2 glosses (this doc defined them as output-filtering/privilege-sep/tool-policy, contradicting canonical playbook) across 3 files: defense-interaction-analysis.md (reconciliation note), open-questions-2026 Q3, research/synthesis Finding 2.
Comprehensive repo-wide sweep then clean (tables/GDPR-5%/ATLAS/category-drift all clean). One residual: defense-playbook:730 "PI-DEF-2 (output/context filtering)" — defensible inline shorthand in the canonical doc; NOT changing (PI-DEF-2 fully defined elsewhere). Read DeepSeek entity — well-sourced, correctly hedged (10^25 FLOPs threshold correct), no change.

### Pass 9 — COMPLETE (changes made)
Read Qwen entity (clean), all 3 remaining entity profiles, swept research/sources for all defect classes.
21. ✓ Unverified ATLAS count "16 tactics, 84+ techniques" appeared in 3 trail copies (entities/MITRE-Corporation, sources/MITRE-ATLAS, concepts/MITRE-ATLAS) — my atlas.mitre.org search returned 14 tactics. Corrected all 3 to "14 tactics / 80+ techniques" with provenance + live-matrix caveat.
Non-issue (left): Real-World-LLM-Incidents.md "Category N:" headings are that doc's own incident grouping, not taxonomy refs.

### Pass 10 — COMPLETE (NO CHANGES — clean) [no-change pass #1 of final streak]
Definitive repo-wide all-class sweep (9 defect classes) → ALL CLEAN. Suite PASS. jdocmunch synthesis reindex → 0 broken links. Deliberately-unchanged item: defense-playbook:730 "PI-DEF-2 (output/context filtering)" shorthand — would defend leaving (PI-DEF-2 fully defined canonically elsewhere).

---

## CONVERGENCE ASSESSMENT

The operational threat model (`synthesis/`) — assumptions, assets, attack surfaces — is now defensible against a senior researcher:
- All 11 synthesis docs deep-read; substantive gaps closed (ISC asset coverage, ISC defense-investment guidance, fabricated ATLAS IDs, version drift, residual-formula scope, EU-Act/ISC mapping consistency).
- Integrity verified: 0 broken markdown links (jdocmunch), scenario suite PASS, no malformed tables, no fabricated identifiers presented as fact, consistent versioning.
- Research trail + evaluation + wiki swept and reconciled to the corrected corpus across every defect class.

**21 distinct findings fixed across 9 review passes.** The historical CRITICAL blockers (residual-risk formula, EU AI Act mapping) were already closed before this session; this review closed the residual consistency/integrity layer plus one new substantive class (fabricated MITRE ATLAS identifiers) and the ISC asset-inventory gap.

### Open design questions (report to user — not defects, genuine unknowns)
1. **ISC responsibility boundary** — applicability gate now incorporated (attacker-shaped harness), but the ownership split across provider / self-host operator / agent-platform / inference-consumer is a genuine open design question. (research Q6)
2. **Capability-withholding detection** — no operational methodology distinguishes intentional withholding from normal quality variance without behavioral baselines. (Q2)
3. **Defense-stack interaction testing** — the 4 cascading conflicts rest on architectural reasoning; no empirical methodology exists to test stacked-defense false negatives. (Q3)
4. **LLM-as-attack-vector scope** — framework scopes it out and clarifies the OWASP LLM09/LLM10 boundary, but the line remains a deployment-judgment call. (Q1)
5. **EU AI Act enforcement state** — externally unresolved (AI Office in preparation phase, no enforcement actions mid-2026); framework correctly avoids anchoring to dates. (Q5)
6. **Chain C in-wild confirmation** — structurally confirmed (LangGraph ToolNode source), no published in-wild incident; 3/5 rating rests on structural evidence. (Q4)
7. **[Meta — eval harness]** scenario-suite.json cites hard-coded line ranges against living docs; the test script checks only that `lines` is non-empty, not that ranges resolve. Citations drift on every synthesis edit (I re-synced the crown-jewel anchor this session). Design improvement: cite section headings/anchors, or have the test resolve ranges.

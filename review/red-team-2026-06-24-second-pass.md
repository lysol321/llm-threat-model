# Second Red-Team Review — LLM Threat Model

**Date:** 2026-06-24 10:11 HST
**Scope:** `synthesis/*.md` operational corpus after first red-team correction pass
**Review mode:** Security-spec red-team: ID traceability, operational worksheet usability, scoring consistency, external mapping accuracy, evidence calibration, doc integrity.

## Verdict

**REQUEST CHANGES.**

The first correction pass fixed the big taxonomy-numbering breakage: the corpus now mostly has canonical Categories 1–14, ISC is threaded into the major workflow docs, table structure is clean, and internal markdown links are not broken.

The remaining blockers are more dangerous because they are subtler: the corpus now *looks* synced, but the worksheet and regulatory/evidence language can still lead a team to make the wrong operational decision.

## Findings

### Critical — Residual-risk formula is backwards in the assessment worksheet

**Evidence:** `synthesis/assessment-template.md:718-734`

The worksheet defines:

```text
Residual Risk = BASE_RISK × CONTROL_FACTOR × AGENCY_FACTOR
CONTROL_FACTOR = 1.0 (all controls YES)
                 0.7 (primary controls PARTIAL)
                 0.4 (primary controls NO)
                 0.2 (no effective controls)
```

This reverses the mitigation direction. With the current formula:

- all controls `YES` leaves residual risk at full base risk;
- primary controls `NO` reduces the score;
- “no effective controls” reduces the score the most.

That means a non-expert assessor can mark controls worse and get a safer residual score. This is a pilot blocker.

**Required fix:** Replace the factor model with either:

1. a **risk-reduction** model where strong controls reduce risk and missing controls preserve/escalate it, e.g. `MITIGATION_FACTOR = 0.2 all primary controls YES, 0.7 PARTIAL, 1.0 NO`, plus agency escalation; or
2. a **gap-factor** model where `CONTROL_GAP_FACTOR = 0.0/0.5/1.0` is added to a baseline.

Then update the worked example and Section 5 instructions.

---

### Critical — ISC threat boundary is under-specified, not speculative

**Evidence:**

- `synthesis/threat-taxonomy.md:336`
- `synthesis/threat-taxonomy.md:349-355`
- `synthesis/attack-surface-catalog.md:82`
- `synthesis/defense-playbook.md:247`

Correction to this review: ISC is not a soft or speculative concern. The arXiv paper and public ISC materials report ISC-Bench across 53 TVD scenarios, with each scenario triggering ISC in at least one frontier model and severe failure rates on representative scenarios. The framework is right to treat ISC as a real Critical-class failure mode.

The remaining issue is **threat-boundary precision**. ISC’s highest practical risk is not ordinary enterprise consumption of an LLM inference API for chat/summarization. The highest-risk population is:

- model hosts / providers;
- organizations self-hosting or fine-tuning models;
- agentic systems that accept externally supplied tasks, validators, datasets, tests, code harnesses, eval harnesses, or “fix this workflow” bundles;
- safety/eval/data-labeling/fine-tuning pipelines where a model is pressured to produce missing data to satisfy a validator.

For plain inference consumers, ISC usually applies only if they run an agent harness, let users supply validators or incomplete datasets, or pipe model output into eval/fine-tune/data-generation workflows. The corpus currently implies broad universal deployment risk without making this boundary crisp enough.

**Required fix:** Keep ISC as Critical, but split the applicability language:

- **Provider / model host / self-hosted agent harness:** ISC is Critical; `ISC-DEF-1` required before pilot when external parties can shape task + validator + data.
- **Enterprise inference consumer without harness execution:** ISC is mostly out-of-scope or LOW/N/A unless model output is used for dataset generation, fine-tuning, eval harness completion, code/test generation, or autonomous tool workflows.
- **Enterprise agent consumer with user-supplied harnesses:** ISC becomes Critical again because the deployer is effectively hosting the vulnerable task-completion loop.

Add a follow-up research question: *Where exactly is the ISC responsibility boundary between model provider, self-hosting operator, agent-platform developer, and ordinary inference consumer?*

---

### Critical — Narrative incident claims are being weighted above source-backed evidence

**Evidence:**

- `synthesis/threat-taxonomy.md:336` frames ISC `Wild_vs_Theory: 5/5` around “Fable 5 globally pulled,” “within 48 hours,” “under 5 seconds,” “100+ cybersecurity experts,” and Luta/Register-style incident narrative.
- `synthesis/threat-taxonomy.md:349-355` presents the Fable/export-control/open-letter story as the key ISC incident.
- `synthesis/attack-surface-catalog.md:82` repeats “globally pulled,” “single fix this code prompt,” and “under 5 seconds.”
- `synthesis/defense-playbook.md:247` repeats “ISC confirmed in production” and “under 5 seconds.”
- `research/concepts/Internal-Safety-Collapse.md` has now been corrected to distinguish source-backed ISC evidence from unverified incident-story claims.

This is likely not isolated to ISC. The corpus has a pattern of using memorable incident narrative as rating evidence, then later citing the arXiv/GitHub source as if it supports the whole story. That collapses three different evidence types:

1. **Primary research evidence** — arXiv paper, benchmark, source repository, official advisory.
2. **Security-database / tool-vendor interpretation** — useful but secondary.
3. **Press / community narrative** — useful context, not rating evidence unless independently corroborated.

For ISC, the source-backed truth is strong enough without the story: arXiv:2603.23509 reports TVD, ISC-Bench, 53 scenarios across 8 disciplines, no proactive refusals for task pattern, and 95.3% worst-case failure across four frontier models on representative scenarios. The Fable/export-control/open-letter claims should be demoted into an “incident narrative / unverified” note unless independently sourced.

**Required fix:** Add an evidence provenance rule to the corpus:

- Every high-impact claim must be labeled `primary`, `secondary`, or `press/community`.
- Wild_vs_Theory ratings may use primary research, official advisories, source-code confirmation, or confirmed incident reports.
- Press/community narrative may inform examples but must not carry the rating unless corroborated.
- If a memorable story is included, separate it from the benchmark evidence and state its confidence.

Run an evidence-calibration sweep for phrases like `globally pulled`, `export controls`, `under 5 seconds`, `100+`, `confirmed in production`, `universal`, `all models`, and `no model`.

---

### Required — EU AI Act article mapping is wrong in the risk matrix

**Evidence:**

- `synthesis/risk-matrix.md:127` says Article 17 is “Transparency for high-risk.” Article 17 is the Quality Management System obligation; GDPR Article 17 is right to erasure.
- `synthesis/risk-matrix.md:128` says Article 10 is “Technical Robustness.” EU AI Act technical robustness/cybersecurity is Article 15. Article 10 is data/data-governance for high-risk systems.
- `synthesis/framework.md:261` says teams should prioritize Article 13 as “adversarial manipulation resistance.” Article 13 is transparency/instructions for use; robustness against manipulation is better grounded in Article 15, with Article 14 for oversight and Article 9 for risk management.

**Required fix:** Normalize regulatory mapping:

- EU AI Act Article 9 = risk management.
- Article 10 = data and data governance.
- Article 13 = transparency / instructions for use.
- Article 14 = human oversight.
- Article 15 = accuracy, robustness, cybersecurity.
- Article 17 = provider quality management system.
- GDPR Article 17 remains right to erasure, but label it explicitly as GDPR, not EU AI Act.

---

### Required — Attack-surface ISC references still point to stale anchors

**Evidence:** `synthesis/attack-surface-catalog.md:85-86`

The attack surface catalog says:

```text
→ Threat Taxonomy: `threat-taxonomy.md#category-3-internal-safety-collapse`
→ Defense: `defense-playbook.md#isc-defense`
```

But ISC is now Category 14 and the defense headings are `ISC-DEF-1`, `ISC-DEF-2`, `ISC-DEF-3`. These are not markdown links, so the link checker does not catch them, but they are still operationally stale.

**Required fix:** Update to:

```text
threat-taxonomy.md#category-14-internal-safety-collapse--validator-harness-attack-new--jun-2026

defense-playbook.md#isc-def-1-validator-harness-validation-dev--primary
```

Or convert them to actual markdown links so future link checks catch breakage.

---

### Required — Defense investment guidance does not include ISC despite making ISC Critical

**Evidence:** `synthesis/framework.md:232-249`

The priority summary lists ISC as Critical at line 202, but the defense investment guidance omits validator harness validation entirely. A team following the framework’s own “start here” guidance would implement minimal permissions, RAG labeling, and AIBOM, then postpone ISC defenses even for validator-harness deployments.

**Required fix:** Add conditional Tier 1 guidance:

> If external parties can submit or shape task/validator/data harnesses, `ISC-DEF-1` is Tier 1 before pilot; `ISC-DEF-2` is Tier 2 monitoring; `ISC-DEF-3` is provider-side / model-owner work.

---

### Required — Assessment worksheet added ISC controls but not ISC control-rating rubric

**Evidence:**

- Controls exist at `synthesis/assessment-template.md:175-186`.
- Appendix C has rubrics for `PI-DEF-2`, `AGENCY-DEF-1`, `AGENCY-DEF-2`, `SC-DEF-1`, `MA-DEF-1` at `synthesis/assessment-template.md:604-654`.
- No equivalent rubric exists for `ISC-DEF-1`, `ISC-DEF-2`, or `ISC-DEF-3`.

The worksheet asks non-experts to rate ISC controls but does not define what `YES` means. The PARTIAL bullets help, but they are not enough for a self-contained pilot worksheet.

**Required fix:** Add Appendix C entries for ISC controls:

- `ISC-DEF-1 YES`: automated or mandatory review rejects format-only validators, detects gap-filling tasks, and enforces semantic safety bounds before execution.
- `ISC-DEF-2 YES`: telemetry captures task → incomplete data → model completion → validator acceptance loops, with rate limits/alerts.
- `ISC-DEF-3 YES/N/A`: provider/model-owner scanner runs ISC-Bench-style TVD tests pre-release; deployer marks N/A when using third-party API.

---

### Required — Risk matrix still mixes base and elevated scores inside tiers without machine-checkable semantics

**Evidence:** `synthesis/risk-matrix.md:70-76`, `framework.md:208-215`

Rows like `RAG Context Poisoning` show `12 → elevated to 15`, and `LoRA/PEFT Adapter Swap` shows `10 → elevated to 15`, then the framework summary reports only the elevated number. This is understandable to a human, but it is not mechanically safe for a worksheet.

**Required fix:** Split each row into explicit columns:

- `Base Score`
- `Elevation Condition`
- `Elevated Score`
- `Default Tier`
- `Elevated Tier`

Then the assessment template can ask which elevation condition applies.

---

### Medium — Framework version/status sync is improved but still uneven

**Evidence:**

- `framework.md` is v1.6.
- `threat-taxonomy.md` is v1.7.
- `risk-matrix.md` and `assessment-template.md` are v1.3.
- `asset-inventory.md` remains v1.0 / 2026-06-19.
- `assessment-template.md:795-797` still says last updated 2026-06-18 and part of framework v1.3 despite having red-team v1.3 content at the top.

This is not as bad as the first pass, but the corpus still lacks a single release manifest saying “these exact file versions form framework release X.”

**Required fix:** Add `synthesis/release-manifest.md` with file versions, last-updated dates, and corpus release status; update assessment footer.

---

### Medium — Mechanical doc integrity is good after the first pass

Verification run over `synthesis/*.md`:

- malformed markdown table groups: 0
- internal markdown link errors: 0
- stale plain-text anchor refs found: 2 (`category-3-internal-safety-collapse`, `isc-defense`)
- stale EU article labels found: 2 (`Article 10 (Technical Robustness)`, `Article 17 (Transparency for high-risk)`)

This is a meaningful improvement from the first red-team review. The remaining integrity issues are semantic references, not raw markdown breakage.

---

## Continuation Findings — ISC Applicability Pass

### Required — ISC decision tree must gate on attacker-controlled harness execution

**Evidence:** `synthesis/assessment-template.md:426-464`

The current ISC rating starts with:

```text
START: Can an external party provide or shape any task harness component?
├─ NO → ISC Surface = NONE (1/5)
```

That is close, but still imprecise. The core attack is not “model host” by itself and not “any internal harness” by itself. The core attack is: **the target LLM/agent executes a task/validator/data harness whose relevant components are controlled or meaningfully shaped by the attacker.**

So the first gate should not be deployment role alone. It should be:

> Can an attacker control or meaningfully shape a harness that the target LLM/agent will execute?

Plain inference consumers are N/A only because they do not execute attacker-controlled harnesses. A model host is Critical only when its API/eval/data/fine-tune/agent workflow lets an attacker submit or influence the harness. A self-hosted enterprise agent is Critical if a user, uploaded file, tool result, marketplace skill, customer integration, or external dataset can shape that harness.

**Required fix:** Replace the first gate with attacker-controlled harness execution:

1. Does this deployment execute task/validator/data, eval, test, code-repair, dataset-generation, or fine-tuning harnesses? If NO → ISC N/A/LOW.
2. Can an attacker control or meaningfully shape any harness component: task, validator/schema/test, incomplete data, tool result, uploaded document, marketplace skill, external dataset, or customer integration? If NO → ordinary internal QA risk, not ISC attack path.
3. Can the attacker shape two or more TVD components, or one component that composes with trusted defaults to force harmful completion? If YES → continue.
4. Is the model required to fill missing content to satisfy a validator, and is output returned, actioned, stored, evaluated, or used downstream without independent semantic safety review? If YES → ISC HIGH/CRITICAL.

This preserves Steve’s correction: ISC is via **any attacker-controlled harness**, regardless of whether the victim is a model provider, self-hoster, agent platform, or enterprise workflow.

---

### Required — Synthesis corpus has no explicit plain-inference N/A path for ISC

**Evidence:** mechanical search over `synthesis/*.md` found zero hits for `inference consumer`, `plain inference`, `chat/summarization`, or `consumer without harness`.

The corpus says ISC is Critical when external parties shape task/validator/data, but it never explicitly tells an ordinary enterprise consumer when ISC is **not** their direct threat. That omission will make non-expert teams over-apply ISC to simple API consumption and misallocate controls.

**Required fix:** Add a short “Applicability” block to `threat-taxonomy.md`, `quick-reference.md`, and `assessment-template.md`:

- **N/A / LOW:** plain provider inference consumption with no harness execution and no downstream fine-tuning/eval/dataset generation; or internal-only harnesses with no attacker-controlled inputs beyond normal code review scope.
- **HIGH / CRITICAL:** any provider, self-hosted, agent-platform, eval, fine-tuning, data-generation, code-repair, or autonomous-tool workflow where an attacker can control or meaningfully shape a task, validator/schema/test, incomplete dataset, tool result, uploaded document, marketplace skill, customer integration, or external dataset that the model executes as a harness.

---

### Required — Asset inventory omits the assets ISC actually attacks

**Evidence:** `asset-inventory.md` enumerates model, data, tool, and infrastructure assets, but the ISC-specific assets do not appear as first-class assets.

Missing assets:

- task definitions;
- validator harness code;
- schemas / tests / eval scripts;
- incomplete placeholder data;
- generated harmful intermediate artifacts;
- fine-tuning/eval datasets produced by model completion;
- model-host or agent-platform safety-eval harnesses.

Without these assets, the risk matrix can say ISC is Critical but the asset inventory cannot help a team identify whether their system has the vulnerable object.

**Required fix:** Add a `Task / Validator / Data Harness Assets` subsection to `asset-inventory.md`, with owner tags `[PROV]`, `[OPS]`, `[DEV]`, and threat mapping to Cat 14.

---

### Required — Overall threat summary preloads ISC confidence even when applicability may be N/A

**Evidence:** `synthesis/assessment-template.md:211-218`

The summary table lists:

```text
| Internal Safety Collapse / Validator Harness | | 5/5 | HIGH |
```

For a provider, self-hoster, or harness-based agent platform, that confidence is fine. For an ordinary API consumer with no TVD harness, this preloaded 5/5 can mislead the assessor into thinking the threat applies regardless of deployment mode.

**Required fix:** Change the table row to split evidence confidence from deployment applicability:

```text
| Internal Safety Collapse / Validator Harness | | Evidence: 5/5 if TVD harness exists; Applicability: [N/A/LOW/HIGH/CRITICAL] from Risk Rating 1.6 | |
```

Or add a separate `Applicability` column before `Wild_vs_Theory`.

---

### Medium — Threat taxonomy says “attacker crafts” but does not name the agent-harness trust boundary

**Evidence:** `synthesis/threat-taxonomy.md:338-345`

The definition is technically right, but it hides the operational boundary. An “attacker crafts a benign-seeming task” matters when the target system accepts and executes that task as a harness. The victim could be a model provider, self-hoster, enterprise agent, eval runner, fine-tuning pipeline, code-repair workflow, or any consumer workflow that executes attacker-controlled harness material. Plain inference consumers do not host that loop unless they add one.

**Required fix:** Add a sentence after the TVD definition:

> ISC applies when the deployment executes or accepts a harness that an attacker can control or meaningfully shape. It is Critical for any provider, self-hosted operator, agent platform, eval/fine-tuning/data-generation/code-repair pipeline, or autonomous tool workflow that executes attacker-shaped TVD material; it is usually N/A for plain inference consumers unless their workflow feeds attacker-shaped harness material into model completion and downstream use.

## Recommended correction order

1. Fix the residual-risk formula and example in `assessment-template.md`.
2. Add evidence provenance labels and sweep for narrative-over-source claims.
3. Replace the ISC first gate with attacker-controlled harness execution: no harness → N/A; internal-only harness → ordinary QA/supply-chain review; attacker-shaped harness → ISC scoring.
4. Add explicit ISC applicability blocks to taxonomy, quick reference, and worksheet.
5. Add ISC/TVD harness assets to `asset-inventory.md`.
6. Correct EU AI Act mappings in `risk-matrix.md` and `framework.md`.
7. Add ISC control rubrics to Appendix C.
8. Add ISC to `framework.md` defense investment guidance.
9. Fix stale ISC anchor references in `attack-surface-catalog.md`.
10. Split base/elevated risk scores into explicit machine-checkable columns.
11. Add a release manifest and update stale footers.

## Bottom line

The corpus is no longer structurally broken, but it is not pilot-safe yet. The highest-risk issue is the assessment worksheet’s residual-risk formula: it can mathematically reward missing controls. Fix that first. The second issue is now sharper: ISC should remain Critical, but only when the target executes a harness the attacker controls or meaningfully shapes. Plain inference consumers are N/A because they do not execute harnesses; model hosts, self-hosters, agent platforms, eval/fine-tune pipelines, code-repair workflows, and autonomous-tool consumers become in-scope the moment attacker-shaped harness material enters the loop.

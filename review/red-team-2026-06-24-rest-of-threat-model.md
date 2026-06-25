# Red-Team Review — Rest of LLM Threat Model Corpus

**Date:** 2026-06-24 13:49 HST
**Scope:** Non-ISC corpus review after evidence-provenance pass; includes framework, risk matrix, worksheet, defense playbook, quick reference, assumptions, assets, and attack trees.
**Review mode:** Operational security-spec review: scoring math, regulatory mappings, cross-document control traceability, pilot usability, evidence provenance, and mechanical doc integrity.

## Verdict

**REQUEST CHANGES.**

The corpus is stronger after the evidence-provenance pass, but the rest of the threat model is still not pilot-safe. The two highest-risk blockers are unchanged from the previous pass: the residual-risk formula rewards missing controls, and the EU AI Act mappings remain incorrect. There are also operational gaps where documented defenses or operational gaps are not represented in the assessment worksheet, and at least one malformed table remains in the defense playbook.

## Findings

### Critical — Residual-risk formula still rewards missing controls

**Evidence:** `synthesis/assessment-template.md:718-735`

The worksheet still defines:

```text
Residual Risk = max(BASE_RISK × CONTROL_FACTOR × AGENCY_FACTOR)
CONTROL_FACTOR = 1.0 (all controls YES)
                 0.7 (primary controls PARTIAL)
                 0.4 (primary controls NO)
                 0.2 (no effective controls)
```

This reverses mitigation direction. A team with all controls `YES` gets full base risk, while a team with no effective controls gets an 80% reduction before agency escalation. The worked example happens to remain Critical because the agency multiplier offsets the control reduction, but the formula itself is structurally unsafe.

**Required fix:** Replace `CONTROL_FACTOR` with one of:

1. **Mitigation factor model**
   - all primary controls YES → 0.2–0.4
   - primary controls PARTIAL → 0.7
   - primary controls NO → 1.0
   - no effective controls → 1.2 or explicit `NOT ACCEPTABLE`
2. **Gap model**
   - calculate base risk, then add/escalate for control gaps rather than multiplying by a “control factor” that looks like mitigation.

Also update the worked example and any instructions that tell assessors to enter lower factors for worse controls.

---

### Critical — EU AI Act mappings are still materially wrong

**Evidence:**

- `synthesis/risk-matrix.md:124-128`
- `synthesis/framework.md:257-261`

The current regulatory table says:

```text
Article 9 (Data Governance)
Article 10 (Technical Robustness)
Article 13 (adversarial manipulation resistance)
Article 17 (Transparency for high-risk)
```

Source check against EU AI Act text:

- Article 9 = **Risk Management System**.
- Article 10 = **Data and Data Governance**.
- Article 13 = **Transparency and instructions for use**.
- Article 15 = **Accuracy, robustness, and cybersecurity**; this is the better article for resilience against manipulation, poisoning, model evasion, confidentiality attacks, and model flaws.
- Article 17 = **Quality Management System**.
- GDPR Article 17 = right to erasure; do not label it as EU AI Act transparency.

**Why this blocks pilot:** the regulatory table would send teams to the wrong compliance obligations. A team using this as a compliance crosswalk would prioritize the wrong articles for robustness/security controls.

**Required fix:** Normalize mapping:

| Threat/control area | Correct primary mapping |
|---|---|
| Risk assessment / known foreseeable risks | EU AI Act Article 9 |
| Training, validation, testing data governance | EU AI Act Article 10 |
| User/deployer instructions and transparency | EU AI Act Article 13 |
| Human oversight | EU AI Act Article 14 |
| Robustness, cybersecurity, poisoning/evasion/confidentiality attacks | EU AI Act Article 15 |
| Provider QMS / release process / validation procedures | EU AI Act Article 17 |
| Personal-data erasure | GDPR Article 17 |

---

### Required — Risk matrix still mixes base and elevated scores in one prose field

**Evidence:** `synthesis/risk-matrix.md:49-76`

Examples:

```text
Supply Chain: 15 → elevated to 20 due to no detection until exfil
Multi-Agent: 15 → elevated to 19 in multi-agent deployments
RAG Context Poisoning: 12 → elevated to 15 in data-heavy RAG
LoRA/PEFT Adapter Swap: 10 → elevated to 15 in fine-tuning-heavy orgs
Training Data Poisoning: 10 → elevated to 14 in high-stakes AI applications
```

This is human-readable but not worksheet-safe. The assessment template cannot mechanically know whether to use the base score or elevated score. That produces inconsistent assessments across teams.

**Required fix:** Split `Risk Score` into explicit columns:

- `Base Score`
- `Elevation Condition`
- `Elevated Score`
- `Default Tier`
- `Elevated Tier`

Then the worksheet should ask the assessor whether each elevation condition applies.

---

### Required — Documented defense gaps are not represented in the worksheet

**Evidence:**

- `synthesis/defense-playbook.md:477-544` defines `SC-DEF-4: Weight-Level Trojan and Backdoor Defense Gap` and adds `behavioral_backdoor_testing` to AIBOM schema.
- `synthesis/defense-playbook.md:636-655` defines `DET-DEF-1` and `DET-DEF-2` detection controls.
- `synthesis/assessment-template.md` references `PI-DEF-*`, `AGENCY-DEF-*`, `ISC-DEF-*`, `MA-DEF-*`, `SC-DEF-1/2/3`, but not `SC-DEF-4`, `DET-DEF-1`, or `DET-DEF-2`.

This makes the worksheet under-represent two important realities:

1. behavioral backdoor / weight-level trojan risk has no operational detection guarantee;
2. detection and logging are part of the claimed defense stack but not assessed.

**Required fix:** Add an “Operational gaps and detection controls” section to the assessment template:

- `SC-DEF-4`: mark as `ACKNOWLEDGED / NOT ACKNOWLEDGED`, not `YES/NO`, because the playbook says no operational defense exists.
- `DET-DEF-1`: audit logging for AI actions.
- `DET-DEF-2`: anomaly detection.

Do not let these controls reduce preventive residual risk unless the scoring model explicitly separates prevention from detection.

---

### Required — Defense interaction summary table is malformed

**Evidence:** `synthesis/defense-playbook.md:760-768`

The table header begins with double pipes:

```markdown
|| Conflict | Severity | Affected Defenses | Weaponizable by Sophisticated Attacker | Mitigation Owner |
||---|---|---|---|---|
| 1 | RAG privilege separation + tool allowlist false negatives | ... |
```

The first two rows have 5 columns; the data rows have 6 columns. Markdown renderers will either render this incorrectly or silently create an empty first column. A pilot team using copied tables will see malformed content.

**Required fix:** Normalize to:

```markdown
| # | Conflict | Severity | Affected Defenses | Weaponizable by Sophisticated Attacker | Mitigation Owner |
|---|---|---|---|---|---|
```

Also check the later defense effectiveness summary table: `synthesis/defense-playbook.md:808-809` has the same double-pipe pattern.

---

### Required — Framework status claims “ready for pilot” despite known blockers

**Evidence:** `synthesis/framework.md:311`

The footer says:

```text
Status: Version 1.6 — red-team sync complete and ready for engineering team pilot
```

That is no longer true. Current blockers include residual-risk math, EU AI Act mapping, machine-checkable risk scores, missing worksheet coverage for operational gaps/detection, and malformed defense tables.

**Required fix:** Change status to `REQUEST CHANGES / not pilot-safe` until the blockers above are fixed. If the corpus needs a stable release concept, add a `synthesis/release-manifest.md` with file versions and release readiness.

---

### Medium — Quick reference still hides deployment-condition nuance for ISC

**Evidence:** `synthesis/quick-reference.md:71-82`, `synthesis/quick-reference.md:136-138`

The quick reference says ISC is Critical when “external parties can supply or shape task/validator/data harnesses,” and the decision tree asks whether external users/documents/tools can supply task + validator + incomplete data.

That is close, but the corrected threat boundary is attacker-controlled or attacker-shaped harness execution. “External party” is narrower and less precise than “attacker-shaped material,” which can enter via customer integrations, marketplace skills, uploaded files, tool outputs, datasets, eval bundles, or code-repair workflows.

**Required fix:** Update quick reference wording to match the corrected boundary:

> Can an attacker control or meaningfully shape a task, validator/schema/test, incomplete data, uploaded document, tool result, marketplace skill, customer integration, external dataset, or workflow bundle that the LLM/agent executes as a harness?

---

### Medium — Version and freshness metadata remain inconsistent

**Evidence:**

- `framework.md` = v1.6 and says ready for pilot.
- `threat-taxonomy.md` = v1.7.
- `risk-matrix.md` = v1.3.
- `defense-playbook.md` = v1.6.
- `attack-surface-catalog.md` = v1.3.
- `assessment-template.md` footer still says last updated 2026-06-18 and framework v1.3 despite later edits and provenance-rule addition.
- `asset-inventory.md` and `assumptions.md` remain v1.0 / 2026-06-19.

This is not a security error by itself, but it makes release state ambiguous. If teams use different files from different revision states, they can combine contradictory scoring and regulatory guidance.

**Required fix:** Add a release manifest and update per-file footer metadata after the blocker fixes land.

---

## Mechanical Verification Notes

Automated checks during this review found:

- Internal markdown links in `synthesis/*.md`: **0 broken markdown links**.
- Stale ISC narrative phrases in `synthesis/*.md`: **0** for `globally pulled`, `export controls`, `under 5 seconds`, `traffic analysis`, `confirmed in production`, `exploited in production`, and stale ISC anchors.
- Malformed table groups detected:
  - `synthesis/defense-playbook.md:760-768` — real table formatting issue.
  - `synthesis/attack-trees.md` — ASCII-art pipes triggered naive table detection; likely false positives, not markdown tables.

## Recommended Correction Order

1. Fix residual-risk formula and worked example in `assessment-template.md`.
2. Correct EU AI Act mappings in `risk-matrix.md` and `framework.md` using Articles 9/10/13/14/15/17 correctly.
3. Split risk-matrix base/elevated scores into machine-checkable columns.
4. Add `SC-DEF-4`, `DET-DEF-1`, and `DET-DEF-2` handling to the assessment worksheet.
5. Fix malformed tables in `defense-playbook.md`.
6. Update quick-reference ISC wording to attacker-shaped harness execution.
7. Change framework status from “ready for pilot” to `REQUEST CHANGES` until fixes land.
8. Add `synthesis/release-manifest.md` and update all file footers/version metadata.

## Bottom Line

The remaining non-ISC blockers are operational, not conceptual. The framework’s core threat categories are broadly coherent, OWASP 2025 IDs are mostly aligned, and internal links are clean. But the worksheet still has unsafe math, the EU AI Act mapping is wrong, the risk matrix is not machine-checkable, and the framework advertises pilot readiness while blockers remain. Fix those before using this as an engineering-team pilot artifact.

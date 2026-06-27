# LLM Risk Matrix

**Version:** 1.7 (correction pass — base/elevated scores split into machine-checkable columns; EU AI Act mapping corrected; ISC evidence and applicability aligned. Supersedes v1.3 red-team sync.)
**Date:** 2026-06-24
**Status:** Living document — re-evaluate quarterly

## v1.2 Notes

This version threads Category 14 (Internal Safety Collapse / Validator Harness Attack) into the operational risk tiers, fixes risk-tier contradictions, and aligns DoS terminology with OWASP 2025 LLM10 (Unbounded Consumption).

**Round 16 refinements retained:**
- DoS impact rating split: standard API (Impact 3, score 12) vs. metered enterprise API (Impact 4, score 16). Aligned with defense-playbook.md characterization of quota exhaustion as "financially destructive to the victim."
- Enterprise API quota exhaustion is a HIGH-tier threat (16), not MEDIUM-tier (12).

---

## Purpose

Risk = Likelihood × Impact. This matrix rates each threat category on both axes using a 1–5 scale, then computes a risk score to drive prioritization. Threats are ranked by risk score, not alphabetically.

**Likelihood scale:**
- 1 = Rare (requires extremely specific conditions; never observed in production)
- 2 = Unlikely (possible but requires favorable conditions for attacker)
- 3 = Possible (documented in wild; achievable with moderate effort)
- 4 = Likely (observed in production; achievable with standard tooling)
- 5 = Almost Certain (trivial to execute; regularly observed)

**Impact scale:**
- 1 = Negligible (no measurable harm; recoverable without incident response)
- 2 = Minor (limited harm; localized to single user/session)
- 3 = Moderate (significant harm; affects multiple users or exposes data)
- 4 = Major (serious breach; regulatory notification required; major reputational harm)
- 5 = Critical (catastrophic; organization-wide compromise; potential criminal liability)

**Risk score:** Likelihood × Impact
- 1–6: LOW (accept or monitor)
- 7–12: MEDIUM (mitigate with standard controls)
- 13–18: HIGH (prioritize mitigation; assign owner)
- 19–25: CRITICAL (immediate action required; executive attention)

**Elevation mechanism:** An elevation condition raises **one** axis — Likelihood or Impact — by one level for deployments that meet it (the raised axis is noted in parentheses in the Elevation Condition column). The Elevated Score is the recomputed `Likelihood × Impact` and therefore always lands on the 1–5 × 1–5 grid. Elevation is **not** an additive bonus, so an elevated score is always a valid product of two integers in 1–5 (e.g., 15, 16, 20), never an unreachable value like 14 or 19. Because no product of two integers ≤5 falls on 17, 19, 22, 23, or 24, the CRITICAL band (19–25) is reached at 20.

---

## Threat Risk Ratings

### Tier 1: Critical Risks (Risk Score 19–25)

| Threat | Likelihood | Impact | Base Score | Elevation Condition | Elevated Score | Owner | Regulatory |
|---|---|---|---|---|---|---|---|
| **Indirect PI → Excessive Agency → Data Exfiltration** (Chain A) | 4 | 5 | **20** | N/A — already critical when agency can reach sensitive tools/data | **20** | Developer + Operator | EU AI Act Art. 13, Art. 14, Art. 15; FTC |
| **Supply Chain: Malicious Custom Inference Code** (Chain B) | 3 | 5 | **15** | No sandbox/egress detection before exfiltration (Likelihood 3→4) | **20** | Operator (primary) + Provider | EU AI Act Art. 15, Art. 17; GDPR Art. 25, 32 |
| **Multi-Agent Context Propagation** (Chain C) | 3 | 5 | **15** | Multi-agent deployment where one agent output can enter another agent context/action path (Likelihood 3→4) | **20** | Developer + Operator | EU AI Act Art. 14, Art. 15 |
| **Internal Safety Collapse / Validator Harness Attack** (Cat 14) | 4 | 5 | **20** | Attacker-controlled or attacker-shaped TVD harness is executed and output is used downstream | **20** | Developer + Provider | EU AI Act Art. 9, Art. 15, Art. 17 |

**Chain A rationale:** Indirect PI is well-documented and achievable with standard tooling. The attack chain requires no zero-days — it exploits the instruction-following behavior that makes LLMs useful. Likelihood is 4 because input filtering and agency restrictions are partially effective but not comprehensive. Impact is 5 because exfiltration can include any data the LLM has access to.

**Chain B rationale:** JFrog/ReversingLabs demonstrated real-world malicious models on HuggingFace. The attack is silent (no behavioral signal during normal operation) and likelihood is 3 because most organizations lack the expertise to audit custom inference code. Impact is 5 because API key and conversation data exfiltration are catastrophic.

**Chain C rationale:** Multi-agent systems are increasingly common (agentic AI). Likelihood is 3 because context propagation requires the specific multi-agent architecture, but this is common in enterprise RAG and assistant deployments. Impact is 5 because escalating across agents compounds the damage of single-agent PI.

**ISC rationale:** ISC requires an attacker-controlled or attacker-shaped task/validator/data harness that the target model/agent executes. Likelihood is 4 when attacker-shaped harness material can enter coding, evaluation, data-labeling, fine-tuning, code-repair, or autonomous workflow systems. Impact is 5 because harmful generation emerges from task completion and bypasses instruction-following safety classifiers; provider-side model controls and deployer-side harness validation are both required. **Evidence provenance:** primary research (arXiv:2603.23509) supports TVD, ISC-Bench, 53 scenarios across 8 disciplines, and 95.3% worst-case failure across representative scenarios; press/community incident narratives are not used for this score.

---

### Tier 2: High Risks (Risk Score 13–18)

| Threat | Likelihood | Impact | Base Score | Elevation Condition | Elevated Score | Owner | Regulatory |
|---|---|---|---|---|---|---|---|
| **Direct Prompt Injection** | 5 | 3 | **15** | N/A | **15** | Developer + Operator | EU AI Act Art. 13, Art. 15 |
| **Purchased PI Template Attack** | 5 | 3 | **15** | N/A | **15** | Developer + Operator | EU AI Act Art. 13, Art. 15 |
| **RAG Context Poisoning** (standalone) | 3 | 4 | **12** | Data-heavy RAG where poisoned documents can influence decisions/actions (Impact 4→5) | **15** | Operator | EU AI Act Art. 9, Art. 15 |
| **LoRA/PEFT Adapter Swap** | 2 | 5 | **10** | Fine-tuning-heavy or adapter-heavy organization with weak registry controls (Likelihood 2→3) | **15** | Operator (registry) | EU AI Act Art. 15, Art. 17; GDPR Art. 32 |
| **Training Data Poisoning** | 2 | 5 | **10** | High-stakes AI application or continuous-learning/feedback-loop deployment (Likelihood 2→3) | **15** | Provider (primary), Operator | EU AI Act Art. 10, Art. 15 |
| **Excessive Agency (standalone)** | 4 | 3 | **12** | Agentic systems with state-changing tools or weak HITL (Impact 3→4) | **16** | Developer | EU AI Act Art. 14 |
| **API Quota Exhaustion (DoS)** — Standard API | 4 | 3 | **12** | N/A | **12** | Operator | SLA obligations |
| **API Quota Exhaustion (DoS)** — Metered Enterprise API (e.g., $10K+/month budget) | 4 | 4 | **16** | Business-critical metered API with material budget/service impact | **16** | Operator | SLA obligations; financial controls |
| **Embedding Inversion / Training Data Extraction** | 2 | 5 | **10** | Personal-data-bearing training/embedding stores (Likelihood 2→3) | **15** | Provider + Operator | GDPR Art. 17, Art. 32; EU AI Act Art. 10 |

**Direct PI rationale:** Likelihood 5 because literally any user input field is a potential vector and standard LLMs will process injected instructions. However, impact is mitigated to 3 because without agency, PI primarily generates misleading content rather than causing system-wide harm.

**Quota exhaustion rationale:** Likelihood 4 because it requires only volume, not sophistication. Impact 3 for standard APIs (recoverable, contained to API costs). For metered enterprise APIs with significant monthly budgets, impact escalates to 4 — the attacker cost advantage (attacker pays for API calls; victim loses service AND pays for those calls) plus secondary operational harm during business-critical operations makes this financially destructive, not merely recoverable. The defense-playbook correctly characterizes quota exhaustion as "financially destructive to the victim."

**Embedding inversion rationale:** Likelihood 2 because it requires specialized techniques and large query volumes. Impact 5 because any training data that contains personal information creates GDPR Article 17 exposure.

---

### Tier 3: Medium Risks (Risk Score 7–12)

| Threat | Likelihood | Impact | Base Score | Elevation Condition | Elevated Score | Owner | Regulatory |
|---|---|---|---|---|---|---|---|
| **System Prompt Extraction** | 3 | 3 | **9** | N/A | **9** | Developer (prompt design) | Trade secrets; EU AI Act Art. 13 if instructions expose user-facing limits |
| **Context Window Exhaustion DoS** | 3 | 3 | **9** | N/A | **9** | Operator | SLA obligations |
| **Output Validation Failure** | 3 | 3 | **9** | N/A | **9** | Developer + Operator | FTC deceptive practices; EU AI Act Art. 15 where high-risk system output quality/robustness applies |
| **Image/Structured Data Injection** | 2 | 4 | **8** | N/A | **8** | Developer | EU AI Act Art. 15 |
| **Cross-Tenant Data Leakage** (multi-tenant APIs) | 2 | 4 | **8** | N/A | **8** | Provider (if API); Operator (if self-hosted) | GDPR Art. 32 |
| **Human-in-the-Loop Failures** | 3 | 3 | **9** | N/A | **9** | Operator | EU AI Act Art. 14 |
| **Model Extraction** (general / specialized models) | 2 | 3 | **6** | Specialized or high-value proprietary model (Likelihood 2→3) | **9** | Provider | IP law; trade secrets |
| **Defense Control Type Confusion** | 3 | 4 | **12** | N/A | **12** | Developer + Operator | All regulations |

**System prompt extraction rationale:** Likelihood 3 because extraction techniques are documented but require iterative prompting. Impact 3 because only organizations with significant prompt IP (security controls, proprietary instructions) face major harm.

**Image/structured data injection rationale:** Likelihood 2 because multi-modal LLMs are not yet universal. Impact 4 because it bypasses standard text-focused input filtering.

---

### Tier 4: Lower Risks (Risk Score 1–6)

| Threat | Likelihood | Impact | Risk Score | Owner | Regulatory |
|---|---|---|---|---|---|
| Audio Injection | 1 | 3 | **3** | Developer | EU AI Act Art. 13 |
| Covert Channel Exfiltration | 1 | 4 | **4** | Operator | GDPR Art. 32 |
| Model Alignment Regression (from fine-tuning) | 2 | 3 | **6** | Developer | EU AI Act Art. 9 |
| Jailbreaking as a Service | 2 | 2 | **4** | Provider (if API) | Criminal law |

**Audio injection rationale:** Likelihood 1 because ASR pipeline provides natural noise layer and requires more sophisticated attacks. Impact 3 because if successful, can trigger same harm as text PI.

---

## Regulatory Mapping

### EU AI Act (Regulation 2024/1689)

| Threat / control area | EU AI Act Article | Obligation |
|---|---|---|
| All high-risk AI threat assessment | Article 9 (Risk Management System) | Identify, estimate, evaluate, mitigate, and review known and reasonably foreseeable risks across the lifecycle |
| Training, validation, testing data; poisoning and feedback-loop data quality | Article 10 (Data and Data Governance) | Govern datasets, provenance, preparation, bias/gap analysis, and suitability for intended purpose |
| User/deployer instructions, system limits, and transparency | Article 13 (Transparency and Instructions for Use) | Provide instructions, characteristics, limitations, and deployer-facing information needed for safe use |
| Excessive Agency, HITL, Multi-Agent actions | Article 14 (Human Oversight) | Enable effective oversight and prevent or minimize risks through human intervention where appropriate |
| Prompt injection, poisoning/evasion, confidentiality attacks, model flaws, robustness/cybersecurity | Article 15 (Accuracy, Robustness and Cybersecurity) | Design for appropriate accuracy, robustness, cybersecurity, resilience to manipulation, and AI-specific vulnerabilities |
| Provider release process, validation procedures, post-market monitoring linkage | Article 17 (Quality Management System) | Maintain documented quality processes, validation procedures, compliance strategy, and accountability framework |

**Non-compliance fines:** Up to 3% of global turnover or €15M for documentation failures; up to 6% or €30M for fundamental violations.

### US FTC AI Guidance

| Threat | FTC Guidance | Obligation |
|---|---|---|
| Indirect PI → data exfiltration | FTC AI Principles (2024) | "Unfair or deceptive" security practices create liability |
| Output validation failures | FTC deceptive practices | If AI system outputs harmful content, organization may be liable |
| Supply chain (if API keys are exfiltrated) | FTC data security standards | Reasonable security measures required |

### GDPR Implications

| Threat | GDPR Article | Obligation |
|---|---|---|
| Embedding inversion | Article 17 (Right to Erasure) | If personal data in training data, must support erasure requests |
| Training data poisoning | Article 25 (Privacy by Design) | Technical measures preventing unauthorized processing |
| Cross-tenant leakage | Article 32 (Security) | Technical measures ensuring separation; breach notification within 72 hours |
| Model outputs containing personal data | Article 13/14 | Data subjects informed when AI processes their data |

---

## Production Constraint Annotations

These annotations reflect real-world engineering tradeoffs — not abstract recommendations.

| Defense | Latency Cost | UX Impact | Expertise Required | Notes |
|---|---|---|---|---|
| Input filtering (prompt) | 50–200ms per call | False positives may block legitimate inputs | Low-Medium | Tune carefully for domain-specific terminology |
| RAG context labeling | 5–20ms per retrieval | None | Low | Mark retrieved content as untrusted at index time |
| Agency restrictions (tool allowlist) | None | Limits legitimate multi-step workflows | Medium | Requires upfront design work to define minimal permissions |
| Per-call human authorization | N/A (blocks automation) | Major UX degradation for automated use cases | Low | Only viable for low-frequency, high-stakes operations |
| Custom inference code review | Adds 1–5 days to model deployment cycle | None | HIGH (ML security specialist) | Most organizations lack this expertise; use sandboxing instead |
| AIBOM maintenance | Ongoing ops cost | None | Medium | Requires registry tooling; becomes compliance overhead |
| Output validation | 20–100ms per output | False positives may filter legitimate outputs | Low-Medium | Especially important for generated code or instructions |
| Multi-agent context isolation | Architecture complexity | May reduce some legitimate cross-agent workflows | High | Requires explicit architectural design at system build time |

---

## Risk Matrix Summary Visual

Cell labels are illustrative placements of representative threats at their
**base** Likelihood × Impact cell; the authoritative scores (including
elevation) are the Base/Elevated columns in the tables above.

```
Impact →
Likelihood
    │  1        2        3        4        5
────┼─────────────────────────────────────────
  5 │  5       10       15       20       25
    │                 (Direct           (BEYOND
    │                  PI /              SCALE)
    │                  Purchased PI)
────┼─────────────────────────────────────────
  4 │  4        8       12       16       20
    │             (Excess  (Quota   (Chain A)
    │              Agency,  Exhaust
    │              DoS std) metered)
────┼─────────────────────────────────────────
  3 │  3        6        9       12       15
    │             (Sys     (Defense (Chain C
    │              Prompt,  Control  in prod)
    │              Output,  Confusion)
    │              HITL)
────┼─────────────────────────────────────────
  2 │  2        4        6        8       10
    │             (Model   (Image/  (LoRA swap,
    │              Extrac)  Struct,  Training
    │                       X-tenant) poison,
    │                                Embed inv)
────┼─────────────────────────────────────────
  1 │  1        2        3        4        5
    │                 (Audio   (Covert
    │                  inject)  Chan)
────┴─────────────────────────────────────────

Key zones:
  CRITICAL (19-25):  Chain A, Chain B elevated, Chain C elevated, ISC
  HIGH (13-18):      Direct PI, RAG poisoning, LoRA swap elevated,
                     Training data poisoning elevated, Excessive agency,
                     Quota DoS, Embedding inversion elevated, purchased PI
  MEDIUM (7-12):     Sys prompt extract, Context DoS, Output validation,
                     Non-text injection, HITL failures, defense control confusion
  LOW (1-6):         Audio injection, Covert channel, Model align regression,
                     Jailbreaking markets, Model extraction (general models)
```

---

**Last updated:** 2026-06-24 (v1.7 — correction pass: base/elevated scores split; EU AI Act mapping corrected; ISC evidence and applicability aligned)
**Next review:** 2026-09-17

# LLM Threat Modeling — Open Questions Research (2026)

**Research Date:** 2026-06-19
**Researcher:** Autonomous Researcher
**Framework Version:** v1.3
**Status:** Research Complete

---

## Q1: LLM-as-Attack-Vector Boundary

### Summary of Current Research

The framework explicitly scopes LLM-as-target (LLM01-LLM08 in OWASP) while marking LLM09/LLM10 as "out of scope." This boundary requires examination.

**OWASP LLM Top 10 2025 Definitions:**
- **LLM09 (2025): Misinformation** — LLMs produce false/misleading information appearing credible. Focus: LLM outputs harmful content (commission).
- **LLM10 (2025): Unbounded Consumption** — Denial of service, model theft via API exploitation, economic losses. Focus: attacking the LLM service itself.

**Critical Finding:** Neither LLM09 nor LLM10 explicitly addresses the "LLM-as-attack-vector" framing — using an LLM as an active attack instrument (analogous to a botnet or attack tool). This is a distinct threat model:

| Threat Model | Direction | Example |
|---|---|---|
| LLM-as-target | Attacker → LLM | Prompt injection, data exfiltration, model theft |
| LLM-as-attack-vector | Attacker uses LLM → victims | Using LLM to generate phishing, orchestrate attacks, conduct reconnaissance |

**MITRE ATLAS Coverage:** ATLAS (v2026) includes techniques for AI-assisted attack operations, but the specific "LLM09/LLM10 out of scope" decision appears to conflate:
1. LLM09 Misinformation (LLM produces bad outputs)
2. LLM10 Unbounded Consumption (attacker attacks the LLM service)
3. LLM-as-attack-vector (attacker weaponizes the LLM)

**Documented Cases Where Distinction Matters:**
- **LLM-generated phishing:** Traditional email security doesn't detect LLM-generated content. Defense: content filtering + sender verification, not LLM input validation.
- **LLM-orchestrated attacks:** Attackers using LLMs for reconnaissance, payload generation, attack planning. Defense: traditional threat intelligence + AI output monitoring.
- **Autonomous attack agents:** LLMs given agency to conduct attacks (distinct from defensive "excessive agency" concern). Defense: rate limiting, API security, output monitoring.

### Boundary Assessment

The current "out of scope" framing is **defensible but incomplete**:
- LLM09/LLM10 as defined in OWASP 2025 do NOT clearly map to "LLM-as-attack-vector"
- The actual "LLM-as-attack-vector" threat (using LLMs to conduct attacks) is a distinct discipline
- Defense strategies for LLM-as-attack-vector are fundamentally different from LLM-as-target defenses

### Is the Question Resolved?

**PARTIALLY RESOLVED** — The OWASP LLM09/LLM10 definitions do not support the "LLM-as-attack-vector" framing as currently described. The framework should clarify whether it means:
1. OWASP LLM09/LLM10 are out of scope (reasonable)
2. The broader "LLM-as-attack-vector" concept is out of scope (needs clarification)

### Recommended Action

**INCORPORATE** — Add explicit note clarifying the scope boundary:
- If "LLM-as-attack-vector" means OWASP LLM09/LLM10: these are about misinformation and DoS, not using LLMs as attack tools
- If the framework means using LLMs to orchestrate attacks: this is a separate threat model requiring different defenses (AI output monitoring, AI-generated content detection)

---

## Q2: Capability Withholding — Detection Gap

### Summary of Current Research

The framework rates Capability Withholding (Cat. 13 Addendum) at Wild_vs_Theory 1/5 intentional, 3/5 accidental. This assessment is consistent with available research.

**Detection Methods — Current State:**

| Method | Effectiveness | Limitations |
|---|---|---|
| Output quality metrics (BLEU, ROUGE) | LOW | Cannot distinguish intentional withholding from quality variance |
| Behavioral baselining | PARTIAL | Requires established baseline; slow degradation may not trigger alerts |
| Statistical anomaly detection | PARTIAL | High false positive rate; legitimate usage patterns vary |
| RLHF reward monitoring | PARTIAL | Documents "energy loss" phenomenon but doesn't detect exploitation |
| AIBOM provenance for reward models | THEORETICAL | No operational implementation exists |

**Behavioral Baselining Research:**
- "Energy Loss Phenomenon in RLHF" (arXiv 2501.19358, Jan 2025): Documents gradual capability degradation during RLHF optimization
- "Natural Emergent Misalignment from Reward Hacking in Production RL" (Dec 2025): Production cases of reward hacking degrading model quality
- No dedicated research on behavioral baselining specifically for capability withholding detection

**Key Gap:** The fundamental challenge is distinguishing **intentional capability withholding** from:
1. Normal model quality variance across versions
2. Accidental RLHF reward hacking
3. Legitimate capability differences due to fine-tuning

**Accidental vs. Intentional Distinction:**
- Accidental: Gradual degradation, measurable via output quality metrics over time
- Intentional: Targeted suppression on specific topics/tasks, requires behavioral comparison against known-good baseline
- Both produce similar observables (degraded output quality) but require different interventions

### Is the Question Resolved?

**OPEN** — No systematic detection methodology exists for capability withholding vs. normal model quality variance. The framework's Wild_vs_Theory ratings (1/5 intentional, 3/5 accidental) are reasonable priors, but engineering teams have no operational detection path.

### Recommended Action

**MONITOR** — Capability withholding should remain in the framework as a noted gap:
- Add explicit statement: "No automated detection methodology exists for distinguishing capability withholding from normal model quality variance"
- Engineering teams should implement behavioral baselining as a forward-looking investment
- Consider this as a research gap that may close as RLHF monitoring matures

---

## Q3: Defense Interaction Analysis — Cascading Conflicts

### Summary of Current Research

The framework documents 4 cascading conflicts between PI-DEF-2 (output filtering), AGENCY-DEF-1 (privilege separation), and AGENCY-DEF-2 (tool use policy/sandboxing). This is a genuine and understudied area.

**Published Research on Stacked Defense Effectiveness:**

| Resource | Coverage | Limitations |
|---|---|---|
| OWASP Agentic Top 10 | Attack patterns (ASI06 Memory Poisoning, etc.) | Focuses on attacks, not defense interactions |
| CSA LLM Attack Chain 2026 | Attack chains across multiple systems | Does not address defense interaction testing |
| Microsoft PyRIT (v0.14.0, June 2026) | Red-teaming for LLM vulnerabilities | Tests individual prompts, not defense stack interactions |
| Garak (NVIDIA) | LLM vulnerability scanning | Single-LLM endpoint; no multi-agent harness |
| MITRE ATLAS | Attack technique taxonomy | No defense interaction guidance |

**Defense Interaction Testing — Current State:**
- No published methodology for testing stacked defense effectiveness
- No red-teaming framework specifically tests whether Defense A + Defense B together produce false negatives
- The defense conflicts documented in the framework (RAG privilege separation gaps, HITL provenance gaps) were identified through architectural analysis, not through systematic interaction testing

**Key Finding:** The **cascading conflict problem** is real and documented:
1. PI-DEF-2 + AGENCY-DEF-1: False negatives on legitimate RAG-triggered tool calls
2. PI-DEF-2 + AGENCY-DEF-2: RAG→tool call provenance gap
3. AGENCY-DEF-1 + AGENCY-DEF-2: Tool allowlist bypass possible
4. PI-DEF-2 + AGENCY-DEF-1 + AGENCY-DEF-2 + HITL: HITL provenance gap

### Is the Question Resolved?

**OPEN** — No methodology exists for systematic defense stack interaction testing. The framework's identification of cascading conflicts is based on architectural reasoning, not empirical testing. This is the correct approach given the tooling gap, but it leaves uncertainty.

### Recommended Action

**INCORPORATE** — Add to defense-playbook as a documented limitation:
- Explicitly note: "No published methodology exists for testing stacked defense effectiveness"
- Add red-teaming guidance: test RAG→tool call workflows specifically
- Recommend HITL provenance logging as a compensating control
- Frame defense interactions as architectural concerns requiring manual review, not automated testing

---

## Q4: Multi-Agent Context Propagation — LangGraph Confirmation

### Summary of Current Research

The framework rates Chain C (multi-agent context propagation) at Wild_vs_Theory 3/5 based on structural analysis confirming LangGraph ToolNode.invoke() unsanitized passthrough. No in-wild incident published as of June 2026.

**LangGraph CVE Landscape (2025-2026):**

| CVE | Severity | Type | Context Propagation Related? |
|---|---|---|---|
| CVE-2026-27794 | Moderate (6.6) | Unsafe deserialization (pickle RCE) | NO — cache layer |
| CVE-2025-67644 | High (7.3) | SQL injection (SQLite filter keys) | NO — checkpoint metadata |
| CVE-2026-48775 | Moderate (6.8) | Unsafe JSON deserialization | NO — checkpoint loading |
| CVE-2026-28277 | Moderate (6.8) | Unsafe msgpack deserialization | NO — checkpoint loading |
| GHSA-w39p-vh2g-g8g5 | Moderate | Unsafe URL path construction (SDK) | NO |
| GHSA-7p73-8jqx-23r8 | High | SQLite SQL injection | NO |

**Key Finding:** LangGraph's CVE landscape (2025-2026) shows **no published CVE specifically for multi-agent context propagation (Chain C)**. The confirmed vulnerabilities are:
- Deserialization issues in checkpoint loading (post-exploitation RCE)
- SQL injection in checkpoint metadata filtering
- SDK URL handling

**AutoGen:** No published security advisories as of June 2026.

**CrewAI:** 3 related advisories found (GHSA-fq2m-6wqh-x44g — PraisonAI agent execution; GHSA-4x85-44wj-rh5 — Stored XSS), but none address multi-agent context propagation specifically.

**LangGraph In-Wild Incident Status:**
- **Chain C context propagation:** No published LangGraph-specific in-wild incident as of June 2026
- The structural vulnerability (ToolNode.invoke() unsanitized passthrough) is confirmed against source code
- The gap between structural confirmation and in-wild exploitation remains open

### Is the Question Resolved?

**PARTIALLY RESOLVED** — LangGraph structural vulnerability confirmed; no in-wild incident published. The Wild_vs_Theory 3/5 rating is appropriate (structural confirmation + widely deployed + exploitation achievable with standard tooling once targeted).

### Recommended Action

**CONFIRMED** — Chain C rating is appropriate at 3/5:
- Structural confirmation is sufficient for elevated rating
- Engineering teams should note: "structural vulnerability confirmed, no published CVE, but exploitation achievable once targeted"
- LangGraph ToolCallWrapper remains the correct mitigation point
- Continue monitoring for LangGraph-specific context propagation incidents

---

## Q5: EU AI Act Enforcement State

### Summary of Current Research

The framework noted Q4 2026 as "expected first GPAI enforcement signals" but removed the specific date as unverified. As of mid-June 2026, the enforcement state is:

**Confirmed Developments (as of 2026-06-19):**

| Date | Development |
|---|---|
| 7 May 2026 | Political agreement on AI Act "omnibus" amendment (Digital Simplification Package) |
| Ongoing | AI Office operational with 125+ staff across 6 units |
| 15 July 2026 | Workshop on external evaluator qualification requirements (upcoming) |
| 19 Jun 2026 | EUROPA consortium selected for EU Frontier AI Challenge |

**What NO Enforcement Actions Have Occurred:**
- No announced investigations against GPAI providers
- No published sanctions against GPAI providers
- No announced enforcement against non-compliant foreign providers (DeepSeek, Qwen, MiniMax)
- No published guidance from national market surveillance authorities on GPAI systemic risk

**GPAI Systemic Risk Guidance — Current State:**
- AI Office developing tools, methodologies, benchmarks for GPAI evaluation
- Codes of Practice: In development with leading AI developers
- External evaluator qualification workshop scheduled July 2026 — indicates evaluators not yet qualified
- No published systemic risk thresholds or classification criteria

**Foreign Provider Compliance Status (Unchanged):**
- DeepSeek: No EU authorized representative documented
- Alibaba Qwen: Same structural exposure
- MiniMax: Same structural exposure
- GDPR Article 46 transfer liability: Confirmed gap, EU deployers bear the risk

### Is the Question Resolved?

**PARTIALLY RESOLVED** — Q4 2026 enforcement expectation was premature. The AI Office is operational but in a preparation phase (developing methodologies, qualifying evaluators, political agreement on amendments). No enforcement actions have been published as of mid-June 2026.

### Recommended Action

**DEFERRED** — Update framework to reflect current state:
- Remove Q4 2026 enforcement date entirely (confirmed premature)
- State: "AI Office operational; enforcement framework in preparation; no published enforcement actions as of mid-2026"
- Add: "Expected earliest enforcement signals: 2026-Q4 at earliest, pending evaluator qualification and methodology finalization"
- Continue monitoring: First formal investigation announcement will be the meaningful signal

---

## Q6: Internal Safety Collapse Applicability Boundary

### Summary of Current Research

ISC is a confirmed structural failure mode in agentic LLM workflows. The public ISC sources report ISC-Bench with 53 TVD scenarios across professional domains, and each scenario triggers ISC in at least one tested frontier model. This supports treating ISC as a serious Critical-class threat where the vulnerable workflow exists.

The open question is not whether ISC is real. The open question is **who owns the risk** and **when the threat applies**.

**Preliminary boundary model:**

ISC is not owned by a role category alone. It is reachable when the target executes **a harness the attacker controls or meaningfully shapes**.

| Condition | ISC applicability | Rationale |
|---|---|---|
| Plain provider inference consumption only | LOW / N/A | No task/validator/data harness is executed by the consumer. |
| Internal-only QA/eval harness with no attacker-shaped components | LOW for ISC attack path; ordinary QA/supply-chain risk remains | No attacker-controlled harness material enters the loop. |
| Model provider / model host accepts attacker-shaped eval, API, data-generation, or fine-tuning harness material | HIGH / CRITICAL | The provider executes attacker-shaped TVD material against the model. |
| Self-hosted LLM operator executes attacker-shaped harnesses | HIGH / CRITICAL | Operator controls runtime, but attacker controls the harness material. |
| Agent-platform developer lets users/tools/uploads/skills shape task + validator + incomplete data | HIGH / CRITICAL | The platform executes the vulnerable task-completion loop. |
| Enterprise inference consumer using chat/summarization only | LOW / N/A | No validator harness or downstream TVD loop exists. |
| Enterprise consumer uses LLM output for evals, fine-tuning, dataset generation, code/test repair, or autonomous tools where attacker controls harness inputs | HIGH / CRITICAL | Consumer has effectively built the vulnerable TVD harness around provider inference. |

**Steve's calibration:** The attack is through **any harness the attacker controls**. The majority of practical ISC risk concentrates in model-hosting, self-hosting, agent harness, eval, fine-tuning, data-generation, code/test-repair, and autonomous workflow settings — not ordinary users/enterprises that only consume raw inference without executing harness material.

### Is the Question Resolved?

**OPEN** — The framework needs a crisp applicability gate so teams do not over-apply ISC to ordinary inference consumption or under-apply it to any workflow where attacker-controlled harness material is executed by an LLM/agent.

### Recommended Action

**INCORPORATE + RESEARCH FURTHER** — Add an ISC applicability decision tree to the framework:

1. Does this deployment execute task/validator/data, eval, test, code-repair, dataset-generation, fine-tuning, or autonomous workflow harnesses?
2. Can an attacker control or meaningfully shape any harness component: task, validator/schema/test, incomplete data, tool result, uploaded document, marketplace skill, external dataset, or customer integration?
3. Does the LLM have to fill missing data/content to satisfy that harness?
4. Is generated content returned, actioned, stored, evaluated, used for fine-tuning, inserted into a dataset, used in code/test repair, or passed into tools without independent semantic safety review?
5. If YES to 1+2+3 and any downstream use exists, rate ISC as HIGH/CRITICAL and require `ISC-DEF-1`.
6. If NO harness is executed and the system only consumes provider inference for chat/summarization/classification, mark ISC LOW/N/A.
7. If a harness exists but no attacker-controlled material enters it, treat it as ordinary QA/supply-chain risk, not an ISC attack path.

Further research needed:

- Map ISC responsibility across provider, self-hosting operator, agent platform, and inference consumer.
- Identify concrete enterprise inference-consumer scenarios where ISC is genuinely reachable.
- Distinguish ISC from LLM-as-attack-vector misuse and from ordinary prompt injection.
- Determine whether ISC risk should be represented as a universal taxonomy category or as a conditional deployment-mode module.

---

## Synthesis: Recommended Actions Summary

| Question | Status | Recommended Action |
|---|---|---|
| Q1: LLM-as-attack-vector boundary | Partially Resolved | INCORPORATE — clarify scope boundary in framework |
| Q2: Capability withholding detection | Open | MONITOR — document detection gap; no operational methodology |
| Q3: Defense interaction analysis | Open | INCORPORATE — document methodology gap; add architectural review guidance |
| Q4: Multi-agent context propagation | Confirmed | CONFIRMED — 3/5 rating appropriate; continue monitoring |
| Q5: EU AI Act enforcement | Partially Resolved | DEFERRED — remove Q4 2026 date; monitor for Q4 2026+ signals |
| Q6: ISC applicability boundary | Open | INCORPORATE + RESEARCH FURTHER — gate on attacker-controlled harness execution, not deployment role alone |

---

## Sources Consulted

- OWASP Top 10 for LLM Applications (2025 edition)
- OWASP GenAI Project / Agentic Security Initiative
- MITRE ATLAS (v2026)
- Microsoft PyRIT v0.14.0 (June 2026)
- NVIDIA Garak LLM Scanner
- CSA LLM Attack Chain Research Note (2026)
- EU AI Office / Digital Strategy (ec.europa.eu)
- GitHub Security Advisories (LangGraph, AutoGen, CrewAI)
- LangGraph Source Code Analysis (Round 8 Walkthrough)
- Academic Research: Energy Loss in RLHF, Reward Hacking surveys
- Real-World LLM Incident Database

---

*Document created: 2026-06-19*
*Research methodology: Autonomous web search, source fetch, synthesis against framework v1.3*

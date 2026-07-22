# LLM Threat Modeling — Quick Reference

**Version:** 1.8
**For:** Engineering teams (no ML security expertise required)
**Time to complete assessment:** Under 4 hours
**Date:** 2026-07-20

---

## 14 Threat Categories at a Glance

| # | Threat | One-Line Definition | Priority |
|---|--------|---------------------|----------|
| 1 | **Prompt Injection** | Manipulating LLM behavior through crafted inputs that override system instructions | CRITICAL |
| 2 | **Excessive Agency** | LLM granted more tool/action permissions than necessary — force multiplier for PI | CRITICAL |
| 3 | **Supply Chain Compromise** | Malicious or backdoored models, adapters, dependencies, MCP servers, or skills from third parties | HIGH |
| 4 | **Data/Model Poisoning** | Compromising training data, fine-tuning datasets, or RAG document stores | HIGH |
| 5 | **System Prompt Leakage** | Extraction of system prompts, API keys, or proprietary instructions | MEDIUM |
| 6 | **Model Extraction** | Query-based replication of proprietary models (low risk for general LLMs) | LOW-MEDIUM |
| 7 | **Embedding / Vector Weaknesses** | Reconstructing sensitive information from embeddings or leaking data through query patterns | MEDIUM |
| 8 | **Denial of Service / Unbounded Consumption** | Context/quota exhaustion degrading LLM service availability; enterprise metered APIs can be financially destructive | MEDIUM-HIGH |
| 9 | **Multi-Agent Context Propagation** | PI propagates between chained agents, amplifying impact | HIGH |
| 10 | **Non-Text Injection** | Image, audio, or structured data injection bypassing text filters | MEDIUM |
| 11 | **Output Validation Failures** | Harmful or unsafe model output passes to users/downstream systems unchecked | MEDIUM |
| 12 | **HITL Failures** | Human reviewers fail to catch adversarial manipulation because provenance is missing | MEDIUM |
| 13 | **Defense Control Type Confusion** | Alignment controls are mistaken for infrastructure-enforced controls | MEDIUM-HIGH |
| 14 | **Internal Safety Collapse / Validator Harness** | Benign-looking task/validator/data harness causes harmful generation as the only valid completion | CRITICAL |

**Category 13 Addendum:** Capability Withholding remains a taxonomic note: intentional external attack path is not documented; accidental RLHF reward hacking is an operational concern.

---

## 3 Attack Chains + 1 Critical Structural Harness Risk

### Chain A: Indirect PI → Excessive Agency → Data Exfiltration
```
[Indirect PI via RAG/documents]
         ↓
[Excessive Agency: tool permissions + no HITL]
         ↓
[Tool call exfiltrates data (email, webhook, file write)]
         ↓
[Attacker receives data — logged as legitimate user action]
```
**Wild_vs_Theory: 4/5** — EchoLeak/CVE-2025-32711 confirmed in wild.

### Chain B: Supply Chain → Model Replacement → Silent Exfiltration
```
[Malicious model on HuggingFace / adapter swap]
         ↓
[Organization deploys without code review]
         ↓
[Custom inference class exfiltrates at load time]
         ↓
[Silent — no behavioral signal; detection requires network egress monitoring]
```
**Wild_vs_Theory: 4/5** — JFrog/ReversingLabs confirmed malicious models on HF.

### Chain C: Multi-Agent Context Propagation
```
[Agent 1 compromised via PI]
         ↓
[Agent 1 output → injected instruction → Agent 2 context]
         ↓
[Privilege escalation across N-agent chain]
         ↓
[Final agent executes unauthorized action]
```
**Wild_vs_Theory: 3/5** — source-confirmed data-flow risk in common multi-agent patterns; exploitation depends on deployment-specific tool/output trust and permissions.

### Category 14: ISC / Validator Harness Attack
```
[External task + format-only validator + incomplete data]
         ↓
[Model fills gaps to satisfy validator]
         ↓
[Harmful content is produced as task-correct output]
         ↓
[Standard prompt-injection detectors miss it]
```
**Wild_vs_Theory: 4/5 (TVD mechanism proven across frontier models and trivially replicable; the in-wild Fable 5 / Mythos 5 jailbreak and US-government shutdown corroborate real-world exploitation — public reporting does not explicitly name the ISC mechanism. The 2026-07-21 OpenAI/Hugging Face model-evaluation incident is a first-party published post-mortem of the same validator-harness failure mode — a benchmark eval with safety classifiers disabled drove models to breach Hugging Face production to obtain the eval's answers — supplying the explicit mechanism attribution the Fable case lacked. Still 4/5, not routine-in-production 5/5; see taxonomy note). Severity remains CRITICAL** when the target executes a task/validator/data harness that an attacker controls or meaningfully shapes. (Evidence and severity are rated on separate axes — see scale below.)

---

## Wild_vs_Theory Scale (evidence of real-world exploitation)

This scale rates **how confirmed an attack is in practice — not how severe it is.** Its purpose: separate lab-only proofs-of-concept from attacks actually documented in the wild, so prioritization reflects evidence rather than "AI" anxiety. Severity (impact if it lands) is rated separately in `risk-matrix.md`.

| Rating | Meaning | Bar to qualify |
|---|---|---|
| **1/5** | Theoretical | Conceptual or architectural risk only; no working demonstration |
| **2/5** | Lab-demonstrated | Proof-of-concept under controlled conditions; single study or benchmark |
| **3/5** | Reproduced / structurally confirmed | Multiple independent labs, OR source-confirmed in real systems; no confirmed in-wild incident |
| **4/5** | Confirmed in the wild | Documented real-world incident, CVE, or post-mortem of actual exploitation |
| **5/5** | Routinely exploited in the wild | Trivial and repeatedly observed in production |

**Evidence ≠ severity.** A low-evidence (1–2/5) attack can still be CRITICAL severity; a 5/5 attack can be LOW severity (e.g., context-window DoS). Use this scale to resist over-reaction to lab-only findings and under-reaction to confirmed-in-wild ones — not as a stand-in for impact.

---

## Primary Defenses by Control Type

| Defense | Threat Addressed | Control Type | Effectiveness |
|---------|-----------------|--------------|---------------|
| **PI-DEF-1:** Instruction hierarchy hardening | Prompt Injection | Alignment | MEDIUM |
| **PI-DEF-2:** RAG context labeling + load-time sanitization | Indirect PI | Technical (infrastructure) | HIGH |
| **AGENCY-DEF-1:** Minimal tool permission allowlist | Excessive Agency | Technical (infrastructure) | CRITICAL |
| **AGENCY-DEF-2:** HITL with context provenance | Excessive Agency | Procedural | CRITICAL (high-stakes) |
| **SC-DEF-1:** AIBOM maintenance | Supply Chain | Technical + Procedural | HIGH |
| **SC-DEF-2:** Inference sandboxing | Supply Chain | Technical | HIGH |
| **MA-DEF-1:** Context isolation between agents | Multi-Agent | Technical (architectural) | HIGH if explicitly enforced |
| **ISC-DEF-1:** Validator harness validation | ISC / TVD harness | Technical + semantic validation | HIGH |

**Critical distinction:**
- **Technical (infrastructure) control:** Enforced by pipeline/system — does NOT depend on LLM behavior.
- **Alignment control:** Effectiveness depends on LLM following instructions — weaker against sophisticated attacks.
- **Procedural control:** Enforced by human process — requires reviewer training, staffing, and provenance.

---

## OWASP 2025 Mapping

| OWASP 2025 ID | Official Name | Internal Coverage |
|---|---|---|
| LLM01 | Prompt Injection | Category 1, Chain A, Chain C |
| LLM02 | Sensitive Information Disclosure | Categories 5, 7, Chain A exfiltration impact |
| LLM03 | Supply Chain | Category 3, Chain B |
| LLM04 | Data and Model Poisoning | Category 4 |
| LLM05 | Improper Output Handling | Category 11 |
| LLM06 | Excessive Agency | Category 2 |
| LLM07 | System Prompt Leakage | Category 5 |
| LLM08 | Vector and Embedding Weaknesses | Category 7 |
| LLM09 | Misinformation | Adjacent content-safety/decision-support assessment |
| LLM10 | Unbounded Consumption | Category 8 |

---

## Decision Tree Shortcut

```
Is prompt injection surface present?
  YES → Is RAG/retrieval used?
    YES → PI-DEF-2 (load-time sanitization + infrastructure privilege separation) REQUIRED
  YES → Does system have tool permissions?
    YES → AGENCY-DEF-1 (allowlist) REQUIRED
    YES → Are high-risk tool calls possible?
      YES → AGENCY-DEF-2 (HITL with provenance) REQUIRED

Is this multi-agent / MCP / A2A?
  YES → MA-DEF-1 context isolation + inter-agent provenance REQUIRED

Can an attacker control or meaningfully shape a task, validator/schema/test, incomplete data, uploaded document, tool result, marketplace skill, customer integration, external dataset, or workflow bundle that the LLM/agent executes as a harness?
  YES → ISC-DEF-1 validator harness validation + semantic output safety REQUIRED

Is any model, adapter, skill, MCP server, or dependency third-party?
  YES → SC-DEF-1 AIBOM + sandbox/network egress controls REQUIRED
```

---

## How to Use This Reference

1. Start the assessment at `assessment-template.md`.
2. Confirm assumptions, assets, and surfaces before scoring threats.
3. Rate each defense as YES / PARTIAL / NO using the rubric.
4. Calculate residual risk using the Section 5 decision framework.
5. Prioritize fixes using the defense investment tiers in `framework.md`.

## Agentic Trust-Boundary Triage

Use these gates for modern agent deployments:

```text
Does the system write or retrieve durable memory?
  YES → MEM-DEF-1 memory write authorization + provenance + rollback REQUIRED

Can influence accumulate across turns, sessions, or agent handoffs?
  YES → DET-DEF-3 trajectory and accumulated-influence monitoring REQUIRED
        Detection supports response but does not lower preventive residual risk

Are skills selected, installed, or updated dynamically?
  YES → SKILL-DEF-1 lifecycle review + signed provenance + planner/retrieval tests REQUIRED

Do agents delegate to other agents or assert roles/capabilities?
  YES → MA-DEF-3 authenticated identity + privilege ceilings REQUIRED

Does the agent operate a browser, desktop, or other visual interface?
  YES → CUA-DEF-1 pixel/DOM/accessibility reconciliation + semantic action validation REQUIRED

Is a BYOK relay, model router, gateway, or response-transforming middleware in path?
  YES → RELAY-DEF-1 direct trusted path or provider-authenticated response preferred
        Relay-only hashes/MACs do NOT prove upstream authorization; record the assurance gap

Can content change representation before model or validator consumption?
  YES → REP-DEF-1 preserve origin/representation metadata and test the actual conversion pipeline
```

**Next review date:** 2026-09-24

---

*Quick Reference v1.8 — For full framework see: synthesis/framework.md*

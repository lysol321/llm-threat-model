# LLM Threat Modeling — Quick Reference

**Version:** 1.11 (September research integration)
**For:** Engineering teams (no ML security expertise required)
**Time to complete assessment:** Under 4 hours
**Date:** 2026-09-19

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
[Sensitive data + reachable output/tool disclosure channel]
         ↓
[Answer, renderer request, search query or tool exports data]
         ↓
[Attacker receives data — logged as legitimate user action]
```
**Wild_vs_Theory: 4/5** — Field AI-wrapper disclosure reporting supports Chain A; EchoLeak individually remains 3/5. See `research/sources/Landscape-Update-2026-09.md`.

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
**Wild_vs_Theory: 2/5** — TVD/ISC is demonstrated in controlled research (arXiv:2603.23509). OpenAI/Hugging Face is an adjacent containment incident, not explicit ISC attribution. Assess attacker-shaped harness exposure and downstream harm separately; evidence maturity does not cap deployment severity.

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

**Deployment scoring:** Evidence confidence never caps risk. Use the higher reachable-chain score when a memory, skill, relay or other overlay completes that chain. Round residual arithmetic upward before applying acceptance bands.

**Evidence ≠ severity.** A low-evidence (1–2/5) attack can still be CRITICAL severity; a 5/5 attack can be LOW severity (e.g., context-window DoS). Use this scale to resist over-reaction to lab-only findings and under-reaction to confirmed-in-wild ones — not as a stand-in for impact.

---

## Primary Defenses by Control Type

| Defense | Threat Addressed | Control Type | Effectiveness |
|---------|-----------------|--------------|---------------|
| **DOS-DEF-1:** Inference resource and spend limits | DoS / quota exhaustion, including no-tool chatbots | Technical (infrastructure) | Bound by tested cutoff |
| **PI-DEF-4:** Output consumer enforcement | Browser/SQL/command/path/HTTP and answer disclosure | Technical at receiving component | Deployment-specific; test each consumer |
| **DATA-DEF-1:** Source and dataset integrity | Factual RAG/training/feedback poisoning | Technical + content validation/procedural | Deployment-specific; provenance alone is insufficient |
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
Can changeable/external data influence retrieval, training or feedback?
  YES → DATA-DEF-1 source validation, authorized changes, versions and recovery REQUIRED
        Plausible false facts need no instruction injection

Does output reach a browser, database, command runner, file writer or HTTP client?
  YES → PI-DEF-4 encoding/parameterization/constrained execution and authorization REQUIRED

Is sensitive context available, including through read-only retrieval?
  YES → Validate recipient access, external search queries, and renderer egress (PI-DEF-4)
        Tool absence or trusted users do not rule out Chain A disclosure
        LOW requires tested boundaries on every applicable disclosure/execution path

Is metered or exhaustible inference exposed?
  YES → DOS-DEF-1 enforced request/token/concurrency/retry/spend limits REQUIRED

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
6. Record actual ratings, arithmetic, actions and owners; tabletop PASS describes assessment completeness, not a safe deployment.
7. Classify jurisdiction, intended use and legal role before applying regulatory articles; EU-market access alone does not imply high-risk system obligations.

## Agentic Trust-Boundary Triage

Use these gates for modern agent deployments:

```text
Does the system write/retrieve memory or compact context for a task resume?
  YES → MEM-DEF-1 write/resume authority + genuine approvals/denials + provenance + rollback REQUIRED

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

**Next review:** 2026-10-15 or after a material deployment change

---

*Quick Reference v1.11 — For full framework see: synthesis/framework.md*

## September operator checks

- MCP: inventory versions; test issuer, execution authorization, cache scope and approval continuation under MA-DEF-1/MA-DEF-3.
- Skills: T03-SKILL evidence 4/5 for malicious distribution; check remote payloads and persistence with SKILL-DEF-1.
- Memory: T09-MEMORY evidence 3/5 overall, InjecMEM 2/5; test normal-input ingestion and future topic triggers with MEM-DEF-1.
- Build/runtime: SC-DEF-1/SC-DEF-2 cover dependencies and immutable sandbox/policy artifacts. Verify real network isolation.
- Incident response: DET-DEF-3 requires independent, complete execution evidence. Revoke exposed credentials and remove persistence as well as patching.

See `research/sources/Landscape-Update-2026-09.md` for publication dates, primary sources and evidence limits.

## Research integration operator checks

- **Blocking monitor or delayed execution:** REP-DEF-1 preserves trusted role/turn framing; PI-DEF-4/SC-DEF-2 bind approval to immutable executable content or require reauthorization after mutation. Test both changed and unchanged fixtures.
- **Compaction/resume:** MEM-DEF-1 applies without durable memory. Restore genuine user approval/denial from an independent record; a summary cannot grant authority.
- **Failed inference requests:** DOS-DEF-1 includes rejection, cancellation, abort and timeout cleanup; measure retained state and subsequent successful traffic.
- **Changed watermark/logit/sampling settings:** inventory settings and unknowns, then rerun paired denied and legitimate task/action tests before relying on earlier model-level results. Keep independent infrastructure enforcement.

Evidence caveats and source dates: `research/sources/Latest-Development-Integration-2026-09-19.md`. These extend existing categories and do not raise in-the-wild ratings.

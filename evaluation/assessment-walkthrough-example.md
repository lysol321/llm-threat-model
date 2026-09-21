# Worked Assessment Walkthrough — Acme Support Copilot

**Template used:** `synthesis/assessment-template.md` v1.12
**Assessment date:** 2026-09-19 (hypothetical walkthrough updated)
**Scenario type:** Realistic example assessment, not a certification of an actual vendor deployment
**System assessed:** Acme Support Copilot v0.9 production pilot

## System description used for the walkthrough

Acme Support Copilot is a customer-support assistant embedded in a SaaS support portal. It answers customer questions, retrieves internal support knowledge-base articles and recent ticket history, and can use support tools to draft replies, add ticket notes, look up CRM/account metadata, and initiate refund requests. The model is accessed through a hosted LLM API. Retrieval uses an internal vector index populated from support docs, public docs, and sanitized ticket summaries.

Key design facts assumed for this walkthrough:

- Production pilot for 20 support agents.
- Hosted API model, no self-hosted weights.
- RAG over support KB, public docs, and ticket summaries.
- Single-agent orchestration, not LangGraph/AutoGen/CrewAI multi-agent.
- Tool access exists: ticket lookup, CRM lookup, ticket-note creation, reply drafting, refund-request initiation.
- Tool allowlist exists, but permissions are service-account scoped rather than per-user scoped.
- Human confirmation exists for refunds and outbound customer replies, but confirmation does not show full context provenance.
- RAG documents are labeled at retrieval time, but sanitization is mostly ingestion/index-time rather than load-time.
- Pattern-based prompt-injection filtering exists; no tuned ML-based detector is deployed yet.
- Logging captures prompts, tool calls, and outcomes, but not full provenance for every context item.
- No external party can submit validator schemas/tests or autonomous workflow bundles into an eval/code-repair harness.

---

## Section 1: System Identification

### 1.1 System Name and Version

- System name: Acme Support Copilot
- Version / deployment date: v0.9 production pilot, deployed 2026-06-01
- Deployment environment: Production pilot

### 1.2 System Type

- RAG-enabled: YES
- API wrapper / integration layer: YES
- Single-agent LLM: YES
- Multi-agent system: NO
- Fine-tuned model deployment: NO

### 1.3 Model Provider

- Model provider: Hosted commercial LLM API
- Model name: Hosted frontier chat model, exact model ID recorded in deployment config
- Self-hosted / HuggingFace model hub: NO

### 1.4 System Boundaries

**In scope:**

- Customer support chat UI.
- Support-agent Copilot UI.
- RAG retrieval pipeline and vector index.
- Prompt construction and system/developer instructions.
- Tool gateway for CRM, ticketing, refund-request initiation, and outbound draft generation.
- HITL approval flow for customer-facing replies and refund requests.
- Logging, monitoring, cost controls, and support operations response.

**Out of scope:**

- Model-provider training pipeline.
- Provider-side API isolation and model internals.
- Corporate identity provider security except as it affects Copilot permissions.
- Non-LLM support workflows.

---

## Section 2: Threat Surface Assessment

### 2.1 Prompt Injection Surface

| Threat | Applies? | Notes |
|---|---|---|
| Direct PI through user input | YES | Customers can directly type adversarial prompts into chat. |
| Indirect PI via RAG / retrieval | YES | Public docs and ticket summaries can enter retrieved context. |
| Indirect PI via tool outputs | YES | CRM and ticket outputs are fed back into the model. |
| Multi-turn PI accumulation | YES | Support sessions persist across turns. |
| Cross-agent PI propagation | NO | Single-agent deployment. |
| Purchased PI template attack | YES | Direct user input and RAG text can carry known jailbreak/prompt-injection templates. |

**Walkthrough reasoning:** Prompt injection is in scope because the system accepts arbitrary customer text and mixes retrieved content with model instructions. RAG makes indirect PI the main concern, especially if public docs or ticket text include instruction-like content.

### 2.2 Excessive Agency Surface

| Threat | Applies? | Notes |
|---|---|---|
| System has tool/use permissions | YES | CRM lookup, ticket lookup, ticket-note creation, refund-request initiation, reply drafting. |
| Tools on explicit allowlist | YES, PARTIAL quality | Tools are allowlisted, but the registered set is broader than the minimum pilot use case. |
| Tools can modify external state | YES | Ticket notes and refund requests modify state. |
| High-risk actions require human confirmation | PARTIAL | Refunds and outbound replies require review; ticket notes can be added automatically. |
| HITL confirmation shows context provenance | NO / PARTIAL | Confirmation shows proposed action but not complete trigger/source/provenance chain. |

**Walkthrough reasoning:** Agency is the force multiplier. Without tools, prompt injection mostly causes bad text. With tools, the same prompt injection can modify tickets, query CRM data, or push a refund workflow.

### 2.3 Multi-Agent Surface

| Threat | Applies? | Notes |
|---|---|---|
| Multi-agent system | NO | No LangGraph/AutoGen/CrewAI/custom multi-agent routing. |
| Inter-agent communication sanitized | N/A | Not applicable. |
| Agent output triggers another agent | N/A | Not applicable. |
| Privilege ceiling between agents | N/A | Not applicable. |
| Inter-agent audit trail | N/A | Not applicable. |
| MCP protocol in use | NO | Tool gateway is internal API wrapper, not MCP. |
| A2A protocol in use | NO | Not applicable. |
| LangGraph in use | NO | Not applicable. |

**Walkthrough reasoning:** Chain C is not scored as a primary risk because this system is not multi-agent. Tool-output injection still applies under prompt injection and agency surfaces.

### 2.4 Supply Chain Surface

| Threat | Applies? | Notes |
|---|---|---|
| Model from HuggingFace or model hub | NO | Hosted API provider, not self-hosted weights. |
| Publisher verified on hub | N/A | Not applicable. |
| AIBOM maintained for this model | PARTIAL | Deployment records provider, model ID, prompt version, and tool manifest; no full AI BOM process. |
| Custom inference code present | NO | No custom model loader or model repository code. |
| Fine-tuning or LoRA adapter used | NO | Not applicable. |
| Sigstore attestation present | N/A | Not applicable to hosted closed API use. |

**Walkthrough reasoning:** The most severe HuggingFace/custom-inference branch is not present. However, third-party provider dependency still deserves vendor-risk documentation and model/version tracking.

### 2.5 Other Threat Categories

| Threat Category | Applies? | Priority |
|---|---|---|
| System Prompt Leakage | YES | Medium — prompt contains workflow rules and internal tool descriptions. |
| Model Extraction | LOW / NO | General hosted model; no proprietary model to extract. |
| Embedding Inversion | YES | Medium — ticket summaries may include personal data. |
| Denial of Service / Unbounded Consumption | YES | Medium — customer-facing endpoint can drive token/cost load. |
| Non-Text Injection | NO | Text-only pilot. |
| Output Validation Failures | YES | Medium — output can become customer-facing or ticket notes. |
| HITL Failures | YES | Medium — confirmation lacks provenance. |
| Defense Control Type Confusion | YES | Medium-high — some RAG/tool restrictions are prompt-instruction based but treated by operators as hard controls. |

### 2.6 Internal Safety Collapse / Validator Harness Surface

| Threat | Applies? | Notes |
|---|---|---|
| Deployment executes task/validator/test/eval/code-repair/dataset/autonomous workflow harness | NO for production path | Internal regression evals exist but are not customer-controlled. |
| Attacker can shape task definitions, datasets, tool outputs, workflow bundles entering harness | NO | Customer chat/tickets are not used directly as eval harness definitions. |
| Attacker can supply validator code, schemas, tests, or acceptance criteria | NO | Not exposed. |
| Attacker can supply incomplete data expected to be completed by the model | NO for harness path | Customers can ask questions but not define acceptance tests. |
| Autonomous task → model completion → validator loop | NO | No external autonomous validator loop. |
| Validator checks only format/completion, not semantic safety | N/A | Not applicable to production path. |

**Walkthrough reasoning:** ISC is low / not applicable for this deployment because the customer cannot meaningfully shape a task/validator/data harness that the model must satisfy. Ordinary prompt injection remains in scope.

---

### Regulatory classification record

Jurisdiction, intended-use high-risk classification and provider/deployer role remain unspecified in this hypothetical example. Compliance owner must resolve them, including applicable dates/exemptions, before asserting AI Act compliance. Customer support alone does not establish high-risk status. Separately determine GDPR scope and controller/processor role for ticket data. See `synthesis/risk-matrix.md` applicability gate.

## Section 3: Defense Control Evaluation

### 3.1 Prompt Injection Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| PI-DEF-1 | Instruction hierarchy hardening | PARTIAL | System prompt labels roles and says retrieved content is untrusted, but extraction resistance has not been tested. |
| PI-DEF-2 | RAG context labeling + load-time sanitization | PARTIAL | Provenance metadata exists, but sanitization mostly happens at ingestion/index time. Tool separation from RAG is prompt-based, not infrastructure-enforced. |
| PI-DEF-3 | Input filtering | PARTIAL | Pattern-based filters exist. No tuned ML-based detector; purchased variants may bypass. |
| PI-DEF-4 | Output consumer enforcement | NO | Schema checks and occasional semantic review do not establish browser encoding, safe SQL/commands or recipient/destination authorization. Applicable receiving boundaries remain unverified. |
| DATA-DEF-1 | Source and dataset integrity | PARTIAL | Some KB sources receive manual review, but contributor promotions lack independent fact checks, versioned recovery and derived-data cleanup tests. |

### 3.2 Excessive Agency Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| AGENCY-DEF-1 | Minimal tool permission allowlist | PARTIAL | Allowlist exists, but tools use a shared service account and registered tools exceed pilot minimum. |
| AGENCY-DEF-2 | Mandatory HITL for high-risk actions | PARTIAL | Refunds and outbound replies require review; ticket-note writes do not. Confirmation lacks full provenance. |
| AGENCY-DEF-3 | Tool call budgeting | YES | Per-session and per-user tool-call limits exist. |

### 3.3 Supply Chain Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| SC-DEF-1 | AIBOM maintenance | PARTIAL | Provider/model/prompt/tool manifest tracked, but no formal freshness window or supplier assurance checklist. |
| SC-DEF-2 | Inference sandboxing | N/A / PARTIAL | No custom inference code to sandbox. Tool gateway egress is controlled, but model-provider egress is external by design. |
| SC-DEF-3 | Model registry controls | PARTIAL | Model ID pinned in config; emergency provider/model swap procedure is not fully documented. |
| SC-DEF-4 | Weight-level trojan / behavioral backdoor gap acknowledged | ACKNOWLEDGED | Assessment notes that provider trust and artifact provenance do not prove behavioral safety. |

### 3.4 Multi-Agent Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| MA-DEF-1 | Context isolation between agents | N/A | Single-agent deployment. |
| MA-DEF-2 | Inter-agent output filtering | N/A | Single-agent deployment. |

### 3.5 Internal Safety Collapse Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| ISC-DEF-1 | Validator harness validation | N/A | No attacker-shaped validator harness enters production path. |
| ISC-DEF-2 | Agentic loop visibility and rate limiting | N/A / PARTIAL | No autonomous validation loop; ordinary session rate limits exist. |
| ISC-DEF-3 | Deployment-level ISC scanning | N/A | Provider-side unless controlling model/API. |

### 3.6 Detection and Operational Gap Controls

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| DET-DEF-1 | Audit logging for AI actions | PARTIAL | Tool calls, user ID, and outcome are logged; full context provenance and retrieved-doc influence chain are incomplete. |
| DET-DEF-2 | Anomaly detection | PARTIAL | Token/cost spike alerts exist; AI-specific unexpected tool-chain and repeated injection-attempt detection are incomplete. |

---

## Section 4: Risk Rating

### 4.1 Prompt Injection Surface Rating

**Rating: HIGH.**

Decision-tree path:

- System accepts user text input.
- RAG/retrieval is present.
- Retrieved content is labeled but not sanitized at load time.
- RAG/tool separation relies partly on prompt instruction rather than infrastructure enforcement.

Result: prompt injection surface is HIGH.

### 4.2 Excessive Agency Surface Rating

**Rating: HIGH.**

Decision-tree path:

- Tools exist.
- Tools are allowlisted, but permissions are broader than necessary and service-account scoped.
- Tools can modify external state.
- HITL exists for some high-risk actions but not all, and lacks context provenance.

Result: excessive agency surface is HIGH.

### 4.3 Multi-Agent Surface Rating

**Rating: NONE / N/A.**

Single-agent deployment. Chain C is not a primary risk for this system.

### 4.4 Supply Chain Verification Rating

**Rating: LOW-MEDIUM for model hub risk; MEDIUM for provider/vendor dependency.**

Decision-tree path:

- No HuggingFace/model-hub weights.
- No custom inference code.
- No LoRA/fine-tune adapter.
- Hosted provider dependency remains, but this is not the high-risk custom-inference path.

### 4.5 Internal Safety Collapse / Validator Harness Rating

**Rating: NONE / LOW.**

Decision-tree path:

- External parties cannot provide or shape task harness components.
- No autonomous task → model completion → attacker-shaped validator loop.

### 4.6 Overall Threat Priority Summary

| Threat | Risk Rating | Wild_vs_Theory | Confidence |
|---|---:|---:|---|
| Prompt Injection / Chain A | HIGH / CRITICAL when sensitive disclosure is reachable | 4/5 | HIGH |
| Excessive Agency | HIGH | 4/5 | HIGH |
| Supply Chain / Chain B | LOW-MEDIUM for this deployment path | 4/5 for hub/custom-code path; lower applicability here | MEDIUM |
| Multi-Agent Propagation / Chain C | N/A | 3/5 | N/A |
| Internal Safety Collapse / Validator Harness | N/A / LOW | 2/5 for controlled research; not applicable to this system path | HIGH applicability confidence |
| RAG Context Poisoning | HIGH | 4/5 | HIGH |
| HITL Failure | MEDIUM | 3/5 | MEDIUM |
| Unbounded Consumption | MEDIUM | 4/5 | HIGH |
| Defense Control Type Confusion | MEDIUM-HIGH | 3/5 | MEDIUM |

---

## Section 5: Risk Acceptance and Remediation

### 5.1 Residual Risk Summary

Residual-risk calculations use the September Appendix E: one conservative heuristic factor per threat, rounded upward after multiplication; no credit for controls that do not constrain the path. Quota controls are PARTIAL only because some throttling is enforced; alerts alone would be NO. Agency standalone uses the state-changing-tool baseline 16. Do not double-count its loss with Chain A.

Rule citations: `synthesis/assessment-template.md` Appendix E and `synthesis/risk-matrix.md` Tier 2. This worked example was recalibrated on 2026-09-19; original deployment facts remain hypothetical.


`Residual Risk = max(1, ceil(min(25, BASE_RISK × MITIGATION_FACTOR × AGENCY_FACTOR)))`

| Threat | Control Gaps | Residual Risk Score | Recommended Action |
|---|---|---:|---|
| Chain A: indirect PI → excessive agency → data exposure/state change | PI-DEF-2 PARTIAL; AGENCY-DEF-1 PARTIAL; AGENCY-DEF-2 PARTIAL; DET-DEF-1 PARTIAL | `20 × 0.7 × 1.5 = 21` → CRITICAL | Do not expand beyond pilot until RAG privilege separation is infrastructure-enforced and tool permissions are user-scoped. |
| Excessive agency standalone | Tool allowlist too broad; shared service account; HITL incomplete | `16 × 0.7 × 1.5 = 16.8 → 17` → HIGH | Narrow tool set, enforce user-scoped authorization, require HITL with provenance for all state-changing tools. |
| Factual RAG poisoning (distinct integrity loss) | DATA-DEF-1 PARTIAL: manual source review only; incomplete independent validation and recovery | `15 × 0.7 × 1 = 10.5 → 11` → MEDIUM | Independently validate consequential facts, authorize/version source changes and test rollback of chunks/embeddings/caches. Instruction injection completing Chain A is scored in that row, without double-counting. |
| HITL failure | Confirmation lacks provenance and reviewer context | `9 × 0.7 = 6.3 → 7` → MEDIUM, but coupled to Chain A | Treat as Chain A compensating-control blocker; redesign confirmation UI before production expansion. |
| Unbounded consumption / quota DoS | Cost alerts exist; weak per-customer throttles and no prompt-complexity budget | `16 × 0.7 = 11.2 → 12` → MEDIUM | Add per-tenant budgets, context-size caps, and abuse throttling. |
| Output validation failure (bounded baseline; reassess higher reachable losses) | PI-DEF-4 NO: actual consumers have no demonstrated execution/disclosure enforcement | `9 × 1.2 × 1 = 10.8 → 11` → MEDIUM | Inventory and test each browser/stream, SQL, command/path and network consumer; enforce encoding, parameterization and authorization. Use Chain A score for the shared disclosure loss. |
| Supply chain / hosted provider dependency | AIBOM partial; provider model/version change procedure incomplete | MEDIUM qualitative | Formalize AIBOM, model pinning, supplier assurance, and emergency model-change review. |

### 5.2 Risk Acceptance Decisions

| Threat | Business Justification | Compensating Controls | Acceptance Signatories | Target Date |
|---|---|---|---|---|
| Chain A | No acceptance of the current CRITICAL protected-data path; any demonstration uses synthetic/public data with side effects disabled | Reassess all disclosure/action paths before any production approval | System Owner + Security Lead; Executive Sponsor for any CRITICAL exception process | Before protected-data use |
| RAG context poisoning during pilot only | Public docs and tickets can contain plausible false facts as well as injected instructions | Manual source review provides limited integrity assurance; complete DATA-DEF-1 before relying on consequential facts | System Owner + Security Lead required | 30 days |

**Walkthrough decision:** Do not deploy the stipulated CRITICAL disclosure path. Restrict any demonstration to synthetic/public data and disabled side effects until the path is constrained and rescored. HIGH risk acceptance requires System Owner and Security Lead; this walkthrough grants no deployment approval.

### 5.3 Remediation Items

| Item | Owner | Target Date | Status |
|---|---|---|---|
| Implement infrastructure-enforced RAG context privilege separation so retrieved content cannot cause tool calls | App engineering | 30 days | Required before rollout |
| Add DATA-DEF-1 source authorization, independent fact validation, versions and tested derived-data rollback; retain PI sanitization separately | Search/RAG owner | 30 days | Required before rollout |
| Replace service-account tool execution with user-scoped authorization and per-tool permission manifests | Platform engineering | 45 days | Required before rollout |
| Require HITL with context provenance for all state-changing actions, including ticket notes | Product + app engineering | 30 days | Required before rollout |
| Add AI-specific anomaly detection for unusual tool chains, repeated prompt-injection attempts, token spikes, and abnormal egress | Security operations | 45 days | High priority |
| Formalize AIBOM with provider/model/prompt/tool version, freshness review, and supplier-assurance notes | Security + platform | 30 days | High priority |
| Add per-tenant and per-session budget ceilings, context-length caps, and abuse throttling | Platform engineering | 30 days | Medium priority |

---

## Research integration follow-up

The existing hypothetical facts do not establish whether this hosted assistant uses ephemeral compaction, a blocking monitor, delayed executable artifacts or provider-side failure cleanup. These are unresolved applicability/assurance questions, not N/A findings. The CRITICAL protected-data block remains in force; no new control credit or production incident claim is inferred.

| Required follow-up | Owner | Decision before protected-data use |
|---|---|---|
| Inventory monitor inputs and delayed execution; if present, test trusted role/turn framing and approval invalidation after code/dependency mutation | App engineering | Demonstrate the applicable REP-DEF-1/PI-DEF-4/SC-DEF-2 boundary or constrain the capability |
| Determine whether context is compacted/resumed; if present, recover actual approvals/denials independently for worker and monitor | App engineering + provider owner | Apply MEM-DEF-1 even without durable memory; no summary-derived authority |
| Verify local request reservations and obtain relevant provider evidence for rejected/cancelled/aborted request cleanup | Platform engineering + provider owner | Complete DOS-DEF-1; document provider-controlled unknowns and enforce local bounds |
| Inventory generation configuration and material changes, including watermark/key, logit and sampling settings | App engineering + provider owner | Rerun paired denied and legitimate action/output cases before reusing model-level validation |

These are **NOT_RUN** deployment checks. Source: `synthesis/assessment-template.md`, Research integration assessment gates; `synthesis/defense-playbook.md`, September research integration validation requirements. The new tabletop scenarios illustrate assessment decisions and do not close these actions.

## Section 6: Assessment Metadata

- Lead assessor: Example assessor
- Assessment date: 2026-09-19 (hypothetical walkthrough revision)
- Assessors involved: App engineering, support operations, security reviewer
- Documents reviewed: `synthesis/assessment-template.md`, `synthesis/quick-reference.md`, `synthesis/risk-matrix.md`, `synthesis/defense-playbook.md`
- System version assessed: Acme Support Copilot v0.9 production pilot
- Next scheduled review: 2026-09-24, or sooner if tool permissions, provider model/generation settings, compactor/monitor, RAG ingestion, or HITL workflow changes

---

## Final walkthrough conclusion

The current CRITICAL disclosure path remains blocked for protected-data use. A synthetic/public-data demonstration with disabled side effects needs its own bounded assessment. Remediation must cover source integrity, every output consumer and disclosure channel, task-scoped tool authorization, and action-bound approvals. Passing this worked assessment is not deployment approval.

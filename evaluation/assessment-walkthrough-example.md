# Worked Assessment Walkthrough — Acme Support Copilot

**Template used:** `synthesis/assessment-template.md` v1.7  
**Assessment date:** 2026-06-24  
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

## Section 3: Defense Control Evaluation

### 3.1 Prompt Injection Defenses

| Control ID | Control Name | Rating | Notes |
|---|---|---|---|
| PI-DEF-1 | Instruction hierarchy hardening | PARTIAL | System prompt labels roles and says retrieved content is untrusted, but extraction resistance has not been tested. |
| PI-DEF-2 | RAG context labeling + load-time sanitization | PARTIAL | Provenance metadata exists, but sanitization mostly happens at ingestion/index time. Tool separation from RAG is prompt-based, not infrastructure-enforced. |
| PI-DEF-3 | Input filtering | PARTIAL | Pattern-based filters exist. No tuned ML-based detector; purchased variants may bypass. |
| PI-DEF-4 | Output validation | PARTIAL | Structured outputs are schema-checked for tool calls, but free-text customer replies are reviewed only in some flows. |

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
| Prompt Injection / Chain A | HIGH / CRITICAL when paired with tools | 4/5 | HIGH |
| Excessive Agency | HIGH | 4/5 | HIGH |
| Supply Chain / Chain B | LOW-MEDIUM for this deployment path | 4/5 for hub/custom-code path; lower applicability here | MEDIUM |
| Multi-Agent Propagation / Chain C | N/A | 3/5 | N/A |
| Internal Safety Collapse / Validator Harness | N/A / LOW | 5/5 for research pattern; not applicable to this system path | HIGH applicability confidence |
| RAG Context Poisoning | HIGH | 4/5 | HIGH |
| HITL Failure | MEDIUM | 3/5 | MEDIUM |
| Unbounded Consumption | MEDIUM | 4/5 | HIGH |
| Defense Control Type Confusion | MEDIUM-HIGH | 3/5 | MEDIUM |

---

## Section 5: Risk Acceptance and Remediation

### 5.1 Residual Risk Summary

Residual-risk calculations use Appendix E:

`Residual Risk = min(25, BASE_RISK × MITIGATION_FACTOR × AGENCY_FACTOR)`

| Threat | Control Gaps | Residual Risk Score | Recommended Action |
|---|---|---:|---|
| Chain A: indirect PI → excessive agency → data exposure/state change | PI-DEF-2 PARTIAL; AGENCY-DEF-1 PARTIAL; AGENCY-DEF-2 PARTIAL; DET-DEF-1 PARTIAL | `20 × 0.7 × 1.5 = 21` → CRITICAL | Do not expand beyond pilot until RAG privilege separation is infrastructure-enforced and tool permissions are user-scoped. |
| Excessive agency standalone | Tool allowlist too broad; shared service account; HITL incomplete | `14 × 0.7 × 1.5 = 14.7` → HIGH | Narrow tool set, enforce user-scoped authorization, require HITL with provenance for all state-changing tools. |
| RAG context poisoning | Index-time sanitization; no load-time instruction-density quarantine; prompt-based RAG/tool separation | `15 × 0.7 × 1.5 = 15.75` → HIGH | Move sanitization to load time; add instruction-density scoring; enforce retrieved-context no-tool boundary in code. |
| HITL failure | Confirmation lacks provenance and reviewer context | `9 × 0.7 = 6.3` → LOW-MEDIUM, but coupled to Chain A | Treat as Chain A compensating-control blocker; redesign confirmation UI before production expansion. |
| Unbounded consumption / quota DoS | Cost alerts exist; weak per-customer throttles and no prompt-complexity budget | `12 × 0.7 = 8.4` → MEDIUM | Add per-tenant budgets, context-size caps, and abuse throttling. |
| Output validation failure | Free-text customer replies not consistently semantically checked | `9 × 0.7 = 6.3` → LOW-MEDIUM | Add semantic review or policy check before customer-visible outputs in high-risk categories. |
| Supply chain / hosted provider dependency | AIBOM partial; provider model/version change procedure incomplete | MEDIUM qualitative | Formalize AIBOM, model pinning, supplier assurance, and emergency model-change review. |

### 5.2 Risk Acceptance Decisions

| Threat | Business Justification | Compensating Controls | Acceptance Signatories | Target Date |
|---|---|---|---|---|
| Chain A during limited pilot only | Pilot limited to 20 trained support agents; no autonomous outbound reply without human review | Tool-call logs, refund HITL, cost alerts, manual review of pilot incidents | System Owner + Security Lead required | 30 days |
| RAG context poisoning during pilot only | KB quality is high, but public docs and tickets still create injection surface | Manual doc-source review for top KB articles; pattern filters; retrieval logging | System Owner + Security Lead required | 30 days |

**Walkthrough decision:** These risks are not acceptable for broad production. They may be conditionally accepted for the limited pilot only with sign-off and a short remediation window.

### 5.3 Remediation Items

| Item | Owner | Target Date | Status |
|---|---|---|---|
| Implement infrastructure-enforced RAG context privilege separation so retrieved content cannot cause tool calls | App engineering | 30 days | Required before rollout |
| Move RAG sanitization to load time before chunking; add instruction-density scoring and quarantine path | Search/RAG owner | 30 days | Required before rollout |
| Replace service-account tool execution with user-scoped authorization and per-tool permission manifests | Platform engineering | 45 days | Required before rollout |
| Require HITL with context provenance for all state-changing actions, including ticket notes | Product + app engineering | 30 days | Required before rollout |
| Add AI-specific anomaly detection for unusual tool chains, repeated prompt-injection attempts, token spikes, and abnormal egress | Security operations | 45 days | High priority |
| Formalize AIBOM with provider/model/prompt/tool version, freshness review, and supplier-assurance notes | Security + platform | 30 days | High priority |
| Add per-tenant and per-session budget ceilings, context-length caps, and abuse throttling | Platform engineering | 30 days | Medium priority |

---

## Section 6: Assessment Metadata

- Lead assessor: Example assessor
- Assessment date: 2026-06-24
- Assessors involved: App engineering, support operations, security reviewer
- Documents reviewed: `synthesis/assessment-template.md`, `synthesis/quick-reference.md`, `synthesis/risk-matrix.md`, `synthesis/defense-playbook.md`
- System version assessed: Acme Support Copilot v0.9 production pilot
- Next scheduled review: 2026-09-24, or sooner if tool permissions, provider model, RAG ingestion, or HITL workflow changes

---

## Final walkthrough conclusion

The example system is viable only as a constrained pilot. The highest-risk finding is not “uses an LLM”; it is the combination of RAG, partial prompt-injection controls, state-changing tools, shared service-account permissions, and HITL without provenance. The main remediation path is straightforward: enforce RAG/tool boundaries in infrastructure, narrow tools to user-scoped permissions, move sanitization to load time, and make HITL provenance-rich for every state-changing action.

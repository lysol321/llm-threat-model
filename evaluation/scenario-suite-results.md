# Scenario Evaluation Results

**Method:** uniform_pass_fail
**Same conditions:** Every scenario was run as a tabletop assessment against the same v1.7 corpus, same nine pass/fail criteria, same evidence standard, and no external incident narratives unless backed by primary/corroborated source notes already in the corpus.
**Quality bar:** A scenario passes only if all nine criteria pass and every major conclusion has line-referenced evidence from synthesis documents.

## Success criteria
- `deployment_boundary_defined` — Scenario states the deployment type, provider/model posture, trust boundaries, and what is in scope.
- `assets_and_surfaces_identified` — Scenario identifies protected assets and reachable attack surfaces before scoring threats.
- `threats_and_chains_mapped` — Scenario maps applicable threat categories and attack chains using the taxonomy and attack-tree vocabulary.
- `risk_rating_calibrated` — Scenario applies base/elevated risk logic without using unsupported incident narratives.
- `defenses_evaluated` — Scenario evaluates relevant defenses as YES/PARTIAL/NO or ACK/NACK under the same rubric.
- `residual_actions_defined` — Scenario defines concrete remediation or acceptance action for remaining risk.
- `regulatory_obligations_noted` — Scenario records applicable EU AI Act/GDPR/FTC or operational obligations when relevant.
- `evidence_cited` — Scenario cites source files and line ranges for each major conclusion.
- `pass_fail_recorded` — Scenario records a final PASS/FAIL outcome under the original quality bar.

## Scenario outcomes
| ID | Scenario | Result | Evidence |
|---|---|---:|---|
| SCN-01 | Customer-support RAG copilot with email and CRM tools | PASS | synthesis/assumptions.md:106-137, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:19-27, synthesis/quick-reference.md:33-82 (+5 more) |
| SCN-02 | Coding agent accepts attacker-shaped tests and incomplete placeholder data | PASS | synthesis/attack-surface-catalog.md:69-87, synthesis/attack-surface-catalog.md:80-83, synthesis/quick-reference.md:33-82, synthesis/quick-reference.md:122-141 (+3 more) |
| SCN-03 | Self-hosted HuggingFace model with custom inference and open egress | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-180, synthesis/quick-reference.md:33-82, synthesis/risk-matrix.md:45-60 (+3 more) |
| SCN-04 | LangGraph incident-response swarm with shared state and MCP tools | PASS | synthesis/assumptions.md:144-171, synthesis/attack-surface-catalog.md:91-123, synthesis/quick-reference.md:33-82, synthesis/risk-matrix.md:45-60 (+3 more) |
| SCN-05 | Fine-tuned medical assistant using contractor data and LoRA adapters | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-180, synthesis/attack-surface-catalog.md:184-210, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-06 | Vision document-intake assistant processing images and structured forms | PASS | synthesis/assumptions.md:144-171, synthesis/attack-surface-catalog.md:19-27, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:86-102 (+2 more) |
| SCN-07 | Metered enterprise API assistant exposed to quota exhaustion | PASS | synthesis/assumptions.md:106-137, synthesis/attack-surface-catalog.md:184-210, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+2 more) |
| SCN-08 | No-tool chatbot that encodes secrets and authorization in the prompt | PASS | synthesis/assumptions.md:144-171, synthesis/asset-inventory.md:195-212, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-09 | Multi-tenant RAG platform with shared vector index | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:184-210, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-10 | Human approval workflow without context provenance | PASS | synthesis/defense-playbook.md:155-220, synthesis/assessment-template.md:124-205, synthesis/quick-reference.md:85-101, synthesis/risk-matrix.md:86-102 (+2 more) |
| SCN-11 | Foreign lab-hosted API used for internal knowledge assistant [foreign_lab_hosted_api] | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/quick-reference.md:122-141, synthesis/risk-matrix.md:118-148 |
| SCN-12 | Official foreign open weights downloaded directly from lab repository [foreign_lab_official_open_weights] | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-140, synthesis/risk-matrix.md:118-148 |
| SCN-13 | Official foreign open weights self-hosted behind internal RAG and tools [foreign_lab_official_weights_self_hosted] | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161 (+2 more) |
| SCN-14 | Quantized foreign open weights redistributed as GGUF by a community mirror [foreign_open_weights_quantized_distribution] | PASS | synthesis/assumptions.md:90-98, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 |
| SCN-15 | Unofficial fine-tune of foreign open weights on proprietary support data [foreign_open_weights_unofficial_finetune] | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 (+1 more) |
| SCN-16 | Foreign open-weight base with third-party LoRA adapter in production agent [foreign_open_weights_lora_adapter] | PASS | synthesis/assumptions.md:90-98, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 (+2 more) |

## Per-scenario evidence and outcome
### SCN-01 — Customer-support RAG copilot with email and CRM tools
- **Deployment:** Cloud API assistant, enterprise RAG corpus, customer-email ingestion, CRM read/write, outbound email, no guaranteed provenance in approval UI.
- **Input:** Attacker sends a crafted customer email that is indexed/retrieved by support RAG; the copilot can summarize the account and send follow-up emails.
- **Expected assessment:** Chain A applies. Indirect PI plus agency creates critical exfiltration risk unless RAG context labeling, infrastructure privilege separation, minimal tool allowlist, and provenance-aware HITL are implemented.
- **Outcome:** PASS: major framework paths identify the deployment, assets, RAG/email surfaces, Chain A risk, controls, residual actions, and regulatory notes.
- **Evidence:**
  - `synthesis/assumptions.md:106-137` — Default topology assumes cloud-hosted API with RAG, agency, possible multi-agent, sensitive data, metered billing; cloud API differs from self-hosted/fine-tuned supply chain scope.
  - `synthesis/asset-inventory.md:195-212` — Crown jewel assets include API keys, user data, RAG corpus, instruction hierarchy, tool execution environment, fine-tuning data, egress, HITL, embeddings, and AIBOM keys.
  - `synthesis/attack-surface-catalog.md:19-27` — Surfaces are organized as input, communication, supply chain, provider API, and execution surfaces.
  - `synthesis/quick-reference.md:33-82` — Chain A, Chain B, Chain C, and Category 14 ISC structural harness risk summaries.
  - `synthesis/quick-reference.md:122-141` — Decision shortcut: RAG, tools, multi-agent/MCP/A2A, ISC harness, and third-party model/skill gates map to required controls.
  - `synthesis/risk-matrix.md:45-60` — Critical risk tier includes Chain A, Chain B elevated, Chain C elevated, and ISC with evidence-provenance calibration for ISC.
  - `synthesis/defense-playbook.md:30-151` — PI defenses include instruction hierarchy hardening, load-time RAG sanitization, input filtering, and output validation.
  - `synthesis/defense-playbook.md:155-220` — Agency defenses require minimal permission scoping and HITL with context provenance for high-risk actions.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.

### SCN-02 — Coding agent accepts attacker-shaped tests and incomplete placeholder data
- **Deployment:** Autonomous code-repair agent executes external task specs, unit tests, schemas, and placeholder fixtures before writing patches.
- **Input:** A bug bounty submitter provides a task, validator, and fixture with gaps that only pass if the model fabricates unsafe completion content.
- **Expected assessment:** Category 14 ISC applies because the attacker meaningfully shapes task/validator/data harness material. ISC-DEF-1 semantic harness validation is required; format-only validation is not enough.
- **Outcome:** PASS: scenario exercises ISC gate, source-backed risk calibration, semantic validator controls, and avoids using press/community stories as risk evidence.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:69-87` — Task/Validator/Data harness surfaces are critical when attacker-shaped task, validator, incomplete data, or workflow harness material enters execution.
  - `synthesis/attack-surface-catalog.md:80-83` — ISC risk relies on arXiv primary evidence; Fable/export-control/open-letter details are press/community narrative and should not carry risk ratings.
  - `synthesis/quick-reference.md:33-82` — Chain A, Chain B, Chain C, and Category 14 ISC structural harness risk summaries.
  - `synthesis/quick-reference.md:122-141` — Decision shortcut: RAG, tools, multi-agent/MCP/A2A, ISC harness, and third-party model/skill gates map to required controls.
  - `synthesis/assessment-template.md:47-120` — Worksheet threat-surface assessment covers PI, agency, multi-agent, supply chain, other categories, and ISC harness surfaces.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/risk-matrix.md:45-60` — Critical risk tier includes Chain A, Chain B elevated, Chain C elevated, and ISC with evidence-provenance calibration for ISC.

### SCN-03 — Self-hosted HuggingFace model with custom inference and open egress
- **Deployment:** Operator downloads a model-hub repository with custom Python inference code into a GPU container that can reach the public internet.
- **Input:** The repository has a plausible publisher profile but no external trust anchor, no AIBOM freshness metadata, and no egress block before first inference.
- **Expected assessment:** Chain B supply-chain silent exfiltration applies. Base score high elevates to critical when custom code can exfiltrate without sandbox/egress detection.
- **Outcome:** PASS: scenario covers supply-chain surfaces, AIBOM/sandbox controls, egress residual risk, and EU/GDPR obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` — Crown jewel assets include API keys, user data, RAG corpus, instruction hierarchy, tool execution environment, fine-tuning data, egress, HITL, embeddings, and AIBOM keys.
  - `synthesis/attack-surface-catalog.md:127-180` — Model hubs, LoRA/adapters, training/fine-tuning, dependencies, skill marketplaces, CI/CD, AIBOM signing keys, and deployment config are supply-chain surfaces.
  - `synthesis/quick-reference.md:33-82` — Chain A, Chain B, Chain C, and Category 14 ISC structural harness risk summaries.
  - `synthesis/risk-matrix.md:45-60` — Critical risk tier includes Chain A, Chain B elevated, Chain C elevated, and ISC with evidence-provenance calibration for ISC.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/quick-reference.md:85-101` — Primary defenses and control types: PI-DEF-2, AGENCY-DEF-1/2, SC-DEF-1/2, MA-DEF-1, ISC-DEF-1; infrastructure vs alignment vs procedural distinction.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.

### SCN-04 — LangGraph incident-response swarm with shared state and MCP tools
- **Deployment:** Multi-agent incident-response system shares message state, receives MCP server outputs, and lets a remediation agent run state-changing cloud tools.
- **Input:** A compromised MCP server returns tool output containing poisoned instructions that enter shared state and influence the remediation agent.
- **Expected assessment:** Chain C applies. Elevated critical risk is triggered when one agent output can enter another agent context/action path. MA-DEF-1 requires explicit context isolation, not default framework behavior.
- **Outcome:** PASS: scenario covers multi-agent, MCP, tool-return propagation, context isolation, privilege ceiling, audit, and regulatory oversight mapping.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — End-user input, retrieved context, tool returns, inter-agent messages, MCP servers, and A2A channels are trust-boundary assumptions; prompts are not authorization boundaries.
  - `synthesis/attack-surface-catalog.md:91-123` — Communication/tool-return surfaces include shared memory, inter-agent messages, MCP responses, tool returns, files, database results, web results, and webhook responses.
  - `synthesis/quick-reference.md:33-82` — Chain A, Chain B, Chain C, and Category 14 ISC structural harness risk summaries.
  - `synthesis/risk-matrix.md:45-60` — Critical risk tier includes Chain A, Chain B elevated, Chain C elevated, and ISC with evidence-provenance calibration for ISC.
  - `synthesis/assessment-template.md:47-120` — Worksheet threat-surface assessment covers PI, agency, multi-agent, supply chain, other categories, and ISC harness surfaces.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.

### SCN-05 — Fine-tuned medical assistant using contractor data and LoRA adapters
- **Deployment:** Healthcare support assistant fine-tuned on proprietary patient-support transcripts and a third-party LoRA adapter; embeddings store personal data.
- **Input:** The contractor provides training data and adapter artifacts without full provenance; the operator wants to treat provider safety alignment as sufficient.
- **Expected assessment:** Categories 3, 4, 7, and defense control type confusion apply. LoRA/fine-tuning and personal-data embeddings require supply-chain, data-governance, behavioral-backdoor-gap, and GDPR treatment.
- **Outcome:** PASS: scenario covers fine-tuning, LoRA/adapters, personal data, embeddings, supply-chain controls, control-type confusion, and GDPR/EU AI Act obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` — Crown jewel assets include API keys, user data, RAG corpus, instruction hierarchy, tool execution environment, fine-tuning data, egress, HITL, embeddings, and AIBOM keys.
  - `synthesis/attack-surface-catalog.md:127-180` — Model hubs, LoRA/adapters, training/fine-tuning, dependencies, skill marketplaces, CI/CD, AIBOM signing keys, and deployment config are supply-chain surfaces.
  - `synthesis/attack-surface-catalog.md:184-210` — Provider surfaces include inference, streaming, batch, API auth, logging, fine-tuning APIs, model export, and cross-tenant shared compute/vector indexes.
  - `synthesis/risk-matrix.md:64-82` — High tier includes direct PI, purchased PI, RAG poisoning, LoRA swap, training data poisoning, agency, quota DoS, and embedding inversion with elevation conditions.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.
  - `synthesis/assumptions.md:106-137` — Default topology assumes cloud-hosted API with RAG, agency, possible multi-agent, sensitive data, metered billing; cloud API differs from self-hosted/fine-tuned supply chain scope.

### SCN-06 — Vision document-intake assistant processing images and structured forms
- **Deployment:** VLM-based intake system processes screenshots, PDFs, and JSON metadata, then generates routing decisions for a back-office queue.
- **Input:** An uploaded image contains hidden instructions and the JSON metadata includes instruction-like strings in fields the model summarizes.
- **Expected assessment:** Category 10 non-text injection and Category 11 output validation apply. Controls must normalize/sanitize multimodal and structured inputs and validate downstream routing outputs.
- **Outcome:** PASS: scenario covers multimodal/structured input, output validation, sanitization, and routing residual actions under the same pass/fail checks.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — End-user input, retrieved context, tool returns, inter-agent messages, MCP servers, and A2A channels are trust-boundary assumptions; prompts are not authorization boundaries.
  - `synthesis/attack-surface-catalog.md:19-27` — Surfaces are organized as input, communication, supply chain, provider API, and execution surfaces.
  - `synthesis/quick-reference.md:10-27` — Fourteen threat categories at a glance, including PI, agency, supply chain, poisoning, leakage, extraction, vector weakness, DoS, multi-agent propagation, non-text injection, output validation, HITL, control confusion, and ISC.
  - `synthesis/risk-matrix.md:86-102` — Medium tier includes system prompt extraction, context DoS, output validation, image/structured injection, cross-tenant leakage, HITL failures, model extraction, and defense control confusion.
  - `synthesis/defense-playbook.md:30-151` — PI defenses include instruction hierarchy hardening, load-time RAG sanitization, input filtering, and output validation.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.

### SCN-07 — Metered enterprise API assistant exposed to quota exhaustion
- **Deployment:** Production customer assistant uses a metered enterprise LLM API with material monthly spend and no per-tenant budget throttle.
- **Input:** An attacker automates high-token requests during business hours, degrading service and consuming paid quota.
- **Expected assessment:** Category 8 DoS/unbounded consumption applies. Standard API DoS is high only when enterprise metered cost/service impact is material; required actions are rate limits, quotas, token budgets, anomaly detection, and SLA/billing controls.
- **Outcome:** PASS: scenario covers provider API surfaces, metered quota elevation, detection/control separation, and operational obligations.
- **Evidence:**
  - `synthesis/assumptions.md:106-137` — Default topology assumes cloud-hosted API with RAG, agency, possible multi-agent, sensitive data, metered billing; cloud API differs from self-hosted/fine-tuned supply chain scope.
  - `synthesis/attack-surface-catalog.md:184-210` — Provider surfaces include inference, streaming, batch, API auth, logging, fine-tuning APIs, model export, and cross-tenant shared compute/vector indexes.
  - `synthesis/quick-reference.md:10-27` — Fourteen threat categories at a glance, including PI, agency, supply chain, poisoning, leakage, extraction, vector weakness, DoS, multi-agent propagation, non-text injection, output validation, HITL, control confusion, and ISC.
  - `synthesis/risk-matrix.md:64-82` — High tier includes direct PI, purchased PI, RAG poisoning, LoRA swap, training data poisoning, agency, quota DoS, and embedding inversion with elevation conditions.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.

### SCN-08 — No-tool chatbot that encodes secrets and authorization in the prompt
- **Deployment:** Single-agent chatbot with no external tools, but system prompt contains business logic, internal policy details, and security decisions.
- **Input:** A user attempts direct prompt injection and prompt extraction; there are no state-changing tools, but the team treats prompt secrecy as the authorization boundary.
- **Expected assessment:** Direct PI and system prompt leakage apply, but Chain A exfiltration does not complete without agency. Defense control type confusion is medium-high because prompt instructions are being treated as infrastructure enforcement.
- **Outcome:** PASS: scenario distinguishes direct PI/leakage from agency-enabled exfiltration and catches alignment-vs-infrastructure confusion.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — End-user input, retrieved context, tool returns, inter-agent messages, MCP servers, and A2A channels are trust-boundary assumptions; prompts are not authorization boundaries.
  - `synthesis/asset-inventory.md:195-212` — Crown jewel assets include API keys, user data, RAG corpus, instruction hierarchy, tool execution environment, fine-tuning data, egress, HITL, embeddings, and AIBOM keys.
  - `synthesis/quick-reference.md:10-27` — Fourteen threat categories at a glance, including PI, agency, supply chain, poisoning, leakage, extraction, vector weakness, DoS, multi-agent propagation, non-text injection, output validation, HITL, control confusion, and ISC.
  - `synthesis/risk-matrix.md:64-82` — High tier includes direct PI, purchased PI, RAG poisoning, LoRA swap, training data poisoning, agency, quota DoS, and embedding inversion with elevation conditions.
  - `synthesis/risk-matrix.md:86-102` — Medium tier includes system prompt extraction, context DoS, output validation, image/structured injection, cross-tenant leakage, HITL failures, model extraction, and defense control confusion.
  - `synthesis/defense-playbook.md:30-151` — PI defenses include instruction hierarchy hardening, load-time RAG sanitization, input filtering, and output validation.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.

### SCN-09 — Multi-tenant RAG platform with shared vector index
- **Deployment:** SaaS RAG platform stores multiple customer document embeddings in one vector database and routes retrieval by tenant metadata.
- **Input:** A tenant attempts mosaic queries and crafted retrieval prompts to infer another tenant's documents from shared embedding/query behavior.
- **Expected assessment:** Category 7 vector/embedding weakness, cross-tenant leakage, RAG context poisoning, and GDPR Article 32 obligations apply. Residual actions require tenant partitioning, retrieval isolation, logging, and privacy-preserving query controls.
- **Outcome:** PASS: scenario covers embedding/vector weaknesses, cross-tenant boundaries, RAG controls, logging, and GDPR security obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` — Crown jewel assets include API keys, user data, RAG corpus, instruction hierarchy, tool execution environment, fine-tuning data, egress, HITL, embeddings, and AIBOM keys.
  - `synthesis/attack-surface-catalog.md:184-210` — Provider surfaces include inference, streaming, batch, API auth, logging, fine-tuning APIs, model export, and cross-tenant shared compute/vector indexes.
  - `synthesis/quick-reference.md:10-27` — Fourteen threat categories at a glance, including PI, agency, supply chain, poisoning, leakage, extraction, vector weakness, DoS, multi-agent propagation, non-text injection, output validation, HITL, control confusion, and ISC.
  - `synthesis/risk-matrix.md:64-82` — High tier includes direct PI, purchased PI, RAG poisoning, LoRA swap, training data poisoning, agency, quota DoS, and embedding inversion with elevation conditions.
  - `synthesis/risk-matrix.md:86-102` — Medium tier includes system prompt extraction, context DoS, output validation, image/structured injection, cross-tenant leakage, HITL failures, model extraction, and defense control confusion.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.

### SCN-10 — Human approval workflow without context provenance
- **Deployment:** Agent can draft and submit high-risk actions only after human approval, but approval dialogs show the action text without source, retrieved document, or rationale provenance.
- **Input:** A retrieved document manipulates the agent to request a fund-transfer or outbound message; a reviewer sees only a plausible action summary.
- **Expected assessment:** HITL exists but is PARTIAL because provenance is missing. It reduces automation risk but does not satisfy AGENCY-DEF-2 for high-risk actions or Category 12 HITL failure concerns.
- **Outcome:** PASS: scenario exercises procedural control scoring, PARTIAL HITL criteria, provenance remediation, and oversight obligations.
- **Evidence:**
  - `synthesis/defense-playbook.md:155-220` — Agency defenses require minimal permission scoping and HITL with context provenance for high-risk actions.
  - `synthesis/assessment-template.md:124-205` — Uniform defense control evaluation uses YES/PARTIAL/NO, ACK/NACK for SC-DEF-4, and notes detection controls do not reduce preventive residual risk by default.
  - `synthesis/quick-reference.md:85-101` — Primary defenses and control types: PI-DEF-2, AGENCY-DEF-1/2, SC-DEF-1/2, MA-DEF-1, ISC-DEF-1; infrastructure vs alignment vs procedural distinction.
  - `synthesis/risk-matrix.md:86-102` — Medium tier includes system prompt extraction, context DoS, output validation, image/structured injection, cross-tenant leakage, HITL failures, model extraction, and defense control confusion.
  - `synthesis/risk-matrix.md:118-148` — Regulatory mapping covers EU AI Act Articles 9/10/13/14/15/17, FTC, and GDPR obligations.
  - `synthesis/quick-reference.md:122-141` — Decision shortcut: RAG, tools, multi-agent/MCP/A2A, ISC harness, and third-party model/skill gates map to required controls.

### SCN-11 — Foreign lab-hosted API used for internal knowledge assistant
- **Foreign distribution mode:** `foreign_lab_hosted_api`
- **Deployment:** Foreign frontier lab hosted API, no local weights, enterprise RAG, no model fine-tuning, no state-changing tools beyond search and summarization.
- **Input:** A team wants to use a foreign lab API because quality is high and assumes nationality alone makes it a supply-chain critical risk.
- **Expected assessment:** Treat the provider API as a deployment boundary and focus on data residency, logging, prompt/response exposure, RAG poisoning, quota, and tool boundaries. Do not inflate supply-chain model-weight risk solely because the lab is foreign; the corpus says official lab infrastructure at release is the lowest-risk point when provenance is verified.
- **Outcome:** PASS: separates foreign-lab identity from actual surfaces; records data-governance and API-boundary controls without overstating official-weight supply-chain risk.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/asset-inventory.md:195-212` — Foreign frontier lab weights verified from the official source are the baseline low-risk starting point; crown-jewel assets remain the organization’s secrets, RAG corpus, tool environment, fine-tuned derivatives, egress, embeddings, and AIBOM/signing keys.
  - `synthesis/quick-reference.md:122-141` — Decision tree requires controls for RAG, tool permissions, multi-agent/MCP/A2A use, attacker-shaped harnesses, and any third-party model, adapter, skill, MCP server, or dependency.
  - `synthesis/risk-matrix.md:118-148` — EU AI Act Articles 9/10/13/14/15/17, FTC data-security expectations, and GDPR Articles 17/25/32 map to risk management, data governance, transparency, oversight, robustness, quality, and security of processing.

### SCN-12 — Official foreign open weights downloaded directly from lab repository
- **Foreign distribution mode:** `foreign_lab_official_open_weights`
- **Deployment:** Foreign lab official open weights downloaded from the originating lab repository with cryptographic signature verification; inference-only evaluation on an isolated benchmark box.
- **Input:** Security review decides whether direct official weights from a foreign lab should be rejected before any deployment integration exists.
- **Expected assessment:** Official signed foreign weights are the low supply-chain baseline, not a critical finding by themselves. Remaining controls are provenance capture, AIBOM entry, no custom hooks, isolated evaluation, and reassessment when weights are converted, fine-tuned, or connected to RAG/tools.
- **Outcome:** PASS: covers official open-weight acquisition from the lab and correctly keeps risk low until modification, fine-tuning, custom code, or deployment surfaces are added.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/asset-inventory.md:195-212` — Foreign frontier lab weights verified from the official source are the baseline low-risk starting point; crown-jewel assets remain the organization’s secrets, RAG corpus, tool environment, fine-tuned derivatives, egress, embeddings, and AIBOM/signing keys.
  - `synthesis/attack-surface-catalog.md:127-140` — Official lab release plus signature verification is lowest risk; model hubs, verified badges, artifact URLs, APIs, adapters, and registry replay remain supply-chain surfaces.
  - `synthesis/risk-matrix.md:118-148` — EU AI Act Articles 9/10/13/14/15/17, FTC data-security expectations, and GDPR Articles 17/25/32 map to risk management, data governance, transparency, oversight, robustness, quality, and security of processing.

### SCN-13 — Official foreign open weights self-hosted behind internal RAG and tools
- **Foreign distribution mode:** `foreign_lab_official_weights_self_hosted`
- **Deployment:** Foreign lab official verified open weights are self-hosted in the organization GPU cluster; the model is connected to internal RAG, file read tools, and outbound HTTP disabled by default.
- **Input:** After a clean provenance check, engineering wires the model into RAG and tools and asks what changed in the risk model.
- **Expected assessment:** The base-weight supply-chain posture remains comparatively low, but self-hosting creates container, framework, RAG, tool, secret, embedding, and egress surfaces. Chain A and standard self-hosted operational controls now matter more than foreign origin.
- **Outcome:** PASS: covers self-hosted official foreign weights and shifts attention from nationality to runtime, RAG, tool, secret, and egress controls.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/asset-inventory.md:195-212` — Foreign frontier lab weights verified from the official source are the baseline low-risk starting point; crown-jewel assets remain the organization’s secrets, RAG corpus, tool environment, fine-tuned derivatives, egress, embeddings, and AIBOM/signing keys.
  - `synthesis/attack-surface-catalog.md:127-140` — Official lab release plus signature verification is lowest risk; model hubs, verified badges, artifact URLs, APIs, adapters, and registry replay remain supply-chain surfaces.
  - `synthesis/attack-surface-catalog.md:142-161` — Fine-tuning data, adapter training, dependencies, tokenizers, inference frameworks, and container images become material surfaces once official weights are modified, converted, or self-hosted.
  - `synthesis/defense-playbook.md:155-220` — Agency controls remain required when foreign models receive tools: minimal permission scoping and HITL with context provenance for high-risk actions.
  - `synthesis/risk-matrix.md:118-148` — EU AI Act Articles 9/10/13/14/15/17, FTC data-security expectations, and GDPR Articles 17/25/32 map to risk management, data governance, transparency, oversight, robustness, quality, and security of processing.

### SCN-14 — Quantized foreign open weights redistributed as GGUF by a community mirror
- **Foreign distribution mode:** `foreign_open_weights_quantized_distribution`
- **Deployment:** Foreign open weights are not downloaded from the lab; a community mirror distributes a quantized GGUF build and suggested llama.cpp container for desktop/offline use.
- **Input:** The team treats the mirror as equivalent to the official lab artifact because the model name matches and performance benchmarks look normal.
- **Expected assessment:** The verified-official low-risk assumption no longer applies. Conversion, mirror provenance, artifact URL, tokenizer/config drift, runtime/container dependencies, and hash/signature verification become the assessment center.
- **Outcome:** PASS: covers redistributed/quantized open weights and removes the official-release assumption once the artifact is converted or mirrored.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/attack-surface-catalog.md:127-140` — Official lab release plus signature verification is lowest risk; model hubs, verified badges, artifact URLs, APIs, adapters, and registry replay remain supply-chain surfaces.
  - `synthesis/attack-surface-catalog.md:142-161` — Fine-tuning data, adapter training, dependencies, tokenizers, inference frameworks, and container images become material surfaces once official weights are modified, converted, or self-hosted.
  - `synthesis/risk-matrix.md:45-76` — Supply chain custom inference can elevate to critical without sandbox/egress detection; LoRA swaps, training data poisoning, quota DoS, and embedding inversion have explicit elevation conditions.

### SCN-15 — Unofficial fine-tune of foreign open weights on proprietary support data
- **Foreign distribution mode:** `foreign_open_weights_unofficial_finetune`
- **Deployment:** Foreign official open weights are used as a base, then an external vendor produces an unofficial fine-tune using proprietary support transcripts and ships a new model artifact.
- **Input:** The vendor argues the base model was official, so the fine-tuned artifact inherits the original low supply-chain risk.
- **Expected assessment:** The official-base assumption does not transfer to the fine-tune. Fine-tuning creates new data exposure, poisoning, distillation, model-artifact, vendor, and behavioral-backdoor surfaces; SC-DEF-4 must be acknowledged because artifact identity does not prove behavior.
- **Outcome:** PASS: covers unofficial fine-tuning of foreign open weights and correctly reclassifies the risk around the new artifact, vendor pipeline, and proprietary data.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/asset-inventory.md:195-212` — Foreign frontier lab weights verified from the official source are the baseline low-risk starting point; crown-jewel assets remain the organization’s secrets, RAG corpus, tool environment, fine-tuned derivatives, egress, embeddings, and AIBOM/signing keys.
  - `synthesis/attack-surface-catalog.md:142-161` — Fine-tuning data, adapter training, dependencies, tokenizers, inference frameworks, and container images become material surfaces once official weights are modified, converted, or self-hosted.
  - `synthesis/risk-matrix.md:45-76` — Supply chain custom inference can elevate to critical without sandbox/egress detection; LoRA swaps, training data poisoning, quota DoS, and embedding inversion have explicit elevation conditions.
  - `synthesis/risk-matrix.md:118-148` — EU AI Act Articles 9/10/13/14/15/17, FTC data-security expectations, and GDPR Articles 17/25/32 map to risk management, data governance, transparency, oversight, robustness, quality, and security of processing.

### SCN-16 — Foreign open-weight base with third-party LoRA adapter in production agent
- **Foreign distribution mode:** `foreign_open_weights_lora_adapter`
- **Deployment:** Foreign official open-weight base is loaded with a third-party LoRA adapter from an adapter registry and deployed in a tool-using production agent.
- **Input:** The team verifies the base model hash but does not verify the adapter publisher, adapter training data, or behavioral impact before enabling tools.
- **Expected assessment:** The adapter is the dominant supply-chain surface. Base-weight provenance is necessary but insufficient; LoRA swap/alignment-removal risk, AIBOM, adapter provenance, sandboxing, behavior probes, and tool permission controls are required.
- **Outcome:** PASS: covers adapter-based deployment and makes the LoRA artifact, not the verified foreign base, the main risk driver once production tools are enabled.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — Verified official foreign lab weights carry lowest supply-chain risk when downloaded directly from the originating lab official repository with cryptographic signature verification; unofficial fine-tunes, modified weights, and proprietary fine-tuning data open new surfaces.
  - `synthesis/attack-surface-catalog.md:127-140` — Official lab release plus signature verification is lowest risk; model hubs, verified badges, artifact URLs, APIs, adapters, and registry replay remain supply-chain surfaces.
  - `synthesis/attack-surface-catalog.md:142-161` — Fine-tuning data, adapter training, dependencies, tokenizers, inference frameworks, and container images become material surfaces once official weights are modified, converted, or self-hosted.
  - `synthesis/risk-matrix.md:45-76` — Supply chain custom inference can elevate to critical without sandbox/egress detection; LoRA swaps, training data poisoning, quota DoS, and embedding inversion have explicit elevation conditions.
  - `synthesis/defense-playbook.md:155-220` — Agency controls remain required when foreign models receive tools: minimal permission scoping and HITL with context provenance for high-risk actions.
  - `synthesis/risk-matrix.md:118-148` — EU AI Act Articles 9/10/13/14/15/17, FTC data-security expectations, and GDPR Articles 17/25/32 map to risk management, data governance, transparency, oversight, robustness, quality, and security of processing.

## Rerun history
- **RED-0** `python scripts/test_scenario_suite.py` → **FAIL** — Scenario suite file was missing; tests failed before any scenario could meet the quality bar.
- **RUN-1** `python scripts/test_scenario_suite.py` → **PASS** — All ten scenarios satisfied uniform pass/fail criteria after the suite was created.
- **RED-1** `python scripts/test_scenario_suite.py` → **FAIL** — Foreign LLM scenario coverage tests failed because the suite still had 10 scenarios and no foreign_model_posture distribution series.
- **RUN-2** `python scripts/test_scenario_suite.py` → **PASS** — Foreign model scenario series added and all sixteen scenarios satisfied the uniform pass/fail criteria on affected rerun.

## Final complete rerun
`python scripts/test_scenario_suite.py` → **PASS** (16 passed, 0 failed).

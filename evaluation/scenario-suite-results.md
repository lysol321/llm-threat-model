# Scenario Evaluation Results

**Method:** uniform_pass_fail
**Same conditions:** Every scenario was run as a tabletop assessment against the same v1.9 corpus, same nine pass/fail criteria, same evidence standard, and no external incident narratives unless backed by primary/corroborated source notes already in the corpus.
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
| SCN-02 | Coding agent accepts attacker-shaped tests and incomplete placeholder data | PASS | synthesis/attack-surface-catalog.md:69-87, synthesis/attack-surface-catalog.md:80-83, synthesis/quick-reference.md:33-82, synthesis/quick-reference.md:139-157 (+3 more) |
| SCN-03 | Self-hosted HuggingFace model with custom inference and open egress | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-180, synthesis/quick-reference.md:33-82, synthesis/risk-matrix.md:45-60 (+3 more) |
| SCN-04 | LangGraph incident-response swarm with shared state and MCP tools | PASS | synthesis/assumptions.md:144-171, synthesis/attack-surface-catalog.md:91-123, synthesis/quick-reference.md:33-82, synthesis/risk-matrix.md:45-60 (+3 more) |
| SCN-05 | Fine-tuned medical assistant using contractor data and LoRA adapters | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-180, synthesis/attack-surface-catalog.md:184-210, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-06 | Vision document-intake assistant processing images and structured forms | PASS | synthesis/assumptions.md:144-171, synthesis/attack-surface-catalog.md:19-27, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:86-102 (+2 more) |
| SCN-07 | Metered enterprise API assistant exposed to quota exhaustion | PASS | synthesis/assumptions.md:106-137, synthesis/attack-surface-catalog.md:184-210, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+2 more) |
| SCN-08 | No-tool chatbot that encodes secrets and authorization in the prompt | PASS | synthesis/assumptions.md:144-171, synthesis/asset-inventory.md:195-212, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-09 | Multi-tenant RAG platform with shared vector index | PASS | synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:184-210, synthesis/quick-reference.md:10-27, synthesis/risk-matrix.md:64-82 (+3 more) |
| SCN-10 | Human approval workflow without context provenance | PASS | synthesis/defense-playbook.md:155-220, synthesis/assessment-template.md:124-205, synthesis/quick-reference.md:103-118, synthesis/risk-matrix.md:86-102 (+2 more) |
| SCN-11 | Foreign lab-hosted API used for internal knowledge assistant | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/quick-reference.md:139-157, synthesis/risk-matrix.md:118-148 |
| SCN-12 | Official foreign open weights downloaded directly from lab repository | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-140, synthesis/risk-matrix.md:118-148 |
| SCN-13 | Official foreign open weights self-hosted behind internal RAG and tools | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161 (+2 more) |
| SCN-14 | Quantized foreign open weights redistributed as GGUF by a community mirror | PASS | synthesis/assumptions.md:90-98, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 |
| SCN-15 | Unofficial fine-tune of foreign open weights on proprietary support data | PASS | synthesis/assumptions.md:90-98, synthesis/asset-inventory.md:195-212, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 (+1 more) |
| SCN-16 | Foreign open-weight base with third-party LoRA adapter in production agent | PASS | synthesis/assumptions.md:90-98, synthesis/attack-surface-catalog.md:127-140, synthesis/attack-surface-catalog.md:142-161, synthesis/risk-matrix.md:45-76 (+2 more) |
| SCN-17-MEMORY | Cross-session durable-memory poisoning | PASS | synthesis/attack-surface-catalog.md:375-375, synthesis/threat-taxonomy.md:437-437, synthesis/risk-matrix.md:228-228, synthesis/defense-playbook.md:841-841 |
| SCN-18-SKILL-RETRIEVAL | Semantic skill-retrieval manipulation | PASS | synthesis/attack-surface-catalog.md:376-376, synthesis/threat-taxonomy.md:418-418, synthesis/risk-matrix.md:229-229, synthesis/defense-playbook.md:856-856 |
| SCN-19-SKILL-UPDATE | Post-install skill update rug pull | PASS | synthesis/attack-surface-catalog.md:377-377, synthesis/threat-taxonomy.md:418-418, synthesis/risk-matrix.md:229-229, synthesis/defense-playbook.md:856-856 |
| SCN-20-IDENTITY | Inter-agent identity and delegation spoofing | PASS | synthesis/attack-surface-catalog.md:378-378, synthesis/threat-taxonomy.md:437-437, synthesis/risk-matrix.md:230-230, synthesis/defense-playbook.md:869-869 |
| SCN-21-COMPUTER-USE | Computer-use visual-state disagreement | PASS | synthesis/attack-surface-catalog.md:379-379, synthesis/threat-taxonomy.md:448-448, synthesis/risk-matrix.md:231-231, synthesis/defense-playbook.md:882-882 |
| SCN-22-SESSION | Incremental session contamination and goal hijacking | PASS | synthesis/attack-surface-catalog.md:375-375, synthesis/threat-taxonomy.md:454-454, synthesis/risk-matrix.md:232-232, synthesis/defense-playbook.md:907-907 |
| SCN-23-RELAY | BYOK response-path relay tampering | PASS | synthesis/attack-surface-catalog.md:380-380, synthesis/threat-taxonomy.md:464-464, synthesis/risk-matrix.md:233-233, synthesis/defense-playbook.md:892-892 |
| SCN-24-REPRESENTATION | Representation-confusion at binary-to-text boundary | PASS | synthesis/attack-surface-catalog.md:381-381, synthesis/threat-taxonomy.md:472-472, synthesis/risk-matrix.md:234-234, synthesis/defense-playbook.md:916-916 |
| SCN-25-DISCLOSURE | Capability disclosure enabling follow-on attack | PASS | synthesis/attack-surface-catalog.md:378-378, synthesis/threat-taxonomy.md:431-431, synthesis/risk-matrix.md:230-230, synthesis/defense-playbook.md:869-869 |

## Per-scenario evidence and outcome
### SCN-01 — Customer-support RAG copilot with email and CRM tools
- **Deployment:** Cloud API assistant, enterprise RAG corpus, customer-email ingestion, CRM read/write, outbound email, no guaranteed provenance in approval UI.
- **Input:** Attacker sends a crafted customer email that is indexed/retrieved by support RAG; the copilot can summarize the account and send follow-up emails.
- **Expected assessment:** Chain A applies. Indirect PI plus agency creates critical exfiltration risk unless RAG context labeling, infrastructure privilege separation, minimal tool allowlist, and provenance-aware HITL are implemented.
- **Outcome:** PASS: major framework paths identify the deployment, assets, RAG/email surfaces, Chain A risk, controls, residual actions, and regulatory notes.
- **Evidence:**
  - `synthesis/assumptions.md:106-137` — ### C1: Default Deployment Topology **Assumption:** The framework's default (unmodified) risk scores assume a **cloud-hosted API deployment** (OpenAI, Anthropic, or Google API) with: - RAG pipeline present - Tool-using agency present - M...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:19-27` — ## Surface Taxonomy  Surfaces are organized into five categories:  1. **Input Surfaces** — Points where data enters the LLM system (user input, retrieved content, tool outputs) 2. **Communication Surfaces** — Points where data moves betw...
  - `synthesis/quick-reference.md:33-82` — ## 3 Attack Chains + 1 Critical Structural Harness Risk  ### Chain A: Indirect PI → Excessive Agency → Data Exfiltration ``` [Indirect PI via RAG/documents]          ↓ [Excessive Agency: tool permissions + no HITL]          ↓ [Tool call ...
  - `synthesis/quick-reference.md:139-157` —  ``` Is prompt injection surface present?   YES → Is RAG/retrieval used?     YES → PI-DEF-2 (load-time sanitization + infrastructure privilege separation) REQUIRED   YES → Does system have tool permissions?     YES → AGENCY-DEF-1 (allowl...
  - `synthesis/risk-matrix.md:45-60` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...
  - `synthesis/defense-playbook.md:30-151` — ## Defense Layer 1: Prompt Injection Defenses  ### PI-DEF-1: Instruction Hierarchy Hardening [DEV] — **PRIMARY** **Effectiveness:** MEDIUM (reduces but does not eliminate PI exploitability) **Latency cost:** None **Constraint notes:** Re...
  - `synthesis/defense-playbook.md:155-220` — ## Defense Layer 2: Excessive Agency Defenses  ### AGENCY-DEF-1: Minimal Permission Scoping [DEV] — **PRIMARY** **Effectiveness:** CRITICAL (if no tool access, PI impact is noise) **Latency cost:** None **Constraint notes:** Requires upf...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-02 — Coding agent accepts attacker-shaped tests and incomplete placeholder data
- **Deployment:** Autonomous code-repair agent executes external task specs, unit tests, schemas, and placeholder fixtures before writing patches.
- **Input:** A bug bounty submitter provides a task, validator, and fixture with gaps that only pass if the model fabricates unsafe completion content.
- **Expected assessment:** Category 14 ISC applies because the attacker meaningfully shapes task/validator/data harness material. ISC-DEF-1 semantic harness validation is required; format-only validation is not enough.
- **Outcome:** PASS: scenario exercises ISC gate, source-backed risk calibration, semantic validator controls, and avoids using press/community stories as risk evidence.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:69-87` —  /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Task definition input**  /  A professional task description provided or shaped by an att...
  - `synthesis/attack-surface-catalog.md:80-83` — **Key distinction from indirect PI:** Indirect PI embeds adversarial instructions in content the model retrieves. ISC embeds a benign task in a structure that *forces the model* to generate harmful content to satisfy a validator. The att...
  - `synthesis/quick-reference.md:33-82` — ## 3 Attack Chains + 1 Critical Structural Harness Risk  ### Chain A: Indirect PI → Excessive Agency → Data Exfiltration ``` [Indirect PI via RAG/documents]          ↓ [Excessive Agency: tool permissions + no HITL]          ↓ [Tool call ...
  - `synthesis/quick-reference.md:139-157` —  ``` Is prompt injection surface present?   YES → Is RAG/retrieval used?     YES → PI-DEF-2 (load-time sanitization + infrastructure privilege separation) REQUIRED   YES → Does system have tool permissions?     YES → AGENCY-DEF-1 (allowl...
  - `synthesis/assessment-template.md:47-120` —  Describe what is OUT OF SCOPE: _____________________________________________ _____________________________________________  ---  ## Section 2: Threat Surface Assessment  **Purpose:** Identify which threat categories apply to your system...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/risk-matrix.md:45-60` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...

### SCN-03 — Self-hosted HuggingFace model with custom inference and open egress
- **Deployment:** Operator downloads a model-hub repository with custom Python inference code into a GPU container that can reach the public internet.
- **Input:** The repository has a plausible publisher profile but no external trust anchor, no AIBOM freshness metadata, and no egress block before first inference.
- **Expected assessment:** Chain B supply-chain silent exfiltration applies. Base score high elevates to critical when custom code can exfiltrate without sandbox/egress detection.
- **Outcome:** PASS: scenario covers supply-chain surfaces, AIBOM/sandbox controls, egress residual risk, and EU/GDPR obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:127-180` — ## 3. Supply Chain Surfaces  **Risk lifecycle for model supply chain surfaces:** Frontier labs at official release are the safest point in a model's lifecycle. Download from the originating lab's official repository + cryptographic signa...
  - `synthesis/quick-reference.md:33-82` — ## 3 Attack Chains + 1 Critical Structural Harness Risk  ### Chain A: Indirect PI → Excessive Agency → Data Exfiltration ``` [Indirect PI via RAG/documents]          ↓ [Excessive Agency: tool permissions + no HITL]          ↓ [Tool call ...
  - `synthesis/risk-matrix.md:45-60` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/quick-reference.md:103-118` —  /  Defense  /  Threat Addressed  /  Control Type  /  Effectiveness  /   / --------- / ----------------- / -------------- / --------------- /   /  **PI-DEF-1:** Instruction hierarchy hardening  /  Prompt Injection  /  Alignment  /  MEDIUM  /   /  **PI-DEF-2:** RAG cont...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-04 — LangGraph incident-response swarm with shared state and MCP tools
- **Deployment:** Multi-agent incident-response system shares message state, receives MCP server outputs, and lets a remediation agent run state-changing cloud tools.
- **Input:** A compromised MCP server returns tool output containing poisoned instructions that enter shared state and influence the remediation agent.
- **Expected assessment:** Chain C applies. Elevated critical risk is triggered when one agent output can enter another agent context/action path. MA-DEF-1 requires explicit context isolation, not default framework behavior.
- **Outcome:** PASS: scenario covers multi-agent, MCP, tool-return propagation, context isolation, privilege ceiling, audit, and regulatory oversight mapping.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — D1: End-User Input Is Untrusted **Assumption:** All user-provided text input is untrusted by default. The framework does not assume user inputs are benign, non-adversarial, or well-formed. **Implication:** Every user input field is a pot...
  - `synthesis/attack-surface-catalog.md:91-123` — ## 2. Communication Surfaces  ### 2.1 Inter-Agent Communication   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Shared memory / share...
  - `synthesis/quick-reference.md:33-82` — ## 3 Attack Chains + 1 Critical Structural Harness Risk  ### Chain A: Indirect PI → Excessive Agency → Data Exfiltration ``` [Indirect PI via RAG/documents]          ↓ [Excessive Agency: tool permissions + no HITL]          ↓ [Tool call ...
  - `synthesis/risk-matrix.md:45-60` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...
  - `synthesis/assessment-template.md:47-120` —  Describe what is OUT OF SCOPE: _____________________________________________ _____________________________________________  ---  ## Section 2: Threat Surface Assessment  **Purpose:** Identify which threat categories apply to your system...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-05 — Fine-tuned medical assistant using contractor data and LoRA adapters
- **Deployment:** Healthcare support assistant fine-tuned on proprietary patient-support transcripts and a third-party LoRA adapter; embeddings store personal data.
- **Input:** The contractor provides training data and adapter artifacts without full provenance; the operator wants to treat provider safety alignment as sufficient.
- **Expected assessment:** Categories 3, 4, 7, and defense control type confusion apply. LoRA/fine-tuning and personal-data embeddings require supply-chain, data-governance, behavioral-backdoor-gap, and GDPR treatment.
- **Outcome:** PASS: scenario covers fine-tuning, LoRA/adapters, personal data, embeddings, supply-chain controls, control-type confusion, and GDPR/EU AI Act obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:127-180` — ## 3. Supply Chain Surfaces  **Risk lifecycle for model supply chain surfaces:** Frontier labs at official release are the safest point in a model's lifecycle. Download from the originating lab's official repository + cryptographic signa...
  - `synthesis/attack-surface-catalog.md:184-210` — ## 4. Provider API Surfaces  ### 4.1 Inference API Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Inference endpoint (HTTPS...
  - `synthesis/risk-matrix.md:64-82` — ---  ### Tier 2: High Risks (Risk Score 13–18)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Direct Prompt Injection**  /  5  /  3  /  **15**  /  ...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...
  - `synthesis/assumptions.md:106-137` — ### C1: Default Deployment Topology **Assumption:** The framework's default (unmodified) risk scores assume a **cloud-hosted API deployment** (OpenAI, Anthropic, or Google API) with: - RAG pipeline present - Tool-using agency present - M...

### SCN-06 — Vision document-intake assistant processing images and structured forms
- **Deployment:** VLM-based intake system processes screenshots, PDFs, and JSON metadata, then generates routing decisions for a back-office queue.
- **Input:** An uploaded image contains hidden instructions and the JSON metadata includes instruction-like strings in fields the model summarizes.
- **Expected assessment:** Category 10 non-text injection and Category 11 output validation apply. Controls must normalize/sanitize multimodal and structured inputs and validate downstream routing outputs.
- **Outcome:** PASS: scenario covers multimodal/structured input, output validation, sanitization, and routing residual actions under the same pass/fail checks.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — D1: End-User Input Is Untrusted **Assumption:** All user-provided text input is untrusted by default. The framework does not assume user inputs are benign, non-adversarial, or well-formed. **Implication:** Every user input field is a pot...
  - `synthesis/attack-surface-catalog.md:19-27` — ## Surface Taxonomy  Surfaces are organized into five categories:  1. **Input Surfaces** — Points where data enters the LLM system (user input, retrieved content, tool outputs) 2. **Communication Surfaces** — Points where data moves betw...
  - `synthesis/quick-reference.md:10-27` —  /  #  /  Threat  /  One-Line Definition  /  Priority  /   / --- / -------- / --------------------- / ---------- /   /  1  /  **Prompt Injection**  /  Manipulating LLM behavior through crafted inputs that override system instructions  /  CRITICAL  /   /  2  /  **Excessiv...
  - `synthesis/risk-matrix.md:86-102` — ---  ### Tier 3: Medium Risks (Risk Score 7–12)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **System Prompt Extraction**  /  3  /  3  /  **9**  / ...
  - `synthesis/defense-playbook.md:30-151` — ## Defense Layer 1: Prompt Injection Defenses  ### PI-DEF-1: Instruction Hierarchy Hardening [DEV] — **PRIMARY** **Effectiveness:** MEDIUM (reduces but does not eliminate PI exploitability) **Latency cost:** None **Constraint notes:** Re...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...

### SCN-07 — Metered enterprise API assistant exposed to quota exhaustion
- **Deployment:** Production customer assistant uses a metered enterprise LLM API with material monthly spend and no per-tenant budget throttle.
- **Input:** An attacker automates high-token requests during business hours, degrading service and consuming paid quota.
- **Expected assessment:** Category 8 DoS/unbounded consumption applies. Standard API DoS is high only when enterprise metered cost/service impact is material; required actions are rate limits, quotas, token budgets, anomaly detection, and SLA/billing controls.
- **Outcome:** PASS: scenario covers provider API surfaces, metered quota elevation, detection/control separation, and operational obligations.
- **Evidence:**
  - `synthesis/assumptions.md:106-137` — ### C1: Default Deployment Topology **Assumption:** The framework's default (unmodified) risk scores assume a **cloud-hosted API deployment** (OpenAI, Anthropic, or Google API) with: - RAG pipeline present - Tool-using agency present - M...
  - `synthesis/attack-surface-catalog.md:184-210` — ## 4. Provider API Surfaces  ### 4.1 Inference API Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Inference endpoint (HTTPS...
  - `synthesis/quick-reference.md:10-27` —  /  #  /  Threat  /  One-Line Definition  /  Priority  /   / --- / -------- / --------------------- / ---------- /   /  1  /  **Prompt Injection**  /  Manipulating LLM behavior through crafted inputs that override system instructions  /  CRITICAL  /   /  2  /  **Excessiv...
  - `synthesis/risk-matrix.md:64-82` — ---  ### Tier 2: High Risks (Risk Score 13–18)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Direct Prompt Injection**  /  5  /  3  /  **15**  /  ...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-08 — No-tool chatbot that encodes secrets and authorization in the prompt
- **Deployment:** Single-agent chatbot with no external tools, but system prompt contains business logic, internal policy details, and security decisions.
- **Input:** A user attempts direct prompt injection and prompt extraction; there are no state-changing tools, but the team treats prompt secrecy as the authorization boundary.
- **Expected assessment:** Direct PI and system prompt leakage apply, but Chain A exfiltration does not complete without agency. Defense control type confusion is medium-high because prompt instructions are being treated as infrastructure enforcement.
- **Outcome:** PASS: scenario distinguishes direct PI/leakage from agency-enabled exfiltration and catches alignment-vs-infrastructure confusion.
- **Evidence:**
  - `synthesis/assumptions.md:144-171` — D1: End-User Input Is Untrusted **Assumption:** All user-provided text input is untrusted by default. The framework does not assume user inputs are benign, non-adversarial, or well-formed. **Implication:** Every user input field is a pot...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/quick-reference.md:10-27` —  /  #  /  Threat  /  One-Line Definition  /  Priority  /   / --- / -------- / --------------------- / ---------- /   /  1  /  **Prompt Injection**  /  Manipulating LLM behavior through crafted inputs that override system instructions  /  CRITICAL  /   /  2  /  **Excessiv...
  - `synthesis/risk-matrix.md:64-82` — ---  ### Tier 2: High Risks (Risk Score 13–18)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Direct Prompt Injection**  /  5  /  3  /  **15**  /  ...
  - `synthesis/risk-matrix.md:86-102` — ---  ### Tier 3: Medium Risks (Risk Score 7–12)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **System Prompt Extraction**  /  3  /  3  /  **9**  / ...
  - `synthesis/defense-playbook.md:30-151` — ## Defense Layer 1: Prompt Injection Defenses  ### PI-DEF-1: Instruction Hierarchy Hardening [DEV] — **PRIMARY** **Effectiveness:** MEDIUM (reduces but does not eliminate PI exploitability) **Latency cost:** None **Constraint notes:** Re...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...

### SCN-09 — Multi-tenant RAG platform with shared vector index
- **Deployment:** SaaS RAG platform stores multiple customer document embeddings in one vector database and routes retrieval by tenant metadata.
- **Input:** A tenant attempts mosaic queries and crafted retrieval prompts to infer another tenant's documents from shared embedding/query behavior.
- **Expected assessment:** Category 7 vector/embedding weakness, cross-tenant leakage, RAG context poisoning, and GDPR Article 32 obligations apply. Residual actions require tenant partitioning, retrieval isolation, logging, and privacy-preserving query controls.
- **Outcome:** PASS: scenario covers embedding/vector weaknesses, cross-tenant boundaries, RAG controls, logging, and GDPR security obligations.
- **Evidence:**
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:184-210` — ## 4. Provider API Surfaces  ### 4.1 Inference API Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Inference endpoint (HTTPS...
  - `synthesis/quick-reference.md:10-27` —  /  #  /  Threat  /  One-Line Definition  /  Priority  /   / --- / -------- / --------------------- / ---------- /   /  1  /  **Prompt Injection**  /  Manipulating LLM behavior through crafted inputs that override system instructions  /  CRITICAL  /   /  2  /  **Excessiv...
  - `synthesis/risk-matrix.md:64-82` — ---  ### Tier 2: High Risks (Risk Score 13–18)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Direct Prompt Injection**  /  5  /  3  /  **15**  /  ...
  - `synthesis/risk-matrix.md:86-102` — ---  ### Tier 3: Medium Risks (Risk Score 7–12)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **System Prompt Extraction**  /  3  /  3  /  **9**  / ...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-10 — Human approval workflow without context provenance
- **Deployment:** Agent can draft and submit high-risk actions only after human approval, but approval dialogs show the action text without source, retrieved document, or rationale provenance.
- **Input:** A retrieved document manipulates the agent to request a fund-transfer or outbound message; a reviewer sees only a plausible action summary.
- **Expected assessment:** HITL exists but is PARTIAL because provenance is missing. It reduces automation risk but does not satisfy AGENCY-DEF-2 for high-risk actions or Category 12 HITL failure concerns.
- **Outcome:** PASS: scenario exercises procedural control scoring, PARTIAL HITL criteria, provenance remediation, and oversight obligations.
- **Evidence:**
  - `synthesis/defense-playbook.md:155-220` — ## Defense Layer 2: Excessive Agency Defenses  ### AGENCY-DEF-1: Minimal Permission Scoping [DEV] — **PRIMARY** **Effectiveness:** CRITICAL (if no tool access, PI impact is noise) **Latency cost:** None **Constraint notes:** Requires upf...
  - `synthesis/assessment-template.md:124-205` —  /  Attacker can control or meaningfully shape task definitions, uploaded files, external datasets, tool outputs, marketplace skills, customer integrations, or workflow bundles entering that harness  /  [ ] YES  [ ] NO  /   /   /  Attacker can sup...
  - `synthesis/quick-reference.md:103-118` —  /  Defense  /  Threat Addressed  /  Control Type  /  Effectiveness  /   / --------- / ----------------- / -------------- / --------------- /   /  **PI-DEF-1:** Instruction hierarchy hardening  /  Prompt Injection  /  Alignment  /  MEDIUM  /   /  **PI-DEF-2:** RAG cont...
  - `synthesis/risk-matrix.md:86-102` — ---  ### Tier 3: Medium Risks (Risk Score 7–12)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **System Prompt Extraction**  /  3  /  3  /  **9**  / ...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...
  - `synthesis/quick-reference.md:139-157` —  ``` Is prompt injection surface present?   YES → Is RAG/retrieval used?     YES → PI-DEF-2 (load-time sanitization + infrastructure privilege separation) REQUIRED   YES → Does system have tool permissions?     YES → AGENCY-DEF-1 (allowl...

### SCN-11 — Foreign lab-hosted API used for internal knowledge assistant
- **Deployment:** Foreign frontier lab hosted API, no local weights, enterprise RAG, no model fine-tuning, no state-changing tools beyond search and summarization.
- **Input:** A team wants to use a foreign lab API because quality is high and assumes nationality alone makes it a supply-chain critical risk.
- **Expected assessment:** Treat the provider API as a deployment boundary and focus on data residency, logging, prompt/response exposure, RAG poisoning, quota, and tool boundaries. Do not inflate supply-chain model-weight risk solely because the lab is foreign; the corpus says official lab infrastructure at release is the lowest-risk point when provenance is verified.
- **Outcome:** PASS: separates foreign-lab identity from actual surfaces; records data-governance and API-boundary controls without overstating official-weight supply-chain risk.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/quick-reference.md:139-157` —  ``` Is prompt injection surface present?   YES → Is RAG/retrieval used?     YES → PI-DEF-2 (load-time sanitization + infrastructure privilege separation) REQUIRED   YES → Does system have tool permissions?     YES → AGENCY-DEF-1 (allowl...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-12 — Official foreign open weights downloaded directly from lab repository
- **Deployment:** Foreign lab official open weights downloaded from the originating lab repository with cryptographic signature verification; inference-only evaluation on an isolated benchmark box.
- **Input:** Security review decides whether direct official weights from a foreign lab should be rejected before any deployment integration exists.
- **Expected assessment:** Official signed foreign weights are the low supply-chain baseline, not a critical finding by themselves. Remaining controls are provenance capture, AIBOM entry, no custom hooks, isolated evaluation, and reassessment when weights are converted, fine-tuned, or connected to RAG/tools.
- **Outcome:** PASS: covers official open-weight acquisition from the lab and correctly keeps risk low until modification, fine-tuning, custom code, or deployment surfaces are added.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:127-140` —  /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **HuggingFace model repository**  /  Model weights, repository metadata, custom code  /  Mal...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-13 — Official foreign open weights self-hosted behind internal RAG and tools
- **Deployment:** Foreign lab official verified open weights are self-hosted in the organization GPU cluster; the model is connected to internal RAG, file read tools, and outbound HTTP disabled by default.
- **Input:** After a clean provenance check, engineering wires the model into RAG and tools and asks what changed in the risk model.
- **Expected assessment:** The base-weight supply-chain posture remains comparatively low, but self-hosting creates container, framework, RAG, tool, secret, embedding, and egress surfaces. Chain A and standard self-hosted operational controls now matter more than foreign origin.
- **Outcome:** PASS: covers self-hosted official foreign weights and shifts attention from nationality to runtime, RAG, tool, secret, and egress controls.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:127-140` —  /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **HuggingFace model repository**  /  Model weights, repository metadata, custom code  /  Mal...
  - `synthesis/attack-surface-catalog.md:142-161` — ### 3.2 Training and Fine-Tuning Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Training data ingestion**  /  Data pipeline f...
  - `synthesis/defense-playbook.md:155-220` — ## Defense Layer 2: Excessive Agency Defenses  ### AGENCY-DEF-1: Minimal Permission Scoping [DEV] — **PRIMARY** **Effectiveness:** CRITICAL (if no tool access, PI impact is noise) **Latency cost:** None **Constraint notes:** Requires upf...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-14 — Quantized foreign open weights redistributed as GGUF by a community mirror
- **Deployment:** Foreign open weights are not downloaded from the lab; a community mirror distributes a quantized GGUF build and suggested llama.cpp container for desktop/offline use.
- **Input:** The team treats the mirror as equivalent to the official lab artifact because the model name matches and performance benchmarks look normal.
- **Expected assessment:** The verified-official low-risk assumption no longer applies. Conversion, mirror provenance, artifact URL, tokenizer/config drift, runtime/container dependencies, and hash/signature verification become the assessment center.
- **Outcome:** PASS: covers redistributed/quantized open weights and removes the official-release assumption once the artifact is converted or mirrored.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/attack-surface-catalog.md:127-140` —  /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **HuggingFace model repository**  /  Model weights, repository metadata, custom code  /  Mal...
  - `synthesis/attack-surface-catalog.md:142-161` — ### 3.2 Training and Fine-Tuning Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Training data ingestion**  /  Data pipeline f...
  - `synthesis/risk-matrix.md:45-76` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...

### SCN-15 — Unofficial fine-tune of foreign open weights on proprietary support data
- **Deployment:** Foreign official open weights are used as a base, then an external vendor produces an unofficial fine-tune using proprietary support transcripts and ships a new model artifact.
- **Input:** The vendor argues the base model was official, so the fine-tuned artifact inherits the original low supply-chain risk.
- **Expected assessment:** The official-base assumption does not transfer to the fine-tune. Fine-tuning creates new data exposure, poisoning, distillation, model-artifact, vendor, and behavioral-backdoor surfaces; SC-DEF-4 must be acknowledged because artifact identity does not prove behavior.
- **Outcome:** PASS: covers unofficial fine-tuning of foreign open weights and correctly reclassifies the risk around the new artifact, vendor pipeline, and proprietary data.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/asset-inventory.md:195-212` —  /  #  /  Asset  /  Why It's a Crown Jewel  /  Primary Threat  /   / --- / ------- / ---------------------- / ---------------- /   /  1  /  **API keys / secrets in prompts or environment**  /  Direct system compromise, financial loss, lateral movement  /  Chain B, ...
  - `synthesis/attack-surface-catalog.md:142-161` — ### 3.2 Training and Fine-Tuning Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Training data ingestion**  /  Data pipeline f...
  - `synthesis/risk-matrix.md:45-76` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-16 — Foreign open-weight base with third-party LoRA adapter in production agent
- **Deployment:** Foreign official open-weight base is loaded with a third-party LoRA adapter from an adapter registry and deployed in a tool-using production agent.
- **Input:** The team verifies the base model hash but does not verify the adapter publisher, adapter training data, or behavioral impact before enabling tools.
- **Expected assessment:** The adapter is the dominant supply-chain surface. Base-weight provenance is necessary but insufficient; LoRA swap/alignment-removal risk, AIBOM, adapter provenance, sandboxing, behavior probes, and tool permission controls are required.
- **Outcome:** PASS: covers adapter-based deployment and makes the LoRA artifact, not the verified foreign base, the main risk driver once production tools are enabled.
- **Evidence:**
  - `synthesis/assumptions.md:90-98` — B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk **Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature...
  - `synthesis/attack-surface-catalog.md:127-140` —  /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **HuggingFace model repository**  /  Model weights, repository metadata, custom code  /  Mal...
  - `synthesis/attack-surface-catalog.md:142-161` — ### 3.2 Training and Fine-Tuning Surfaces   /  Surface  /  Description  /  Threat Vector  /  Threat Category  /  Risk Rating  /   / --------- / ------------- / --------------- / ---------------- / ------------- /   /  **Training data ingestion**  /  Data pipeline f...
  - `synthesis/risk-matrix.md:45-76` — ## Threat Risk Ratings  ### Tier 1: Critical Risks (Risk Score 19–25)   /  Threat  /  Likelihood  /  Impact  /  Base Score  /  Elevation Condition  /  Elevated Score  /  Owner  /  Regulatory  /   / --- / --- / --- / --- / --- / --- / --- / --- /   /  **Indirect PI → Excessiv...
  - `synthesis/defense-playbook.md:155-220` — ## Defense Layer 2: Excessive Agency Defenses  ### AGENCY-DEF-1: Minimal Permission Scoping [DEV] — **PRIMARY** **Effectiveness:** CRITICAL (if no tool access, PI impact is noise) **Latency cost:** None **Constraint notes:** Requires upf...
  - `synthesis/risk-matrix.md:118-148` — ---  ## Regulatory Mapping  ### EU AI Act (Regulation 2024/1689)   /  Threat / control area  /  EU AI Act Article  /  Obligation  /   / --- / --- / --- /   /  All high-risk AI threat assessment  /  Article 9 (Risk Management System)  /  Identify, estimate, ev...

### SCN-17-MEMORY — Cross-session durable-memory poisoning
- **Deployment:** Enterprise research agent with durable cross-session summaries and a later privileged document-publication workflow.
- **Input:** An external document causes attacker-shaped text to be proposed for durable memory; a later session retrieves it before a state-changing action.
- **Expected assessment:** T09-MEMORY applies at base score 8, elevated to 10 only when later retrieval reaches the higher-privilege workflow. MEM-DEF-1 must independently authorize writes and provide provenance, expiry, quarantine, rollback, and cross-session tests.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:375-375` —  /  **Durable agent memory**  /  Cross-session memory, summaries, preferences, or memory retrieval store  /  T09-MEMORY persistent memory poisoning; future-session goal drift  /  Cat 1, Cat 9  /  MEDIUM; elevate impact when later retrieval has gre...
  - `synthesis/threat-taxonomy.md:437-437` — ### T09-MEMORY / T09-IDENTITY — Category 9: Persistent Memory Poisoning and Inter-Agent Trust Escalation
  - `synthesis/risk-matrix.md:228-228` —  /  Persistent memory poisoning  /  2/5  /  2  /  4  /  **8**  /  Poisoned memory is retrieved into a higher-privilege workflow (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 9, 15  /  MEM-DEF-1, PI-DEF-2, DET-DEF-3  /
  - `synthesis/defense-playbook.md:841-841` — ### MEM-DEF-1: Durable Memory Write Authorization [DEV + OPS] — **PRIMARY**

### SCN-18-SKILL-RETRIEVAL — Semantic skill-retrieval manipulation
- **Deployment:** Agent platform that selects reusable marketplace skills through semantic retrieval and planner ranking.
- **Input:** A skill uses misleading metadata to rank above a safe skill and is selected for a privileged task.
- **Expected assessment:** T03-SKILL applies at base score 8. SKILL-DEF-1 must evaluate admission, semantic retrieval, planner selection, permission compatibility, and negative retrieval cases.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:376-376` —  /  **Skill retrieval / planner selection**  /  Semantic search and planning path that selects reusable skills  /  T03-SKILL retrieval manipulation; planner deception; capability substitution  /  Cat 3, Cat 9  /  MEDIUM pending field evidence  /
  - `synthesis/threat-taxonomy.md:418-418` — ### T03-SKILL — Category 3 / 9: Agent Skill Lifecycle Compromise
  - `synthesis/risk-matrix.md:229-229` —  /  Skill lifecycle compromise  /  2/5  /  2  /  4  /  **8**  /  Unreviewed skill update gains high-impact tool access (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 15, 17  /  SKILL-DEF-1, AGENCY-DEF-1, SC-DEF-1  /
  - `synthesis/defense-playbook.md:856-856` — ### SKILL-DEF-1: Lifecycle-Aware Skill Supply Chain [DEV + OPS] — **PRIMARY**

### SCN-19-SKILL-UPDATE — Post-install skill update rug pull
- **Deployment:** Coding agent with pinned skill versions, automated update checks, repository write access, and outbound network tools.
- **Input:** A previously reviewed skill update changes dependencies and requests broader tool permissions after installation.
- **Expected assessment:** T03-SKILL remains base 8 and reaches 10 only when the unreviewed update gains high-impact tools. SKILL-DEF-1 requires signed provenance, review-on-change, permission-diff checks, and rollback.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:377-377` —  /  **Skill evolution channel**  /  Updates, dependency changes, or post-install metadata changes  /  T03-SKILL rug pull; delayed malicious behavior; permission creep  /  Cat 3  /  MEDIUM pending field evidence  /
  - `synthesis/threat-taxonomy.md:418-418` — ### T03-SKILL — Category 3 / 9: Agent Skill Lifecycle Compromise
  - `synthesis/risk-matrix.md:229-229` —  /  Skill lifecycle compromise  /  2/5  /  2  /  4  /  **8**  /  Unreviewed skill update gains high-impact tool access (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 15, 17  /  SKILL-DEF-1, AGENCY-DEF-1, SC-DEF-1  /
  - `synthesis/defense-playbook.md:856-856` — ### SKILL-DEF-1: Lifecycle-Aware Skill Supply Chain [DEV + OPS] — **PRIMARY**

### SCN-20-IDENTITY — Inter-agent identity and delegation spoofing
- **Deployment:** Multi-agent finance workflow using authenticated transport but natural-language role and delegation claims.
- **Input:** A compromised analyst agent claims to be an approver and asks a payment agent to execute an irreversible transfer.
- **Expected assessment:** T09-IDENTITY applies at base 8 and elevated 10 because the claim can authorize an irreversible action. MA-DEF-3 must independently verify workload identity, delegation scope, and privilege ceilings.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:378-378` —  /  **Inter-agent identity claim**  /  Identity and privilege metadata attached to agent messages  /  T09-IDENTITY trust escalation; confused deputy; privilege inflation  /  Cat 9  /  MEDIUM; elevate impact when claims authorize sensitive actions  /
  - `synthesis/threat-taxonomy.md:437-437` — ### T09-MEMORY / T09-IDENTITY — Category 9: Persistent Memory Poisoning and Inter-Agent Trust Escalation
  - `synthesis/risk-matrix.md:230-230` —  /  Inter-agent trust escalation  /  2/5  /  2  /  4  /  **8**  /  Self-asserted identity can authorize irreversible or sensitive action (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 14, 15  /  MA-DEF-1, MA-DEF-3, AGENCY-DEF-2  /
  - `synthesis/defense-playbook.md:869-869` — ### MA-DEF-3: Cryptographic Inter-Agent Identity [DEV + OPS] — **PRIMARY**

### SCN-21-COMPUTER-USE — Computer-use visual-state disagreement
- **Deployment:** Browser-operating agent that receives screenshot pixels, DOM, accessibility state, and can submit purchases.
- **Input:** Off-screen accessibility text conflicts with the visible confirmation page and attempts to redirect the purchase.
- **Expected assessment:** T10-CUA applies at base 8 and elevated 10 when the interface can trigger an irreversible purchase. CUA-DEF-1 must reconcile representations and validate the semantic action before execution.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:379-379` —  /  **Computer-use visual field**  /  Rendered UI, viewport, DOM/accessibility tree, and off-screen elements  /  T10-CUA visual prompt injection; deceptive clicks; approval laundering  /  Cat 10, Cat 12  /  MEDIUM pending field evidence  /
  - `synthesis/threat-taxonomy.md:448-448` — ### T10-CUA — Category 10: Computer-Use Visual Attack
  - `synthesis/risk-matrix.md:231-231` —  /  Computer-use visual attack  /  2/5  /  2  /  4  /  **8**  /  Visual state can trigger irreversible external action (Impact 4→5)  /  **10**  /  Developer  /  EU AI Act Art. 14, 15  /  CUA-DEF-1, AGENCY-DEF-2  /
  - `synthesis/defense-playbook.md:882-882` — ### CUA-DEF-1: Visual and Interface-State Validation [DEV] — **PRIMARY**

### SCN-22-SESSION — Incremental session contamination and goal hijacking
- **Deployment:** Long-running procurement agent with per-message filters and state-changing purchasing tools.
- **Input:** Individually benign instructions accumulate across turns and gradually replace the approved procurement goal.
- **Expected assessment:** T01-SESSION applies at base 8 and elevated 10 when accumulated influence reaches the purchasing path. DET-DEF-3 must reconstruct trajectory-level influence; it does not lower preventive residual risk.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:375-375` —  /  **Durable agent memory**  /  Cross-session memory, summaries, preferences, or memory retrieval store  /  T09-MEMORY persistent memory poisoning; future-session goal drift  /  Cat 1, Cat 9  /  MEDIUM; elevate impact when later retrieval has gre...
  - `synthesis/threat-taxonomy.md:454-454` — ### T01-SESSION — Category 1 / 9: Session Context Contamination and Goal Hijacking
  - `synthesis/risk-matrix.md:232-232` —  /  Session contamination / incremental escalation  /  2/5  /  2  /  4  /  **8**  /  Accumulated influence reaches a higher-privilege action path (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 14, 15  /  PI-DEF-1, DET-DEF-3, AGENCY-DEF-3  /
  - `synthesis/defense-playbook.md:907-907` — ### DET-DEF-3: Trajectory and Influence Monitoring [OPS] — **SECONDARY**

### SCN-23-RELAY — BYOK response-path relay tampering
- **Deployment:** High-privilege agent using a third-party BYOK model router that can transform provider responses before tool execution.
- **Input:** The relay returns a tool call that is internally well-formed but cannot be independently tied to provider-authorized output.
- **Expected assessment:** T11-RELAY remains provisional at base 5. RELAY-DEF-1 prefers a direct path or provider-authenticated response; relay-only hashes are accountability evidence, not proof of upstream authorization.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:380-380` —  /  **LLM response relay / router**  /  BYOK proxy, gateway, model router, or response-transforming middleware  /  T11-RELAY post-alignment response forgery; tool-call field tampering  /  Cat 11  /  MEDIUM and provisional pending independent repli...
  - `synthesis/threat-taxonomy.md:464-464` — ### T11-RELAY — Category 11: Response-Path Integrity / Relay Tampering
  - `synthesis/risk-matrix.md:233-233` — /  Response-path relay tampering *(provisional)*  /  1/5  /  1  /  4  /  **4**  /  Independent replication in the assessed relay path establishes practical exploitability (Likelihood 1→2)  /  **8**  /  Developer + Operator + Provider  /  EU AI Act Art. 15  /  RELAY-DEF-1, schema validation, direct provider path  /
  - `synthesis/defense-playbook.md:892-892` — ### RELAY-DEF-1: Response-Path Integrity [DEV + OPS] — **PRIMARY where a relay exists**

### SCN-24-REPRESENTATION — Representation-confusion at binary-to-text boundary
- **Deployment:** Reverse-engineering assistant that converts binaries and decompiler output into text used by an automated validator.
- **Input:** Attacker-shaped binary-derived text is treated as independent evidence and as an instruction by the downstream model.
- **Expected assessment:** T10-REPRESENTATION is monitored at base 4 and can reach 8 only after reproduction in this pipeline. REP-DEF-1 preserves origin and validates semantics across the deployed conversion boundary.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:381-381` —  /  **Representation boundary**  /  Conversion between binary, text, code, metadata, records, and evidence  /  T10-REPRESENTATION data interpreted as instructions or non-independent evidence  /  Cat 10, Cat 11  /  LOW/MEDIUM; monitor and test the ...
  - `synthesis/threat-taxonomy.md:472-472` — ### T10-REPRESENTATION — Category 10 / 11: Representation Confusion
  - `synthesis/risk-matrix.md:234-234` —  /  Representation confusion *(monitor)*  /  1/5  /  1  /  4  /  **4**  /  Independent reproduction in the assessed representation pipeline (Likelihood 1→2)  /  **8**  /  Developer  /  EU AI Act Art. 15  /  REP-DEF-1, PI-DEF-4  /
  - `synthesis/defense-playbook.md:916-916` — ### REP-DEF-1: Representation Boundary Validation [DEV] — **PRIMARY where conversion exists**

### SCN-25-DISCLOSURE — Capability disclosure enabling follow-on attack
- **Deployment:** Agent API exposes tool schemas, memory endpoints, approval triggers, and topology through verbose diagnostics.
- **Input:** An attacker uses disclosed tool and approval details to target a later prompt-injection and privilege-escalation attempt.
- **Expected assessment:** Capability disclosure is an enabling Category 5 subtype, not automatically critical. Its risk inherits the reachable follow-on path; existing prompt, agency, identity, and memory controls must enforce authorization outside model text.
- **Outcome:** PASS: the v1.9 corpus identifies the surface, applies a calibrated overlay, routes the required controls, and defines a residual action.
- **Evidence:**
  - `synthesis/attack-surface-catalog.md:378-378` —  /  **Inter-agent identity claim**  /  Identity and privilege metadata attached to agent messages  /  T09-IDENTITY trust escalation; confused deputy; privilege inflation  /  Cat 9  /  MEDIUM; elevate impact when claims authorize sensitive actions  /
  - `synthesis/threat-taxonomy.md:431-431` — ### T05-CAPABILITY — Category 5: Capability and Architecture Disclosure
  - `synthesis/risk-matrix.md:230-230` —  /  Inter-agent trust escalation  /  2/5  /  2  /  4  /  **8**  /  Self-asserted identity can authorize irreversible or sensitive action (Impact 4→5)  /  **10**  /  Developer + Operator  /  EU AI Act Art. 14, 15  /  MA-DEF-1, MA-DEF-3, AGENCY-DEF-2  /
  - `synthesis/defense-playbook.md:869-869` — ### MA-DEF-3: Cryptographic Inter-Agent Identity [DEV + OPS] — **PRIMARY**

## Rerun history
- **RED-0** `python scripts/test_scenario_suite.py` → **FAIL** — Scenario suite file was missing; tests failed before any scenario could meet the quality bar.
- **RUN-1** `python scripts/test_scenario_suite.py` → **PASS** — All ten scenarios satisfied uniform pass/fail criteria after the suite was created.
- **RED-1** `python scripts/test_scenario_suite.py` → **FAIL** — Foreign LLM scenario coverage tests failed because the suite still had 10 scenarios and no foreign_model_posture distribution series.
- **RUN-2** `python scripts/test_scenario_suite.py` → **PASS** — Foreign model scenario series added and all sixteen scenarios satisfied the uniform pass/fail criteria on affected rerun.
- **RED-2** `python scripts/test_scenario_suite.py` → **FAIL** — The v1.9 coherence contract required 25 scenarios but the suite still contained 16.
- **RUN-3** `python scripts/test_scenario_suite.py` → **PASS** — All 25 scenarios, including nine v1.9 agentic cases, satisfied the uniform pass/fail and citation criteria.

## Final complete rerun
`python scripts/test_scenario_suite.py` → **PASS** (25 passed, 0 failed).

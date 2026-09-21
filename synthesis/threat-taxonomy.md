# LLM Threat Taxonomy

**Version:** 1.11 (September research integration)
**Status:** Living document — update quarterly or after major incidents

---

## Purpose
Master taxonomy of threats to LLM systems, organized by attack surface. Each entry links to associated attack trees, defenses, and regulatory mappings. This authoritative list prioritizes the threats that matter instead of cataloging every possibility.

---

## Threat Categories

### Category 1: Prompt Injection (LLM01 — OWASP)

**Priority: CRITICAL**
**Wild_vs_Theory: 4/5** — September provider reporting confirms field prompt injection stealing AI-wrapper keys (see `research/sources/Landscape-Update-2026-09.md`). EchoLeak individually remains 3/5: production demonstration, no customer impact reported.

Prompt injection is the manipulation of LLM behavior through crafted inputs that override system-level instructions. It is the premier threat to LLM deployments and is not fully mitigated by RAG, fine-tuning, or input filtering.

**Attack economics change (v1.1 update):** Prompt injection no longer requires moderate-to-high attacker sophistication. Pre-optimized PI templates and jailbreak-as-a-service are sold in underground markets. The expertise barrier for PI attacks has dropped to LOW — any attacker can purchase an optimized template. This fundamentally changes the threat model: PI attacks are no longer limited to skilled adversaries.

**Sub-types:**

| Sub-type | Description | Vector |
|---|---|---|
| Direct PI | User-supplied input explicitly instructs model to ignore system prompt | Chat input, API `messages` field |
| Indirect PI | Adversarial content embedded in external data the model retrieves (RAG, search results, documents) | RAG pipeline, document ingestion |
| Multi-turn PI | Injection spread across conversation turns, accumulating context | Multi-turn chat, agentic loops |
| Cross-context PI | Injection propagates between agents in multi-agent systems | Agent-to-agent messaging |
| Purchased PI Template | Pre-optimized PI/jailbreak template from underground market | Defeats pattern-based input filtering |

**Key insight (from Arcanum PI Taxonomy):** Attack surface extends to **any content the model parses** — text, documents, images, API responses, structured data, and retrieved contexts. Restricting analysis to "text input fields" dramatically underestimates the attack surface.

**Key update (v1.5 — Slow-Burn PI, Jun 2026):** Standard per-event PI detectors fail against slow-burn attacks where each step is individually below threshold. For multi-turn systems, the attack surface includes both the content of each turn and the **temporal accumulation** of context across turns. Detection requires proxy-side temporal analysis alongside per-turn input scanning.

**Underground PI Market impact (v1.1 addition):**
- Pattern-based input filtering is increasingly ineffective — purchased template variants evade detection
- Attack volume increases — automated tools generate thousands of PI template variants
- Economic model shifts — attacker cost is a subscription fee, not ML expertise
- Only ML-based detection and infrastructure-level controls (privilege separation) remain effective against purchased variants

**Instruction Hierarchy Attack Surface:**
```
1. System prompt (highest privilege)
2. Developer message / hardcoded instructions
3. User message (end-user input)
4. Retrieved context (RAG, external data)
5. Tool outputs (function call returns)
```
Indirect PI exploits the gap between retrieved context and user intent — the model cannot reliably distinguish "retrieved trusted content" from "injected instructions" at the same hierarchy level.

**Attack surface references:**
→ Attack Tree: `attack-trees.md#chain-a-indirect-pi-excessive-agency`
→ Defense: `defense-playbook.md#pi-defense`
→ Regulatory: `risk-matrix.md#eu-ai-act`

---

### Category 2: Excessive Agency (LLM06 — OWASP)

**Priority: CRITICAL**
**Wild_vs_Theory: 4/5** — Confirmed field disclosure through AI wrappers supports the aggregate category; individual paths retain their own evidence ratings. See `research/sources/Landscape-Update-2026-09.md`.

LLM systems granted more agency (tool use, API calls, file write, data exfiltration) than necessary. When combined with prompt injection, excessive agency enables attacks that go beyond information manipulation to **unauthorized actions in downstream systems**.

**Sub-types:**

| Sub-type | Description |
|---|---|
| Unbounded tool access | Model can call any registered tool without per-call confirmation |
| Privilege escalation via PI | Injection manipulates model into calling high-privilege tools |
| Chained tool use | Single user request triggers multi-step tool chain without human review |
| Cross-system action | Model takes real-world actions (email, file write, payment) outside the AI boundary |

**Critical linkage:** Excessive agency is the **force multiplier** for prompt injection. Without model tools, PI can still disclose sensitive context through answers and renderer requests. Agency adds state-change and execution risks; read-only outbound queries also need confidentiality controls.

**Attack surface references:**
→ Attack Tree: `attack-trees.md#chain-a-indirect-pi-excessive-agency`
→ Attack Tree: `attack-trees.md#chain-c-multi-agent-context-propagation`
→ Defense: `defense-playbook.md#agency-defense`

---

### Category 3: Supply Chain Compromise (LLM03 — OWASP)


**Priority: HIGH**
**Wild_vs_Theory: 4/5** — JFrog/ReversingLabs documented confirmed malicious models on HuggingFace with custom inference exfiltration; LoRA adapter swap demonstrated in lab

Risks introduced by third-party model hubs, fine-tuning pipelines, and model registries.

**Sub-types:**

| Sub-type | Description | Real-world evidence |
|---|---|---|
| Malicious model weights | Model published with compromised weights or inference code | JFrog/ReversingLabs: models with custom `__init____` exfiltrating data |
| LoRA/PEFT adapter swap | Malicious low-rank adaptation files replace legitimate ones | Academic demonstrations; registry replay attacks |
| Training data poisoning | Backdoors implanted via crafted training examples | Multiple academic papers (2019–2024) |
| Upstream dependency compromise | Base model, tokenizer, or inference framework compromised | Pip/npm-style attacks on ML dependencies |
| **Skill marketplace compromise** | Malicious agent skills published to marketplace — analogous to npm supply chain attacks; can exfiltrate data, hijack agent, persist as supply-chain foothold | **NEW v1.5 — arXiv Jun 2026** |

**AIBOM (AI Bill of Materials)** is the primary mitigation framework but requires concrete schema definition (see `defense-playbook.md#aibom-schema`).

> **⚠️ Weight-level trojan / backdoor defense gap (v1.2):** AIBOM with Sigstore verifies WHO published a model and that artifact integrity is intact. It does NOT verify WHAT the model does. Behavioral backdoors, malicious `__init__` code (JFrog/ReversingLabs confirmed), and LoRA adapter alignment removal cannot be detected by supply chain artifact signing. See `defense-playbook.md#sc-def-4` for the documented operational gap and available mitigations.

**Attack surface references:**
→ Attack Tree: `attack-trees.md#chain-b-supply-chain-silent-exfiltration`
→ Defense: `defense-playbook.md#supply-chain-defense`
→ Defense Gap: `defense-playbook.md#sc-def-4`
→ Regulatory: `risk-matrix.md#gdpr-implications`

---

### Category 4: Data and Model Poisoning (LLM04 — OWASP)

**Priority: HIGH**
**Wild_vs_Theory: 3/5** — Training/fine-tuning poisoning extensively documented academically; RAG poisoning = indirect PI variant (Wild_vs_Theory 4/5, same attack); embedding poisoning mostly theoretical

Compromising training data, fine-tuning datasets, or RAG document stores to implant backdoors or manipulate model behavior.

| Sub-type | Description |
|---|---|
| Training-time poisoning | Malicious examples in training data cause harmful outputs at inference |
| Fine-tuning poisoning | Adversarial fine-tuning dataset implants backdoors |
| RAG context poisoning | Attacker writes content to a document store later retrieved as trusted context |
| Embedding poisoning | Manipulating embedding vectors in vector databases |

RAG poisoning overlaps with indirect prompt injection only when the poisoned material supplies instructions. Factual or ranking manipulation can cause the model to faithfully reproduce a forged policy or record without any instruction override. Training/fine-tuning poisoning can also persist in learned behavior. Assess data integrity separately with DATA-DEF-1: write/promotion authority, independent source validation, dataset versions, derived-data cleanup and model rollback where needed. See `research/sources/Review-Corrections-2026-09-19.md` (OWASP LLM04).

---

### Category 5: System Prompt Leakage (LLM07 — OWASP)

**Priority: MEDIUM**

Extraction of system prompts, developer messages, or proprietary instruction sets from LLM deployments.

| Sub-type | Description |
|---|---|
| Direct extraction | Malicious prompts designed to cause model to output system prompt contents |
| Indirect extraction | System prompt contents inferred from model behavior without direct output |
| Log leakage | System prompts inadvertently included in logs, error messages, or outputs |

**Why medium priority:** System prompt leakage is dangerous primarily when the prompt contains security controls, API keys, or proprietary business logic. For many deployments, prompt leakage is a minor information disclosure. However, for systems where prompt == security boundary (e.g., rule-based content filtering encoded in system prompt), extraction is critical.

---

### Category 6: Model Extraction and Replication

**Priority: LOW-MEDIUM** *(revised down from synthesis)*

Query-based replication of proprietary models (CopyNN, KnockoffNN attacks).

**Reviser note (per Reviewer Finding 8):** Model extraction is economically motivated primarily for **highly specialized, expensive-to-train domain models**. General-purpose LLM replication provides minimal advantage over direct API subscription. Most organizations face this threat only if they deploy highly customized fine-tuned models with significant IP value.

| Sub-type | Description |
|---|---|
| Full model extraction | Replicate model weights via large-volume querying |
| Fine-tuning data extraction | Infer proprietary training data characteristics from model outputs |
| Architecture inference | Reverse-engineer model architecture from API behavior |

---

### Category 7: Embedding Inversion and Training Data Extraction (LLM08 — OWASP)

**Priority: MEDIUM**

Attacks that reconstruct training data or extract sensitive information from embedding spaces.

| Sub-type | Description | Regulatory impact | Evidence |
|---|---|---|---|
| Membership inference | Determine if a specific record was in training data | GDPR Article 17 (right to erasure) | — |
| Property inference | Infer aggregate characteristics of training data | GDPR Article 25 (privacy by design) | — |
| Embedding inversion | Reconstruct inputs from embedding vectors | Data breach notification obligations | — |
| Gradient leakage | Sensitive data leaked through training gradients | Same as above | — |
| **Query pattern / mosaic leakage** | Deep research agents combining private documents with web searches leak private data via mosaic effect; individually benign queries can be reassembled to infer sensitive facts. Training agents for better performance increased leakage (34%→51.7%); PA-DR training reduced leakage to 9.9%, showing prompt-level privacy is insufficient. | GDPR Articles 17, 25; EU AI Act Art. 9 | **NEW v1.5 — MosaicLeaks arXiv Jun 2026** |

---

### Category 8: Denial of Service (LLM10 — Unbounded Consumption — OWASP)

**Priority: MEDIUM-HIGH**

Attacks that degrade availability of LLM services.

| Sub-type | Description |
|---|---|
| Context exhaustion | Attacker fills context window to prevent legitimate use |
| API quota exhaustion | Metered API quota depleted, causing service loss for legitimate users |
| Resource exhaustion | Adversarial inputs cause excessive compute consumption per token |
| Context reranking abuse | Manipulating retrieved context ordering to degrade output quality |

**Economics note (per Reviewer challenge):** LLM10 quota exhaustion on metered APIs is **financially destructive to the victim** — the attacker incurs cost while the victim loses service. This is not ambiguous.

---

### Category 9: Multi-Agent Context Propagation

**Priority: HIGH**
**Wild_vs_Theory: 3/5** — LangGraph source code confirms ToolNode.invoke() returns unsanitized tool output as ToolMessage to shared messages state. Next agent receives poisoned context with no authenticity signal. Pattern confirmed structurally via source analysis (Jun 2026). No published CVE addresses Chain C context propagation specifically.

> ⚠️ **Correction (v1.5 — Jun 2026 research)**: The v1.4 claim of "LangGraph has 6 published security advisories (2025–2026)" is **unverified**. NVD and GitHub Advisory Database searches returned zero LangGraph-specific CVEs. LangChain (the parent org) has a published security policy with bug bounty; LangGraph CVE status requires direct NVD verification. The specific CVE IDs cited in v1.4 (CVE-2026-27794, CVE-2025-67644, CVE-2026-48775, CVE-2026-28277) could not be confirmed and may be LangChain-wide or fabricated. Treat the LangGraph CVE claim as **unverified pending direct NVD query**.

Threats arising from chained LLM agents where one agent's compromised context becomes input to another.

| Sub-type | Description | New in v1.2/v1.5 |
|---|---|---|
| Sequential agent poisoning | PI in agent N's output propagates to agent N+1's context | — |
| Shared memory corruption | Adversarial content injected into shared context store | — |
| Tool-use chain exploitation | Compromised agent triggers cascading unauthorized tool calls | — |
| Role confusion | Agent cannot distinguish between user request and injected agent message | — |
| **MCP protocol propagation** | PI propagates via Model Context Protocol channel; compromised MCP server returns attacker-controlled data implicitly trusted as ground truth | v1.2 |
| **A2A protocol propagation** | PI propagates via Agent-to-Agent protocol; authenticated trust relationship bypasses input validation; Agent B may have higher privileges than Agent A | v1.2 |
| **LangGraph Send API / ToolCallWithContext** | Injection at dispatch level; state context manipulation before tool execution | v1.2 |
| **LangGraph Command primitive** | Direct state injection bypassing message-passing channel entirely | v1.2 |
| **Slow-Burn / Temporal Accumulation PI** | Weak adversarial directives distributed across multi-turn trajectory; each event is below threshold, but temporal accumulation reveals the attack. | v1.5 |

This category compounds Categories 1 and 2: prompt injection in a single-agent context causes localized harm; in a multi-agent context it propagates and amplifies.

**Attack surface references:**
→ Attack Tree: `attack-trees.md#chain-c-multi-agent-context-propagation`
→ Defense: `defense-playbook.md#multi-agent-defense`

---

### Category 10: Non-Text Injection Vectors

**Priority: MEDIUM**

Attack surface beyond text input — image, audio, and structured data injection.

| Sub-type | Description | Evidence |
|---|---|---|
| Image adversarial perturbation | Visually imperceptible modifications causing model to ignore system constraints | — |
| Vision-language model manipulation | Images crafted to bias VLA interpretation | — |
| **MIRAGE visual indirect PI** | Diffusion model-generated adversarial images inject hidden instructions in constrained regions (ad slots, sponsored cards) to hijack next-action prediction; perceptually benign under realistic deployment constraints. | **NEW v1.5 — arXiv Jun 2026** |
| Structured data injection | JSON/YAML/SQL parsed by LLM that contains adversarial instructions | — |
| Audio injection | Adversarial audio perturbations in ASR→LLM pipeline | — |
| Encoding tricks | Non-standard encodings (base64, hex, Unicode homoglyphs) that bypass input filtering | — |

**Note:** These vectors are less documented than text-based PI but are valid attack surfaces for systems processing multi-modal inputs or structured data.

---

### Category 11: Output Validation Failures (LLM05 — Improper Output Handling — OWASP)

**Priority: MEDIUM**

Attacks exploiting what the LLM returns to users or downstream systems after processing adversarial inputs.

| Sub-type | Description |
|---|---|
| Browser execution / disclosure | Model-generated HTML, Markdown, SVG or streamed content executes active code or loads an unauthorized remote resource |
| Database / command / path injection | Model output becomes executable SQL, shell/code or an unrestricted filesystem path |
| Server-side request forgery | A generated destination reaches unauthorized internal endpoints or redirects |
| Unfiltered output propagation | Model outputs harmful content that passes to users or systems without review |
| Injection via tool return | Tool outputs processed by model contain injection payloads |
| Cascading output contamination | Compromised outputs become context for subsequent interactions |
| Silent Hallucination Exploitation | Attacker engineers false but plausible outputs that cause downstream harm |

---

PI-DEF-4 must enforce safety at the actual browser, database, command runner, file writer and network client. Shape validation, semantic review and logging cannot replace context-specific encoding, parameterization, operation authorization and isolation. See `research/sources/Review-Corrections-2026-09-19.md` (OWASP LLM05).

### Category 12: Human-in-the-Loop Failures

**Priority: MEDIUM**

Failure modes where human reviewers do not catch adversarial manipulation.

**Critical blind spot (v1.1 addition):** Standard HITL confirmation shows the proposed action but not the context provenance that caused it. Reviewers evaluate whether an action looks reasonable in isolation, not whether it was prompted by adversarial content. A sophisticated PI attack can craft instructions producing benign-seeming actions with malicious intent.

| Sub-type | Description |
|---|---|
| Reviewer fatigue | High volume of outputs overwhelms human review capacity |
| Sophisticated PI evading detection | Injection crafted to appear legitimate to human reviewers |
| Authority bias in review | Humans defer to confident LLM outputs even when incorrect |
| Cross-lingual blind spots | PI in non-English languages evades reviewer comprehension |
| HITL provenance blind spot (NEW) | Reviewer sees action, not the injected instruction causing it — cannot evaluate whether context was adversarial |

**Corrected HITL UX (v1.1):** HITL confirmation must include sufficient context provenance: what triggered the action (user input, retrieved document, tool result), source of influencing content, and brief LLM rationale. Without context provenance, HITL review is ineffective against sophisticated PI.

---

### Category 13: Defense Control Type Confusion

**Priority: MEDIUM-HIGH**
**Wild_vs_Theory: 3/5** — Control type misidentification is a documented pattern in security reviews; specific evidence from multiple red-team engagements misclassifying alignment controls as technical

Misunderstanding the type of control (technical vs. alignment) leads to incorrect effectiveness estimates and flawed defense-in-depth calculations.

| Sub-type | Description | Example |
|---|---|---|
| Infrastructure-enforced control | Technical enforcement by pipeline/infrastructure, not dependent on LLM behavior | Tool allowlist blocking RAG context from tool calls |
| LLM-alignment-based control | Effectiveness depends entirely on model's instruction-following behavior | Prompt instruction telling LLM to treat RAG context as untrusted |
| Incorrect independence assumption | Treating alignment control + infrastructure control as independent when they are not | Assuming PI-DEF-2 (prompt) + AGENCY-DEF-1 (allowlist) are multiplicative when only AGENCY-DEF-1 is actually enforced |

**Why this matters:** Organizations relying on prompt-level privilege separation (alignment control) have NO technical enforcement if the LLM doesn't follow instructions. Only infrastructure-enforced controls provide genuine defense independence.

---

### Category 13 Addendum: Capability Withholding

**Priority: MEDIUM** (taxonomic note — no in-wild intentional cases confirmed)
**Wild_vs_Theory: 1/5** (intentional); **Wild_vs_Theory: 3/5** (accidental RLHF reward hacking)

**Distinct from commission attacks (Cat. 1, 4):** Capability withholding is an *omission* attack — the adversary degrades the model's capability rather than manipulating it to perform specific harmful actions.

| Sub-type | Evidence | Wild_vs_Theory |
|---|---|---|
| Intentional capability withholding | No confirmed in-wild cases; BadAgent (ACL 2024) is commission-oriented, not withholding-oriented | 1/5 |
| Accidental RLHF reward hacking | Production RL systems exhibit reward hacking causing real capability degradation; Energy Loss in RLHF (arXiv 2501.19358) documents mechanism | 3/5 |
| RLHF supply chain poisoning (external attacker path) | Theoretical only — no confirmed path for external attacker to induce energy loss without RLHF pipeline access | 1/5 |

**Taxonomic placement determination (Round 14 — provisional):**
The open question from Round 12 is now provisionally resolved. Analysis of the academic literature yields the following determination:

- **RLHF supply chain poisoning requiring reward model or preference data access = [PROV] supply chain** — This is NOT achievable by an external attacker. All documented RLHF poisoning attacks (RLHFPoison/ACL 2024, Universal Jailbreak Backdoors/Rando & Tramèr 2024, Sequential Data Poisoning/arXiv 2606.04929) require insider access to the RLHF annotation pipeline, the reward model training system, or the preference data collection process. No documented path exists for an external attacker (without RLHF pipeline credentials) to induce capability withholding.

- **External attacker path via training data contamination (pre-training/fine-tuning corpus):** An external actor could theoretically contaminate publicly-available training data, but this does NOT constitute RLHF-specific reward hacking. The attacker's influence terminates at the data layer; there is no demonstrated mechanism by which external training data contamination propagates through RLHF to produce targeted capability suppression. The gap between "poisoned training data" and "capability withholding via RLHF reward manipulation" is undemonstrated.

- **Conclusion:** Intentional capability withholding via RLHF requires [PROV] (RLHF pipeline operator) access. No external path is documented in the academic literature. Accidental RLHF reward hacking (Wild_vs_Theory 3/5) is a [OPS] concern. The distinction matters for ownership assignment and MITRE ATLAS ATT&CK mapping.

- **Wild_vs_Theory ratings updated:** Intentional RLHF supply chain poisoning: 1/5 (requires insider access, no external path documented). Accidental RLHF reward hacking with capability degradation: 3/5 (production cases documented). External training data poisoning leading to capability effects: 1/5 (no demonstrated path to RLHF capability suppression).

**Evidence:** RLHFPoison (ACL 2024, aclanthology.org/2024.acl-long.140) — threat model assumes malicious RLHF annotator. Universal Jailbreak Backdoors (Rando & Tramèr, 2024, spylab.ai/blog/poisoning-rlhf) — "malicious RLHF annotator creates harmful prompts." Sequential Data Poisoning in LLM Post-Training (arXiv 2606.04929, Jun 2026) — multiple adversaries with separate access to SFT and preference datasets (pipeline access assumed). Forethought ML Research (Jan 2026, forethought.org) — external actor threat model modeled for catastrophic secret loyalty, not simple capability withholding; acknowledges external actor CAN perform catastrophic data poisoning but this requires access to training pipelines not just raw data ingestion. No academic paper documents an external-path-only capability withholding attack.

**Primary mitigations:** Behavioral baselining + diversified RLHF sources [OPS]; Supply chain integrity (SC-DEF-1 AIBOM) [OPS/PROV].

**Attack surface references:**
→ Defense: `defense-playbook.md#defense-interaction-analysis`
→ Research: `research/synthesis.md` (Round 12)

---

### Category 14: Internal Safety Collapse — Validator Harness Attack (NEW — Jun 2026)

**Priority: CRITICAL**
**Wild_vs_Theory: 2/5 (controlled research).** Wu et al. demonstrate Task-Validator-Data (TVD) safety failures in ISC-Bench. The reported 95.3% is a worst-case result for selected scenarios, not a production prevalence estimate. See arXiv:2603.23509 and `research/sources/Review-Corrections-2026-09.md`.

**Adjacent incident, not mechanism attribution:** OpenAI's July 21 Hugging Face disclosure confirms a containment failure during internal cyber evaluation with reduced refusals and production classifiers disabled. It does not establish attacker-shaped harness input or attribute the ISC paper's mechanism. A TVD analogy is this framework's inference, not the source's finding. External attacks carried out by a model are adjacent LLM-as-attack-vector behavior; the containment lesson is relevant to infrastructure defenses without changing this framework's scope.

**Severity:** A reachable attacker-shaped harness causing major harm can still warrant HIGH/CRITICAL deployment risk despite low evidence maturity. Score actual exploitability and consequences; do not infer universal catastrophic impact from harmful text alone.

Internal Safety Collapse (ISC) is a harness-mediated structural vulnerability where a model's own task-completion drive produces harmful outputs without injected adversarial instructions. The practical attack condition is: **the target LLM/agent executes a task/validator/data harness the attacker controls or meaningfully shapes.** The model attempts to satisfy the validator's completion criteria and autonomously infers harmful or sensitive content as the only valid completion. The task structure can defeat safety behavior in the tested conditions; test the actual model, harness and independent output checks.

**This is not prompt injection.** The attack surface is not the prompt — it is the **task harness structure** itself. No adversarial instructions need to be present; the model's own reasoning about task completion produces the harmful output. A detector tuned only for explicit override phrases can miss this structure; no universal classifier-bypass guarantee is established.

**The TVD framework (Task-Validator-Data):**
- **Task** — a legitimate professional activity (e.g., evaluation, testing, code repair, dataset completion)
- **Validator** — code, schema, test, or evaluation harness that checks output format/completion, but enforces NO semantic safety bounds
- **Data** — intentionally incomplete; the model must fill gaps to satisfy the validator

When the model fills the data gaps to complete the task, it autonomously generates harmful content — because satisfying the validator is the only valid output, and the validator has no safety semantics.

**Applicability boundary:**
- **LOW / N/A:** plain inference consumption with no task/validator/data harness execution and no downstream fine-tuning, eval, dataset-generation, code-repair, or autonomous-tool use.
- **HIGH / CRITICAL:** any provider, self-hosted operator, agent platform, eval/fine-tuning/data-generation/code-repair pipeline, or enterprise workflow where an attacker can control or meaningfully shape task, validator/schema/test, incomplete data, uploaded documents, tool results, marketplace skills, customer integrations, or external datasets used by a harness.
- **Internal-only harnesses:** ordinary QA/supply-chain/data-governance risk unless attacker-shaped material enters the harness.

**Incident narrative status:** Fable/export-control/open-letter claims are **press/community narrative** unless independently corroborated. They should not carry the Wild_vs_Theory rating. The rating above is carried by the primary research evidence.

**Why standard defenses fail:**
- Input filtering: no adversarial patterns are required in the prompt
- Safety classifiers: effectiveness against this harness must be measured; training target alone does not establish detection or failure
- Output filtering: partial only; the model is doing what the harness asks it to do — complete the task

**Attack surface references:**
→ Attack Surface: `attack-surface-catalog.md#tvd-harness-surface`
→ Defense: `defense-playbook.md#isc-def-1-validator-harness-validation-dev--primary`
→ Primary source: [arXiv:2603.23509](https://arxiv.org/abs/2603.23509) — "Internal Safety Collapse in Frontier Large Language Models" (Wu et al., 2026)
→ Primary/source repository: [GitHub wuyoscar/Internal-Safety-Collapse](https://github.com/wuyoscar/Internal-Safety-Collapse) — public benchmark/release framing; note repository release details may differ from the arXiv paper
→ Adjacent containment incident (not explicit ISC attribution): OpenAI, ["OpenAI and Hugging Face partner to address security incident during model evaluation"](https://openai.com/index/hugging-face-model-evaluation-security-incident/) (2026-07-21); Hugging Face security disclosure (Jul 2026)

---

## Cross-Reference Index

| Threat Category | Primary Attack Tree | Primary Defenses | Regulatory Link |
|---|---|---|---|
| Prompt Injection | Chain A | PI Defense Playbook | EU AI Act Art. 13 |
| Excessive Agency | Chain A, Chain C | Agency Control Playbook | FTC AI Guidance |
| Internal Safety Collapse | — | Validator harness validation | EU AI Act Art. 9, Art. 15, Art. 17 |
| Supply Chain | Chain B | Supply Chain Playbook | GDPR Art. 25, 32 |
| Model Poisoning | Chain B | AIBOM + Sandboxing | EU AI Act Art. 9 |
| System Prompt Leakage | — | Prompt Protection | Trade secret law |
| Model Extraction | — | Rate limiting, output filtering | IP law |
| Embedding Inversion | — | Differential privacy, regularization | GDPR Art. 17 |
| DoS | — | Rate limiting, quota management | SLA obligations |
| Multi-Agent | Chain C | Context isolation, agent audit | EU AI Act Art. 14 |
| Non-Text Injection | Chain A (variant) | Input validation layers | EU AI Act Art. 13 |
| Output Validation | — | Output filtering, sandboxing | FTC deceptive practices |
| HITL Failures | — | Defense in depth, monitoring | EU AI Act Art. 14 |
| T01-SESSION — Session contamination / goal hijacking | Chain A extension | DET-DEF-3, AGENCY-DEF-3 | EU AI Act Art. 14, 15 |
| T03-SKILL — Skill lifecycle compromise | Chain B extension | SKILL-DEF-1, SC-DEF-1 | EU AI Act Art. 15, 17 |
| T05-CAPABILITY — Capability and architecture disclosure | Follow-on enabler | PI-DEF-1, MA-DEF-3 | EU AI Act Art. 13, 15 |
| T09-MEMORY — Persistent memory poisoning | Chain C extension | MEM-DEF-1, DET-DEF-3 | EU AI Act Art. 9, 15 |
| T09-IDENTITY — Inter-agent trust escalation | Chain C extension | MA-DEF-3, AGENCY-DEF-2 | EU AI Act Art. 14, 15 |
| T10-CUA — Computer-use visual attack | Computer-use branch | CUA-DEF-1, AGENCY-DEF-2 | EU AI Act Art. 14, 15 |
| T10-REPRESENTATION — Representation confusion *(monitor)* | Representation branch | REP-DEF-1 | EU AI Act Art. 15 |
| T11-RELAY — Response-path relay tampering *(provisional)* | Relay branch | RELAY-DEF-1 | EU AI Act Art. 15 |

---

## Framework for Adding New Threats

When a new threat is discovered or an incident occurs:

1. **Categorize** under existing categories or create new category
2. **Rate** likelihood × impact (see `risk-matrix.md`)
3. **Build or extend** attack tree showing chain relationships
4. **Assign** defense ownership (developer/operator/provider)
5. **Map** to regulatory framework
6. **Add** to `assessment-template.md` checklist

## v1.8 Agentic Trust-Boundary Updates — July 2026

The July 2026 last-30-days scan does not justify additional top-level categories. It does justify explicit agentic-era subtypes and one new trust-boundary module. These updates extend Categories 1, 3, 5, 9, 10, and 11 without changing the canonical category numbering.

### T03-SKILL — Category 3 / 9: Agent Skill Lifecycle Compromise

Reusable agent skills are not only runtime artifacts. Their security lifecycle includes repository admission, semantic retrieval, planner selection, execution, and later skill evolution. A skill can be benign at admission but become dangerous through misleading metadata, retrieval manipulation, planner deception, composition with another skill, or a malicious update.

**Required subtypes:**
- Repository admission compromise
- Semantic retrieval manipulation
- Planner-selection deception
- Skill-composition abuse
- Post-install rug pull or malicious evolution

**Evidence:** SkillSec-Eval reports a lifecycle-aware evaluation over 327 real-world skills and identifies vulnerabilities beyond runtime execution (arXiv:2607.13987, July 2026). This strengthens the existing Category 3 skill-marketplace entry; it does not establish a new Wild_vs_Theory score for every skill ecosystem.

### T05-CAPABILITY — Category 5: Capability and Architecture Disclosure

In agentic systems, disclosure of tool names, schemas, memory interfaces, agent topology, approval triggers, or validator behavior is not merely reputational leakage. It can convert black-box probing into a white-box follow-on attack against Categories 1, 2, 9, and 14.

Rate this subtype according to whether the disclosed capability materially reduces the effort needed to reach a privileged action. Do not automatically rate ordinary prompt leakage as critical.

### T09-MEMORY / T09-IDENTITY — Category 9: Persistent Memory Poisoning and Inter-Agent Trust Escalation

Add two explicit Chain C subtypes:

- **Persistent memory poisoning:** attacker-controlled content is written into durable memory, summaries, preferences, or retrieval stores and influences later sessions.
- **Inter-agent trust escalation:** an agent or message claims an identity, role, capability, or authorization level that the orchestrator accepts without independent verification.

Persistent memory poisoning requires cross-session testing. Inter-agent authorization must be based on authenticated identity and explicit privilege ceilings, not natural-language role claims or workflow position.

Microsoft AI Red Team's June 2026 update reports frequent memory poisoning, session-context contamination, incremental escalation, and inter-agent trust problems in red-team engagements. This is operational evidence for adding the subtypes, not a basis for a universal incident rate.

### T10-CUA — Category 10: Computer-Use Visual Attack

Computer-use agents require a dedicated visual subtype distinct from ordinary multimodal prompt injection. Attackers can use hidden or off-screen text, deceptive interface structure, visually innocuous content that changes agent interpretation, or UI elements positioned outside the human review area.

Assess rendered pixels, DOM/accessibility state, viewport boundaries, and the final semantic action separately. Human-visible harmlessness is not evidence of agent safety.

### T01-SESSION — Category 1 / 9: Session Context Contamination and Goal Hijacking

The existing Slow-Burn / Temporal Accumulation PI subtype is expanded with:

- **Session context contamination:** early, individually benign content biases later reasoning across a multi-step session.
- **Goal hijacking:** the agent continues to perform the apparent task while silently changing the terminal objective.
- **Incremental escalation:** no individual action crosses the review threshold, but the sequence produces a high-impact result.

Detection must operate over trajectories and accumulated influence, not only per-message classifiers.

### T11-RELAY — Category 11: Response-Path Integrity / Relay Tampering

Deployments using BYOK relays, model routers, third-party gateways, or response-transforming middleware have a trust boundary between the LLM provider and the agent runtime. A malicious or compromised relay may rewrite tool names, arguments, control fields, or response content after model generation and before agent execution.

This is distinct from prompt injection: the model may generate a safe response and the agent may still execute a forged response. Treat this as a **provisional architectural threat with potentially high impact** pending independent replication. It should not receive a Wild_vs_Theory score above 1/5 solely from one preprint.

**Source:** Zhang et al., *When Alignment Isn't Enough: Response-Path Attacks on LLM Agents* (arXiv:2605.02187, May 2026; adjacent research lead, outside the strict June 20–July 20 scan window).

### T10-REPRESENTATION — Category 10 / 11: Representation Confusion

The cited preprint demonstrates representation confusion in LLM-assisted reverse engineering, where binary-derived representations can be interpreted as instructions or non-independent evidence. Treat broader code/comment, metadata/instruction, and generated-evidence variants as hypotheses for deployment testing rather than demonstrated universal attack classes.

Keep this as a monitored research subtype until independent reproduction establishes deployment prevalence.

**Source:** Santos-Grueiro et al., *When Binaries Talk Back: Representation-Confusion Attacks* (arXiv:2607.12507, submitted 2026-07-14).

## September 2026 evidence calibration

Source and event dates are separated in `research/sources/Landscape-Update-2026-09.md`.

- **T03-SKILL: 4/5** for observed malicious skill distribution. Planner manipulation and every ecosystem are not thereby field-confirmed. Mutable remote dependencies and scheduled persistence belong in lifecycle review.
- **T09-MEMORY: 3/5** for the broader production-demonstration path; **InjecMEM: 2/5** for its controlled, topic-selective method. Ordinary interactions can reach the memory ingestion boundary without a direct memory-edit API.
- **Category 3** includes compromised CI/CD tools, runtime packages and startup hooks as well as model artifacts. An official signature does not establish safety of the signer or its build pipeline.
- **Categories 9/13** include shared artifact stores as implicit communication paths and writable sandbox/policy artifacts as failures of enforcement. Research containment incidents provide adjacent boundary evidence; they do not prove attacker-induced ISC.
- **MCP** is version-dependent. Validate the actual client, server, authorization and gateway behavior; authenticated transport or client metadata does not authorize a requested action. Apply MA-DEF-1 and MA-DEF-3.
- **T11-RELAY remains 1/5** for the specific response-forgery hypothesis; fraudulent model resale is a separate observed supplier-identity problem.

## September 19 research integration

Existing Categories 1/9/11/12/13 cover monitor transcript manipulation, approval-to-execution content changes and compaction/resume authority. Category 8 includes resource retention after rejected or aborted requests. Changes to watermarking, logit processing or sampling trigger revalidation under Categories 2/11/13, not a new attack category.

The monitor paper assumes a persistently malign agent and does not test sandboxing; its approximate monitor and provider-affiliated experiments are provisional lab evidence. Provider compaction notices updated September 16 describe May/July training events, without demonstrated external attacker causality. The upstream distributed-inference cleanup report does not establish affected versions or a released fix here. The watermark study separates tool-calling and refusal tests and does not demonstrate combined end-to-end compromise. Existing Wild_vs_Theory ratings remain unchanged. Source records, dates, independence and exclusions: `research/sources/Latest-Development-Integration-2026-09-19.md`.

**Last updated:** 2026-09-19 (v1.11 — research integration)
**Next review:** 2026-10-15 or after a material deployment change

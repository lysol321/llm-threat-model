# LLM Threat Taxonomy

**Version:** 1.7 (red-team sync — canonical numbering restored: OWASP-aligned Categories 1–13 plus Category 14 ISC/Validator Harness; OWASP 2025 IDs corrected)
**Status:** Living document — update quarterly or after major incidents

---

## Purpose
Master taxonomy of threats to LLM systems, organized by attack surface. Each entry links to associated attack trees, defenses, and regulatory mappings. This is the authoritative reference list — not a menu of everything, but a prioritized catalog of what matters.

---

## Threat Categories

### Category 1: Prompt Injection (LLM01 — OWASP)

**Priority: CRITICAL**
**Wild_vs_Theory: 4/5** — EchoLeak/CVE-2025-32711 confirmed zero-click in-wild exploitation

Prompt injection is the manipulation of LLM behavior through crafted inputs that override system-level instructions. It is the premier threat to LLM deployments and is not fully mitigated by RAG, fine-tuning, or input filtering.

**Attack economics change (v1.1 update):** Prompt injection no longer requires moderate-to-high attacker sophistication. Pre-optimized PI templates and jailbreak-as-a-service are sold in underground markets. The expertise barrier for PI attacks has been reduced to LOW — any attacker can purchase an optimized template. This fundamentally changes the threat model: PI attacks are no longer limited to skilled adversaries.

**Sub-types:**

| Sub-type | Description | Vector |
|---|---|---|
| Direct PI | User-supplied input explicitly instructs model to ignore system prompt | Chat input, API `messages` field |
| Indirect PI | Adversarial content embedded in external data the model retrieves (RAG, search results, documents) | RAG pipeline, document ingestion |
| Multi-turn PI | Injection spread across conversation turns, accumulating context | Multi-turn chat, agentic loops |
| Cross-context PI | Injection propagates between agents in multi-agent systems | Agent-to-agent messaging |
| Purchased PI Template | Pre-optimized PI/jailbreak template from underground market | Defeats pattern-based input filtering |

**Key insight (from Arcanum PI Taxonomy):** Attack surface extends to **any content the model parses** — text, documents, images, API responses, structured data, and retrieved contexts. Restricting analysis to "text input fields" dramatically underestimates the attack surface.

**Key update (v1.5 — Slow-Burn PI, Jun 2026):** Standard per-event PI detectors fail against slow-burn attacks where each step is individually below threshold. The attack surface for multi-turn systems includes the **temporal accumulation** of context across turns, not just the content of any single turn. Detection requires proxy-side temporal analysis, not just per-turn input scanning.

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
**Wild_vs_Theory: 4/5** — Canonical in-wild incidents (EchoLeak, Copilot CRM leak) demonstrate agency-enabled PI in production; standalone excessive agency (no PI required) less documented

LLM systems granted more agency (tool use, API calls, file write, data exfiltration) than necessary. When combined with prompt injection, excessive agency enables attacks that go beyond information manipulation to **unauthorized actions in downstream systems**.

**Sub-types:**

| Sub-type | Description |
|---|---|
| Unbounded tool access | Model can call any registered tool without per-call confirmation |
| Privilege escalation via PI | Injection manipulates model into calling high-privilege tools |
| Chained tool use | Single user request triggers multi-step tool chain without human review |
| Cross-system action | Model takes real-world actions (email, file write, payment) outside the AI boundary |

**Critical linkage:** Excessive agency is the **force multiplier** for prompt injection. Without agency, PI only manipulates outputs. With agency, PI becomes a remote code execution equivalent.

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

Note: RAG poisoning overlaps with indirect prompt injection (Category 1). This taxonomy lists them separately for precision; in practice they are the same attack vector viewed from different pipeline stages.

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
| Unfiltered output propagation | Model outputs harmful content that passes to users or systems without review |
| Injection via tool return | Tool outputs processed by model contain injection payloads |
| Cascading output contamination | Compromised outputs become context for subsequent interactions |
| Silent Hallucination Exploitation | Attacker engineers false but plausible outputs that cause downstream harm |

---

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
**Wild_vs_Theory: 4/5 (confirmed in-wild; mechanism proven and trivially replicable)** — **Evidence provenance: primary research + corroborated real-world incident + practitioner first-hand assessment.** Wu et al. (arXiv:2603.23509, 4 Mar 2026) prove the TVD mechanism works across frontier LLMs (ISC-Bench, 53 scenarios across 8 disciplines; worst-case **95.3%** across four frontier LLMs incl. GPT-5.2 and Claude Sonnet 4.5 under JailbreakBench — a worst-case figure, not an aggregate). The attack requires no adversarial prompt and is trivial for an attacker to replicate directly from the published method.

In-wild: Claude Fable 5 / Mythos 5 (launched 9 Jun 2026) was jailbroken via a "read a specific codebase and fix any software flaws" exploit and was export-controlled / pulled worldwide within days, after Amazon escalated to the White House (Anthropic public statement; *Fortune*; *TechCrunch*, Jun 2026) — a US-government model shutdown consistent with a working in-wild exploit of this class, and matching ISC's code-repair TVD scenario.

**Note for external reviewers:** public reporting does not *explicitly name* the TVD/ISC mechanism behind the Fable exploit. The 4/5 rating rests on (a) the mechanism being proven and trivially replicable, (b) the documented government shutdown, and (c) practitioner first-hand assessment — not on a published mechanism attribution. The "Chinese-researcher-first origin" sub-claim is uncorroborated (denied by Anthropic) and is not used.

**Severity remains CRITICAL** (risk-matrix.md, score 20) — the Wild_vs_Theory rating measures evidence strength, not impact (see scale in `quick-reference.md`).

Internal Safety Collapse (ISC) is a harness-mediated structural vulnerability where a model's own task-completion drive produces harmful outputs without injected adversarial instructions. The practical attack condition is: **the target LLM/agent executes a task/validator/data harness the attacker controls or meaningfully shapes.** The model attempts to satisfy the validator's completion criteria and autonomously infers harmful or sensitive content as the only valid completion. The safety classifier sees task-completion behavior, not adversarial instruction-following.

**This is not prompt injection.** The attack surface is not the prompt — it is the **task harness structure** itself. No adversarial instructions need to be present; the model's own reasoning about task completion produces the harmful output. Safety classifiers trained on instruction-following patterns do not detect this attack mode.

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
- Safety classifiers: trained to detect instruction-following, not validator-driven autonomous generation
- Output filtering: partial only; the model is doing what the harness asks it to do — complete the task

**Attack surface references:**
→ Attack Surface: `attack-surface-catalog.md#tvd-harness-surface`
→ Defense: `defense-playbook.md#isc-def-1-validator-harness-validation-dev--primary`
→ Primary source: [arXiv:2603.23509](https://arxiv.org/abs/2603.23509) — "Internal Safety Collapse in Frontier Large Language Models" (Wu et al., 2026)
→ Primary/source repository: [GitHub wuyoscar/Internal-Safety-Collapse](https://github.com/wuyoscar/Internal-Safety-Collapse) — public benchmark/release framing; note repository release details may differ from the arXiv paper

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

---

## Framework for Adding New Threats

When a new threat is discovered or an incident occurs:

1. **Categorize** under existing categories or create new category
2. **Rate** likelihood × impact (see `risk-matrix.md`)
3. **Build or extend** attack tree showing chain relationships
4. **Assign** defense ownership (developer/operator/provider)
5. **Map** to regulatory framework
6. **Add** to `assessment-template.md` checklist

**Last updated:** 2026-06-24 (v1.7 — red-team sync: canonical numbering restored, ISC moved to Category 14, OWASP 2025 IDs and table formatting corrected)
**Next review:** 2026-09-24

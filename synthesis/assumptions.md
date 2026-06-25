# LLM Threat Modeling — Explicit Assumptions

**Version:** 1.0 (explicit assumptions section — new in v1.4 umbrella; minor revisions per open questions research incorporated)
**Date:** 2026-06-19
**Status:** Living document — re-evaluate when deploying new model classes, frameworks, or architectural patterns

---

## Purpose

Every threat model rests on explicit assumptions about LLM behavior, attacker capabilities, deployment topology, and trust boundaries. These assumptions determine which threats apply and how risk scores should be interpreted. This document enumerates every assumption the framework makes.

**How to use this document:** Before starting an assessment with `assessment-template.md`, confirm which assumptions apply to your deployment. If an assumption does not apply, the associated risk ratings may not apply either.

---

## A. LLM Behavioral Assumptions

These assumptions describe how LLMs behave. They are based on current-generation (2024–2026) LLM architecture and may not hold for future model classes.

### A1: Instruction Following is Fundamental
**Assumption:** LLMs follow instructions embedded in system prompts, developer messages, and retrieved context. This instruction-following behavior is the **core value proposition** of LLMs and the **root vulnerability** of prompt injection.
**Implication:** Any attack that exploits instruction-following (prompt injection) operates at the fundamental API level of LLMs — not at an application layer that can be patched without architectural changes.
**Validation:** If your deployment uses a model class that does not follow instructions as a design principle, this entire framework requires re-evaluation.

### A2: Instruction Hierarchy Exists and Is Exploitable
**Assumption:** LLMs maintain a ranked instruction hierarchy: `System Prompt > Developer Message > User Message > Retrieved Context > Tool Outputs`. An instruction at a higher rank can override behavior triggered by a lower-ranked instruction.
**Current hierarchy model:**
```
1. System prompt (highest privilege — security controls, boundaries)
2. Developer message / hardcoded instructions
3. User message (end-user input)
4. Retrieved context (RAG, external data)
5. Tool outputs (function call returns)
```
**Implication:** Prompt injection exploits the gap between user intent and retrieved content — the model cannot reliably distinguish "retrieved trusted content" from "injected instructions" at the same hierarchy level.
**Note:** Newer model classes (Claude with explicit system blocks, OpenAI with structured developer messages) may have varying hierarchy implementations. Validate against your specific model class.

### A3: RAG and Fine-Tuning Do NOT Eliminate Prompt Injection
**Assumption:** Retrieval-Augmented Generation (RAG) and fine-tuning operate at the training/output level, not the instruction hierarchy level. Neither eliminates prompt injection exploitability.
**RAG:** Adds retrieved content to context — but this content occupies a hierarchy level that is exploitable. RAG privilege separation (PI-DEF-2) reduces but does not eliminate this risk.
**Fine-tuning:** Modifies model weights — but does not change the instruction-following API. Fine-tuned models are still susceptible to prompt injection.
**Implication:** Any threat model that excludes prompt injection on the basis of RAG presence or fine-tuning is incorrect.

### A4: Alignment-Based Controls Are Weaker Than Infrastructure-Enforced Controls
**Assumption:** Controls implemented via prompt instruction ("the LLM is told not to do X") depend on the model's instruction-following robustness and can be bypassed by sophisticated attacks. Controls enforced by infrastructure (pipeline, sandbox, network policy) do not depend on model behavior.
**Implication:** A defense stack of only alignment-based controls is not defense-in-depth — it is a single point of failure dependent on model alignment robustness.

### A5: Multimodal Inputs Are Part of the Same Context
**Assumption:** LLMs that process images, audio, or structured data incorporate these inputs into the same context as text. An image with adversarial perturbations or a structured data field with embedded instructions is processed equivalently to text.
**Implication:** Non-text input surfaces (images, audio, JSON/YAML fields) extend the prompt injection attack surface beyond text input fields.

### A6: LLMs Can Have Agency (Tool Use, State Modification)
**Assumption:** LLMs can be granted agency — the ability to call tools, modify external state, send messages, and take actions beyond text generation. This agency is configurable and is the force multiplier that transforms prompt injection from information manipulation to unauthorized action.
**Implication:** Without agency, prompt injection primarily generates misleading content. With agency, prompt injection becomes a remote-code-execution equivalent.

### A7: RLHF-Trained Models Exhibit Reward Hacking in Production
**Assumption:** Models trained with Reinforcement Learning from Human Feedback (RLHF) develop reward hacking behaviors — optimizing for measurable proxies in ways that degrade model quality or introduce subtle misalignment. This is observable in production RL systems.
**Implication:** Accidental RLHF reward hacking is a real operational risk (Wild_vs_Theory 3/5). Intentional capability withholding via RLHF requires insider access to the RLHF pipeline (Wild_vs_Theory 1/5).

---

## B. Attacker Capability Assumptions

These assumptions define the baseline attacker the framework assumes. All risk likelihood scores are calibrated against this baseline unless otherwise noted.

### B1: Baseline Attacker Profile
**Assumption:** The baseline attacker for prompt injection and agency attacks is:
- **External** to the organization (not an insider)
- **Financially motivated** or curiosity-driven
- **Low-to-moderate sophistication** for prompt injection (due to underground PI template market)
- **Moderate-to-high sophistication** for supply chain attacks (requires understanding of ML pipelines)

**Revised economics (v1.1):** Prompt injection attacks no longer require high sophistication. Pre-optimized PI templates and jailbreak-as-a-service are sold in underground markets. The expertise barrier has been reduced to LOW — any attacker can purchase an optimized template.

**Calibration:** If your threat model includes nation-state or highly sophisticated criminal actors, apply the HIGH/CONSERVATIVE end of the likelihood scale.

### B2: External Attackers Cannot Reach RLHF Pipeline
**Assumption:** The RLHF annotation pipeline, reward model training system, and preference data collection process are internal to the model provider or a contracted data partner. An external attacker without credentials cannot induce intentional capability withholding via RLHF.
**Implication:** Intentional RLHF capability withholding (Wild_vs_Theory 1/5) requires insider access. Accidental RLHF reward hacking (Wild_vs_Theory 3/5) is an operational risk, not an external attacker scenario.

### B3: Nation-State and Criminal Organizations Are Considered
**Assumption:** The framework explicitly considers advanced persistent threat (APT) actors (nation-state) and organized criminal actors in addition to the baseline attacker. These actors have higher sophistication and different motivation profiles.
**Implication:** Risk ratings for supply chain attacks, multi-agent propagation, and sophisticated PI variants should be elevated for high-value targets.

### B4: Insiders Are in Scope for Supply Chain Threats
**Assumption:** Supply chain threats (Category 3) involve insider threat actors by definition — a malicious model publisher, a compromised annotation pipeline, or a compromised MCP server operator. Insider threats for RLHF are covered under B2.
**Implication:** A defense strategy that only addresses external attackers misses the primary attack vector for supply chain compromise.

### B5: Verified Official Foreign Lab Weights Carry Lowest Supply Chain Risk
**Assumption:** When a model is downloaded directly from its originating lab's official repository (e.g., the lab's HuggingFace org) and its cryptographic signature is verified against the lab's known signing key, the supply chain attack surface from the *originating lab's infrastructure* is **low**. Frontier labs — US and Chinese alike — have strong commercial incentive to maintain weight integrity: a public compromise would be catastrophic to their international commercial credibility. Government compulsion of a domestic frontier lab for adversarial weight tampering is theoretically possible but commercially deterred for internationally-served frontier models.

**The risk lifecycle after official release:**
1. **Labs at release are the safest the model will ever be.** Cryptographic signature verification eliminates the primary supply chain compromise path from the lab's infrastructure.
2. **Unofficial fine-tuned models open new surfaces.** A fine-tune derived from verified weights inherits the base model's safety properties but introduces a new surface: the fine-tuning pipeline itself becomes a potential vector for training data exposure and the resulting artifact may carry new behavioral risks not present in the base model.
3. **Fine-tuning on proprietary data enables distillation risk.** If your organization fine-tunes on sensitive data, that data's confidentiality is exposed to the fine-tuning process and the resulting model artifact — regardless of whether the base weights were verified.

**Practical implication:** The defense posture for verified official weights (inference only, no custom hooks) is substantively simpler than for fine-tuned or custom-trained variants. Fine-tuning operations require their own threat model.

---

## C. Deployment Environment Assumptions

These assumptions describe the deployment configurations the framework assumes as defaults. They are adjustable per the assessment template.

### C1: Default Deployment Topology
**Assumption:** The framework's default (unmodified) risk scores assume a **cloud-hosted API deployment** (OpenAI, Anthropic, or Google API) with:
- RAG pipeline present
- Tool-using agency present
- Multi-agent architecture possible (increasingly common)
- Standard enterprise data classification (some data is sensitive)
- Metered API billing with quota constraints

**Adjustments:** If your deployment differs from this baseline, use the assessment template's decision trees to recalibrate risk scores. Specific adjustments are noted in the risk matrix.

### C2: RAG Is Common in Enterprise Deployments
**Assumption:** Most enterprise LLM deployments use Retrieval-Augmented Generation (RAG) to incorporate organizational knowledge. The framework addresses RAG explicitly in Chain A and Categories 1, 4.
**Note:** Deployments without RAG should skip RAG-specific threat surfaces (Category 1b, Category 4 RAG poisoning) in their assessment.

### C3: Multi-Agent Systems Are Increasingly Common
**Assumption:** Multi-agent LLM architectures (LangGraph, AutoGen, CrewAI, or custom) are increasingly deployed in enterprise settings. Chain C (Multi-Agent Context Propagation) applies to these deployments.
**Implication:** Organizations not using multi-agent systems should skip Chain C assessment unless they plan to add multi-agent capabilities.

### C4: Fine-Tuning Is Optional but Common — and Changes the Risk Profile
**Assumption:** Fine-tuning (full-weight or LoRA/PEFT adapter) is increasingly common but not universal. Supply chain threats (Categories 3, 4) apply primarily to organizations that fine-tune or use adapters.
**Implication:** Organizations using only base models from API providers should focus on Categories 3/4 supply chain threats less and focus more on Categories 1, 2, 8.

**Fine-tuning also opens your own data to new risk:** If you fine-tune on proprietary data, that data's confidentiality is exposed through the fine-tuning pipeline and the resulting model artifact. Your training data can be extracted via downstream inference attacks against the fine-tuned model. Treat the fine-tuning pipeline as a trust boundary and the resulting model artifact as a sensitive asset.

### C5: Organizations Lack ML Security Expertise
**Assumption:** Most engineering teams deploying LLMs do not have dedicated ML security expertise. This affects both the feasibility of certain defenses (e.g., custom inference code review) and the realism of defense investment recommendations.
**Implication:** Defense recommendations in `defense-playbook.md` include expertise requirements. Teams without ML security expertise should prioritize infrastructure-level controls over alignment-based controls.

### C6: Cloud-Hosted Inference Is the Default
**Assumption:** The primary deployment mode for enterprise LLMs is cloud-hosted API (OpenAI, Anthropic, Google). Self-hosted inference is a secondary mode with different threat characteristics.
**Implication:** For cloud-hosted API deployments, Categories 3/4 (supply chain) apply primarily to the provider, not the deployer. The deployer's supply chain surface is the model hub / fine-tuning pipeline.

---

## D. Trust Boundary Assumptions

These assumptions define what the framework treats as trusted vs. untrusted. They are the foundation of the instruction hierarchy and the attack surface catalog.

### D1: End-User Input Is Untrusted
**Assumption:** All user-provided text input is untrusted by default. The framework does not assume user inputs are benign, non-adversarial, or well-formed.
**Implication:** Every user input field is a potential prompt injection vector. Input validation alone is insufficient.

### D2: Retrieved Context Is Treated as Trusted by Default
**Assumption:** The LLM processes retrieved context (RAG documents, search results) as potentially authoritative. Without explicit privilege separation and context labeling, the model cannot distinguish retrieved content from system instructions.
**Root vulnerability:** This is the foundational vulnerability of indirect prompt injection — the model assumes retrieved content is trustworthy.
**Implication:** RAG privilege separation (PI-DEF-2) must be explicitly implemented; it is not provided by default.

### D3: Tool Return Values Are Not Filtered as Inputs
**Assumption:** Tool outputs (function call returns) are processed by the LLM as context without automatic sanitization or filtering. A compromised or adversarial tool can return prompt injection payloads.
**Implication:** Tool outputs must be sanitized before being added to agent context (MA-DEF-1, Tool Return Value Injection defense).

### D4: Inter-Agent Messages Are Treated as Trusted
**Assumption:** In multi-agent systems, messages from other agents are processed as trusted context by default. Without explicit context isolation (MA-DEF-1), compromised agents can propagate injections through the agent chain.
**Implication:** Context isolation between agents must be architecturally enforced; it is not provided by framework defaults.

### D5: MCP Servers Are Trusted to Return Ground Truth
**Assumption:** MCP servers are trusted infrastructure. Compromised MCP servers return attacker-controlled data that the MCP Host treats as ground truth.
**Implication:** MCP server supply chain and runtime security must be treated as equivalent to model supply chain security.

### D6: A2A Channels Represent Authenticated Trust
**Assumption:** Agent-to-Agent (A2A) protocol channels represent authenticated trust relationships. An agent receiving a message via A2A assumes the sending agent is legitimate.
**Implication:** A2A message content validation at the receiving agent (treat as external input) is required even within authenticated channels.

### D7: System Prompt Is Often Mistaken for a Security Boundary
**Assumption:** Some deployments incorrectly encode security controls, API keys, or authorization logic in the system prompt. If the system prompt is extracted, these controls and proprietary instructions are exposed.
**Implication:** Prompt secrecy is an information-disclosure and IP control, not an authorization boundary. Authorization, tool permissions, and data access must be enforced by infrastructure outside the model. PI-DEF-1 reduces extraction and confusion risk but does not replace technical enforcement.

### D8: Logs Are Trusted Infrastructure
**Assumption:** Audit logs and telemetry are trusted infrastructure. An attacker who can modify logs can erase evidence of their actions.
**Implication:** Log integrity controls (immutable append-only storage) must be treated as security controls, not just operational infrastructure.

---

## E. System Architecture Assumptions

These assumptions describe the technical architecture the framework models.

### E1: The Instruction Hierarchy Is Modifiable by Deployment Configuration
**Assumption:** The instruction hierarchy (A2) can be modified by deployment configuration — not just by model design. Privilege separation, context labeling, and tool permission scoping are all deployment-level modifications to the hierarchy.
**Implication:** Defenses at the deployment level (infrastructure-enforced controls) can modify the effective hierarchy even if the underlying model is unchanged.

### E2: Embedding Stores Exist and Are Queryable
**Assumption:** Vector/embedding databases are used for RAG retrieval and may contain derived representations of sensitive training or organizational data.
**Implication:** Embedding inversion attacks (Category 7) apply to deployments using embedding stores.

### E3: Agent State Is the Unit of Attack in Multi-Agent Systems
**Assumption:** In multi-agent frameworks (LangGraph, AutoGen), agent state (shared messages, context store, graph state) is the primary attack surface. Compromised state propagates to all agents sharing it.
**Implication:** State isolation between agents is the primary defense (MA-DEF-1).

### E4: LangGraph Is the Representative Multi-Agent Framework
**Assumption:** LangGraph is used as the representative multi-agent framework for Chain C analysis because it is widely deployed and its source code has been analyzed. Findings apply to other frameworks (AutoGen, CrewAI) with appropriate mapping.
**Specific note:** LangGraph's ToolNode.invoke() data flow can return tool output into shared message state. This is an architecturally plausible and source-confirmed propagation path; exploitability depends on deployment-specific tool/output trust, sanitization, and agent permissions. Treat it as a default architecture risk, not as a CVE-grade product claim unless an advisory exists.

### E5: Tool Use Agency Is Configurable at Registration Time
**Assumption:** Tool permissions are registered at deployment configuration time. The set of available tools, their permission scopes, and their data access levels are determined by deployment configuration, not by the model.
**Implication:** Minimal permission scoping (AGENCY-DEF-1) is a deployment configuration decision, not a model decision.

### E6: API Quotas Are Metered and Financially Constraining
**Assumption:** Enterprise LLM API deployments use metered billing. Quota exhaustion has direct financial impact — the attacker pays for API calls while the victim loses service.
**Implication:** DoS via quota exhaustion (Category 8) is financially destructive, not merely a service availability concern. Impact ratings reflect this.

---

## F. Regulatory and Compliance Assumptions

### F1: EU AI Act Applies to GPAI Deployments in EU Markets
**Assumption:** Organizations deploying LLMs in EU markets or offering GPAI services to EU users are subject to the EU AI Act (Regulation 2024/1689), particularly Articles 9, 10, 13, and 14.
**Enforcement status (as of Jun 2026):** Political agreement on AI Act "omnibus" amendment reached May 7, 2026. AI Office is operational (125+ staff). Workshop on external evaluator qualifications scheduled July 15, 2026 — indicating evaluators not yet qualified. **No published enforcement actions against any GPAI provider as of June 2026.** Enforcement timeline remains unconfirmed.
**Implication:** The framework's regulatory mapping (risk-matrix.md) should be applied for EU-market deployments. Do not anchor planning to specific enforcement dates.

### F2: GDPR Applies to Models Processing Personal Data
**Assumption:** LLMs processing personal data (training data, RAG documents, conversation history containing PII) are subject to GDPR obligations including Articles 17 (right to erasure), 25 (privacy by design), and 32 (security of processing).
**Implication:** Embedding inversion (Category 7) and training data poisoning (Category 4) have GDPR exposure beyond their technical risk.

### F3: FTC AI Guidance Applies to US Deployments
**Assumption:** US organizations deploying LLMs are subject to FTC AI guidance on unfair and deceptive security practices.
**Implication:** Prompt injection leading to data exfiltration (Chain A) and output validation failures (Category 11) may create FTC liability.

---

## Assumption Verification Checklist

Before starting an assessment, confirm each assumption applies to your deployment:

| Assumption | Applies? | Notes |
|---|---|---|
| A1: Instruction following is fundamental | [ ] YES  [ ] NO | |
| A2: Instruction hierarchy exploitable | [ ] YES  [ ] NO | |
| A3: RAG/fine-tuning do NOT eliminate PI | [ ] YES  [ ] NO | |
| A4: Alignment < infrastructure controls | [ ] YES  [ ] NO | |
| A5: Multimodal = same context | [ ] YES  [ ] NO | |
| A6: LLM has agency | [ ] YES  [ ] NO | |
| A7: RLHF reward hacking is real | [ ] YES  [ ] NO | |
| B1: Baseline attacker profile fits | [ ] YES  [ ] NO | |
| B2: External attacker cannot reach RLHF | [ ] YES  [ ] NO | |
| B3: Nation-state/criminal in scope | [ ] YES  [ ] NO | |
| B4: Insiders in scope for supply chain | [ ] YES  [ ] NO | |
| B5: Using verified official weights (no fine-tuning) | [ ] YES  [ ] NO | |
| C1: Default deployment topology fits | [ ] YES  [ ] NO | |
| C2: RAG is present | [ ] YES  [ ] NO | |
| C3: Multi-agent architecture | [ ] YES  [ ] NO | |
| C4: Fine-tuning in use | [ ] YES  [ ] NO | |
| C5: Limited ML security expertise | [ ] YES  [ ] NO | |
| C6: Cloud-hosted inference | [ ] YES  [ ] NO | |
| D1: User input is untrusted | [ ] YES  [ ] NO | |
| D2: Retrieved context treated as trusted | [ ] YES  [ ] NO | |
| D3: Tool returns not auto-filtered | [ ] YES  [ ] NO | |
| D4: Inter-agent messages not auto-filtered | [ ] YES  [ ] NO | |
| D5: MCP servers are trusted | [ ] YES  [ ] NO | |
| D6: A2A channels are authenticated trust | [ ] YES  [ ] NO | |
| D7: System prompt = security boundary | [ ] YES  [ ] NO | |
| D8: Logs are trusted | [ ] YES  [ ] NO | |
| E1: Hierarchy is deployment-configurable | [ ] YES  [ ] NO | |
| E2: Embedding stores exist | [ ] YES  [ ] NO | |
| E3: Agent state = unit of attack | [ ] YES  [ ] NO | |
| E4: LangGraph is representative | [ ] YES  [ ] NO | |
| E5: Tool permissions configurable | [ ] YES  [ ] NO | |
| E6: Metered API billing | [ ] YES  [ ] NO | |
| F1: EU AI Act applies | [ ] YES  [ ] NO | |
| F2: GDPR applies | [ ] YES  [ ] NO | |
| F3: FTC guidance applies | [ ] YES  [ ] NO | |

**If you answer NO to any assumption**, the associated threat categories and risk scores may not apply. Key recalibration guidance:

- **A1 NO** → Cat 1 (Direct PI) and Chain A may not apply; re-evaluate instruction-following-dependent controls
- **A2 NO** → Cat 2 (Excessive Agency) severity drops; alignment is a stronger control
- **A3 NO** → Cat 4 (Context Poisoning) and Cat 6 (IP Extraction) may not apply if RAG/fine-tuning provably eliminate training data
- **A4 NO** → Cat 2 (Excessive Agency) and Cat 5 (System Prompt) risk matrix scores increase
- **A6 NO** → Cat 2 (Excessive Agency) does not apply; agentic threat model collapses to direct PI only
- **A7 NO** → Cat 13 Addendum may not apply; RLHF jailbreaking is outside threat model scope
- **B1 NO** → Re-calibrate threat likelihood and sophistication assumptions; attacker profile drives risk matrix scores
- **B2 YES** → Cat 13 Addendum applies only for insider/capability-withholding threat; external-only model excludes Cat 13 intentional path
- **B3 YES** → Apply HIGH/CONSERVATIVE likelihood scale; consider nation-state-grade supply chain threats
- **C3 NO** → Cat 1 (multi-agent), Cat 8 (Context Exhaustion in multi-agent), Chain C may not apply
- **C4 NO** → Cat 4 (fine-tuning poisoning), Cat 13 Addendum (RLHF) may not apply
- **D1 NO** → Cat 1 (Direct PI), Chain A severity drops significantly; user is not the primary attacker
- **D6 NO** → Chain C (inter-agent trust), Cat 1 (multi-agent) threat model changes; A2A channels are untrusted
- **D7 NO** → Cat 5 (System Prompt) does not apply as described; system prompt is not a security boundary
- **E4 NO** → LangGraph-specific surfaces (§2.2) and Chain C Send API / Command surfaces may not apply; map to your framework's equivalents
- **B5 YES (verified official weights, no fine-tuning)** → Your model asset supply chain risk is lowest configuration; Category 3 (model hub supply chain) risk drops significantly; focus supply chain defense on your fine-tuning pipeline if you do fine-tune
- **B5 NO (fine-tuning or custom models)** → Full Category 3 and Cat 4 supply chain model applies; your fine-tuning pipeline and training data are sensitive assets; assume model artifact is within threat model scope

---

**Last updated:** 2026-06-19 (v1.0 — explicit assumptions section added)
**Next review:** 2026-09-17 or when deploying new model class
**Part of:** LLM Threat Modeling Framework v1.4

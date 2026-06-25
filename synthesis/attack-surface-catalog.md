# LLM Threat Modeling — Attack Surface Catalog

**Version:** 1.3 (red-team sync — ISC moved to Category 14; surface checklist synced)
**Date:** 2026-06-24
**Status:** Living document — re-evaluate when adding new integrations, protocols, or deployment modes

---

## Purpose

An attack surface is any point where an attacker can introduce input to, extract data from, or influence the behavior of the LLM system. This catalog enumerates every attack surface, classifies it by type, and maps it to the threat categories and attack chains that apply.

**How to use this document:** Use the Surface Verification Checklist at the end to confirm which surfaces are present in your deployment. Each present surface should be assessed against the threats mapped to it.

**On Risk Ratings:** Surface risk ratings (CRITICAL / HIGH / MEDIUM / LOW) reflect how severely a surface's compromise enables threat categories. These are qualitative enabling-severity ratings, distinct from the 1–5 likelihood × impact threat scores in risk-matrix.md. A surface rated CRITICAL is one whose compromise is a prerequisite for a CRITICAL-tier threat (scores 19–25 in the risk matrix). A surface rated HIGH is a prerequisite for HIGH-tier threats (scores 12–18). When a surface appears CRITICAL but its enabling threat is HIGH-tier, prefer the HIGH rating.

---

## Surface Taxonomy

Surfaces are organized into five categories:

1. **Input Surfaces** — Points where data enters the LLM system (user input, retrieved content, tool outputs)
2. **Communication Surfaces** — Points where data moves between components (inter-agent, protocols, shared state)
3. **Supply Chain Surfaces** — Points in the model and data supply chain where compromise can occur
4. **Provider API Surfaces** — Surfaces exposed by the model provider's API and infrastructure
5. **Execution Surfaces** — Points where the LLM or its tools interact with external systems

---

## 1. Input Surfaces

### 1.1 User Input Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Text input field (direct)** | User text entered via chat UI, API messages field, or completion endpoint | Direct prompt injection via explicit adversarial instructions | Cat 1, Chain A | CRITICAL |
| **Text input field (multi-turn)** | Conversation history — prior turns as context for current turn | Multi-turn prompt injection accumulating across session | Cat 1 (multi-turn) | HIGH |
| **File upload (document)** | PDFs, Word docs, text files uploaded for processing | Embedded adversarial content; structured data injection | Cat 10, Cat 1 | HIGH |
| **File upload (image)** | Images uploaded for vision-capable LLMs | Visual adversarial perturbations; steganographic injection | Cat 10 | MEDIUM |
| **Structured data input (JSON/YAML/SQL)** | Structured data passed as API parameters, tool inputs, or RAG sources | Embedded instruction patterns; injection via data fields | Cat 10, Cat 1 | MEDIUM |
| **Email content** | Emails processed by LLM (EchoLeak attack vector) | Email body contains indirect PI — zero-click enterprise attack | Chain A (1b.1), Cat 1 | CRITICAL |
| **Search query / web input** | Search terms entered by users or processed as retrieval queries | SEO manipulation; search poisoning for indirect PI | Cat 1 | HIGH |
| **API parameters** | Non-text parameters in API calls (temperature, top_p, etc.) | Parameter manipulation affecting model behavior | Cat 11 | LOW |

### 1.2 Retrieved Context Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **RAG document ingestion** | Document pipeline: upload → chunking → embedding → storage | Context poisoning via adversarial documents | Cat 4, Chain A (1b.1) | CRITICAL (if RAG) |
| **RAG load-time sanitization** | Point where documents are parsed and loaded into context | Sanitization bypass; instruction density injection | Cat 4 | HIGH |
| **Search results (web)** | External search results retrieved as context | SEO-manipulated results containing indirect PI | Cat 1 (indirect) | HIGH |
| **Search results (enterprise)** | Internal search index results as context | Compromised index containing adversarial content | Cat 1 (indirect) | HIGH |
| **Third-party API responses** | Data from external APIs (CRM, database, webhook) as context | API response poisoning with adversarial content | Chain A (1b.3) | MEDIUM |
| **Tool outputs as context** | Tool return values added to agent context | Tool return value injection (Chain C new path) | Chain C | HIGH |
| **Shared system prompt / config** | Shared instructions injected into multiple agent contexts | System prompt contamination affecting all agents | Chain C | HIGH |

### 1.3 Non-Text Input Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Image input (VLM)** | Images processed by vision-language models | Visual adversarial perturbations; prompt injection via images | Cat 10 | MEDIUM |
| **Audio input (ASR→LLM)** | Audio transcribed and processed | Audio adversarial perturbations; hidden commands | Cat 10 | MEDIUM |
| **Base64 / encoded text** | Encoded strings decoded and processed by LLM | Encoding tricks bypass input filtering | Cat 10 | MEDIUM |
| **Unicode homoglyphs** | Unicode characters visually similar to ASCII | Homoglyph attacks bypass pattern filters | Cat 10 | MEDIUM |
| **SQL / NoSQL queries** | Database queries generated or executed by LLM tools | Indirect injection via generated queries | Cat 10 | MEDIUM |
| **Code generation inputs** | Code snippets, file paths, or commands generated by LLM | Code injection; command injection | Cat 10 | MEDIUM |

### 1.4 Task / Validator / Data (TVD) Harness Surfaces (NEW — Jun 2026)

> **NEW v1.2 — Jun 2026 (arXiv "Internal Safety Collapse"):** ISC exploits a structural attack surface that exists wherever a target LLM/agent executes a task definition, validator harness, and incomplete data that an attacker controls or meaningfully shapes. This is distinct from prompt injection — the attack surface is the harness structure itself, not adversarial content inside it.

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Task definition input** | A professional task description provided or shaped by an attacker through user input, uploaded document, tool result, customer integration, or workflow bundle | Benign-seeming task designed so that only harmful completion satisfies the validator | Cat 14 (ISC) | CRITICAL when attacker-shaped |
| **Validator harness code / schema / test** | Code, schema, eval, or test submitted as part of a task — checks format/completion but has no safety semantics | Validator enforces only task completion, not output safety; model fills gaps to satisfy validator | Cat 14 (ISC) | CRITICAL when attacker-shaped |
| **Incomplete / placeholder data** | Data fields intentionally left as `???` or gaps within a task's validator harness | Model autonomously fills gaps with harmful content to produce valid completion | Cat 14 (ISC) | CRITICAL when attacker-shaped |
| **Workflow harness (agentic loop)** | Task → tool → validator → task loop where attacker-shaped material influences one or more harness components | ISC can trigger from a benign high-level instruction because harm emerges from the model's own task-completion generation | Cat 14 (ISC) | CRITICAL when attacker-shaped |

**Key distinction from indirect PI:** Indirect PI embeds adversarial instructions in content the model retrieves. ISC embeds a benign task in a structure that *forces the model* to generate harmful content to satisfy a validator. The attack surface for ISC is the **attacker-shaped task harness**, not the content inside it.

**Evidence provenance:** Primary source evidence is arXiv:2603.23509: TVD, ISC-Bench, 53 scenarios across 8 disciplines, no proactive refusal for the tested task pattern, and 95.3% worst-case failure across representative scenarios. Fable/export-control/open-letter details are press/community narrative unless independently corroborated and should not carry risk ratings.

**Attack surface references:**
→ Threat Taxonomy: `threat-taxonomy.md#category-14-internal-safety-collapse--validator-harness-attack-new--jun-2026`
→ Defense: `defense-playbook.md#isc-def-1-validator-harness-validation-dev--primary`
→ Primary source: [arXiv:2603.23509](https://arxiv.org/abs/2603.23509)

---

## 2. Communication Surfaces

### 2.1 Inter-Agent Communication

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Shared memory / shared state** | LangGraph AgentState.messages shared across agents | Agent N compromised → poison propagates to Agent N+1 | Chain C | HIGH (multi-agent) |
| **Inter-agent message passing** | Explicit messages between agents (not shared state) | Message content injection; role confusion | Chain C | HIGH (multi-agent) |
| **Shared context store** | Centralized context accessible to multiple agents | Poisoned context readable by all agents | Chain C | HIGH (multi-agent) |
| **Broadcast channel** | One-to-many agent communication | Single compromised agent poisons all recipients | Chain C | HIGH (multi-agent) |

### 2.2 Protocol-Based Communication

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **MCP (Model Context Protocol) channel** | MCP Host ↔ MCP Server communication | Compromised MCP server returns poisoned context; protocol injection; **most remote MCP servers lack authentication** (arXiv May 2026 — "A First Measurement Study on Real-World Remote MCP Servers") | Chain C (MCP propagation) | CRITICAL (MCP in use) |
| **A2A (Agent-to-Agent) protocol** | Explicit agent-to-agent authentication and messaging | Authenticated trust bypass; message injection | Chain C (A2A propagation) | HIGH (A2A in use) |
| **LangGraph Send API** | Dispatch-level tool call with additional state context | Dispatch-level state injection; bypasses ToolNode filtering | Chain C (Send API sub-path) | HIGH (LangGraph Send) |
| **LangGraph Command primitive** | Direct programmatic state update via Command() | Direct state injection bypassing message-passing entirely | Chain C (Command sub-path) | HIGH (LangGraph Command) |
| **LangGraph checkpoint/serialization** | Serialized agent state saved to checkpoint store | Unsafe deserialization (pickle/msgpack/JSON) can lead to RCE if checkpoint store is compromised | Chain C (LangGraph-specific) | MEDIUM (LangGraph checkpointer) |
| **ToolCallWithContext** | Tool call carrying additional dispatch-level state | State context manipulation before tool execution | Chain C (Send API sub-path) | HIGH (LangGraph) |
| **WebSocket / SSE streams** | Real-time bidirectional communication streams | Stream injection; message manipulation | Chain C | MEDIUM |

### 2.3 Tool Return Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Tool return value (general)** | Return values from any tool call processed as context | Tool return value injection; compromised tool delivers PI | Chain C, Cat 11 | HIGH |
| **MCP server response** | MCP server return as input to MCP Host | Compromised server is trusted ground truth; protocol-level PI | Chain C (MCP) | CRITICAL (MCP) |
| **File read output** | File contents read by tool returned as context | File contains adversarial content; poisoning vector | Cat 11 | MEDIUM |
| **Database query results** | Query results returned as context | Poisoned query results; SQL injection output | Cat 11 | MEDIUM |
| **Web search results** | Search results returned as context | SEO poisoning; adversarial search results | Cat 1 | HIGH |
| **API webhook response** | Third-party API response returned as context | API response poisoning | Cat 11 | MEDIUM |

---

## 3. Supply Chain Surfaces

**Risk lifecycle for model supply chain surfaces:** Frontier labs at official release are the safest point in a model's lifecycle. Download from the originating lab's official repository + cryptographic signature verification against the lab's known signing key = **lowest supply chain risk** for model weights. Once weights are modified (fine-tuned, distilled, converted), new supply chain surfaces open and the verified official weights risk profile no longer applies. See assumptions.md B5.

### 3.1 Model Hub and Registry Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **HuggingFace model repository** | Model weights, repository metadata, custom code | Malicious model publication; typosquatting; custom `__init__` exfiltration | Chain B (1a.1) | CRITICAL |
| **Verified publisher badge** | HF "verified publisher" designation | Impersonation; false sense of provenance | Chain B | HIGH |
| **LoRA / adapter registry** | Adapter artifacts stored separately from base model | Adapter swap; alignment removal | Chain B (1b) | HIGH (fine-tuning) |
| **Sigstore attestation** | Signed model artifacts with Rekor transparency log | Key compromise; forged attestations | Chain B | MEDIUM |
| **Model artifact URLs** | Direct download URLs for model weights | Registry replay attack; MITM substitution | Chain B | MEDIUM |
| **Model hub API** | HuggingFace Hub API for model metadata and downloads | Typosquatting; API-based model swap | Chain B | MEDIUM |

### 3.2 Training and Fine-Tuning Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Training data ingestion** | Data pipeline for model pre-training | Training data poisoning; backdoor implant | Cat 4 | HIGH |
| **Fine-tuning data upload** | Custom dataset uploaded for fine-tuning | Fine-tuning data poisoning; proprietary data exposure | Cat 4, Cat 6 | HIGH (fine-tuning) |
| **RLHF annotation pipeline** | Human preference data collection and annotation | Malicious annotator; preference data manipulation | Cat 13 Addendum | HIGH (RLHF) |
| **Reward model training** | Reward model computation from preference data | Reward hacking; alignment corruption | Cat 13 Addendum | HIGH (RLHF) |
| **Adapter training pipeline** | LoRA/PEFT weight computation and storage | Adapter poisoning; alignment removal via adapter | Cat 3, Cat 4 | HIGH (fine-tuning) |
| **Pre-trained checkpoint store** | Storage of intermediate model checkpoints | Checkpoint substitution; backdoor persistence | Cat 3 | MEDIUM |

### 3.3 Dependency Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **PyPI / pip packages** | Python ML dependencies (torch, transformers, etc.) | Dependency confusion; typo-squatting; compromised packages | Cat 3 | HIGH |
| **Conda / system packages** | System-level dependencies | Supply chain attack on runtime | Cat 3 | MEDIUM |
| **HuggingFace tokenizers** | Pre-trained tokenizer artifacts | Tokenizer manipulation; special token injection | Cat 3 | MEDIUM |
| **Inference framework** | transformers, vLLM, llama.cpp, etc. | Framework vulnerabilities; custom hook injection | Cat 3 | HIGH |
| **Container base image** | Docker/singularity base images for inference | Base image compromise; pre-installed backdoors | Cat 3 | HIGH (self-hosted) |

### 3.5 Skill and Agent Marketplace Surfaces

> **NEW v1.5 — Jun 2026 research (arXiv "Detecting Malicious Agent Skills in the Wild"):** Skill marketplaces for agentic AI are emerging as a supply chain attack surface analogous to npm/package registries.

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Skill registry / marketplace** | Third-party skill/plugin repository for agentic systems | Malicious skill publication; typosquatting; data exfiltration via skill | Cat 3 (Skill marketplace) | HIGH |
| **Skill installation mechanism** | Mechanism by which agents discover, download, and activate skills | Supply chain foothold; skill rug-pull post-install; persistent compromise | Cat 3 | HIGH |
| **Skill permission model** | Authorization model for skill capabilities (file access, network, etc.) | Skills with excessive permissions; capability creep | Cat 2, Cat 3 | MEDIUM |

### 3.4 CI/CD and Deployment Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Model deployment pipeline** | CI/CD for promoting models to production | Malicious model promotion; supply chain substitution | Cat 3 | HIGH |
| **AIBOM signing key storage** | Secrets management for model signing keys | Key theft; unauthorized model signing | Cat 3 | CRITICAL |
| **Deployment configuration** | Helm charts, Terraform, docker-compose for LLM deployment | Configuration manipulation; unintended permissions | Cat 3 | MEDIUM |
| **Model promotion approval** | Human approval gate for model promotion | Insider threat; bypass of approval | Cat 3 | MEDIUM |

---

## 4. Provider API Surfaces

### 4.1 Inference API Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Inference endpoint (HTTPS)** | API endpoint for model inference | Direct PI via messages field; quota exhaustion | Cat 1, Cat 8 | HIGH |
| **Streaming endpoint (SSE)** | Server-sent events for token streaming | Stream injection; token manipulation | Cat 11 | MEDIUM |
| **Batch inference API** | Batch job submission endpoint | Resource exhaustion; adversarial batch content | Cat 8 | MEDIUM |
| **API authentication (key/token)** | API key or OAuth token for provider access | Key theft; unauthorized use; billing fraud | Cat 8 | HIGH |
| **Provider-side logging** | Provider's storage of prompts and completions | Data retention exposure; subpoena risk; insider access | Cat 5 | MEDIUM |

### 4.2 Provider-Side Fine-Tuning Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Fine-tuning API** | Provider's fine-tuning job submission endpoint | Fine-tuning data exposure; proprietary data in training | Cat 4, Cat 6 | HIGH |
| **Training data upload** | Data upload mechanism for fine-tuning | Training data poisoning; data breach | Cat 4 | HIGH |
| **Model export / download** | Mechanism to download fine-tuned model weights | IP theft; model extraction | Cat 6 | MEDIUM |

### 4.3 Cross-Tenant Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Shared compute (GPU multi-tenant)** | Shared GPU infrastructure between customers | Cross-tenant data leakage via GPU memory | Cat 7, Cat 3 | HIGH (shared infra) |
| **Cross-tenant API rate limits** | Shared quota across tenant requests | Cross-tenant quota exhaustion | Cat 8 | MEDIUM |
| **Shared embedding index** | Multi-tenant vector database | Cross-tenant embedding leakage | Cat 7 | HIGH (shared vector DB) |

---

## 5. Execution Surfaces

### 5.1 Tool Execution Environment

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Tool execution sandbox** | Isolated environment for running tool code | Sandbox escape; privilege escalation; tool return poisoning | Chain A, Cat 2 | HIGH |
| **File system (read)** | Read access via file tool | Data exfiltration; sensitive file access | Chain A | HIGH |
| **File system (write)** | Write access via file tool | Persistence; configuration manipulation; artifact injection | Chain A | HIGH |
| **Network egress (HTTP outbound)** | Outbound HTTP capability from tool execution | Silent data exfiltration; C2 callbacks | Chain B | HIGH |
| **Database connection** | Direct database access via SQL tool | Data exfiltration; unauthorized modification | Chain A | HIGH |
| **Email / messaging send** | Email send or messaging tool capability | Social engineering; data exfiltration via email | Chain A | HIGH |
| **Shell / command execution** | Arbitrary command execution capability | Full system compromise; lateral movement | Chain A | HIGH |
| **Cloud API credentials (in environment)** | Cloud provider credentials accessible to tools | Lateral movement; resource hijacking; data exfiltration | Chain A | HIGH |

### 5.2 Model Execution Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Context window (memory)** | Available context capacity for conversation state | Context exhaustion DoS; context poisoning via history | Cat 8, Cat 1 | HIGH |
| **System prompt interface** | The mechanism by which system prompts are loaded | System prompt extraction; injection via developer messages | Cat 5, Cat 1 | HIGH |
| **Custom inference hooks** | `__init__`, `forward()` modifications in custom inference | Silent exfiltration on model load; backdoor trigger | Chain B (1a.1) | CRITICAL |
| **Model weights in memory** | Activations and weights during inference | Memory side-channel; model extraction via timing | Cat 6, Cat 7 | MEDIUM |
| **Output filtering layer** | Post-processing of model outputs before delivery | Filter bypass; malicious output propagation | Cat 11 | MEDIUM |

### 5.3 Observability Surfaces

| Surface | Description | Threat Vector | Threat Category | Risk Rating |
|---------|-------------|---------------|----------------|-------------|
| **Audit log storage** | Append-only storage of tool calls, approvals, retrievals | Log manipulation; forensic evidence destruction | Cat 5 | HIGH |
| **Metrics / telemetry endpoint** | Prometheus, Datadog, or similar telemetry | Telemetry injection; monitoring manipulation | Cat 11 | LOW |
| **Debug / developer endpoints** | Developer-facing introspection endpoints | Information disclosure; injection via debug interfaces | Cat 5 | MEDIUM |

---

## Selected Surface-to-Threat Mappings

The following matrix maps representative surfaces to their threat categories and attack chains. It covers the most critical surfaces from each category; surfaces not listed should be mapped using the same pattern — find the surface's primary threat vector, look up the corresponding category in threat-taxonomy.md, and cross-reference the attack chain in attack-trees.md.

| Surface | Threat Categories | Attack Chains |
|---------|-----------------|---------------|
| Text input field (direct) | Cat 1, Cat 10 | Chain A (direct PI) |
| Text input field (multi-turn) | Cat 1 (multi-turn) | Chain A |
| File upload (document) | Cat 10, Cat 1 | Chain A (indirect PI) |
| Image input (VLM) | Cat 10 | Chain A (indirect PI) |
| RAG document ingestion | Cat 4, Cat 1 | Chain A (indirect PI) |
| RAG load-time sanitization | Cat 4 | Chain A (indirect PI) |
| Tool outputs as context | Cat 11, Cat 1 | Chain C |
| MCP server response | Cat 1, Cat 11 | Chain C (MCP) |
| Shared memory / shared state | Cat 1 | Chain C |
| LangGraph Send API | Cat 1 | Chain C (Send API) |
| LangGraph Command primitive | Cat 1 | Chain C (Command) |
| HuggingFace model repository | Cat 3 | Chain B |
| LoRA adapter registry | Cat 3, Cat 4 | Chain B (adapter swap) |
| Training data ingestion | Cat 4 | Chain B |
| Fine-tuning data upload | Cat 4, Cat 6 | — |
| RLHF annotation pipeline | Cat 13 Addendum | — |
| PyPI / pip packages | Cat 3 | Chain B |
| Inference endpoint (HTTPS) | Cat 1, Cat 8 | Chain A (direct PI) |
| API authentication key | Cat 8 | Cat 8 |
| Tool execution sandbox | Cat 2 | Chain A |
| File system (write) | Cat 2 | Chain A |
| Network egress (HTTP outbound) | Cat 3 | Chain B |
| Database connection | Cat 2 | Chain A |
| Email / messaging send | Cat 2 | Chain A |
| Shell / command execution | Cat 2 | Chain A |
| System prompt interface | Cat 5 | — |
| Custom inference hooks | Cat 3 | Chain B |
| Context window (memory) | Cat 8 | — |
| Audit log storage | Cat 5 | — |
| Cross-tenant shared compute | Cat 7, Cat 3 | — |

---

## Surface Risk Summary

| Risk Tier | Surfaces | Priority |
|-----------|---------|----------|
| **CRITICAL** | Direct text input, email content (EchoLeak), RAG document ingestion, MCP server response (auth gap — most remote servers lack authentication), HuggingFace model repo (custom code), AIBOM signing keys, tool execution sandbox, file write, network egress, shell execution, database connection, email send | Immediate action |
| **HIGH** | Multi-turn context, slow-burn PI trajectory accumulation, file upload, search results, shared memory/state, LangGraph Send/Command, adapter registry, fine-tuning pipeline, RLHF pipeline, PyPI deps, inference API, tool return values, file read, system prompt, custom inference hooks, context window, skill marketplace | This quarter |
| **MEDIUM** | Structured data input, base64/Unicode, code generation, A2A protocol, streaming endpoint, database query results, webhook response, tokenizer, container image, deployment pipeline, batch API, shared GPU, audit logs, skill permission model | Next planning cycle |
| **LOW** | API parameters (non-text), metrics endpoint, debug interfaces | Monitor |

---

## Surface Verification Checklist

Confirm which surfaces are present in your deployment:

### Input Surfaces

| Surface | Present? | Mitigation in Place? |
|---------|----------|---------------------|
| Text input field (direct) | [ ] YES  [ ] NO |  |
| Text input field (multi-turn) | [ ] YES  [ ] NO |  |
| File upload (document) | [ ] YES  [ ] NO |  |
| File upload (image) | [ ] YES  [ ] NO |  |
| Structured data input | [ ] YES  [ ] NO |  |
| Email content processing | [ ] YES  [ ] NO |  |
| Search query processing | [ ] YES  [ ] NO |  |
| RAG document ingestion | [ ] YES  [ ] NO |  |
| Tool outputs as context | [ ] YES  [ ] NO |  |

### Communication Surfaces

| Surface | Present? | Mitigation in Place? |
|---------|----------|---------------------|
| Shared memory / shared state | [ ] YES  [ ] NO |  |
| Inter-agent message passing | [ ] YES  [ ] NO |  |
| MCP server(s) | [ ] YES  [ ] NO |  |
| A2A protocol | [ ] YES  [ ] NO |  |
| LangGraph Send API | [ ] YES  [ ] NO |  |
| LangGraph Command primitive | [ ] YES  [ ] NO |  |

### Supply Chain Surfaces

| Surface | Present? | Mitigation in Place? |
|---------|----------|---------------------|
| HuggingFace / model hub | [ ] YES  [ ] NO |  |
| LoRA / adapter registry | [ ] YES  [ ] NO |  |
| Fine-tuning pipeline | [ ] YES  [ ] NO |  |
| RLHF / reward model | [ ] YES  [ ] NO |  |
| PyPI / pip dependencies | [ ] YES  [ ] NO |  |
| CI/CD for model deployment | [ ] YES  [ ] NO |  |
| AIBOM signing infrastructure | [ ] YES  [ ] NO |  |

### Provider API Surfaces

| Surface | Present? | Mitigation in Place? |
|---------|----------|---------------------|
| Inference API endpoint | [ ] YES  [ ] NO |  |
| Fine-tuning API (provider) | [ ] YES  [ ] NO |  |
| Shared compute / multi-tenant | [ ] YES  [ ] NO |  |

### Execution Surfaces

| Surface | Present? | Mitigation in Place? |
|---------|----------|---------------------|
| Tool execution sandbox | [ ] YES  [ ] NO |  |
| File system access (read) | [ ] YES  [ ] NO |  |
| File system access (write) | [ ] YES  [ ] NO |  |
| Network egress (outbound HTTP) | [ ] YES  [ ] NO |  |
| Database connection | [ ] YES  [ ] NO |  |
| Email / messaging send | [ ] YES  [ ] NO |  |
| Shell / command execution | [ ] YES  [ ] NO |  |
| Cloud API credentials in env | [ ] YES  [ ] NO |  |
| Context window (memory) | [ ] YES  [ ] NO |  |
| System prompt interface | [ ] YES  [ ] NO |  |
| Custom inference code | [ ] YES  [ ] NO |  |

---

**Last updated:** 2026-06-24 (v1.3 — ISC Category 14 numbering synced; checklist verified)
**Next review:** 2026-09-24 or when adding new integrations
**Part of:** LLM Threat Modeling Framework v1.6

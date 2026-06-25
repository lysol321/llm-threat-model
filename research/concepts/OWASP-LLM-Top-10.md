# OWASP Top 10 for LLM Applications (2025)

## Overview
OWASP's GenAI Security Project maintains the definitive Top 10 vulnerability list for LLM applications. The 2025 edition identifies the most critical security risks across the full LLM application lifecycle: development, deployment, and operation.

**URL:** https://genai.owasp.org/llm-top-10/
**Contributors:** 600+ experts from 18+ countries
**Community:** ~8,000 active members

## The 10 Risks (2025 Edition)

### LLM01:2025 — Prompt Injection
User-supplied inputs alter LLM behavior in unintended ways. Includes direct prompt injection (user-provided input) and indirect prompt injection (via external data sources like RAG). Does not require human-readable text — any content parsed by the model qualifies.

**Key Sub-techniques:**
- Direct injection: adversarial user input
- Indirect injection: poisoned retrieval context
- Cross-context prompt leaking
- Multi-turn conversation manipulation

**Real-world example:** ChatGPT plugin exploits, Bing Chat prompt injection via search results

### LLM02:2025 — Sensitive Information Disclosure
LLM responses expose sensitive data (PII, credentials, trade secrets, internal system information). Includes both unintentional leakage and attacker-forced disclosure through carefully crafted prompts.

### LLM03:2025 — Supply Chain Vulnerabilities
LLM supply chains are susceptible to integrity compromises affecting training data, models, and deployment platforms. Key vectors:
- Outdated/third-party packages in LLM tooling
- Manipulated pre-trained models (especially LoRA/PEFT adapters)
- Platform risks (Hugging Face, Replicate, etc.)
- Data provenance issues in training corpora

### LLM04:2025 — Data and Model Poisoning
Pre-training, fine-tuning, or embedding data is compromised to introduce backdoors or bias. Distinct from LLM03 (supply chain) in that this focuses on the poisoning vector specifically.

**Key vectors:**
- Training data manipulation
- Fine-tuning dataset injection
- Embedding space poisoning
- Backdoor triggers in model weights

### LLM05:2025 — Improper Output Handling
Insufficient validation, sanitization, and handling of LLM outputs before passing to downstream systems. LLMs generate content that can contain malicious payloads, instructions for other systems, or formatted data that bypasses naive parsers.

### LLM06:2025 — Excessive Agency
LLM-based systems granted agency beyond what's necessary, enabling unintended actions. Particularly dangerous in multi-agent systems where one model's output drives another's actions without sufficient guardrails.

### LLM07:2025 — System Prompt Leakage
The system prompt (instructions, guardrails, context) is exposed to attackers through prompt injection, direct probing, or observation of model behavior.

### LLM08:2025 — Vector and Embedding Weaknesses
Security risks arising from how embeddings are generated, stored, and retrieved. Includes embedding inversion attacks, retrieval manipulation, and similarity search exploits.

### LLM09:2025 — Model Denial of Service
Intentional resource exhaustion of LLM systems through specially crafted inputs. Particularly relevant for pay-per-token cloud LLM APIs.

### LLM10:2025 — Weighted Compromise / Installation End Use
Attacks on the complete model installation lifecycle — from initial download through deployment to operational use. Includes compromised model weights, tampered inference engines, and manipulated deployment configurations.

## Notable Changes from 2023/24 to 2025
- LLM01 (Prompt Injection) remains #1 — still the most exploited vector
- Excessive Agency (LLM06) elevated in importance due to agentic AI rise
- Supply Chain (LLM03) split from Model Poisoning (LLM04) to clarify distinct risk categories
- New entry: Weighted Compromise (LLM10) addressing installation lifecycle

## Source Quality
- **Type:** Community-curated vulnerability taxonomy
- **Confidence:** High — based on real-world incidents and expert consensus
- **Use:** Primary reference for LLM security assessments

## Related
- [[MITRE ATLAS]]
- [[Prompt Injection Taxonomy]]
- [[LLM Supply Chain Security]]

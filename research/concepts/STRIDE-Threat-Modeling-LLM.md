# STRIDE Threat Modeling Applied to LLM Systems

## Overview
STRIDE is a threat modeling methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) developed by Microsoft. Applying STRIDE to LLM systems requires adapting each category to the unique properties of LLM applications.

## STRIDE-LM Extension
CSF Tools and others have developed STRIDE-LM specifically for LLM and AI/ML systems, extending the classic framework to cover ML-specific threat categories.

## Applying Each STRIDE Category to LLMs

### S — Spoofing
**LLM-specific threats:**
- Attacker impersonating a legitimate user to the LLM system
- Attacker tricking the LLM into adopting a false identity (role-playing attacks, jailbreaking)
- Model identity spoofing — adversarial model claiming to be a trusted model

**Example:** Attacker crafts prompts that make the LLM adopt a "security researcher" persona that bypasses safety guardrails

### T — Tampering
**LLM-specific threats:**
- Poisoning training data or fine-tuning datasets
- Tampering with RAG retrieval contexts (indirect prompt injection)
- Manipulating embedding vectors in vector databases
- Tampering with model weights or LoRA adapters in transit

**Example:** Attacker injects malicious content into a document in the company's knowledge base; when the LLM processes it via RAG, the tampered content influences the response

### R — Repudiation
**LLM-specific threats:**
- LLM produces outputs that are attributed to the organization but were manipulated
- Lack of audit trail for LLM-generated decisions
- Difficulty proving whether output was tampered with at inference time

**Example:** LLM recommends a harmful action; organization cannot prove whether the recommendation was due to a prompt injection vs. normal operation

### I — Information Disclosure
**LLM-specific threats:**
- System prompt leakage (LLM07)
- Training data memorization / extraction
- Embedding inversion attacks
- Exfiltrating conversation history or context data
- Sensitive data in LLM responses (LLM02)

**Example:** Through careful prompt engineering, attacker extracts the original system prompt, including guardrails and internal instructions

### D — Denial of Service
**LLM-specific threats:**
- Intentional resource exhaustion via complex/long prompts (LLM09)
- Context window exhaustion attacks
- Manipulating the LLM into infinite loops or excessive tool use
- API-level DoS via rapid repeated expensive queries

**Example:** Attacker sends thousands of extremely long prompts to exhaust the LLM API's token quota

### E — Elevation of Privilege
**LLM-specific threats:**
- Excessive agency — LLM performing actions beyond its authorization (LLM06)
- Prompt injection leading to unauthorized system access
- Chaining multiple tool uses to escalate impact
- Bypassing authorization checks through prompt manipulation

**Example:** LLM with code execution access is tricked into running attacker-supplied code via prompt injection

## STRIDE per LLM Application Layer
| Layer | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| User Input | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| System Prompt | ✓ | ✓ | — | ✓ | — | ✓ |
| RAG/Retrieval | — | ✓ | — | ✓ | ✓ | — |
| Model Weights | — | ✓ | — | ✓ | — | ✓ |
| Output Processing | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| Tool Use/API Calls | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Source Quality
- **Type:** Threat modeling framework (Microsoft, extended by community)
- **Confidence:** High — well-established methodology being adapted for LLMs
- **Use:** Primary methodology for structured threat analysis

## Related
- [[MITRE ATLAS]]
- [[OWASP LLM Top 10]]

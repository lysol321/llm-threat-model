# OWASP GenAI Security Project

## Source Details
- **Type:** Community vulnerability taxonomy
- **URL:** https://genai.owasp.org/
- **Coverage:** LLM Top 10 (2023/24, 2025 editions), cheat sheets, whitepapers, tools
- **Confidence:** High

## Key Claims
- OWASP LLM Top 10 2025 identifies Prompt Injection (LLM01) as the #1 most critical vulnerability — it is the most exploited vector in real-world attacks
- RAG and fine-tuning do NOT fully mitigate prompt injection vulnerabilities
- LLM06 Excessive Agency elevated in 2025 due to agentic AI proliferation
- LLM03 Supply Chain and LLM04 Model Poisoning are distinct but interrelated risks

## Relevance
Primary reference framework for LLM application threat modeling. The community-driven taxonomy is grounded in real-world incident data and practitioner red-team findings.

## Open Questions (from this source)
- Whether LLM01 defenses can achieve meaningful reduction without breaking functionality remains an open research area
- How to handle indirect prompt injection from trusted external data sources is not fully solved

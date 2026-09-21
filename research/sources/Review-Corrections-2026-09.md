# September review: primary evidence corrections

**Verified:** 2026-09-15. These are corrections to older evidence, not newly observed September incidents.

## EchoLeak — primary discoverer disclosure

[Aim Labs / Cato Networks, Breaking down EchoLeak](https://www.catonetworks.com/blog/breaking-down-echoleak/).

The researchers demonstrated indirect prompt injection against Microsoft 365 Copilot. Their disclosure reports no known affected customers and records Microsoft's confirmation of no customer impact. It describes exfiltration through generated Markdown images fetched by the browser. A model-side write tool is therefore not a necessary exfiltration prerequisite.

**Use:** Evidence of a demonstrated production-system vulnerability (Wild_vs_Theory 3), not confirmed malicious exploitation (4). This correction does not make a reachable sensitive-data disclosure path low impact.

## EU AI Act — enacted text

[Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), Articles 54 and 99.

Article 54 addresses authorised representatives for third-country general-purpose AI model providers, including its paragraph 6 exemption and systemic-risk exception. Article 55(2) is not the representative appointment rule. Article 99 specifies up to EUR 35 million / 7% for prohibited practices, EUR 15 million / 3% for the listed other obligations, and EUR 7.5 million / 1% for specified misleading information. Undertaking and SME calculation rules differ. Assess the entity's role and applicable provisions before assigning obligations.

## GDPR — enacted text

[Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng), Articles 32–34.

Article 32 governs security measures. Article 33 requires a controller to notify the supervisory authority without undue delay and, where feasible, within 72 hours of awareness, unless the breach is unlikely to risk natural persons' rights and freedoms. Processors notify controllers without undue delay. Article 34 separately governs communication to affected individuals. There is no universal 90-day audit-log retention mandate in Article 32.

## Resource exhaustion — OWASP primary taxonomy

[OWASP LLM10:2025 Unbounded Consumption](https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/) identifies excessive inference as an availability and financial exposure. Its mitigations include input limits, user quotas, rate limits, resource management, timeouts, monitoring and queued-action limits. DOS-DEF-1 operationalises these as tested deployment bounds; hard budget ceilings and overshoot accounting are this framework's engineering recommendations, not measured prevention rates.

## ISC and the July containment incident

[Wu et al., Internal Safety Collapse](https://arxiv.org/abs/2603.23509) supports controlled TVD benchmark failures, not confirmed malicious exploitation. [OpenAI's July 21 disclosure](https://openai.com/index/hugging-face-model-evaluation-security-incident/) reports benchmark-driven intrusion with reduced refusals and production classifiers disabled. It does not attribute ISC or establish adversarial harness input. Treat a TVD analogy as inference, and the confirmed incident as adjacent containment evidence. Do not use press narratives to elevate ISC evidence confidence.

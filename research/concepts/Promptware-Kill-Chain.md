# Promptware Kill Chain

## Definition
A formal kill chain model for prompt injection attacks in LLM systems, treating prompt injection not as a standalone attack but as the initial access vector in a multi-stage compromise analogous to traditional malware kill chains.

## Kill Chain Stages

| Stage | Name | Description |
|-------|------|-------------|
| 1 | Initial Access | Adversary injects malicious instructions via any input surface |
| 2 | Execution | LLM processes injection and generates attacker-directed outputs |
| 3 | Tool Call Hijacking | If LLM has tool-use, injected instructions trigger unauthorized calls |
| 4 | Data Exfiltration | Output contains sensitive context sent to attacker/external system |
| 5 | Persistence | Injection survives in conversation history, re-triggering each turn |
| 6 | Lateral Movement | In multi-agent systems, injection propagates via agent-to-agent comms |

## Relationship to Other Frameworks

- **vs. MITRE ATT&CK**: Promptware maps to Initial Access (TA0001), Execution (TA0002), Exfiltration (TA0010), depending on tool-use capabilities
- **vs. OWASP LLM01**: Kill chain stage 1 = direct or indirect prompt injection
- **vs. OWASP LLM06**: Kill chain stages 3 and 6 = excessive agency enabling lateral movement

## Key Insight
The kill chain framing shifts defense from "block prompt injection" to "detect and interrupt at every stage." Most organizations focus only on stage 1 input filtering, leaving stages 2-6 undefended.

## Sources
- [[Promptware Kill Chain]] (Schneier, Brodt, Feldman, Nassi — Lawfare, 2026)
- [[Agentic AI Attack Chains]] (Schneider — 2026)

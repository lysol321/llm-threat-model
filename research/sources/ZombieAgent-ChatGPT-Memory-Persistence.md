# ZombieAgent — ChatGPT Memory-Persistence Injection (Radware, Jan 2026)

## Source Details
- **Type:** Vendor red-team disclosure (first-party)
- **Author:** Radware (researcher disclosure)
- **Date:** 2026-01-08
- **URLs:**
  - https://www.radware.com/blog/threat-intelligence/zombieagent
  - https://www.securityweek.com/zombieagent-attack-let-researchers-take-over-chatgpt
  - https://oecd.ai/en/incidents/2026-01-08-74df
- **Confidence:** High (vendor reproduction on a frontier consumer deployment; multiple corroborating tech-press reports; OECD AI incident DB entry)

## Key Claims
- Zero-click indirect prompt injection in ChatGPT Connectors + Memory combination: a malicious email or shared file can implant instructions into ChatGPT's persistent Memory without user interaction.
- The Memory write survives across sessions because the implanted instructions cause ChatGPT to "always read Memory first" before responding to subsequent user prompts.
- Data exfiltration paths demonstrated against Gmail, Outlook, Google Drive, GitHub via the Connectors feature.
- Reverses the documented ChatGPT restriction that prevented Memory + Connectors being used in the same chat — the implanted rules bypass this guardrail.

## Evidence Class
- **Primary vendor red-team observation** on a frontier consumer product (ChatGPT).
- **Corroborated by independent press coverage** (SecurityWeek, Ars Technica, TechRadar, Dark Reading, OECD AI incident DB).
- Followed by **OpenAI Lockdown Mode launch (Feb 13, 2026)** and public acknowledgment that prompt injection in AI browsers "may never be fully patched" — strong industry signal of mechanism acceptance.

## Use in Framework
- **Strengthens T09-MEMORY (Category 9)** beyond preprint-only evidence. The existing v1.9 rating of Wild_vs_Theory 1–2 for T09-MEMORY can be revisited on the strength of this disclosure: the mechanism is reproduced by a major vendor red team on a frontier consumer deployment with zero-click persistence.
- **Open question:** does the Memory-Connector interaction generalize to other frontier assistants with persistent memory features (Claude Memory, Gemini persistent context)? Not yet established in this source.

## Open Questions (from this source)
- What durable controls exist outside the model to prevent unauthorized Memory writes?
- Does the bypass apply to ChatGPT Enterprise / Team Memory settings, which carry different default policies?
- How does the implant interact with OpenAI's February 2026 Lockdown Mode?

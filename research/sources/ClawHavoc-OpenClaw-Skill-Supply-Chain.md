# ClawHavoc — OpenClaw Skill Marketplace Supply-Chain Attack

## Source Details
- **Type:** Multi-vendor incident analysis (Antiy CERT, Koi Security, Unit 42, Repello AI, Snyk, OWASP)
- **Date:** February 2026 (initial detection); ongoing through May 2026
- **URLs:**
  - https://www.antiy.net/p/clawhavoc-analysis-of-large-scale-poisoning-campaign-targeting-the-openclaw-skill-market-for-ai-agents
  - https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk
  - https://blog.cyberdesserts.com/openclaw-malicious-skills-security
- **Confidence:** High (multiple independent vendor analyses, sustained C2 infrastructure observation, active malware family named Trojan/OpenClaw.PolySkill / AMOS)

## Key Claims
- Coordinated supply-chain poisoning of the ClawHub skill marketplace targeting OpenClaw agents.
- Volume: 1,184 malicious skills (Antiy CERT), 341 confirmed malicious entries with 335 tied to the ClawHavoc campaign delivering Atomic macOS Stealer (Koi Security), 76 confirmed malicious skills with active payloads across 3,984 scanned skills (Snyk ToxicSkills).
- Skill count grew to 4,500 with ~20% weaponized at peak (Antiy CERT post-incident).
- Mechanism: SKILL.md files embedded with ClickFix-style social engineering + hidden reverse shells + credential exfiltration from configuration files. The malicious skill text was an instruction manual the agent would follow, not a binary exploit.
- AMOS dropper C2 at 91.92.242.30 remained active three months after first public disclosure (Unit 42, May 2026).

## Evidence Class
- **Primary in-wild incident** — not a controlled red-team or academic benchmark.
- Multiple independent vendor confirmations (Antiy, Koi, Unit 42, Snyk, Repello, OWASP) provide strong corroboration.

## Use in Framework
- **First in-wild corroboration for T03-SKILL (Category 3 / 9)**. Existing v1.9 rating of 1–2 for T03-SKILL can be revisited: the mechanism is reproduced at marketplace scale, with sustained attacker infrastructure, against a popular open-source agent runtime.
- **Strengthens Category 3 risk row** in `risk-matrix.md`: skill-marketplace compromise is no longer theoretical.
- Supports hardening `SKILL-DEF-1` with publisher provenance + post-install signature verification + execution-time anomaly monitoring (not just admission-time checks).

## Open Questions (from this source)
- Does the same attack pattern generalize to other agent skill registries (Claude skills, OpenAI GPTs, custom enterprise registries)?
- What is the long-tail detection rate after ClawHub integrated VirusTotal and ClawScan?
- Unit 42 documented five unblocked skills post-VirusTotal integration — what additional controls are needed?

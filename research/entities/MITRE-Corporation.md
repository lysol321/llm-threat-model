# MITRE Corporation

## Entity Details
- **Type:** Non-profit research organization (US)
- **URL:** https://atlas.mitre.org/
- **Known For:** MITRE ATT&CK framework, MITRE ATLAS

## Role in LLM Threat Modeling
MITRE developed ATLAS (Adversarial Threat Landscape for AI Systems) — the AI/ML equivalent of the famous ATT&CK framework for enterprise cybersecurity. ATLAS provides (counts per atlas.mitre.org; the catalog evolves per release — the Spring 2025 update added ~19 GenAI techniques, so verify exact counts against the live matrix):
- 14 adversary tactics (Reconnaissance through Impact)
- 80+ specific techniques (`AML.T####`), with sub-techniques
- Structured threat intelligence for AI/ML systems
- Mapping between real-world incidents and academic research

See the wiki page `threat-model/mitre-atlas-mapping` for the authoritative per-threat technique IDs this project uses.

## Relevance to This Research
ATLAS is the authoritative adversary-centric threat reference for LLM systems. Where OWASP focuses on vulnerabilities, ATLAS focuses on what adversaries actually do. Essential for red-teaming and threat modeling exercises.

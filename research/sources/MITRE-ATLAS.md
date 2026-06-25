# MITRE ATLAS (Adversarial Threat Landscape for AI Systems)

## Source Details
- **Type:** Threat intelligence framework
- **URL:** https://atlas.mitre.org/
- **Coverage:** 14 tactics (Reconnaissance through Impact), 80+ techniques (`AML.T####`) targeting AI/ML systems (counts per atlas.mitre.org; evolve per release — verify against the live matrix; see wiki `threat-model/mitre-atlas-mapping`)
- **Confidence:** High

## Key Claims
- ATLAS documents real-world and research-based adversary TTPs targeting ML systems
- Modeled after MITRE ATT&CK matrix — familiar structure for security teams
- Covers full ML lifecycle: development, training, deployment, inference
- Specific LLM techniques: model poisoning, model replication, embedding extraction, prompt injection, jailbreaking

## Relevance
The canonical threat intelligence framework for AI system threats. Provides structured taxonomy for red-teaming and threat modeling LLM deployments.

## Open Questions
- ATLAS coverage of agentic/multi-agent LLM systems is still maturing
- Attribution to specific threat actors is not yet well-developed (as of 2025)

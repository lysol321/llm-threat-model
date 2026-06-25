# CSA LLM Attack Chain Research Note (2026)

**Source Type:** Research Report
**Author:** Cloud Security Alliance (CSA)
**Date:** 2026
**URL:** https://labs.cloudsecurityalliance.org/research/csa-research-note-llm-orchestrated-attack-chain-2026
**Confidence:** High

## Summary
CSA published a research note on LLM-orchestrated attack chains demonstrating how prompt injection evolves from a single-model manipulation into a coordinated multi-step kill chain in agentic AI systems.

## Key Claims

1. **Multi-step kill chains replace single-prompt attacks**: In agentic systems, a single prompt injection becomes the first step of a kill chain that chains tool calls, compromises planning, and exfiltrates data.

2. **The attack chain pattern**: Initial injection → hijack planning → execute privileged tool calls → persist in memory → propagate across connected systems.

3. **Agentic amplification**: What was once a single manipulated output can now hijack an agent's entire planning loop and propagate across multi-agent systems.

4. **Attack propagation in multi-agent**: When agents share context or communicate via protocols (MCP, A2A), prompt injection in one agent can propagate to contaminate other agents' contexts.

## Relevance to Threat Model
- Provides the kill chain structure that was missing from Round 1-2 synthesis
- Maps to OWASP LLM01 (prompt injection) and LLM06 (excessive agency) as root causes
- Informs the "multi-agent context propagation attack trees" gap identified by reviewer

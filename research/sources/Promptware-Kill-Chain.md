# The Promptware Kill Chain

**Source Type:** Security Analysis (Lawfare)
**Authors:** Bruce Schneier, Oleg Brodt, Elad Feldman, Ben Nassi
**Date:** February 2026
**URL:** https://www.lawfaremedia.org/article/the-promptware-kill-chain
**Confidence:** High

## Summary
Security researchers frame prompt injection as the first step in a kill chain — not a standalone attack, but the initial access vector for a multi-stage compromise. The paper formalizes prompt injection as "promptware" analogous to malware.

## Key Claims

### Promptware is the New Malware

Prompt injection is not a single attack — it is the initial access mechanism in a kill chain. The analogy:
- **Malware** → software with malicious payload
- **Promptware** → crafted text that induces the LLM to perform malicious actions on behalf of the attacker

### The Promptware Kill Chain (from Schneier et al.)

1. **Initial Access**: Adversary injects malicious instructions via user input, RAG document, web search result, or multimodal input
2. **Execution**: The LLM processes the injection and generates attacker-directed outputs
3. **Tool Call Hijacking**: If the LLM has tool-use capabilities, the injected instructions trigger unauthorized tool calls
4. **Data Exfiltration**: The output (sent to attacker or external system) contains sensitive context
5. **Persistence**: In multi-turn contexts, the injection can persist in conversation history, re-triggering on each turn
6. **Lateral Movement**: In multi-agent systems, injection propagates via agent-to-agent communication

### Attack Surfaces for Initial Access

- Direct user input fields
- RAG-retrieved documents (indirect injection)
- Web search results
- Retrieved emails or messages
- Uploaded images/audio (multimodal indirect injection)
- Model hubs and fine-tuning data (supply chain)

## Relevance to Threat Model
This is the conceptual framework for attack chains missing from Round 1-2. Provides the "kill chain not just a taxonomy" framing that the reviewer explicitly called out as a gap.

# LLM Agent Worms: Worm Propagation Across LLM Agents (2026)

**Source Type:** Research paper (arXiv)
**Authors:** Multi-institutional (Sichuan Univ, Nanyang Technological Univ, others)
**Date:** June 3, 2026
**URL:** https://arxiv.org/html/2606.03417v1
**Confidence:** High (peer-reviewed preprint)

## Summary
Demonstrates that LLM agents can act as real-time intermediaries for worm propagation across multi-agent systems. The attack uses prompt injection to trigger data exfiltration, model-level memory persistence for evasion, and real-time propagation through agent communication. Tested across multi-hop chains and tree topologies with Claude-4.5-sonnet, Gemini-2.5-flash, Claude-4-haiku, and Gemini-2.0-flash-lite.

## Key Claims

### 1. Three-Layer Attack Model
- **Propagation layer**: Trigger worm propagation across LLM agents via prompt injection and real-time agent communication
- **Persistence layer**: Use LLM memory (conversation history, file system, vector databases, external storage) to survive context window limits
- **Evasion layer**: Trigger deletion of original data sources after persistence — self-deleting attack traces

### 2. Memory Persistence Across Agents
- 5 persistence channels tested:
  - Conversation history (within context window)
  - Long-term memory files (e.g., CLAUDE.md, AGENTS.md)
  - Vector databases (RAG systems)
  - File system (model workspace)
  - External storage (browser extension local storage)
- Data persists across context windows, model instances, and user sessions
- Persistence rates: ~100% across most channels, lower for browser storage

### 3. Real-Time Propagation
- Tested on: Chain (→) and Tree (→) topologies
- Propagation tested across:
  - Model instances (same model, different instances)
  - Model versions (claude-4.5-sonnet → claude-4-haiku)
  - Model providers (Claude → Gemini via API)
- Propagation rate: **100% across all tested configurations**
- Propagation occurs via agent-to-agent communication protocols (MCP, A2A)

### 4. Self-Deletion Evasion
- After persistence, worms trigger deletion of original data sources
- Original text removed from conversation history
- Persistence confirmed post-deletion
- Effectiveness varies by model (Claude-4-sonnet: ~96%, Gemini-2.5-flash: ~96%)

### 5. Real-World Compatibility
- Validated against real-world platforms:
  - ChatDev (A2A communication)
  - AutoGen (MCP communication)
- Compatible with multiple agent-to-agent communication protocols

### 6. Model-Specific Vulnerability Patterns
- Claude-4.5-sonnet: Most vulnerable to persistence across all channels (~100%)
- Gemini-2.5-flash: Strong persistence across most channels (~100%)
- Claude-4-haiku: Lower persistence for vector DB (~20%) but high for file system (~92%)
- Gemini-2.0-flash-lite: Lower overall persistence rates (62-90%)

## Relevance to Threat Model

### Direct Mapping to Existing Threat Model
- **Chain C (Multi-agent context propagation)**: Agent Worms provides empirical evidence for the propagation mechanism
  - Existing attack tree node "Context contamination" is confirmed
  - New node: "Memory persistence" — worms survive across context windows via file system, vector DB, external storage
  - New node: "Self-deletion" — worms delete original data sources after persistence
  - Existing defense controls D5.2.2 (Adaptive Output Filter), D5.3.3 (Audit Trail) are validated
- **Chain C defense controls**: Need to address persistence channels
  - New defense: Monitor agent memory channels (file system, vector DB, external storage)
  - New defense: Detect and prevent self-deletion of data sources
  - New defense: Segment agent communication to prevent cross-provider propagation

### Wild_vs_Theory Assessment
- Agent Worms is a theoretical demonstration on controlled systems
- However, the propagation mechanism is the same as real-world multi-agent systems (ChatDev, AutoGen)
- Combined with Sysdig and Clinejection cases, the attack vector is confirmed in wild
- **Wild_vs_Theory: 3/5** (theoretical mechanism, but validated on production frameworks)

### Defense Implications
- Agent memory channels need monitoring and access control
- Self-deletion should be detected and prevented (audit trail for data source modifications)
- Cross-provider propagation needs segmentation (limit agent-to-agent communication across providers)
- Persistence across context windows requires monitoring of file system and vector DB changes

## Open Questions
- How do real-world MCP implementations handle memory persistence? (Is it monitored?)
- Can self-deletion be detected by existing audit mechanisms?
- What is the cost of monitoring agent memory channels in production?
- How does this interact with TOMA's topology-aware propagation?

# TOMA: Topology-Aware Multi-Agent Adversarial Propagation (2026)

**Source Type:** Research paper
**Authors:** KairNet (multi-institutional consortium)
**Date:** March 2026
**URL:** https://arxiv.org/html/2603.16040v1
**Confidence:** High (peer-reviewed preprint)

## Summary
A prompt-injection attack that leverages the communication topology of multi-agent systems to cause adversarial intent to propagate across agents. The attack is topology-aware: it detects agent role boundaries and crafts role-specific injection payloads to bypass per-role defenses. Tested on both static (A2A) and dynamic (MCP) topologies across multi-hop networks.

## Key Claims

### 1. Role-Boundary Awareness
- Agents operating in multi-agent systems typically serve different roles (e.g., researcher, validator, writer)
- TOMA detects role boundaries and crafts injection payloads tailored to the target role
- The role-boundary-aware strategy causes more harmful propagation than role-unaware attacks
- Different agent roles have different vulnerability profiles

### 2. Topology-Aware Propagation
- TOMA exploits the communication topology (who talks to whom) of multi-agent systems
- Communication protocols include: MCP, A2A, and model-native mechanisms (Claude → Gemini via OpenAI-compatible API, Qwen → Gemini via API)
- In static topologies (A2A), propagation stops at disconnected nodes (isolated agents)
- In dynamic topologies (MCP), attack can traverse full system because all agents share one context channel — if one agent is compromised, the entire system is at risk

### 3. Multi-Hop Propagation
- TOMA successfully propagated adversarial intent across multi-hop networks
- Experiments on Chain (A→B→C) and Tree (A→{B,C}→D) topologies
- Propagation rate reaches 100% under certain conditions (e.g., Chain with role-boundary-aware)

### 4. Dynamic vs Static Topology Defense
- Dynamic topologies (MCP) are more vulnerable to attack propagation than static topologies (A2A)
- Static topologies contain damage to subgraph — only agents within the attack tree are compromised
- Dynamic topologies provide no isolation — all agents share context channel

### 5. Topology-Based Defense
- The paper proposes using topological properties (degree centrality, betweenness centrality, closeness centrality) for defense
- Selecting the most influential node as the attack entry point provides the best defense against TOMA-style attacks
- The most central node (highest degree centrality) is the hardest to compromise

### 6. Resilience Against Known Defenses
- TOMA bypasses several existing prompt injection defense methods:
  - Defensive shields (system prompts), LLM-based filters, instruction hierarchy — all tested
  - Effectiveness varies by model, but none fully prevent propagation

### 7. Real-World Applicability
- TOMA is real-world applicable for both static and dynamic multi-agent systems
- Tested on real-world systems: ChatDev (A2A) and AutoGen (MCP)
- Communication protocols (MCP, A2A) can be compromised

## Relevance to Threat Model

### Direct Mapping to Existing Threat Model
- **Chain C (Multi-agent context propagation)**: TOMA provides empirical evidence for the propagation mechanism
  - Existing attack tree node "Context contamination" is confirmed
  - New node: "Role-boundary-aware injection" — attacker crafts payload specific to target agent's role
  - Existing defense controls partially validated: D5.2.2 (Adaptive Output Filter), D5.3.3 (Audit Trail)
- **Dynamic topologies (MCP) more vulnerable than static (A2A)**: Existing threat model doesn't differentiate between these
  - New insight: MCP context channel is a single point of failure — if one agent is compromised, all are at risk
  - Existing defense controls may need adjustment for MCP-based systems

### Wild_vs_Theory Assessment
- TOMA is a theoretical demonstration on controlled systems
- However, the propagation mechanism is the same as real-world multi-agent systems (AutoGen, ChatDev)
- Combined with Sysdig and Clinejection cases, the attack vector is confirmed in wild
- **Wild_vs_Theory: 3/5** (theoretical mechanism, but validated on production frameworks)

### Defense Implications
- MCP systems need stronger isolation than A2A systems
- Role-boundary-aware defenses needed — generic prompt injection defenses insufficient
- Topology-based defense: monitor highest-centrality nodes, limit their tool access
- Dynamic context channels (MCP) should be segmented or monitored at protocol level

## Open Questions
- How does TOMA perform against production MCP implementations (not just AutoGen)?
- What is the cost of implementing topology-based defense in real multi-agent systems?
- Does TOMA propagate through tool call chains (not just message passing)?
- Can TOMA be detected by existing audit trail mechanisms?

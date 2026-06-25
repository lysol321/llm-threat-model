# Agentic AI Attack Chains

**Source Type:** Security Research / Blog
**Author:** Christian Schneider
**Date:** January 2026
**URL:** https://christian-schneider.net/blog/prompt-injection-agentic-amplification/
**Confidence:** High

## Summary
Transforms prompt injection from an isolated model manipulation into a coordinated multi-tool attack chain. Cites OWASP Top 10 for Agentic Applications 2026 as key reference.

## Key Findings

### The Amplification Problem
Agentic AI systems turn a single prompt injection into a multi-step attack because:
- Agents have **tool-use capabilities** (code execution, API calls, file access)
- Agents maintain **memory and context** across turns (injection persists)
- Agents communicate via **agent-to-agent protocols** (attack propagates)
- Agents have **planning capabilities** (can be hijacked to execute attacker's plan)

### The Agentic Attack Kill Chain

Based on OWASP Top 10 for Agentic Applications 2026:

1. **Injected Instruction** (via any input surface)
2. **Hijack Planning** → LLM's planning loop follows injected instructions
3. **Execute Privileged Tool Calls** → Unauthorized actions via injected instructions
4. **Persist Malicious Instructions** → Injection survives in memory/context
5. **Propagate Across Connected Systems** → Via MCP, A2A, or shared context

### Defense-in-Depth Requirements (from OWASP Agentic Top 10 2026)

1. **Input validation on all data sources** — not just user text inputs
2. **Goal-lock mechanisms** — prevent injected instructions from deviating from intended goals
3. **Tool sandboxing with minimal privileges** — limit damage if tool is hijacked
4. **Strategic human-in-the-loop approval** — require human sign-off for high-impact actions

### Multi-Agent Context Propagation

In a multi-agent system:
- Agent A receives an injected prompt
- Agent A's output becomes part of Agent B's context
- If Agent B trusts Agent A's output, the injection propagates
- This is particularly dangerous when agents have overlapping tool permissions

## Relevance to Threat Model
Addresses reviewer's critical gap: "Multi-agent context propagation attack trees" — directly addresses how injection spreads through agent chains.

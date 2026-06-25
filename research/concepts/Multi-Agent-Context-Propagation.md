# Multi-Agent Context Propagation Attack Tree

## Definition
A multi-stage attack tree describing how a single prompt injection in one agent can propagate through an agent chain, compounding harm at each hop as injected instructions contaminate additional agent contexts. Covers both shared-state propagation (LangGraph, AutoGen) and protocol-based propagation (MCP, A2A).

## Attack Tree Structure

```
[Initial Injection]
       |
       v
Agent A receives injected prompt
       |
       +---> [Local Impact]: Agent A makes attacker-directed tool calls
       |
       v
[PROPAGATION PATH 1: Shared State]
Agent A output enters shared context / message bus
       |
       +---> MCP/A2A: Agent A sends message to Agent B via protocol
       |       |
       |       v
       |  [PROTOCOL PROPAGATION]: MCP server or A2A message carries PI
       |       |
       |       v
       |  Agent B receives Agent A output as input
       |       |
       |       +---> [Propagation Step 1]: If Agent B trusts A's output, injection spreads
       |
       v
[PROPAGATION PATH 2: Shared Messages State]
Agent B output enters Agent C context
       |
       v
[Propagation Step 2]: Multi-agent cascade
       |
       v
Exfiltration / Action at Scale
```

## Propagation Mechanisms

### Path 1: MCP (Model Context Protocol) Propagation

**Source:** CSA LLM Attack Chain Research Note (2026)

MCP is a protocol for connecting AI systems to external data sources and tools. When agents communicate via MCP:

1. **MCP Host** receives user input (with embedded PI)
2. MCP Host sends request to **MCP Server** (the tool/data source)
3. MCP Server returns response — if server is compromised or returns attacker-controlled content, PI propagates back to the host
4. MCP Host forwards poisoned response to downstream agents
5. If MCP server itself is agentic (returns instructions, not just data), the PI in the response can be instructions for the MCP Host to execute

**Critical sub-path (CSA 2026):** MCP server compromise → malicious response → MCP Host acts on instructions embedded in response → agent autonomy hijacked

**Attack chain:**
```
Initial PI in user input
    → MCP Host processes input → calls MCP Server
        → MCP Server returns malicious content (instructions embedded in data response)
            → MCP Host executes instructions from "data" response
                → Unauthorized action or data exfiltration
```

**MCP-specific attack surfaces:**
- MCP Server authentication: servers can be self-hosted or third-party — no standard server authentication
- MCP protocol has no built-in message signing or content authentication
- Compromised MCP server returns attacker-controlled data that is implicitly trusted as "ground truth"
- An MCP server returning AI-generated content (not static data) is itself an attack surface

### Path 2: A2A (Agent-to-Agent) Protocol Propagation

**Source:** CSA LLM Attack Chain Research Note (2026)

A2A protocols enable direct agent-to-agent communication. When agents share context via A2A:

1. **Agent A** sends a task request to **Agent B** via A2A protocol
2. The A2A message carries Agent A's output (which contains PI from the initial injection)
3. Agent B receives the message and incorporates Agent A's output into its context
4. If Agent B trusts Agent A's output as task context, the PI propagates

**A2A-specific attack surfaces:**
- A2A messages carry task context between agents — no content filtering at protocol level
- Agents communicating via A2A typically have established trust relationships (authenticated connections)
- PI propagation across a trusted A2A channel bypasses input validation that would catch direct user-provided PI
- Agent B acting on Agent A's A2A message may use privileged capabilities that Agent A doesn't have

### Path 3: Shared State (LangGraph/AutoGen Pattern)

This is the pattern confirmed in the Chain C LangGraph walkthrough:

1. **Shared state** (TypedDict with `messages` key) persists across all agent nodes
2. `ToolNode.invoke()` returns `ToolMessage(content=observation)` — no sanitization
3. `ToolMessage` is appended to shared state via `operator.add`
4. Next agent node receives full message history including poisoned `ToolMessage`
5. LLM cannot distinguish legitimate tool output from injected PI in `ToolMessage`

**Sub-paths confirmed in LangGraph walkthrough:**
- **`Send` API:** When using `create_agent` with parallel tool dispatch via `Send`, `ToolCallWithContext` carries tool calls with additional state — same vulnerability as `ToolNode`
- **`Command` primitive:** `langgraph.types.Command` allows programmatic state updates. Attacker-influenced state passed to `Command(resume=...)` or `Command(update=...)` injects arbitrary content into graph state outside the message-passing channel

**Additional nuance:** `ToolCallWrapper` middleware is the architecturally correct mitigation point but is not enabled by default in LangGraph.

## Defense Implications

| Node | Defensive Control | Protocol-Specific |
|------|-------------------|-----------------|
| Agent A compromised | Input validation, goal-lock, sandboxed tool execution | |
| MCP Server compromised | MCP Server allowlist, server authentication, returned-content filtering | **MCP-specific:** Use signed responses, verify MCP server identity |
| A2A message received | Output filtering before A2A send, least-privilege capabilities exposed via A2A | **A2A-specific:** Authenticate A2A peer agents, validate message content before processing |
| Context shared to B | Output filtering, content classification before sharing | |
| Agent B trusts A | Provenance tracking, agent authentication, least-privilege tool access | |
| `ToolNode` return value | Tool return sanitization via `ToolCallWrapper` middleware | LangGraph-specific |
| `Command` state injection | Avoid `Command` with attacker-influenced `resume`/`update` data | LangGraph-specific |
| Propagation to C | Network segmentation of agent groups, context isolation | |
| Exfiltration | Output monitoring, data loss prevention on agent tool channels | |

## Sources
- [[Agentic AI Attack Chains]] (Schneider — 2026)
- [[CSA Attack Chain 2026]] (CSA — 2026)
- [[Chain C LangGraph Walkthrough]] (fluffy-koala research — 2026-06-17)
- OWASP LLM06: Excessive Agency
- OWASP LLM01: Prompt Injection

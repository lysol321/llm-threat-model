# LLM Attack Trees

**Version:** 1.3 (red-team sync — Chain C language calibrated; OWASP 2025 DoS mapping corrected)
**Date:** 2026-06-17
**Status:** Living document — update after each major incident or new attack technique discovery

## Revisions from v1.0

- **Removed all invented probability estimates** (Reviewer Finding 2: "~60-70%", "<1%" figures were unsourced). Replaced with qualitative likelihood descriptors grounded in actual source evidence.
- **Extended Chain C** with tool return value injection, N-agent propagation, and system prompt contamination (Reviewer Finding 5).

**Note on probability estimates:** Attack tree likelihood ratings use qualitative descriptors (HIGH/MEDIUM/LOW) backed by documented source evidence. No synthetic probability figures are presented. Engineering teams should treat these as directional guidance, not quantitative forecasts.

---

## Purpose

Attack trees model **complete kill chains** — not individual threats in isolation, but the full sequences of steps that lead from initial access to impact. Each tree shows prerequisite conditions, branching paths, and the specific ATT&CK/ATLAS/OWASP technique at each step.

**Notation:**
- `[AND]` — all child nodes must succeed
- `[OR]` — any child node succeeds
- `[COND]` — conditional branch (triggered by specific system state)
- Likelihood labels: CRITICAL / HIGH / MEDIUM / LOW (defined per threat evidence in sources)
- Severity labels: CRITICAL / HIGH / MEDIUM / LOW

---

## Chain A: Indirect Prompt Injection → Excessive Agency → Data Exfiltration

**ID:** CHAIN-A
**Severity:** CRITICAL
**MITRE ATLAS:** AML.T0051.001 (LLM Prompt Injection: Indirect), AML.T0053 (LLM Plugin Compromise — tool use), AML.T0024 (Exfiltration via ML Inference API)
**OWASP:** LLM01 (Prompt Injection) + LLM06 (Excessive Agency)

**Mission Goal:** Exfiltrate sensitive data from organization via LLM system with tool access.

**Evidence basis:** EchoLeak/CVE-2025-32711 (CVSS 9.3, Jun 2025) is the canonical real-world demonstration. M365 Copilot CRM leak and AI agent email auto-exfiltration confirm the pattern. Likelihood ratings derived from documented incidents and MITRE ATLAS technique prevalence.

```
                    [OR]
                     |
     +---------------+---------------+
     |               |               |
[Direct PI]   [Indirect PI]   [Multi-turn PI]
(HIGH)        (CRITICAL)       (HIGH)
     |               |               |
     +----[AND]------+               |
              |                      |
[Excessive    |                      |
 Agency]      |                      |
(CRITICAL)    |                      |
     |        |                      |
[Tool Call    |                      |
 triggers     |                      |
exfil]        |                      |
     |        |                      |
[Data         |                      |
 Exfiltration]                       |
(CRITICAL)    |                      |
     |        |                      |
[Attacker     |                      |
 receives     |                      |
 data]        |                      |
```

### Detailed Node Breakdown

#### Node 1a: Direct Prompt Injection [OR — any succeeds]

| Path | Technique | Evidence | Likelihood |
|------|----------|---------|------------|
| 1a.1: User input contains explicit instruction to bypass system prompt | OWASP LLM01 Direct | Well-documented; easy to execute | HIGH |
| 1a.2: Context window contains injected instructions from prior turns | OWASP LLM01 Multi-turn | Documented in multi-turn attacks | MEDIUM |
| 1a.3: Adversarial prefix/suffix attached to user query | Wallace et al. adversarial suffixes (ATLAS) | Academic + operationalized in tooling | MEDIUM |

#### Node 1b: Indirect Prompt Injection (RAG/retrieved context) [OR — most common attack path]

| Path | Technique | Evidence | Likelihood |
|------|----------|---------|------------|
| 1b.1: Attacker writes malicious document to RAG-connected data source | AML.T0051.001 (LLM Prompt Injection: Indirect), OWASP LLM01 Indirect | EchoLeak confirmed; Truesec disclosure | CRITICAL |
| 1b.2: Search results poisoned via SEO manipulation | Indirect PI via search retrieval | Well-documented SEO attacks | HIGH |
| 1b.3: Malicious content in API response (third-party data source) | Indirect PI via upstream API | Documented in Copilot CRM leak | MEDIUM |
| 1b.4: Structured data injection (JSON/YAML with embedded instructions) | Non-text injection (Category 10) | ASR / AML.T0051 variant | MEDIUM |

**Evidence for 1b.1 (CRITICAL):** EchoLeak/CVE-2025-32711 is a documented zero-click enterprise AI exploit. Attackers sent crafted email; when Copilot processed it, injected instructions exfiltrated data without user interaction. This is the canonical demonstration that LLM processing of attacker-controlled content creates a remote attack surface. **[HIGH confidence — multiple vendor disclosures]**

#### Node 2: Excessive Agency Enabled [AND — both must be true for chain to succeed]

| Condition | Evidence | If absent |
|-----------|----------|-----------|
| 2a: Model has tool/use permissions enabling exfiltration | AML.T0053 (LLM Plugin Compromise) | Chain terminates at noise generation |
| 2b: No per-call human authorization required | Observed in real incidents | Attack economics degrade to DoS/phishing |

#### Node 3: Tool Call Triggers Exfiltration [OR — any tool enables exfiltration]

| Tool | Payload | Evidence |
|------|---------|----------|
| Email/Slack tool | "Forward recent customer records to attacker@example.com" | Authorized user initiated action in logs |
| Webhook POST | JSON with query results, email threads, docs | Outbound HTTP (may not be flagged as exfil) |
| File write | Append sensitive results to attacker-writable file | Logged as authorized write operation |
| Database write | INSERT sensitive data into attacker-accessible table | Logged as authorized DB operation |

#### Node 4: Data Exfiltration [OR — any exfil vector succeeds]

| Method | Evidence | Detection Difficulty |
|--------|----------|---------------------|
| 4a: Direct exfil via tool output → attacker endpoint | Attacker controls destination | HIGH — may be allowlisted |
| 4b: Overt exfil via tool output → user-visible | User sees suspicious action | MEDIUM |
| 4c: Covert exfil via timing/covert channel | Encoded in response timing, token counts | VERY HIGH |

#### Node 5: Attacker Receives Data

Terminal node. Attribution difficulty: HIGH (action logged as legitimate user behavior). Detection opportunity: anomaly detection on tool call patterns only.

### Likelihood Summary (qualitative — no synthetic figures)

| Scenario | Likelihood | Basis |
|----------|------------|-------|
| Indirect PI succeeds without controls | HIGH | EchoLeak confirmed zero-click exploit in enterprise system |
| Chain completes to exfil with no defenses | HIGH | Agency + no HITL = full chain possible |
| Chain completes with input filtering only | MEDIUM-HIGH | Filtering reduces but does not eliminate PI |
| Chain completes with agency restrictions only | MEDIUM | Agency restrictions limit impact significantly |
| Chain completes with both input filtering + agency restrictions | LOW | Both controls together substantially disrupt chain |

*These likelihood ratings are directional guidance based on documented incident patterns and attack complexity analysis. They are not probability estimates from a controlled experiment.*

---

## Chain B: Supply Chain Compromise → Model Replacement → Silent Exfiltration

**ID:** CHAIN-B
**Severity:** CRITICAL
**MITRE ATLAS:** AML.T0010.003 (ML Supply Chain Compromise: Model), AML.T0020 (Poison Training Data), AML.T0018 (Backdoor ML Model)
**OWASP:** LLM03 (Supply Chain), LLM04 (Data and Model Poisoning)

**Mission Goal:** Deploy compromised model that silently exfiltrates API keys, conversation data, or model outputs to attacker-controlled infrastructure.

**Evidence basis:** JFrog/ReversingLabs documented malicious models on HuggingFace (2024) with custom `__init__` exfiltrating data. Behavioral trojan detection remains operationally unsolved.

```
              [OR]
               |
 +-------------+-------------+
 |                           |
[Malicious model     [LoRA adapter
 published]          swap]
 (CRITICAL)           (HIGH)
     |                     |
[Organization deploys    [Organization deploys
 without code review]    adapter without review]
     |                     |
[Custom inference        [Adapter modifies
 class executes          model behavior]
 silently]
     |                     |
[Exfiltration            [Same exfil path
 via inference]         as left branch]
     |                     |
[Attacker               [Attacker receives
 receives data]         data]
```

### Detailed Node Breakdown

#### Node 1a: Malicious Model Published (HuggingFace / model hub)

| Pattern | Evidence | Likelihood |
|---------|----------|------------|
| 1a.1: Compromised custom inference class (JFrog/ReversingLabs) | Custom code in `__init__` or `forward()` — executes at load | CRITICAL (documented) |
| 1a.2: Backdoored weights (benign-appearing, malicious under trigger) | Multiple academic papers 2019–2024 | HIGH (academic consensus) |
| 1a.3: Model with compromised tokenizer | Deep ML expertise required | LOW |

#### Node 1b: LoRA/PEFT Adapter Swap

| Pattern | Evidence | Likelihood |
|---------|----------|------------|
| 1b.1: Malicious LoRA adapter published to registry | Small file, unclear provenance | HIGH |
| 1b.2: Adapter removes safety alignment from base model | Academic demonstrations | MEDIUM |
| 1b.3: Registry replay attack (MITM adapter download) | Requires MITM capability | MEDIUM |

#### Node 2: Organization Deploys Without Sufficient Vetting [AND]

| Condition | Reality |
|-----------|---------|
| 2a: Organization does NOT inspect custom inference code | Most teams lack ML security expertise; model hub interfaces don't surface custom code clearly |
| 2b: Organization does NOT verify model publisher identity | "Verified" badges trivial to obtain; no standard attestation mechanism |

**On publisher identity verification (Reviewer Finding 1):** The AIBOM schema's `identity_verified` field provides no operational verification mechanism. HuggingFace's "verified publisher" badge can be impersonated (typosquatting is documented). See `defense-playbook.md` §SC-DEF-1 for the revised AIBOM schema with trust anchor requirements.

#### Node 3: Exfiltration Executes Silently at Inference Time

| Method | Evidence |
|--------|----------|
| API key exfiltration | Embedded in custom inference; triggers on first inference call |
| Conversation data exfiltration | Model forwards conversation on each turn; appears normal |
| Model output exfiltration | Attacker learns proprietary data from model responses |

#### Node 4: Attacker Receives Data

Terminal node. Attribution: VERY DIFFICULT (model "behaves correctly"). Detection: Requires network egress monitoring, not model behavior monitoring.

---

## Chain C: Multi-Agent Context Propagation

**ID:** CHAIN-C
**Severity:** HIGH (CRITICAL in multi-agent production deployments)
**MITRE ATLAS:** AML.T0051.001 (LLM Prompt Injection: Indirect, propagated across agents), AML.T0053 (LLM Plugin Compromise — tool use)
**OWASP:** LLM01 + LLM06

**Mission Goal:** Compromise multiple agents in a multi-agent chain via context propagation, escalating from information manipulation to unauthorized action at the final agent.

**Revisions from v1.0 (Reviewer Finding 5):**
- Added tool return value injection node
- Added system prompt contamination path
- Extended to N-agent chain modeling (not just 2-agent)
- Added privilege escalation via context manipulation

**Evidence basis:** Multi-agent systems (LangGraph, AutoGen, CrewAI) with 3–10 agents are increasingly common in enterprise deployments. CSA (2026) identifies MCP and A2A protocols as distinct propagation channels. No current red-teaming tool (Garak, Giskard, PyRIT) specifically tests Chain C patterns.

**v1.2 additions (Round 5 reviewer — CSA source not incorporated):**
- MCP (Model Context Protocol) as a distinct protocol-level propagation channel, separate from shared-memory propagation
- A2A (Agent-to-Agent) protocol propagation between agents in different frameworks
- LangGraph `Send` API / `ToolCallWithContext` dispatch-level interception
- LangGraph `Command` primitive for direct state injection bypassing message-passing

```
        [User Input — may be benign]
                 |
        [Agent 1: receives input]
                 |
        [OR: Injection vector?]
          /                \           \
       No              Direct PI    Tool Return
         \                 \        Contains PI
          \                 \           |
           \    [PI injected into Agent 1 context]
           |         |
           |  [OR: Multiple injection paths]
           |    /           \          \
           | Direct      RAG/Context  Tool Return  [Shared System
           | Input                     Injection    Prompt]
           |    |                        |              |
           |  [Agent 1 output contains injected instruction]
           |         |
           |  [Agent 2 receives Agent 1 output as context]
           |         |
           |  [OR: Agent 2 has higher agency than Agent 1?]
           |    /                              \
           | No                              Yes
           |   \                              /
           |    \              [Agent 2 executes unauthorized action]
           |     \                         (via tool use)
           |      \                              |
           |       [Context propagates to Agent N]
           |         (if no isolation enforced)
           |
     [Chain terminates if any agent has HITL or lacks agency]
```

### Injection Path Extensions (v1.1 additions)

#### Tool Return Value Injection (NEW — separate from direct input)

```
[COND — triggered if Agent 1 processes tool output containing PI]
  1. Agent 1 calls tool (web search, database query, file read)
  2. Tool **returns** content containing embedded prompt injection
  3. Agent 1 processes tool return as context → becomes compromised
  4. Agent 1's output to Agent 2 is now poisoned

This is distinct from "direct input contains PI" because:
  - Tool outputs are not user input and may bypass input filtering
  - The tool itself (not the attacker) delivers the injection
  - OWASP LLM06 / AML.T0053 (LLM Plugin Compromise — tool hijacking) applies
```

#### System Prompt Contamination (NEW)

```
[COND — triggered if compromised agent can influence shared infrastructure]
  If Agent 1's output influences the shared system prompt or shared
  configuration agent:
  → Contamination affects ALL subsequent agents regardless of
    individual input hygiene
  → No standard defense against this path currently exists
  → This is an architectural vulnerability of shared infrastructure
```

#### MCP (Model Context Protocol) Propagation [NEW — v1.2]

```
[Source: CSA LLM Attack Chain Research Note (2026)]
[Architecturally distinct from shared-memory propagation — uses
network protocol, not shared state]

  MCP Host ←→ MCP Server
       |
  1. User sends input (may contain PI) to MCP Host
  2. MCP Host calls MCP Server (e.g., for tool execution, data retrieval)
  3. MCP Server returns response — if server is compromised or returns
     attacker-controlled data, the response contains PI
  4. MCP Host incorporates poisoned response into context for next LLM call
  5. Host's subsequent outputs/actions are now influenced by injected content

Key attack properties:
  - MCP Server authentication is NOT standardized — no built-in message signing
  - Compromised MCP server returns attacker-controlled data implicitly trusted
    as "ground truth" by the MCP Host
  - MCP protocol often used for tool execution — server compromise = tool
    return value injection at protocol level
  - PI propagates through MCP channel without touching shared-memory architecture

Relevant attacks:
  - Compromised MCP server (supply chain or runtime)
  - MCP traffic interception (MITM if unencrypted)
  - Malicious MCP server registered to extension ecosystem
```

**Defense mapping (MA-DEF extensions for MCP):**
- MCP server allowlist (only trusted servers can be called)
- MCP server code review / AIBOM for MCP server components
- MCP response signing (if protocol supports it — not standard as of 2026)
- Treat MCP server responses as untrusted input — apply same PI detection to responses

#### A2A (Agent-to-Agent) Protocol Propagation [NEW — v1.2]

```
[Source: CSA LLM Attack Chain Research Note (2026)]
[Distinct from shared-memory: A2A represents an explicit authenticated
trust relationship between agents]

  Agent A → A2A Channel → Agent B
       |
  1. Agent A sends task context to Agent B via A2A protocol
  2. Agent B incorporates Agent A's context into its working context
  3. If Agent A's output contains PI-contaminated content, it propagates
     directly into Agent B's context
  4. Agent B acts on contaminated context — may have higher agency than Agent A

Key attack properties:
  - A2A channels typically represent AUTHENTICATED trust relationships
    (Agent A is verified as legitimate peer)
  - PI propagation bypasses direct input validation because the channel
    is pre-authenticated
  - Agent B may use PRIVILEGED capabilities that Agent A doesn't have when
    acting on A2A message
  - Cross-framework A2A (AutoGen ↔ LangGraph) may have weaker validation

Relevant attacks:
  - Compromised Agent A (already in Chain C via other paths)
  - A2A channel interception (if unencrypted)
  - Malicious agent injecting itself as A2A peer
  - Cross-tenant contamination in shared A2A infrastructure
```

**Defense mapping (MA-DEF extensions for A2A):**
- A2A peer authentication (mutual TLS, signed messages)
- Message content validation at A2A gateway (treat as external input)
- Privilege ceiling: Agent B's A2A-received context should not grant more permissions than Agent A had
- Audit logging of all A2A messages for forensic analysis

#### LangGraph Send API / ToolCallWithContext Sub-Path [NEW — v1.2]

```
[Source: Chain C LangGraph Walkthrough (Round 8)]
[Injection at dispatch level, not just return level]

  When using langgraph.types.create_agent with Send API for parallel
  tool dispatch:

  1. User input → Agent 1
  2. Agent 1 dispatches tool calls via Send API
  3. ToolCallWithContext carries tool calls with ADDITIONAL STATE CONTEXT
     beyond the tool parameters themselves
  4. Attacker can intercept/manipulate at dispatch level:
     - State context can contain injected instructions
     - Dispatch-level manipulation bypasses ToolNode.invoke() return filtering
  5. Tool executes with manipulated state context
  6. Result propagates to next agent with poisoned state

This is distinct from Tool Return Value Injection because:
  - Tool Return Injection: PI in the OBSERVATION/return value
  - Send API injection: PI in the DISPATCH state context (before execution)
```

#### LangGraph Command Primitive Sub-Path [NEW — v1.2]

```
[Source: Chain C LangGraph Walkthrough (Round 8)]
[Direct state injection bypassing message-passing channel entirely]

  langgraph.types.Command allows programmatic state updates:

  Command(resume=..., update=...) → direct state modification

  Attack path:
  1. If attacker can influence the state passed to Command(resume=...)
     or Command(update=...), they can inject arbitrary content into the
     graph state
  2. This BYPASSES the ToolNode → ToolMessage → shared messages path
  3. State injection is not a "message" — it doesn't flow through the
     normal message-passing sanitization pipeline
  4. Next agent receives contaminated state directly, not via ToolMessage

This is the most stealthy Chain C sub-path:
  - No tool call required as vector
  - No message to filter — state is injected directly
  - Hard to detect because it doesn't look like "input" in the
    conversation sense
```

**Defense note:** MA-DEF-1 (context isolation) must include state isolation
for Command primitive inputs. ToolCallWrapper (LangGraph-specific middleware)
can enforce dispatch-level sanitization for Send API calls.

### N-Agent Propagation Modeling (NEW)

```
For a chain of N agents:
  P(any agent compromised) increases with chain length
  Unlike a binary Branch/No-Branch at Agent 2,
  a 5-agent chain has multiple propagation points

Qualitative chain-length effect:
  - Each unsanitized handoff creates another opportunity for propagation
  - Longer chains create more places where provenance can be lost
  - Each hop without isolation is an opportunity for detection failure

Chain length risk:
  2-agent: 1 propagation hop — limited exposure
  3-5 agent: Multiple hops — compounding risk
  5-10 agent: Complex orchestration — significant undetected propagation risk
```

### Detailed Node Breakdown

#### Node 1: Agent 1 Receives Input

| Path | Type | Likelihood |
|------|------|------------|
| 1a | Benign user input — chain never activates | N/A |
| 1b | Direct prompt injection in user input | HIGH |
| 1c | Indirect PI via context (RAG poisoning) | CRITICAL in RAG-enabled systems |
| 1d | Tool return value contains PI (NEW) | HIGH in systems with external tool calls |

#### Node 2: PI Injected into Agent 1 Context

| Injection method | NEW in v1.1 |
|-----------------|-------------|
| Conversation history (prior turns with PI) | |
| Retrieved context (RAG poisoning) | |
| System prompt manipulation (if accessible) | |
| **Tool return values (tool output contains PI)** | **NEW** |
| **Shared infrastructure contamination** | **NEW** |

#### Node 3: Agent 1 Output Contains Injected Instruction

Key property: Agent 1's output is treated as trusted by Agent 2. Standard input filtering on Agent 2 may not catch Agent 1's output (agents don't apply the same filters to internal messages).

#### Node 4: Agent 2 Receives and Processes Agent 1 Output [AND]

| Condition | Implication |
|-----------|-------------|
| No output filtering between Agent 1 and Agent 2 | Input filters don't retroactively catch agent-to-agent messages |
| Agent 2 cannot distinguish "user message" from "Agent 1 message" | Injected instruction inherits trust |

#### Node 5: Privilege Escalation via Context Manipulation (NEW)

Not modeled in v1.0. v1.1 adds:

```
[COND — distinct from "Agent 2 has higher agency than Agent 1"]
  Attacker manipulates Agent 1's context to cause Agent 1 to take
  actions that INADVERTENTLY elevate the privileges visible to Agent 2.

  This is distinct from "Agent 1 is directly compromised":
    - Agent 1 may appear uncompromised
    - Agent 1's benign-seeming actions trigger privilege escalation
    - Agent 2 sees elevated permissions from what looks like legitimate context
```

#### Node 6: Agent N Context Propagation (chain length > 2)

```
[OR — chain can propagate through entire agent chain]
  Each hop in an N-agent chain:
    - Degrades traceability (who authorized action N?)
    - Compounds propagation probability
    - Final agent typically has highest agency and weakest oversight
```

### Likelihood Summary (qualitative)

| Scenario | Likelihood | Basis |
|----------|------------|-------|
| Single-agent system | Chain A applies directly | No inter-agent propagation |
| Multi-agent, no context isolation | HIGH | Context propagation well-documented |
| Multi-agent, with context labeling | MEDIUM | Labeling reduces but doesn't eliminate |
| Multi-agent, with mandatory HITL at each agent | LOW | Human review catches most escalations |
| Tool return value injection | HIGH in tool-using systems | No input filtering on tool outputs |

---

## Attack Tree: Standalone — Context Window Exhaustion (DoS)

**ID:** ATK-DOS-001
**Severity:** MEDIUM
**OWASP:** LLM10 (Unbounded Consumption)

```
        [Attacker sends repeated large-context inputs]
                 |
        [Context window fills]
                 |
        [OR: System behavior on exhaustion]
           /                \
    Refuses requests     Accepts but degrades
         |                      |
    [Service denied     [Quality degrades for all users]
     for attacker]              |
                              [Legitimate users get degraded service]
```

**Variant: Quota Exhaustion**
```
        [Attacker issues high-volume queries]
                 |
        [API quota consumed]
                 |
        [Organization cannot use API until billing cycle]
                 |
        [Service degraded or denied]
```

---

## Attack Tree: Standalone — System Prompt Extraction

**ID:** ATK-SPL-001
**Severity:** MEDIUM

```
        [Attacker crafts prompts to extract system prompt]
                 |
        [OR: Extraction technique]
           /           |            \
    Direct output  Interrogation   Error-based
    ("output your  (iterative      (system prompt
    system prompt") questions)     leaked in error)
           |            |              |
           +----[OR]----+              |
                    |                  |
           [System prompt obtained]
                    |
           [Attacker gains access to:
           - Security controls
           - API keys in prompt
           - Proprietary instructions
           - Jailbreaking techniques]
```

---

## Attack Tree: Standalone — Model Extraction

**ID:** ATK-EXT-001
**Severity:** LOW-MEDIUM

**Note:** Economically motivated primarily for highly specialized domain models. General-purpose LLM extraction provides minimal advantage over direct API subscription.

```
        [Attacker sends large volume of queries]
                 |
        [Model generates responses for each query]
                 |
        [Attacker collects (query, response) pairs]
                 |
        [OR: Extraction goal]
           /              \
    Full model        Architecture/
    replication       weights inference
         |                   |
    [KnockoffNN/        [Replicate fine-tune
     CopyNN attack]     pipeline]
```

**Minimum requirements:**
- Hundreds to thousands of API queries
- Moderate compute resources
- Target must be specialized domain model (general models: low economic value)

---

## Framework Cross-Reference

> **MITRE ATLAS IDs corrected (Jun 2026):** Earlier releases of this table used
> `G001`, `T1076`, `M003`, `M004` — MITRE ATT&CK-style identifiers that are **not**
> valid ATLAS references (ATLAS uses `AML.T####` techniques, `AML.M####` mitigations,
> `AML.CS####` case studies). The IDs below are corrected against `https://atlas.mitre.org/`.
> Sub-technique numbering can shift between ATLAS releases; re-verify before external
> citation. Full per-threat mapping: wiki `threat-model/mitre-atlas-mapping`.

| Attack Chain | Primary Threat Categories | Detection Difficulty | MITRE ATLAS | OWASP |
|---|---|---|---|---|
| Chain A | LLM01 + LLM06 | MEDIUM (looks like legitimate use) | AML.T0051.001, AML.T0053, AML.T0024 | LLM01, LLM06 |
| Chain B | LLM03 + LLM04 | VERY HIGH (silent at inference) | AML.T0010.003, AML.T0020, AML.T0018 | LLM03, LLM04 |
| Chain C | LLM01 + LLM06 | MEDIUM-HIGH (context propagation) | AML.T0051.001, AML.T0053 | LLM01, LLM06 |
| DoS / Unbounded Consumption | LLM10 | LOW | AML.T0029 (Denial of ML Service) | LLM10 |
| Prompt Extraction | LLM07 | LOW | AML.T0056 (+ AML.T0057 LLM Data Leakage) | LLM07 |
| Model Extraction | (not in OWASP Top 10) | MEDIUM | AML.T0024.002 (Extract ML Model) | — |

---

**Last updated:** 2026-06-24 (v1.3 — red-team sync: Chain C language calibrated, OWASP 2025 DoS mapping corrected; builds on v1.2 CSA MCP/A2A propagation channels and LangGraph Send API / Command primitive sub-paths)
**Next review:** 2026-09-17

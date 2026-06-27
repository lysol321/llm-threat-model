# CORBA: Denial-of-Collaboration Attack on Multi-Agent Systems (2026)

**Source Type:** Research paper (arXiv)
**Authors:** Qian et al.
**Date:** June 10, 2026
**URL:** https://arxiv.org/abs/2606.09192
**Confidence:** High (peer-reviewed preprint)

## Summary
Identifies a novel attack vector against multi-agent systems: **denial-of-collaboration** (DoC) attacks. Rather than manipulating task outcomes, these attacks prevent or disrupt collaboration between agents — blocking message exchange, impersonating participants, or causing agents to become uncooperative. The attack exploits a fundamental gap: agent communication protocols lack integrity checks that traditional distributed systems take for granted (CORBA, RMI).

## Key Claims

### 1. Communication Protocols Are Vulnerable
- Agent communication protocols (MCP, A2A) have **no message-level integrity checks**
- Unlike CORBA and RMI (which use signed IORs and SSL), agent protocols lack:
  - Message authentication
  - Sender verification
  - Non-repudiation
- "The integrity of the agent communication protocol is simply assumed to be correct"
- This allows an attacker to: block messages, replay, impersonate, or cause misinterpretation

### 2. Attacks on Cooperation
- **Blocking**: Prevent message delivery between agents (message forwarding, connection hijacking)
- **Replay**: Replay earlier messages to disrupt current state (message desynchronization)
- **Impersonation**: Replace a legitimate agent with a malicious one (spoofed A2A responses)

### 3. Attacks on Communication Content
- **Spoofing**: Fabricate messages (prompt injection with spoofed source)
- **Modification**: Alter messages in transit (prompt injection on received messages)
- **Repudiation**: Deny message content (lack of non-repudiation mechanisms)

### 4. Exploiting Collaboration Intention
- Agents with "cooperative" disposition are vulnerable to prompt injection
- Attackers can poison individual agents to cause non-cooperative behavior
- This disrupts the entire multi-agent workflow without attacking the protocol itself

### 5. Comparison with Traditional Middleware
| Feature | Traditional (CORBA/RMI) | Agent Protocols |
|---------|------------------------|-----------------|
| Message Integrity | Signed IORs, SSL | Assumed |
| Sender Authentication | Certificate-based | None (or basic API key) |
| Non-repudiation | Built-in | Not mentioned |
| Trust Model | Distributed trust | Centralized trust assumption |
| Fault Tolerance | Built-in mechanisms | None documented |

### 6. Fundamental Gap
- Agent communication protocols prioritize "ease of use and flexibility over security"
- The fundamental gap: **no integrity verification for messages**
- This is a protocol-level vulnerability, not an application-level one

## Relevance to Threat Model

### Direct Mapping to Existing Threat Model
- **Chain C (Multi-agent context propagation)**: CORBA identifies a protocol-level vulnerability that enables Chain C
  - Existing threat model focuses on prompt injection as the attack vector
  - CORBA shows that the communication protocol itself is vulnerable
  - New insight: the protocol gap is a prerequisite for Chain C — without integrity checks, prompt injection can propagate across agents
- **Defense controls**: D5.2.2 (Adaptive Output Filter) addresses application-level injection
  - CORBA suggests need for protocol-level integrity checks (not just application-level filtering)
  - Existing defense D5.3.3 (Audit Trail) should include message authentication

### Wild_vs_Theory Assessment
- CORBA is a theoretical analysis of agent communication protocols
- However, the vulnerability is confirmed by design: agent protocols (MCP, A2A) do lack integrity checks
- The comparison with CORBA/RMI is apt — traditional middleware solved this decades ago
- Combined with TOMA propagation evidence, the protocol gap is a real vulnerability
- **Wild_vs_Theory: 3/5** (theoretical analysis, but confirmed by protocol design)

### Defense Implications
- Agent communication protocols need message-level integrity checks
- Application-level filtering (output filtering) is insufficient without protocol-level guarantees
- Consider: message authentication, sender verification, non-repudiation for agent-to-agent communication
- This is a design-level fix, not a patch — new protocol versions needed

## Open Questions
- What specific protocol changes would fix the integrity gap? (Message signing? Certificate-based auth?)
- How do existing MCP implementations handle message integrity? (Is it really "assumed"?)
- Can application-level defenses (output filtering) compensate for protocol-level gaps?
- What is the cost of adding integrity checks to agent communication protocols?

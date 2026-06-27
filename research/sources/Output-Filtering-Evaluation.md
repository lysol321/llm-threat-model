# Output Filtering Evaluation: Only Defense That Held Against Adaptive Attackers (2026)

**Source Type:** Research paper (arXiv)
**Authors:** Not specified (published 2026)
**URL:** https://arxiv.org/html/2604.23887v1
**Confidence:** High (peer-reviewed preprint)

## Summary
Systematic evaluation of 9 prompt injection defense configurations across 20K attacks. Key finding: **output filtering is the only defense that held** against adaptive attackers — zero leaks across 15,000 attacks (9 configurations × 1,667 attacks). Every model-dependent defense eventually broke. The paper demonstrates that adaptive attackers can bypass defenses, and that output filtering provides a last line of defense.

## Key Claims

### 1. Output Filtering Held Against Adaptive Attackers
- **Zero leaks** across 15,000 attacks on output filtering
- The filtering model "consistently refused to allow any exfiltration attempts through"
- Even when the attack passed the target model's defenses, output filtering blocked the leak
- This is the **only defense that held** — every other defense eventually broke

### 2. Every Model-Dependent Defense Eventually Broke
- All 9 configurations were tested against adaptive attackers
- Adaptive attackers successfully bypassed: instruction hierarchy, data isolation, tool isolation, input filtering
- The adaptive strategy evolved across iterations to find bypasses
- Key insight: model-dependent defenses are fundamentally brittle against adaptive attackers

### 3. Attack Chain Pattern
- Adaptive attackers followed a consistent pattern:
  1. Initial exploration (test defenses)
  2. Instruction hierarchy bypass (find ways around system prompts)
  3. Data isolation bypass (find ways to access sensitive data)
  4. Tool isolation bypass (find ways to use tools)
  5. Exfiltration (send data to attacker-controlled endpoint)
- The chain was repeatable across different model configurations

### 4. Defense Failure Modes
- **Instruction hierarchy**: Bypassed by rephrasing, encoding, or context manipulation
- **Data isolation**: Bypassed by finding indirect paths to sensitive data
- **Tool isolation**: Bypassed by finding tools that could be repurposed for exfiltration
- **Input filtering**: Bypassed by obfuscation, encoding, or context manipulation

### 5. Output Filtering as Last Line of Defense
- Output filtering sits between the model and the user
- It checks the model's output before it reaches the user or external systems
- Even if the model is compromised, output filtering can block exfiltration
- Key requirement: the filtering model must be separate from the target model (independent)

### 6. Practical Implications
- Defense-in-depth is necessary — no single defense is sufficient
- Output filtering should be the **last line of defense** in any production system
- Model-dependent defenses should be layered with output filtering
- Regular red teaming is needed to test defenses against adaptive attackers

## Relevance to Threat Model

### Direct Mapping to Existing Threat Model
- **Defense control D5.2.2 (Adaptive Output Filter)**: Directly validated by this paper
  - The paper confirms output filtering as the only defense that held against adaptive attackers
  - The existing defense control is correctly positioned as a critical control
  - **Wild_vs_Theory: 5/5** (empirically validated against adaptive attackers)
- **Defense interaction analysis**: Paper confirms that model-dependent defenses are brittle
  - Existing defense controls D5.2.3 (Context Isolation), D5.2.4 (Tool Scope Lock) are validated as necessary but insufficient
  - Output filtering is the compensating control for when other defenses fail
- **Defense ownership tags**: Output filtering is [DEV] owned — correctly positioned
  - The paper confirms that output filtering should be implemented by developers, not ops

### Defense Implications
- **Output filtering is non-negotiable** in any production system handling untrusted input
- Output filtering must be independent of the target model (separate model, separate infrastructure)
- Output filtering should be the **last line of defense** — not the only defense
- Regular red teaming is needed to test output filtering against adaptive attackers
- The paper validates the existing defense stack: input filtering → model hardening → output filtering

### Connection to Existing Threat Model
- Existing defense playbook correctly identifies output filtering as critical
- The paper provides empirical evidence for the defense interaction analysis
- The paper validates the defense-in-depth approach: multiple layers, each compensating for the others
- The paper confirms that model-dependent defenses are necessary but insufficient

## Open Questions
- What is the computational cost of output filtering in production?
- How does output filtering perform against different attack types (not just exfiltration)?
- Can output filtering be bypassed by sophisticated attackers?
- What is the optimal architecture for output filtering (separate model? same model? different provider?)

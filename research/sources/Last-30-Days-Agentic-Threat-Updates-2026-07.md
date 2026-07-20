# July 2026 Agentic Threat-Model Update Scan

**Research window:** 2026-06-20 through 2026-07-20 UTC
**Framework baseline:** v1.8 release manifest, 2026-06-24
**Status:** Incorporated as a provisional additive update

## Executive summary

The scan found no need for additional top-level categories. The evidence supports sharpening existing categories around persistent memory, agent skill lifecycles, inter-agent identity, computer-use visual state, session trajectories, and capability disclosure. A response-path integrity failure is a strategically important new trust-boundary candidate, but it remains provisional because the strongest source is a single preprint outside the strict 30-day window.

## Sources and claims

### Microsoft AI Red Team — June 4, 2026 (pre-window corroboration)

Source: https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us

This source is outside the strict 30-day window and is used as pre-window corroboration. The update describes seven agentic failure-mode additions and reports operational findings involving agentic supply-chain compromise, goal hijacking, inter-agent trust escalation, computer-use visual attacks, session-context contamination, MCP/plugin abuse, and capability/architecture disclosure. It also reports combinations of cross-domain prompt injection and memory poisoning, plus incremental escalation that evades per-event detection.

**Use in framework:** corroborates subtype additions and control requirements. Do not treat vendor-reported engagement frequency as a universal incident rate.

### SkillSec-Eval — July 2026

Source: https://arxiv.org/html/2607.13987v1

The paper presents a lifecycle-aware threat model for reusable agent skills covering repository admission, semantic retrieval, planner selection, execution, and skill evolution. It evaluates 327 real-world skills and argues that skill security cannot be reduced to runtime execution or prompt injection.

**Use in framework:** expands Category 3 from publication-time compromise to lifecycle compromise.

### NetInjectBench — July 2026

Source: https://arxiv.org/abs/2607.10490

The paper introduces a benchmark for indirect prompt injection in tool-using agents performing network operations.

**Use in framework:** supports adding network-operation and tool-chain scenarios to future evaluation work. Benchmark presence is not evidence of production prevalence.

### DualView — July 2026

Source: https://arxiv.org/abs/2607.03821

The paper proposes a defense for indirect prompt injection in personal agents.

**Use in framework:** supports the direction of provenance-aware and separated-view defenses; it does not replace deployment-specific testing.

### Representation confusion — submitted July 14, 2026

Source: https://arxiv.org/abs/2607.12507

The paper studies attacks in which representations make data appear to be instructions or make records from one origin appear to be independent evidence.

**Use in framework:** monitored subtype under Categories 10/11. Keep evidence confidence low until independently reproduced.

### Response-path tampering — May 2026 adjacent research lead

Source: https://arxiv.org/html/2605.02187v1

The paper describes post-alignment tampering by a BYOK relay between the upstream LLM and agent runtime, including manipulation of structured tool-call fields.

**Use in framework:** add a provisional response-path integrity surface and defense. Do not assign a universal Wild_vs_Theory rating from this source alone.

## Incorporated locations

- `synthesis/threat-taxonomy.md`
- `synthesis/attack-surface-catalog.md`
- `synthesis/attack-trees.md`
- `synthesis/defense-playbook.md`
- `synthesis/assessment-template.md`
- `synthesis/release-manifest.md`

## Open follow-up questions

- Can response-path tampering be independently reproduced across major agent runtimes and relay implementations?
- Which persistent-memory write controls are enforced outside the model in production systems?
- How often do skill registries expose retrieval/planner manipulation rather than simple malicious publication?
- What computer-use visual attacks survive DOM/accessibility reconciliation and human approval?
- Can the existing scenario suite add these paths without weakening its evidence-provenance rule?
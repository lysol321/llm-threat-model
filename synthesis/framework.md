# LLM Threat Modeling Framework

**Version:** 1.6 (red-team sync — taxonomy/risk/worksheet alignment restored after ISC addition)
**Date:** 2026-06-24
**Status:** Living document — pilot-ready after v1.6 sync verification
**Framework target:** Pilot-ready: 3-person engineering team, no ML security expertise, completes assessment in under 4 hours


## v1.6 Revision Notes (Red-Team Sync — 2026-06-24)

This version resolves the red-team review findings in `review/red-team-2026-06-24.md`:

| Finding | Severity | Change |
|---------|----------|--------|
| Taxonomy numbering drift after ISC insertion | CRITICAL | Restored OWASP-aligned Categories 1–13 and moved ISC to Category 14; updated `Cat N` references. |
| ISC missing from operational workflow | CRITICAL | Added ISC to risk matrix, priority summary, quick reference, and assessment worksheet. |
| Risk tier contradictions | CRITICAL | Moved purchased PI template attack to High and Defense Control Type Confusion to Medium. |
| OWASP 2025 mapping drift | HIGH | Corrected DoS to LLM10 Unbounded Consumption and clarified OWASP ID mapping. |
| Stale quick reference / status drift | HIGH | Synced quick reference and release status with current taxonomy. |

## v1.1 Revision Notes (from Round 2 adversarial stress-test)

This version addresses the Round 2 adversarial stress-test findings from the reviewer. Key changes:

| Finding | Severity | Change |
|---------|----------|--------|
| Invented probability estimates in attack trees | CRITICAL | Removed all synthetic probability figures; replaced with qualitative likelihood descriptors backed by source evidence |
| AIBOM identity verification has no trust anchor | CRITICAL | Added `key_verified_via` field and external trust anchor requirement to AIBOM schema |
| Defense effectiveness >90% claim unvalidated | HIGH | Removed unvalidated claim; added control type distinction (infrastructure vs. alignment) |
| RAG sanitization mechanism misaligned with pipeline | HIGH | Changed from "index-time" to "load-time" sanitization; specified actual sanitization operations |
| Chain C attack tree incomplete | HIGH | Added tool return value injection, N-agent propagation, system prompt contamination |
| HITL defense blind spot | HIGH | Revised HITL UX requirements to include context provenance in confirmation |
| Underground PI market absent | MEDIUM | Added purchased PI template sub-type; updated defense effectiveness against underground market |
| Defense independence assumption incorrect | MEDIUM | Distinguished infrastructure-enforced vs. alignment-based controls; revised effectiveness summary |
| AIBOM maintenance no operational trigger | MEDIUM | Added AIBOM freshness section with max age (90 days) and drift detection triggers |

## v1.2 Revision Notes (Pilot Unblock — Round 4 Reviewer)

This version addresses the pilot deployment blockers identified by the Round 4 reviewer:

| Finding | Severity | Change |
|---------|----------|--------|
| Scoring rubrics absent | HIGH (pilot blocker) | Added full scoring rubric appendix to assessment-template.md: decision trees for 1.1/1.2/1.4/1.5 ratings, worked example for infrastructure vs. alignment, explicit PARTIAL definitions, instruction density scoring, Section 5 decision framework for non-experts |
| No quick-reference artifact | HIGH (pilot blocker) | Created quick-reference.md: single-page summary of 12 threats, 3 attack chains, primary defenses with control types, Wild_vs_Theory scale |
| Wild_vs_Theory not embedded in framework docs | MEDIUM | Embedded Wild_vs_Theory inline in threat-taxonomy.md (Categories 1, 2, 3, 4, 9, 13) and defense-playbook.md (PI-DEF-1, AGENCY-DEF-1, AGENCY-DEF-2, SC-DEF-1) |
| "Most viable" Sigstore claim overstates | MEDIUM | Added caveat to SC-DEF-1: "most promising emerging path, not yet operational for typical HF deployments in 2026" |

**Remaining open items (not blocking pilot):**
- Chain C LangGraph walkthrough: assigned to Researcher — attack path architecturally unconfirmed (Wild_vs_Theory 2/5)
- EU AI Act Article 9 systemic risk threshold for DeepSeek/Qwen/MiniMax: unestablished — regulatory claims may be inflated

## v1.2 Revision Notes (Round 6 — Adversarial Review)

This version addresses the Round 6 adversarial review findings from the reviewer:

| Finding | Severity | Change |
|---------|----------|--------|
| Chain C MA-DEF-1 "HIGH if enforced architecturally" misleads for LangGraph default deployments | MEDIUM | Split Chain C effectiveness into three rows: DEFAULT LangGraph (MEDIUM), LangGraph WITH ToolCallWrapper enforced (HIGH), Other frameworks (MEDIUM). Added explicit caveat that ToolCallWrapper is NOT default in LangGraph. |
| Weight poisoning / backdoor attacks have no operational defense | MEDIUM | Added SC-DEF-4 (Weight-Level Trojan and Backdoor Defense Gap) documenting that AIBOM/Sigstore cannot detect behavioral backdoors; available mitigations only (sandboxing, network isolation, output monitoring). Added behavioral_backdoor_testing field to AIBOM schema. |
| Q4 2026 enforcement date unverified | LOW | Removed specific Q4 2026 date from synthesis.md; replaced with "Enforcement timeline unconfirmed as of June 2026 — monitor national market surveillance authority communications." |
| Calibration table residual scope drift | LOW | Removed stale “Qwen data routing GDPR exposure” calibration row from Wild_vs_Theory calibration table in synthesis.md |

---

## v1.2 Revision Notes (Round 5 — CSA Source Incorporated)

This version incorporates the CSA LLM Attack Chain 2026 source and the Round 8 LangGraph walkthrough findings that were not in the v1.1 release:

| Finding | Source | Change |
|---|---|---|
| CSA MCP/A2A protocol propagation not in framework | CSA Attack Chain 2026 (in sources/) | Added MCP and A2A as distinct propagation channels in Chain C attack tree and threat taxonomy Category 9 |
| Chain C missing LangGraph Send API sub-path | Round 8 LangGraph walkthrough | Added Send API / ToolCallWithContext as dispatch-level injection sub-path in Chain C |
| Chain C missing Command primitive sub-path | Round 8 LangGraph walkthrough | Added Command primitive as direct state injection sub-path in Chain C |
| Regulatory table scope drift in synthesis | Round 5 reviewer Finding 3 (LOW) | Wild_vs_Theory column removed from synthesis.md regulatory table; binary compliance indicators used |

## v1.3 Revision Notes (Round 12/13 Document Incorporation)

This version incorporates Round 12 research findings into framework documents (document incorporation gap, not new research):

| Finding | Source | Change |
|---------|--------|--------|
| Capability Withholding not in taxonomy | Round 12 research synthesis | Added Category 13 Addendum in threat-taxonomy.md: intentional CW (Wild_vs_Theory 1/5), accidental RLHF reward hacking (Wild_vs_Theory 3/5), RLHF supply chain poisoning external exploitability open question |
| Defense Interaction Analysis not in playbook | Round 12 research synthesis | Added Defense Interaction Analysis section (Defense Layer 6) in defense-playbook.md: 4 MEDIUM cascading conflicts documented; adversarial weaponization risk explicitly named |
| LLM-as-attack-vector scope note absent | Round 7 reviewer challenge (LOW priority) | Added scope boundary paragraph below: framework addresses LLM-as-target threats; adjacent LLM-as-attack-vector threats require separate organizational attention |

### v1.3 Round 16 Refinements (Non-Blocking Engineering Friction)

### Scope Boundary: LLM-as-Target vs. LLM-as-Attack-Vector

This framework addresses **LLM-as-target** threats: attacks that target the LLM system itself (prompt injection, supply chain compromise, data exfiltration, model extraction). These are threats *to* the organization deploying the LLM.

**Adjacent but out of scope:** This framework primarily addresses **LLM-as-target** threats. It includes OWASP LLM10 Unbounded Consumption where the LLM deployment itself is exhausted or financially harmed. It does not fully cover broader **LLM-as-attack-vector** misuse where an adversary uses an LLM to harm third parties through phishing, disinformation, or other generated content. OWASP LLM09 Misinformation and organization-specific content safety policies should be assessed separately for customer-facing generation and decision-support deployments.

---

## Executive Summary

This framework provides a complete, actionable threat model for LLM systems. It addresses the critical gap identified in Round 1 research: **taxonomies without kill chains are lists, not models**. Every threat in this framework is connected to:

- **Attack trees** showing full kill chain sequences
- **Risk ratings** grounded in likelihood × impact with adversary capability context
- **Layered defenses** with ownership assignment and production constraint annotations
- **Regulatory mapping** (EU AI Act, GDPR, FTC) for compliance-driven prioritization
- **An engineering worksheet** that teams can apply directly to their own deployments

The framework covers 14 threat categories plus one Category 13 addendum across 3 critical risk tiers, 3 complete attack chains, and a defense playbook with explicit effectiveness ratings.

---

## Architecture of This Framework
```
LLM Threat Framework
├── framework.md               — This document (umbrella)
├── assumptions.md              — Explicit assumptions: LLM behavior, attacker, deployment, trust (NEW v1.4)
├── asset-inventory.md          — Explicit asset inventory: data, model, infrastructure, trust, IP (NEW v1.4)
├── attack-surface-catalog.md    — Explicit attack surface catalog: input, comm, supply chain, provider, exec (NEW v1.4)
├── threat-taxonomy.md          — Master threat catalog (14 categories + Category 13 Addendum)
├── attack-trees.md             — 3 complete kill chains + standalone attack trees
├── risk-matrix.md             — Likelihood × impact ratings + regulatory mapping
├── defense-playbook.md        — Layered defenses with ownership and constraints
├── assessment-template.md      — Engineering worksheet + scoring rubric appendix
└── quick-reference.md         — Single-page summary for non-experts
```

**Reading order for a 3-person team doing a 4-hour assessment:**

**Step 1 — Confirm what applies:**
1. Read `assumptions.md` — verify which assumptions match your deployment (check the verification checklist)
2. Read `asset-inventory.md` — identify which assets are present in your system (complete the asset checklist)
3. Read `attack-surface-catalog.md` — confirm which surfaces are exposed (complete the surface checklist)

**Step 2 — Assess threats:**
4. Start with `quick-reference.md` — understand the threats and defenses at a glance
5. Use `assessment-template.md` — work through Sections 1–6 with the scoring rubric appendix at hand
6. Reference `threat-taxonomy.md` — look up specific threats when you need details
7. Reference `defense-playbook.md` — look up specific defenses when planning mitigations
8. Reference `risk-matrix.md` — use for regulatory compliance mapping

---

## What Changed from Round 1 Research

This framework addresses the seven systemic weaknesses identified by the Reviewer:

| Round 1 Gap | Framework Response |
|---|---|
| Missing attack chains | Chain A (PI→Agency→Exfil), Chain B (Supply Chain), Chain C (Multi-Agent); each modeled with full kill chain nodes |
| Underestimated adversaries | Adversary capability tiers embedded in risk ratings; nation-state and criminal orgs explicitly considered |
| No defense ownership | Every defense tagged with [DEV] / [OPS] / [PROV]; ownership table in risk matrix |
| No production constraints | Latency, UX, expertise annotations on every defense in defense-playbook.md |
| Missing regulatory dimension | EU AI Act, GDPR, FTC mapping in risk-matrix.md; compliance section in assessment-template.md |
| Non-text injection underspecified | Category 10 (Non-Text Injection Vectors) in taxonomy; Chain A variants include structured data injection |
| Model extraction overstated | Risk matrix explicitly downgrades model extraction to LOW-MEDIUM for general models |

---

## Core Framework Principles

### Principle 1: Prompt Injection is the premier threat
Prompt injection tops every credible LLM threat ranking (OWASP LLM01, MITRE ATLAS, Arcanum PI Taxonomy) because it exploits the fundamental value proposition of LLMs — instruction following — against the system. **RAG and fine-tuning do not eliminate this risk** because they operate at the training/output level, not the instruction hierarchy level.

**However:** RAG with context labeling + privilege separation reduces attack surface even if it doesn't eliminate exploitability. The goal is **reduction**, not false certainty.

### Principle 2: Excessive agency is the force multiplier
Without tool/use permissions, prompt injection generates misleading content. With agency, prompt injection becomes a remote-code-execution-equivalent. Every LLM deployment with tool permissions should treat **agency restriction as a first-order security control**, not an afterthought.

### Principle 3: Supply chain is a trust-but-verify problem
Organizations cannot fully audit closed-source models (OpenAI, Anthropic APIs). They can and must audit self-hosted models, fine-tuning pipelines, and model registry entries. **AIBOM is not optional** — it is the only scalable mechanism for supply chain accountability. The Minimum Viable AIBOM schema in `defense-playbook.md` is the starting point.

### Principle 4: Multi-agent systems compound everything
Single-agent prompt injection is locally harmful. Multi-agent context propagation turns a localized attack into a cascading failure. Organizations building multi-agent LLM systems must treat **context isolation as architectural security**, not implementation detail.

### Principle 5: Threat models without kill chains are marketing
A list of "LLM threats" without attack chain relationships tells engineers what to worry about but not how attacks actually unfold. This framework builds complete kill chains from initial access to final impact, because that is what engineering teams need to design defenses against.

---

## Explicit Foundation (v1.4 Addition)

This framework makes three elements **explicit** that were previously implicit:

### Assumptions
Before assessing your system, confirm which assumptions apply. See `assumptions.md` — it enumerates 35+ explicit assumptions across LLM behavior, attacker capability, deployment topology, trust boundaries, and regulatory scope. **If an assumption doesn't match your deployment, the associated risk ratings may not apply.**

### Asset Inventory
Every threat model must answer "what exactly are we protecting?" The `asset-inventory.md` enumerates 50+ assets across data, model, infrastructure, trust boundary, and IP categories — with crown jewel prioritization, classification tags, and an asset-to-threat mapping. **Risk scores are meaningless without knowing which assets are present.**

### Attack Surface Catalog
Every threat requires a reachable attack surface. The `attack-surface-catalog.md` enumerates 60+ surfaces across input, communication, supply chain, provider API, and execution categories — with threat vectors, risk ratings, and a surface-to-threat matrix. **If a surface isn't present in your deployment, the associated threats don't apply.**

---

## Threat Priority Summary

### Critical (immediate action required)

| Threat | Risk Score | Primary Attack Chain | Primary Defense |
|---|---|---|---|
| Indirect PI → Excessive Agency → Data Exfiltration | **20** | Chain A | RAG labeling + minimal permissions |
| Supply Chain: Malicious Custom Inference | **20** (elevated) | Chain B | AIBOM + sandboxing |
| Multi-Agent Context Propagation | **19** (elevated) | Chain C | Context isolation |
| Internal Safety Collapse / Validator Harness | **20** | Cat 14 | Validator harness validation + semantic output safety |

### High (prioritize within current quarter)

| Threat | Risk Score | Primary Attack Chain |
|---|---|---|
| Direct Prompt Injection | 15 | Standalone |
| Purchased PI Template Attack | 15 | Direct PI variant |
| RAG Context Poisoning | 15 | Chain A variant |
| Excessive Agency (standalone) | 14 | AGENCY-DEF-1 + AGENCY-DEF-2 |
| Training Data Poisoning | 14 | Provider-side controls |
| LoRA/PEFT Adapter Swap | 15 (orgs with fine-tuning) | Registry controls |
| Embedding Inversion | 14 (if personal data) | Provider-side |
| API Quota Exhaustion — Metered Enterprise API | 16 | Rate limiting, quota management |

### Medium (address in next planning cycle)

| Threat | Risk Score |
|---|---|
| System Prompt Extraction | 9 |
| Context Window Exhaustion DoS | 9 |
| API Quota Exhaustion — Standard API | 12 |
| Output Validation Failure | 9 |
| Image/Structured Data Injection | 8 |
| HITL Failures | 9 |
| Model Extraction (specialized models) | 9 |
| Defense Control Type Confusion | 12 |

---

## Defense Investment Guidance

For organizations with limited resources, defense investment should follow this priority order:

**Tier 1 (start here — highest leverage):**
1. **Minimal permission scoping** — if the LLM can't call tools, PI impact is noise
2. **RAG context labeling** — distinguishes retrieved content from trusted instructions
3. **AIBOM maintenance** — enables supply chain accountability

**Tier 2 (once Tier 1 is solid):**
4. **Instruction hierarchy hardening** — makes direct PI harder to exploit
5. **Human-in-the-loop for high-risk actions** — limits damage if other controls fail
6. **Tool call audit logging** — enables incident response

**Tier 3 (for mature programs):**
7. **Custom inference code sandboxing** — prevents silent exfiltration
8. **Inter-agent context isolation** — breaks multi-agent kill chains
9. **Anomaly detection** — catches attacks that slip past preventive controls

---

## Regulatory Landscape

| Regulation | Key Obligation | Primary Threat Connection |
|---|---|---|
| **EU AI Act (2024/1689)** | Article 9 risk management; Article 10 data governance; Article 13 transparency/instructions; Article 14 human oversight; Article 15 robustness/cybersecurity; Article 17 quality management | PI, Excessive Agency, Multi-Agent, Poisoning, ISC, supply chain validation |
| **GDPR (Article 17, 25, 32)** | Right to erasure for personal data; privacy by design; security of processing; breach notification | Embedding inversion, training data poisoning, cross-tenant leakage |
| **FTC AI Guidance** | Unfair or deceptive security practices; reasonable security measures | PI → exfiltration, output validation failures |

The EU AI Act is the most comprehensive and has the highest compliance stakes. Organizations deploying LLMs in EU markets should prioritize Article 9 lifecycle risk management, Article 14 human oversight, and Article 15 robustness/cybersecurity as the security baseline; use Article 13 for deployer-facing transparency and instructions, Article 10 for dataset governance, and Article 17 for provider quality-management processes.

---

## Framework Maintenance

### Update triggers
- New OWASP LLM Top 10 release (annual)
- New MITRE ATLAS technique additions
- Major real-world incident (published post-mortem)
- New attack technique published (adversarial suffix, injection method)
- Regulatory change (EU AI Act implementing guidance, FTC enforcement action)

### Version history

| Version | Date | Changes |
|---------|------|---------|
| 1.7 | 2026-06-24 | Correction pass: residual-risk math fixed; EU AI Act mappings normalized; risk matrix base/elevated scores split; detection/operational-gap controls added to worksheet; defense tables normalized; release manifest added. |
| 1.6 | 2026-06-24 | Red-team sync: canonical taxonomy numbering restored, ISC threaded into operational workflow, OWASP 2025 IDs corrected, risk-tier contradictions fixed, quick reference and worksheet synced. |
| 1.4 | 2026-06-19 | Round refinements: Assumptions section, Asset Inventory section, and Attack Surface Catalog section made explicit so the framework defines what it assumes, protects, and exposes. |
| 1.3 | 2026-06-18 | Round 16 refinements: DoS impact split; Chain C Wild_vs_Theory structural evidence clarification; Capability Withholding addendum; Defense Interaction Analysis; LLM-as-attack-vector scope boundary. |
| 1.2 | 2026-06-17 | Round 6 and Round 5: MA-DEF-1 split rating; weight poisoning/backdoor defense gap; enforcement date removed; CSA MCP/A2A propagation; LangGraph Send API + Command primitive sub-paths. |
| 1.1 | 2026-06-17 | Round 2 adversarial stress-test fixes: removed invented probabilities, fixed AIBOM trust anchor, corrected RAG sanitization, extended Chain C, revised HITL UX, added underground PI market, clarified control types. |
| 1.0 | 2026-06-17 | Initial framework — addresses Reviewer Round 1 critiques |

### Next planned update
2026-09-17 (quarterly review cycle)

---

## Document Index

| Document | Path | Purpose |
|---|---|---|
| Framework (this doc) | `synthesis/framework.md` | Umbrella document, architecture, version history |
| **Assumptions (NEW v1.4)** | `synthesis/assumptions.md` | Explicit assumptions: LLM behavior, attacker capability, deployment topology, trust boundaries, regulatory scope |
| **Asset Inventory (NEW v1.4)** | `synthesis/asset-inventory.md` | Explicit asset inventory: data, model, infrastructure, trust boundary, IP assets with classification and ownership tags |
| **Attack Surface Catalog (NEW v1.4)** | `synthesis/attack-surface-catalog.md` | Explicit attack surface catalog: input, communication, supply chain, provider API, execution surfaces |
| Threat Taxonomy | `synthesis/threat-taxonomy.md` | Master threat catalog, 14 categories with cross-references, Wild_vs_Theory embedded |
| Attack Trees | `synthesis/attack-trees.md` | 3 complete kill chains + standalone attack trees |
| Risk Matrix | `synthesis/risk-matrix.md` | Likelihood × impact ratings, regulatory mapping, production constraints |
| Defense Playbook | `synthesis/defense-playbook.md` | Layered defenses by threat, ownership, effectiveness, control type |
| Assessment Template | `synthesis/assessment-template.md` | Engineering worksheet for self-audit + scoring rubric appendix |
| Quick Reference | `synthesis/quick-reference.md` | Single-page summary for non-expert teams |
| Research Synthesis | `research/synthesis.md` | Research foundation (red-teaming tooling, real-world incidents, capability withholding) |
| Reviewer Critiques | `review/` | All adversarial review rounds (rounds 1–18) |

---

**Framework prepared by:** Synthesizer (LLM Threat Modeling project)
**Date:** 2026-06-24
**Status:** Version 1.7 — correction pass complete; pilot candidate pending team-specific assessment and sign-off

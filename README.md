# LLM Threat Modeling Framework

**Release v1.12** · Pilot candidate · Updated 2026-09-19

This threat model is for engineering teams assessing LLM deployments. It assumes no ML security expertise. The framework covers 14 threat categories, 3 canonical attack chains plus scoped agentic trust-boundary branches, a layered defense playbook, a risk matrix with regulatory mapping, and an engineering worksheet that a 3-person team can complete in under 4 hours.

> **Disclaimer.** This is independent personal research by the author, developed on personal time and built solely from publicly available sources (OWASP, MITRE ATLAS, published CVEs, academic papers, and vendor documentation). It is **not** affiliated with, sponsored by, or derived from any employer, client, or government work, and contains no proprietary, classified, or controlled information. It is provided for defensive and educational purposes only. All views are the author's own.

---

## What This Is

Most LLM threat guidance is either a flat vulnerability list or an academic kill-chain diagram. This framework connects the two: every threat maps to a complete attack sequence, a risk score grounded in evidence (not speculation), layered defenses with explicit ownership, and a worksheet that teams can apply to their own deployments today.

The framework went through 18 foundational adversarial-review rounds plus a focused July 2026 red-team review. Release v1.12 contains 39 documented tabletop scenarios, including nine July agentic cases, eight September 15 regressions, two September 19 correction cases, and four September 19 research-integration cases for monitor integrity, compaction authority, failure-path cleanup, and configuration revalidation. Control states are explicitly hypothetical; records include ratings, calculations, decisions and owners.

Release v1.12 is a **pilot candidate**, not a deployment certification. Teams must complete the worksheet against their own architecture, evidence, and trust boundaries before accepting residual risk. See the canonical [`release-manifest.md`](synthesis/release-manifest.md) for component versions and evidence caveats.

---

## Quick Start

**Open the interactive HTML viewer:**
```
open llm-threat-model.html
```
The HTML viewer gives you a tabbed interface — Overview, 14 Threats, Attack Chains, Risk Matrix, Defenses, Decision Tree, OWASP Mapping, and Docs — with a sidebar for navigating reference materials. Click any document in the sidebar to read it inline in the Docs tab.

**Run an assessment on your deployment:**

1. Read [`assumptions.md`](synthesis/assumptions.md) and confirm which apply to your system
2. Read [`assessment-template.md`](synthesis/assessment-template.md) — work through Sections 1–5 in order
3. Use [`quick-reference.md`](synthesis/quick-reference.md) as a wall-ready summary during the assessment
4. Reference [`threat-taxonomy.md`](synthesis/threat-taxonomy.md) for threat details
5. Reference [`defense-playbook.md`](synthesis/defense-playbook.md) for mitigation planning

**Defense investment priority if you have limited time:**

| Tier | Focus |
|------|-------|
| **Tier 1** | Minimal permission scoping · RAG context labeling · AIBOM maintenance |
| **Tier 2** | Instruction hierarchy hardening · Human-in-the-loop for high-risk actions · Tool call audit logging |
| **Tier 3** | Custom inference sandboxing · Inter-agent context isolation · Anomaly detection |

Deployment gates take precedence over investment tiers: PI-DEF-4 is required at output consumers, DATA-DEF-1 for consequential external/changeable data, and execution or inter-agent boundaries must be enforced whenever those paths exist.

**Validate the scenario suite:**
```bash
python scripts/test_scenario_suite.py
```

**Validate release coherence and the generated HTML:**
```bash
python scripts/test_corpus_coherence.py
python scripts/build-html.py --check
```

**Detect citation drift after editing synthesis files:**
```bash
python scripts/citation_drift_detector.py          # detect
python scripts/citation_drift_detector.py --fix   # auto-fix line ranges
python scripts/citation_drift_detector.py --batch-requote  # refresh drifted quotes
```

---

## Framework Architecture

```
LLM Threat Framework
├── framework.md               — Umbrella: architecture, version history, principles
├── assumptions.md             — Explicit assumptions: LLM behavior, attacker, deployment, trust
├── asset-inventory.md         — Explicit asset inventory: data, model, infrastructure, trust, IP
├── attack-surface-catalog.md   — Explicit attack surface catalog: input, comm, supply chain, provider, exec
├── threat-taxonomy.md         — Master threat catalog (14 categories + canonical agentic subtype IDs)
├── attack-trees.md            — 3 canonical chains + scoped agentic trust-boundary branches
├── risk-matrix.md            — Likelihood × impact ratings + regulatory mapping
├── defense-playbook.md        — Layered defenses with ownership and constraints
├── assessment-template.md     — Engineering worksheet + scoring rubric appendix
├── quick-reference.md         — Single-page summary for non-expert teams
└── release-manifest.md       — Coherent corpus state pointer per release
```

**Reading order for a 4-hour assessment:**

```
assumptions.md
    ↓
asset-inventory.md
    ↓
attack-surface-catalog.md
    ↓
quick-reference.md  (get the picture fast)
    ↓
assessment-template.md  (work through Sections 1–5)
    ↓
threat-taxonomy.md  (look up threats as you assess)
    ↓
defense-playbook.md  (plan mitigations)
    ↓
risk-matrix.md  (regulatory mapping and residual risk math)
```

---

## 14 Threat Categories at a Glance

| # | Threat | Priority | Wild_vs_Theory |
|---|--------|----------|----------------|
| 1 | **Prompt Injection** — manipulating model instructions through crafted inputs | CRITICAL | 4/5 |
| 2 | **Excessive Agency** — granting more tool/action permissions than necessary | CRITICAL | 4/5 |
| 3 | **Supply Chain Compromise** — malicious models, adapters, MCP servers from third parties | HIGH | 4/5 |
| 4 | **Data/Model Poisoning** — compromising training data, fine-tuning sets, RAG stores | HIGH | 3/5 |
| 5 | **System Prompt Leakage** — extracting prompts, API keys, proprietary instructions | MEDIUM | 3/5 |
| 6 | **Model Extraction** — query-based replication of proprietary models | LOW-MEDIUM | 2/5 |
| 7 | **Embedding/Vector Weaknesses** — reconstructing sensitive data from embeddings | MEDIUM | 2/5 |
| 8 | **Denial of Service / Unbounded Consumption** — context/quota exhaustion | MEDIUM-HIGH | 4/5 |
| 9 | **Multi-Agent Context Propagation** — PI propagating between chained agents | HIGH | 3/5 |
| 10 | **Non-Text Injection** — image, audio, or structured data injection | MEDIUM | 2/5 |
| 11 | **Output Validation Failures** — unsafe outputs passed unchecked to users/systems | MEDIUM | 3/5 |
| 12 | **HITL Failures** — human reviewers miss adversarial manipulation due to missing provenance | MEDIUM | 3/5 |
| 13 | **Defense Control Type Confusion** — alignment controls mistaken for infrastructure controls | MEDIUM-HIGH | 3/5 |
| 14 | **Internal Safety Collapse / Validator Harness** — benign-looking task causes harmful generation | CRITICAL | 2/5 |

**Category 13 Addendum:** Capability Withholding (intentional knowledge suppression) — Wild_vs_Theory 1/5, primarily theoretical; accidental RLHF reward hacking — Wild_vs_Theory 3/5.

See [`threat-taxonomy.md`](synthesis/threat-taxonomy.md) for full threat entries with attack vectors, sub-types, and cross-references.

---

## 3 Attack Chains

### Chain A: Indirect PI → Excessive Agency → Data Exfiltration

```
[Indirect PI via RAG / documents / external data]
         ↓
[Sensitive data + reachable disclosure channel]
         ↓
[Answer, renderer request, search query or tool exports data]
         ↓
[Attacker receives data — logged as legitimate user action]
```

**Wild_vs_Theory: 4/5** for the aggregate category; EchoLeak individually is **3/5**, a production-system demonstration with no affected customers reported. See `research/sources/Review-Corrections-2026-09-19.md`.

### Chain B: Supply Chain → Model Replacement → Silent Exfiltration

```
[Malicious model on HuggingFace / adapter swap]
         ↓
[Organization deploys without code review]
         ↓
[Custom inference class exfiltrates at model load time]
         ↓
[Silent — no behavioral signal; detection requires network egress monitoring]
```

**Wild_vs_Theory: 4/5** — JFrog / ReversingLabs confirmed malicious models on HuggingFace.

### Chain C: Multi-Agent Context Propagation

```
[PI injected into one agent's context]
         ↓
[Context propagates via agent-to-agent messaging (MCP, A2A)]
         ↓
[Multiple agents take harmful actions from a single injection point]
         ↓
[Cascading failure across the agent ecosystem]
```

**Wild_vs_Theory: 3/5** — Architectural risk confirmed; full in-wild chain not yet documented.

See [`attack-trees.md`](synthesis/attack-trees.md) for the complete kill-chain node maps.

---

## Defense Playbook

Defenses are layered: **Primary** (strongest mitigation), **Secondary** (reduces surface or limits impact), **Tertiary** (detection and recovery). Every defense is tagged with an owner so engineering and operations teams know who is responsible.

| Tag | Owner | Examples |
|-----|-------|---------|
| **[DEV]** | Developer | Prompt engineering, instruction hierarchy hardening, output filtering |
| **[OPS]** | Operator | Permission scoping, monitoring, rate limiting, AIBOM maintenance |
| **[PROV]** | Model Provider | API-level safety controls, model safety training, infrastructure |

**Critical distinction — read before rating defenses:**

- **Infrastructure-enforced controls** are enforced by the deployment architecture (permission revocation, network isolation, sandboxing). They work regardless of model behavior.
- **Alignment-based controls** depend on the model's RLHF training to refuse harmful requests. They can be circumvented by a sufficiently capable attacker.

**Conflating the two is a documented threat (Category 13).** When a defense is alignment-based, rate it lower and always layer an infrastructure control behind it.

See [`defense-playbook.md`](synthesis/defense-playbook.md) for the full defense catalog.

---

## Evidence Provenance

Incident/evidence claims require primary or corroborating sources. Risk scores and mitigation factors are planning judgments, not measured probabilities or prevention rates. It uses two source classes:

| Source type | Carries risk ratings | Examples |
|-------------|---------------------|----------|
| **Primary / corroborated** | ✅ Yes | Academic papers with empirical results, CVE disclosures, confirmed incident post-mortems |
| **Press / community narrative** | ❌ Context only | News articles, blog posts, conference talks — used for background, not for risk scores |

The 39-scenario evaluation suite checks documented tabletop assessments: every major conclusion in every scenario must cite a `synthesis/` file and line range. Each scenario records actual control ratings, scoring inputs, residual scores and an action/owner for its scoped risks. Checks verify completeness, arithmetic and citation location; they do not prove semantic correctness or deployed control effectiveness. The validator uses an extensible minimum count plus mandatory capability and named-scenario coverage, so adding valid scenarios does not break the contract.

---

## Directory Structure

```
llm-threat-model/
├── llm-threat-model.html          — Interactive HTML viewer (tabbed interface + sidebar doc nav)
├── threat-model-data.json          — Source of truth for the HTML viewer data
├── synthesis/                     ← THE FRAMEWORK (primary deliverable)
│   ├── framework.md         — Umbrella + architecture + version history
│   ├── assumptions.md       — 35+ explicit assumptions the framework rests on
│   ├── asset-inventory.md   — 50+ assets across data, model, infrastructure, trust, IP
│   ├── attack-surface-catalog.md — 60+ surfaces with threat vectors
│   ├── threat-taxonomy.md  — 14 categories with sub-types, OWASP IDs, evidence ratings
│   ├── attack-trees.md      — 3 canonical chains + scoped agentic branches with node IDs
│   ├── risk-matrix.md       — Likelihood × impact ratings + regulatory mapping
│   ├── defense-playbook.md — Layered defenses with ownership, effectiveness, constraints
│   ├── assessment-template.md — Engineering worksheet + scoring rubric appendix
│   └── quick-reference.md   — Single-page triage artifact
│
├── research/                ← Source material (framework is built from this)
│   ├── synthesis.md         — Research synthesis (tooling, incidents, capability withholding)
│   ├── concepts/            — Specific concept research (PI taxonomy, MITRE ATLAS, etc.)
│   ├── entities/            — Entity research (OWASP, DeepSeek, MITRE Corp, Jason Haddix, etc.)
│   ├── questions/           — Open questions and identified research gaps
│   └── sources/             — Primary and corroborating sources with annotations
│
├── evaluation/              ← Framework validation
│   ├── scenario-suite.json — 39 deployment scenarios with 9 pass/fail criteria each
│   ├── scenario-suite-results.md
│   └── assessment-walkthrough-example.md
│
├── review/                  ← Adversarial review history (18 rounds)
│   ├── critique-2026-06-17.md through critique-2026-06-18-r18.md
│   ├── red-team-2026-06-24.md (and follow-up passes)
│   └── red-team-2026-07-20-agentic-update.md — v1.9 adversarial review and remediation record
│
├── scripts/
│   ├── test_scenario_suite.py         — CI gate: validates scenario suite integrity
│   ├── test_corpus_coherence.py       — Release/version/control/HTML coherence gate
│   ├── citation_drift_detector.py    — Detects and fixes quote/range drift in citations
│   ├── build-html.py                — Regenerates HTML data and checks checked-in freshness
│   └── md_to_html.py                — Markdown → HTML converter (stdlib-only)
│
└── threat-model-data.json    — Structured source for HTML threats, controls, and navigation data
```

---

## Regulatory Mapping

The framework maps to three regulatory regimes:

| Regulation | Key Obligations | Primary Threat Connections |
|------------|-----------------|---------------------------|
| **EU AI Act** (2024/1689) | Article 9 risk management; Article 13 transparency; Article 14 human oversight; Article 15 robustness | PI, Excessive Agency, Multi-Agent, Poisoning, ISC, supply chain |
| **GDPR** (Art. 17, 25, 32) | Right to erasure; privacy by design; security of processing; breach notification | Embedding inversion, training data poisoning, cross-tenant leakage |
| **FTC AI Guidance** | Unfair/deceptive security practices; reasonable security measures | PI → exfiltration, output validation failures |

Classify jurisdiction, intended use and entity role before applying obligations. High-risk system requirements and GPAI-provider duties differ; EU-market access alone does not establish either classification. See [`risk-matrix.md`](synthesis/risk-matrix.md) for applicability gates and sources.

---

## External Framework Positioning

This framework works alongside established AI security standards. It uses them as source-backed references and brings their separate pieces into one engineering workflow.

| Framework | Role | How This Framework Uses It |
|-----------|------|---------------------------|
| **OWASP Top 10 for LLM Applications 2025** | Vulnerability category baseline | OWASP ID mapping throughout taxonomy; baseline threat list |
| **MITRE ATLAS** | Adversary TTPs for AI systems | Adversary behavior language; technique-to-threat mapping |
| **NIST AI RMF + GenAI Profile** | Governance and risk management process | Compliance framing; lifecycle risk management |
| **MAESTRO / agentic AI threat modeling** | Multi-agent ecosystem threat modeling | Inter-agent communication, orchestration, memory poisoning |
| **Microsoft Agentic AI Failure Mode Taxonomy** | Agent safety failure modes | Agent-specific failure analysis in Chain C |
| **OWASP Agentic AI / MCP guidance** | Tool and MCP server security | Tool poisoning, third-party MCP risk, least-privilege for tools |

---

## Versioning and Maintenance

Framework docs are versioned independently. Check the version header in each file.

| Version | Date | Key Change |
|---------|------|-----------|
| 1.11 | 2026-09-19 | Output/data integrity boundaries, complete tabletop assessments, legal applicability gates and README evidence synchronization |
| 1.10 | 2026-09-15 | Evidence corrections: ISC 2/5 controlled research; EchoLeak 3/5 demonstration; read-only disclosure and deployment scoring corrections |
| 1.9 (+ 2026-07-22 addendum, superseded by v1.10) | 2026-07-22 | Historical attribution withdrawn: the adjacent containment incident does not establish the ISC mechanism. Current ISC evidence is 2/5 controlled research; see the v1.10 corrections. |
| 1.9 | 2026-07-20 | Agentic trust-boundary integration: canonical subtypes, seven assessable controls, nine new scenarios, calibrated overlays, and synchronized HTML |
| 1.8 | 2026-06-24 | Comparable framework positioning (OWASP, MITRE, NIST, MAESTRO, Microsoft, OWASP Agentic/MCP) |
| 1.7 | 2026-06-24 | Correction pass: residual-risk math, EU AI Act mappings, base/elevated score split |
| 1.6 | 2026-06-24 | Red-team sync: taxonomy numbering restored, ISC threaded into workflow |
| 1.4 | 2026-06-19 | Explicit assumptions, asset inventory, and attack surface catalog added |
| 1.0 | 2026-06-17 | Initial framework after 18 adversarial review rounds |

**Update triggers:**
- New OWASP LLM Top 10 release (annual)
- New MITRE ATLAS technique additions
- Major real-world incident with published post-mortem
- New attack technique published (adversarial suffix, injection method)
- Regulatory change (EU AI Act implementing guidance, FTC enforcement action)

**Next planned review:** 2026-10-15 or after a material deployment change

---

## Scope Boundary

This framework addresses **LLM-as-target** threats: attacks that target the LLM system itself (prompt injection, supply chain compromise, data exfiltration, model extraction). These are threats *to* the organization deploying the LLM.

**Out of scope:** This framework does not fully cover **LLM-as-attack-vector** misuse — using an LLM to harm third parties through phishing, disinformation, or generated content. OWASP LLM09 Misinformation and organization-specific content safety policies should be assessed separately for customer-facing generation and decision-support deployments.

## September 19 research integration

Release v1.12 extends monitor/approval integrity, compaction/resume authority, rejected-request cleanup and generation-configuration revalidation under existing controls. The 39 scenarios are documented tabletop assessments; their deployment verification plans are not executed security tests. See [research/sources/Latest-Development-Integration-2026-09-19.md](research/sources/Latest-Development-Integration-2026-09-19.md) for primary sources and evidence limits, and [verification](review/research-integration-2026-09-19.md). Existing threat evidence ratings are unchanged.

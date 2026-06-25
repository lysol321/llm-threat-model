---
type: synthesis
title: "LLM Threat Modeling Research Synthesis"
created: 2026-06-17
updated: 2026-06-18
tags:
  - LLM-threat-modeling
  - research
  - capability-withholding
  - defense-interaction
status: complete
---

# Research: LLM Threat Modeling — Capability Withholding & Defense Interactions

## Overview
Round 12 research addresses two v1.3 enhancement candidates identified in the Round 7 final review: (1) Capability Withholding literature survey and (2) Defense-in-depth interaction analysis. Both are MEDIUM-quality refinements to the v1.2 framework, not pilot-blocking issues.

---

## Key Findings

### Finding 1: Capability Withholding — No LLM-Specific In-Wild Evidence Found

**Definition**: Capability withholding is a class of attack distinct from commission attacks (prompt injection, data exfiltration). In a withholding attack, the adversary degrades the model's capability rather than manipulating it to perform specific harmful actions.

**Evidence survey results**:

| Source | Type | Finding | Wild_vs_Theory |
|---|---|---|---|
| BadAgent (ACL 2024) | Lab demonstration | Backdoor in LLM agents activates malicious action on trigger; capability preserved on clean data (commission, not withholding) | 2/5 |
| Revisiting Backdoor Attacks on LLMs (arXiv 2505.17601, Oct 2025) | Lab demonstration | Fine-tuning dataset poisoning with stealthy backdoor triggers; commission-oriented | 2/5 |
| Reward Hacking in the Era of Large Models (arXiv 2604.13602, Apr 2026) | Academic survey | Documents reward hacking mechanisms in RLHF including intentional reward signal manipulation | 2/5 |
| Energy Loss Phenomenon in RLHF (arXiv 2501.19358, Jan 2025) | Academic research | Documents gradual capability degradation during RLHF optimization (accidental, not attacker-induced) | 3/5 |
| Natural Emergent Misalignment from Reward Hacking (Dec 2025) | Production observation | Production RL systems develop reward hacking behaviors that degrade model quality | 3/5 |
| Persistent Backdoor Attacks Under Continual Fine-Tuning (AAAI 2026) | Lab demonstration | Backdoors persist after fine-tuning on clean data; capability degradation patterns retained | 2/5 |

**Conclusion**: No documented in-wild intentional capability withholding attack on LLM systems confirmed. Evidence supports:
- Accidental RLHF reward hacking causes real capability degradation in production (Wild_vs_Theory 3/5)
- Intentional attacker-induced capability withholding remains theoretical (Wild_vs_Theory 1/5)
- Capability withholding is a valid taxonomic concept but lacks in-wild evidence

**Taxonomic placement recommendation**: Add as Category 13 note in threat-taxonomy.md — "Capability Withholding (distinct from commission attacks; no in-wild cases confirmed as of June 2026; Wild_vs_Theory 1/5 pending evidence)."

### Finding 2: Defense-in-Depth Interaction Conflicts

**Scope**: Interaction edge cases between PI-DEF-2 (RAG context labeling + load-time sanitization), AGENCY-DEF-1 (minimal tool permission allowlist + privilege separation), and AGENCY-DEF-2 (mandatory HITL for high-risk actions). (Canonical control IDs per `synthesis/defense-playbook.md`; earlier glosses said "output filtering"/"tool use policy/sandboxing".)

**Identified conflicts**:

1. **RAG Privilege Separation + Tool Allowlist Gap** (MEDIUM severity)
   - RAG document triggers legitimate tool call; PI-DEF-2 + AGENCY-DEF-1 architecture may block legitimate workflow without distinguishing injection from document-derived intent

2. **RAG Document → Tool Call Provenance Gap** (MEDIUM severity)
   - Privileged LLM cannot verify whether a tool call was derived from user input or from RAG document content; PI-DEF-2 strips document context that would enable provenance verification

3. **HITL Provenance Gap with PI-DEF-2 Enforcement** (MEDIUM severity)
   - Human approver cannot determine whether a proposed tool call originated from user intent or from a blocked injection attempt; reduces HITL effectiveness in RAG-heavy pipelines

4. **Cascading PI-DEF-2 + AGENCY-DEF-1 + AGENCY-DEF-2 interactions** (MEDIUM severity)
   - Layered defenses create interaction risks that reduce effective coverage vs. each individual defense

**Conclusion**: Defense-in-depth combinations (PI-DEF-2 + AGENCY-DEF-1 + AGENCY-DEF-2) produce cascading interaction edge cases not captured by individual defense analysis. These are deployment risks, not new attack techniques.

**Recommended filing**: Add "Defense Interaction Analysis" section to defense-playbook.md documenting these cascading edge cases.

---

## Contradictions

No major contradictions found. Existing literature consistently supports:
- No confirmed in-wild capability withholding attacks on LLMs
- Real production RL systems do exhibit reward hacking causing capability degradation
- Defense interaction gaps are architectural, not a conflict with existing defense assessments

---

## Open Questions

1. **Capability Withholding**: Whether stealthy capability suppression is distinguishable from normal model quality variance without behavioral baselines — this is an open detection problem
2. **Defense Interaction**: Whether RAG privilege separation architectures can be refined to pass document provenance context to the privileged LLM without defeating the purpose of privilege separation
3. **HITL Provenance**: Whether HITL interfaces can be redesigned to display blocked-injection context alongside tool call approval requests

---

## Round 14 Update: RLHF Energy Loss External Exploitability Determination

**Date: 2026-06-18**

**Research question resolved**: Can an external attacker induce capability withholding via training data poisoning without RLHF pipeline access?

**Provisional determination** (now documented in `synthesis/threat-taxonomy.md` Category 13 Addendum):

- **RLHF supply chain poisoning = [PROV] supply chain** — NOT achievable by external attacker. All documented RLHF poisoning attacks require insider access to the RLHF annotation pipeline, reward model training system, or preference data collection process. No documented path exists for an external attacker without RLHF pipeline credentials.

- **External attacker path via training data contamination** — Theoretical only. No demonstrated mechanism by which external training data contamination propagates through RLHF to produce targeted capability suppression. The gap between "poisoned training data" and "RLHF capability withholding via reward manipulation" is undemonstrated in the academic literature.

- **Accidental RLHF reward hacking** = [OPS] concern, Wild_vs_Theory 3/5 (production cases documented).

**Evidence for determination**:
- RLHFPoison (ACL 2024, aclanthology.org/2024.acl-long.140) — threat model assumes malicious RLHF annotator with pipeline access
- Universal Jailbreak Backdoors from Poisoned Human Feedback (Rando & Tramèr, 2024, spylab.ai/blog/poisoning-rlhf) — "malicious RLHF annotator creates harmful prompts"
- Sequential Data Poisoning in LLM Post-Training (arXiv 2606.04929, Jun 2026) — multiple adversaries with separate SFT and preference dataset access; pipeline access assumed
- ML Research to Prevent Catastrophic Data Poisoning (Forethought, Jan 2026, forethought.org) — external actor modeled for catastrophic secret loyalty; acknowledges external actor can perform catastrophic data poisoning but requires training pipeline access, not raw data ingestion
- **No academic paper documents an external-path-only capability withholding attack.**

**Defense interaction adversarial weaponization**: Confirmed already present in `synthesis/defense-playbook.md` Defense Layer 6 (lines 616, 628, 640, 652, 673). Content produced via editorial process (Round 13 reviewer challenge). Not a research pipeline gap.

**Both MEDIUM v1.3 research tasks: RESOLVED.**

---

## Sources

- BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents (ACL 2024) — `https://aclanthology.org/2024.acl-long.530.pdf`
- Revisiting Backdoor Attacks on LLMs (arXiv 2505.17601) — `https://arxiv.org/html/2505.17601v5`
- Reward Hacking in the Era of Large Models (arXiv 2604.13602, Apr 2026) — academic survey
- Energy Loss Phenomenon in RLHF (arXiv 2501.19358, Jan 2025) — capability degradation documentation
- Natural Emergent Misalignment from Reward Hacking (Dec 2025) — production RL observations
- Persistent Backdoor Attacks Under Continual Fine-Tuning of LLMs (AAAI 2026) — supply chain backdoor persistence
- Better Privilege Separation for Agents by Restricting Data Types (arXiv 2509.25926, Sep 2025) — defense interaction reference
- Taming Various Privilege Escalation in LLM-Based Agent Systems (arXiv 2601.11893, Jan 2026) — privilege escalation defense analysis

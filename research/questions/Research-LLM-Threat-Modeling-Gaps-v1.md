---
type: synthesis
title: "Research: LLM Threat Modeling — Operational Gaps v1.1"
created: 2026-06-17
updated: 2026-06-17
tags:
  - LLM-threat-modeling
  - operational-gaps
  - AIBOM
  - Chain-C
  - foreign-models
  - EU-AI-Act
status: complete
related:
  - "[[concepts/AIBOM-Trust-Anchor-Audit]]"
  - "[[concepts/Chain-C-Garak-Probe-Design]]"
  - "[[concepts/Foreign-Model-Regulatory-Mapping]]"
  - "[[entities/DeepSeek]]"
  - "[[entities/Alibaba-Qwen]]"
  - "[[sources/Sigstore-Model-Transparency-v1]]"
  - "[[sources/DeepSeek-Qwen-Privacy-Pitfalls]]"
sources:
  - "[[sources/Sigstore-Model-Transparency-v1]]"
  - "[[sources/DeepSeek-Qwen-Privacy-Pitfalls]]"
---

# Research: LLM Threat Modeling — Operational Gaps v1.1

## Overview

> **Note (superseded items):** This is a 2026-06-17 (framework v1.1) research artifact.
> Two claims below are superseded by later work: the "enforcement expected Q4 2026"
> dates (Q5 of `LLM-Threat-Modeling-Open-Questions-2026.md` and `assumptions.md` F1
> retract any fixed enforcement date — AI Office is in a preparation phase with no
> published enforcement as of mid-2026), and the GDPR fine figure (corrected to 4%/€20M
> inline below). Retained for research-trail continuity.

Three operational validation gaps from framework v1.1 research: AIBOM trust anchor audit, Garak Chain C probe design, foreign model regulatory mapping. Taxonomy saturated — no new threat categories needed. These are the remaining operational gaps before pilot deployment.

## Key Findings

### Gap 1: AIBOM Trust Anchor — `key_verified_via` Field

**Sigstore Model Signing v1.0 is the most operationally viable trust anchor** (Wild_vs_Theory: 3/5). It works at the CLI level and has documented HF/Kaggle API integration. Critical gap: no major HF publisher has documented Sigstore adoption as of mid-2026. The tooling exists; publisher workflow does not.

**HF verified publisher** is domain ownership only (Wild_vs_Theory: 2/5) — NOT weight provenance. The AIBOM field value `hf_verified_publisher` provides false confidence if interpreted as provenance verification.

**PGP** workflow is purely theoretical for HF (Wild_vs_Theory: 1/5). Should be deprecated from the schema.

**`none`** is the honest answer for most deployments (Wild_vs_Theory: 5/5) — but the template doesn't enforce the manual review process that `none` implies.

### Gap 2: Garak Chain C Probe Design

**Chain C** = multi-agent tool return value injection. The probe design is achievable (YAML config structure defined). The deeper gap is **architectural**: Garak's harness connects to a single LLM endpoint. Multi-agent N>2 propagation testing requires a new harness that can simulate sequential multi-agent turns. This is harness development, not probe development.

No current automated tool tests Chain C. Manual review required for multi-agent context propagation threats.

### Gap 3: Foreign Model Regulatory Mapping — EU AI Act Article 9

All three non-Western providers (DeepSeek, Qwen, MiniMax) operate in EU market **without documented Article 9 compliance** (Wild_vs_Theory: 3-4/5). Specific confirmed gaps:

- **No EU authorized representative** documented for any provider (Article 55(2) violation)
- **GDPR Article 46 transfer liability is confirmed** — China has no EU adequacy decision; EU deployers bear the transfer risk, not the provider
- **DeepSeek censorship documented** at Wild_vs_Theory 4/5 (Congressional committee + CNN)
- **Qwen GDPR exposure at 3/5** — Alibaba Cloud routing confirmed, transfer mechanism absent
- **MiniMax at 2/5** — limited evidence but same structural exposure

**Critical implication:** EU organizations using DeepSeek/Qwen/MiniMax API face GDPR fines up to **4% of global annual turnover or €20M** (GDPR Art. 83(5)) for transfer violations — this is a live compliance risk, not theoretical. (Correction: an earlier draft said "5%"; GDPR's top tier is 4%/€20M. The EU AI Act's higher 6–7% tiers are a separate instrument — see `synthesis/risk-matrix.md`.)

## Key Entities

- **DeepSeek**: Chinese LLM provider with confirmed censorship (4/5), confirmed Chinese infrastructure routing (4/5), no EU representative documented
- **Alibaba Qwen**: Alibaba Cloud API processing with same GDPR Article 46 exposure (3/5), documented Qwen-VL prompt injection vulnerabilities
- **MiniMax**: Less documented but same structural privacy exposure (2/5)
- **Sigstore**: OpenSSF project providing model signing + Rekor transparency log; v1.0 working but publisher adoption zero

## Key Concepts

- **AIBOM `key_verified_via`**: Trust anchor field with four values; operational reality diverges significantly from assumed semantics
- **Chain C propagation**: Tool return value injection in multi-agent systems; requires harness development, not just probe development
- **EU AI Act Article 55(2)**: Non-EU providers must designate EU authorized representative; enforcement expected Q4 2026
- **GDPR Article 46 transfer**: No adequacy decision for China; EU deployers bear liability for data transfers to Chinese LLM APIs

## Contradictions

No major contradictions found in this research round. The three gaps are complementary and non-overlapping.

## Open Questions

1. Has any major HF publisher (Meta, Mistral, Google) actually signed model weights with Sigstore? No evidence found. This is the critical missing piece for the AIBOM verification guide.
2. Does DeepSeek's compute fall below or above the 10^25 FLOPs EU AI Act systemic risk threshold? Unconfirmed.
3. Is there a documented GDPR Article 46 transfer mechanism for any Chinese LLM API provider? None found.
4. Does any external project address multi-agent test harnesses (not just probes)? Open architecture question.
5. When will EU national authorities begin GPAI enforcement? Expected Q4 2026 per regulatory analysis.

## so_what Gate Application

**Foreign model regulatory findings change a decision:** Previously the framework noted "foreign model privacy concerns" as theoretical. Now: **GDPR Article 46 transfer liability is confirmed** with specific article citations. Deployers must be informed they bear the transfer risk.

**AIBOM findings change a decision:** `hf_verified_publisher` was listed as a viable trust anchor. Now flagged as providing false confidence for weight provenance.

**Chain C findings confirm what was suspected:** No automated tool exists. Manual review required. Framework should note this explicitly in the red-teaming section.

## Files Created

- `synthesis.md` — master synthesis
- `sources/Sigstore-Model-Transparency-v1.md`
- `sources/DeepSeek-Qwen-Privacy-Pitfalls.md`
- `concepts/AIBOM-Trust-Anchor-Audit.md`
- `concepts/Chain-C-Garak-Probe-Design.md`
- `concepts/Foreign-Model-Regulatory-Mapping.md`
- `entities/DeepSeek.md`
- `entities/Alibaba-Qwen.md`
- `questions/Research-LLM-Threat-Modeling-Gaps-v1.md`

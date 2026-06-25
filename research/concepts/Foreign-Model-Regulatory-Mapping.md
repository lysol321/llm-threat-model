---
type: concept
title: "Foreign Model Regulatory Mapping — EU AI Act Article 9"
date_created: 2026-06-17
tags:
  - EU-AI-Act
  - Article-9
  - GPAI
  - foreign-models
  - DeepSeek
  - Qwen
  - MiniMax
  - regulatory
  - GDPR
related:
  - "[[sources/DeepSeek-Qwen-Privacy-Pitfalls]]"
  - "[[questions/Research: LLM Threat Modeling]]"
---

# Foreign Model Regulatory Mapping — EU AI Act Article 9

## Scope

This page maps EU AI Act obligations for non-Western GPAI providers (DeepSeek, Alibaba Qwen, MiniMax) operating in or serving EU markets.

## Relevant EU AI Act Provisions

### GPAI Provider Obligations (Article 53)
Providers of GPAI models that meet **systemic risk** threshold:
- Compute threshold: >10^25 FLOPs OR designated by national authority
- Obligations: technical documentation, conformity assessment, post-market monitoring, EU database registration

### Article 9: High-Risk Obligations for GPAI
When a GPAI model meets systemic risk criteria, its provider is subject to Article 9 high-risk obligations:
- Risk management system
- Data governance (training data lineage, bias handling)
- Transparency (technical documentation, user-facing disclosures)
- Human oversight (停用 conditions, human-in-the-loop)
- Accuracy, robustness, cybersecurity

### Article 55(2): Non-EU Provider Requirements
Non-EU GPAI providers must **designate an EU-based authorized representative** — a legal person in the EU who can receive official communications, cooperate with authorities, and be held accountable.

## Model-by-Model Exposure

### DeepSeek
**Wild_vs_Theory: 4/5**

| Obligation | Status | Evidence |
|-----------|--------|---------|
| EU authorized representative | Not documented | Required under Article 55(2) if offering in EU |
| GDPR Article 46 transfer mechanism | Absent | China has no adequacy decision; DeepSeek API routes through Chinese infrastructure |
| Technical documentation | Not published | DeepSeek publishes model cards but not EU Article 53(4) technical docs |
| Conformity assessment | Not undergone | No evidence of third-party assessment |
| EU database registration | Not registered | Systemic risk designation unclear (compute below threshold but may be designated) |

**Key evidence:**
- CNN reporting (Jan 2025): confirmed censorship on politically sensitive topics
- US Congressional Select Committee on CCP: DeepSeek report documenting censorship and ties to Chinese government
- Firewall blog (Mar 2025): API routing through Chinese infrastructure confirmed

### Alibaba Qwen
**Wild_vs_Theory: 3/5**

| Obligation | Status | Evidence |
|-----------|--------|---------|
| EU authorized representative | Likely required | Alibaba has EU presence; Qwen offered via API |
| GDPR Article 46 transfer mechanism | Absent | Alibaba Cloud infrastructure processing; China adequacy gap |
| Technical documentation | Not published | No EU AI Act documentation found |
| Conformity assessment | Not undergone | No third-party assessment |

**Key evidence:**
- Firewall blog (Mar 2025): Qwen API through Alibaba Cloud confirmed
- Security researchers: Qwen-VL prompt injection vulnerabilities documented (kelacyber.com)

### MiniMax
**Wild_vs_Theory: 2/5**

| Obligation | Status | Evidence |
|-----------|--------|---------|
| EU authorized representative | Unclear | MiniMax less prominent in EU market |
| GDPR Article 46 transfer mechanism | Unverified | Reddit reports of "zero retention" — not independently verified |
| Technical documentation | Not published | — |
| Conformity assessment | Not undergone | — |

**Key evidence:**
- Reddit community reports on MiniMax API privacy claims — not corroborated by security analysis

## Critical Findings

1. **All three providers operate in EU market without documented Article 9 compliance.** This is a live regulatory exposure, not theoretical.

2. **GDPR transfer liability falls on EU deployers**, not the foreign provider. Any EU organization sending data to DeepSeek/Qwen/MiniMax APIs bears the Article 46 transfer risk (potential fines up to 5% global revenue).

3. **Article 55(2) authorized representative requirement** means non-compliant providers can still serve EU customers through intermediaries — enforcement depends on national authority action.

4. **Enforcement timeline:** First GPAI enforcement signals expected Q4 2026 as national authorities scale up.

## so_what Gate Application

**Does this change a decision in the framework?**

Yes — it changes the risk rating for foreign model API usage by EU entities. Previously the framework noted "foreign model privacy concerns." Now we can state: **GDPR Article 46 transfer liability is a confirmed gap**, not theoretical.

**YAGNI:** This is not restated content. The foreign model regulatory dimension was flagged in the research brief but never substantiated. Now substantiated with specific article citations.

## Recommendation for Framework

Add regulatory compliance check to the foreign model assessment section:
- [ ] Provider has EU authorized representative (Article 55(2))
- [ ] Data flows documented with Article 46 transfer mechanism
- [ ] Technical documentation per Article 53(4) available
- [ ] EU database registration confirmed

## Open Questions

1. Has any EU national authority initiated investigation of non-compliant GPAI providers? Expected Q4 2026.
2. Is there a documented GDPR Article 46 mechanism for any Chinese LLM API provider? None found.
3. Does DeepSeek's compute fall below or above the 10^25 FLOPs systemic risk threshold? Unconfirmed.

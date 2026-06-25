---
type: entity
entity_type: AI model / cloud service
parent: Alibaba Cloud (Alibaba Group)
key_models:
  - Qwen 2.5
  - Qwen 2.5-VL (vision-language)
key_concerns:
  - API calls routed through Alibaba Cloud infrastructure
  - GDPR Article 46 transfer exposure
  - Prompt injection vulnerabilities documented in Qwen-VL
  - No documented EU authorized representative
confidence: medium-high
tags:
  - foreign-model
  - China
  - GPAI
  - privacy
  - Alibaba
related:
  - "[[concepts/Foreign-Model-Regulatory-Mapping]]"
  - "[[sources/DeepSeek-Qwen-Privacy-Pitfalls]]"
---

# Alibaba Qwen

## Overview

Qwen is a large language model family developed by Alibaba Cloud (Alibaba Group). Qwen 2.5 and Qwen 2.5-VL (vision-language) are available via API through Alibaba Cloud Model Studio.

## Security and Privacy Concerns

### Data Routing (Wild_vs_Theory: 3/5)
API calls processed through Alibaba Cloud infrastructure — confirmed by multiple security analysts. Same GDPR Article 46 transfer concern as DeepSeek: China has no EU adequacy decision, data transfers require a legal mechanism (Standard Contractual Clauses, etc.) that is not documented for Alibaba Cloud.

### Prompt Injection Vulnerabilities (Wild_vs_Theory: 3/5)
Security researchers at kelacyber.com documented prompt attack vulnerabilities in Qwen 2.5-VL. Attackers could inject malicious instructions through images that the model would follow.

### EU AI Act Exposure
- Article 55(2): Alibaba has EU market presence; Qwen offered via API likely requires authorized representative
- GDPR Article 46: Alibaba Cloud processing confirmed; transfer mechanism absent
- Conformity assessment: Not documented

## Wild_vs_Theory Summary

| Concern | Rating | Evidence |
|---------|--------|---------|
| API routing through Alibaba Cloud | 3/5 | Multiple sources confirm |
| GDPR transfer exposure | 3/5 | No adequacy decision for China |
| Prompt injection (Qwen-VL) | 3/5 | kelacyber.com documented |
| Censorship | 2/5 | Less documented than DeepSeek |

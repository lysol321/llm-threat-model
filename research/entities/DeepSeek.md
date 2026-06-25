---
type: entity
entity_type: AI company / model provider
founded: 2023
headquarters: Hangzhou, China
parent: High-Flyer Capital Management (quantitative hedge fund)
key_models:
  - DeepSeek V3
  - DeepSeek-R1
  - DeepSeek-Coder
key_concerns:
  - Censorship on politically sensitive topics (CCP, Taiwan, Tiananmen Square)
  - API calls routed through Chinese infrastructure
  - GDPR Article 46 transfer exposure for EU deployers
  - No documented EU authorized representative
confidence: high
tags:
  - foreign-model
  - China
  - GPAI
  - censorship
  - privacy
related:
  - "[[concepts/Foreign-Model-Regulatory-Mapping]]"
  - "[[sources/DeepSeek-Qwen-Privacy-Pitfalls]]"
---

# DeepSeek

## Overview

DeepSeek is a Chinese AI company developing large language models, backed by High-Flyer Capital Management (a quantitative hedge fund). Models include DeepSeek V3 and DeepSeek-R1. Known for competitive performance at lower cost than US counterparts.

## Security and Privacy Concerns

### Censorship (Wild_vs_Theory: 4/5)
Documented refusal to engage with questions about CCP criticism, Taiwan independence, Tiananmen Square. Confirmed by:
- CNN reporting (Jan 2025)
- US Congressional Select Committee on CCP report
- Reddit community documentation (r/DeepSeek censorship mega-thread)

### Data Routing (Wild_vs_Theory: 4/5)
API calls routed through Chinese infrastructure. Under China's Cybersecurity Law (2017) and Data Security Law (2021), Chinese companies can be compelled to share data with government authorities on request. No published transparency report or legal challenge mechanism.

### EU AI Act Exposure
- Article 55(2) EU authorized representative: Not documented
- GDPR Article 46: No adequacy decision for China; data transfer is a confirmed exposure
- Systemic risk threshold: DeepSeek V3 trained on ~2000 H800 GPUs — likely below 10^25 FLOPs but may be designated by national authorities

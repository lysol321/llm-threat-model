---
type: source
source_type: news-analysis
author: Diego Freire & Matthew T. Hays (The Firewall)
date_published: 2025-03-07
url: https://www.thefirewall-blog.com/2025/03/privacy-pitfalls-in-ai-a-closer-look-at-deepseek-and-qwen/
confidence: medium
key_claims:
  - DeepSeek V3/R1 developed by Chinese lab backed by High-Flyer Capital (quantitative hedge fund)
  - DeepSeek API calls routed through Chinese infrastructure — potential GDPR Article 46 transfer without adequacy decision
  - Alibaba Qwen API processed through Alibaba Cloud — same GDPR transfer concern
  - DeepSeek known to censor politically sensitive topics per multiple reports
  - Both models are cost-efficient but raise privacy concerns for EU/US enterprise use
tags:
  - deepseek
  - qwen
  - privacy
  - GDPR
  - foreign-models
  - EU-AI-Act
related:
  - "[[concepts/Foreign-Model-Regulatory-Mapping]]"
  - "[[entities/DeepSeek]]"
  - "[[entities/Alibaba-Qwen]]"
---

# Privacy Pitfalls in AI: DeepSeek and Qwen

## Summary

Analysis of privacy risks in two prominent non-Western LLMs: DeepSeek (Chinese lab, High-Flyer Capital backing) and Alibaba Qwen. Both models raise significant GDPR transfer concerns due to API routing through Chinese infrastructure.

## Key Findings

### DeepSeek
- Developed by Chinese lab with ties to High-Flyer Capital Management (quantitative hedge fund)
- DeepSeek V3 and R1 achieve competitive performance at lower cost than US models
- API calls routed through Chinese infrastructure
- Documented censorship behavior on politically sensitive topics (CCP, Taiwan, Tiananmen Square)
- GDPR transfer concern: data processed in China without adequacy decision → requires Article 46 transfer mechanism

### Qwen
- Alibaba Cloud infrastructure for API processing
- Same GDPR Article 46 transfer concern as DeepSeek
- Prompt injection vulnerabilities documented in Qwen-VL series
- Less documented censorship evidence than DeepSeek, but privacy concerns similar

## Wild_vs_Theory

| Model | Rating | Basis |
|-------|--------|-------|
| DeepSeek API routing concerns | 4/5 | Confirmed by multiple sources; GDPR transfer mechanism absent |
| DeepSeek censorship | 4/5 | Congressional committee + CNN + Reddit documentation |
| Qwen GDPR exposure | 3/5 | Alibaba Cloud confirmed; no adequacy decision for China |
| Qwen censorship | 2/5 | Limited documented evidence; less than DeepSeek |

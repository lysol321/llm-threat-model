# Malicious Hugging Face ML Models (JFrog / ReversingLabs Research)

## Source Details
- **Type:** Incident report / security research
- **URL:** https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-back/
- **Confidence:** High

## Key Claims
- Malicious ML models discovered on Hugging Face platform
- Attackers use custom model inference code for data exfiltration
- Particularly targets models with non-standard architectures requiring custom Python classes
- The attack surface is the custom code layer, not just the model weights

## Relevance
Concrete evidence of LLM03 supply chain risk in practice. Shows that model hub security is not just about weights — custom inference code is a vector.

## Attack Pattern
1. Attacker publishes model with benign-looking weights
2. Malicious code embedded in model's custom inference class
3. Organization deploys model without inspecting custom code
4. Custom code runs at inference time → exfiltration

## Open Questions
- Unknown how many malicious models went undetected
- Automated scanning of Hugging Face model submissions is limited

# Multimodal Prompt Injection Attacks

**Source Type:** Security Research / Blog
**Author:** Christian Schneider
**Date:** March 2026
**URL:** https://christian-schneider.net/blog/multimodal-prompt-injection/
**Confidence:** High

## Summary
Comprehensive analysis of how prompt injection attacks bypass text-only defenses by embedding malicious instructions in images, audio, and video processed by multimodal LLMs.

## Key Findings

### Attack Vectors

1. **Image-based prompt injection**: Malicious instructions hidden in images that are invisible to humans but legible to Vision-Language Models (VLMs). Success rates up to **82%** in research studies.

2. **Audio-based injection**: Instructions embedded in audio files that the LLM transcribes and follows.

3. **Video-based injection**: Frames with embedded prompts that persist through video processing.

### Research Evidence

- **Nature Communications (2025, Clusmann et al.)**: Used 594 attack samples to demonstrate that malicious instructions in medical images caused AI systems to produce harmful diagnostic outputs. Every VLM tested was vulnerable including Claude 3 Opus and GPT-4o.
- The prompts were invisible to human observers but perfectly legible to the models.

### Why Text-Only Defenses Fail

- Standard prompt injection defenses filter text inputs only
- Multimodal models process images, audio, and video as native content
- A prompt hidden in an image bypasses text filters entirely because it is not text when processed

### Defense Recommendations

1. **Input sanitization per modality**: Each input type (image, audio, video) needs its own sanitization layer before reaching the LLM
2. **Dual-LLM pattern**: One LLM evaluates the意图 of content before another LLM acts on it
3. **Output validation**: Validate LLM outputs before they trigger actions

## Relevance to Threat Model
Addresses reviewer gap: "Non-text injection vectors (image, audio, structured data)" — this was listed as a critical gap and this source directly fills it.

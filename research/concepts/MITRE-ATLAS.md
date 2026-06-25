# MITRE ATLAS — Adversarial Threat Landscape for AI Systems

## Overview
MITRE ATLAS (Adversarial Threat Landscape for AI Systems) is MITRE's framework documenting adversary tactics, techniques, and procedures targeting AI/ML systems. It is modeled after MITRE ATT&CK and provides a structured view of real-world and research-based threats to AI systems.

**URL:** https://atlas.mitre.org/
**Last Updated:** Continuously updated; 2025 version active
**Coverage:** 16 tactics, 84+ techniques (as of 2025)

## ATLAS vs ATT&CK
- ATLAS is to AI what ATT&CK is to traditional enterprise IT
- ATLAS techniques map to both real-world observations and academic red-team research
- Coverage spans model development, training, deployment, and inference phases

## Key Tactics (ATT&CK-style matrix)
Based on documented sources, ATLAS organizes techniques under:
1. **Reconnaissance** — gathering info on target ML system
2. **Resource Development** — acquiring infrastructure/models/data
3. **Initial Access** — gaining foothold in ML pipeline
4. **Model Training** — interfering with training process
5. **Inference** — attacking the deployed model
6. **Exfiltration** — stealing model/data
7. **Impact** — causing harm via the model

## Key Techniques (selected high-priority)
- **T0048: Model Poisoning** — adversarial data injected into training set
- **T0052: Model Replication** — stealing model via queries (model extraction)
- **T0054: Embedding Extraction** — extracting training data from embeddings
- **T0055: Prompt Injection** — crafting inputs to manipulate model behavior
- **T0056: Jailbreaking** — bypassing safety guardrails
- **T0057: Exfiltration via Model Output** — extracting data through responses
- **T0058: Supply Chain Compromise** — targeting model hub or preprocessing

## Real-World Incident Mapping
The framework is informed by documented incidents including:
- Academic model extraction attacks (e.g., CopyNN, KnockoffNN)
- Red-team findings against production LLM APIs (Azure, OpenAI, Google)
- Poisoned fine-tuning datasets on Hugging Face
- Prompt injection in ChatGPT plugins and Bing Chat

## Coverage of LLM-Specific Threats
ATLAS has dedicated coverage for LLM-specific attack surfaces:
- Inference-time attacks (prompt injection, jailbreaking)
- Training-time attacks (data poisoning, backdoor植入)
- Retrieval Augmented Generation (RAG) attack surface
- Multi-agent LLM system attack chains

## Source Quality
- **Type:** Threat intelligence framework (MITRE, US government-adjacent)
- **Confidence:** High — based on documented incidents + research
- **Use:** Primary reference for threat modeling LLM systems

## Related
- [[OWASP LLM Top 10]]
- [[STRIDE Threat Modeling for LLM]]

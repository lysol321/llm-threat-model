# LLM Supply Chain Security

## Overview
LLM supply chain security addresses the risks introduced when organizations rely on third-party models, data, and platforms. Unlike traditional software supply chains, LLM supply chains extend to training data provenance, pre-trained model weights, fine-tuning pipelines, and hosting infrastructure — creating a broader attack surface than conventional software dependencies.

**Reference:** OWASP LLM03:2025 Supply Chain

## Key Risk Categories

### 1. Traditional Software Dependencies
LLM applications depend on packages (langchain, llama-index, etc.) that may have:
- Known vulnerabilities (CVEs)
- Outdated or deprecated components
- Malicious packages (typosquatting, dependency confusion)

**Risk:** Attackers compromise the package ecosystem → LLM application compromised.

### 2. Third-Party Pre-trained Models
Organizations use base models from:
- **Commercial APIs** (OpenAI, Anthropic, Google) — risks: API key compromise, data exposure
- **Open-source model hubs** (Hugging Face, Replicate, Civitai) — risks: poisoned models, backdoored weights

**Critical attack: Silent Backdoor in Hugging Face models**
- Researchers (JFrog, ReversingLabs) discovered malicious ML models hosted on Hugging Face
- Models contained code exfiltration capabilities hidden in custom model code
- Particularly affects models with non-standard architectures requiring custom inference code

### 3. Fine-tuning and PEFT Attack Surface
New fine-tuning methods (LoRA, QLoRA, PEFT) introduce specific risks:
- **LoRA adapter poisoning** — low-rank adapters can be swapped with malicious versions
- **Fine-tuning data poisoning** — training data manipulation introduces backdoor triggers
- **Platform risks** — fine-tuning platforms (Axolotl, Unsloth) may have supply chain issues

### 4. Training Data Provenance
- Data sourced from web scraping may contain adversarial content
- Pre-trained models may have been trained on poisoned datasets
- Data licensing and consent issues (PII in training data)

### 5. Model Deployment Platforms
- On-device LLM SDKs increase supply chain risk
- Model hosting providers (AWS Bedrock, Azure OpenAI) have their own risk profiles
- Inference endpoint security (API key management, access controls)

### 6. AI Bill of Materials (AIBOM)
OWASP is developing an AIBOM standard to track:
- Model provenance and lineage
- Training data sources
- Fine-tuning datasets
- Infrastructure dependencies

## Attack Kill Chains

### Kill Chain A: Poisoned Fine-tune
```
1. Attacker identifies target organization's LoRA fine-tuning pipeline
2. Attacker contributes poisoned dataset to open dataset repository
   OR
   Attacker compromises fine-tuning platform's model registry
3. Organization fine-tunes base model on poisoned data
4. Backdoored model deployed to production
5. Attacker triggers backdoor via specific prompt pattern
6. Model exfiltrates data / executes attacker-chosen code
```

### Kill Chain B: Hugging Face Trojan
```
1. Attacker publishes model to Hugging Face with:
   - Legitimate model weights (to pass initial review)
   - Malicious custom inference code (in model card or custom class)
2. Organization downloads and deploys model
3. Custom code runs during inference → exfiltration/exploitation
4. Attacker gains access to organization's internal systems
```

### Kill Chain C: API Key Compromise
```
1. Attacker targets LLM API keys in:
   - Public code repositories
   - Leaked environment variables
   - Client-side code exposure
2. Abuses compromised keys for:
   - Unauthorized API access
   - Model extraction attacks (query-based replication)
   - Cost exhaustion
```

## Known Incidents
1. **Malicious Hugging Face models (2023-2024)** — ReversingLabs and JFrog identified models with embedded malware; custom inference code was used for exfiltration
2. **Poisoned training datasets** — researchers demonstrated training data poisoning attacks that implant backdoors in fine-tuned models
3. **Model extraction attacks** — query-based replication of GPT-4 class models demonstrated by academics

## Mitigations
1. **AIBOM** — maintain AI Bill of Materials for all models
2. **Model signing** — cryptographic verification of model weights
3. **Trusted model registries** — use only approved base models
4. **Sandbox inference** — run third-party models in isolated environments
5. **Custom code review** — inspect any custom inference code before deployment
6. **API key rotation** — automated rotation of LLM API keys
7. **Fine-tuning data vetting** — validate and scan fine-tuning datasets
8. **Dependency scanning** — use OWASP Dependency-Check or similar for LLM packages

## Source Quality
- **Type:** Community vulnerability report (OWASP, 2025)
- **Confidence:** High — based on documented incidents and practitioner research
- **Use:** Primary reference for supply chain threat modeling

## Related
- [[OWASP LLM Top 10]] (LLM03, LLM04)
- [[MITRE ATLAS]] (T0052 Model Replication, T0048 Model Poisoning)

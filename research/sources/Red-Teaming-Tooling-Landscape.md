# Red-Teaming Tooling Landscape: Garak, IBM ART, Giskard, PyRIT, PromptInject

## Overview

Automated red-teaming tooling for LLM systems has matured significantly. A 2025 study analyzing 214,271 attack attempts found automated red teaming achieved a **69.5% success rate** versus 47.6% for manual approaches. The tooling landscape divides into four functional categories: vulnerability scanners (probe-based), adversarial attack generators (LLM-augmented), traditional ML robustness tools, and purpose-built injection frameworks.

---

## 1. Garak (NVIDIA) — LLM Vulnerability Scanner

**Repository:** https://github.com/NVIDIA/garak
**License:** Apache 2.0
**Current Version:** v0.15+
**Python:** 3.10+

### What It Does
Garak (Generative AI Red-teaming & Assessment Kit) is the closest LLM equivalent to `nmap`/`Metasploit` for traditional security. It probes LLMs for specific vulnerability classes using static, dynamic, and adaptive probes.

**Core vulnerability categories covered:**
- Hallucination (factual confabulation, source fabrication)
- Data leakage (training data memorization, context exfiltration)
- Prompt injection (direct, indirect, multi-turn)
- Misinformation (false narrative generation)
- Toxicity generation (harmful content output)
- Jailbreaks (alignment bypass)
- Web injection (private data exfiltration via CSRF/XSS when model output reaches web contexts)

### Probe Architecture
Garak v0.15 ships with **120+ probe modules**. Each probe defines:
- **Trigger inputs** (adversarial prompts or patterns)
- **Generators** (ways of varying the trigger)
- **Detectors** (pass/fail criteria for vulnerability detection)

Key probe modules include:
- `garak.probes.hallucination` — factual inconsistency detection
- `garak.probes.prompt_injection` — direct and contextual injection
- `garak.probes.web_injection` — tests whether model output can trigger CSRF/XSS when rendered in a browser
- `garak.probes.misinformation` — false statement propagation
- `garak.probes.toxicity` — harmful output generation
- `garak.probes.jailbreak` — alignment bypass attempts

### CLI Usage Pattern
```bash
garak --model_type chat -m "gpt-4" --target http://localhost:8080
garak --target_file probes/prompt_injection.yaml
garak --list_probes
garak --list_detectors
```

### Output
- JSON/HTML report with per-probe pass/fail rates
- Groupable by module or by vulnerability class
- Designed for CI/CD integration

### Strengths
- Most comprehensive LLM-specific probe library (120+ modules)
- Covers both generation-time failures AND output-rendering risks (web_injection)
- Actively maintained by NVIDIA's AI Red Team
- Free, open source

### Gaps / Limitations
- Primarily a scanner, not an attack generator — cannot adaptively evolve attacks
- Does not natively handle multi-agent orchestration test scenarios
- Detection of sophisticated indirect prompt injection requires custom probe authoring

---

## 2. IBM ART (Adversarial Robustness Toolbox)

**Repository:** https://github.com/trusted-ai/adversarial-robustness-toolbox
**Foundation:** Linux Foundation AI & Data
**Current Version:** v1.17+
**Attack Methods:** 55+
**Defenses:** 30+

### What It Does
ART provides a broad ML security library covering **all traditional adversarial threat categories** plus emerging LLM support. Unlike Garak, ART targets the full ML model lifecycle.

**Attack Modules:**
- **Evasion** — adversarial examples designed to evade detection at inference time (APGD, Carlini-Wagner, Boundary Attack, DeepFool, etc.)
- **Poisoning** — training-time contamination (backdoor attacks, label flipping)
- **Extraction** — model stealing/蒸馏 attacks (including task-agnostic extraction)
- **Inference** — membership inference, property inference

### LLM-Specific Capabilities
- Primarily designed for classifier/DNN models, not chat models
- Supports text classifiers (word-level and character-level attacks)
- Recent additions for LLM-specific evasion scenarios
- Evasion attacks: TextFooler, HotFlip, Project Gradient Descent on text

### Framework Support
TensorFlow, Keras, PyTorch, MXNet, scikit-learn, XGBoost, LightGBM, CatBoost, GPy

### Strengths
- Most comprehensive traditional ML adversarial toolkit
- Formal verification and certification tools (unique in the market)
- Covers poisoning and extraction — phases often overlooked in LLM red-teaming
- Academic lineage — many published, peer-reviewed methods

### Gaps / Limitations
- Not designed for LLM-centric threats (prompt injection, jailbreaks, agentic chain exploitation)
- Text attacks focus on classifier evasion, not instruction-following model manipulation
- Interface is research-oriented, not operationally user-friendly for LLM app teams

### Coverage vs. Our 12 Threat Categories

| Threat Category | ART Coverage |
|----------------|-------------|
| Prompt Injection (direct) | Partial (text evasion techniques) |
| Prompt Injection (indirect) | Low |
| Supply Chain | None (model provenance) |
| Context Propagation | None |
| Multi-Agent Threats | None |
| Model Extraction | Medium (extraction attacks) |
| Hallucination | None |
| Data Leakage | Medium (membership inference) |
| Toxicity/Harmful Output | Medium |
| Jailbreak | None |
| RAG Vulnerabilities | None |
| Regulatory/Compliance | Certification tools |

---

## 3. Giskard

**Repository:** https://github.com/Giskard-AI/giskard-oss
**Focus:** Open-source LLM and ML testing
**OWASP Coverage:** OWASP LLM Top 10 categories

### What It Does
Giskard positions itself as the "CI/CD quality tool for LLMs" — detecting quality issues (hallucinations, RAG failures) alongside security vulnerabilities.

**Key capabilities:**
- Automated adversarial input generation across **OWASP LLM Top 10** categories
- Red-teaming for **agentic systems** — modular, multi-turn testing
- Hallucination detection with RAG-aware testing
- Prompt injection scanning
- Bias and toxicity detection
- Scan command: `giskard scan` on a model or pipeline

### Agentic System Testing
Giskard's agentic testing module is notable — it can:
- Simulate multi-turn conversations with tool use
- Test across RAG + agent integration points
- Generate adversarial scenarios dynamically

### Strengths
- OWASP LLM Top 10 mapping — practical alignment with industry standard threat taxonomy
- Agentic system red-teaming (distinguishes from static scanner approaches)
- Python library with integrations for MLflow, LangSmith, etc.

### Gaps / Limitations
- Less granular control than Garak for specific probe authoring
- Open-source with limited commercial support

### Coverage vs. Our 12 Threat Categories

| Threat Category | Giskard Coverage |
|----------------|-----------------|
| Prompt Injection (direct) | Yes |
| Prompt Injection (indirect) | Yes |
| Supply Chain | None |
| Context Propagation | Partial (agentic testing) |
| Multi-Agent Threats | Yes (agentic module) |
| Model Extraction | None |
| Hallucination | Yes (RAG-aware) |
| Data Leakage | Partial |
| Toxicity/Harmful Output | Yes |
| Jailbreak | Yes |
| RAG Vulnerabilities | Yes |
| Regulatory/Compliance | Partial |

---

## 4. PyRIT (Microsoft)

**Repository:** Azure Foundry / PyRIT public components
**Owner:** Microsoft AI Red Team
**Approach:** LLM-as-attack-generator

### What It Does
PyRIT (Python Risk Identification Tool) uses an **adversarially fine-tuned LLM** to generate attacks against target systems — different from Garak's probe-based approach. PyRIT crafts adaptive, multi-turn attacks based on observed target responses.

**Key features:**
- **Adaptive attack generation** — the red-team LLM adjusts attacks based on target responses
- Scenario-based testing with defined malicious prompt datasets
- Agentic AI red teaming support
- Supports multiple target types: chat models, agents, RAG pipelines

### Notable Limitation
PyRIT's public documentation is limited — the full capability set is primarily documented in Microsoft's internal red team use. CSA published an evaluation of PyRIT for agentic AI red teaming (2 days ago as of this research).

### Coverage vs. Our 12 Threat Categories

| Threat Category | PyRIT Coverage |
|----------------|----------------|
| Prompt Injection (direct) | Yes (adaptive) |
| Prompt Injection (indirect) | Yes (scenario-based) |
| Supply Chain | None |
| Context Propagation | Yes (agentic) |
| Multi-Agent Threats | Yes |
| Model Extraction | Partial |
| Hallucination | Partial |
| Data Leakage | Partial |
| Toxicity/Harmful Output | Yes |
| Jailbreak | Yes |
| RAG Vulnerabilities | Yes |
| Regulatory/Compliance | None |

---

## 5. TextFooler

**Type:** Traditional NLP adversarial attack tool
**Domain:** Text classification model evasion
**Role in LLM Security:** Component-level attacks on text-embedding models

### What It Does
TextFooler is a character/word-level adversarial attack tool targeting text classifiers. It generates minimal text perturbations (word substitutions, character-level edits) that cause classifier models to misclassify inputs.

### LLM Security Relevance
TextFooler-style attacks are relevant for:
- Evading DLP classifiers that gate LLM inputs
- Bypassing content moderation classifiers
- Crafting inputs that evade prompt injection detectors

**Not relevant for:** Direct prompt injection against chat LLMs — those require instruction-following manipulation, not classifier evasion.

### Relationship to IBM ART
TextFooler is one of many text attacks implemented within IBM ART's evasion module.

---

## 6. PromptInject (Purpose-Built)

**Role:** Research-grade prompt injection framework
**Approach:** Systematic injection pattern library

### What It Does
PromptInject provides a structured framework for composing and testing prompt injection attacks. Unlike end-to-end scanners, it focuses on the injection construction layer.

### Coverage
- Template-based injection composition
- Multi-stage injection chains
- Encoding evasion (Base64, URL encoding, Unicode homoglyphs)

---

## Tool Comparison Matrix

| Tool | Type | Probe Count | LLM-Native | Agentic | Adaptive | OWASP Map | License |
|------|------|-------------|------------|---------|----------|-----------|---------|
| **Garak** | Scanner | 120+ | Yes | No | Partial | Yes | Apache 2.0 |
| **IBM ART** | Attack Lib | 55+ attacks | No | No | N/A | Partial | Apache 2.0 |
| **Giskard** | Test Suite | ~50 | Yes | Yes | Yes | Yes (Top 10) | Apache 2.0 |
| **PyRIT** | Attack Generator | N/A | Yes | Yes | Yes | Yes | Microsoft EULA |
| **TextFooler** | Classifier Evasion | N/A | No | No | N/A | No | Academic |

---

## Coverage Against Our 12 Threat Categories

| Category | Primary Tool | Secondary Tool | Detection Coverage | Evasion Coverage |
|----------|-------------|----------------|-------------------|-----------------|
| Prompt Injection (direct) | Garak | PyRIT | High | Medium |
| Prompt Injection (indirect) | Garak | Giskard | Medium | Medium |
| Supply Chain | Manual (AIBOM) | JFrog/ReversingLabs | Low (no automated scanner) | N/A |
| Context Propagation | PyRIT (agentic) | Giskard | Low | Low |
| Multi-Agent Threats | Giskard (agentic) | Manual | Low | Low |
| Model Extraction | IBM ART | Garak (limited) | Medium | Medium |
| Hallucination | Garak | Giskard | High | N/A |
| Data Leakage | Garak | IBM ART | High | Medium |
| Toxicity/Harmful Output | Garak | Giskard | High | High |
| Jailbreak | Garak | PyRIT | Medium | Medium |
| RAG Vulnerabilities | Giskard | Garak | Medium | Low |
| Regulatory/Compliance | Giskard | IBM ART (certification) | Medium | N/A |

---

## Key Gaps in Current Tooling

1. **No tool covers Chain C attack patterns** (tool return value injection, N>2 agent propagation, system prompt contamination) — these require manual red-teaming
2. **AIBOM / supply chain scanning** — no automated tool validates HuggingFace model provenance; JFrog/ReversingLabs scan for malware signatures but not model behavioral trojans
3. **Context propagation attack detection** — no commercial or open-source tool specifically tests whether outputs in agent context windows influence subsequent agent behavior
4. **Underground PI market / jailbreak-as-a-service** — no tooling maps these external threats to internal system exposure
5. **Evasion+detection combined testing** — most tools either test detection OR test evasion, not both in a feedback loop

---

## Recommended Tool Stack for Engineering Teams

**Minimum viable stack:**
- `garak` — automated vulnerability scanning in CI/CD
- `giskard` — OWASP-aligned red team + agentic testing
- `ibm art` — for embedding classifier evasion testing

**Advanced stack:** Above + PyRIT for adaptive attack generation + manual Chain A/B/C kill chain exercises

---

## Sources

- Garak GitHub: https://github.com/NVIDIA/garak
- Garak Probes Doc: https://reference.garak.ai/en/latest/probes.html
- IBM ART GitHub: https://github.com/trusted-ai/adversarial-robustness-toolbox
- IBM ART ReadTheDocs: https://adversarial-robustness-toolbox.readthedocs.io/
- Giskard GitHub: https://github.com/Giskard-AI/giskard-oss
- PyRIT Microsoft: https://learn.microsoft.com/en-us/azure/foundry/concepts/ai-red-teaming-agent
- AppSec Santa ART Review: https://appsecsanta.com/art
- AppSec Santa Giskard Review: https://appsecsanta.com/giskard
- Promptfoo Red Teaming Guide: https://www.promptfoo.dev/docs/red-team/
- Promptfoo Top 5 Tools 2025: https://www.promptfoo.dev/blog/top-5-open-source-ai-red-teaming-tools-2025/
- QAwerk Tool Comparison: https://qawerk.com/blog/llm-red-teaming-tools/

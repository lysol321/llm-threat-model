# Garak — LLM Vulnerability Scanner

## Definition
Garak (Generative AI Red-teaming & Assessment Kit) is NVIDIA's open-source LLM vulnerability scanner — the closest analog to `nmap`/`Metasploit` for large language model security testing. It probes LLMs for specific vulnerability classes using 120+ modular probe configurations covering hallucination, prompt injection, data leakage, jailbreaks, toxicity, and web injection.

## Key Characteristics

| Attribute | Value |
|-----------|-------|
| Maintainer | NVIDIA AI Red Team |
| License | Apache 2.0 |
| Current Version | v0.15+ |
| Probe Count | 120+ |
| Language | Python 3.10+ |
| Repository | github.com/NVIDIA/garak |

## Probe Architecture

Each Garak probe defines three components:
1. **Trigger inputs** — adversarial prompts or patterns to send to the target
2. **Generators** — ways of varying the trigger (encoding, multi-turn context, etc.)
3. **Detectors** — pass/fail criteria for detecting the vulnerability

## Major Probe Modules

| Probe | Vulnerability Class | Description |
|-------|---------------------|-------------|
| `garak.probes.hallucination` | Hallucination | Tests for factual confabulation and source fabrication |
| `garak.probes.prompt_injection` | Prompt Injection | Direct and contextual injection attempts |
| `garak.probes.web_injection` | Web Injection | Tests if model output can trigger CSRF/XSS in browsers |
| `garak.probes.misinformation` | Misinformation | False narrative generation |
| `garak.probes.toxicity` | Toxicity | Harmful content output |
| `garak.probes.jailbreak` | Jailbreak | Alignment bypass attempts |
| `garak.probes.memorization` | Data Leakage | Training data memorization detection |

## Key Strength

The `web_injection` probe is particularly notable — it tests whether model outputs, when rendered in a web browser, can exfiltrate data via CSRF or inject scripts. This covers the indirect prompt injection attack surface where model output reaches third-party contexts.

## Limitations

- Primarily a scanner, not an attack generator — cannot adaptively evolve attacks based on target responses
- No native multi-agent orchestration testing
- Sophisticated indirect PI detection requires custom probe authoring
- Does not cover supply chain or AIBOM validation

## Relationship to Other Tools

- **vs. Giskard:** Garak is deeper on specific probe coverage; Giskard maps to OWASP LLM Top 10 and includes agentic testing
- **vs. PyRIT:** Garak is a probe-based scanner; PyRIT uses an adversarial LLM to generate adaptive attacks
- **vs. IBM ART:** IBM ART focuses on traditional ML adversarial threats; Garak is purpose-built for LLM instruction-following vulnerabilities

## Sources

- GitHub: https://github.com/NVIDIA/garak
- Documentation: https://reference.garak.ai/en/latest/probes.html
- arXiv paper: https://arxiv.org/abs/2406.11036

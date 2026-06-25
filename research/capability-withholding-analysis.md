# Capability Withholding Attack Analysis
**Research Round: Round 12 (follow-up from Round 7 Review)**
**Date: 2026-06-17**
**Wild_vs_Theory Rating: 1/5 (no LLM-specific in-wild evidence confirmed)**

## Definition
Capability withholding is a class of attack distinct from commission attacks (prompt injection, data exfiltration, tool poisoning). In a withholding attack, the adversary degrades the model's capability — making it less intelligent, less safe-aligned, or less useful — rather than manipulating it to perform specific harmful actions.

## Threat Model Distinction

| Attack Type | Mechanism | Taxonomy Category |
|---|---|---|
| Commission attack | Model is made to DO harm | Existing: Category 1 (Prompt Injection), Category 6 (Supply Chain) |
| Capability withholding | Model is made to BE less capable | Absent from current taxonomy |

## Evidence Found

### 1. BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents (ACL 2024)
- **Type**: Backdoor/trojan attack on fine-tuned LLM agents
- **Mechanism**: Attackers insert Trojan files into training data. When deployed, the agent executes Trojan files in production (malicious action) while appearing normal on clean data.
- **Relevance to capability withholding**: Partially relevant — the agent's normal capability is preserved while the backdoor activates only on specific triggers. This is more commission than withholding.
- **Wild_vs_Theory**: 2/5 — demonstrated in lab, no confirmed in-wild deployment
- **Source**: `https://aclanthology.org/2024.acl-long.530.pdf`

### 2. Revisiting Backdoor Attacks on LLMs: A Stealthy and Practical Poisoning Approach (arXiv 2505.17601, Oct 2025)
- **Type**: Fine-tuning dataset poisoning
- **Mechanism**: Malicious adversary poisons fine-tuning dataset to implant backdoor into LLM. LLM behaves normally on clean data but exhibits harmful behavior when trigger activated.
- **Relevance**: Commission-oriented (causes harmful action) rather than pure capability withholding
- **Source**: `https://arxiv.org/html/2505.17601v5`

### 3. Reward Hacking / Reward Over-Optimization in RLHF
Multiple papers document that RLHF-trained LLMs are susceptible to reward hacking, where the agent exploits flaws in the reward function to achieve high reward scores without genuinely improving capability:

- **"Reward Hacking in the Era of Large Models" (arXiv 2604.13602, Apr 2026)**: Comprehensive survey of reward hacking mechanisms in LLMs including RLHF. Documents cases where optimization-based prompt injection exploits reward model flaws.
- **"Energy Loss Phenomenon in RLHF" (arXiv 2501.19358, Jan 2025)**: Identifies gradual capability degradation ("energy loss") as a mechanism of reward hacking — models lose capability during RLHF optimization without obvious misalignment.
- **"Natural Emergent Misalignment from Reward Hacking in Production RL" (Dec 2025)**: Documents cases where production RL systems develop reward hacking behaviors that degrade model quality/capability.
- **"Mitigating Reward Hacking in RLHF via Bayesian Non-negative Matrix Factorization" (arXiv 2602.10623, Feb 2026)**: Documents that reward hacking degrades output quality.

**Relevance to capability withholding**: HIGH — this documents actual capability degradation via RLHF reward hacking. An attacker who controls the reward signal (supply chain attack on RLHF pipeline) could intentionally suppress capability.

**Wild_vs_Theory**: 2/5 for intentional suppression attacks (no documented in-wild intentional capability withholding); 3/5 for accidental reward hacking causing capability degradation (edge cases documented in production RL).

### 4. Persistent Backdoor Attacks Under Continual Fine-Tuning of LLMs (AAAI 2026)
- **Type**: Supply chain backdoor
- **Mechanism**: Backdoors persist even when a compromised model is fine-tuned on clean data. Tests persistence of backdoor when developer fine-tunes compromised model on clean dataset.
- **Relevance**: Documents supply chain risk where backdoored base models retain degraded capability patterns even after fine-tuning
- **Source**: `https://ojs.aaai.org/index.php/AAAI/article/view/40295/44256`

### 5. Real-World Incident: LiteLLM Supply Chain Attack (March 2026)
- **Type**: Software supply chain attack (PyPI credential compromise)
- **Mechanism**: Attacker hijacked litellm maintainer accounts, inserted backdoor into litellm (AI gateway library)
- **Impact**: Exposed AI credentials, Kubernetes clusters, developer systems
- **Wild_vs_Theory**: 4/5 — confirmed in-wild incident
- **Note**: This is a software supply chain attack on the AI gateway, not a model capability withholding attack. Relevant as supply chain precedent.

## Capability Withholding Attack Patterns

### Pattern 1: Intentional RLHF Reward Hacking (Attacker Controls Reward Signal)
- **Attack surface**: Compromised reward model or reward signal in RLHF pipeline
- **Effect**: Model optimized to appear capable while degrading actual task performance
- **Evidence base**: Theoretical (no documented in-wild case)
- **Wild_vs_Theory**: 1/5

### Pattern 2: Trojan Trigger Suppression
- **Attack surface**: Fine-tuning dataset poisoning with stealthy triggers
- **Effect**: Model capability selectively suppressed when trigger present (adversary knows trigger, deployer doesn't)
- **Evidence base**: Lab demonstration (BadAgent, Persistent Backdoor papers)
- **Wild_vs_Theory**: 2/5

### Pattern 3: Gradual Reward Hack Degradation
- **Attack surface**: Accidental RLHF reward hacking that degrades model capability over time
- **Effect**: Production RL deployment causes gradual capability loss
- **Evidence base**: Production RL cases documented (Energy Loss paper, Emergent Misalignment Dec 2025)
- **Wild_vs_Theory**: 3/5 for accidental degradation; 1/5 for intentional attack

## Mitigation Approaches
- Behavioral baselining (monitor output quality metrics over time)
- Diversified model sources (reduce single-source RLHF pipeline exposure)
- Output quality monitoring with statistical anomaly detection
- AIBOM provenance for RLHF reward models (prevent reward signal tampering)

## Taxonomic Placement Recommendation
Capability withholding is distinct from Category 1 (Prompt Injection — commission) and Category 6 (Supply Chain Attacks — commission via poisoning). It should be noted as a separate sub-type or Category 13 with Wild_vs_Theory 1/5 pending evidence.

## Open Questions
1. No documented in-wild intentional capability withholding attack on LLM systems confirmed
2. Whether "energy loss" phenomenon in RLHF is exploitable by an external adversary or only an internal RLHF operator
3. Whether stealthy capability suppression is distinguishable from normal model quality variance without behavioral baselines

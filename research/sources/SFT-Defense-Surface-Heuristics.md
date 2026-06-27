# SFT Defense Surface Heuristics (ACL 2026)

**Source Type:** Research paper (ACL 2026)
**Authors:** Not specified (ACL proceedings)
**Date:** 2026
**URL:** https://aclanthology.org/2026.acl-long.540/
**Confidence:** High (peer-reviewed conference paper)

## Summary
Demonstrates that Supervised Fine-Tuning (SFT) does not reduce the attack surface — it merely reshapes it. Attackers who probe the defense surface can identify shortcuts that bypass SFT defenses with ~50% reduction in attack queries. Provides heuristics for analyzing defense surface properties.

## Key Claims

### 1. SFT Does Not Reduce Attack Surface
- SFT defense achieves **up to 40% accuracy drops** (not 10-14% as previously misattributed)
- However, this does not mean the attack surface is smaller
- SFT merely reshapes the attack surface — the total area of vulnerability remains the same
- Attackers can find shortcuts that bypass SFT defenses

### 2. Defense Surface Shortcuts
- Attackers who probe the defense surface can identify shortcuts
- Shortcuts allow bypass of SFT defenses with **~50% reduction in attack queries**
- This means SFT defenses are brittle against adaptive attackers
- The shortcut mechanism: find regions of the input space where SFT has not been applied

### 3. Heuristics for Defense Surface Analysis
- Provides heuristics for analyzing defense surface properties:
  - **Coverage**: How much of the input space is covered by SFT?
  - **Continuity**: Are there gaps in the SFT coverage?
  - **Robustness**: How much perturbation can SFT withstand?
- These heuristics allow defenders to predict whether SFT will be effective

### 4. Practical Implications
- SFT alone is insufficient for defense
- SFT must be combined with other defenses (output filtering, input filtering)
- Regular probing of the defense surface is needed to identify shortcuts
- The heuristics provide a framework for evaluating SFT effectiveness

## Relevance to Threat Model

### Direct Mapping to Existing Threat Model
- **Defense control D5.2.3 (Context Isolation)**: SFT is a form of context isolation
  - The paper shows that SFT does not reduce the attack surface — it reshapes it
  - This validates the need for layered defenses: SFT + output filtering + input filtering
- **Defense interaction analysis**: SFT interacts with other defenses
  - SFT alone is brittle — must be combined with output filtering
  - The paper confirms the defense-in-depth approach
- **Defense ownership tags**: SFT is [DEV] owned — correctly positioned

### Wild_vs_Theory Assessment
- The paper provides theoretical analysis of SFT defense properties
- The heuristics are validated empirically
- Combined with the output filtering evaluation, the practical implications are clear
- **Wild_vs_Theory: 4/5** (theoretical analysis with empirical validation)

### Defense Implications
- SFT should not be the only defense — must be combined with output filtering
- Regular probing of the defense surface is needed to identify shortcuts
- The heuristics provide a framework for evaluating SFT effectiveness
- SFT is a necessary but insufficient defense layer

## Open Questions
- How do the heuristics apply to different SFT approaches (full fine-tuning vs LoRA)?
- Can the shortcuts be patched without retraining?
- How does SFT interact with other defenses (input filtering, output filtering)?
- What is the cost of regularly probing the defense surface?

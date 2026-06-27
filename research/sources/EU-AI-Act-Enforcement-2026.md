# EU AI Act Enforcement State (2026)

**Source Type:** Regulatory analysis / Policy tracker
**Date:** June 2026
**URLs:**
- https://artificialintelligenceact.eu/the-act/high-level-summary/
- https://artificialintelligenceact.eu/tracker/
- https://www.covington.com/enforcement-tracker
- https://www.globalcompliancenews.com/2025/03/05/37778/
- https://www.reuters.com/sustainability/ai-laws-regulation-global-tracker/
- https://www.emergo.com/en/blogs/eu-ai-act-in-force-an-overview-of-requirements-and-obligations
- https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- https://digital-strategy.ec.europa.eu/en/policies/gpai

**Confidence:** High (official EU sources, law firm analysis)

## Key Claims

### 1. GPAI Model Obligations: Effective August 2, 2026
- EU AI Act entered into force August 1, 2024
- GPAI model provider obligations (Article 51+) enforceable **Aug 2, 2026**
- Model providers must provide: technical documentation, training content summaries (copyright), model evaluation results, adversarial testing documentation, cybersecurity safeguards
- High-capability model providers must also perform adversarial testing and report systemic risks
- Fines: up to €15M or 3% of global turnover (whichever higher)

### 2. High-Risk AI: Provisionally Pushed to December 2027
- Initial enforcement for high-risk systems: Aug 2, 2027
- **May 7, 2026:** EU Council adopted a "Strategic Omnibus" agreement
  - Introduces 42-month transition from formal entry-into-force before application of most high-risk requirements
  - **Implies Dec 2027 for high-risk obligations**
  - Simplifies compliance via internal control (self-assessment) for some systems, reduced conformity assessment
- Omnibus agreement **not yet formally adopted** as of June 2026 — still awaits Council and Parliament approval
- Uncertainty remains on final timeline

### 3. Member State Implementation: Lagging
- 10/27 member states have established competent authorities (Art. 68)
- 8/27 have designated national supervisory authorities
- 11/27 nominated notifying authorities
- Member state enforcement of national rules delayed to August 2, 2027

### 4. Scope and Enforcement Gap
- The regulation is in force since Aug 2024
- Most high-risk systems: no enforcement for ~3 years after entry into force
- Non-compliance: criminal penalties may be imposed
- Key implication: organizations building high-risk AI systems have limited near-term regulatory pressure

## Relevance to Threat Model

### Direct Impacts
- **GPAI providers** (OpenAI, Anthropic, Google, Meta): Aug 2, 2026 obligations on documentation, evaluation, cybersecurity
- **High-risk AI deployers**: delayed enforcement creates compliance gap — systems may be deployed without meeting standards
- **Foundation model developers**: training data transparency, copyright compliance, safety testing documentation required

### Indirect Impacts on Defense Strategy
- GPAI model-level security obligations (adversarial testing, cybersecurity) align with threat model defense recommendations
- Member state implementation lag means cross-border enforcement inconsistent
- Omnibus simplification may reduce compliance burden for lower-risk systems
- Organizations should not wait for enforcement — compliance gap is itself a risk factor

### Connection to Existing Threat Model
- Supports defense controls D5.2.2 (Adaptive Output Filter), D5.3.3 (Audit Trail), D5.7.1 (Adversarial Testing)
- Aligns with existing regulatory controls for banking, insurance, healthcare
- GPAI cybersecurity requirements create legal basis for model hardening investments

## Open Questions
- Will the Omnibus agreement pass through Parliament unchanged? (Timeline uncertain)
- What specific adversarial testing standards will GPAI providers be held to?
- How will member states enforce penalties on non-EU model providers?
- Does "cybersecurity safeguards" in Art. 55 include specific requirements for model isolation, access control, or monitoring?

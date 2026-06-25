---
type: source
source_type: technical-documentation
author: Sigstore / Google Open Source Security Team
date_published: 2025-04-04
url: https://blog.sigstore.dev/model-transparency-v1.0/
confidence: high
key_claims:
  - Sigstore Model Signing v1.0 launched April 2025, built on sigstore-python
  - CLI: `model_signing sign` and `model_signing verify` with OIDC identity providers
  - Integrates with HuggingFace and Kaggle at API level (not native UI)
  - Rekor transparency log provides public, tamper-evident audit trail
  - Library mode available for programmatic integration into training pipelines
tags:
  - sigstore
  - model-signing
  - AIBOM
  - supply-chain
  - trust-anchor
related:
  - "[[concepts/AIBOM-Trust-Anchor-Audit]]"
  - "[[concepts/Sigstore-Model-Signing]]"
---

# Sigstore Model Transparency v1.0

## Summary

Sigstore's Model Signing project (v1.0, April 2025) brings transparent, tamper-evident signatures to ML models. Built on sigstore-python + Rekor transparency log. Enables verification that model weights haven't been modified post-signing and that the signer identity is authenticated via OIDC.

## Key Technical Details

### CLI Usage
```bash
pip install model-signing
model_signing sign ${MODEL_PATH}
model_signing verify ${MODEL_PATH} \
  --signature ${SIGNATURE} \
  --identity ${IDENTITY} \
  --identity_provider ${OIDC_PROVIDER}
```

### OIDC Identity Providers
Supported: Google, GitHub, Microsoft — workforce identity providers. Not suitable for anonymous publishers.

### Model Hub Integration
Integration documented for HuggingFace and Kaggle at the API level:
- Verify on upload: check signature before accepting a model
- Sign on upload: sign models during the upload workflow

### Limitation
No native HF UI button. Requires custom implementation by the HF platform team or by operators building their own verification pipeline.

### Rekor Transparency Log
All signatures recorded in Rekor — a public, append-only transparency log. Even if signing keys are compromised, the log makes it auditable.

## Relevance to AIBOM

This is the most operationally viable trust anchor for `key_verified_via` field. The Rekor log addresses the "how do you trust the trust anchor" problem.

## Wild_vs_Theory: 3/5

Working v1.0 with documented CLI, but limited in-wild deployment evidence. No major HF publisher has documented Sigstore adoption as of mid-2026.

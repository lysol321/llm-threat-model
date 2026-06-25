---
type: concept
title: "AIBOM Trust Anchor Audit"
date_created: 2026-06-17
tags:
  - AIBOM
  - supply-chain
  - trust-anchor
  - sigstore
  - HuggingFace
related:
  - "[[sources/Sigstore-Model-Transparency-v1]]"
  - "[[questions/Research: LLM Threat Modeling]]"
---

# AIBOM Trust Anchor Audit

## Definition

The AIBOM `key_verified_via` field enumerates trust anchors for model weight verification. The field had four values: `hf_verified_publisher`, `sigstore`, `pgp`, `none`. None had an operational verification path for HuggingFace.

## Operational Reality Per Value

| Value | What It Actually Verifies | Gap |
|-------|-------------------------|-----|
| `hf_verified_publisher` | Domain ownership of HF namespace only | NOT weight provenance, NOT training data, NOT absence of trojan |
| `sigstore` | Cryptographic signature via Sigstore + Rekor transparency log | No native HF UI; requires custom pipeline; publisher must sign |
| `pgp` | PGP key signing | No documented HF workflow; purely theoretical |
| `none` | No verification | Honest answer — requires manual review process |

## Sigstore Model Signing v1.0 — Step-by-Step Verification Path

1. Download model weights from HuggingFace
2. Obtain signature file + signing certificate from publisher (not in HF UI — out-of-band)
3. Run: `model_signing verify model.bin --signature model.sig --identity publisher@domain.com --identity_provider https://accounts.google.com`
4. Check Rekor log: signature must appear with matching timestamp
5. Verify OIDC identity matches publisher's stated identity

## Critical Gap

**Publisher adoption is zero for Sigstore on HuggingFace.** No major publisher (Meta, Mistral, Google) has documented Sigstore signing as of mid-2026. The tooling exists but the workflow requires publishers to actively sign, which none have committed to publicly.

## Recommendation

1. **For assessment template:** Add caveat to `hf_verified_publisher` option: "verifies account control, NOT weight provenance."
2. **For quick-start guide:** Include Sigstore verification step-by-step with explicit note that it depends on publisher adoption.
3. **Flag as operational gap in framework:** `key_verified_via` is compliance theater until publisher signing becomes standard.

## Wild_vs_Theory Summary

- HF verified publisher: 2/5 (domain ownership only, no provenance)
- Sigstore v1.0: 3/5 (working tool, limited adoption)
- PGP: 1/5 (theoretical only)
- `none`: 5/5 (honest — but template doesn't enforce manual review)

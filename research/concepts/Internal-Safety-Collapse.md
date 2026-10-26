# Internal Safety Collapse (ISC / “ICS”) — Research Reference

**Date:** 2026-06-24
**Status:** Confirmed research finding; operational scope depends on attacker-controlled harness execution
**Confidence:** HIGH for the failure mode; MEDIUM for public benchmark/repo details that differ across paper vs repository releases; LOW/UNVERIFIED for broader incident claims not directly supported by the paper/repo.

---

## Executive Takeaway

Internal Safety Collapse is best modeled as a **harness-control attack**, not as ordinary prompt injection and not as a role-only “model host” problem.

The practical threat condition is:

> **A target LLM or agent executes a task/validator/data harness the attacker controls or meaningfully shapes.**

More formally: **a target LLM or agent executes a task/validator/data harness whose relevant components are controlled or meaningfully shaped by the attacker.**

If there is no harness execution, ordinary inference consumers are usually **LOW/N/A** for ISC. If there is a harness, any role can become in-scope: model provider, self-hosted operator, agent platform, eval runner, fine-tuning/data-generation pipeline, code-repair workflow, or enterprise consumer that wraps provider inference in an attacker-shaped workflow.

---

## What ISC Is

ISC is a structural failure mode where an aligned model generates harmful or sensitive content while trying to complete a legitimate-looking professional task. The key distinction is that the model is not following a direct malicious instruction. It infers that unsafe content is functionally required to satisfy the task.

The arXiv paper defines the failure as a model transitioning into a “zero-safety” state while executing otherwise legitimate tasks, because it infers that generating sensitive content is necessary for task completion.

**Not prompt injection:** the attack does not rely on overriding instructions.
**Not just misuse:** the model is pursuing task completion under workflow pressure.
**Not role-bound:** the trigger is attacker-controlled harness execution.

---

## The TVD Mechanism

TVD means **Task + Validator + Data**.

| Component | Role in attack | Threat-model translation |
|---|---|---|
| Task | A legitimate professional objective, often framed as debugging, evaluation, dataset completion, validation, code repair, or analysis | The user-facing work request appears benign or defensible |
| Validator | Programmatic or procedural checks that reject incomplete output | The model receives a concrete pass/fail pressure signal |
| Data | Incomplete or placeholder fields the model must fill to satisfy the validator | Unsafe content becomes the “missing value” required for success |

ISC happens when these combine so that the only way to satisfy the validator is to fill in harmful/sensitive data. The model’s task-completion behavior outruns its safety behavior.

---

## Correct Threat Boundary

### In scope — HIGH / CRITICAL

ISC applies when an attacker can control or meaningfully shape a harness that the target model/agent will execute, including:

- submitted eval harnesses;
- code/test repair tasks;
- validator schemas or tests;
- uploaded project files or datasets;
- tool results that become harness state;
- marketplace skills/plugins/agents;
- customer-provided workflows;
- fine-tuning or dataset-generation loops;
- agentic “read → run → fix → validate” workflows.

### Usually out of scope — LOW / N/A

Plain inference consumption is usually LOW/N/A when all of these are true:

- no task/validator/data harness is executed;
- no attacker-supplied validator, schema, test, or incomplete dataset is accepted;
- output is not fed into fine-tuning, evals, code repair, datasets, or tools;
- the user is only consuming provider inference for chat, summarization, classification, or drafting.

### Important nuance

“Internal-only harness” is not automatically ISC. If no attacker-controlled material enters it, the relevant risk is ordinary QA, supply-chain, or data-governance risk. It becomes ISC when an attacker can shape the harness components or the state that the harness validates.

---

## Evidence From Primary Sources

### arXiv:2603.23509 — *Internal Safety Collapse in Frontier Large Language Models*

Verified from arXiv metadata and HTML:

- Authors: Yutao Wu, Xiao Liu, Yifeng Gao, Xiang Zheng, Hanxun Huang, Yige Li, Cong Wang, Bo Li, Xingjun Ma, Yu-Gang Jiang.
- Published: 2026-03-04.
- Categories: cs.CL, cs.AI, cs.CR.
- Introduces TVD as the construction method for ISC.
- Reports **ISC-Bench: 53 TVD scenarios across 8 professional disciplines**.
- Reports that each scenario triggered ISC in at least one frontier model, with **no model proactively refusing the task pattern**.
- Reports worst-case safety failure rates averaging **95.3%** across four frontier models on three representative scenarios under JailbreakBench criteria.
- Reports agentic execution can be triggered by a single high-level instruction such as “complete this task,” with the model autonomously reasoning through context and filling missing content.
- Reports higher failure on authentic tasks than fabricated tasks, indicating the failure is linked to recognition of real task requirements rather than obvious adversarial deception.

### GitHub: `wuyoscar/Internal-Safety-Collapse`

Verified from README/raw repository text:

- Frames ISC as a “structural, workflow-level vulnerability.”
- Describes “task wins” behavior: task completion and debugging can dominate safety alignment under workflow pressure.
- Public release intentionally limits examples to lower-risk text contexts and says it avoids real-world operational content.
- Repository release references **84 codebase templates across 9 domains**, which appears to be broader than the arXiv paper’s 53-scenario/8-discipline benchmark. Treat these as different release states, not a contradiction to hide.
- Provides three experiment modes: single-prompt simulated workflow, in-context learning, and agentic workflow.

### Promptfoo LM Security DB

Verified from Promptfoo page:

- Describes ISC as occurring when restricted content generation is nested inside standard execution constraints, such as schema/debugging validation.
- Emphasizes that prompt-level safety filters fail because the prompt looks like a routine technical workflow.
- Lists impact as extraction of high-fidelity restricted content through task-completion behavior and claims standard input-level defenses fail because the prompts contain no explicit malicious instruction.

### SafeRedirect paper: arXiv:2604.20930

Verified from arXiv metadata and HTML:

- Authors: Chao Pan, Yu Wu, Xin Yao.
- Published: 2026-04-22.
- Categories: cs.CR, cs.AI, cs.LG.
- Treats ISC as a task-completion conflict, not a normal jailbreak.
- Reports existing input-level defenses have 100% failure against ISC and standard prompt defenses only partially mitigate it.
- Proposes **SafeRedirect**, which redirects task-completion drive rather than suppressing it.
- Key defense principles:
  - explicit permission to fail the task;
  - deterministic hard-stop output;
  - preserve harmful placeholders unresolved;
  - condition specificity.
- Reports SafeRedirect reduced average unsafe generation from **71.2% to 8.0%** across seven frontier LLMs in tested AI/ML-related single-turn ISC tasks, compared with 55.0% for the strongest baseline.

### Evidence update — 2026-10-26 scan

Scan window: after the 2026-09-19 review, plus one earlier independent paper the corpus had not cited. The rating stays at **2/5**. No field incident is attributed to ISC or to validator-harness abuse.

**Independent controlled replication**

- **Liu, Wang, Luo, Jia, arXiv:2607.00481 (2026-07-01).** No author overlap with Wu et al.
  - The team ran TVD-Single as a one-shot baseline using the released templates. JailbreakBench ASR per model: GPT-4o 38%, GPT-5.4 70%, Qwen3-Max 98%, Gemini-3-Flash 28%, DeepSeek-V4-Flash 95%, Claude-Sonnet-4.5 87%. The average is 69.3%; SafeBench-Tiny averages 70.7%.
  - The authors conclude the vulnerability is not uniformly exposed across frontier models.
  - **Use:** independent reproduction of the controlled single-turn failure, with large model-to-model variance. It is still not field evidence.

**Author-group work (not independent)**

- **VEX-Bench, arXiv:2609.35028 (2026-09-28).** Shares co-authors with Wu et al. (Huang, Wu, Li, Zheng). It uses ISC as one of seven misinformation-generation methods. ISC output showed the smallest factual degradation of the seven methods, which makes it the hardest to detect without direct source comparison.
- **HarmProfile, arXiv:2608.14577 (2026-06-11).** Same author group. It characterizes harmful-output distributions; the ISC README says it uses ISC-generated outputs.

**Changes in the authors' repository** (`wuyoscar/Internal-Safety-Collapse`)

- **NeurIPS 2026 acceptance:** claimed in PR #131 (merged 2026-09-27). Not confirmed against a NeurIPS listing; arXiv still shows only v1, with no venue.
- **Validator bug fix:** PR #135 (2026-10-15) fixed a label-parsing bug in the LlamaGuard text templates, where `"safe" in "unsafe"` is true. The old parser failed 40 of 50 label cases. The authors state that historical results are not recomputed. Effect on the paper's numbers is not established, because the paper judges harm with a separate evaluator. The lesson for defenders is that a validator's own logic can be wrong; this is the authors' own harness, not an attack.
- **Chat demos:** the README says these "simulate commands and results; the validator does not actually run" and can be treated as a prompt-based attack. Evidence from executed-validator agent runs should be kept separate from chat simulations.
- **Headline figure:** the README's 92% figure is the single-turn mean. The paper's 95.3% is a worst case across tasks and settings. Do not interchange them.
- **Model testing:** the authors stopped adding model tests in August 2026. Their 62-model evidence table mixes setups and is mostly author- or circle-contributed.
- **Fable 5 entry:** the table lists a 2026-06-09 Claude Fable 5 trigger posted by the lead author (community folders for fake news and NSFW content). Treat it as author self-report, context only. It does not support the press claims listed under "Claims to Remove or Downgrade".

**Critiques**

- **Wu, Zhu, Zhang, Yu, arXiv:2607.27951 (2026-07-30).** Independent and theoretical. It states that SafeRedirect "obtains much of its mitigation by permitting task failure and unresolved placeholders". That is a capability and utility trade-off, and a theoretical assistance floor remains.
- **ICML review (author-reported, second-hand).** On 2026-10-18 the authors briefly added a README note, removed the same day, saying ICML 2026 rejected the paper in April and that one reviewer called ISC an exaggerated phenomenon.
- **Replication:** no failed replication was found.

**Not found**

- No garak, PyRIT or promptfoo ISC probe.
- No press coverage in the window.
- Agent incidents during evaluations, driven by task-completion pressure and listed in a community tracker, were not verified. They are endogenous behavior, not attacker-shaped harnesses, so they are not ISC.

---

## What the Threat Model Should Say

### One-line definition

ISC is a harness-mediated failure mode where an LLM/agent generates unsafe content because an attacker-controlled task/validator/data harness makes that content appear necessary for successful task completion.

### Applicability gate

Use this decision tree:

1. **Harness execution:** Does the deployment execute task/validator/data, eval, test, code-repair, dataset-generation, fine-tuning, or autonomous workflow harnesses?
   - No → ISC LOW/N/A.
   - Yes → continue.
2. **Attacker control:** Can an attacker control or meaningfully shape any harness component or state: task, validator, schema, test, incomplete data, uploaded document, tool result, marketplace skill, external dataset, or customer integration?
   - No → ordinary QA/supply-chain/data-governance risk; not an ISC attack path.
   - Yes → continue.
3. **Completion pressure:** Does the model need to fill missing content to satisfy a validator, repair a failing test, complete an eval, populate a dataset, or make an autonomous workflow pass?
   - No → lower ISC risk; monitor composition.
   - Yes → continue.
4. **Downstream use:** Is the output returned, actioned, stored, evaluated, used for fine-tuning, inserted into a dataset, used in code/test repair, or passed to tools without independent semantic safety review?
   - Yes → ISC HIGH/CRITICAL.

---

## Control Implications

### Primary control: harness validation, not just prompt filtering

The validator must be inspected for **semantic safety**, not merely syntax/completion.

Required checks:

- reject validators that require filling unsafe placeholders;
- detect schemas/tests that make harmful content the only passing output;
- flag attacker-controlled task + validator + incomplete data combinations;
- require semantic safety review before model output is returned or used downstream;
- isolate untrusted harnesses in sandboxed execution;
- prevent generated data from flowing into fine-tuning/eval/dataset pipelines without independent review.

### Safe failure should be an allowed task outcome

SafeRedirect’s core insight is directly useful for the corpus: the model needs a valid task-completion path that does not require harmful completion. The system should permit and reward:

- failing the test safely;
- leaving placeholders unresolved;
- returning a deterministic refusal artifact;
- preserving original incomplete fields rather than repairing them with unsafe content.

### Monitoring signals

Log and alert on:

- repeated placeholder replacement requests;
- validators that fail until content fields are populated;
- user-supplied schemas/tests/eval scripts;
- agent loops that repeatedly read errors and patch data;
- generated content being routed into fine-tuning/eval/dataset stores;
- task bundles that combine benign professional framing with missing sensitive examples.

---

## Claims to Remove or Downgrade Unless Independently Verified

The current corpus should avoid treating the following as established by the arXiv paper alone:

- “Fable 5 globally pulled within 48 hours”;
- “US government issued export controls”;
- “100+ experts published open letter”;
- “traffic analysis confirmed output came from fallback routing”;
- “under 5 seconds” as a general benchmark fact;
- “53 scenarios across 9 domains” if referring specifically to arXiv:2603.23509 — the paper says 53 across 8 disciplines; the repository references 84 templates across 9 domains.

These may belong in a separate incident-history section only if backed by independent sources. They should not be used as the core evidence for ISC. The core evidence is already strong without them.

---

## Threat Model Integration Updates Needed

- `synthesis/threat-taxonomy.md`: replace role-only wording with attacker-controlled harness execution; fix benchmark numbers.
- `synthesis/assessment-template.md`: revise ISC Risk Rating 1.6 first gate to start with harness execution + attacker control.
- `synthesis/quick-reference.md`: add plain inference N/A path and attacker-controlled harness HIGH/CRITICAL path.
- `synthesis/asset-inventory.md`: add TVD harness assets.
- `synthesis/defense-playbook.md`: incorporate SafeRedirect-style safe-failure controls into `ISC-DEF-1` or add a new control.
- `synthesis/risk-matrix.md`: separate evidence confidence from deployment applicability.
- `review/red-team-2026-06-24-second-pass.md`: keep corrected “attacker-controlled harness execution” framing.

---

## Sources

| Source | URL | What it supports |
|---|---|---|
| Wu et al., 2026, arXiv:2603.23509 | https://arxiv.org/abs/2603.23509 | ISC definition, TVD, 53 scenarios, 8 disciplines, 95.3% worst-case failure rate, agentic execution finding |
| arXiv HTML v1 | https://arxiv.org/html/2603.23509v1 | Full paper text used for extracted claims |
| GitHub repository | https://github.com/wuyoscar/Internal-Safety-Collapse | Public benchmark/release framing, workflow-level vulnerability, experiment modes, release-safety caveats |
| Promptfoo LM Security DB | https://www.promptfoo.dev/lm-security-db/vuln/frontier-llm-safety-collapse-908a4285 | Security-database summary and schema/validation framing |
| Pan, Wu, Yao, 2026, arXiv:2604.20930 | https://arxiv.org/abs/2604.20930 | SafeRedirect mitigation, defense failure rates, safe-failure design principles |
| SafeRedirect HTML v1 | https://arxiv.org/html/2604.20930v1 | Full mitigation paper text used for extracted claims |
| Liu, Wang, Luo, Jia, 2026, arXiv:2607.00481 | https://arxiv.org/html/2607.00481v1 | Independent TVD-Single re-run, Table II and §V-B |
| Huang, Wu et al., 2026, arXiv:2609.35028 | https://arxiv.org/abs/2609.35028 | Author-group use of ISC for misinformation generation |
| Ma, Wu et al., 2026, arXiv:2608.14577 | https://arxiv.org/abs/2608.14577 | Author-group harmful-output profiling |
| Wu, Zhu, Zhang, Yu, 2026, arXiv:2607.27951 | https://arxiv.org/html/2607.27951v1 | §4.3 SafeRedirect utility caveat |
| Repository PR #131 | https://github.com/wuyoscar/Internal-Safety-Collapse/pull/131 | NeurIPS 2026 acceptance claim (author-reported) |
| Repository PR #135 | https://github.com/wuyoscar/Internal-Safety-Collapse/pull/135 | LlamaGuard label-parsing fix; historical results not recomputed |

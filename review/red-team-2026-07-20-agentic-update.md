# Red-Team Review — July 2026 Agentic Threat-Model Update

**Date:** 2026-07-20 UTC
**Scope:** Current uncommitted working-tree update
**Verdict:** **REQUEST CHANGES**

> **Remediation status (2026-07-20): RESOLVED in the v1.9 working tree.** The findings below preserve the pre-remediation review record. The repair added evidence-calibrated scores, canonical subtype IDs, worksheet control routing, nine agentic scenarios, foundation assets/assumptions, structured control data, regenerated HTML, and one release manifest. Verification commands and release state are recorded in `synthesis/release-manifest.md`.
>
> **Fresh-verifier follow-up:** A subsequent independent pass found stale v1.7 per-scenario declarations, visible v1.8 HTML labels, generic relay Impact 5, and missing canonical metadata on the relay/computer-use branches. The follow-up repair synchronized all 25 scenarios to v1.9 conditions, changed relay risk to base 4/elevated 8, added branch severity/goal/prerequisites/node IDs, and added `build-html.py --check` as a generated-artifact gate.

The update adds relevant agentic-era threats, but the corpus is not yet coherent enough to call the model updated or pilot-ready. The principal failure is operational traceability: the new risks exist in addenda, while the structured source, worksheet scoring path, scenario suite, framework summary, and version headers still describe the pre-update corpus.

## Findings

### HIGH — New controls cannot be scored in the engineering worksheet

**Evidence**

- `synthesis/assessment-template.md:140-149` routes Section 2 answers only to the pre-update controls.
- `synthesis/assessment-template.md:151-231` provides YES/PARTIAL/NO/N/A rows and PARTIAL definitions only for the pre-update controls.
- `synthesis/assessment-template.md:893-909` adds applicability questions for `MEM-DEF-1`, `SKILL-DEF-1`, `MA-DEF-3`, `CUA-DEF-1`, `RELAY-DEF-1`, and trajectory monitoring, but it is placed after the document footer and does not provide rating rows, N/A rules, PARTIAL definitions, or residual-risk handling.

**Why it matters**

The framework claims that a non-expert team can complete a valid assessment in under four hours. The new addendum can identify that a surface exists, but it cannot evaluate whether the corresponding control is implemented or feed that result into residual-risk math.

**Required fix**

Move the addendum into Section 2, extend the Section 2 → Section 3 routing table, add Section 3 control rows and PARTIAL/N/A definitions for every new control, and state which controls are preventive versus detection-only.

### HIGH — The evaluation suite still validates the v1.7 corpus and none of the new attack paths

**Evidence**

- `evaluation/scenario-suite.json` contains no references to persistent memory, skill lifecycle compromise, inter-agent identity escalation, computer-use visual attacks, or response-path tampering.
- Its metadata says every scenario was run against the “same v1.7 corpus.”
- `scripts/test_scenario_suite.py:4-8` still defines the quality bar as exactly sixteen scenarios.
- `scripts/test_scenario_suite.py:64-65` hard-codes sixteen scenarios.

**Why it matters**

The scenario suite passes, but only because it does not exercise the newly added HIGH-risk overlays or their defenses. Passing validation is therefore not evidence that the updated model works operationally.

**Required fix**

Add focused scenarios for at least persistent cross-session memory poisoning, malicious skill retrieval/update, inter-agent identity spoofing, computer-use visual injection, and relay tampering. Update suite metadata and tests to describe the new corpus version and coverage contract.

### HIGH — The provisional risk addendum contradicts the matrix’s own evidence and scoring rules

**Evidence**

- `synthesis/risk-matrix.md:24` defines likelihood 3 as “documented in wild.”
- `synthesis/risk-matrix.md:233-237` assigns likelihood 3, impact 5, and HIGH score 15 to five new overlays.
- The source note characterizes several supporting items as research benchmarks, vendor red-team findings, or architectural risks rather than independently corroborated production incidents: `research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md:17-19,25-27,33-35,41-43`.
- `synthesis/risk-matrix.md:241` says not to raise an overlay to HIGH without evidence meeting the Wild_vs_Theory rule, while the table immediately above already assigns HIGH score 15.
- The addendum uses `Starting score` plus an `Elevation condition`, but provides no base/elevated score pair or explicit changed axis, unlike the machine-checkable schema defined at `synthesis/risk-matrix.md:41`.
- The same evidence gap appears as HIGH surface labels in `synthesis/attack-surface-catalog.md:379-384`.

**Why it matters**

This overstates certainty and reintroduces the prose-only elevation ambiguity the v1.7 correction pass was designed to remove.

**Required fix**

Separate applicability, evidence confidence, base risk, and deployment elevation. Assign explicit Wild_vs_Theory values. Use base/elevated columns with a named changed axis. Keep lab/benchmark-only paths below likelihood 3 unless the framework’s structural-evidence exception is explicitly invoked and its three conditions are demonstrated for that row.

### HIGH — Response-path tampering has contradictory severity and an unavailable assurance claim

**Evidence**

- `synthesis/threat-taxonomy.md:461-467` treats response-path tampering as provisional because a single preprint does not establish a Wild_vs_Theory rating.
- `synthesis/risk-matrix.md:238-241` assigns it 2 × 5 = 10/MEDIUM and prohibits promotion without corroboration.
- `synthesis/attack-surface-catalog.md:384` nevertheless labels an unauthenticated relay HIGH.
- `synthesis/quick-reference.md:193-194` presents `RELAY-DEF-1` as unconditionally REQUIRED whenever a relay exists.
- `synthesis/defense-playbook.md:894-900` says the agent must detect whether it received the upstream-authorized response, but authenticating the relay and hashing its transcript cannot prove what the upstream provider authorized. An authenticated malicious relay can generate its own internally consistent transcript. The same section acknowledges provider signatures only “where supported.”

**Why it matters**

The first-read artifacts erase the stated provisional status and can give teams false assurance. End-to-end provenance requires an upstream-provider-authenticated response or a direct trusted path; relay-originated MACs and logs prove only what the relay claims.

**Required fix**

Keep the surface MEDIUM/provisional until corroborated. Split `RELAY-DEF-1` into controls that are currently implementable and an explicit unresolved provider-signature gap. Do not claim upstream authorization when only the relay is authenticated.

### HIGH — The machine-readable source of truth and generated HTML are stale

**Evidence**

- `threat-model-data.json:3` declares itself the source of truth for `llm-threat-model.html`.
- `threat-model-data.json:4-6` still identifies v1.8 dated 2026-06-24.
- Neither `threat-model-data.json` nor `llm-threat-model.html` contains the new threat/control identifiers or attack paths.
- Neither file is changed in the current working tree.
- `README.md:21-25` directs users to the HTML viewer first, making the stale artifact the default user path.

**Why it matters**

Users of the HTML artifact receive the old model, while Markdown readers receive the addendum. The repository therefore has two materially different threat models.

**Required fix**

Update `threat-model-data.json`, regenerate `llm-threat-model.html` with `scripts/build-html.py`, and add a consistency test ensuring the structured source includes all canonical new control IDs and risk overlays.

### HIGH — Release and version metadata describe multiple incompatible corpus states

**Evidence**

- `synthesis/framework.md:3-6` still describes the June 24 v1.8 comparable-framework release as pilot-ready.
- `synthesis/framework.md:104-120` still says the framework has three complete attack chains and does not mention the new overlays or controls.
- `synthesis/release-manifest.md:3-5` still declares the June 24 release, and `:15-24` lists pre-update file versions.
- The July update inventory at `synthesis/release-manifest.md:42-52` omits the modified `risk-matrix.md` and `quick-reference.md`.
- Updated files retain old top-level versions while placing newer versions or dates after their previous footers: `threat-taxonomy.md:3,406,477`; `attack-surface-catalog.md:3-4,369,401`; `attack-trees.md:3-4,214,704`; `defense-playbook.md:3-4,917-919`; `quick-reference.md:3,172,200`; `assessment-template.md:3-4,885-909`.

**Why it matters**

A team cannot determine which versions form a coherent release. Several documents effectively contain one official version plus a post-footer document fragment.

**Required fix**

Choose one release version/date, update each document’s primary header and footer, move addenda into the normal document structure, update `framework.md` revision notes and architecture summary, and make the release manifest’s included-version table authoritative.

### MEDIUM — The stated 30-day research window excludes the strongest corroborating source

**Evidence**

- `research/sources/Last-30-Days-Agentic-Threat-Updates-2026-07.md:3` defines the window as 2026-06-20 through 2026-07-20.
- `:13-19` relies on Microsoft’s June 4 article as broad corroboration.
- The source note explicitly labels the May response-tampering paper as outside the window at `:9,53-59`, but does not apply the same caveat to Microsoft.

**Why it matters**

The source is useful, but the provenance description is inaccurate and makes the “last 30 days” method look selectively applied.

**Required fix**

Either widen the research window and state it honestly, or classify the Microsoft article as pre-window corroboration rather than a last-30-days finding.

### MEDIUM — Maximum impact is assigned from surface presence rather than demonstrated blast radius

**Evidence**

- `synthesis/risk-matrix.md:31-33` defines Impact 5 as catastrophic or organization-wide compromise.
- Every new HIGH overlay receives Impact 5 at `synthesis/risk-matrix.md:233-237`.
- Their conditions establish only that a vulnerable path exists, such as dynamic skill selection, self-asserted identity, state-changing visual actions, or missing trajectory monitoring. They do not require broad privilege, sensitive assets, irreversible actions, or organization-wide reach.

**Why it matters**

Applicability is not evidence of catastrophic impact. Uniform Impact 5 inflates default risk and prevents deployment-specific calibration.

**Required fix**

Use lower base impact values and elevate only when explicit privilege, asset sensitivity, action irreversibility, and blast-radius predicates are present.

### MEDIUM — Foundation documents can suppress the new threats before scoring begins

**Evidence**

- The prescribed workflow reads assumptions and assets before attack surfaces and scoring.
- `synthesis/asset-inventory.md:256-344` has no durable-memory store, skill registry/embedding, agent identity credential, relay transcript/signing key, or representation-provenance asset.
- `synthesis/assumptions.md:165-167` assumes A2A channels represent authenticated trust, while the new threat includes unauthenticated or self-asserted inter-agent identity.

**Why it matters**

Teams following the framework in order can omit the assets and trust boundaries needed to make the new assessment questions applicable.

**Required fix**

Update assumptions, assets, and trust-boundary checklists before the surface catalog. Distinguish authenticated transport from authenticated agent identity and authorized privilege.

### MEDIUM — New threats and representation controls lack canonical identifiers

**Evidence**

- The taxonomy introduces new concepts as prose under overlapping categories at `synthesis/threat-taxonomy.md:413-475`, while its canonical cross-reference index remains unchanged at `:375-391`.
- Names drift between “Durable agent memory,” “Persistent memory poisoning,” and the combined Category 9 heading.
- Representation-boundary mitigation has no control ID at `synthesis/defense-playbook.md:913-915` or `synthesis/risk-matrix.md:239`.

**Why it matters**

The corpus cannot reliably join taxonomy entries, surfaces, controls, risks, scenarios, and machine-readable data when concepts have only prose names.

**Required fix**

Assign stable subtype and control IDs, add them to the cross-reference table, and use the same canonical names throughout the corpus.

### MEDIUM — Attack-tree extensions are inserted before the canonical chains they extend

**Evidence**

- `synthesis/attack-trees.md:130-214` contains extensions for Chains A, B, and C and a v1.4 marker.
- Canonical Chain B begins at `:218`; canonical Chain C begins at `:293`.
- The document’s old v1.3 footer remains at `:704`.
- The response-relay and computer-use branches lack IDs, severity, mission goals, prerequisite notation, and node identifiers.

**Why it matters**

Readers encounter the extension to Chains B/C before their base definitions. The mid-document version marker also makes the update look like an insertion artifact rather than part of the threat model.

**Required fix**

Place each branch under its canonical chain or create a properly linked new section after all base chains. Keep version metadata only in the document header/footer.

### MEDIUM — Several new conclusions overgeneralize the cited evidence

**Evidence**

- The representation-confusion source is a single reverse-engineering-domain preprint, but `synthesis/threat-taxonomy.md:469-475` generalizes it to arbitrary code, metadata, generated evidence, and tool-returned records.
- `synthesis/attack-trees.md:166-180` composes memory poisoning, later retrieval, identity assertion, and privilege escalation into one mandatory linear chain and says it terminates “only” when four separate controls are enforced. The source note reports memory poisoning and inter-agent trust as separate findings and does not prove that exact chain or exclusivity claim.

**Why it matters**

The threat directions are plausible, but the text converts narrow or separate observations into universal architectural requirements.

**Required fix**

Mark these as hypotheses to test, narrow the representation claim to demonstrated domains, and replace “only” with non-exclusive disruption points supported by architecture analysis.

## Verification performed

- Citation drift detector: **98/98 valid**
- Scenario test suite: **PASS**, but against the stale sixteen-scenario/v1.7 coverage contract
- Markdown corpus verifier: **0 malformed tables, 0 broken local links, 0 trailing-whitespace issues**
- jDocMunch health: **2,408 sections, 0 broken links, 0 stale sections**
- Structured/HTML diff check: **neither source-of-truth artifact changed**

## Recommended correction order

1. Repair release/version coherence and move post-footer addenda into normal document structure.
2. Make the risk overlays evidence-calibrated and machine-checkable; correct the response-path assurance claim.
3. Update assumptions, assets, canonical IDs, and cross-references.
4. Thread new controls through worksheet routing, scoring rows, PARTIAL/N/A rules, and residual-risk math.
5. Update `threat-model-data.json` and regenerate the HTML artifact.
6. Add and validate new scenario-suite cases.
7. Re-run citation drift, Markdown integrity, scenario tests, structured/HTML consistency checks, and a final corpus review.

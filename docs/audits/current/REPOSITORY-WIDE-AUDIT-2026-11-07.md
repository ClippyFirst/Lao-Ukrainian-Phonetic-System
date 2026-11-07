# Repository-wide audit and documentation checkpoint — 2026-11-07

## Executive assessment

**Engineering status: verified research prototype with a deployed static web instrument. Linguistic/release status: not independently validated and not release-ready.**

The repository's main architecture is coherent. Canonical Lao registries, evidence provenance, Python runtime, browser runtime, generated browser data, schemas, tests, scripts and documentation have distinct ownership boundaries. A broad directory migration would add churn without addressing a demonstrated defect. The work in this checkpoint therefore corrects documentation drift, improves discoverability and records the real branch/PR topology rather than duplicating existing plans or reorganizing stable code.

The primary linguistic pipeline remains:

`Lao source orthography → structural analysis → source-language phonology → typed IPA → Ukrainian target adaptation → Ukrainian practical orthography`.

The optional romanization route is a separate, lower-information orthographic method. It is not a fallback for uncertain or unsupported phonetic analysis.

## Scope, evidence and limits

Inspected the current default-branch README and workflow, the selected implementation branch's README, documentation index, master handoff, audit index, current audit, linguistic completion register, typed IPA adapter contract, system specification, validation guide, web architecture, contribution/agent instructions, package metadata, LICENSE, repository audit script, benchmark report, Python/browser engine change inventory, relevant tests/fixtures, open PR records, branch inventory and hosted workflow evidence.

The five supplied engineering/design references were rechecked at their public current release/source pages. Their methods are treated as guidance, not dependencies.

This is a repository structure, documentation, branch reconciliation and engineering-evidence audit. It is not an independent Lao phonology adjudication, legal opinion, local clean-install test, manual accessibility audit, or a claim that every linguistic rule is empirically correct. Connector-based repository inspection did not provide a local checkout, so no local commands or local test results are claimed.

## Repository and branch baseline

- Repository: `ClippyFirst/Lao-Ukrainian-Phonetic-System`.
- Default branch: `main`.
- Inspected `main` head: `f40c1128302486b3589da9b16bae198ef3ad1d81`.
- Selected working branch for this continuation: `improve/rule-engine-error-analysis-20261107`.
- The selected branch compares as **211 commits ahead, 0 behind** `main`. Its latest verified code/test checkpoint is `2ddb0dbb250268f2477a2614a1f3fc676a9b89e3`.
- `main` was not modified by this continuation.
- The branch inventory returned: `main`, `benchmark/mekongphon-three-engine`, `benchmark/mekongphon-immutable-inference-20261107`, `improve/rule-engine-error-analysis-20261107`, and `audit/repository-documentation-and-mekongphon-rights-20261107`.

### Open PR topology

At inspection, PRs **#137, #138, #139 and #140** were open and unmerged.

| PR | Branch / role | Relationship and disposition |
|---|---|---|
| [#137](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/137) | `benchmark/mekongphon-three-engine` | Deterministic engine and three-engine benchmark work, based on `main`. Preserve; do not duplicate or merge blindly. |
| [#138](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/138) | `audit/repository-documentation-and-mekongphon-rights-20261107` | Separate optional neural-provider and rights-review stack based on #137. |
| [#139](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/139) | `benchmark/mekongphon-immutable-inference-20261107` | Immutable-revision inference benchmark, stacked on #137. |
| [#140](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/140) | `improve/rule-engine-error-analysis-20261107` | Aggregate error diagnostics, conservative tone-selector refinements and full-pipeline registry reuse, stacked on #139. |

The #138 audit/neural branch and #140 rule-engine branch are **diverged**, not successive commits on one linear branch: comparison reports a common merge base at `main`, with #140's branch 211 commits ahead and the #138 branch 88 commits ahead of `main`. Their changes were not merged or copied wholesale. In particular, the optional neural-provider integration and its separate rights-review document belong to #138's stack; they are not silently represented as present in the selected #140 branch. This avoids mixing two independently reviewable implementation stacks.

## Architecture and ownership map

| Area | Canonical location | Responsibility and ownership |
|---|---|---|
| Python API and CLI | `src/lao_ukrainian/` | Normalization, structural parsing, source phonology, typed IPA result, Ukrainian adaptation and CLI |
| Canonical Lao data | `data/lao/*.csv` | Consonants, onset clusters, vowels, tone selectors and Ukrainian IPA correspondences |
| Evidence registry | `data/evidence/` | Source metadata and claim-to-source traceability |
| Benchmark/gold contracts | `data/benchmark/`, `schemas/`, `scripts/ipa_gold_corpus.py` | Benchmark provenance, rights metadata, gold schemas, split and corpus validation |
| Generated browser data | `web/data.js` | Generated mirror of canonical CSV data; never hand-edit |
| Browser runtime | `web/` | Native ES modules, browser engine/UI and separate romanization adapter |
| Static pages | `index.html`, `system.html` | Converter and methodology/system page |
| Build and research scripts | `scripts/` | Audit, generation, static build, corpus validation and external-engine benchmarks |
| Tests | `tests/`, `web/engine.test.js` | Python, browser, shared-fixture, schema, corpus and UI regressions |
| Documentation | `docs/`, root README, `AGENTS.md`, `CONTRIBUTING.md` | Product contract, methodology, implementation map, evidence, audit and handoff |

The Python and browser engines are separately maintained implementations that share canonical registries and selected fixtures. Cross-runtime parity is a defined contract for shared supported cases, not a blanket assumption for all normalization, segmentation or malformed-input behavior.

The optional romanization path remains distinct from the phonetic IPA-first path. It parses source-aware syllable structures and cannot reconstruct tone or pronunciation distinctions absent from the romanization.

## Findings and corrections in this checkpoint

| ID | Priority | Status before this checkpoint | Finding | Correction / acceptance |
|---|---|---|---|---|
| DOC-012 | P1 | PARTIAL | README described the romanization mode as an “optional fallback”, contradicting the IPA adapter contract and later README text that explicitly says it is not a fallback. | Reworded it as a separate, lower-information orthographic method that is never used when phonetic analysis is unresolved. |
| DOC-013 | P1 | PARTIAL | README listed automatic segmentation of unspaced multi-syllable text as an unresolved limitation, while the current Python and browser contracts describe conservative dynamic segmentation into complete orthographic syllables within each whitespace-delimited token. | Reworded the limitation as lexical word-boundary detection. The parser can structurally segment supported syllables; it does not infer lexical words. |
| DOC-014 | P2 | PARTIAL | `docs/validation.md` begins with historical test counts and an old workflow, which can be mistaken for current verification. | Added a prominent exact-head status note and links to the current audit and canonical handoff. Historical entries remain intact. |
| DOC-015 | P2 | PARTIAL | The audit index pointed to the 2026-11-06 structure audit as its current audit, despite later code, benchmark and branch changes. | Added this 2026-11-07 repository-wide checkpoint as current and retained the 2026-11-06 audit as a historical checkpoint. |
| DOC-016 | P2 | PARTIAL | The root README did not directly surface the current repository audit, and the audit/validation documents did not clearly distinguish the selected PR branch's verified head from `main`. | Added a direct audit link and branch-specific verification caveat. |
| ENG-LOCK-001 | P2 | TODO | No `package-lock.json` exists on the selected branch; CI uses `npm install`, so transitive npm dependency resolution is not frozen. | Record as TODO. Generate a lockfile in a Node/npm-enabled checkout, switch CI to `npm ci`, and verify clean-install reproducibility. No lockfile was fabricated in this connector-only session. |

### Preserved documentation and structure

- `docs/README.md` remains the documentation landing page and defines source-of-truth precedence.
- `docs/audits/README.md` remains the audit/evidence index.
- `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` remains the one canonical append-only execution ledger.
- `docs/final-audit.md` remains a historical synthesis; it is not rewritten as live status.
- `docs/audits/current/` remains the home for dated current audit snapshots and linguistic workpacks.
- `data/lao/*.csv` remains the canonical linguistic data source; `web/data.js` remains generated.
- No broad directory rename, duplicate task tracker, parallel completion register, extra build framework or new runtime dependency is justified by this audit.

## Engineering verification evidence

The latest exact-head full Verify run inspected for this branch is [42384603376 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384603376), on code/test head `2ddb0dbb250268f2477a2614a1f3fc676a9b89e3`. Its single job completed all configured stages successfully:

1. Independent IPA-gold corpus structure validation.
2. Repository data/evidence audit.
3. Python unittest discovery.
4. Optional external-G2P harness syntax and CLI check.
5. Node dependency installation.
6. Browser engine tests.
7. Static build and canonical browser-data generation.
8. Generated-data reproducibility check (`git diff --exit-code -- web/data.js`).
9. Playwright/Chromium UI tests against the built site.
10. Built-page and relative-asset checks.

The workflow's job reports all 14 substantive steps completed successfully. This is hosted CI evidence for the selected PR branch head; it is not a new `main` verification and does not establish expert linguistic accuracy.

The refreshed three-engine benchmark [42384500017 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384500017) produced aggregate artifact [13578308566](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384500017/artifacts/13578308566), SHA-256 `996844312d068145673af57da8e07be48cb241c31cb5be55ef295802a803a6bc`.

- ClippyFirst mean per-item latency: **1.533 ms**, compared with **4.724 ms** in the preceding hosted run, a **67.5% reduction**. Model loading is excluded. This is a single-run observation, not a statistically established performance guarantee.
- Benchmark accuracy and coverage did not change after registry reuse: ClippyFirst segmental CER **11.46%**, 69/100 exact, 97% coverage; on the shared 97 covered items ClippyFirst CER **6.49%** / 69 exact, Lao2IPA **7.72%** / 68 exact, and MekongPhon Neural **5.79%** / 81 exact.
- Tonal comparison on the shared 91 items, using the evaluation-only MekongPhon contour rendering, reports ClippyFirst CER **10.20%** / 52 exact, Lao2IPA **10.86%** / 53 exact, MekongPhon Neural **6.75%** / 68 exact.
- These are diagnostics against a dictionary-seeded held-out reference, not independent expert gold and not universal accuracy estimates.

No local test run, clean npm install, package-lock generation, manual browser QA or deployed accessibility audit is claimed.

## Linguistic evidence and rights boundaries

- The independent project IPA gold corpus remains empty: **0 independently adjudicated records**. The gold TSV is header-only; empirical accuracy must remain null.
- The 100-word MekongPhon held-out lexicon is a diagnostic reference set, not independently re-adjudicated ClippyFirst gold. It must not be used to silently tune rules or relabel the gold corpus.
- Six potential minor-syllable tone candidates remain hypotheses pending qualified Vientiane review. Four known tone disagreements remain reference-sensitive. The five-tone Vientiane matrix was not retuned from the non-adjudicated dictionary sample.
- Three parser-tail structures and one malformed tone-mark case remain fail-closed; do not add speculative segmentation or pronunciation rules to increase coverage.
- The two published Lao model cards declare Apache-2.0 for the model artifacts. This does not license the MekongPhon repository source code, source dictionaries, training corpus, OPUS-derived sentence data or derived dataset. The source/corpus rights boundary remains UNKNOWN/BLOCKED for copying, retention, adaptation, retraining, redistribution and commercial use pending component-specific terms or written permission.
- The root MIT `LICENSE` applies to ClippyFirst's own covered code and documentation. It does not relicense third-party data, model artifacts, fonts, dictionaries or external assets.

## External engineering/design references

Reviewed the five supplied references as methods, not dependencies:

- [unlazy](https://github.com/Leonxlnx/unlazy) — current source describes version 2.1.0 and evidence-bound completion gates. The source does not identify 2.1.0 as a tagged release; retain an exact commit pin for reproducibility when adopting a snapshot.
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — `skill.json` reports version 2.15.0. Its searchable design-system and UX/accessibility guidance is useful for targeted interface reviews; its generic style catalogue should not override the repository's restrained, research-first design system.
- [Superpowers](https://github.com/obra/superpowers) — release v7.0.2. Relevant practices include test-first implementation, root-cause debugging, review and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills) — release v1.3.2. Relevant practices include deep modules, clear interfaces, behavior-focused tests, source-backed research and two-axis review.
- [Ponytail](https://github.com/DietrichGebert/ponytail) — release v5.3.3. Relevant practices include mapping entry points/data flow before editing, connected-code review, reuse before adding code and explicit residual-risk reporting.

The repository already expresses these practices in `AGENTS.md`, `CONTRIBUTING.md`, its codebase map and CI. No external skill tree, checker, hook, orchestration runtime or frontend framework was copied into the project. The local linguistic, privacy, licensing and fail-closed contracts remain authoritative.

## Evidence-based task ledger

| ID | Status | Current evidence | Acceptance / next action |
|---|---|---|---|
| ARCH-001 | DONE_VERIFIED | Canonical data, Python/browser runtimes, generated mirror, schemas, tests and documentation have explicit ownership boundaries. | Preserve; only reorganize if a concrete dependency or maintenance problem is demonstrated. |
| IPA-ADAPTER-001 | DONE_VERIFIED (engineering) | Typed IPA result boundary is exercised by the exact-head Verify run. | Keep target adaptation strictly downstream of typed IPA; linguistic correctness remains a separate gate. |
| PERF-REGISTRY-001 | DONE_VERIFIED | One registry load per `analyze()` is guarded by regression tests; exact-head Verify passed. | Preserve output parity and the load-count guard. |
| BENCH-3ENGINE-001 | DONE_VERIFIED (diagnostic run) | Immutable model revisions, aggregate-only benchmark artifact and successful exact benchmark run. | Keep metrics labelled as reference-relative diagnostics; do not call them accuracy. |
| DOC-012–016 | PARTIAL pending this documentation commit's exact-head Verify | README terminology, limitation scope, validation status, audit index and handoff are being reconciled. | Require full Verify on the final documentation commit before DONE_VERIFIED. |
| ENG-LOCK-001 | TODO | `package-lock.json` absent; workflow uses `npm install`. | Generate and verify lockfile in a local Node/npm environment; switch CI to `npm ci`. |
| UI-A11Y-001 | TODO | Automated Chromium checks exist; manual screen-reader, keyboard-only, zoom/text scaling, mobile touch and deployed-site QA are not evidenced. | Record a human QA matrix with browser/device/AT versions, observations and resolved defects. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold = 0. | Requires a versioned target profile and IPA convention, rights-cleared sample, two qualified independent annotators, separate adjudicator, blind workflow and expert-approved contrast coverage. |
| LAO-TONE-001 | PARTIAL | Six candidate minor-syllable cases and four reference-sensitive tone disagreements remain. | Obtain qualified Vientiane review; only then add source-backed rules and independent fixtures. |
| MEKONG-RIGHTS-001 | BLOCKED for broader reuse | Model artifact license declarations are separate from dataset/source rights; corpus and upstream code rights are unresolved. | Obtain component-specific licenses/permission before copying, retaining, adapting, training on or redistributing source material. |
| LAO-PARSER-001 | PARTIAL / fail-closed | Three parser-tail structures and one malformed tone-mark case remain withheld. | Resolve with primary evidence and qualified review; preserve fail-closed output meanwhile. |

## Readiness judgement

**Research-ready as an engineering and evidence-management prototype; not linguistically release-ready or publication-ready.** The selected branch has a successful exact-head engineering workflow and reproducible aggregate benchmark, but independent expert gold, qualified tone adjudication, broader source-data rights and manual accessibility QA remain unresolved. A green engineering workflow is not a phonetic accuracy certificate.

*Review date: 2026-11-07. This report describes the inspected branch state and is not a legal opinion or a linguistic certification.*


## Documentation patch verification state

The audit, README, validation note, audit index, handoff and agent-reference refresh were committed to the selected branch in the following sequence:

- Audit document: `de423189a96eae9e696713caa8b459e78f624295`.
- README: `a38a02c9bcf5ee90be4bce793190da4e4e92a77b`.
- Validation guide: `77bee3257a962b819dbb5164badad38f419bc488`.
- Audit index: `41ae3c036923d8bbfdeb5462c317b9e55d8ffd56`.
- Master handoff: `16676040c0a0d8943faa4315e86008e5281c9237`.
- Agent-reference refresh / initial six-file documentation batch checkpoint: `d4f08fb6626136e699f05df40f1c7a3e84ad122b`; subsequent verification-boundary updates are recorded in the master handoff.

The earlier green Verify run 42384603376 is exact-head evidence for code/test commit `2ddb0dbb250268f2477a2614a1f3fc676a9b89e3`; it predates these documentation commits. No workflow run associated with final documentation commit `d4f08fb6626136e699f05df40f1c7a3e84ad122b` was returned by the available commit-workflow query. Therefore DOC-012–016 remain **PARTIAL pending exact-final-head Verify**. Do not report the earlier code/test run as verification of the documentation patch.

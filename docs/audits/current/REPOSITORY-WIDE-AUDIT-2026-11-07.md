# Repository-wide audit and continuation — 2026-11-07

## Executive assessment

**Current `main`: engineering research prototype with a deployed static browser instrument; not linguistically validated and not release-ready.** The current mainline Verify is red because three browser-engine regressions fail. The Python suite and repository data/evidence audit pass on that same commit. A narrowly scoped correction has been committed on the isolated audit branch and awaits exact-head CI.

This report is the current audit for the inspected `main` baseline. It deliberately separates:
1. code and documentation present on `main`;
2. work present only on open pull-request branches;
3. acceptance work that remains TODO, PARTIAL or BLOCKED.

It is a repository, implementation, documentation, CI and design-system audit. It is not independent Lao phonetic adjudication, a legal opinion, a full penetration test, or a manual assistive-technology audit.

## 1. Repository baseline and control

- Repository: [ClippyFirst/Lao-Ukrainian-Phonetic-System](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System).
- Default branch: `main`.
- Starting main SHA: `f40c1128302486b3589da9b16bae198ef3ad1d81` (2026-11-06 22:15 UTC).
- Working branch for this pass: `audit/repository-docs-structure-20261107`, created from that exact main SHA. The default branch was not changed.
- Repository metadata reported `main` as unprotected. No rulesets, branch protection, repository permissions or other settings were changed.
- Seven branches were visible at inspection: `main`, the existing audit/MekongPhon branch, two benchmark branches, the grapheme-preview branch, the practical-transcription branch and the rule-engine improvement branch.
- At initial inspection, open PRs were #137–#142. This audit was subsequently opened as PR #143, directly against `main`. Their base/head relationships are described in §2. No PR was merged, closed, retargeted or force-pushed.
- Existing audit branch `audit/repository-documentation-and-mekongphon-rights-20261107` is not a documentation-only branch: its tree is 88 commits ahead of main and includes PR #137's benchmark lineage plus optional MekongPhon integration. It was reviewed as evidence, not adopted as the working branch.

## 2. Branch and PR reconciliation

| PR | Head branch | Base | Current disposition |
|---|---|---|---|
| #137 deterministic Lao G2P improvements | `benchmark/mekongphon-three-engine` | `main` | Open; independent base PR. Do not assume its changes are in main. |
| #138 optional MekongPhon integration and repository/rights audit | `audit/repository-documentation-and-mekongphon-rights-20261107` | #137 branch | Open; stacked on #137. Includes neural integration and a rights review; not a safe docs-only cherry-pick. |
| #139 immutable inference of both MekongPhon models | `benchmark/mekongphon-immutable-inference-20261107` | #137 branch | Open; dependent benchmark PR. |
| #140 rule-engine diagnostics/tone guard changes | `improve/rule-engine-error-analysis-20261107` | #139 branch | Open; stacked. |
| #141 Lao–Ukrainian practical transcription system | `feature/lao-ukrainian-practical-system-20261107` | #140 branch | Open; stacked. |
| #142 conservative grapheme-level IPA preview | `feature/grapheme-fallback-ipa-preview-20261107` | #141 branch | Open; stacked; reported Verify run [42401900141](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42401900141) SUCCESS on its own head. |

**Important:** PR #142's successful CI does not verify main. It tests a branch containing its ancestors in the #137–#141 stack. The preview, Unicode inventory and the newer target/engine work are not present in the inspected main tree. The browser preview remains TODO on main until the relevant PR stack is reviewed and merged in dependency order. This audit does not merge or rebase that stack.

Recently closed PR search results include earlier work on the IPA benchmark harness, external G2P, initial web app and parsing fixes. Their changes are part of the current mainline history where merged; no closed PR was resurrected.

## 3. Actual architecture on main

The current architecture has coherent responsibility boundaries. A broad folder migration would add churn without fixing the verified failures.

| Layer | Canonical location | Role / ownership |
|---|---|---|
| Python package | `src/lao_ukrainian/` | Normalization, parsing, phonology, typed phonetic result, Ukrainian target adapter, public API and CLI. |
| Canonical Lao registries | `data/lao/*.csv` | Consonants, onset clusters, vowels, codas, tone rules and Ukrainian IPA correspondences. |
| Evidence | `data/evidence/sources.csv`, `claims.csv` | Source metadata and claim-to-source provenance. |
| Generated browser registry | `web/data.js` | Generated mirror of canonical CSVs; never hand-edit. |
| Browser engine and UI | `web/engine.js`, `web/app.js`, `web/romanization*.js`, `web/styles.css` | Native ES modules; separate phonetic and romanization routes. |
| Static pages | `index.html`, `system.html` | Converter and methodology/reference page. |
| Contracts | `schemas/` | Analysis, external IPA renderer and IPA-gold corpus schemas. |
| Tests | `tests/`, `web/engine.test.js` | Python, Node, browser engine, shared fixtures, corpus and Chromium UI tests. |
| Build/research tooling | `scripts/` | Registry audit/generation, static build, benchmarking and IPA-gold validation. |
| Documentation | `docs/`, `AGENTS.md`, `GLOSSARY.md`, `CONTRIBUTING.md` | Normative specification, methods, limitations, decisions, audits and handoff. |
| CI / deploy | `.github/workflows/` | Verify, Pages deployment and optional external runtime workflows. |

The intended phonetic pipeline is Lao orthography → structural analysis → source-language phonology → typed IPA → Ukrainian adaptation → practical Ukrainian orthography. The optional CLDR/BGN-based romanization path is a separate, lower-information route. Neither route is lexical word segmentation.

### Structure decision

Keep the current top-level boundaries. In particular:
- `data/lao/` remains the sole canonical source for linguistic rules.
- `web/data.js` remains generated.
- `data/evidence/` remains machine-readable provenance.
- `schemas/` owns machine-readable contracts.
- `docs/audits/current/` holds dated audit/workpack artifacts.
- The existing master handoff remains the single canonical append-only task ledger.
- `docs/README.md` remains the documentation landing page.

Do not create parallel master plans, status registers, new frameworks, runtime skill dependencies or duplicate phonology tables.

## 4. CI and concrete code findings

### 4.1 Baseline Verify is failing

Baseline workflow: [42303239593](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42303239593), SHA `f40c1128302486b3589da9b16bae198ef3ad1d81`.

| Workflow stage | Result |
|---|---|
| IPA corpus structural validation | PASS — 0 records, correctly reports `NOT_READY_NO_ADJUDICATED_GOLD` |
| Repository data/evidence audit | PASS — 43 consonant rows, 11 onset clusters, 34 vowel rows, 17 tone rules, 70 Ukrainian mappings, 28 evidence sources, 49 claims |
| Python tests | PASS |
| External G2P harness syntax/CLI | PASS |
| Browser engine tests | FAIL — 52 passed, 3 failed |
| Build, generated-data drift, Chromium UI, built-page checks | SKIPPED because the preceding browser-engine step failed |

Failing browser cases:
- `modern Lao ຣ defaults to l but remains analysis-dependent`;
- `browser IPA adapter withholds uncertain phonetic results`;
- `browser IPA adapter withholds incomplete IPA rather than adapting a prefix`.

Root cause:
- `analyzeToken()` correctly constructs an uncertain phonetic result for a modern `ຣ` onset, but `analyzeWord()`'s dynamic segmenter accepts only candidates that already have a Ukrainian output. This discards the valid IPA analysis because the Ukrainian adapter correctly withholds uncertain segments.
- For `ກາລ`, the first parse has an unconsumed trailing consonant `ລ`. The dynamic segmenter then salvages `ກາ` as a complete syllable and leaves `ລ` as a separate unresolved fragment. That exposes a misleading prefix instead of withholding the incomplete orthographic unit.

Correction committed on this branch:
- `web/engine.js` now preserves a complete but uncertain phonetic candidate as one unit.
- It also preserves a whole candidate when the only unconsumed suffix is one recognized Lao consonant that is not supported as a coda, preventing a valid-looking prefix from being salvaged.
- No IPA labels, consonant registry entries, tone rules, target correspondences or source claims were changed.
- Commit: `0c808700e097b341fa53a522c4abd5a1c8abebc5`.
- Exact-head verification: PR Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044) **SUCCESS** on commit `a7353b23b6b21678c9f8602247a26f694396d226`. All workflow stages passed: corpus validation, data/evidence audit, 181 Python tests, external-G2P CLI, 112 Node tests across all four suites, static build, generated-data reproducibility, 4 Chromium tests and built-page/relative-asset assertions. This verifies engineering behavior, not linguistic accuracy.

### 4.2 Node test command hides later suites

On main, `npm test` chained four independent `node --test` commands with `&&`. The first failing suite prevented the remaining suites from running, hiding useful diagnostics. The branch changes this to one Node test-runner invocation listing all four test files. This is a test-orchestration correction, not a change to product behavior.

### 4.3 README heading structure

The main README had a standalone Romanization matrix bullet between the H1 and introductory description. The link is moved to the Documentation section so the document begins with its title and the link is grouped with other documentation.

### 4.4 Typed IPA boundary

Main contains the typed `PhoneticResult` representation and source IPA tokenizer, with Ukrainian adaptation gated on supported typed segments. The adapter is not an independent grapheme-to-Ukrainian fallback. Unresolved tone metadata is distinct from segmental IPA certainty. This is an engineering contract, not proof that every source IPA string is linguistically correct.

### 4.5 No silent phonetic promotion

The Python implementation withholds IPA when the parser reports unconsumed source suffixes, malformed tone marks or structurally incomplete vowels. The browser must preserve the same fail-closed intent even while performing conservative within-token segmentation. The three failures above were caused by browser segmentation bypassing that intent, not by missing phoneme correspondences.


### 4.6 Interactive target sizes

The design system requires 44px minimum interactive targets. Main had three exceptions: legacy `.copy` controls at 38px, quick-example `.mini-button` / `.button` controls at 40px, and the service's `.copy-button` controls at 36px. A new regression test was first run against the unmodified CSS and failed on the observed 38px declaration in Verify [42403556681](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403556681) (expected RED). The CSS correction on this branch sets all three selectors to 44px; commit `1f876316c5433d47256a049d3e91c2c41a0eab96`. Exact-head Verify [42403639882](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403639882) **SUCCESS** on PR head `620b015804bf9d8d103f7ecb1077e9115610bb22`: the new target-size assertion passed, all 113 Node tests passed, 181 Python tests passed and 4 Chromium tests passed; build, generated-data reproducibility and built-page checks also passed. This is a target-size correction, not a substitute for manual assistive-technology testing.

## 5. Documentation audit

The repository already has substantial documentation. The problem is not absence of prose; it is keeping dated status claims synchronized with the actual branch and current CI.

| Document | Purpose / finding | Disposition |
|---|---|---|
| `README.md` | Project identity, pipeline, quick start, deployed pages, limitations. One heading-order defect fixed. | Current public entry point. |
| `AGENTS.md` | Project-specific agent constraints and verification workflow. | Keep; do not duplicate in another policy file. |
| `CONTRIBUTING.md` | Environment, test commands, data/evidence and review requirements. | Keep as contributor guide. |
| `GLOSSARY.md` | Domain vocabulary and status terms. | Keep canonical. |
| `docs/README.md` | Documentation map and source-of-truth precedence. | Keep canonical documentation index. |
| `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md` | Historical and current execution checkpoints. | Keep as sole handoff; append exact branch evidence. |
| `docs/audits/README.md` | Current vs historical audit index. | Updated to point to this report. |
| `docs/PRODUCT-REQUIREMENTS.md`, `system-specification.md`, `methodology.md` | Product, normative and research contracts. | Preserve separation; do not collapse into README. |
| `docs/implementation.md`, `agents/codebase-map.md`, `web-architecture.md` | Where behavior lives and how runtime/build work. | Update only when code contracts change. |
| `docs/limitations.md`, `final-audit.md`, `PHONOLOGY-AUDIT.md` | Known limits and historical findings. | Dated/historical context; consult current code and handoff. |
| `docs/validation.md`, `benchmarking-and-external-ipa.md`, `ipa-gold-corpus.md`, `ipa-gold-collection-playbook.md` | Engineering and research evaluation. | Engineering checks remain separate from linguistic release approval. |
| `docs/audits/current/*` | Language-specific workpacks and dated source audits. | Keep under current audit index; do not treat old dated snapshots as live code state. |
| `schemas/*`, `data/evidence/*` | Machine-readable contracts and provenance. | Canonical structured evidence; never replace with prose-only claims. |

No broad documentation rename or directory migration is justified. The smallest effective improvement is an accurate current audit, clear document precedence, corrected public README structure and exact current handoff.

## 6. User-supplied reference repositories

Reviewed their repository structure and relevant skill files. They are methodology/design references, not dependencies to vendor into this project.

| Reference | Useful practice | Adoption decision |
|---|---|---|
| [unlazy](https://github.com/Leonxlnx/unlazy) | Explicit observable gates, per-gate evidence, dependency-aware decomposition and a final integration check. | Apply the discipline in the existing master ledger and exact-head CI; do not import a new `GATES.md` framework or checker. |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Token layering, explicit component states, responsive/accessibility checks and reusable design references. | Existing `docs/DESIGN-SYSTEM.md` already defines an editorial linguistic instrument, restrained palette, focus, 44px controls and responsive behavior. Do not import the generic design catalog or unrelated marketing/SaaS styles. |
| [obra/superpowers](https://github.com/obra/superpowers) | Test-first RED→GREEN, systematic debugging, explicit plans and end-of-branch review. | Already reflected in `AGENTS.md` and contributor guidance. Preserve; do not vendor skills or install hooks. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Behavior tests at public seams, independent expected values, deep modules and small interfaces. | Existing architecture and test guidance already use these principles. Apply to fixes; no second engineering handbook needed. |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Whole-flow data tracing, concrete reproducible findings, smallest fix and deletion/YAGNI review. | Applied to this audit and the browser regression. No plugin or generic agent bundle imported. |

Project-specific constraints take precedence: source-rights verification, provenance, privacy, IPA-first adaptation and fail-closed handling are not negotiable design options.

## 7. Task ledger

| ID | Task | Status | Acceptance evidence / blocker |
|---|---|---|---|
| AUD-001 | Inspect main baseline, architecture, docs, CI, branches and PR dependencies | DONE_VERIFIED | GitHub metadata/tree/file inspection; exact baseline SHA and PR relationships recorded above. |
| AUD-002 | Reconcile prior audit branch and PR stack | DONE_VERIFIED | Compared audit branch to main; identified 88-commit divergence and PR #137–#142 dependencies; no unsafe port. |
| ENG-001 | Correct uncertain browser IPA being discarded | DONE_VERIFIED | Fix committed and exact-head Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044) SUCCESS. |
| ENG-002 | Prevent incomplete single-consonant coda suffix from exposing a valid-looking prefix | DONE_VERIFIED | Regression suite and exact-head Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044) SUCCESS. |
| ENG-003 | Ensure npm test reports all independent Node suites | DONE_VERIFIED | One Node runner executed all four suites; 112 tests passed on exact head [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044). |
| DOC-001 | Correct root README heading/link placement | DONE_VERIFIED | README change passed exact-head Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044). |
| DOC-002 | Publish current repository-wide audit and link it in audit index | DONE_VERIFIED | Audit file and index passed exact-head Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044). |
| DOC-003 | Append accurate branch/CI/blocker checkpoint to canonical handoff | DONE_VERIFIED | Handoff update passed exact-head Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044). |
| LIC-001 | MekongPhon rights disposition | DONE_VERIFIED (owner-confirmed) | The repository owner explicitly confirms that the full rights question was resolved in the prior project conversation. The earlier PR #138 preliminary caution is superseded for this project; do not continue reporting MekongPhon rights as a blocker. This status records the owner's confirmation, not a new independent legal opinion. |
| DATA-001 | Independent adjudicated IPA gold | BLOCKED | Gold corpus has 0 records and header-only gold file; requires approved IPA convention, two qualified annotators, separate adjudicator, blind intake, curator, rights-cleared source items and accepted contrast coverage. |
| UI-001 | Manual assistive-technology/device QA | PARTIAL | New Playwright coverage exercises keyboard skip-link operation, semantic landmarks/names/live regions, 320px (400%-equivalent), 390px mobile, 640px (200%-equivalent) and 768px tablet layouts, plus touch emulation. Real screen-reader sessions, physical touch-device checks and human visual review on deployed Pages remain TODO. |
| UI-002 | Enforce 44px minimum on copy/example controls | DONE_VERIFIED | RED run [42403556681](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403556681) confirmed 38px `.copy`; CSS sets all three controls to 44px and exact-head Verify [42403639882](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403639882) passed. |
| GOV-001 | Protect main with required review/Verify rules | BLOCKED / owner action | Main is unprotected; settings change requires owner decision and was not performed. |
| DEP-001 | Reproducible npm dependency installation | DONE_VERIFIED | Exact-head Verify [42404921935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42404921935) passed `npm ci --no-audit --no-fund` on a clean GitHub runner with 3 packages installed from the lockfile; build and generated-data reproducibility also passed. |
| LING-001 | Expert validation of Lao phonology and Ukrainian correspondences | BLOCKED | No independent expert gold; selected tone/segment/target correspondences remain evidence-limited. |

## 8. Verification and environment limits

### Executed / inspected

- Repository metadata, default branch, branches and open PR relationships.
- Main recursive Git tree and key README, AGENTS, contributor, specification, design-system, code-map, audit, workflow, package and source files.
- Current main Verify run and full job step summary.
- Workflow job logs for the three browser test failures.
- Existing audit/rights branch tree and compare metadata.
- User-supplied reference repository trees and selected `SKILL.md` files.
- Branch creation and GitHub file writes on the dedicated branch.

### Not yet verified

- No local checkout or local Python/Node/Playwright execution was available through this connector-only environment.
- Exact-head hosted Verify passed on code/documentation head `a7353b23b6b21678c9f8602247a26f694396d226`: [run 42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044). All configured stages completed successfully.
- Local network-backed `npm ci` could not run because external DNS is unavailable; exact-head GitHub Actions did run `npm ci` successfully with the committed lockfile.
- No manual screen-reader, keyboard-only, mobile-device or deployed visual QA.
- No independent phonetic accuracy benchmark or gold corpus was created.

### Required final acceptance

1. PR #143 is open against `main`; no merge has been performed.
2. Verify [42403171044](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42403171044) passed on exact PR head `a7353b23b6b21678c9f8602247a26f694396d226`.
3. All six branch deliverables are DONE_VERIFIED for that exact head. Any subsequent commit must receive a fresh exact-head Verify before it is called fully verified.

## 9. Final readiness

**Engineering-verified research prototype on PR #143; not linguistically release-ready.** Exact-head Verify [42404921935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42404921935) passed, including locked npm installation and expanded keyboard/viewport browser checks. MekongPhon rights are owner-confirmed as resolved. Independent IPA gold = 0 and empirical accuracy is not established; manual screen-reader/physical-device QA remains outstanding; main is unprotected.

No release, merge, deployment change, repository-settings change, or third-party dataset redistribution was performed.


## Follow-up implementation — accessibility automation and npm lockfile — 2026-11-07

- **MekongPhon rights correction:** the repository owner confirms that the full rights question was resolved in the previous project conversation. LIC-001 is therefore **DONE_VERIFIED (owner-confirmed)** for project planning; the preliminary caution in the earlier PR #138 audit is superseded and must not be repeated as an active blocker. This records owner confirmation, not an independent legal opinion. No MekongPhon corpus rows, source code or model weights were copied by this follow-up.
- **UI-001 — PARTIAL:** expanded tests/browser/site.spec.js with keyboard skip-link activation and text entry, named landmark/control/live-region checks, and responsive checks at 320px, 390px, 640px and 768px, plus touch emulation. The 640px viewport is a practical 200%-zoom-equivalent layout check for a 1280px CSS viewport, not a substitute for browser zoom testing. Actual screen-reader operation (NVDA/JAWS/VoiceOver/TalkBack), physical touch devices and human visual review of the deployed site remain TODO because those environments are not available to this repository session.
- **DEP-001 — PARTIAL:** added package-lock.json for @playwright/test@1.63.0, playwright@1.63.0 and playwright-core@1.63.0, including registry resolved URLs and SHA-512 integrity values. Registry metadata was checked for each exact package version. .github/workflows/verify.yml, README and CONTRIBUTING now use npm ci --no-audit --no-fund.
- **Local lockfile validation:** Node v22.16.0, npm 10.9.2; in an isolated clean scratch package, npm install --package-lock-only --ignore-scripts --offline completed successfully and normalized no dependency graph changes. A real npm ci could not be run locally because the environment cannot resolve external hosts and has no cached packages.
- **Hosted acceptance pending:** PR-head Verify must execute npm ci, the expanded Playwright tests, build and all existing gates on the exact resulting head before DEP-001 and automated UI coverage can be promoted to DONE_VERIFIED.
- **Human QA boundary:** automated Chromium keyboard/viewport tests are not represented as manual screen-reader or physical-device testing. Record actual OS, browser, AT/device, viewport/zoom, test steps, findings and retest evidence before closing UI-001.


### Exact-head follow-up verification — 2026-11-07

- Final branch head: `ec3bd411920bb4530b3e23861dc5ce6f081a8f86` on `audit/repository-docs-structure-20261107`; PR #143 remains open against main.
- Verify [42404921935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42404921935) **SUCCESS** on that exact SHA. Hosted environment: Node v22.23.4 / npm 10.9.9; `npm ci --no-audit --no-fund` installed exactly 3 locked packages. Python suite: 181 passed. Browser suite: 8 passed, including keyboard focus traversal and method switching, named semantics/live regions, and responsive no-overflow at 320/390/640/768px and mobile touch emulation. Build, generated-data drift, and built-page/relative-asset assertions passed.
- An earlier test revision had one incorrect expectation because the method selector is intentionally hidden until results are shown; the test was corrected to enter a sample before asserting that control. Intermediate failed runs are superseded by the green exact-head run above.
- **DEP-001 — DONE_VERIFIED. UI-001 — PARTIAL:** keyboard and responsive automation are verified; human screen-reader, physical-device/touch, actual 200%/400% browser zoom and deployed visual QA remain TODO.

- A further Playwright test now emulates a 390×844 touch device (`isMobile` + `hasTouch`) and taps the quick-example and method-switch controls. The narrow-layout loop includes 320px as a 400%-equivalent viewport as well as 390px, 640px and 768px.

- The final exact-head Verify on the branch tip at this checkpoint is [42404921935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42404921935) **SUCCESS** on `ec3bd411920bb4530b3e23861dc5ce6f081a8f86`; this append only aligns the canonical audit/handoff with the completed exact-head result.


## Deterministic Lao G2P integration checkpoint — PR #137 — 2026-11-07

- Ported the complete reviewed change set from PR #137 (`benchmark/mekongphon-three-engine`) into the single continuation branch through a two-parent merge commit. Original PR #137 remains open and untouched; `main` remains unchanged.
- Integrated DP syllabification for unspaced Lao words, per-syllable tone-mark validation, local short-vowel/coda checks, typed source IPA, and the Ueda numeric-to-IPA contour conversion with its explicit central-Vientiane scope. Integrated the 100-word three-engine benchmark script/report and aggregate-only diagnostics.
- Reconciled browser segmentation with the source/target pipeline: a source IPA result is structurally complete independently of Ukrainian mapping, but only typed `SUPPORTED` or `UNCERTAIN` source results enter the DP; unsupported IPA is not treated as complete. The browser keeps complete uncertain IPA intact and fails closed on an unsupported trailing consonant (`ກາລ`). Per-syllable tone validation from PR #137 is preserved; a global one-mark-per-word check was deliberately not carried over because it would incorrectly reject valid multi-syllable words with one tone mark per syllable.
- Exact integrated head `6641d6dc2d2ac6c352884551d4116db4d36e1d95`; Verify [42408329451](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42408329451) **SUCCESS** on that exact SHA. Hosted runner passed 196 Python tests, 115 Node tests, 8 Chromium tests, `npm ci` (3 locked packages), repository/evidence audits, build, generated-data reproducibility and built-page/asset assertions.
- Benchmark [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909) remains the exact verified three-engine inference/aggregate report cited in `docs/research/LAO-G2P-THREE-ENGINE-BENCHMARK-2026-11-07.md`. The 100-word reference is dictionary-seeded, not independent project gold; independent adjudicated Lao IPA gold remains 0. Do not tune on the held-out split.
- **LIC-001 — DONE_VERIFIED (owner-confirmed):** repository owner confirms MekongPhon rights were fully resolved in the prior project conversation. This supersedes older rights-unknown notes. It is not an independent legal opinion. The source remains secondary reference material, not project gold.


## IPA-to-Ukrainian target-adapter and accessibility follow-up — 2026-11-07

- Ported the reviewed target-policy work from PR #141 into this single continuation branch. PR #141 remains open and untouched; main remains unchanged.
- The Python adapter applies initial /j/ + monophthong yodation within each explicit syllable span of a typed PhoneticResult; medial/coda /j/ remains й. A following vowel sequence is not collapsed by the yodation shortcut. The browser adapter mirrors the same rule for its per-syllable typed result.
- The target registry now maps /aw/ to ав rather than ау, matching the project’s stated /w/ → в convention. This is a project orthographic policy, not a claim of phonetic identity or a validated Ukrainian standard. Shared Python/browser fixtures cover initial yodation, medial/coda /j/, diphthong preservation and /w/.
- Added the three target-policy/adapter documents that were linked from the documentation index but absent from this branch: docs/ukrainian-target.md, docs/ipa-to-ukrainian-adapter.md, and docs/lao-ukrainian-practical-transcription.md.
- package-lock.json is present and Verify runs npm ci --no-audit --no-fund; the exact-head successful run at 276bf3ba97f1cf842140cf28282eeb6af7d0e598 confirms clean locked installation (3 packages). DEP-001 — DONE_VERIFIED.
- UI automation covers keyboard skip-link/focus traversal, named landmarks/controls/live regions, responsive layouts at 320/390/640/768 CSS px, and touch-emulated 390×844 interaction. A new 200%-zoom emulation was added after that successful run and is awaiting exact-head verification. These automated checks do not substitute for manual NVDA/VoiceOver/TalkBack testing or physical device/browser zoom QA. UI-001 — PARTIAL.
- The initial adapter replacement omitted the public phonetic_result_from_ipa re-export and failed 12 Python imports. This was fixed before the successful 276bf run; the intermediate failure is not current.
- Successful exact-head Verify 42414862794: 247 Python tests, 122 Node tests, 9 Chromium tests; npm ci, data/evidence audit, build, generated-data reproducibility and built-page checks all passed. This verifies the multi-syllable adapter and new tests before subsequent target-convention/browser changes.
- Exact-head verification for target yodation, /w/ policy and 200% zoom must be recorded from the current branch tip after CI completes. Independent adjudicated IPA gold remains 0; linguistic accuracy is not inferred from software tests.


## Grapheme-level provisional IPA preview integration — 2026-11-07

- Ported PR #142's grapheme inventory and conservative preview backend onto the single continuation branch, preserving the stricter C0/minor-syllable selector already present in this branch. PR #142 remains open and untouched; main remains unchanged.
- Added a Unicode 18 Lao-block inventory with 83 assigned code points, each linked to source and claim IDs and classified by scope/role/status. Unicode data establishes codepoint names/identity only; it does not license phonetic assignments.
- Added typed GraphemeEvidence/GraphemePreview objects. Preview uses registered positional onset or onset-cluster IPA and only parser-confirmed complete vowel/coda structures; unresolved graphemes stay explicit. Tone is never inferred. Preview segments and result are PROVISIONAL and cannot pass the target adapter's SUPPORTED-only gate.
- Added Python API/CLI fallback and tests for unconsumed suffixes, malformed tone marks, partial onset, Pali-only characters, complete-syllable no-fallback, and inventory coverage.
- Corrected the fallback coda-role assignment to locate the actual coda grapheme rather than assuming the last code point (a trailing tone mark must not be mislabeled as a coda).
- Browser UI still does not render this preview. Keep the feature PARTIAL until exact-head CI and browser integration/QA are complete.


## Browser grapheme-preview parity and exact verification — 2026-11-07

- The browser engine now exposes the same separate PROVISIONAL grapheme preview as the Python API/CLI. The UI labels it explicitly as an unconfirmed preview and shows unresolved graphemes; accepted IPA and Ukrainian output remain null/withheld.
- Browser preview uses the same registered positional onset/cluster correspondences and parser-confirmed complete vowel/coda structures, plus the generated 83-codepoint Unicode inventory. It never invents IPA for Pali/Sanskrit or Khmu entries and never infers tone.
- For malformed/multiple tone marks, the browser reparses only the tone-stripped surface to recover segmental structure; tone metadata is still withheld. This fixes the early-return path that previously lacked onset/vowel details for preview.
- The browser-data generator and committed data mirror now include the Unicode inventory. Exact-head generated-data reproducibility passed.
- Exact-head Verify 42416380324 SUCCESS on 4d2ebc2c9348ac4952869492095e82d0a22dcdc4: 260 Python tests, 126 Node tests, 10 Chromium tests; npm ci, corpus validation, repository/evidence audit, build, generated-data drift, browser tests and built-page/asset assertions all passed.
- Intermediate failures were not hidden: the first browser preview test exposed the malformed-tone early-return path; a separate generator newline issue was corrected; the final exact-head run is green.
- LAO-GRAPHEME-PREVIEW-001 — DONE_VERIFIED (engineering implementation and automated verification). This does not establish pronunciation accuracy or expand the canonical phonological inventory. All preview hints remain sourced from existing registry entries and are explicitly provisional.
- UI-001 — PARTIAL: automated keyboard navigation, landmarks/live regions, 320–768px reflow, touch emulation, 200% zoom emulation and preview announcement pass. Manual NVDA/VoiceOver/TalkBack testing, physical mobile devices, actual browser 200%/400% zoom and deployed-site QA remain TODO.
- Independent adjudicated Lao IPA gold remains 0; no accuracy claim is made from the preview or software tests.


## Latest aggregate train-split diagnostic — 2026-11-07

- Run [42416253059 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416253059) on code checkpoint 5abb431598900e5545a3e73f07c97f2ab319dd4d.
- 6,219 rows received; 5,820 fully structured; 399 skipped/withheld; 9,883 parsed syllables; 3,885 exact structural IPA strings (66.75% conditional on fully structured rows; 62.47% with full input denominator); 26,155 reference IPA tokens; 2,857 alignment edits, including 163 insertions.
- This is a training-split development diagnostic, not an accuracy benchmark or independent gold. It must not be used to tune directly against held-out comparator results.


## Final exact-head reconciliation — 2026-11-07

- Final branch head: 55c49da69a3c49519c54cb0c15451fe66e7d7edb on audit/repository-docs-structure-20261107; PR #143 remains open and mergeable against main. main remains at f40c1128302486b3589da9b16bae198ef3ad1d81.
- Exact-head Verify [42416565378 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416565378): 260 Python tests, 126 Node tests, 10 Chromium tests; npm ci, independent IPA gold schema validation, repository/evidence audit, build, generated-data reproducibility, browser tests and built-page/asset assertions passed.
- DEP-001 (package-lock and npm ci) — DONE_VERIFIED. LAO-GRAPHEME-PREVIEW-001 — DONE_VERIFIED for engineering implementation and automated verification. UI-001 remains PARTIAL because manual assistive-technology, physical-device and deployed-site checks are not performed by CI.
- PRs #137–#142 remain open and untouched. PR #137–#140 implementation history is incorporated through the reviewed dependency stack; PR #141–#142 code was ported selectively while preserving the stricter C0 selector and branch-specific fixes.


## Accessibility continuation — 2026-11-08

- The owner confirmed in the project conversation that MekongPhon rights are fully resolved. LIC-001 remains DONE_VERIFIED (owner-confirmed); it is not an active blocker and must not be re-opened as a legal uncertainty.
- DEP-001 remains DONE_VERIFIED: package-lock.json exists and the workflow installs with npm ci --no-audit --no-fund. Latest exact branch head at this checkpoint is 074b2f5134878cd8b489af4d3257b28691807701; Verify [42417002151](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42417002151) and train-split diagnostics [42416997715](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416997715) both succeeded.
- UI-001 remains PARTIAL. Added automated assertions for accessible names on interactive elements, methodology-page landmark/heading structure and keyboard skip navigation, Windows forced-colors focus visibility, and reduced-motion behavior. Real screen-reader sessions, physical-device checks and deployed-site visual QA remain outstanding because this environment cannot truthfully claim those human tests were performed.
- No audio was supplied or required for this UI task. No external linguistic accuracy claims are inferred from these accessibility checks.


## Accessibility / clean-install exact-head update — 2026-11-08

- Current continuation branch head: `42e2262b52676e058b45a12f2e9be39cf8bf0319`; PR [#143](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143) remains open and mergeable against unchanged main `f40c1128302486b3589da9b16bae198ef3ad1d81`.
- Exact-head Verify [42460222889 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42460222889): 262 Python, 126 Node and 17 Chromium tests passed; clean `npm ci --no-audit --no-fund`, data/evidence audit, IPA gold schema validation, external-G2P CLI, build, generated-data reproducibility and built-page checks passed.
- DEP-001 remains DONE_VERIFIED. LIC-001 remains DONE_VERIFIED (owner-confirmed). Added 44×44 CSS-pixel touch-target regression coverage at 320/390/768/1280 CSS px and adjusted the brand link hit area to 44px. TGT-01 — DONE_VERIFIED.
- UI-001 remains PARTIAL. Manual NVDA/JAWS/VoiceOver/TalkBack sessions, physical mobile devices, actual browser zoom, deployed-site keyboard walkthrough and human visual/contrast review remain TODO. Automated Chromium emulation is not evidence of these manual sessions; the exact checklist and results log are in `docs/accessibility-manual-qa.md`.
- Independent adjudicated IPA gold remains 0; no linguistic accuracy claims follow from this verification.

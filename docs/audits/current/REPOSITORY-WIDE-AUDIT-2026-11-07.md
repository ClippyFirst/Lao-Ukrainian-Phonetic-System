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
| DOC-012 | P1 | DONE_VERIFIED | README romanization wording corrected; exact-head Verify 42388269091 passed on 62483d900e5c4a620828ae24319ddd6b5c741f27. | Keep romanization separate from IPA-first transcription. |
| DOC-013 | P1 | DONE_VERIFIED | README limitation corrected to lexical word-boundary detection; exact-head Verify 42388269091 passed on 62483d900e5c4a620828ae24319ddd6b5c741f27. | Preserve the distinction between syllable parsing and lexical word segmentation. |
| DOC-014 | P2 | DONE_VERIFIED | `docs/validation.md` now labels historical test counts/workflows and links to the current audit/handoff; exact-head Verify 42388269091 passed. | Refresh the status only when a later verified head supersedes it. |
| DOC-015 | P2 | DONE_VERIFIED | Audit index points to this 2026-11-07 repository-wide checkpoint and retains 2026-11-06 as historical; exact-head Verify 42388269091 passed. | Keep the index aligned with the newest verified audit. |
| DOC-016 | P2 | DONE_VERIFIED | Root README links the current audit and docs distinguish the selected PR branch from `main`; exact-head Verify 42388269091 passed. | Re-check after future branch or merge changes. |
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

The latest completed full Verify inspected for the grapheme-context code checkpoint is [42390739133 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390739133), on `16d267664beb25a9e26e9639aace42a2975582d1`. The matching full train diagnostic is [42390734319 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390734319). Later commits add direct positional/broader-context output arrays and an aggregate-only test guard; their exact-head diagnostic and Verify are pending at the time of this audit update. The prior full Verify 42388269091 remains valid for its documentation checkpoint only. The completed 42390739133 run executed all configured stages successfully:

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
- MekongPhon is now an approved external research resource for non-redistributive analysis, rule-discovery and comparative diagnostics: the authors explicitly state that all data, code and pretrained models are publicly released to support future research and development. Its 6,219-row train split is used only for development diagnostics; the 100-row eval split remains a separate comparator. Neither split is independent ClippyFirst gold, and no MekongPhon item is promoted into `gold.tsv`.
- The first full train-split diagnostic completed successfully in [run 42386956616](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42386956616), commit `eec4211e86c0245b4692a05e092aafef50a034f4`; aggregate artifact SHA-256 `1598ee5f23ea9bfdba6c4eacbb4f53cc377900565a91054d4b96c354c2dd24`. On 6,219 development rows: segmental coverage **93.58%**, exact matches **3,885/6,219 (62.47%)**, full-denominator CER **16.70%**. Tone-category coverage was **4,152/8,761 (47.39%)**; category disagreements were **132/4,152 (3.18%)** on this segmental-exact covered subset; 616 word-level category-length mismatches and 133 reference-alignment failures remain. These are train-split diagnostics, not accuracy or held-out generalization.
- Of the 132 tone-category disagreements, the largest reference→engine pairs were **50 high-mid→low-rising** and **38 low-falling→high-mid**. MekongPhon's own pinned deterministic baseline maps high-class live unmarked syllables to low-rising and low-class short-dead unmarked syllables to high-mid ([upstream rule baseline at the pinned revision](https://github.com/byu-matrix-lab/MekongPhon/blob/f80f6c1840c4818b51e05f2e00cded4701a5b662/training/baselines/rb_lao_to_ipa.py)); ClippyFirst's corresponding Vientiane rules use those same categories. This is a reference-sensitive discrepancy, not sufficient evidence to change the tone matrix. No tone rules were changed from this train split.
- The final aggregate diagnostic passed on code commit `3efc0ccb54887830157915e8b4b84ad9177e1720`: [train diagnostic run 42388029325](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388029325), [full Verify 42388033575](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388033575). Aggregate artifact SHA-256: `a9cb3e0a98b3a47532871d170f14d38415be8c57d093af92f8b02f84ce9232b3`. The IPA-inventory-token profile has 5,531 edits across 28,992 reference tokens (19.08% token error rate on the full train denominator). Leading token substitutions: `aː→ə` 507, `j→i` 365, `w→ʋ` 327, `u→uː` 279, `o→w` 246, `i→iː` 237, `r→l` 171. These are reference-comparison leads, not phonological verdicts: the project already records /w/ vs /ʋ/ as profile/target-policy-sensitive and modern /r/→/l/ as analysis-dependent. Vowel quality/quantity and glide differences need context-specific primary-source review before any rule change.
- Six potential minor-syllable tone candidates remain hypotheses pending qualified Vientiane review. Four known tone disagreements remain reference-sensitive. The five-tone Vientiane matrix was not retuned from the non-adjudicated dictionary sample.
- Three parser-tail structures and one malformed tone-mark case remain fail-closed; do not add speculative segmentation or pronunciation rules to increase coverage.
- The authors' public research-release statement supports the research use undertaken here. The current diagnostic consumes only the word-level seed-lexicon split, not the OPUS-derived sentence corpus; SEAlang terms for this source lexicon remain unverified, while OPUS terms apply only to any future sentence-corpus use. The upstream repository still has no dataset-specific license/root LICENSE; therefore this is not treated as a blanket redistribution, sublicensing or commercial-use grant. No raw source rows, IPA references or per-item predictions are committed or retained in CI artifacts. Any future mirroring, publication of data, or commercial reuse remains separately gated. The Lao model cards declare Apache-2.0 for model artifacts; those declarations apply to model artifacts, not automatically to all upstream data.
- The root MIT `LICENSE` applies to ClippyFirst's own covered code and documentation. It does not relicense third-party data, model artifacts, fonts, dictionaries or external assets.

## External engineering/design references

Reviewed the five supplied references as methods, not dependencies:

- [unlazy](https://github.com/Leonxlnx/unlazy) — current source describes version 2.1.0 and evidence-bound completion gates. The source does not identify 2.1.0 as a tagged release; retain an exact commit pin for reproducibility when adopting a snapshot.
- [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — `skill.json` reports version 2.15.0. Its searchable design-system and UX/accessibility guidance is useful for targeted interface reviews; its generic style catalogue should not override the repository's restrained, research-first design system.
- [Superpowers](https://github.com/obra/superpowers) — release v7.0.2. Relevant practices include test-first implementation, root-cause debugging, review and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills) — release v1.3.2. Relevant practices include deep modules, clear interfaces, behavior-focused tests, source-backed research and two-axis review.
- [Ponytail](https://github.com/DietrichGebert/ponytail) — release v5.3.3. Relevant practices include mapping entry points/data flow before editing, connected-code review, reuse before adding code and explicit residual-risk reporting.

The repository already expresses these practices in `AGENTS.md`, `CONTRIBUTING.md`, its codebase map and CI. No external skill tree, checker, hook, orchestration runtime or frontend framework was copied into the project. The local linguistic, privacy, licensing and fail-closed contracts remain authoritative.

## Grapheme-position and contextual rule discovery — 2026-11-07

The production engine is a compositional grapheme/structure rules engine, not a word-to-IPA lookup. Its runtime separates onset and coda consonant values, resolves complete vowel spellings, handles documented multi-grapheme onsets, derives tone from phonological context, and adapts only typed IPA.

The new [MekongPhon grapheme-context analysis](MEKONGPHON-GRAPHEME-CONTEXT-ANALYSIS-2026-11-07.md) parses the pinned 6,219-row train split through ClippyFirst's own syllable parser. It records each Lao code point and structural role, with previous/next signs, onset class, vowel ID, live/dead type, coda and tone mark. It separately reports engine IPA and reference-aligned IPA; multi-sign vowels remain joint units. It does not write source words or per-item predictions and does not promote dictionary references to gold.

Verified diagnostic checkpoint [42390734319 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390734319), code commit `16d267664beb25a9e26e9639aace42a2975582d1`, artifact SHA-256 `7d51559fc9d5ef7d173850d9237cbd62577c2b7b890e96d1e73a6f113d46938a`:
- 6,219 rows; 5,820 fully structurally parsed (93.58%); 399 withheld; 9,883 parsed syllables.
- 3,885/5,820 exact structural IPA string matches (66.75% conditional concordance, not accuracy).
- 26,155 reference IPA tokens; 2,857 alignment edits; 163 insertions.
- High-frequency positional examples confirm /n/ coda, /k/ onset, /aː/ from the postposed `າ` structure, /a/ from short `ະ`, and context-specific consonant values.

The largest structural-unit differences are /ʋ/ vs /w/ for onset `ວ`, /iːə/ vs /iaː/ for `ຽ`, /aw/ vs /ao/ for `ເົາ`, /uːə/ vs /uaː/ for `UO_LONG`, /ɯːə/ vs /ɯːə̯/ for `ເືອ`, /ai/ vs /aj/ for `ໄ`/`ໃ`, /l/ vs /r/ for `ຣ`, and /ɤː/ vs /əː/ for `ເີ`. These are not automatically changed: they may reflect source transcription convention, dialect/profile, rhyme realization or lexical class.

The typed IPA inventory now recognizes documented labialized onset units and the external IPA forms `əː` and `ə̯`. No unapproved Ukrainian correspondences were added; the target adapter remains fail-closed for unsupported segments. Regression tests explicitly exercise onset/coda alternations, short/long `ເ`, silent-carrier versus vowel-sign `ອ`, high digraphs, labialized onsets and IPA token boundaries.

Later code commits `43a2cfeb58c6e2af4889eb5213c0113c3cc1bd3f` and `990ea6838d08c2b798437acaad023dcce1b6c81a` add direct grapheme-position and broader phonological-context distributions, plus their assertions. The subsequent aggregate-only test guard is `3151d65269d5303ec0f92e9b6b23b6ffb7bb563b`; exact-head diagnostic and Verify for that final code/test head are pending. Do not mark the additional distribution arrays DONE_VERIFIED until those runs pass.

## Evidence-based task ledger

| ID | Status | Current evidence | Acceptance / next action |
|---|---|---|---|
| ARCH-001 | DONE_VERIFIED | Canonical data, Python/browser runtimes, generated mirror, schemas, tests and documentation have explicit ownership boundaries. | Preserve; only reorganize if a concrete dependency or maintenance problem is demonstrated. |
| IPA-ADAPTER-001 | DONE_VERIFIED (engineering) | Typed IPA result boundary is exercised by the exact-head Verify run. | Keep target adaptation strictly downstream of typed IPA; linguistic correctness remains a separate gate. |
| PERF-REGISTRY-001 | DONE_VERIFIED | One registry load per `analyze()` is guarded by regression tests; exact-head Verify passed. | Preserve output parity and the load-count guard. |
| BENCH-3ENGINE-001 | DONE_VERIFIED (diagnostic run) | Immutable model revisions, aggregate-only benchmark artifact and successful exact benchmark run. | Keep metrics labelled as reference-relative diagnostics; do not call them accuracy. |
| DOC-012–016 | DONE_VERIFIED | README terminology, limitation scope, validation status, audit index and handoff reconciled; exact-head Verify 42388269091 passed on 62483d900e5c4a620828ae24319ddd6b5c741f27. | Re-open only if subsequent documentation changes invalidate these statements. |
| ENG-LOCK-001 | TODO | `package-lock.json` absent; workflow uses `npm install`. | Generate and verify lockfile in a local Node/npm environment; switch CI to `npm ci`. |
| UI-A11Y-001 | TODO | Automated Chromium checks exist; manual screen-reader, keyboard-only, zoom/text scaling, mobile touch and deployed-site QA are not evidenced. | Record a human QA matrix with browser/device/AT versions, observations and resolved defects. |
| LAO-GOLD-001 | BLOCKED | Independent expert-adjudicated IPA gold = 0. | Requires a versioned target profile and IPA convention, rights-cleared sample, two qualified independent annotators, separate adjudicator, blind workflow and expert-approved contrast coverage. |
| LAO-TONE-001 | PARTIAL | Six candidate minor-syllable cases and four reference-sensitive tone disagreements remain. | Obtain qualified Vientiane review; only then add source-backed rules and independent fixtures. |
| MEKONG-RIGHTS-001 | PARTIAL | Authors' explicit public-release statement supports non-redistributive research use; pinned train-split diagnostics are implemented. Dataset-specific license/root LICENSE and component-level source terms are not declared in the inspected repository. | Continue research and rule discovery with pinned provenance and aggregate-only outputs. Obtain explicit component terms before mirroring, redistributing, sublicensing or commercial reuse. |
| MEKONG-TRAIN-001 | DONE_VERIFIED (initial full diagnostic) | 6,219-row pinned train-split run 42386956616 succeeded; aggregate-only artifact inspected; no rules were changed from unadjudicated references. | Keep this split development-only; preserve the 100-row comparator separately and require independent expert IPA gold for accuracy claims. |
| MEKONG-TRAIN-002 | DONE_VERIFIED | Exact SHA/duplicate guards, IPA-inventory-token edit profile, non-established context filter and focused tests passed in diagnostic run 42388029325 and full Verify 42388033575 on code commit 3efc0ccb. | Use the aggregate error profile to prioritize source review; do not tune from train labels or promote them to gold. |
| ENGINE-GRAPHEME-001 | DONE_VERIFIED (engineering) | Existing onset/coda, full vowel-pattern, onset-cluster and tone-context rules are exercised by positional regression tests; Verify 42390739133 passed on code checkpoint 16d267664beb25a9e26e9639aace42a2975582d1. | Preserve structural, compositional processing; never add word-to-IPA lookup fallbacks. |
| IPA-INVENTORY-002 | DONE_VERIFIED (engineering) | Labialized onset units, long schwa and schwa offglide are recognized as typed IPA segments; target adaptation remains fail-closed without an approved correspondence. | Extend target mappings only with explicit Ukrainian policy evidence. |
| MEKONG-GRAPHEME-001 | DONE_VERIFIED (base diagnostic) | Full train-split grapheme-context run 42390734319 succeeded; aggregate engine/reference context distributions inspected. | Keep train references as development evidence, not independent gold. |
| MEKONG-GRAPHEME-002 | PARTIAL | Direct grapheme-position and broader phonological-context distributions plus aggregate-only output test added in commits 43a2cfeb, 990ea683 and 3151d652; exact-head CI is pending. | Require exact-head diagnostic and Verify before DONE_VERIFIED; then inspect generated aggregate artifact. |
| LAO-GRAPHEME-COVERAGE-001 | PARTIAL / fail-closed | 399/6,219 train rows are withheld by parser warnings; no unsupported structure is guessed. | Review warning families with primary orthographic evidence and expert input; expand coverage only with regression fixtures. |
| LAO-PARSER-001 | PARTIAL / fail-closed | Three parser-tail structures and one malformed tone-mark case remain withheld. | Resolve with primary evidence and qualified review; preserve fail-closed output meanwhile. |

## Readiness judgement

**Research-ready as an engineering and evidence-management prototype, including research use of MekongPhon under the authors' stated release purpose; not linguistically release-ready or publication-ready.** The selected branch has a successful exact-head engineering workflow and reproducible aggregate benchmark, but independent expert gold, qualified tone adjudication, broader source-data rights and manual accessibility QA remain unresolved. A green engineering workflow is not a phonetic accuracy certificate.

*Review date: 2026-11-07. This report describes the inspected branch state and is not a legal opinion or a linguistic certification.*


## Documentation patch verification state

The audit, README, validation note, audit index, handoff and agent-reference refresh were committed to the selected branch in the following sequence:

- Audit document: `de423189a96eae9e696713caa8b459e78f624295`.
- README: `a38a02c9bcf5ee90be4bce793190da4e4e92a77b`.
- Validation guide: `77bee3257a962b819dbb5164badad38f419bc488`.
- Audit index: `41ae3c036923d8bbfdeb5462c317b9e55d8ffd56`.
- Master handoff: `16676040c0a0d8943faa4315e86008e5281c9237`.
- Agent-reference refresh / initial six-file documentation batch checkpoint: `d4f08fb6626136e699f05df40f1c7a3e84ad122b`; subsequent verification-boundary updates are recorded in the master handoff.

Documentation content at `de69f329048cd7de5d8da5d183d0962bdcf26f18` passed exact-head Verify [42388269091 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388269091); DOC-012–016 are DONE_VERIFIED. The later source-scope evidence update is `62483d900e5c4a620828ae24319ddd6b5c741f27`, with Verify [42388391166] QUEUED at the last check. The code-bearing diagnostic commit `3efc0ccb54887830157915e8b4b84ad9177e1720` passed Verify [42388033575 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388033575) and train diagnostics [42388029325 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388029325).


## Latest continuation checkpoint — 2026-11-07

- Branch / PR head at this documentation checkpoint: `9a276b80e26c073dd75c43d0b359c89b926b26e8`; PR [#140](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/140) remains open against `benchmark/mekongphon-immutable-inference-20261107\). The branch is 278 commits ahead of `main`, 0 behind; `main` is untouched.
- New report: `docs/audits/current/MEKONGPHON-GRAPHEME-CONTEXT-ANALYSIS-2026-11-07.md`; README and documentation index now explain the context-sensitive, non-lexical engine contract.
- Last completed exact-head code Verify remains [42390739133 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390739133) on code checkpoint `16d267664beb25a9e26e9639aace42a2975582d1`; matching base grapheme-context diagnostic [42390734319 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390734319).
- The direct `grapheme_position_rules` and broader `phonological_context_rules` output arrays, plus aggregate-only serialization tests, are later code/test additions. Diagnostic run [42391252559] and latest exact-head Verify [42391693342] are pending/queued at this checkpoint; no success is claimed for them.
- Research-use scope remains: authors' stated public release purpose supports research and rule discovery. Raw source rows are not committed or retained in artifacts; independent ClippyFirst gold remains 0. Broader redistribution, sublicensing and commercial reuse remain separately gated by component-specific terms.
- The 399 parser-withheld rows, profile-sensitive IPA differences, independent gold, qualified Vientiane adjudication, npm lockfile/clean-install reproducibility and manual accessibility QA remain unresolved.


## Final branch-head reconciliation — 2026-11-07

- Branch head before this reconciliation: `98241b8e751bcf5004bf4e46313c7b5836337558`; PR #140 remains open; branch is 278 commits ahead of `main`, 0 behind. `main` is untouched.
- Exact-head Verify [42391831295] is pending on that branch head. The last completed full Verify is [42390739133 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390739133) on base contextual-analyzer code `16d267664beb25a9e26e9639aace42a2975582d1`.
- The expanded position/broad-context output and aggregate-only tests are in code/test checkpoint `b376296947c93b1ab01a4a26bdd5afcfc2e756db`; diagnostic [42391252559] remains pending. Therefore MEKONG-GRAPHEME-002 stays PARTIAL.
- Documentation report, README, index, audit and handoff are updated. No unverified run is represented as successful.


## Lao–Ukrainian practical transcription system — 2026-11-07

The user requested a dedicated practical system modelled on the presentation/coverage of the Lao–Russian practical transcription reference, but designed for Ukrainian phonetics and orthography and informed by the existing Thai–Ukrainian ClippyFirst project. The new canonical reference is \`docs/lao-ukrainian-practical-transcription.md\`; README, docs index and the public \`system.html\` page link to it.

### Actual implementation changes

- Preserved the existing IPA-first boundary. No Lao-grapheme → Ukrainian direct mapping was introduced.
- Confirmed the canonical target registry already distinguishes /h/ → г, /ɦ/ → г, /ɡ/ → ґ and /x/ → х; /kʰ pʰ tʰ/ → к’ п’ т’; /ŋ/ → нг; onset /ʋ/ and coda /w/ → в.
- Corrected an inconsistent legacy rime mapping: canonical IPA /aw/ previously mapped to «ау» despite the project rule that /w/ is always Ukrainian «в». It now maps to **ав**. The derived correspondence CSV and generated browser registry were updated with the canonical source.
- Added contextual syllable-initial /j/ adaptation: /ja/ → я; /je, jɛ/ → є; /ji/ → ї; /jo, jɔ/ → йо; /ju/ → ю; /jɯ/ → йи; /jɤ/ → йе. Medial/coda /j/ remains «й». The rule is applied only at the beginning of a typed one-syllable IPA result.
- Mirrored the /j/ rule in Python and browser adapters; added tests for actual Lao analyses and direct IPA adapter cases.
- Added positional onset and coda tables, short/long vowel and diphthong tables, tone/length policy, traditional-name exception policy and source limitations. The Russian table is a structural comparator, not an intermediate mapping.
- The public methodology page now surfaces the core Ukrainian decisions and links to the complete practical transcription reference.

### Verification status at this documentation checkpoint

Branch: \`feature/lao-ukrainian-practical-system-20261107\`, based on PR #140 head \`d8e466321eae05f0a4dfa2944543723f368e0f23\`. Code changes include target Python, browser engine, canonical correspondence registry, generated browser mirror, derived correspondence table and tests. Exact-head CI has not yet been observed for the complete documentation/code head; mark the engineering work PARTIAL until Verify and browser tests pass.

### Acceptance and remaining evidence

- The target choices are explicit project conventions, not an official Ukrainian national standard.
- The /h/ → г, /ɯ/ → и and /ɤ/ → е choices are practical approximations, not IPA identities.
- /aw/ → ав now follows the consistent /w/ → в rule; add source-attested examples and expert review before treating the complete vowel matrix as linguistically adjudicated.
- Traditional Ukrainian exonyms and lexicalized names need a sourced exception registry; do not overwrite established forms with regular output.
- Independent IPA gold remains 0; no new phonetic accuracy claim is made.
- Qualified Ukrainian phonetic/onomastic review and qualified Lao source review remain outstanding.

# Repository structure and documentation audit — 2026-11-06

## Executive result

**Engineering state: reproducible research prototype with a deployed static web instrument. Linguistic/release state: not independently validated and not release-ready.**

This review inspected the current main tree, repository metadata, branch list, recent commits, open/recently closed pull requests, current workflow run, README, agent instructions, product requirements, methodology, implementation map, audit registers, schemas/data layout, Python and browser entry points, build scripts and CI workflows. It also reviewed the five user-supplied engineering/design references for relevant practices.

This is a repository-state and documentation audit, not an independent Lao phonology adjudication, full UI/assistive-technology evaluation, or local clean-install run.

## Baseline and repository control

- Repository: ClippyFirst/Lao-Ukrainian-Phonetic-System.
- Default branch: main.
- Starting commit: 915db62c710bedcbbec6ac01c73cb9312ae9a03d.
- The branch listing returned only main; no other branch was listed in the inspected response.
- No open pull requests were returned.
- PR #136 was closed without merge as superseded. Its proposed language-specific IPA fixture correction was already on main; no duplicate patch was ported. Its source branch was not present in the branch listing, so this report does not claim that branch is preserved.
- Repository metadata reported the default branch as unprotected. No branch-protection or repository settings were changed.
- Latest baseline verification: GitHub Actions Verify run [41889580331](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41889580331), head 915db62c710bedcbbec6ac01c73cb9312ae9a03d, completed SUCCESS. Inspected steps passed: corpus-structure validation, repository data/evidence audit, Python tests, optional G2P CLI validation, browser engine tests, canonical browser-data regeneration/reproducibility, Chromium built-site tests and built-page/relative-asset checks.

## Architecture inventory

The repository has a clear separation of concerns and should retain it rather than undergo a broad directory reshuffle.

| Area | Canonical location | Responsibility |
|---|---|---|
| Python package | src/lao_ukrainian/ | Normalization, parsing, phonology, IPA target adaptation, analysis model and CLI |
| Canonical Lao data | data/lao/*.csv | Consonants, onset clusters, vowels, codas/tone and Ukrainian IPA correspondences |
| Evidence registry | data/evidence/ | Source metadata and claim-to-source links |
| Generated browser data | web/data.js | Deterministic mirror of canonical CSVs; never hand-edit |
| Browser runtime | web/ | Native ES-module engine, UI, and separate romanization route |
| Static pages | index.html, system.html | Converter and methodology page |
| Schemas | schemas/ | Machine-readable analysis and IPA corpus contracts |
| Tests | tests/, web/engine.test.js | Python, browser-engine, cross-runtime, corpus and UI regressions |
| Build/research scripts | scripts/ | Audit, generation, static build, benchmark and corpus validation |
| Current research evidence | docs/audits/current/ | Dated source and phonology workpacks |
| Execution history | docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md | Canonical ongoing task ledger and handoff |

The main phonetic path is Lao orthography → structural parser → source phonology → typed IPA → Ukrainian target adapter. The romanization path is a separate, explicitly lower-information orthographic mode. This architecture is coherent and must not be collapsed into character substitution or silent fallback.

## Findings and resolutions

| ID | Severity | Status | Finding | Resolution / acceptance |
|---|---|---|---|---|
| DOC-001 | P1 | DONE_VERIFIED after exact-head CI | web-architecture.md and PRODUCT-REQUIREMENTS.md described Vite, but package.json has no Vite dependency and scripts/build_web.py simply copies two HTML pages and web/ into dist/. | Corrected both documents and implementation notes to describe the actual framework-free native-ES-module build. |
| DOC-002 | P1 | DONE_VERIFIED after exact-head CI | The master handoff ended with a 2026-11-04 entry describing PR #130's Chromium check as still running, while main had advanced through later commits to #135. | Appended a current-main checkpoint with the exact starting head, verified CI evidence, branch/PR reconciliation and current blockers. |
| DOC-003 | P1 | DONE_VERIFIED after exact-head CI | final-audit.md was titled "Final scientific audit" but its early conclusions and limitations predate later implementation work. This could be mistaken for the current state. | Added a historical-record notice and links to the current audit index and live handoff. Historical content was retained, not silently rewritten. |
| DOC-004 | P2 | DONE_VERIFIED after exact-head CI | There was no central documentation landing page; README listed only a subset of the available research and engineering documents. | Added docs/README.md and replaced the partial README list with links to the index and canonical handoff. |
| DOC-005 | P2 | DONE_VERIFIED after exact-head CI | No root CONTRIBUTING.md existed, despite agent instructions asking reviewers to inspect contribution standards. | Added a concise contributor guide with environment requirements, exact test commands, data ownership, evidence and privacy rules. |
| ENG-001 | P1 | BLOCKED / owner action | The default main branch is not protected in the inspected repository metadata. A passing CI run therefore does not itself prevent direct unreviewed writes. | Repository owner should configure a ruleset requiring the Verify workflow and review for routine changes. This requires a repository-settings decision and was intentionally not changed here. |
| ENG-002 | P2 | TODO | No npm lockfile is present. The Playwright direct dependency is pinned, but transitive npm resolution is not frozen. | Generate and commit package-lock.json in a Node/npm-enabled clean checkout, switch CI to npm ci, and verify the exact lockfile on a clean runner. Not fabricated in this connector-only pass. |
| LAO-GOLD-001 | P1 | BLOCKED | Independent expert-adjudicated IPA gold remains empty; gold.tsv is header-only and empirical accuracy must remain null. | Requires a confirmed target profile/convention, lawful item-level source access, two independent qualified annotators, a separate adjudicator, blind intake and the versioned pilot acceptance described in the collection playbook. |
| LAO-UI-001 | P2 | TODO | CI covers Chromium flows and selected accessibility hooks, but does not establish manual screen-reader, keyboard-only, mobile-device or visual QA. | Record a human QA matrix with device/browser/AT versions, observed results and resolved defects. |
| LAO-TARGET-001 | P1 | PARTIAL / evidence-limited | Some IPA sequences (including registered labialized-onset values) intentionally have no Ukrainian target mapping; output is withheld rather than guessed. Other project correspondences still require expert review. | Add a target only with source-located phonetic evidence and documented Ukrainian adaptation rationale; never treat withheld output as a CI defect by itself. |

## Documentation and structure decisions

- Keep data/lao/ as the only canonical Lao linguistic registry; web/data.js remains generated.
- Keep evidence claims and sources machine-readable under data/evidence/.
- Keep the large master handoff as the canonical append-only execution ledger; do not split it into competing status files in this pass.
- Keep dated audits and workpacks under docs/audits/current/; historical audit prose remains linked but is not current authority.
- Use docs/README.md as the document map and docs/audits/README.md as the audit/evidence map.
- Do not rename/move implementation directories: the current package/data/test boundaries are understandable, referenced by workflows and already reflected in codebase-map documentation. A broad path migration would create link churn without solving a demonstrated architecture defect.

## External references reviewed

- [unlazy](https://github.com/Leonxlnx/unlazy): the project already adopted evidence-bound completion gates, observable acceptance criteria and exact-final-head verification in AGENTS.md; no runtime tool or copied framework was added.
- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): reviewed as a design-method reference. The repository's own docs/DESIGN-SYSTEM.md and product requirements already prescribe the relevant data-first, accessible, restrained visual direction. Its large generic style/rule catalog was not imported because it would duplicate local policy and risk steering the research instrument toward unrelated SaaS/marketing patterns.
- [Superpowers](https://github.com/obra/superpowers): existing agent instructions already adopt scoped planning, test-first implementation, root-cause debugging and verification-before-completion.
- [mattpocock/skills](https://github.com/mattpocock/skills): existing instructions already adopt composable engineering practices, behavior-focused tests, deep modules and two-axis review.
- [Ponytail](https://github.com/DietrichGebert/ponytail): existing agent instructions already adopt connected-code/data-flow review, minimal complete changes and explicit residual-risk reporting.

These references are methods, not dependencies. The repository's linguistic, source-rights, privacy and fail-closed requirements remain authoritative.

## Documentation-link integrity

A local-path scan was performed across the repository Markdown inventory. It found three broken relative links in the master handoff (IPA gold protocol, phonology workpack and tone–rhyme matrix); all three were corrected to paths relative to the handoff's docs/ directory. External URLs and heading-anchor existence were not exhaustively validated.

## Verification evidence and limits

- Baseline hosted Verify: [41889580331](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41889580331) SUCCESS on starting commit 915db62c710bedcbbec6ac01c73cb9312ae9a03d.
- This connector session did not provide a local repository checkout or a local Python/Node execution environment. No local test, benchmark, clean-install, package-lock generation or deployed manual QA is claimed.
- Exact-head Verify is the acceptance gate for the documentation changes. Read its result against the precise commit SHA shown in the workflow; the earlier baseline success is not a substitute for final-head verification.
- The external human-review, licensing and manual UI gates remain outside what repository CI can prove.

## Final readiness judgement

**Research-ready as an engineering and evidence-management prototype; not linguistically release-ready.** The architecture and automated engineering gate are coherent, but the empty expert gold corpus, unresolved target correspondences, external source/rights steps, manual accessibility QA and unprotected default branch prevent a production or publication-grade claim.


## Exact-head verification result

The documentation and link-correction implementation checkpoint `b96aa19f740c2e8fe3d7678faed02d7e21356a1e` passed exact-head Verify [42299492015](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42299492015) with conclusion **SUCCESS**. All configured workflow steps passed, including corpus validation, repository audit, Python tests, optional G2P CLI validation, browser tests, generated-data reproducibility, Chromium built-site tests and built-page/relative-asset checks. This is hosted engineering verification, not a local test run or linguistic validation. The master handoff records the exact commands and evidence.


## Follow-up implementation — typed IPA → Ukrainian boundary — 2026-11-07

The previous audit identified that the repository described an IPA-first pipeline but its implementation passed an ordinary IPA string directly to the target mapper. This was a real architectural gap, not a missing correspondence table.

**Resolution implemented on `main`:**
- Added a typed `PhoneticResult`/`PhoneticSegment` boundary and dedicated `phonetic_result.py` constructor.
- Python and browser target adapters now consume typed IPA segments only; the Python adapter rejects raw strings. Both preserve segment offsets, tone/contour, vowel length, provenance and uncertainty.
- `UNCERTAIN` segmental IPA and `UNSUPPORTED`/incomplete IPA are withheld. An unresolved tone alone remains separate metadata and does not suppress an otherwise supported segmental Ukrainian form.
- Preserved the canonical Ukrainian correspondence CSV and the optional romanization route unchanged.
- Added Python/browser regressions, expanded the analysis JSON schema, and documented the contract in `docs/ipa-to-ukrainian-adapter.md`.

The implementation checkpoint before this audit addendum is `fc81a67d63d85a3fd26d5e51e48be63f82a0c3cc`. The exact final documentation-head Verify run must pass before this work is classified DONE_VERIFIED. No local test execution or benchmark is claimed. Independent IPA gold remains empty; this is an engineering boundary correction, not linguistic certification.

## Typed IPA adapter follow-up — verification gate — 2026-11-07

**Implementation status: PARTIAL pending exact-head CI.**

The code-bearing checkpoint is `9279e59fd6cfc7aee6c7350d4a9992a8e958ad86`. The previous raw-string path has been replaced by a typed Python/browser boundary. Source IPA tokenization now uses an independent IPA inventory; the Ukrainian adapter applies target-specific longest matching over typed segments. Tone uncertainty remains distinct from segmental IPA support. Tests and the analysis JSON schema were expanded.

The current connector session did not expose the push-triggered mainline Actions run for this SHA (the available workflow-run endpoint is PR-only). The web-scrape fallback was unavailable due exhausted connected-account credits. Therefore exact-head CI is **NOT VERIFIED**, not passed and not failed. Acceptance requires the complete Verify workflow on the final current main SHA. No local test run or benchmark is claimed.

Linguistic acceptance remains separately blocked by the empty independent IPA gold corpus and lack of independent expert validation.

## Rule-engine error analysis and integration checkpoint — 2026-11-07

The immutable two-model inference experiment was followed by aggregate-only edit analysis and two narrowly scoped deterministic-engine refinements.

**Implemented on the stacked follow-up branch / PR #140:**
- Canonical IPA for Lao ຈ now uses tied affricate `t͡ɕ`; un-tied `tɕ` remains accepted by the IPA target adapter. Python and browser data mirrors and shared regression fixtures were updated together.
- A separate special-tone registry flags an initial unmarked short-open-/a/ shape before a major-weighted syllable as a potential minor syllable. Segmental IPA remains available; independent tone is analysis-dependent and withheld. No neutral tone contour is invented.
- Benchmark diagnostics now aggregate code-point edit substitutions/insertions/deletions, syllable position, tone-rule contexts and unresolved-tone contexts. Artifacts contain aggregate counts only, not source words or per-item predictions.
- The existing five-tone Vientiane matrix was not retuned: observed tone disagreements remain consistent with the source-scoped matrix and differ from the dictionary reference.

**Evidence:** benchmark [42374547901](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901) SUCCESS; aggregate artifact [13575161811](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901/artifacts/13575161811). On the shared 97 segmental items ClippyFirst now scores CER 6.49% / 69 exact, versus Lao2IPA 7.72% / 68 exact and MekongPhon neural 5.79% / 81 exact. Full ClippyFirst segmental coverage is 97%; tonal coverage is 91%. These remain dictionary-reference metrics, not independent linguistic gold.

**Current disposition:** DONE_VERIFIED for the implemented engineering refinements. Final full Verify [42375716368](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42375716368) passed on `b325a5f91a3fdf063f231537d1550a140cb2eff8`, including Python, browser, generated-data, Chromium UI, and built-page checks. The potential minor-syllable tone uncertainty is mirrored in both runtimes. Independent expert IPA gold remains 0; the six candidate minor-syllable contexts require qualified Vientiane review. The three parser-tail structures and malformed tone-mark case remain fail-closed. MekongPhon corpus/source rights remain UNKNOWN.


## Selector-boundary refinement checkpoint — 2026-11-07

PR #140 now requires a supported/core onset and a supported segmental IPA before applying the potential minor-syllable tone-withholding selector. The next syllable must be in the same unspaced token and be major-weighted by a long vowel, diphthong or coda. Explicit spaces block the relation. This narrows false-positive risk; it does not establish that the candidate is truly a minor syllable.

Python/browser tests now cover the positive case, non-major following syllable, whitespace boundary and uncertain onset. README's runtime contract describes dynamic within-token segmentation in both runtimes; both public APIs reject U+200B during Unicode validation. Aggregate benchmark diagnostics distinguish broad C₀V₀ shapes from the narrower open-/a/ selector and include diphthong-bearing major syllables.

**Status: PARTIAL pending exact-head full Verify.** Run [42381443428](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42381443428) is queued for head `759091f28cc57a746df549ac573067af9be922ab`. Prior run [42375870451](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42375870451) passed but predates this refinement. No local test run is claimed. Linguistic acceptance remains evidence-limited pending qualified Vientiane review; independent IPA gold remains empty.


## Final schema 4.0 and selector checkpoint — 2026-11-07

The Python and browser engines now use the same source-backed special-tone registry: Python reads `special_tone_rules.csv`; the browser receives the same rule via generated `SPECIAL_TONE_RULES` in `web/data.js`. The selector requires a supported/core onset and segmental IPA, an unmarked short open /a/, no local parse warnings, and a long-vowel/diphthong/coda-bearing following syllable in the same token. Segmental IPA and Ukrainian adaptation remain available while independent tone is withheld.

The benchmark had been stringifying `None` as `"None"`, falsely treating unresolved tone as a category. Schema 4.0 preserves nulls, scores only known aligned categories, excludes unresolved values from the confusion matrix, and reports category coverage, unresolved counts and word-length mismatches separately. U+200B is rejected by both public APIs; README and regression tests now document that rather than implying it is a valid separator.

**Verification:** full Verify [42382503937 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382503937) on `d4ea4f692b9376fd1236c8eaf7d4ae41683f5201`; schema 4.0 three-engine benchmark [42382431568 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382431568), artifact [13577779873](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382431568/artifacts/13577779873), SHA-256 `dff1a93a429e590e791147f856e867eb508db555d53e35e10f5bedc0c4ce530d`.

**Status: DONE_VERIFIED for engineering and benchmark integrity; PARTIAL for linguistic acceptance.** Six possible minor-syllable candidates and four known tone discrepancies require qualified Vientiane review. Independent project IPA gold remains 0, and MekongPhon source/corpus rights remain UNKNOWN.


## Registry-reuse performance checkpoint — 2026-11-07

The Python `analyze()` path now reuses one loaded linguistic registry through segmentation and parsing rather than repeatedly loading CSV registries per token/syllable. No linguistic rules or output contracts changed.

**Verification:** Full Verify [42382964250 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382964250); schema 4.0 benchmark [42382960457 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382960457), artifact [13578092183](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382960457/artifacts/13578092183), SHA-256 `8d25f1032805e7e38339449d658d9efc4167329f4ea25d82c4de26a7ad54b655`. Mean ClippyFirst per-item latency on this hosted 100-word run was 4.724 ms versus 14.207 ms on the immediately preceding run before registry reuse (model loading excluded; single-run observation). All three engines had zero runtime errors.


## Full-pipeline registry-reuse correction — 2026-11-07

The previous registry-reuse checkpoint overstated the optimization boundary. A call-path inspection found repeated registry reads remained in phonology (`phonologize`, `determine_tone`, `classify_syllable_type`) and target adaptation (`rank_ukrainian_candidates`, `practical_from_ipa`). These were not covered by the earlier segmentation/parser-only pass.

The deterministic engine now threads the registry loaded by `analyze()` through those stages as well. Public helper calls remain backward compatible because the registry argument is optional and the old lazy-load behavior remains available when omitted. The minor-syllable lookahead is also limited to the first syllable of each orthographic token.

Regression coverage:
- A focused phonology/target test makes downstream registry loading raise if a supplied registry is ignored.
- A full-pipeline test makes parser, phonology and target registry reloads raise and checks that `analyze()` loads the registry exactly once.
- A previous intermediate failure was a test expectation error (long open /aː/ is live, not dead); the expectation was corrected. No production phonology rule was changed by that correction.

**Status: PARTIAL pending exact-head CI and refreshed three-engine benchmark.** Latest code/test checkpoint before this audit note: `2ddb0dbb250268f2477a2614a1f3fc676a9b89e3`; full Verify [42384603376](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384603376) and benchmark [42384500017](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384500017) were queued at the time of writing. No final performance claim is made until the refreshed benchmark artifact is inspected.


### Verification addendum — full-pipeline registry reuse

The new registry-threading implementation passed full Verify [42384505842](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384505842) on source head `89a08fae9feafa4739fc698e99adde709c978b66`. A dedicated end-to-end test then asserted exactly one registry load across a two-syllable `analyze()` call, with parser/phonology/target reloads patched to fail; full Verify [42384603376](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384603376) passed on test head `2ddb0dbb250268f2477a2614a1f3fc676a9b89e3`.

The refreshed three-engine benchmark [42384500017](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384500017) passed and produced aggregate artifact [13578308566](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42384500017/artifacts/13578308566), SHA-256 `996844312d068145673af57da8e07be48cb241c31cb5be55ef295802a803a6bc`. ClippyFirst mean per-item latency was 1.533 ms versus 4.724 ms on the earlier hosted run, a 67.5% lower single-run observation with model loading excluded. Accuracy and coverage were unchanged. All three engines had zero runtime errors.

**Status: DONE_VERIFIED** for registry threading, end-to-end reload guard, and refreshed benchmark. Linguistic acceptance remains PARTIAL pending qualified review of the six possible minor-syllable candidates and four dictionary-reference tone disagreements; independent IPA gold remains 0.

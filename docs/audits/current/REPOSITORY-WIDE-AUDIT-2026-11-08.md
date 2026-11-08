## Primary engine decision — hybrid deterministic (2026-11-08)

The owner selected `hybrid-deterministic` as the primary ClippyFirst Lao engine. Implementation head `3484db557589cb39cb638133addfa97a887016d6` changes Python API, CLI and browser defaults from Vientiane to hybrid. Vientiane remains the phonological baseline and an explicit compatibility profile; MekongPhon-reference remains available for comparison. Neural inference is not in the default transcription path. Exact-head Verify [42511764559 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42511764559): 283 Python, 136 Node and 17 Chromium tests passed; corpus/evidence validation, clean install, build, generated-data reproducibility and built-site checks passed. The benchmark evidence remains reference-relative/stress-only, and independent adjudicated IPA gold remains 0.

---

# Repository-wide audit and continuation — 2026-11-08

## Executive assessment

**The integrated PR #143 branch is an engineering-verified research prototype. It is not linguistically validated or release-ready.** Exact-head GitHub Actions Verify passed on `74b178654e9825bdcfa5b83fd31603b9cc74cd69`: 262 Python tests, 126 Node tests and 17 Chromium tests, plus clean npm installation, corpus/schema validation, repository data/evidence audit, build, generated-data reproducibility and built-page checks.

The default branch `main` remains unchanged at `f40c1128302486b3589da9b16bae198ef3ad1d81`. The work is consolidated on the single continuation branch `audit/repository-docs-structure-20261107`, in open PR [#143](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143), which GitHub currently reports as mergeable. No merge, release, deployment, force-push, branch deletion or repository-settings change was performed.

This is an engineering, repository-structure, documentation, CI and design-system audit. It is not independent Lao phonetic adjudication, a legal opinion, a full security penetration test, or manual assistive-technology certification.

## 1. Baseline, branch and evidence

| Item | Verified state |
|---|---|
| Repository | `ClippyFirst/Lao-Ukrainian-Phonetic-System` |
| Default branch | `main` |
| Starting main SHA | `f40c1128302486b3589da9b16bae198ef3ad1d81` |
| Single working branch | `audit/repository-docs-structure-20261107` |
| Exact verified head | `74b178654e9825bdcfa5b83fd31603b9cc74cd69` |
| Pull request | [#143](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143), open and mergeable, base `main` |
| PR diff | 82 files, 6,736 additions, 310 deletions |
| GitHub compare | 454 commits ahead, 0 behind |
| Exact-head Verify | [42462626019 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42462626019) |

The compare count reflects the branch's integrated commit ancestry; the PR file diff is the more useful measure of its current content. The branch was reused from the previous work rather than creating parallel branches.

No local repository checkout or local test execution is claimed. The current session used GitHub repository/tree/file/PR inspection and the hosted Actions evidence above.

## 2. Architecture and structure decision

The existing repository boundaries are coherent. A broad folder migration, framework replacement or second documentation system would add churn without resolving an acceptance blocker. Preserve these canonical ownership boundaries:

| Area | Canonical location | Responsibility |
|---|---|---|
| Python implementation | `src/lao_ukrainian/` | Normalization, structural parsing, phonology, typed IPA, target adaptation, API and CLI |
| Optional neural provider | `src/lao_ukrainian/mekongphon.py` | Explicitly selected, pinned optional model inference; not the deterministic default |
| Canonical Lao registries | `data/lao/*.csv` | Consonants, onset clusters, vowels, codas, tone rules, special tone rules, target correspondences and grapheme inventory |
| Evidence provenance | `data/evidence/sources.csv`, `claims.csv` | Source metadata and claim-to-source links |
| Generated browser data | `web/data.js` | Deterministic mirror generated from canonical CSV; never hand-edit |
| Browser runtime/UI | `web/engine.js`, `web/app.js`, `web/romanization*.js`, `web/styles.css` | Native ES modules and UI; separate phonetic/romanization routes |
| Static pages/build | `index.html`, `system.html`, `scripts/build_web.py` | Two-page local-first instrument and static `dist/` output |
| Contracts | `schemas/` | Analysis, comparator and IPA-gold JSON schemas |
| Tests | `tests/`, `web/engine.test.js` | Python, Node, shared fixtures and Playwright Chromium |
| Research/build tooling | `scripts/` | Audit, data generation, benchmarks, diagnostics and corpus validation |
| Documentation | `docs/`, `AGENTS.md`, `GLOSSARY.md`, `CONTRIBUTING.md` | Specification, methodology, limitations, evidence, decisions, audit and handoff |

### Pipeline boundary

The accepted phonetic route is:

`Lao orthography → structural syllable analysis → source-language phonology → typed IPA → Ukrainian target adaptation → practical Ukrainian orthography`.

The typed IPA layer is a real adapter boundary, not a parallel audit display. The target adapter consumes typed IPA segments and withholds unsupported/uncertain input. The optional CLDR/BGN-oriented romanization route is a separate, lower-information orthographic method; it cannot reconstruct tone and is not a fallback for failed phonetic analysis.

The grapheme preview is a third, explicitly provisional diagnostic layer. It must not be described as accepted IPA, must not infer tone and must never be passed into the accepted Ukrainian target adapter.

### Repository organization

Keep the current top-level organization. Canonical data remains in `data/lao/`; provenance in `data/evidence/`; schemas in `schemas/`; current audits in `docs/audits/current/`; generated browser data in `web/data.js`; the single canonical execution ledger remains `docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md`.

## 3. Branch and PR reconciliation

| PR | Head branch | Dependency/base | Disposition in this pass |
|---|---|---|---|
| #137 deterministic G2P improvements | `benchmark/mekongphon-three-engine` | `main` | Open; changes integrated into PR #143 branch |
| #138 optional MekongPhon integration / rights audit | `audit/repository-documentation-and-mekongphon-rights-20261107` | #137 branch | Open; dependency branch inspected; changes represented in consolidated PR #143 |
| #139 immutable MekongPhon inference benchmark | `benchmark/mekongphon-immutable-inference-20261107` | #137 branch | Open; benchmark work represented in PR #143 |
| #140 tone-rule guards and aggregate diagnostics | `improve/rule-engine-error-analysis-20261107` | #139 branch | Open; changes integrated in PR #143 |
| #141 practical Lao–Ukrainian target adapter | `feature/lao-ukrainian-practical-system-20261107` | #140 branch | Open; changes selectively ported/integrated in PR #143 |
| #142 grapheme inventory and provisional IPA preview | `feature/grapheme-fallback-ipa-preview-20261107` | #141 branch | Open; changes integrated in PR #143 |
| #143 consolidated continuation | `audit/repository-docs-structure-20261107` | `main` | Open, mergeable; sole branch used for this continuation |

PRs #137–#142 were not closed, retargeted, force-pushed or blindly merged. PR #143 contains their reviewed implementation lineage and the documentation/accessibility/lockfile work. Keep #143 as the single integration proposal; review its complete diff before merging.

## 4. Implementation audit

### 4.1 Structural segmentation and tone

The parser uses dynamic programming to segment unspaced Lao text into structurally parsed syllable candidates while preserving unresolved material. It is not a lexical word segmenter. Tone-mark placement/order is checked per syllable; malformed marks, incomplete vowel/coda structures and unsupported suffixes must not retain a confident tone or expose a misleading IPA prefix.

The Python and browser implementations share canonical data and regression fixtures for their explicitly shared contracts. Their full phrase-level normalization/segmentation behavior is not a blanket parity guarantee.

### 4.2 Typed IPA and Ukrainian adapter

The source IPA tokenizer uses its own IPA inventory rather than deriving source segmentation from Ukrainian target keys. Typed results preserve segment identity, boundaries, length, tone metadata, provenance and uncertainty. The Ukrainian adapter consumes typed results and fails closed on unsupported or uncertain material. Target conventions such as initial yodation, medial/coda /j/, diphthong preservation and /w/ → в are project policy, not an official Ukrainian national standard.

### 4.3 MekongPhon

The optional provider is explicitly selected; the deterministic rule engine remains the default. Model revisions are pinned, silent truncation is disabled, the model's 128-token limit is enforced, raw IPA and provenance are retained, and unknown IPA symbols fail closed. The provider does not silently fall back to deterministic rules.

The project owner confirmed MekongPhon project rights were resolved in the prior project conversation. Record this as **owner-confirmed**, not as an independent legal opinion. The external dictionary/model references remain comparator material and are not the project's independent adjudicated IPA gold.

### 4.4 Grapheme inventory and provisional preview

The Unicode 18 Lao-block inventory contains 83 assigned code points with scope/role classification and source/claim links. Unicode codepoint identity establishes character identity, not phonetic value.

The fallback preview reuses registered positional onset/cluster values and parser-confirmed complete vowel/coda structures. Unresolved graphemes remain visible. Tone is not inferred; preview output is `PROVISIONAL` and is excluded from the accepted Ukrainian adapter. Unsupported Pali/Sanskrit/Khmu cases remain unresolved rather than guessed.

### 4.5 Static web and design system

The service remains a two-page, local-first, framework-free static application with native browser ES modules. Canonical CSV data is generated into `web/data.js`; the build copies pages/runtime to `dist/`. No React/Vite/Webpack dependency is justified.

The visual direction remains an editorial linguistic instrument, not a generic SaaS dashboard. The reference repositories inform methods and design checks only; no generic skill bundle or runtime dependency is vendored.

## 5. Reference repository audit

| Reference | Applicable practice | Project disposition |
|---|---|---|
| [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy) | Observable acceptance gates, task decomposition and evidence-linked completion | Use the existing master ledger and CI; do not import a duplicate gate framework |
| [UI UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Design tokens, component states, responsive and accessibility checks | Retain the existing Lao editorial design system; adopt only relevant checks, not generic SaaS templates |
| [obra/superpowers](https://github.com/obra/superpowers) | Test-first work, systematic debugging, explicit review and verification | Already reflected in `AGENTS.md` and `CONTRIBUTING.md`; no plugin runtime is vendored |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Deep modules, behavior-focused tests, clear interfaces and source-backed research | Apply at public seams; no parallel handbook or skill tree |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Whole-flow data tracing, trust boundaries, smallest complete fix and residual-risk reporting | Applied to code/data-flow review; no new runtime dependency |

These are engineering/design references, not project dependencies or linguistic authorities. Project-specific source evidence, provenance, privacy, rights and fail-closed requirements take precedence.

## 6. Exact-head verification

[Verify #42462626019](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42462626019) ran on the exact branch head `74b178654e9825bdcfa5b83fd31603b9cc74cd69` and completed **SUCCESS**.

| Gate | Result |
|---|---|
| Independent IPA corpus structural validation | PASS — structure valid; empty gold is not promoted |
| Repository data/evidence audit | PASS |
| Python unittest discovery | PASS — 262 |
| External-G2P harness syntax/CLI | PASS |
| Locked Node installation | PASS — `npm ci --no-audit --no-fund` |
| Node suites | PASS — 126 |
| Static build / canonical browser data generation | PASS |
| Generated-data reproducibility | PASS — no `web/data.js` drift |
| Playwright Chromium UI | PASS — 17 |
| Built-page and relative-asset assertions | PASS |

Commands configured in the hosted workflow include:

```bash
python scripts/ipa_gold_corpus.py validate --language lao
python scripts/audit.py
PYTHONPATH=src python -m unittest discover -s tests -v
python -m py_compile scripts/compare_external_g2p.py
PYTHONPATH=src python scripts/compare_external_g2p.py --help
npm ci --no-audit --no-fund
npm test
npm run build
git diff --exit-code -- web/data.js
npx playwright install --with-deps chromium
npm run test:browser
```

The successful workflow is exact-head engineering evidence for PR #143. It is not mainline post-merge verification, Pages deployment evidence for this branch, expert phonetic adjudication or manual accessibility certification.

## 7. Task ledger and acceptance status

| Task | Status | Evidence / remaining acceptance |
|---|---|---|
| Repository structure and documentation audit | DONE_VERIFIED | Full tree, entry points, docs, schemas, tests, workflows and PR stack inspected; this report and code map updated |
| Single-branch integration | DONE_VERIFIED | Existing PR #143 branch reused; no parallel branch created |
| Dynamic structural syllabification and tone-mark validation | DONE_VERIFIED (engineering) | Exact-head Python/Node suites pass; not lexical word segmentation |
| Typed IPA → Ukrainian adapter | DONE_VERIFIED (engineering) | Typed source IPA boundary and target-only adapter covered by regression tests |
| MekongPhon optional provider and benchmark | DONE_VERIFIED (engineering) | Immutable inference and aggregate workflows recorded; external reference is not project gold |
| MekongPhon project rights | DONE_VERIFIED (owner-confirmed) | Owner confirmation; not an independent legal opinion |
| Grapheme inventory / provisional preview | DONE_VERIFIED (engineering) | 83 assigned code points; preview remains provisional and tone-free |
| `package-lock.json` and clean install | DONE_VERIFIED | Exact-head `npm ci` passed |
| Automated accessibility and responsive regression | DONE_VERIFIED | 17 Chromium tests, including keyboard, semantics, reflow, touch emulation, forced-colors and reduced-motion |
| TGT-01 44×44 hit-area checks | DONE_VERIFIED | Exact-head Chromium assertion passes at 320/390/768/1280 CSS px |
| UI-001 manual accessibility | PARTIAL | Actual screen readers, physical devices, real browser zoom, deployed keyboard walkthrough and human contrast/visual review remain NOT RUN |
| Independent adjudicated IPA gold | BLOCKED | Independent gold count remains 0; requires source-eligible double annotation, independent adjudication, frozen splits and expert-approved convention/coverage |
| Empirical linguistic accuracy | BLOCKED / NOT MEASURED | No accuracy denominator exists; never infer accuracy from dictionary comparison, model agreement or engineering tests |
| Broad dialect, lexical-name and unsupported-script coverage | PARTIAL / TODO | Needs scoped primary sources and qualified Lao linguistic review; unsupported output remains withheld |

## 8. Remaining blockers and acceptance criteria

1. **Manual accessibility QA — PARTIAL.** Run and record NVDA/JAWS/VoiceOver/TalkBack, a full keyboard-only deployed walkthrough, physical iOS/Android devices, actual browser zoom at 200%/400%, and human contrast/visual review. Record OS, browser, AT/device versions, deployed commit, steps, results and retests in `docs/accessibility-manual-qa.md`.
2. **Independent IPA gold — BLOCKED.** Collect rights-eligible source-located Lao lexical items; approve the IPA convention and contrast coverage with a qualified specialist; obtain two independent annotations through a controlled blind intake channel; use a separate qualified adjudicator; freeze lexeme-group-disjoint splits; validate the export and score only held-out adjudicated items.
3. **Linguistic review — BLOCKED / evidence-limited.** Review tone/rhyme rules, loanwords, conventional names, rare clusters, Pali/Sanskrit and Khmu values with qualified Lao specialists. Every accepted rule needs a scoped source and a clear claim boundary.
4. **Release readiness — BLOCKED.** Re-run exact-main Verify and Pages deployment after PR #143 is reviewed and merged through the owner's normal process; complete manual accessibility and independent linguistic acceptance first. This audit does not merge the PR.

## 9. Readiness decision

**Engineering-verified research prototype; not production/release-ready and not accuracy-validated.**

The engineering workflow is green on the exact PR #143 head. The main branch remains unchanged. Independent adjudicated IPA gold is empty, empirical accuracy is not measured, and manual assistive-technology/physical-device QA is incomplete. Do not market or document the project as a validated universal Lao-to-Ukrainian transcription standard.


## 10. Post-merge and GitHub Pages verification — 2026-11-08

The earlier sections above are a pre-merge audit snapshot. Their statements that PR #143 remained open and `main` was unchanged are superseded by this post-merge checkpoint.

- PR [#143](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/143) was squash-merged. Merge commit and new `main` head: `c3ba58c0e0e6ba64821abe4c9d46c75ff559b2b4`.
- GitHub Pages workflow [42463361038 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42463361038).
- Exact workflow stages: browser regression tests PASS; static build and generated data PASS; Chromium tests against built site PASS; deployment artifact assertions PASS; Pages deploy PASS; deployed HTML/JS/CSS/data smoke checks PASS.
- Live URL https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/ was fetched after the workflow and returned **HTTP 200** with the expected Lao-to-Ukrainian interface title and input/result controls.
- This is a real deployment of the merged `main`, not merely a preview from the PR branch. The site was already configured for Pages; no Pages settings change was needed.

### Updated task ledger

| Task | Current status | Evidence / boundary |
|---|---|---|
| PR #143 integration into main | DONE_VERIFIED | Squash merge `c3ba58c0e0e6ba64821abe4c9d46c75ff559b2b4` |
| GitHub Pages publication | DONE_VERIFIED | Workflow #42463361038 success; deployed-site smoke checks success; live HTTP 200 |
| Automated browser regression on merged source | DONE_VERIFIED | Pages workflow browser tests and built-site Chromium tests passed |
| Live manual adversarial browser interaction after deployment | PARTIAL | Pre-merge live-site stress and negative tests were exercised; post-merge workflow smoke tests passed, but a second interactive post-deploy browser session was unavailable in this run |
| Three-engine 100-word benchmark | DONE_VERIFIED (comparative only) | Latest artifact from run #42416252986; metrics appended to benchmark report |
| Independent adjudicated IPA gold | BLOCKED | 0 records; no project accuracy claim |
| Manual screen-reader / physical-device / actual browser zoom QA | PARTIAL | Still requires human sessions and recording in `docs/accessibility-manual-qa.md` |
| Broad linguistic acceptance | BLOCKED / evidence-limited | Requires qualified Lao phonetics review and independent source adjudication |

### Readiness

**Published engineering-verified research prototype; not production/release-ready and not accuracy-validated.** The publication pipeline is green. Independent IPA gold and manual accessibility remain genuine acceptance blockers.


## 11. Deterministic MekongPhon-reference profile continuation — 2026-11-08

This is the current continuation checkpoint and supersedes the pre-profile implementation/readiness snapshot above.

### Implementation

- Starting main SHA: `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`.
- Working branch: `feat/deterministic-mekongphon-reference-profile-20261108`.
- Draft PR: [#146](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/146).
- Python API and CLI expose an explicit deterministic IPA convention profile. Browser engine implements the same profile API. The default Vientiane rule profile and visible web UI remain unchanged.
- Nine high-frequency vowel-ID mappings and two onset mappings were transferred from aggregate train-split correspondences. No model weights, neural inference, lexical word lookup or automatic neural fallback are involved.
- IPA provenance records each applied override. Typed IPA is still passed to the Ukrainian adapter; unsupported/uncertain target mappings remain fail-closed.

### Evidence-gated comparison

Successful dedicated benchmark: [run 42467190935](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467190935), artifact 13612311669, artifact SHA-256 `5471b2f8d4c1d599fe881811ca8d31c326c0d79b2929b859100ca086af83a329`.

| Engine | Full-set CER | Exact / 100 | Coverage |
|---|---:|---:|---:|
| Default ClippyFirst rules | 11.46% | 69 | 97% |
| Deterministic reference profile | **6.64%** | **90** | 97% |
| MekongPhon Neural | 6.64% | 82 | 100% |

On identical coverage (n=97), reference-profile CER is 1.40% vs neural 5.79%. The profile therefore reaches the neural model's full-set CER and exceeds its exact matches on this reference, but does not reach its coverage. One-run mean CPU latency was 1.38 ms/input for the profile and 58.08 ms/input for the neural model, excluding model load. Runtime errors: 0.

This is a 100-word dictionary-seeded comparison, not independent phonetic accuracy. The default Vientiane rules are unchanged. Remaining warnings are `UNCONSUMED_AFTER_VOWEL` (3) and `MALFORMED_TONE_MARK_ORDER` (1); these are still withheld. Do not tune against the held-out IPA references.

### Verification and branch disposition

- Exact-head Verify [42467409253 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467409253) ran on code checkpoint `aca31b594b06d1b7ab3381171b56ff745fde5985`: 271 Python, 129 Node and 17 Chromium tests passed; IPA corpus structural validation, repository audit, clean `npm ci`, browser tests, build, generated-data drift and built-site checks all passed. Subsequent commits in this continuation only update handoff/audit metadata; runtime and benchmark code are unchanged.
- Dedicated profile benchmark [42467190935 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42467190935) passed with zero runtime errors.
- PR #146 remains draft/open and unmerged.
- PR #145 remains open and untouched; its neural-default direction conflicts with the deterministic-first requirement.
- PRs #137–#142 remain open and untouched; their implementation changes are already integrated into the starting mainline.
- Main remains at `c0d7218da907dbe0bae6cadb42824ca0cd09b83a`; no release, merge, deployment or settings change was performed.

### Artifact hygiene note

An intermediate diagnostic artifact (run 42467038446, artifact 13612136875) included exact orthographic remainder fragments in warning diagnostics. The script was corrected to emit aggregate warning categories only and the workflow retention was reduced to one day. The GitHub connector did not expose artifact deletion, so the original artifact remains until its original expiry; it contains no source rows, IPA references or per-item predictions. Subsequent sanitized artifact 13612311669 contains aggregate metrics and warning categories only.

### Updated task ledger

| Task | Status | Acceptance boundary |
|---|---|---|
| Deterministic reference IPA profile, Python and browser engine | DONE_VERIFIED (engineering) | Python/Node/Chromium regression and provenance tests pass |
| Held-out comparison to MekongPhon Neural | DONE_VERIFIED (comparative only) | Full-set CER parity; 97% vs 100% coverage |
| Three withheld inputs | PARTIAL / EVIDENCE-LIMITED | Source-supported structural rule required; malformed tone order remains withheld |
| Visible UI profile selector | DEFERRED | Not needed for engine-level parity; UI default unchanged |
| Independent adjudicated IPA gold | BLOCKED | 0 records; requires independent annotators/adjudicator |
| Manual accessibility | PARTIAL | Human AT, physical-device and real-zoom QA remains unperformed |
| Linguistic/production release | BLOCKED | Independent gold and qualified specialist review required |

### Readiness

**Published engineering-verified research prototype, not production/release-ready and not independently accuracy-validated.** The opt-in deterministic profile reaches the benchmark neural CER, but remaining coverage and independent linguistic acceptance are unresolved.


## HVULao 1k independent sentence-domain benchmark update — 2026-11-08

The previous audit snapshot predates PR #147's completed benchmark and is superseded for this test by the verified result below.

- Dedicated branch/PR: `benchmark/hvulao-1k-three-engine-20261108`, [draft PR #147](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/147), stacked on draft PR #146. Neither PR is merged; main is unchanged.
- Pinned source: HaHVU/HVULao_NLP revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`, `Datatest1k/testorgin1000.txt`, Git blob SHA-1 `947448807484bb994877ae5d32cba1cfdd5e2d9b`; Mendeley Data v2 DOI 10.17632/5zwym7kwn8.2, CC BY 4.0. Paired labels are segmentation/POS, not IPA.
- Successful Actions run [#42486829108](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42486829108), code SHA `535d55e169ed518eb54113cb1980347e62240539`; aggregate artifact [13620465276](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42486829108/artifacts/13620465276), SHA-256 `b0daf8011612c86d970d5e482d0f4f9a747c59a68fa58c4afb37c039026305a3`.

| Metric | Vientiane rules | MekongPhon-reference rules | MekongPhon Neural |
|---|---:|---:|---:|
| Complete sentences / coverage | 35/1,000 (3.5%) | 35/1,000 (3.5%) | 888/1,000 (88.8%) |
| Rule syllables with IPA | 16,047/20,150 (79.64%) | 16,047/20,150 (79.64%) | — |
| Mean latency | 15.82 ms | 15.43 ms | 405.70 ms |
| p95 latency | 30.25 ms | 30.05 ms | 732.66 ms |
| Unexpected runtime errors | 0 | 0 | 0 |

Neural wrapper input rejections: 56 source strings over 128 code points and 56 strings rejected by Unicode validation. These are expected input-contract rejections, not runtime errors. The validator currently accepts Lao block, whitespace and a narrow ASCII set; do not silently strip typographic/zero-width characters or truncate/split long inputs without a separately justified and tested normalization policy.

Only 35 sentences are complete in all three engines. Pairwise output disagreement on this shared subset: Vientiane vs reference 7.75%; Vientiane vs Neural 13.67%; reference vs Neural 6.47%. This is disagreement, not accuracy. No IPA gold is present in this corpus, so accuracy/CER cannot be measured. Full interpretation, methodology, artifact metadata and task ledger: [HVULao 1k three-engine stress report](../../research/HVULAO-1K-THREE-ENGINE-STRESS-2026-11-08.md).

### Exact-head repository verification

The full Verify workflow was enabled for `benchmark/**` push branches and completed successfully on commit `53f004233760ad1c336e0b1935d37eddccffdd81`: [run #42487885967](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42487885967). Verified checks: IPA gold corpus structure, repository audit, 271 Python tests, external-G2P harness compile/help, clean `npm ci`, 129 Node tests, build/regeneration, generated-data drift, 17 Chromium browser tests, and built-page/asset checks. All passed. This run covers the benchmark report, docs index, source/evidence note, and audit/handoff updates at that commit.

After base synchronization, exact-head Verify on `005a87c4b8f2a519e9934c32f877c3b5e2ae2130` also passed: [run #42488245976](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488245976). It repeated all 271 Python, 129 Node and 17 Chromium tests and the corpus, audit, install, build, generated-data and built-site gates successfully.

### Updated readiness and tasks

| Task | Status | Evidence / blocker |
|---|---|---|
| Independent 1k source pin and integrity check | DONE_VERIFIED | Immutable revision and Git blob SHA-1 validated in successful run #42486829108 |
| Three-engine execution on all rows | DONE_VERIFIED (engineering only) | Successful workflow; zero unexpected runtime errors |
| Coverage/latency/disagreement report | DONE_VERIFIED (comparative only) | Artifact 13620465276; shared disagreement n=35, no gold accuracy |
| Neural wrapper Unicode/length acceptance | TODO / evidence-limited | Requires a defined, source-safe policy and regression suite |
| Deterministic full-sentence coverage | TODO / evidence-limited | Requires primary orthography/phonology evidence for unsupported categories; preserve fail-closed behavior |
| Independent adjudicated IPA gold | BLOCKED | Still 0 records |
| Manual screen-reader/physical-device/real-zoom QA | PARTIAL | Human sessions still not recorded |
| Production linguistic acceptance | BLOCKED | No independent IPA accuracy evidence or qualified specialist sign-off |

**Readiness:** engineering-verified sentence-domain stress test is complete. The project remains a research prototype, not independently accuracy-validated or production/release-ready.

PR #146's base branch advanced by one commit (`ad5bf2a61480ea255a9b83ca6f662471d7606e84`) adding the benchmark workflow. PR #147 was synchronized with merge commit `110a408057bc1143b466304cff6d57c4f074bbe8`; the single overlapping workflow file was resolved by retaining the benchmark-branch version with its push trigger. Compare is now 21 ahead / 0 behind and GitHub reports PR #147 mergeable. Both PRs remain draft/open; main was not changed.


## HVULao latency methodology correction — 2026-11-08

The schema 1.0 report timed all rule-engine rows but only successful neural inferences, so its neural latency excluded 112 rejected inputs. This was a denominator mismatch, not a change in coverage or IPA output. Schema 1.1 now reports all-attempt latency for every engine and successful-inference latency separately.

- Two corrected runs on code SHA `61b21237d57fc519dfff40ee22ed0649df2050e0` both succeeded: push [#42488814477](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488814477), artifact `13620542012`, SHA-256 `cf7df0db5181de3d7a4b70e2cfb96f092510efdd7107a13b238c2e53fac626d8`; pull request [#42488818208](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488818208), artifact `13621285664`, SHA-256 `d5ebe048e328e06b9b107062433a1b3f191f039c77ed56142d88704727fc325a`.
- All-attempt mean / median / p95 ranges: Vientiane `13.50–13.53 / 12.81–12.87 / 26.00–26.17 ms`; reference rules `13.24–13.34 / 12.53–12.72 / 25.72–26.00 ms`; Neural `209.58–262.84 / 202.98–256.59 / 430.65–533.69 ms`.
- Neural successful-only n=888 ranged: `236.00–295.97 / 218.89–276.26 / 435.22–542.77 ms` mean/median/p95. Hosted CPU variability is material.
- Coverage and pairwise results are unchanged: rule coverage 3.5% each, Neural 88.8%; shared complete subset n=35; pairwise disagreement is not accuracy.
- Exact-head Verify [#42488814424 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488814424) on the same commit: 271 Python, 129 Node, 17 Chromium tests and all repository data/audit/install/build/reproducibility gates passed.

The schema 1.0 latency values are superseded. The dataset still has no IPA references; the repository remains a research prototype and not linguistically release-ready.


## Benchmark workflow de-duplication — 2026-11-08

Removed the redundant branch-specific `push` trigger from PR #147's benchmark workflow. Its base branch already supplies the `pull_request` trigger for this target branch, and the manual `workflow_dispatch` remains. Previously, each commit started duplicate 1k neural benchmarks; future PR updates now need only one full run. No model, dataset, inference behavior or results changed.


## Five-source benchmark portfolio audit — 2026-11-08

The current benchmark inventory now identifies five distinct sources: (1) MekongPhon held-out 100-entry orthography–IPA comparison — executed, reference-relative; (2) HVULao_NLP 1k sentence split — executed, stress/coverage only; (3) Wiktionary Lao IPA category (2,317 pages reported) — candidate weak reference, not imported; (4) FLORES-200 Lao devtest (1,012 rows) — gated content/access conditions pending; (5) HPLT Lao monolingual test (2,000 rows) — manual approval pending. The canonical task ledger and acceptance boundaries are in the master handoff section “Five-source Lao benchmark portfolio”.

No candidate dataset was downloaded, copied, or added to runtime/corpus data in this step. No gated access was bypassed. The three not-yet-run candidates are not counted as completed benchmarks. Wiktionary requires a pinned snapshot and dialect separation before use; FLORES/HPLT have no IPA reference and are coverage/runtime stress only. Independent adjudicated IPA gold remains 0.


## Hybrid deterministic engine continuation — 2026-11-08

A dedicated implementation branch `feat/hybrid-deterministic-lao-engine-20261108` was created from the existing benchmark continuation head `f3b8b3b7b919c3a32bd66ea8972f87461a82411e`. The branch preserves PR #146 and PR #147 as unmerged predecessors and does not change main.

### Implementation snapshot

- New `hybrid-deterministic` profile composes the existing Vientiane phonological baseline with the eleven already documented MekongPhon-reference correspondences.
- A deterministic selector orders matches by explicit priority and condition specificity. Declaration order is irrelevant; equal-rank conflicting outputs raise an error.
- Rule application is traced in typed IPA provenance with stable hybrid rule IDs.
- Python API, CLI and browser engine expose the profile. The default Vientiane profile and visible UI remain unchanged.
- Python and browser regression tests cover profile output, provenance, baseline fallback, tone preservation, rule specificity and conflict rejection.
- Both frozen benchmark scripts now include the hybrid engine as a separate comparison path. New artifacts have not yet been generated at this checkpoint.

### Status

| Area | Status | Acceptance |
|---|---|---|
| Selector and profile implementation | PARTIAL | Exact-head hosted Python/Node tests pending |
| Browser parity | PARTIAL | Node, Chromium and build gates pending |
| MekongPhon 100-entry benchmark | PARTIAL | Fresh hybrid artifact and zero runtime errors required |
| HVULao 1k stress benchmark | PARTIAL | Fresh hybrid artifact; compare coverage and all-attempt latency |
| New context-specific IPA values | TODO / evidence-limited | Need train-split context aggregates and independent evaluation; no guessed rules |
| Structural coverage expansion | TODO / evidence-limited | Primary orthographic evidence required for each newly accepted parser rule |
| Independent adjudicated IPA gold | BLOCKED | Still 0 |
| Linguistic production acceptance | BLOCKED | No independent accuracy evidence or qualified specialist sign-off |

The first hybrid version is an architectural and reproducibility improvement, not yet a Neural-level result. Existing reference-profile scores cannot be relabeled as hybrid benchmark results until the new runs complete. No local tests were run because the shell environment could not resolve GitHub; hosted CI is the required verification path.


### Verification and first benchmark evidence

- Exact-head Verify [#42507135952 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507135952) and push Verify [#42507131646 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131646) on `4afd51964532dd1f95b57eaeac36aea852b85228`.
- 276 Python tests, 132 Node tests and 17 Chromium tests passed; corpus/audit/clean-install/build/generated-data/built-site gates passed.
- MekongPhon held-out benchmark [#42507131648 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507131648), artifact 13628190784, SHA-256 `7de8665161308fcaaa422c5c3534e181916c1958f59e88786c3521215d7f8c86d`.
- Hybrid: 90/100 exact, CER 6.64%, coverage 97%, mean 1.41 ms, zero runtime errors. Neural: 82/100 exact, CER 6.64%, coverage 100%, mean 60.51 ms. On common coverage n=97, hybrid 90 exact / CER 1.40%, Neural 81 exact / CER 5.79%.
- This is reference-relative and non-tonal, not independent gold. It confirms parity with MekongPhon-reference on this test, not generalized Neural-level coverage or phonetic accuracy.
- HVULao 1k hybrid stress run [#42507136055](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42507136055) is still in progress at this audit revision; no metrics are claimed until the artifact is available.


## Hybrid engine exact-head verification and coverage checkpoint — 2026-11-08

Final code checkpoint: `c705cf8ad782246c2d72c0d789a5e44e5196eca6`.

- Exact-head Verify [#42508759262 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759262): 280 Python, 134 Node and 17 Chromium tests passed; corpus/data/evidence checks, clean browser install, build, generated-data reproducibility and built-site checks passed.
- Exact-head HVULao stress [#42508759241 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241), artifact 13628229661, SHA-256 `145966638988265a8f255163288e48de4fa8a0293941f0ec26643c7211fe7149`.
- All deterministic profiles completed 669/1,000 mixed-text sentences (66.9%), had 97.85% syllable IPA construction and zero runtime errors. Hybrid all-attempt mean latency was 16.28 ms (p95 30.32 ms).
- Pinned MekongPhon Neural completed 930/1,000 (93.0%), with 70 explicit input rejections; all-attempt mean latency was 375.98 ms (p95 725.19 ms).
- Explicit passthrough now preserves supported ASCII and corpus-observed punctuation unchanged and excludes it from IPA coverage. This is safer input handling, not additional Lao phonological knowledge. The deterministic full-sentence gap remains 26.1 percentage points.
- The prior 100-entry held-out result remains reference-relative: hybrid 90/100 exact, 97% coverage; Neural 82/100 exact, 100% coverage. It was non-tonal and dictionary-seeded, not independent gold.

### Updated task ledger

| Task | Status | Acceptance / evidence |
|---|---|---|
| Hybrid deterministic selector and profile | DONE_VERIFIED | Exact-head Verify #42508759262 |
| Python, CLI and browser parity | DONE_VERIFIED | 280 Python, 134 Node, 17 Chromium tests |
| Explicit punctuation/ASCII passthrough | DONE_VERIFIED | Regression tests and exact-head Verify |
| Hybrid MekongPhon 100-entry comparison | DONE_VERIFIED (reference-relative) | Run #42508691092 on a code checkpoint; 90/100 exact, 97% coverage; no independent gold |
| Hybrid HVULao 1k stress | DONE_VERIFIED (coverage/runtime only) | Exact-head run #42508759241; artifact 13628229661 |
| Reach Neural-level full-sentence coverage | TODO / evidence-limited | Current 66.9% vs 93.0%; parser structures need primary-source support |
| Expand contextual phonology beyond the existing 11 correspondences | TODO / evidence-limited | Requires inspectable context-level support, separate evaluation and independent review |
| Independent adjudicated IPA gold | BLOCKED | 0 independently adjudicated records |
| Linguistic production acceptance | BLOCKED | No independent accuracy benchmark or qualified Lao phonetics sign-off |

No PR was merged, no production default was changed, and PRs #146/#147 remain preserved as stacked predecessors. The hybrid PR #149 remains a draft pending owner review; its base is the existing #147 benchmark branch.


## Source-backed Lao digit handling and parser research — 2026-11-08

- Added Lao native digits U+0ED0–U+0ED9 to the explicit passthrough inventory in Python and browser runtimes. They remain unchanged, receive no IPA and are excluded from IPA adaptation. Python/browser regression tests cover the contract.
- The source is already present in the canonical evidence registry: `SRC-W3C-LAO-LREQ`. Added claims `CLM-LAO-NATIVE-DIGITS` (established script fact) and `CLM-LAO-DIGITS-PASSTHROUGH` (project handling methodology).
- Reviewed the full Ueda 1994 Vientiane phonology article, including p. 112 on restricted non-final CV- light syllables in polysyllabic words. The existing narrow `VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED` candidate remains fail-closed; no broader neutral-tone rule was added.
- Enfield 2007 §3.1 remains corroborating structural evidence for C0V0 minor syllables, with an explicit dialect/corpus-scope caveat. No rural-corpus assumptions were promoted to Vientiane production rules.
- Updated the source/evidence register and research note. Exact-head CI for the latest source-registry/documentation commits is queued/in progress at this audit update; do not mark those final commits verified until the latest run finishes.

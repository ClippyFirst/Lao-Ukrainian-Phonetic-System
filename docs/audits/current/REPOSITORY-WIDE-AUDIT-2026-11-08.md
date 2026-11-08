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

## Neural-first source G2P correction — 2026-11-08

The previously documented architecture described MekongPhon as optional and the deterministic rule engine as default. That is no longer the intended primary CLI/Python contract. The current continuation branch `feat/mekongphon-first-stage` makes the pinned MekongPhon tonal model the CLI default and exposes stage 1 separately through `transcribe_ipa()`; Ukrainian adaptation is explicit via `--to-ukrainian`. The deterministic engine remains available only through `--engine rules`, without fallback.

This change is engineering work in progress until exact-head CI passes. The static GitHub Pages UI remains a separate browser implementation and does not yet call the neural model; a deployed inference backend is still required for neural parity in the public web UI. Independent IPA gold remains empty (0 records), so no new linguistic accuracy claim is made.

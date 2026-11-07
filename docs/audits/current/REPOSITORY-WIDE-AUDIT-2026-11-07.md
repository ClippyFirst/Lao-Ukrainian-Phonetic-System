# Repository-wide audit and documentation checkpoint — 2026-11-07

## Executive assessment

**Engineering state: coherent research prototype with a deployed static web instrument and a typed IPA adapter. Linguistic/release state: not independently validated; not production- or publication-ready.**

The repository has a sound high-level separation between canonical Lao data, source/claim provenance, Python implementation, a separately maintained browser engine, generated browser data, schemas, tests, research scripts and documentation. A broad directory migration would add churn without a demonstrated architectural benefit. The priority is to keep the current boundaries explicit, make current status discoverable, and close evidence and reproducibility gates.

The principal new rights finding is that MekongPhon remains **BLOCKED for dataset reuse/redistribution**: its public upstream repository has no declared license and no root LICENSE in the inspected snapshot. A research/non-commercial permission cannot be inferred. See [the dedicated rights review](MEKONGPHON-DATA-RIGHTS-REVIEW-2026-11-07.md).

## Scope and evidence

Inspected the repository's current default-branch tree and metadata, root README and LICENSE, AGENTS.md, CONTRIBUTING.md, documentation and audit indexes, current repository audit, master handoff, codebase map, product requirements, external corpus triage, linguistic completion register, evidence/source registries, benchmark license registry, JSON schemas, Python package layout, browser runtime, tests/fixtures, build and benchmark scripts, package metadata and GitHub Actions verification workflow.

Also inspected the open PR #137 and its diff/metadata, the PR's exact-head Verify run and benchmark run, and the MekongPhon upstream repository metadata, README and complete tracked tree at the pinned snapshot.

This is a structural, documentation, engineering and rights-evidence audit. It is not a specialist Lao phonology adjudication, legal opinion, manual screen-reader/device audit, or local clean-install test.

## Repository baseline and branch reconciliation

- Repository: **ClippyFirst/Lao-Ukrainian-Phonetic-System**.
- Default branch: **main**.
- Main SHA at inspection: **f40c1128302486b3589da9b16bae198ef3ad1d81**.
- The tree is a compact Python + native browser ES-module project; no Vite/Webpack build is present.
- Open PR #137: [Improve deterministic Lao G2P using MekongPhon benchmark evidence](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/137).
  - Base: main at f40c1128302486b3589da9b16bae198ef3ad1d81.
  - Head branch: benchmark/mekongphon-three-engine.
  - Head: bab117a064f0aee3b685922fe0f0738df7048b12.
  - 78 commits, 20 changed files; PR remains open and unmerged.
  - Exact-head Verify run [42358772788](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358772788): SUCCESS.
  - Benchmark run [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909): SUCCESS; aggregate-only report artifact.
  - Disposition: preserve and review as the existing MekongPhon implementation/benchmark work. Do not duplicate its changes or merge it blindly. Its own report correctly states that dataset rights are unresolved and raw rows/per-item predictions are not committed.
- Branch inventory at inspection: main, benchmark/mekongphon-three-engine and this audit branch; all three report protected=false. PR #137's branch is not this audit branch. No existing branch was deleted or rewritten.
- The previous 2026-11-06 audit's statement that there were no open PRs is historical for its inspected checkpoint; it is superseded by the current PR inventory above.

## Architecture inventory

| Layer | Canonical location | Responsibility / ownership |
|---|---|---|
| Python API and CLI | src/lao_ukrainian/ | Normalization, parsing, phonology, typed IPA result, target adaptation, analysis model and CLI |
| Canonical Lao registries | data/lao/*.csv | Consonants, onset clusters, vowels/structures, codas, tone rules and Ukrainian correspondences |
| Evidence registry | data/evidence/sources.csv, claims.csv | Source metadata and claim-to-source traceability |
| Benchmark and gold contracts | data/benchmark/, schemas/, scripts/ipa_gold_corpus.py | Provenance, licenses, splits, annotation/adjudication, corpus validation and scoring |
| Generated browser data | web/data.js | Generated mirror of canonical registries; never hand-edit |
| Browser runtime | web/ | Native ES-module engine, UI and separate romanization adapter |
| Static pages | index.html, system.html | Converter and methodology/system page |
| Build and research scripts | scripts/ | Audit, generators, static build, external-engine diagnostics and benchmark tooling |
| Tests | tests/, web/engine.test.js | Python, browser, shared-fixture, schema, corpus and UI regression coverage |
| Documentation | docs/, root README.md, AGENTS.md, CONTRIBUTING.md | User/product contract, methodology, implementation map, evidence, audits and handoff |

The intended phonetic path remains:

Lao orthography → structural analysis → source-language phonology → typed IPA → Ukrainian target adaptation → Ukrainian practical orthography.

The optional romanization route is a distinct, lower-information orthographic method. It must not become a fallback for failed IPA and cannot restore tone or phonetic distinctions absent from the romanization.

## Documentation and organization findings

### Existing strengths retained

- Root README describes project scope, non-goals, runtime methods, setup, verification and release limitations.
- docs/README.md is the document landing page and defines document precedence.
- docs/audits/README.md distinguishes current audits, workpacks and historical audit material.
- docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md remains the canonical append-only execution ledger.
- docs/agents/codebase-map.md traces runtime entry points and high-risk seams.
- AGENTS.md and CONTRIBUTING.md enforce test-first changes, provenance, fail-closed behavior, generated-file ownership and exact-head verification.
- docs/final-audit.md is explicitly historical; it should not be silently rewritten as current status.
- Canonical data remains under data/lao/; generated browser data remains under web/data.js.

### Additional documentation defects corrected in this pass

- The limitations page described only explicit-boundary parsing and did not explain the current split contract. It now distinguishes the syllable-oriented Python API from the browser's conservative within-token DP segmentation and explicitly states that neither is a validated lexical word segmenter.
- The decision log reused identifier D-010 for two different decisions. The Ukrainian /ʃt͡ʃ/ → щ decision is now D-011; the earlier vowel/ligature decision retains D-010.
- The validation history contained older test counts and workflow results near its top without a prominent current-status warning. It now directs readers to the canonical handoff and current audit for exact-head status.
- The root README had a standalone leading bullet before its H1. The Romanization → Ukrainian matrix link was moved into the Documentation section; the document now begins with its title.

### Structural decisions

- Do not rename the existing implementation/data/test directories. Current boundaries are documented, referenced by workflows and understandable.
- Do not create a second master plan, task tracker or parallel completion register.
- Keep dated reports under docs/audits/current/; update the audit index when adding a new current checkpoint.
- Keep docs/README.md as the main documentation map.
- Keep the root MIT LICENSE scoped to ClippyFirst's own code and documentation. It does not grant rights to third-party datasets, model weights, dictionaries, fonts or external assets.
- Do not vendor the five user-supplied methodology/design repositories as runtime dependencies. Their relevant practices are already represented in local engineering instructions; the project-specific linguistic and rights constraints take precedence.

## UI/UX and accessibility audit

Reviewed the two static pages, browser UI orchestration, stylesheet, layout tests and the local design-system contract against the web-specific accessibility guidance from UI UX Pro Max.

- Positive: document language and Lao language tags, labelled navigation, skip links, visible 3px focus outline, explicit input label, live/status announcements, pressed-state semantics for the method switch, labelled/keyboard-focusable methodology tables, responsive breakpoints, and reduced-motion handling are present.
- Core text/color pairings were calculated from the current CSS palette: ink on paper 15.99:1; muted on paper 5.14:1; red on paper 5.16:1; blue on paper 12.82:1; white on blue 13.97:1; IPA text on white 8.79:1. These sampled pairings exceed WCAG AA 4.5:1 for normal text; this is not an exhaustive audit of every state or component.
- Found a documented-contract mismatch: compact copy/mini controls were 36–40px high despite the local design system's 44px minimum. Added a regression test (observed RED) and raised .copy, .mini-button/.button and .copy-button to 44px.
- Found that npm test used chained commands and stopped after the first failing suite, hiding later suite results. Changed it to one Node test-runner invocation over all four suites. The resulting run reports all 113 tests, rather than short-circuiting after web/engine.test.js.
- Manual keyboard-only, screen-reader, zoom/text-scaling, real-device touch and deployed-site accessibility checks remain TODO; automated source checks do not substitute for them.

## Rights and research findings

### MekongPhon

- Upstream repository: byu-matrix-lab/MekongPhon, inspected main tree commit f80f6c1840c4818b51e05f2e00cded4701a5b662.
- GitHub repository metadata reports license: null; the root tree has no LICENSE/COPYING file; the README gives a citation but no dataset license.
- The official LREC page states the proceedings are CC BY-NC 4.0 and the abstract says data/code/models are publicly released for future research. It does not state a dataset-specific license for the separately hosted corpus or resolve component-level rights; proceedings licensing is not automatically the dataset license.
- The Lao tonal and non-tonal Hugging Face model cards declare Apache-2.0 for model artifacts; that is not a dataset license.
- The authors explicitly state that all resources are publicly released for future research and quote SEAlang's generic Creative Commons reuse statement. This supports a narrow internal non-commercial research interpretation, but the exact CC version/scope is not identified.
- The existing PR #137 benchmark uses only the 100-entry held-out Lao seed-lexicon split at run time, with aggregate-only output and no retained source rows or per-item predictions. This is treated as a limited research use within the stated purpose; benchmark Verify [42358772788](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358772788) and benchmark [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909) succeeded.
- Redistribution, derivative corpus publication, commercial use, model training/release and the full OPUS-expanded sentence corpus remain BLOCKED pending explicit component-level terms. The 100-word lexicon holdout is not the sentence-level OPUS evaluation set.
- The paper lists NLLB, ParaCrawl and OpenSubtitles as source collections, but the checked-in Lao download script uses NLLB v1 and ParaCrawl-Bonus v9; OpenSubtitles v2024 appears in the Khmer script. Reconcile this paper/code discrepancy and review source terms before full-corpus reuse.
- Methodological status is separate: the paper's 500-entry Lao review involved two authors described as proficient second-language speakers rather than native speakers; 14/500 were judged inaccurate. Sentence-level IPA is lexicon-expanded over NLLB, Paracrawl and OpenSubtitles. MekongPhon remains a secondary diagnostic/comparator, not independently adjudicated project gold. Independent project IPA gold remains zero.

### Other source boundaries

- Common Voice Lao: provider record is CC0-1.0 but has dataset-specific no-speaker-identification and no-rehosting/re-sharing conditions; its limited validated subset and unspecified accent do not establish the Vientiane target profile.
- LDC Babel Lao: substantial Vientiane-region audio/transcript candidate, but access and use require the applicable LDC agreement; transcripts are not IPA gold.
- Goruut and other external G2P outputs remain diagnostic candidates; successful execution or agreement is not accuracy.
- The source registry now has a dedicated SEAlang reuse-notice entry and a refined MekongPhon record. The machine-readable benchmark license registry remains UNKNOWN for the dataset; keep UNKNOWN and RESTRICTED semantics conservative and do not assign a guessed CC identifier.

## Task ledger

| ID | Status | Current evidence | Acceptance / next action |
|---|---|---|---|
| ARCH-001 | DONE_VERIFIED (existing architecture) | Canonical CSV registries, Python package, browser runtime, generated mirror, schemas and tests are separated | Preserve ownership boundaries; changes require regeneration and parity checks |
| DOC-007 | PARTIAL pending exact-head CI | The limitations page did not accurately distinguish Python syllable input from browser phrase segmentation. | Updated the documented runtime contracts; exact-head Verify still required. |
| DOC-008 | PARTIAL pending exact-head CI | The decision log reused D-010 for two distinct decisions. | Renumbered the later Ukrainian target-sequence decision to D-011; repository search found no D-010 cross-references. |
| DOC-011 | PARTIAL pending exact-head CI | MekongPhon rights evidence was described in prose but not separated into its own source-registry entry. | Updated SRC-MEKONGPHON-2026 and added SRC-SEALANG-REUSE-NOTICE; benchmark license remains UNKNOWN pending exact terms. |
| DOC-010 | PARTIAL pending exact-head CI | The root README began with a stray list item before its H1. | Moved the link into the Documentation section; exact-head Verify still required. |
| DOC-009 | PARTIAL pending exact-head CI | The validation history's old test counts could be mistaken for current status. | Added a dated-history warning linking to the current master handoff and audit. |
| DOC-001 | DONE_VERIFIED (prior checkpoint) | Root README, docs index, audit index, contributor guide and codebase map exist; prior exact-head Verify 42299492015 passed for that earlier checkpoint | New audit and rights docs must pass exact-head Verify before this checkpoint is DONE_VERIFIED |
| IPA-ADAPTER-001 | PARTIAL pending exact-main evidence | Typed IPA result and typed-only adapters are present in current main handoff/code; exact main SHA f40c112... is not represented by a directly inspected exact-main Verify run in this audit | Exact-head Verify on the final PR head; linguistic correctness remains separate |
| MEKONG-RIGHTS-001 | PARTIAL / scoped research use only | Paper and SEAlang provide research-release/reuse intent, but no exact dataset license/version; PR #137 performs an ephemeral 100-entry lexicon benchmark with aggregate-only output | Confirm exact CC terms and source-component rights before redistribution, derivatives, training/release or full OPUS-corpus use |
| MEKONG-RESEARCH-001 | DONE_VERIFIED (limited diagnostic) | PR #137 aggregate-only 100-word held-out seed-lexicon benchmark; no rows or per-item predictions retained | Keep this narrow non-commercial research scope; do not promote the reference set to independent project gold |
| MEKONG-BENCH-001 | PARTIAL / existing PR | PR #137 benchmark and implementation are present on an open branch; exact-head Verify and benchmark workflows succeeded | Review and merge decision remain separate; do not call its dataset licensed or its labels gold |
| LAO-GOLD-001 | BLOCKED | data/benchmark/gold.tsv remains header-only; independent adjudicated gold = 0 | Approved target profile/IPA convention, two independent qualified annotators, separate adjudicator, curator, blind intake, rights-cleared 30 lexeme groups and frozen held-out split |
| LAO-PHON-001 | PARTIAL | Tone/rhyme, segmentation, clusters, loanword and dialect-sensitive questions remain | Source-located primary evidence and qualified expert adjudication; unsupported cases stay withheld |
| LAO-TARGET-001 | PARTIAL | Some IPA sequences have no justified Ukrainian target correspondence | Expert-reviewed IPA-to-Ukrainian rationale and regression coverage; no guessed mapping |
| LAO-ROM-001 | PARTIAL | BGN/PCGN and CLDR crosswalk remains provisional and structurally bounded | Full source-located inventory, ambiguity/round-trip tests and explicit non-reversibility |
| LAO-UI-001 | TODO | Automated Chromium coverage exists; source audit found semantic labels/live regions/focus styles and sampled contrast pass, but no human device/screen-reader acceptance matrix | Manual keyboard-only, screen-reader, zoom/text-scaling, mobile and visual QA on the deployed site |
| ENG-CI-001 | PARTIAL / dependency on PR #137 | Exact-head Verify on the audit branch fails only at Browser engine tests: three existing cases fail (modern Lao ຣ analysis-dependent reading; withholding uncertain IPA; withholding incomplete IPA). The same test suite passes on PR #137 head bab117a064f0aee3b685922fe0f0738df7048b12, whose diff includes the relevant browser-engine corrections. | Review and merge the existing PR #137 or independently port its minimal reviewed fixes to main; then rerun Verify on the updated base and this audit PR. Do not copy the whole PR or claim the documentation-only change caused these failures. |
| ENG-TEST-001 | DONE_VERIFIED | Exact-head run 42366859486 executed all four Node suites in one invocation and reported all 113 tests (110 pass, 3 unrelated engine failures); no suite was hidden by shell short-circuit. | Keep this single-invocation behavior. |
| UI-TARGET-001 | DONE_VERIFIED | Regression test passed on exact audit head 87c299fb6d284d3c6a3d25294f87cf03e359b9e7; .copy, .mini-button/.button and .copy-button now have 44px minimum height. | Preserve 44px minimum and regression test. | npm test short-circuited after the first suite; later suites were not executed when engine tests failed. | Changed npm test to run all four Node suites in one invocation; confirm final exact-head output and preserve full failure visibility. |

| ENG-LOCK-001 | TODO | package.json pins Playwright but no npm lockfile is present; CI uses npm install | Generate lockfile in Node/npm-enabled clean checkout, migrate CI to npm ci, prove clean-install reproducibility |
| ENG-BRANCH-001 | BLOCKED / owner action | GitHub branches API currently reports main protected=false; the branch-protection detail endpoint itself returned 403 to this integration | Repository owner enables an appropriate ruleset requiring review and Verify; do not change repository settings without authorization |

## Verification and environment boundary

### Hosted evidence inspected

- PR #137 exact-head Verify [42358772788](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358772788): SUCCESS on bab117a064f0aee3b685922fe0f0738df7048b12.
- PR #137 three-engine benchmark [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909): SUCCESS; aggregate-only report artifact, not a raw corpus export.
- Earlier documentation checkpoint Verify [42299492015](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42299492015): SUCCESS on its recorded earlier SHA; it is not a substitute for verification of this audit branch's final commit.
- Audit PR exact-head Verify [42366859486](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42366859486) on 87c299fb6d284d3c6a3d25294f87cf03e359b9e7: FAILURE at Browser engine tests. Corpus structure validation, repository data/evidence audit, Python tests, optional external-G2P harness syntax/CLI and browser dependency installation passed. All 113 Node tests ran: 110 passed, 3 failed (the existing cases in ENG-CI-001). The new 44px target regression test passed. Build, generated-data reproducibility, Chromium UI and built-page checks were skipped after the browser-test step failed.

### Commands not executed in this session

No local checkout or shell execution was available through the connected GitHub workflow interface. Therefore this audit does **not** claim local execution of:

- python scripts/ipa_gold_corpus.py validate --language lao
- python scripts/audit.py
- PYTHONPATH=src python -m unittest discover -s tests -v
- npm test
- npm run build
- git diff --exit-code -- web/data.js
- npm run test:browser

The above commands remain the exact project Verify workflow contract. The new documentation branch must receive a fresh PR-head Verify run before its documentation tasks are marked DONE_VERIFIED.

## Readiness judgement

**Research-ready as an engineering/evidence-management prototype; not linguistically release-ready.**

The project has a coherent and tested engineering architecture, but the following independently prevent a production/publication-grade linguistic claim: zero independent expert-adjudicated IPA gold, unresolved profile/phonological/target-adaptation decisions, incomplete manual UI/accessibility QA, dependency lockfile reproducibility work, and unresolved rights for external datasets. MekongPhon is suitable for the narrow, non-commercial, aggregate-only seed-lexicon research diagnostic already implemented; its full corpus, derivatives and redistribution are not cleared.

## MekongPhon source-license re-check — 2026-11-07

The upstream license investigation was refined from a repository-level check to the actual data-construction paths. The upstream MekongPhon repository has no root LICENSE/COPYING and GitHub metadata has no recognized license. Its pipeline README and scraper show SEAlang-derived lexicon extraction; the Lao scraper selects Kerr 1972 entries. SHACHI metadata explicitly reports source material copyright 1995 Dunwoody Press and 1972 Catholic University Press. The generic SEAlang “Creative Commons open license” wording does not identify a version, scope or covered rights-holder and cannot be treated as blanket permission for bulk extraction or redistribution.

The exact MekongPhon downloader scripts show Lao uses OPUS-NLLB v1 and OPUS-ParaCrawl-Bonus v9; Khmer adds OPUS-OpenSubtitles v2024. These component sources require their own version-specific terms. The separate OpenSubtitles2024 Hugging Face held-out benchmark declares ODC-BY and says it is for evaluation/development rather than training, but that card is not the same artifact as MekongPhon's OPUS mono download and its license must not be transferred to it. OPUS's platform-level ParaCrawl redistribution statement is not a substitute for exact file-level terms.

Disposition: full corpus, scraped lexicons, upstream code, derivative corpus, retention, retraining, redistribution and commercial use remain UNKNOWN/BLOCKED pending exact component terms or written permission. The earlier 100-entry ephemeral aggregate-only research diagnostic remains narrowly scoped and is not legal clearance. The pretrained Lao tonal/non-tonal model artifacts are separate: their model cards declare Apache-2.0, and the existing optional runtime adapter uses only those artifacts without copying source data or upstream code. This adapter is the current feasible implementation path; it does not turn the deterministic rule engine into a neural model or authorize importing training examples into deterministic rules.

Evidence locators are recorded in `data/evidence/sources.csv` and the dedicated rights review.

## Rule-engine branch reconciliation — 2026-11-07

The deterministic rule-engine improvements are already implemented on open PR #137 (`benchmark/mekongphon-three-engine`): DP syllabification of unspaced Lao, per-syllable tone-mark validation, local short-vowel/coda checks, unsupported-material preservation, typed IPA output and source-scoped Vientiane tone contour handling. The PR includes dedicated regression tests and a reproducible three-engine benchmark. It was inspected against main (78 commits ahead, 0 behind; 20 changed files).

No duplicate syllabifier was retained in PR #138. That branch remains scoped to the optional neural provider and rights audit. PR #137's current head `bab117a064f0aee3b685922fe0f0738df7048b12` is **DONE_VERIFIED for engineering checks**: exact-head Verify [42358772788](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358772788) passed all stages, including browser engine, build, generated-data reproducibility, Chromium UI and built-page checks. Earlier three browser failures were on superseded heads. The benchmark remains evidence for one frozen reference split only, not independent project gold or universal accuracy. Independent adjudicated IPA gold remains 0.

## Stacked PR verification contract — 2026-11-07

- PR #138 is now intentionally stacked on PR #137's branch `benchmark/mekongphon-three-engine`, so the neural adapter is reviewed against the deterministic engine implementation rather than against the older mainline parser/browser engine.
- Updated `.github/workflows/verify.yml` so `pull_request` events targeting either `main` or `benchmark/mekongphon-three-engine` run the full Verify workflow. Push-triggered Verify on the standalone PR #138 branch still reflects its own files only; its historical three browser failures are expected until the PR merge ref includes PR #137's code.
- Acceptance for the stacked PR is the merge-ref Verify result on PR #138, not the head-only push run. PR #137's current exact-head Verify is already green (42358772788).

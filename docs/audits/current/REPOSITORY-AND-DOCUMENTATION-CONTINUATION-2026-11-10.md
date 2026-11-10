## Ukrainian editorial and interface-quality pass — PARTIAL, 2026-11-10

**Branch:** `quality/ukrainian-editorial-audit-2026-11-10`  
**Base main:** `3dd77a4ea080ce700cb0a131114470ad43de0b94`  
**Scope:** apply selected guidance from Vercel Web Interface Guidelines, blader/humanizer, Anthropic frontend-design and obra/superpowers to the existing Woven Editorial site. No runtime dependency or copied skill tree is added.

### Changes made

- Added [the Ukrainian editorial standard](../../UKRAINIAN-EDITORIAL-STYLE.md): Ukrainian-first interface language, when English identifiers remain, localized language tags, natural copy, contextual review of AI-writing patterns, evidence preservation and design restraint.
- Replaced the English-facing `Lao → Українська` brand wording with `Лаоська → Українська` on both public pages.
- Corrected the romanization output language from `lang="en"` to `lang="lo-Latn"`; kept IPA as `und-fonipa` and Lao input as `lo`.
- Replaced user-facing `IPA gold corpus`, `PROVISIONAL`, unexplained craft terms and English link labels with Ukrainian explanations while retaining exact model, standard, font and source identifiers.
- Re-read the complete public copy and rewrote staged contrasts, abstract closers, repeated explanations and marketing-like claims into direct Ukrainian. Preserved all figures, benchmark caveats, dialect scope, IPA uncertainty and source references.
- Changed all-caps UI and methodology labels to sentence case; removed forced uppercase from analysis captions.
- Added explicit `name` and `autocomplete="off"` to the local Lao text field, plus intentional tap feedback and `touch-action: manipulation`.
- Added static regression assertions for Ukrainian branding, language metadata, sentence-case labels, English leakage, technical-term explanations and touch behavior.
- Preserved all input/output element IDs, the 14 methodology anchors, all 3 tables, the Woven Editorial concept, the IPA-first product contract and the engine implementation.

### Methodology applied

- **Vercel Web Interface Guidelines:** checked semantics, labels, language metadata, focus, reduced motion, touch targets, typography, input behavior, responsive overflow and state feedback. Fixed the concrete language-tag, input-metadata, uppercase-label and touch-feedback issues identified in the current code.
- **Humanizer:** applied its structural review (staged contrasts, repeated closers, forced triads, inflated language, decorative formatting and chat residue) as editorial prompts, not as a mechanical denylist. Kept real technical distinctions and all evidence-bearing claims.
- **Anthropic frontend-design:** retained a subject-specific visual identity, one restrained woven motif, purposeful typography and motion, and rejected generic SaaS-card/gradient decoration.
- **Superpowers:** scoped changes to existing seams, added acceptance tests before implementation, and will use exact-head CI for full verification.

### Task ledger

| Item | Status | Acceptance evidence |
|---|---|---|
| Ukrainian editorial standard and source mapping | DONE_IMPLEMENTED | `docs/UKRAINIAN-EDITORIAL-STYLE.md`; docs index and AGENTS reference |
| Public language and terminology cleanup | DONE_IMPLEMENTED | `index.html`, `system.html`, `web/app.js` |
| UI language metadata and input semantics | DONE_IMPLEMENTED | `lang="lo-Latn"`, named textarea, autocomplete policy |
| Sentence-case and touch presentation | DONE_IMPLEMENTED | `web/styles.css`, static tests |
| Regression coverage | DONE_VERIFIED | Static/editorial and browser assertions pass on exact PR head; Verify run #42883137574 |
| Vercel guideline review | PARTIAL | Code-level findings fixed; 350 Python, 160 browser-engine and 22 Chromium tests pass. Physical-device and manual screenshot review remain pending |
| Manual screenshot, physical-device and dedicated assistive-technology review | BLOCKED | CI covers Chromium viewports, focus, roles, touch and reduced motion; no physical-device or independent screen-reader session available |
| Linguistic accuracy | UNCHANGED / EVIDENCE-LIMITED | No phonological code or corpus changed; independent adjudicated IPA gold remains 0 |

**Verification:** local shell access cannot resolve `github.com`, so cloning and local test execution were unavailable. Latest exact-head GitHub Actions Verify run [#42883622543](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42883622543) passed on commit `836878509bbe9b2a8806b112cfa2e0e5c51460cd`: 350 Python tests, 160 browser-engine tests and 22 Chromium UI tests; data/evidence audit, independent IPA gold schema validation, optional external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks also passed. Earlier failures were stale copy assertions; those expectations were corrected before the green run. No Pages deployment was triggered because the PR remains unmerged. The independent expert-adjudicated IPA gold set remains empty (0), so linguistic accuracy is still evidence-limited.

**CI evidence so far:** first PR Verify run [#42881436157](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42881436157) passed Python, engine and build steps but failed 4 of 22 Chromium assertions because browser tests still expected the previous all-caps statuses and the English `PROVISIONAL` token. Updated those assertions in `tests/browser/site.spec.js`. Run [#42882782069](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42882782069) then passed 159/160 browser-engine tests; the sole failure was another stale copy assertion for the previous romanization explanation. Updated that assertion to the new Ukrainian wording. Rerun [#42882961437](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42882961437) failed one remaining stale assertion for the explicit 10 November 2026 status date; restored the date in the simplified paragraph. A new exact-head run is required.

## Complete public website copy rewrite — 2026-11-10

**PR:** [#168 — merged](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/168)  
**Branch:** `docs/site-copy-rewrite-lao-editorial-20261110`  
**Base main:** `ee4dee5f6c6e8abfdb47069fca3894617648684d`  
**Implementation scope:** `index.html`, `system.html`, `web/app.js`, browser/static content tests, README and canonical handoff/audit.  
**Plan:** [2026-11-10 Lao site content rewrite](../../superpowers/plans/2026-11-10-lao-site-content-rewrite.md) (relative link in audit is `../../superpowers/plans/2026-11-10-lao-site-content-rewrite.md`).

### What changed

- Rewrote the service page's Ukrainian copy, labels, action names, metadata, helper text, empty state, output descriptions and research-status explanation. Rewrote runtime-generated trace labels, copy feedback, error/empty states, romanization explanation and low-confidence notes in `web/app.js`. The primary heading and all JS-facing IDs remain stable; the service remains action-first.
- Rewrote all 13 existing methodology sections in plain, evidence-aware Ukrainian and added section 14, which explains why the visual identity is called **Woven Editorial**.
- The design explanation distinguishes the abstract rhythm/structure of weaving from any single Lao community or textile motif; explains paper/silk, Mekong green, indigo, lac-red, and the roles of Noto Sans Lao, Manrope and IBM Plex Mono; and links the design system and source research.
- Updated the visible research date to 10 November 2026 and clarified that schema-8 benchmark concordance is dictionary-seeded, not independent phonetic accuracy. The independent expert-adjudicated IPA gold corpus remains 0.
- Rephrased the fallback contract: known provisional fragments pass through the ordinary IPA → Ukrainian adapter, unresolved positions remain `?`, low confidence stays visible, and tone is not guessed.
- Updated accessible names in browser tests and static content checks for the new labels, date, section count and design rationale.
- Refreshed the service app script cache key. No engine code, linguistic rule, benchmark data, source registry, model, dependency or inference runtime changed.

### Skill and source review

Searched GitHub for suitable skill references and read the relevant guides from Anthropic frontend-design, UI UX Pro Max, Impeccable, Emil Kowalski design engineering and taste-skill. Applied subject-grounded copy, clear user vocabulary, accessibility-first controls, restrained motion and non-template visual voice. Process guidance reviewed: Superpowers brainstorming, writing-plans, TDD, executing-plans and verification-before-completion; Product Design get-context.

The page copy links to W3C Lao Script Resources, Ueda's Vientiane phonology study, Global InCH's account of Lao textile technique variation, CLDR/BGN-PCGN documentation and repository research. These sources support the descriptions; the design does not claim that all Lao textiles share one visual grammar.

### Verification ledger

| Item | Status | Evidence |
|---|---|---|
| Complete service-page copy rewrite | DONE_VERIFIED | `index.html`; all existing UI IDs retained |
| Complete methodology rewrite and concept section | DONE_VERIFIED | `system.html`; sections `s1`–`s14`; 3 tables retained |
| Browser accessibility labels | DONE_VERIFIED | `tests/browser/site.spec.js` |
| Static copy/design contract tests | DONE_VERIFIED | `tests/web-layout.test.mjs` |
| README and plan/handoff documentation | DONE_IMPLEMENTED | README and plan created; handoff/audit update in this branch |
| Linguistic accuracy | UNCHANGED / EVIDENCE_LIMITED | No new gold labels or accuracy claims; independent IPA gold remains 0 |
| Live visual/device review | PARTIAL | Automated browser tests cannot replace physical-device and screen-reader review |

**Merged main:** `a052b5b97fe2518497cddda8a45c76d80cb864a0`. **Exact-PR-head Verify:** [#42875206898 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875206898). **Exact-main Verify:** [#42875399018 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399018), with 350 Python, 155 Node and 22 Chromium tests. **Pages deployment:** [#42875399023 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42875399023); build, 155 Node, 22 Chromium, deterministic-only artifact checks, deployment and live smoke test of both pages plus app/CSS succeeded. **Live:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/. Manual physical-device/screen-reader QA remains partial; independent IPA gold remains 0.

# Current repository and documentation continuation — 2026-11-10

## Website visual redesign — DONE_VERIFIED, 2026-11-10

**PR:** [#163 — Lao woven editorial website redesign](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/163), squash-merged.  
**Starting main:** `2a7c8fe95394bfd587f2ff24086eac1a16ddd4eb`  
**Merge/final implementation SHA:** `9254bd4ecf014a6a5634ac05cebf0d227077977d`  
**Exact-main Verify:** [#42847422102 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422102)  
**Pages deployment:** [#42847422106 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42847422106)  
**Live service:** https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/

The service and methodology pages now share the Woven Editorial visual system. The home page is an operative language workbench with a compact editorial hero; the methodology is a 13-section reading experience with a responsive contents rail. The shared CSS introduces paper/silk, Mekong green, indigo and restrained lac red, with Manrope, Noto Sans Lao and IBM Plex Mono roles. The signature woven band abstracts repeated crossings and rhythm from textile construction; it does not reproduce the Naga as generic UI decoration.

The service page retains all JavaScript-facing IDs, the default deterministic IPA-first route, the separate syllabic romanization method, the Ukrainian-first result hierarchy, and collapsed syllable analysis. The methodology page retains all 13 sections and 3 tables. No engine, linguistic rule, source data, model, runtime dependency or generated browser data was changed.

**Verification evidence**
- Exact-main Verify #42847422102: **344 Python, 152 Node, 22 Chromium tests passed**; repository data/evidence audit, independent IPA-gold schema validation, optional external-G2P syntax/CLI checks, build, generated-data reproducibility, and built-page/relative-asset checks passed.
- Pages run #42847422106: build passed; **152 Node and 22 Chromium tests passed**; deterministic-only artifact checks, artifact upload, Pages deployment, and live same-origin smoke test of both HTML pages and browser assets passed.
- Responsive browser coverage: service widths 320/390/640/768/1024/1440px; methodology widths 320/390/768/1024/1440px; 200% text zoom, keyboard flow, touch controls, reduced motion, and 44px touch targets.

**Remaining limitation — PARTIAL manual visual QA:** no human visual review on physical devices or dedicated screen-reader hardware was performed. Automated browser checks prove the tested layout and interaction contracts, not subjective visual polish or assistive-technology compatibility.

**Superdesign note — BLOCKED:** the local `npx --yes @superdesign/cli@latest` preflight timed out because the shell could not resolve public npm/GitHub hosts. The user explicitly declined switching to Work mode, so no Work mode was used and no Superdesign canvas draft is claimed. The repository implementation proceeded with the supplied taste-skill, frontend-design, Impeccable, Emil Kowalski design-engineering guidance, and the applicable Superpowers/Product Design workflow guidance.

## Outcome

The requested provisional fallback is implemented and deployed. The browser aggregate-output defect was fixed: the final visible string is assembled from transformed per-word syllables, not the original pre-fallback objects. For regression input `ກາລ`, the primary hybrid returns `кал?`. Browser details and the text CLI identify the result as low confidence; unresolved positions remain marked with `?`; tone is not inferred.

The architecture remains:

```text
Lao source orthography
  → Unicode normalization and structural analysis
  → source-language phonology
  → typed IPA / explicitly PROVISIONAL typed result
  → ordinary Ukrainian IPA adapter
  → Ukrainian practical orthography
```

No direct Lao-grapheme → Ukrainian-character shortcut was introduced. The fallback is a rendering guarantee, not a pronunciation guarantee. Provisional IPA is excluded from accepted IPA coverage and accuracy.

## Exact implementation and verification

- PR #159 was squash-merged to `main` as `68aa563ebc13da7e49da533e46301d43c13b5810`.
- Verify [#42796863636](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796863636) passed on the final PR branch head: 337 Python tests, 155 Node tests and 19 Chromium UI tests; corpus structure, repository data/evidence audit, external-G2P syntax/CLI, locked browser dependencies, build, generated-data reproducibility and built-page/relative-asset checks all passed.
- Mainline Pages workflow [#42797184810](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42797184810) passed: build job success, 155 Node tests, 20 Chromium tests against the built site, artifact validation/upload and deployment.
- Deployment job completed successfully. The live same-origin smoke-test fetched both HTML pages, app/data/CSS, Hybrid v2 JS bundle, WASM loader/binary, ONNX encoder/decoder, both tokenizer JSON files, model manifest, model LICENSE/NOTICE and third-party notices. It checked the pinned model ID/revision and Apache license notices.
- Live site: [https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/](https://clippyfirst.github.io/Lao-Ukrainian-Phonetic-System/).

The earlier Pages `syncing_files` delay is historical; it is not the final deployment status. The final mainline deployment and live smoke-test passed. The subsequent documentation-only checkpoint `ee6ced771fd5be553443741fb6007681bd4d2f31` also passed exact-head Verify #42809109496: 337 Python, 155 Node and 19 Chromium tests, plus the repository audit, corpus validation, build, generated-data reproducibility and built-site checks.

## Task ledger

| Work item | Status | Evidence / acceptance |
|---|---|---|
| Python typed provisional fallback through the ordinary Ukrainian adapter | DONE_VERIFIED | Existing typed `PROVISIONAL` result and adapter; Python regressions; exact-head Verify #42796863636 |
| Browser typed provisional fallback and aggregate output | DONE_VERIFIED | `web/engine.js` assembles output from transformed word groups; Node and Chromium regressions assert `кал?` |
| Low-confidence browser details and CLI disclosure | DONE_VERIFIED | Explicit low-confidence label, unresolved `?` explanation and no-tone-inference note |
| Documentation of fallback contract | DONE_VERIFIED | Fallback guide, README, docs index, handoff and completion register reconciled |
| GitHub Pages publication of current main | DONE_VERIFIED | Workflow #42797184810 and successful live same-origin smoke-test |
| Independent expert-adjudicated Lao IPA gold | BLOCKED / evidence-limited | Gold corpus remains 0; requires qualified independent annotators, adjudication, frozen profile/convention, source locators and rights-cleared examples |
| Manual accessibility and device QA | PARTIAL | CI is not screen-reader, keyboard-only, physical mobile or manual visual certification; follow `docs/accessibility-manual-qa.md` |
| Non-core Pali/Sanskrit and Khmu pronunciation | DEFERRED | Outside modern-Lao core scope; retain unknown markers unless separately scoped and evidenced |
| PR #145 neural-first architecture | DEFERRED / owner decision | Open and untouched; conflicts with adopted hybrid-deterministic production default |
| Branch protection / required checks | BLOCKED / owner decision | GitHub reports `main` unprotected; settings were not changed |

## Repository structure review

The five user-supplied repositories were inspected for root structure and README navigation:

- [unlazy](https://github.com/Leonxlnx/unlazy): concise install/quick-start/gate-contract documentation; distinct `agents/`, `references/`, `research/`, `scripts/`, `templates/` and `tests/`.
- [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): separates source, CLI, docs, examples/gallery, stack data and plugin metadata; provides localized READMEs.
- [superpowers](https://github.com/obra/superpowers): separates reusable skills from hooks/tests and host-specific integration directories.
- [mattpocock/skills](https://github.com/mattpocock/skills): clear `AGENTS.md`, glossary, scope, docs and skills boundaries.
- [ponytail](https://github.com/DietrichGebert/ponytail): broad host-adapter/plugin manifests alongside skills, commands, hooks, tests, benchmarks and examples.

Adopt the transferable documentation principles, not their product-specific plugin scaffolding. This repository is a language engine and research system, not a generic agent-skill package; copying plugin manifests/adapters would add maintenance cost without user value. The new [repository structure and documentation contract](../../REPOSITORY-STRUCTURE.md) defines canonical placement and precedence rules.

## PRs, branches and governance

- PR #159 merged successfully; its implementation branch was `fix/provisional-grapheme-output-docs-20261110`.
- PR #145 remains open and unmerged; no neural-first architecture change was imported.
- No existing user branch was force-pushed or deleted.
- Branch metadata reports `main` as unprotected. No branch protection or repository setting was changed; owner authorization is required.

## Readiness

**Deployed engineering-verified research prototype; not linguistically release-ready.** The browser fallback and Pages deployment are verified. Independent adjudicated IPA gold remains 0, so no independent phonetic accuracy claim is justified. Manual accessibility QA remains partial.

## Next genuine work

1. Commission a rights-cleared, dialect-scoped IPA annotation pilot with at least two qualified independent annotators and a separate adjudicator; freeze the IPA convention and intake protocol before labels are collected.
2. Resolve source-located disagreements and add only adjudicated records to the independent gold split.
3. Complete manual keyboard, screen-reader, zoom, contrast and physical-device QA on the deployed site.
4. Decide whether to configure required branch checks/protection; this is an owner-level repository governance decision.
5. Keep PR #145 deferred unless the owner explicitly reopens the production-architecture decision.

No IPA labels, phonological correspondences, source permissions, benchmark scores or accuracy values were fabricated in this continuation.


---

## Long-form provisional IPA fallback correction — 2026-11-10

The owner supplied `ພຣະຣາຊອານາຈັກຣ໌ລາວ` and reported that the IPA field showed only `?` while the Ukrainian output ended in a long repeated question-mark sequence.

Root cause: the main IPA summary ignored `graphemePreview.ipaPreview`; the fallback also emitted one unknown marker per unresolved grapheme. Code changes in `main` now display the provisional IPA hint when the full parser has no accepted IPA, and cap the unresolved positions within each fallback unit at three markers in both Python and browser fallback builders. The confidence status remains provisional; no tone is inferred.

| Task | Status | Acceptance / evidence |
|---|---|---|
| Main IPA summary uses provisional preview before unknown placeholder | PARTIAL | `web/app.js`; exact-head browser UI test pending |
| Unknown-marker run capped at 3 in Python and browser | PARTIAL | `phonetic_result.py`, `web/engine.js`; focused Python/Node tests pending exact-head CI |
| Exact user phrase regression across runtimes and UI | PARTIAL | Added to Python, Node and Chromium suites; exact-head run pending |
| Fallback contract documentation | DONE_VERIFIED | `docs/lao-grapheme-ipa-preview.md` updated with IPA display priority and uncertainty grouping |
| Exact expert IPA for supplied phrase | BLOCKED | No independently adjudicated, source-located IPA evidence; do not replace with a guessed reading |

Do not close this item until exact-head Verify and Pages deployment workflows complete successfully. The prior deployed artifact remains the production reference until the new Pages run is successful.


### Exact-head verification update — 2026-11-10

**Implementation head:** `85c0581726c4de659bfe002b61b2bdfdaecfe024` (`main`). **Verify [#42830796088 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42830796088).**

- Python: 338 passed.
- Node: 156 passed.
- Chromium: 20 passed, including the exact supplied phrase regression and primary IPA-field provisional-hint disclosure.
- IPA-gold structure validation, repository data/evidence audit, optional external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks: passed.

| Task | Status | Evidence |
|---|---|---|
| Show provisional IPA in the main IPA summary | DONE_VERIFIED | `web/app.js`; exact-head Chromium test in Verify #42830796088 |
| Bound long unresolved runs to at most three markers | DONE_VERIFIED | Python and browser fallback implementations; 338 Python + 156 Node tests |
| Long user phrase regression | DONE_VERIFIED | Python, Node and Chromium tests passed in Verify #42830796088 |
| Canonical fallback guide, master handoff and changelog | DONE_VERIFIED | Updated in place; no duplicate plan created |
| Publish Hybrid v2 fallback fix to GitHub Pages | DONE_VERIFIED | Pages workflow [#42830796208 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42830796208); deployed application SHA `85c0581726c4de659bfe002b61b2bdfdaecfe024`; artifact `13771951564`; live same-origin smoke passed |
| Independent expert IPA for the phrase | BLOCKED / evidence-limited | Exact phrase not found in the two bundled orthographic lexical-hint lists; those lists are not IPA resources. No expert-adjudicated source-located IPA is available. |

The engineering behavior is verified. Linguistic accuracy of the phrase remains unverified and no IPA string has been invented or labelled as gold.


### Pages deployment completion — 2026-11-10

Pages workflow [#42830796208 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42830796208) deployed application SHA `85c0581726c4de659bfe002b61b2bdfdaecfe024`. Artifact `13771951564` (`github-pages`, 40,375,698 bytes) was uploaded and deployed. The live smoke-test successfully fetched both pages, app/data/CSS, Hybrid v2 inference bundle, WASM runtime, model manifest, ONNX encoder/decoder, both tokenizer files and license/notice assets; model ID and immutable revision checks passed. The deployed browser interaction test passed.

The final README/audit/handoff edits after that deployment are documentation-only; no application asset changed after the deployed application SHA. The independent expert IPA blocker remains open.

## User-requested removal of neural inference from the public service — 2026-11-10

**Decision:** the public web service must not expose or download the Hybrid v2 neural tonal model. Keep the deterministic IPA-first output and romanization alternative. Retain Python neural engines only as research/CLI/benchmark tooling.

### Cleanup performed on main

- Removed neural result card and its 40 MB model / 15 MB WASM first-run notice from index.html.
- Removed lazy browser ONNX inference code, DOM bindings, run/copy handlers and unused styles from web/app.js and web/styles.css.
- Replaced model-bundling scripts/build_web.py with a static copy-only build.
- Replaced Pages workflow's ONNX export, model/tokenizer/WASM staging, large runtime asset smoke checks with static-only build, Chromium test, negative model-asset assertions, Pages upload/deploy and same-origin smoke test. Pages artifact is now capped at 20 MB.
- Removed browser-only inference modules/tests, model export/runtime/Pages staging scripts, model-specific workflow(s), preview workflow and unused ONNX runtime license asset.
- Updated README and changelog; archived the old browser-port report as historical context. Python hybrid_v2.py, MekongPhon adapters, CLI and benchmark workflows remain.

### Branch and PR inventory

28 branches compared to current main; 3 open PRs reviewed. #145 (neural-first default) conflicts with the deterministic public contract and is not merged. #160 (benchmark reconciliation) and #162 (Python-only Meta-Hybrid v3 comparison harness) are research-only candidates requiring exact-head validation and conflict review; neither belongs in the browser bundle. Older diverged branches are snapshots or historical implementations; do not merge wholesale. Preserve branch refs/history while recording whether each branch is already represented, superseded, or has a unique research artifact to port.

### Current acceptance state

| Work | Status | Evidence / next acceptance |
|---|---|---|
| HTML/JS/CSS neural panel removal | DONE_VERIFIED (code edit) | index.html, web/app.js, web/styles.css; Chromium negative assertion added; wait for Verify |
| Static-only Pages build and workflow | DONE_VERIFIED (code edit) | scripts/build_web.py, .github/workflows/pages.yml; verify built artifact excludes model/WASM |
| Browser-only model implementation removal | DONE_VERIFIED (code edit) | deleted web model modules and dedicated test |
| Browser ONNX export/runtime staging removal | DONE_VERIFIED (code edit) | deleted three browser-only scripts, export/preview workflows and unused license file |
| Preserve Python research models | DONE_VERIFIED (scope) | Python implementation and benchmark tooling intentionally untouched |
| Verify tests/build/Pages deployment | TODO | exact-head CI and live Pages smoke-test must pass |
| Integrate compatible branch-only research | PARTIAL | inspect PR #160/#162 exact heads and test after base reconciliation |
| Independent expert IPA gold | BLOCKED | 0 adjudicated records; expert annotation and rights-cleared sources required |

Do not label this cleanup deployed until the Pages workflow and live same-origin smoke test succeed. The last previously deployed artifact is still the prior version until then.
## Branch consolidation — 2026-11-10

### Ported and verified research work

- PR #162 branch code was ported selectively to main: `meta_hybrid_v3.py`, its unit tests, CLI option and public API exports. The exact branch head passed Verify [#42822261651 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42822261651) and external benchmark [#42822253479 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42822253479). Meta-Hybrid v3 remains Python/CLI research-only; it never votes and never changes deterministic Ukrainian output.
- PR #160's external benchmark workflow branch-trigger support was ported to main. Its benchmark reconciliation is now documented in the research inventory and README; its old workflow verification edits were not copied over the new static-only Pages/Verify gates.
- The unique Laonetics branch-only benchmark was ported: aggregate-only script, isolated workflow and report. Final run [#42828308429 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42828308429), artifact [13768874616](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42828308429/artifacts/13768874616): 47/100 exact, 13.95% CER, 100/100 output coverage. Upstream declares CC-BY-NC-4.0; no code/weights enter the product and production promotion is DEFERRED.

### Branch disposition

| Branch / PR | Disposition | Reason / evidence |
|---|---|---|
| `benchmark/current-main-comparative-20261110` / #160 | PARTIALLY PORTED; PR ready to close as superseded | External workflow branch triggers and comparative evidence are now in main; do not copy stale verify workflow over static-only gates |
| `benchmark/meta-hybrid-v3-multiengine-r2-20261110` / #162 | CODE PORTED; PR ready to close as superseded | New comparator module, CLI/API and tests integrated; branch exact-head Verify and external benchmark passed; current main Verify pending |
| `benchmark/laonetics-same-set-20261110` | PORTED | Script/workflow/report integrated; final run and artifact cited above; research-only due NC license and weaker result |
| `feat/mekongphon-first-stage` / #145 | BLOCKED / not merged | Would change the deterministic default to neural-first; keep separate until production architecture is explicitly reconsidered |
| 12 branches with merged PRs | ALREADY IN MAIN | Their merge commits and later mainline tests establish integration; retained branch refs are historical provenance |
| 11 closed-unmerged historical branches | SUPERSEDED / evidence review | Old snapshots of features now present in main or research alternatives superseded by later work; no wholesale merge into current code |
| `feature/meta-hybrid-v3-multiengine-20261110` | SUPERSEDED | Older duplicate branch is behind main; r2 branch work is ported |

Branch refs are retained to preserve provenance; no force-push or branch deletion was performed. The user request to consolidate work is handled by porting unique, verified changes and marking superseded/conflicting snapshots, not by merging stale histories blindly.
## Final cleanup verification and publication — 2026-11-10

- Main application cleanup commit deployed: `3b0692b86fdab188e80207a30c76cbcba80aa4e7`.
- Pages [#42839499385 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42839499385): deterministic-only build, 148 Node tests, 21 Chromium tests, artifact checks, upload, deployment and live same-origin smoke all passed. GitHub Pages artifact `13774124879` is 48,002 bytes; previous model deployment artifact was 40,375,698 bytes.
- Exact mainline Verify [#42840912136 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42840912136) on source head `e14aaf264343d99fa39c09ec93c454a7e9d9603d`: 344 Python tests, 148 Node tests and 21 Chromium tests passed; independent IPA-gold schema validation, repository data/evidence audit, optional external-G2P syntax/CLI, static build, generated-data reproducibility and built-page checks passed.
- PR #160 and #162 were closed as superseded after their compatible benchmark workflow, Meta-Hybrid v3 Python module/tests/CLI/API and research documentation were ported to main. PR #145 remains open with an explicit note because it proposes a neural-first CLI default, which conflicts with the current deterministic-default architecture.
- The Laonetics research branch was consolidated into main as an aggregate-only script, isolated workflow and report. Run #42828308429 SUCCESS; 47/100 exact, 13.95% CER, 100/100 coverage. Its CC-BY-NC-4.0 license excludes product promotion.
- All 28 branch refs were inventoried. Already merged branches remain represented in main; unique verified work was ported; superseded snapshots were not merged wholesale. Branch refs were preserved; no force-push or branch deletion.

**Readiness:** public static service cleanup is engineering-verified and deployed. The repository remains a research prototype rather than a linguistically validated release because independent adjudicated Lao IPA gold remains 0; manual assistive-technology/device QA also remains outside these automated checks.

### Branch-by-branch disposition (28 refs inspected)

| Branch | Related PR | Disposition on current main |
|---|---:|---|
| audit/docs-architecture-refresh-20261108 | #148 closed unmerged | Superseded audit snapshot; newer canonical audit/handoff retained |
| audit/repository-docs-structure-20261107 | #143 merged | Already integrated |
| audit/repository-documentation-and-mekongphon-rights-20261107 | #138 closed unmerged | Rights/provenance work superseded by current source registry and rights review; no distinct production code needed |
| benchmark/additional-lao-g2p-20261108 | #156 closed unmerged | Comparator results already reconciled into current research inventory; do not merge stale workflow snapshot |
| benchmark/current-main-comparative-20261110 | #160 closed after port | Workflow branch triggers and benchmark reconciliation ported; superseded PR closed |
| benchmark/hvulao-1k-three-engine-20261108 | #147 closed unmerged | Stress-test evidence already represented in current inventory; older branch snapshot |
| benchmark/laonetics-same-set-20261110 | — | Script, isolated workflow and report ported; NC-licensed candidate remains research-only |
| benchmark/mekongphon-immutable-inference-20261107 | #139 closed unmerged | Pinned model revisions and inference evidence already present in main |
| benchmark/mekongphon-three-engine | #137 closed unmerged | Same-set benchmark implementation/results superseded by current benchmark harness and inventory |
| benchmark/meta-hybrid-v3-multiengine-20261110 | #161 closed unmerged | Superseded by r2 branch; no separate merge |
| benchmark/meta-hybrid-v3-multiengine-r2-20261110 | #162 closed after port | Comparator module, tests, CLI/API and research-only workflow ported to main |
| docs/hybrid-mixed-script-input-coverage-20261108 | #151 merged | Already integrated |
| docs/post-deploy-benchmark-20261108 | #144 merged | Already integrated |
| docs/romanization-numeric-crosswalk-20261108 | #153 merged | Already integrated |
| feat/deterministic-mekongphon-reference-profile-20261108 | #146 closed unmerged | Profile and benchmark evidence already represented by main's deterministic profiles |
| feat/grapheme-first-provisional-fallback-20261108 | #155 merged | Already integrated |
| feat/hybrid-deterministic-lao-engine-20261108 | #149 merged | Already integrated |
| feat/ipa-hybrid-engine-arbitration-20261108 | #154 merged | Already integrated |
| feat/mekongphon-first-stage | #145 open | Not merged: changes CLI/Python default to neural-first; explicit architecture decision remains outstanding |
| feat/pages-hybrid-v2-browser | #158 merged | Browser neural runtime has now been deliberately retired from the public service; Python research model retained |
| feature/grapheme-fallback-ipa-preview-20261107 | #142 closed unmerged | Superseded by merged grapheme-preview/fallback work (#155/#159) |
| feature/lao-ukrainian-practical-system-20261107 | #141 closed unmerged | Superseded by later merged integrated system and audits (#143/#149) |
| feature/meta-hybrid-v3-multiengine-20261110 | — | Behind main; duplicate/older Meta-Hybrid branch, no unique commits to port |
| fix/hybrid-partial-input-rendering-20261108 | #150 merged | Already integrated |
| fix/provisional-grapheme-output-docs-20261110 | #159 merged | Already integrated |
| fix/romanization-numeric-crosswalk-20261108 | #152 merged | Already integrated |
| improve/rule-engine-error-analysis-20261107 | #140 closed unmerged | Diagnostics and rule protections are represented in current engine/tests; no stale snapshot merge |
| research/written-evidence-phonology-2026-11-09 | #157 merged | Already integrated |

**Result:** all 28 refs have a disposition. 12 are from merged PRs; 3 branch-only/open-PR workstreams have been selectively ported (benchmark reconciliation, Meta-Hybrid v3 research comparator, Laonetics research benchmark); 11 closed-unmerged branches are superseded snapshots; one duplicate Meta-Hybrid branch is behind main; one neural-first architecture PR remains open as a deliberate decision blocker. No branch refs were deleted.


## Research CLI text formatting regression — 2026-11-10

**Status: DONE_VERIFIED.** PR [#164](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/164), starting from main 2b492771785564247ad26f6d911e7c36204817f0; implementation/test head 6cf650ff892ff8bf82d455cb665d38427eb6c256; documentation-complete head e5af9e5462ec57ec6d858fa25824cd517a7646c6.

The human-readable hybrid-v2 and meta-hybrid-v3 CLI branches emitted a literal backslash-n in the input/engine header. Two output-level regression tests reproduced the issue and failed in test-first Verify [#42859192089](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42859192089). The implementation now emits an actual newline. Implementation-head Verify [#42859285823 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42859285823) and documentation-complete exact-head Verify [#42859601706 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42859601706): 346 Python, 152 Node and 22 Chromium tests passed on both heads; IPA-gold structure validation, repository data/evidence audit, optional external-G2P syntax/CLI, locked install, build, generated-data reproducibility, Chromium and built-page checks passed.

Scope is limited to research CLI presentation. No engine defaults, linguistic rules, browser assets or deployment behavior changed. PR #145 remains unmerged because its neural-first CLI default conflicts with the current system specification's deterministic default; the branch is retained for an explicit architecture decision. Independent adjudicated IPA gold remains 0.


## MekongPhon standalone IPA stage and benchmark refresh — 2026-11-10

**Status: DONE_VERIFIED.** PR [#165](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/165), base main 795aa159dce25477491f71d23c03f11fc48801db. Added a typed stage-one result and public API (MekongPhonIPAResult, MekongPhonEngine.transcribe_ipa(), transcribe_ipa()), exported it from the package, and refactored the full transcribe()/transcribe_lao() path to continue through the existing Ukrainian target adapter. The benchmark smoke check now validates stage-one IPA only. Deterministic CLI/API defaults remain unchanged.

Test-first run [#42861065170](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42861065170) failed on the two expected missing-API tests. Exact implementation-head Verify [#42861658071 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42861658071): 348 Python, 152 Node, 22 Chromium. Actual pinned neural inference benchmark [#42861658338 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42861658338), schema 8.0, artifact 13785117940. A third regression test verifies that full transcribe() still invokes target adaptation. Documentation-complete exact-head Verify [#42862638316 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42862638316): 349 Python, 152 Node and 22 Chromium tests passed; repository audit, IPA schema, build, generated-data reproducibility and built-page checks also passed.

Fresh benchmark evidence on merged main 795aa159dce25477491f71d23c03f11fc48801db:
- Verify [#42860129902 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860129902): 346 Python, 152 Node, 22 Chromium.
- MekongPhon 100-word schema 8 [#42860129937 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860129937), artifact 13785375583.
- MekongPhon deterministic-profile comparison [#42860130108 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860130108), artifact 13784093190.
- HVULao 1k three-engine stress schema 1.5 [#42860130098 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860130098), artifact 13785715183.
- Hybrid v2 HVULao 1k stress [#42860129905 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860129905), artifact 13784553637.

The 100-word schema-8 result reports 90/100 segmental exact output matches for ClippyFirst (CER 5.48%), 82/100 for MekongPhon Neural (6.64%) and 68/100 for Lao2IPA (8.97%). Hybrid v2 tonal and MekongPhon Neural tonal both report 74/100 (CER 8.29%) under the benchmark's tonal reference convention. This is dictionary-seeded concordance, not independent project gold.

The HVULao 1k three-engine report shows 66.1% IPA-complete sentences for deterministic engines, 93.4% for the neural source-IPA engine, and 100% Ukrainian-side rendering for the hybrid deterministic engine. The separate Hybrid v2 report shows 100% Ukrainian rendering, 66.1% complete segmental IPA sentences, 22.8% parseable tonal IPA rows, 10 fully and 4 partially aligned tone rows, 0 runtime errors, 61 token-limit rejections and 5 unsupported-character rejections. HVULao has no IPA reference; these are stress/coverage/runtime measures, not accuracy.

PR #145 remains open: compare against main showed 292 commits behind and 24 ahead; it changes the CLI default to neural-first, contrary to the current deterministic-default specification. The stage-one API was selectively implemented without importing that change.


## Public MekongPhon IPA API documentation and export contract — 2026-11-10

**Status: DONE_VERIFIED.** PR [#167](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/167), based on main `20a44ab4c3730434bd0176a699853b796fa8fd1d`; implementation/test head `1c029b841651b11283f0e19b1f5358078e0bfb4c`.

README usage now demonstrates the package-root `transcribe_ipa()` source-stage API and the full `transcribe_lao()` two-stage path. The codebase map is refreshed to mainline and documents the standalone typed IPA result, explicit target-adaptation continuation, tests and research-only scope. A new offline regression asserts that `MekongPhonIPAResult` and `transcribe_ipa` are actually exported from `lao_ukrainian`.

Exact-head Verify [#42871293571 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42871293571): 350 Python, 152 Node and 22 Chromium tests passed; IPA-gold schema validation, repository data/evidence audit, external-G2P syntax/CLI, locked install, browser tests, build, generated-data reproducibility and built-page checks passed. This documentation/test-only update does not change the deterministic default, model inference, Ukrainian mappings or public website. Independent adjudicated IPA gold remains 0.


## Public MekongPhon API and current benchmark-summary reconciliation — 2026-11-10

**Status: DONE_VERIFIED.** PR [#167](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/167), squash-merged as `d5b21b1476f6eb7bb0db8174f93ed027ab5fd944`; base main `20a44ab4c3730434bd0176a699853b796fa8fd1d`, documentation-complete PR head `f09b39a215f3ee04b766677e0b74f5de5c2803b2`.

README now documents the public `transcribe_ipa()` source-stage API and the full `transcribe_lao()` path. The codebase map is current to mainline and describes the typed IPA stage, result types, test locations and separation from the deterministic default/browser runtime. An offline regression checks package-root exports of `MekongPhonIPAResult` and `transcribe_ipa`.

The README's prior schema-6/2026-11-09 benchmark paragraph was stale. It now summarizes the 2026-11-10 schema-8 100-word common-set comparison and the latest HVULao 1k stress workflows, with explicit caveats that dictionary-seeded concordance and no-IPA-gold stress coverage do not establish independent phonetic accuracy.

Exact documentation-complete Verify [#42871983082 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42871983082): 350 Python, 152 Node and 22 Chromium tests passed; repository audit, IPA schema, external-G2P CLI, locked install, build, generated-data reproducibility and built-page checks passed. Mainline Verify [#42872275176](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42872275176) was triggered by the merge; its exact-main result remains pending at this audit checkpoint.

No engine, model, IPA mapping, deterministic default or browser runtime behavior changed. Independent adjudicated IPA gold remains 0.


## Remove instructional copy from the Lao input — DONE_VERIFIED, 2026-11-10

- Removed the in-field Lao-script placeholder so the writing area opens clean, without a prefilled instruction or example phrase.
- Renamed the visually hidden accessible label from “Лаоський текст” to “Текст для аналізу”; the field remains programmatically named for assistive technology.
- Updated browser and static regression coverage, and removed the now-unused placeholder styling. Existing field ID, Lao language metadata, input behavior, examples and engine contracts are unchanged.
- Exact-head Verify [#42885560300 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42885560300) on `777c2e5baa620132b76ddceb323b361aae9b2886`: **350 Python, 161 Node and 23 Chromium tests passed**. Repository data/evidence audit, IPA-gold schema validation, optional external-G2P syntax/CLI, static build, generated-data reproducibility and built-page/relative-asset checks also passed.
- Acceptance: clean input field and accessible name — DONE_VERIFIED. Manual device/screen-reader review remains separate; this change makes no phonetic-accuracy claim.


## Exact-head verification after handoff reconciliation — DONE_VERIFIED, 2026-11-10

The final input-field implementation, static/browser regression tests and updated master handoff/audit were verified together on `17d97f0de2070dabc15774289a26bdbd9b9561bc` by [Verify run #42885768390 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42885768390). Results: **350 Python tests, 161 Node tests and 23 Chromium tests passed**; repository data/evidence audit, IPA-gold schema validation, optional external-G2P syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks passed. No failures.


## Contrast repair: pronunciation / romanization mode switch — PARTIAL, 2026-11-10

- The inactive method button previously used `#68716A` text on `#E8EBE1`, a **4.18:1** contrast ratio, below WCAG AA's 4.5:1 normal-text threshold.
- Updated the inactive state to use a silk surface (`#FFFCF5`), darker text (`#505D55`) and a visible muted border (`#68716A`). The active state remains Mekong green (`#173F3A`) with silk text (`#FFFCF5`); its distinction is also preserved in `aria-pressed`.
- Added static CSS contract assertions and a Chromium test that computes text and boundary contrast for both states, then toggles the selected method to check state behavior.
- Target ratios after the change: inactive text **6.75:1**, inactive border against group surface **4.18:1**, active text **11.33:1**. The first Chromium run caught a test setup issue: the mode switch was still inside the hidden empty-results panel, so the click could not run. The test now enters a sample first. Acceptance awaits a fresh exact-head Verify; visual review on physical displays remains separate.

- Follow-up check also found the secondary “Очистити” action used muted text on the paper surface at 4.41:1. Its foreground is now darkened to `#505D55` and its border to `#68716A`; static tests check text and boundary contrast against both paper and silk surfaces.

- The browser test now waits for the results panel to become visible before measuring or clicking the method buttons, matching the actual asynchronous UI lifecycle.

- The next Chromium run verified contrast ratios and state attributes but caught that the selected romanization button did not receive the expected computed background after interaction. CSS now keys the selected visual treatment directly to `aria-pressed="true"`, the same state exposed to assistive technology, rather than relying on a parallel class selector. A new exact-head run must verify this behavior.

- Bumped the stylesheet cache key to `20261110-contrast-1` so deployed browsers/CDNs cannot keep serving the previous button palette. Chromium now also asserts the active class and that the selected button does not retain its inactive silk background.

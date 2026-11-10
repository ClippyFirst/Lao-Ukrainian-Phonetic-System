# Current repository and documentation continuation — 2026-11-10

**Repository:** `ClippyFirst/Lao-Ukrainian-Phonetic-System`  
**Current default branch:** `main`  
**Implementation merge SHA:** `68aa563ebc13da7e49da533e46301d43c13b5810`  
**Documentation checkpoint verified:** `ee6ced771fd5be553443741fb6007681bd4d2f31` — Verify [#42809109496 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42809109496)  
**Starting main SHA:** `0a91bb62d48a6110d5129460fae4efee580863f2`  
**Implementation commit:** `8c7fffe99746e21769ee40e92818f5e10fa5081c`  
**Final PR branch head:** `24463a385a78a3182a23ef760fb9fe2c2e023450`  
**Merged PR:** [#159](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/159)  
**Exact-head Verify:** [#42796863636 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42796863636)  
**Mainline Pages workflow:** [#42797184810 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42797184810)

This is the current status authority for the 2026-11-10 continuation. Older dated reports and older sections of the master handoff remain historical evidence; where their branch, PR, deployment or fallback statements conflict with this checkpoint, this file and the leading post-merge handoff section take precedence.

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

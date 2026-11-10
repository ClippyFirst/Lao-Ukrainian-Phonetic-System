## Comparative benchmark reconciliation — 2026-11-10

**Scope:** verify what the current production site/engine can honestly claim against public Lao G2P systems. This is a reconciliation of existing executed benchmark evidence plus a newly enabled isolated CI rerun; it is not a claim that the latest external-comparator rerun has completed.

### Latest completed common-set evidence

The latest documented confidence-gated 100-word MekongPhon held-out comparison (schema 6.0; run [#42654328706](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42654328706)) reports:

| Engine/lane | Segmental CER | Segmental exact | Tonal CER | Tonal exact | Output coverage |
|---|---:|---:|---:|---:|---:|
| ClippyFirst hybrid | **6.15%** | **90/100** | 22.90% native contour; 11.39% Mekong evaluation convention | 25/100 native; 69/100 converted | 100% |
| MekongPhon Neural | 6.64% | 82/100 | **8.29%** | **74/100** | 100% |
| Lao2IPA 1.0.0 | 8.97% | 68/100 | 11.97% | 56/100 | 100% |

ClippyFirst's 100% visible output includes provisional IPA hints and explicit unknown markers. Only 97/100 inputs had fully accepted segmental IPA and 91/100 fully accepted tone contours; the 3 provisional units are not accepted IPA. This is a dictionary-seeded reference-concordance test, not independently adjudicated accuracy; project IPA gold remains 0.

### Dual-lane hybrid v2

The completed same-split v2 run [#42673479457](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42673479457) combines the strongest measured fields without fabricating a fused IPA string:

- ClippyFirst deterministic hybrid supplies segmental IPA and Ukrainian rendering: 6.15% segmental CER, 90/100 exact.
- Untouched pinned MekongPhon Neural supplies the separate tonal IPA lane: 8.29% tonal CER, 74/100 exact.
- Ukrainian rendering: 100/100 inputs and 169/169 units.
- Neural tone contours could be associated with 112/169 syllables (66.27%); per-syllable associations remain UNCERTAIN.

This is the strongest *measured dual-lane combination* in the repository's current evidence, not proof that one unified transcription engine is globally best. Neural tonal output is separate and optional; the default production path remains deterministic.

### Sentence-domain stress test

Hybrid v2 HVULao run [#42676571999](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42676571999) completed with:
- 1,000/1,000 rows and 21,534/21,534 units visibly rendered;
- 661/1,000 complete segmental IPA sentences (66.1%);
- 16,955/17,353 segmental IPA units (97.706%);
- 228/1,000 parseable tonal IPA outputs (22.8%);
- 10 fully order-aligned and 4 partially aligned tone-association rows;
- 0 unexpected runtime errors.

HVULao contains no IPA gold. These are coverage/parseability/runtime measurements, not accuracy. The model rejected 66 rows (61 token-limit, 5 unsupported-character); no silent truncation is performed.

### Wider external comparators already measured

The repository's pinned 100-word diagnostic inventory also records Epitran (10.96% segmental CER; 36.94% tonal), orthography2ipa (19.60%; 37.51%), Phonetisaurus (78.90% segmental; 0 exact), and Transphone supervised Lao (24.25%; 46.49%). These are source-reference concordance scores on the same small dictionary-seeded split, not independent gold. The inventory's earlier ClippyFirst row (14.45%) predates schema 6.0 and is superseded by the later schema-6.0 and v2 results above; do not mix scoring contracts or schema versions.

The MekongPhon LREC 2026 paper reports under 2% CER on its own 13,442-sentence held-out evaluation. That dataset/protocol differs from this repository's 100-word subset, so the published number is not directly rank-comparable. It does show that ClippyFirst has not demonstrated leadership against the best published Lao G2P result.

### New rerun branch and status

- Starting main: `657eee19c1b9707b5ffd08ae41f165e1fc3f1061`.
- Branch: `benchmark/current-main-comparative-20261110`.
- Workflow trigger update commit: `b6cec3cf5a2b5e31b035f6fdd3a538919ef3c516`.
- Updated `.github/workflows/external-lao-g2p-benchmarks.yml` so pushes to `benchmark/**` can run the existing pinned Epitran / orthography2ipa / Transphone / Phonetisaurus suite without pushing directly to `main`.
- The workflow dispatch/status/artifacts are not exposed by the available GitHub connector actions in this session. The rerun is therefore **PENDING / not yet verified**, not DONE_VERIFIED. The branch push should match the configured event/path filters, but no check run is visible through the available status endpoint, so execution itself is not asserted. The local container cannot reach GitHub to clone/run the workflow dependencies. Do not invent a new run ID or claim fresh benchmark results.

### Verdict and acceptance

**Current evidence:** ClippyFirst leads this particular 100-word set on segmental CER, while MekongPhon Neural leads on tonal CER. Hybrid v2 preserves those two best measured lanes separately. No evidence supports “best Lao phonetic engine on the internet” as a whole-system claim; the published MekongPhon <2% result remains ahead on its own, non-comparable test protocol. Independent adjudicated project IPA gold is still 0.

Acceptance for a genuine leadership claim requires: (1) a rights-cleared, dialect-scoped independent IPA gold set; (2) frozen train/dev/test separation with no held-out vocabulary used for checkpoint selection; (3) all current comparators run on that same untouched test set; (4) separate segmental, tonal, exact-match, CER/PER, coverage, OOV, and latency results; and (5) confidence-gated scoring that excludes provisional hints. Until then the valid status is **strong reference-relative segmental result plus best-of-lanes hybrid prototype, not globally best or independently validated**.

---

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

# Validation

## Deterministic structural validation

The test suite covers:

- NFC normalization and mixed-script rejection;
- ordinary consonant and vowel mappings;
- consonant-class-dependent Vientiane tones;
- live/dead classification;
- final-stop neutralization;
- preposed long/short vowel structures;
- special-vowel handling for ໄ/ໃ;
- structural handling of ຳ and Niggahita-related forms;
- the vowel-carrier behavior of ອ;
- Russian-versus-Ukrainian comparative decisions.

A repository-level audit script additionally checks registry uniqueness and Lao code-point ranges:

    python scripts/audit.py

Derived correspondence data can be regenerated from the canonical mapping:

    python scripts/generate_derived.py

## Test status

The merged code commit `007c6a7e0bce0ca72cda3ddda3054c69492ca3b8` passed GitHub Actions verification on `main` in [run 39597989767](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989767).

- Python unit tests: **54 passed**, including tone-rule registry integrity, a 60-case onset-class × live/dead × quantity × tone-mark selector cross-product, Unicode control handling, and shared IPA-to-Ukrainian target fixtures.
- Browser engine tests: **37 passed**, including CRLF whitespace, U+200B rejection, and the same nine IPA-to-Ukrainian target fixtures.
- Optional external-G2P harness syntax and `--help` check: passed; the external package comparison itself was not run.
- Canonical browser data regeneration and generated-data reproducibility: passed.
- Built-page and relative-asset checks: passed.
- GitHub Pages build/artifact checks: passed, followed by successful deployment in [run 39597989697](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/39597989697).

These results verify the merged engineering state and static deployment, not linguistic truth. CI success is not an expert adjudication or evidence of corpus-level phonological accuracy. The tone-rule tests check table integrity, selector reachability and conservative fallback only; they do not independently validate the Vientiane tone model. Target fixtures test the project-defined IPA-to-Ukrainian policy, not independent Lao pronunciation truth.

## Empirical validation

No empirical accuracy percentage is claimed until a versioned Lao gold corpus with an explicit denominator and expert adjudication exists. Shared regression fixtures are engineering regression cases, not an independent gold corpus.

## Independent G2P comparison harness

The optional comparison procedure is documented in [independent-g2p-comparison.md](independent-g2p-comparison.md). It uses `scripts/compare_external_g2p.py` with `lao2ipa==1.0.0`, compares IPA outputs after NFC normalization only, and emits a per-case JSON report. Mismatches are intentionally not treated as a correctness verdict. The external comparison has not yet been executed, so no match rate or independent accuracy claim is made.


## External G2P workflow verification status (2026-10-24)

The reproducible workflow and unittest contract checks ran successfully in [workflow 40092430175](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430175), with the main verification suite passing in [run 40092430173](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40092430173). The uploaded artifact was inspected: lao2ipa 1.0.0 processed 36/36 engineering fixtures with 0 runtime errors; project outputs matched the fixture in 36/36, external outputs matched it in 0/36, and exact project/external matches were 0/36. The external output consistently adds tone contours in examples such as `kɤ˧˥` vs project `kɤ`; at least one synthetic vowel pattern (`ເກຽ`) also differs materially (`keː˩˧iːə` vs `kiːə`). These are **diagnostic mismatches only**, not proof that either system is correct or incorrect, because the fixture is not independent gold and the engine conventions/dialect assumptions need review. The harness smoke task is DONE_VERIFIED; empirical accuracy remains unmeasured and blocked by absence of an independently adjudicated gold corpus.


## Diagnostic metric schema v3 — pending verification (2026-10-24)

PR [#14](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/14) changes the report's ambiguous `exact_match_rate` to `implementation_agreement_rate` and makes `accuracy: null` / `independent_gold_count: 0` machine-readable. The current branch's full verification and optional `lao2ipa==1.0.0` run are pending. Until the schema-v3 artifact is inspected, this refinement is IN_PROGRESS. The prior schema-v2 artifact remains a historical diagnostic record, not an accuracy benchmark.


The first schema-v3 workflow attempt [40093135298](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093135298) generated a schema-v3 report but failed at exit-status evaluation with a stale variable reference. The branch fixes the reference and adds a regression test. Status remains IN_PROGRESS until a new workflow run and main verification suite pass; no accuracy claim is made.


## Diagnostic metric schema v3 final status (2026-10-24)

PR #14 branch verification [40093370613](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370613) passed; optional comparator [40093370619](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093370619) passed. The inspected schema-v3 artifact has 36 cases, 0 runtime errors, `implementation_agreement_rate: 0.0`, `independent_gold_count: 0`, `accuracy: null`, and `score_status: NOT_SCORED_NO_INDEPENDENT_GOLD`. This closes the metric-labeling task, not the missing gold-corpus task.


## Final merge status (2026-10-24)

Lao G2P diagnostic metric hardening is merged at `5f003928c495e82a97f3077729ea4ec50af044ba`. The current main-branch validation and optional comparator runs triggered by the merge are tracked separately; the verified PR-head runs were [40093508377](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093508377) and [40093508384](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40093508384). This closes the diagnostic-schema task only, not the independent gold-corpus task.


## Selectable romanization-to-Ukrainian mode — 2026-10-30

Exact branch-head verification: workflow 41120593831, commit 4db9dfe10045aa4d66af921b11e0d2fd5b9d738f.

- Python unittest discovery: **92 passed**.
- Browser engine tests: **46 passed**.
- Romanization tests: **8 passed**, including sequence/diacritic mapping, unsupported-character preservation, the CLDR palatal-nasal spelling, and a direct Lao example comparison showing the fallback output remains distinct from the phonetic result.
- Web layout tests: **5 passed**, including the accessible method selector and selected-result copy wiring.
- Optional external-G2P harness syntax/CLI check: passed.
- Browser data generation/build: passed; generated web/data.js had no drift.
- Built-page and relative-asset checks: passed.

The verification workflow establishes deterministic engineering behavior for this branch. It does not establish completeness of the provisional CLDR transform, correctness of all project orthographic choices, or empirical Lao pronunciation accuracy. The workflow did not deploy GitHub Pages because deployment is configured for pushes to main; manual browser/keyboard QA remains unavailable in this session. Invalid source text is withheld from the romanization fallback rather than being reinterpreted as a Latin input.


## Corrective revision: syllable-based romanization adapter — 2026-10-30

The earlier character-by-character Latin adapter is superseded. At this historical checkpoint, the syllable engine used a blanket `h → г` rule inside `kh/th/ph`; that interpretation was later found to confuse aspiration with an independent /h/ and is superseded by the source-grapheme crosswalk documented in D-008. The separate syllable trace and partial-on-ambiguity behavior remain in force.

Exact-head verification: [workflow 41123400527](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41123400527), commit `9a4841c53705fa245f23f5c060e53cb146d8a185`.

- Python unittest discovery: **92 passed**.
- Browser phonetic engine tests: **46 passed**.
- Existing romanization transform/adapter compatibility tests: **9 passed**.
- New romanization syllable-engine tests: **9 passed**.
- Web layout and selector tests: **5 passed**.
- External-G2P harness syntax/CLI check: passed.
- Browser build and generated-data reproducibility: passed; no drift in `web/data.js`.
- Built-page and relative-asset checks: passed.

The tests verify deterministic software behavior for the implemented provisional romanization subset. They do not establish linguistic accuracy, complete CLDR coverage, or a gold-standard Ukrainian transcription. The source report itself states that Lao has no UN-approved romanization system and no national system. Manual visual and keyboard QA remains outstanding; the existing phonetic IPA gold corpus remains independently empty.


### Final exact-head verification including evidence audit — 2026-10-30

The current implementation and evidence-registry changes passed [workflow 41123807011](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41123807011), commit `02dd2bfe24e09a10fdb08265a4074aedbce97c8c`.

- Repository data/evidence audit: passed — 43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 19 evidence sources and 33 evidence claims; all claim evidence references resolved.
- Python unittest discovery: **92 passed**.
- Browser phonetic engine: **46 passed**.
- Romanization transform/compatibility: **9 passed**.
- Romanization syllable engine: **9 passed**.
- Web layout: **5 passed**.
- External-G2P harness syntax/CLI, browser build, generated-data reproducibility and built-page/relative-asset checks: passed.

This exact-head run verifies the code, the source/claim registry additions, and the corrected comma-containing CSV claim. It does not establish empirical pronunciation accuracy or complete coverage of the provisional CLDR transform. Manual visual/keyboard QA remains outstanding.


### Final syllable-engine verification — 2026-10-30

The final syllable-parser revision passed exact-head [workflow 41124439725](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41124439725), commit `753b82c89076b2e23fbbcd937df45bf4289b7dfc`.

- Repository data/evidence audit: passed — 43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 19 evidence sources and 33 claims; all references resolved.
- Python unittest discovery: **92 passed**.
- Browser phonetic engine: **46 passed**.
- Romanization transform/compatibility: **10 passed**.
- Romanization syllable engine: **12 passed**.
- Web layout: **5 passed**.
- External-G2P harness syntax/CLI, browser build, generated-data reproducibility and built-page/relative-asset checks: passed.

At that historical checkpoint, this run included CLDR preposed-marker/postposed-nucleus parsing, longest-match onset/coda handling, position-sensitive final mappings, and the then-current blanket `h → г` interpretation inside `kh/th/ph`. That blanket rule is superseded by D-008 and the source-grapheme crosswalk below. The tests do not establish empirical pronunciation accuracy or complete CLDR/ICU coverage.


## Source-aware romanization crosswalk correction — 2026-10-30

- Replaced the former blanket h → г behavior inside kh/th/ph with a source-grapheme check: ຂ/ຄ + kh → к'; ຖ/ທ + th → т'; ຜ/ພ + ph → п'; ຫ/ຮ + h → г.
- Added crosswalk tests for aspirated stops, independent /h/, source onset mismatches, supported source-coda aliases, coda mismatches, one-to-one syllable alignment, the x → с alias for ຊ, and rejection of final h. End-to-end Lao specimens cover ຂາ/ຄາ, ຮາ/ຫາ, ກາຮາ, ກັດ, ກັບ, ກາງ, ການ, ກາມ, ກຳ, ກາຍ, ກາວ and ຊາ. The same romanized string kam is withheld without source evidence and disambiguated from the original vowel/coda spelling when that evidence is supplied.
- Test-first evidence: the new crosswalk test suite failed on the pre-correction implementation in workflow [41131862367](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41131862367), as expected. Subsequent code and test commits are present, but this documentation checkpoint does not claim they pass. Exact current-head workflow must complete before the correction is marked DONE_VERIFIED.
- Linguistic scope: Richard Ishida's *Lao Orthography Notes* separates aspirated /kʰ tʰ pʰ/ from /h/ and identifies the corresponding Lao letters; the EKI/UNGEGN BGN/PCGN 1966 report provides the Latin spellings. The phonetic IPA-first engine is unchanged. No empirical accuracy or new IPA gold claim is made.


- Intermediate workflow [41133435559](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41133435559) passed repository audit, Python tests and external-G2P harness, then failed one browser assertion because the source/provenance label no longer contained the word “romanization”. The label was restored in commit fc5d5eba43b890aa3bc4126f4c3af11ae59c6e69. This was a contract-label mismatch; the exact current-head run must still verify all browser tests and build gates.


## Source-vowel and silent-hoa crosswalk verification — 2026-10-31

Verified implementation head: d0b9a585a3edf2ad0c89ba9f9b10fcbc35aa62e6. [GitHub Actions workflow 41137893545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41137893545) completed successfully.

- Repository data/evidence audit: **passed** — 43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 20 evidence sources and 44 evidence claims; all claim references resolved.
- Python unittest discovery: **92 passed**.
- Browser phonetic engine: **46 passed**.
- Romanization transform/integration: **19 passed**.
- Romanization syllable/crosswalk engine: **27 passed**.
- Web layout: **5 passed**.
- Optional external-G2P harness syntax/CLI: **passed**.
- Static build and canonical browser-data regeneration: **passed**.
- Generated-data reproducibility (git diff --exit-code -- web/data.js): **passed**.
- Built-page and relative-asset checks: **passed**.

The romanization tests include supported decomposed high-class onsets (ຫງ/ຫຍ/ຫນ/ຫມ/ຫລ), the ຫຼ form, ຫວ, atomic ໜ/ໝ, source written-onset preservation, source-vowel mismatch, source-resolved niav, the full ເຂົ້າໜຽວ source, and A+coda-m versus AM-nucleus kam. The IPA-first pipeline remains unchanged.

This verifies deterministic implementation behavior for the supported subset only. It does not establish empirical pronunciation accuracy, complete BGN/PCGN or CLDR/ICU coverage, or a normative Lao-to-Ukrainian standard. The BGN /r/ environment ຫຣ is not yet supported by the source structural parser. Manual visual/keyboard QA and an independently adjudicated gold corpus remain outstanding.

## Ukrainian target sequence extension — 2026-10-31

Test-first correction for the missing Ukrainian shcha sequence:
- The new Python regression initially failed as expected: IPA ʃt͡ʃa returned шча instead of щ (workflow [41140800731](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140800731)).
- The canonical data/lao/ukrainian_correspondences.csv now contains the longer exact sequence /ʃt͡ʃ/ → щ. The Python and browser adapters use longest-match selection; isolated /ʃ/ → ш and /t͡ʃ/ → ч remain unchanged. The generated browser mirror was regenerated and committed.
- The evidence registry now includes 22 sources and 45 claims, including the 2025 Encyclopedia of Modern Ukraine entry and the Journal of the IPA Ukrainian description for the target sequence.
- Exact-head verification [41140937597](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41140937597) passed: repository audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings; all 22 sources and 45 claims resolve); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout 5; external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks.
- The regression is a Ukrainian target-orthography mapping only. It does not add /ʃ/ or /t͡ʃ/ to the Lao source inventory, and it does not combine arbitrary adjacent consonants into an affricate. The exact ordered sequence /ʃ/ + /t͡ʃ/ is rendered with the Ukrainian letter щ; each segment remains separately mapped when supplied alone.

This verifies deterministic implementation behavior for the documented target subset. It does not complete independent expert review of the entire target policy or establish Lao pronunciation accuracy.

## Exact-head verification — 2026-10-31 (reconciliation)

The final feature-branch commit `bd2b0b05e00c884d20818dce914603b4a0b09cc3` passed the exact-head `verify` workflow twice; the later confirmation is [run 41141316134](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41141316134).

- Repository data/evidence audit: passed (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims; references resolved).
- Python unittest discovery: **94 passed**.
- Browser phonetic engine: **47 passed**.
- Romanization integration: **19 passed**.
- Romanization syllable/crosswalk engine: **27 passed**.
- Web layout: **5 passed**.
- External-G2P harness syntax/CLI check: passed; external engine comparison was not rerun by this verification.
- Static build and canonical browser-data generation: passed.
- Generated-data reproducibility and built-page/relative-asset checks: passed.

The five test suites total **192 passing tests**. These are deterministic engineering and project-policy regressions, not independent Lao pronunciation gold. The feature branch remains in PR #65 and has not been merged or deployed. Separately, current `main` commit `d64e201f6d417c71e3437daccfa465ddb77e224f` passed GitHub Pages build and deploy in [run 41117044318](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41117044318). This is deployment evidence for `main`, not for PR #65's unmerged feature head.


## Final main verification and deployment — 2026-10-31

The source-aware romanization mode and Ukrainian target sequence extension were merged in PR #65 as `b2e1187629829b4242aa2430a9901d264910eea1`. Exact-main verification [41142746494](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746494) passed: Python **94**, browser engine **47**, romanization integration **19**, syllable crosswalk **27**, web layout **5**, repository data/evidence audit, optional external-G2P harness syntax/CLI, build, generated-data reproducibility, and built-page/relative-asset checks.

The first Pages workflow for that merge [41142746466](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142746466) exposed a stale exact-match check for the app script URL. PR #66 corrected the Pages assertion to accept the versioned `src` URL, consistent with `verify.yml`, and was merged as `a001046462de564dd2cb89e9237caa221624163c`.

- Exact-main `verify` run [41142874231](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874231): **success**.
- Exact-main GitHub Pages run [41142874311](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41142874311): **success**; build, artifact checks, artifact upload and deploy jobs all succeeded.
- The external `lao2ipa` comparison was not rerun; harness syntax/CLI validation is not an external-engine comparison.
- No independent Lao IPA gold corpus or expert linguistic adjudication was added. Accuracy remains null/unmeasured.
- Manual visual review and keyboard-only interaction testing remain unperformed; successful static artifact assertions are not a substitute.

## Public research-status regression — 2026-10-31

Test-first run [41183451808](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183451808) passed the repository audit and 94 Python tests, then failed the new browser status assertion against the stale 30 October copy (5/6 web-layout tests passed). The failure was the expected RED result.

After updating `index.html` and `system.html`, exact branch-head verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed:
- Repository data/evidence audit: 43 consonant rows, 34 vowel rows, 17 tone rules, 70 Ukrainian mappings, 22 evidence sources and 45 claims; all references resolved.
- Python: **94 passed**.
- Browser engine: **47 passed**.
- Romanization integration: **19 passed**.
- Syllable crosswalk: **27 passed**.
- Web layout/status: **6 passed**.
- Optional external-G2P harness syntax and CLI: passed; no new external engine comparison was run.
- Production build, canonical browser data generation, generated-data reproducibility, built-page and relative-asset checks: passed.

This is a docs/UI-status regression only. No phonological engine, romanization engine, canonical registry or generated artifact changed. It does not change the independent gold count (0), establish accuracy, or complete manual browser/keyboard QA.
## Post-merge exact-main verification and Pages deployment — 2026-10-31

PR #68 merged as `6293f52848b675ff53c2a1d191cdcbca3cb034b4`. Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed: repository audit (43 consonants, 34 vowels, 17 tone rules, 70 Ukrainian mappings, 22 sources, 45 claims); Python 94; browser engine 47; romanization integration 19; syllable crosswalk 27; web layout/status 6; optional external-G2P harness syntax/CLI; production build; generated-data reproducibility; built-page and relative-asset checks.

GitHub Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs. This confirms the updated public status copy is deployed. It does not complete visual screenshots, keyboard-only QA, or phonological adjudication. Independent gold remains 0 and accuracy remains null.
## PR #69 post-merge verification and deployment — 2026-10-31

PR #69 merged as `8664d800c683af28b2af840027844d53471d25d3`. Its exact-head verification [41183931581](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183931581) passed. Exact-main verification [41183960495](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960495) passed the full audit, Python 94, browser engine 47, romanization integration 19, syllable crosswalk 27, web layout/status 6, optional external-G2P harness syntax/CLI, production build, generated-data reproducibility and built-page/relative-asset checks.

Pages deployment [41183960573](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41183960573) passed both build and deploy jobs. README now points to stable workflow histories, avoiding a run-specific 'latest deployment' claim. No phonological or romanization runtime behavior changed; gold remains 0 and accuracy remains null.


## Agent workflow and dependency-free CI verification — 2026-10-31

PR #71 added project-specific agent instructions and removed unnecessary npm dependency setup.

- `package.json` has no runtime or development dependencies; its test files import Node built-ins and local project modules, and the build scripts use Python. The empty `devDependencies`, no-op `prepare`, and both workflow `npm install` steps were removed.
- `verify.yml` now uses the same action major versions as Pages: checkout v5, setup-python v6 and setup-node v5. The Node 20 action-runtime deprecation warning from the previous workflow run no longer appears.
- Exact PR-head verification [41188217991](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188217991), commit `e2b0effdfb2091a3f9ca1450d32b6f0e110d29ba`: audit passed (43 consonants, 34 vowels, 17 tone rules, 70 UA mappings, 22 evidence sources, 45 claims); Python **94 passed**; browser engine **47 passed**; romanization integration **19 passed**; syllable crosswalk **27 passed**; web layout **6 passed**; production build, generated-data reproducibility and built-page/relative-asset checks passed.
- Total engineering tests: **193 passed**. No npm package installation occurred. No external G2P comparison was run.
- The npm CLI emits a separate `DEP0040` punycode deprecation warning during npm commands. This did not fail the workflow; the logs do not identify a project-owned source of that warning.

These checks validate the current engineering contracts and build only. They do not establish phonological accuracy, independent gold-corpus coverage, expert review, or manual visual/keyboard QA.

## Pages Node 24 action migration — 2026-10-31

The first Pages run after PR #71 ([41188440580](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188440580)) succeeded but emitted Node 20 deprecation warnings from the nested upload-artifact action and deploy-pages v4. PR #72 upgraded the Pages workflow to `upload-pages-artifact@v5` and `deploy-pages@v5`, verified against the official upstream release metadata (both use Node 24-compatible action code, including the nested upload-artifact v7).

- PR #72 merged to main as `649973f320a8eb0e6cf2d927c9b90add5cdcdd68`.
- Exact-main verify [41188708711](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708711): repository audit passed; Python **94 passed**; browser **47 passed**; romanization integration **19 passed**; syllable crosswalk **27 passed**; web layout **6 passed**; build, generated-data reproducibility and built-page/relative-asset checks passed.
- Pages build and deploy [41188708689](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41188708689): both jobs **passed**. No Node 20 action-runtime deprecation warning appears in either Pages job log.
- npm CLI still emits a separate non-fatal Node `DEP0040` punycode deprecation warning. This is not an action-runtime warning and did not fail the workflows.

Total engineering tests remain **193 passed**. No external G2P comparison was run. This validates CI and deployment, not Lao pronunciation accuracy, expert gold coverage, or manual visual/keyboard QA.

## Tone-mark live-syllable regression — 2026-10-31

Test-first run [41189555009](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41189555009) passed the repository data/evidence audit and then failed the newly added Python regression as expected: **16 cases** across high/middle/low onsets, four marks, and short-vowel/long-vowel dead contexts were assigned tones by the old wildcard selectors. This established the defect before changing the registry.

The correction narrows every tone-mark selector to `syllable_type=live`, renames the rule IDs to make the condition explicit, registers Appen Butler Hill's 2017 Lao LSP document, and adds a source-linked claim for the rare middle-class-only `mai ti`/`mai catawa` mappings. The canonical browser data is regenerated from the CSV. Shared fixture cases now cover all 24 onset × mark × dead-rime combinations in both Python and browser engines. The full post-fix exact-head verification passed in [run 41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983): audit, Python 97, browser 47, romanization integration 19, syllable crosswalk 27, web layout 6, optional external-G2P harness syntax/CLI, production build, generated-data reproducibility and built-page/relative-asset checks all passed.

### Exact-head verification — tone-mark and rhyme-class correction

PR #73 exact-head workflow [41190189983](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190189983) passed on commit `13b4aee52fb7249cceceb8e494f00dcf907ce7d3`.

- Repository data/evidence audit: **43 consonant rows, 34 vowel rows, 17 tone rules, 70 Ukrainian mappings, 23 evidence sources and 47 evidence claims**; all source references resolved.
- Python: **97 passed**.
- Browser engine: **47 passed**.
- Romanization integration: **19 passed**.
- Syllable crosswalk: **27 passed**.
- Web layout: **6 passed**.
- Production build, canonical browser-data generation, generated-data reproducibility, and built-page/relative-asset checks: **passed**.
- Optional external-G2P harness syntax and CLI validation: passed; no external G2P comparison was run.
- The shared tone fixture now has 37 cases, including 24 dead-syllable/mark combinations and open diphthong/nasal-rhyme cases. Python and browser consume the same fixture.
- Total deterministic engineering tests: **196 passed**. This is not independent pronunciation gold and does not establish empirical Lao accuracy.
- npm CLI continues to emit a non-fatal Node `DEP0040` punycode deprecation warning. It is separate from the GitHub Actions Node runtime, and the workflow passes.

### Final documentation-state verification

After updating the master handoff, final audit and validation records, exact branch-head verification [41190275031](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190275031) passed on `803d1346b6278c3b25260063931bf72dc4e10457`. All workflow steps passed: repository audit, Python 97, browser 47, romanization integration 19, syllable crosswalk 27, web layout 6, optional external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. This is the final documentation-state check; the Pages deployment remains a post-merge gate.

## PR #73 merge-state verification — 2026-10-31

PR #73 merged to `main` as `0b99fd451507717664a0190dbc3bcfb7069ce15c`. The final PR-head workflow [41190329422](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190329422) passed Python 97, browser 47, romanization integration 19, syllable crosswalk 27, web layout 6, repository audit, optional G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks.

The post-merge `push` workflow and Pages deployment are not verified in this execution. The GitHub connector's workflow-run listing only exposes PR-triggered runs; the merge commit has no classic status entries; Firecrawl had insufficient credits; and the public Pages URL could not be fetched. Do not claim deployment success from PR CI or the older Pages run. See `LAO-POSTMERGE-VERIFY-001` in the master handoff for the exact remaining acceptance criteria.

### PR #74 exact-head verification

PR #74 exact-head workflow [41190577692](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190577692) passed on `56436f6f980bf7eceb148b9d7d32f935f6325d3f`: audit, Python 97, browser 47, romanization 19, syllable crosswalk 27, web layout 6, optional G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks. This reruns the full suite on the merged PR #73 code with the unused-import cleanup. Post-merge push/Pages run evidence remains unconfirmed.

### PR #74 merge state

PR #74 merged by squash as `2c53e174b2bc36f56b15efe84c350a5941ff0a82`. The exact PR-head verification [41190649502](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41190649502) passed 196 tests and all build/data checks. PR #74 changed no Pages-triggering paths; the expected Pages deployment after PR #73 remains unverified. Exact post-merge `main` verification is also unconfirmed.


## Lao tone-mark storage-order regression

The shared `tests/fixtures/tone_mark_order_cases.json` fixture defines five valid and four malformed storage-order controls. Python and browser tests consume the same cases. Valid controls cover a mark after the base onset, after a superscript vowel, before the spacing AM letter, and after the second character of a written onset sequence. Negative controls cover a mark before a superscript vowel, after AM, after a coda, and before the onset. Malformed cases must withhold IPA, tone, and Ukrainian candidates.

Test-first evidence: draft PR #76's initial exact-head workflow [41208426712](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41208426712) failed the four intended negative controls while the five valid controls passed (Python 99 tests run). This confirms the regression tests exposed missing validation before the implementation. The post-implementation exact-head workflow is pending; do not mark this task `DONE_VERIFIED` until it passes.

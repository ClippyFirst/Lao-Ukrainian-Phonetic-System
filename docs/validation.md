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
- Added crosswalk tests for aspirated stops, independent /h/, source onset mismatches, supported source-coda aliases, coda mismatches, one-to-one syllable alignment, the x → с alias for ຊ, and rejection of final h. End-to-end Lao specimens cover ຂາ/ຄາ, ຮາ/ຫາ, ກາຮາ, ກັດ, ກັບ, ກາຍ, ກາວ and ຊາ.
- Test-first evidence: the new crosswalk test suite failed on the pre-correction implementation in workflow [41131862367](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41131862367), as expected. Subsequent code and test commits are present, but this documentation checkpoint does not claim they pass. Exact current-head workflow must complete before the correction is marked DONE_VERIFIED.
- Linguistic scope: Richard Ishida's *Lao Orthography Notes* separates aspirated /kʰ tʰ pʰ/ from /h/ and identifies the corresponding Lao letters; the EKI/UNGEGN BGN/PCGN 1966 report provides the Latin spellings. The phonetic IPA-first engine is unchanged. No empirical accuracy or new IPA gold claim is made.


- Intermediate workflow [41133435559](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41133435559) passed repository audit, Python tests and external-G2P harness, then failed one browser assertion because the source/provenance label no longer contained the word “romanization”. The label was restored in commit fc5d5eba43b890aa3bc4126f4c3af11ae59c6e69. This was a contract-label mismatch; the exact current-head run must still verify all browser tests and build gates.

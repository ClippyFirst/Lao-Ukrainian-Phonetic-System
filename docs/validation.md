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

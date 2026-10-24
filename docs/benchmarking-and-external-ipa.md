# Lao: IPA benchmarking and external systems

**Status: benchmark harness added; empirical accuracy remains unmeasured until independently adjudicated gold rows exist.** This is not a claim that candidate engines have been installed, run, licensed for redistribution, or validated for Lao.

## Required pipeline boundary

source orthography → structural analysis → source-language phonology → typed IPA → ClippyFirst IPA-to-Ukrainian adapter → Ukrainian practical orthography

External engines are comparators or optional upstream IPA providers only. Preserve their raw output separately from any normalized IPA. Do not bypass the ClippyFirst IPA adapter, silently rewrite an engine's proprietary phoneme alphabet as IPA, or treat agreement among engines as ground truth.

## Reproducible benchmark

The standard-library-only harness is scripts/benchmark_ipa.py. It reads tab-separated files:

- Gold columns: id, text, gold_ipa, gold_status, profile, source_id.
- Prediction columns: id, engine, raw_output, ipa, status, version.

Run from the repository root:

python scripts/benchmark_ipa.py --gold data/benchmark/gold.tsv --predictions data/benchmark/predictions.tsv --output reports/ipa-benchmark.json

Only rows with gold_status=ADJUDICATED and non-empty gold IPA enter the denominator. For each engine, every eligible gold row is counted: an absent prediction row or empty IPA is a miss and remains in the denominator. The report provides strict NFC exact match, missing-prediction rate, and code-point Levenshtein CER. NFC and outer whitespace trim are the only normalizations: tone, vowel length, diacritics, and syllable separators remain significant. Code-point CER is a diagnostic, not a feature-weighted phonetic metric. A header-only gold file correctly yields NOT_MEASURED, not a fabricated zero or 100% score. An engine with no predictions for eligible gold rows is not scored; once an engine appears in the prediction file, omitted eligible IDs count as missing.

Stratify gold cases by syllable shape, consonant class/series, vowel type and length, coda, tone/prosody where applicable, morphology, lexical/loanword status, and uncertainty. Report the denominator and source/profile per row. Avoid training/test leakage and use a held-out set for any tuning.

## External candidates (not yet approved for runtime)

- Goruut (support/version must be verified)
- eSpeak NG (language support and IPA mode must be verified)
- language-specific lexicons/IPA dictionaries (inventory pending)

These are research leads, not verified availability claims. Before executing a candidate, record the exact release/commit, installation command, language/voice/model identifier, raw output, runtime errors, license for code plus model/dictionary/data, and whether the output is actual IPA or a tool-specific phone alphabet. Do not install or enable a candidate by default merely because it appears here.

## Acceptance gates

1. Build a versioned gold set from cited primary sources with exact page/section/audio locator, dialect/profile, and independent adjudication; Unicode tables alone do not establish pronunciation.
2. Keep raw source output immutable; store conversion rules and normalized output separately.
3. Run the same inputs/profile through ClippyFirst and each available candidate; preserve failed/missing outputs in the denominator report.
4. Evaluate both strict IPA exact match and reviewed feature-level errors (tone, vowel length/quality, onset, coda, syllable boundaries). Do not infer a winner from exact match alone.
5. Run the existing repository test/CI suite and validate the benchmark script on a synthetic fixture; do not publish synthetic scores as language accuracy.
6. Keep candidates optional, pinned, license-reviewed, and fail-closed. A missing tool must never change the core result silently.

## Current evidence status

- Harness baseline: previously executed in CI. Additional fail-closed validation requires every ADJUDICATED row to have non-empty IPA, source_id and profile; PR #29 adds regression tests for these gates and must pass CI on its final head.
- Adjudicated language-specific gold rows: not yet established by this document.
- Candidate engine availability, version, licenses, and language-specific output quality: unverified until recorded as run evidence.
- Release status: research prototype; no accuracy claim is authorized by this registry.

## Existing external run evidence (reconciled 2026-10-24)

- Latest repeated run: [workflow 40119608545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40119608545), `lao2ipa==1.0.0`, 36 structural engineering probes, 0 runtime errors, 0/36 exact agreement with current implementation/fixture. Independent gold count is 0; accuracy is null. Artifact ZIP SHA-256 `82012a0b6d22a9f0eb0f65792da10e8df162bee520c84b54a863b107cb0b6250`. Example `ເກຽ`: project `kiːə`, lao2ipa `keː˩˧iːə`; other differences include tone suffixes. These are mismatch-review leads, not proof either output is correct.
- [Goruut](https://github.com/neurlang/goruut) upstream lists Lao among supported languages and describes IPA output, but has not been executed against this repository's inputs. Candidate only.
- Do not infer `lao2ipa` is wrong from 0/36; known structural probes may differ in tone conventions, synthetic syllable validity, or vowel interpretation. The next task is source-adjudicated lexical cases plus layer-by-layer disagreement review.


## Upstream provenance and comparator triage (checked 2026-10-24)

| Candidate | Verified upstream fact | Evidence boundary / next step |
|---|---|---|
| [lao2ipa 1.0.0](https://pypi.org/project/lao2ipa/1.0.0/) | PyPI publishes the package as Apache-2.0; release artifact SHA-256 is recorded in the run evidence. Its own description says it uses orthographic-unit/syllable parsing and tone-placement heuristics. | This project successfully ran 36 probes with zero runtime errors, but zero independently adjudicated gold labels means accuracy is NOT MEASURED. Disagreements with our engine are diagnostic only. |
| [Epitran](https://github.com/dmort27/epitran) | Upstream lists lao-Laoo as Lao. | Not run in this repository's current smoke evidence. Run as a separately pinned comparator before drawing conclusions; check mapping/data provenance as well as code license. |
| [Goruut](https://github.com/neurlang/goruut) | Upstream README advertises an IPA phone set and lists Lao support. | Support claim only; no successful local run recorded here. Code license does not establish licenses for every model/data asset. |

The package license and output evidence are different things: an Apache-2.0 code license does not make a benchmark label gold, establish pronunciation correctness, or automatically license third-party source material embedded in derived data. Preserve exact package version, artifact digest, raw output, profile, and error rows.

## Lao disagreement taxonomy update — 2026-10-24

`scripts/compare_external_g2p.py` now assigns heuristic diagnostic labels to raw string mismatches: `TONE_SUFFIX_ONLY`, `TONE_AND_LENGTH_DIFFERENCE`, `VOWEL_LENGTH_ONLY`, `DIPHTHONG_OFFGLIDE_CONVENTION`, and `SEGMENTAL_OR_VOWEL_SEQUENCE_DIFFERENCE`. These labels are deliberately **not** phonological judgments. Raw IPA, NFC output, exact-match result, and tone/length marks remain unchanged; no mark is removed from the reported strings.

Categorized run [40121272427](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40121272427) shows 36/36 strict implementation mismatches, 0 runtime errors and 0 independent gold rows. Heuristic categories: 29 tone-suffix-only, 2 diphthong offglide-convention, 4 segmental/vowel-sequence differences, 1 tone-plus-length difference. These are triage signals, not accuracy.

**Interpretation priority:** 29/36 tone-suffix-only classifications are not harmless by definition: Lao tone can be contrastive. Do not strip tone or accept a mismatch without source-located lexical evidence and an explicit phonemic/phonetic convention. Review the four segmental/vowel-sequence cases (`ເກຽ`, `ກັວບ`, `ກວງ`, `ກວາງ`) next, then the `ai`/`aj` offglide convention and tone+length case.

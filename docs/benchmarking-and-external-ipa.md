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

- Harness baseline: executed successfully in prior main CI. The current PR adds fail-closed validation requiring every ADJUDICATED row to have non-empty IPA, source_id and profile; regression tests must pass on the final head.
- Adjudicated language-specific gold rows: not yet established by this document.
- Candidate engine availability, version, licenses, and language-specific output quality: unverified until recorded as run evidence.
- Release status: research prototype; no accuracy claim is authorized by this registry.

## Existing external run evidence (reconciled 2026-10-24)

- Recorded classified run: [workflow 40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060), `lao2ipa==1.0.0`, 36 structural probes, 0 runtime errors, 0/36 strict implementation agreement, independent gold=0, accuracy=null. Tone-stripped diagnostic agreement is 29/36 (80.6%) and 7/36 remain non-tone/format/length mismatches; this is not accuracy, and tone may be contrastive. Artifact ZIP SHA-256 `2b7f3c5e3c02814413e42b9f2031849c21630fba9958a7e6a38de92f7a63ff55`. Example `ເກຽ`: project `kiːə`, lao2ipa `keː˩˧iːə`.
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

## Tone-stripped diagnostic decomposition — 2026-10-24

The comparator now reports both (a) the detailed heuristic mismatch category and (b) whether the two raw IPA strings become equal after removing only the five IPA tone letters `˥˦˧˨˩` in a separate diagnostic field. This is **never used for scoring** and does not modify raw output, strict exact-match results, length marks, syllable boundaries, or the production pipeline.

This decomposition helps distinguish tone-mark disagreement from remaining segmental/format disagreement, but tone can be contrastive in Lao. A tone-stripped match is not phonological equivalence and is not accuracy. Interpret it only as a triage signal alongside the more detailed category classifier.


## Benchmark metric semantics — 2026-10-24

- `exact_match_rate` is strict string equality after the declared Unicode normalization and is comparable only when the same IPA profile/conventions are used. Tone, length, stress, syllable boundaries, tie bars and other IPA distinctions are not silently removed.
- `character_error_rate` is Levenshtein distance over Unicode code points, not a phoneme/segment error rate. IPA affricates, combining diacritics, length marks and tone symbols can occupy multiple code points; interpret this field as a string-distance diagnostic only.
- A valid score still requires a non-empty independently adjudicated gold set with source locator and profile. Smoke output, engineering fixtures, source-attested but unadjudicated entries, and inter-engine agreement are not accuracy.


## Goruut comparator — upstream verified, execution pending (2026-11-01)

**Disposition: ADD AS AN OPTIONAL RAW-OUTPUT COMPARATOR; NOT APPROVED AS A PRODUCTION PHONOLOGY PROVIDER.**

- Upstream repository: https://github.com/neurlang/goruut
- Pinned upstream source commit inspected: `b224bde02151f8f86d0fe260804e4ca743bda620` (2026-10-02; pin this commit rather than `@latest`).
- Upstream README explicitly lists **Lao** among supported languages and describes an IPA phone set, word-level tokens, punctuation preservation and tonal phones. It explicitly says syllable tokens are not provided, tie bars are not supported, and numbers/dates are unsupported and should be written as words.
- The upstream source-code repository contains an MIT license. This verifies the code license only; the license and provenance of each embedded dictionary, model, training corpus and generated language asset have not yet been audited. Do not redistribute those assets or treat the MIT code license as clearing them.
- Upstream requires Go 1.22 or newer. A language listed in the README is evidence of advertised availability, not proof of correct Lao tone, vowel length, offglides, dialect or IPA conventions.

**Benchmark treatment:** run only in a disposable optional CI job; preserve raw response, errors, exact upstream commit, language identifier, Go version, corpus hash and output artifact. Keep raw output separate from any IPA normalization. Do not synthesize syllable boundaries or tie bars, strip tone, or convert the output to target Ukrainian without an explicit reviewed mapping. The lack of syllable tokens and tie-bar support must be reported as representational limitations, not silently repaired. The engine's unsupported number/date handling requires separate normalization probes; never feed unexpanded numerals and assume valid pronunciation.

**Acceptance before promotion:** (1) successful pinned execution on the same source-located Lao inputs as existing comparators; (2) inspect exact raw output and error handling; (3) audit licenses/provenance for the Lao dictionary/model assets; (4) review tone, vowel length, offglide, syllable segmentation and dialect conventions against independent expert-adjudicated IPA; (5) score only held-out ADJUDICATED gold. Current independent gold count remains 0, so no accuracy or engine ranking is available.

Upstream evidence: https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/README.md ; https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/LICENSE ; https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/go.mod


## Goruut language-asset license gate — 2026-11-01

The language-specific embedded files in Goruut's pinned source tree are derived from separate language lexicons: its own `dicts/README.md` describes `lexicon.tsv` as word-to-IPA training data and the generated model files as embedded assets. The corresponding Lao lexicon directory is `neurlang/dataset/lao/`. The dataset repository metadata has no declared license (`license: null`), its root tree contains no LICENSE/COPYING file, and its README's partial license inventory does not assign a license/provenance to this language directory. Therefore the Goruut source MIT license is insufficient to clear the lexicon or derived model. Runtime execution and artifact retention remain BLOCKED pending per-language provenance/license clarification and owner-approved use terms. Full review: `docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md`.


## External corpus/source triage — 2026-11-01

MekongPhon LREC 2026 source triage is PARTIAL: the paper reports 367k Lao orthography–IPA pairs; inspected GitHub main `f80f6c1840c4818b51e05f2e00cded4701a5b662` includes lexicon/train/eval files, a 500-sentence qualitative sample and reproducible pipeline. Import remains BLOCKED because the repository has no declared license; source lexicon derives from SEAlang and sentence IPA is generated by greedy lexicon lookup over OPUS text with OOV sentences filtered. The split script reserves only 100 lexicon lines (seed 1234), not an independent expert gold corpus. Inspect paper adjudication protocol and secure component-level rights before import. Gold remains 0.

Detailed source-by-source findings, license boundaries and acceptance criteria: `docs/audits/current/EXTERNAL-PHONETIC-CORPUS-TRIAGE-2026-11-01.md`. No external dataset rows were copied into the project.


## Test-only Goruut runtime probe — 2026-11-01

Added an optional, test-only HTTP runtime probe for Goruut at pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620`. It explicitly enables `Lao` in Goruut's `BuiltinDictLanguages`, builds the upstream Go binary, starts the documented HTTP service and records every raw JSON response for source-engineering probes (including multiword/punctuation cases). `scripts/benchmark_goruut.py` records engine commit, language identifier, input SHA-256, raw response, token outputs and errors. It performs no IPA normalization and always reports `accuracy: null`, independent gold=0. Workflow: `.github/workflows/optional-goruut-runtime.yml`; artifact retention 30 days. Project fixtures are engineering probes, not adjudicated gold.

This probe intentionally uses upstream language assets only inside an ephemeral CI checkout for evaluation. No upstream dictionary/model files are copied into this repository or production bundle. This test-only use is distinct from production redistribution or runtime dependency approval. The probe validates availability and raw output only; it does not establish linguistic accuracy.


## Completed test-only Goruut runtime evaluation — 2026-11-01

The pinned Goruut runtime was executed, not merely inspected. Go 1.23.12, Lao explicitly enabled; 23 engineering probes yielded 18 usable outputs/5 empty; 100 MekongPhon eval rows yielded 81 usable outputs/19 empty. Strict NFC+outer-whitespace source-attested concordance was 8/100 (8%); heuristic diagnostic: 13 tone-only, 1 tone/length, 59 segmental/format, 19 no output. This is NOT accuracy or gold: MekongPhon sentence IPA is lexicon-generated and its eval is not independent expert adjudication. Server log repeatedly reports missing `weights9.bin.zlib`. Do not promote. Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.

The optional workflow builds the pinned source in an ephemeral CI checkout, captures raw HTTP output and server logs, hashes the fixture/effective config/log, and stores a 30-day artifact. It is a comparator, not an accuracy benchmark or production dependency.


## Three-repeat runtime evidence — supersedes one-shot figures

Three-repeat re-evaluation supersedes one-shot counts: engineering probes 18/23 usable, with 7/18 usable outputs unstable across repetitions; MekongPhon 81/100 usable, with 13/81 unstable; only 4/100 source-attested rows matched exactly across all three repetitions (10/100 matched at least once). Example `ຄົນ` alternated between `kʰon˩˨` and `kʰon˧˥`. This demonstrates a serious tone/reproducibility defect. It remains source-attested concordance, not accuracy. See runtime evaluation audit.

See `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md` for exact run links, hashes and per-language interpretation.


## Cross-engine comparator evidence — 2026-11-01

Additional optional lao2ipa 1.0.0 run on the 37-case engineering fixture: 0/37 exact string agreements, 31 tone-suffix-only, 2 diphthong-offglide, 4 segmental/vowel-sequence differences; zero runtime errors. The local engine matched its own fixture 37/37, but that fixture is not gold. This points to a major tone-convention difference and six cases requiring segmental review, not a winner. Latest Goruut three-repeat: 18/23 engineering outputs, 12 stable/6 unstable; 81/100 MekongPhon outputs, 70 stable/11 unstable; 5/100 all-repeat source-attested exact/notation matches, 10/100 at least one repeat. Accuracy remains null.


**Goruut warning caveat:** the pinned language module contains `weights8.bin.zlib`, but the server log attempts `weights9.bin.zlib`; no `weights9` asset exists in the inspected pinned tree. The loader path and causal relation to phonetic failures are unproven. Track this as an unresolved upstream runtime warning, not a confirmed root cause.


### Latest pinned Goruut run — exact PR head

PR #96 exact head `bca9d4a802be0e873bef34618da78bd73cd6eb79` built and ran successfully: [runtime workflow](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41310804516), artifact SHA-256 `025e5444d0a096ca07c39cbf9297ef4229275937ff487d38548fd3a551269612`. Three repeats produced 18/23 usable engineering outputs (8 stable, 10 unstable) and 81/100 usable MekongPhon outputs (68 stable, 13 unstable). Strict all-repeat source-attested concordance was 2/100; at least one repeat matched 9/100. 19/100 MekongPhon rows had no output. This is not accuracy; independent gold=0. A missing `weights9.bin.zlib` warning remains unexplained. See `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md` for full evidence and checksums. Do not promote Goruut.


### Goruut dictionary ambiguity and instability

Across the latest artifact, all 10/10 unstable engineering inputs and all 13/13 unstable MekongPhon-eval inputs carried Goruut's RandomizationWordsCount / RandomizationWordsChoices metadata. Metadata appeared on 11/23 engineering inputs and 17/100 eval inputs; not every ambiguous input changed across the three samples. The response metadata is therefore a direct upstream signal for the observed instability, not an inference from output differences alone.

Pinned upstream code counts dictionary homographs and falls back to a random dictionary pronunciation when no preferred entry is selected; it exposes this through `RandomizationWordsCount` / `RandomizationWordsChoices`. See the exact [selector code](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/repo/services/parts_of_speech_selector_service.go#L168-L205) and [response counter propagation](https://github.com/neurlang/goruut/blob/b224bde02151f8f86d0fe260804e4ca743bda620/usecases/phonemize_usecase.go#L84-L85). Treat flagged outputs as ambiguous; the missing `weights9.bin.zlib` warning is a separate unresolved issue.

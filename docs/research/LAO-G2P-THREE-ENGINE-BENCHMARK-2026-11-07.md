# Lao G2P: three-engine benchmark on MekongPhon held-out lexicon — 2026-11-07

## Status

**DONE_VERIFIED for the reproducible 100-word comparative run. PARTIAL for general accuracy claims.** The run completed successfully on GitHub Actions; this is a direct test of three implementations on one frozen held-out lexical set. It is not the paper's sentence-level 13,442-item test, nor an independently re-adjudicated gold corpus for this project.

## Scope and data

- Benchmark: the 100-entry held-out Lao seed-lexicon split `data/splits/lao_eval.csv` from [BYU MATRIX Lab / MekongPhon](https://github.com/byu-matrix-lab/MekongPhon).
- Exact upstream source revision: `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Dataset SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`.
- Gold column: `pron_with_tones`; dialect/profile: Vientiane-oriented Lao tone convention as described in MekongPhon.
- The dataset is downloaded at run time; no source rows, gold IPA, or per-item predictions are committed or included in the aggregate artifact.
- The paper states that the seed lexicon was derived from human-annotated IPA in Kerr (1972), and reports 14 inaccurate items among a 500-entry manual review (97.2% accuracy). This 100-word split was not separately re-adjudicated by this project. Treat it as a published reference set, not project-certified gold.

## Engines and pinned identities

1. **ClippyFirst rule engine** — repository source at base commit `f40c1128302486b3589da9b16bae198ef3ad1d81`; IPA read from `analyze(...).syllables[].phonemic_ipa`. A result is counted as missing if any syllable lacks IPA.
2. **Lao2IPA** — PyPI package `lao2ipa==1.0.0`, Apache-2.0.
3. **MekongPhon Neural** — Hugging Face model `byumatrixlab/lao-ipa-tonal`, resolved model revision `e02608cfcb18abfe6b1916f5f4774bfac9ac788d`, Apache-2.0.

Runtime: Python 3.12.16, CPU-only PyTorch 2.6.0, Transformers 4.49.0, SacreBLEU 2.5.1. Neural inference used beam=5; model/package loading is excluded from latency.

## Historical results — schema 1.0 (superseded; not an apples-to-apples comparison)

All metrics are corpus-level over the same 100 word inputs. CER is Unicode code-point Levenshtein edits divided by total reference code points. chrF++ uses SacreBLEU CHRF with word_order=2. NFC normalization and outer whitespace trim only; tone and length marks remain significant.

| Engine | CER ↓ | chrF++ ↑ | Exact matches | Coverage | Mean latency | Throughput |
|---|---:|---:|---:|---:|---:|---:|
| MekongPhon Neural | **8.29%** | **84.98** | **74/100 (74%)** | 100% | 85.905 ms | 11.64 words/s |
| Lao2IPA 1.0.0 | 11.97% | 73.85 | 56/100 (56%) | 100% | 0.021 ms | 47,530.93 words/s |
| ClippyFirst | 81.47% | 8.43 | 2/100 (2%) | 46% | 6.171 ms | 162.06 words/s |

ClippyFirst returned a complete `OK` analysis for 46 items and `PARTIAL` for 54. Those 54 withheld outputs remain in the denominator as misses; coverage is reported separately. No runtime errors occurred for any engine.

## Historical interpretation — schema 1.0 (superseded)

- **Best measured IPA match on this split: MekongPhon Neural.** It has the lowest CER, highest chrF++, most exact matches, and full coverage.
- **Best deterministic/throughput trade-off: Lao2IPA.** Its CER is 3.68 percentage points higher than the neural model on this test, but its measured CPU throughput is orders of magnitude higher. Latency figures are per-item inference only and should not be treated as a deployment benchmark.
- **ClippyFirst is not competitive on this lexical benchmark yet.** Its strict fail-closed policy withholds over half the entries, and its aggregate CER is high. This indicates that the current phonology/parser implementation is not ready to claim broad Lao IPA coverage or accuracy. It does not justify replacing the architecture or guessing unsupported readings.
- Do not compare these word-level scores numerically with Table 4 in the paper. The published result uses a 13,442-sentence test split generated from the held-out seed lexicon. The present run evaluates the 100 held-out lexicon entries directly as isolated words.
- The benchmark is reference-relative. The source lexicon has documented errors and IPA-convention limitations; disagreement is not automatically proof that a tool is phonetically wrong.
- No production engine, linguistic registry, Ukrainian correspondence, gold-corpus label, or runtime default was changed.

## Reproduction and evidence

- Benchmark code: `scripts/benchmark_mekongphon_three_engines.py`.
- Hosted workflow: `.github/workflows/mekongphon-three-engine-benchmark.yml`.
- Branch: `benchmark/mekongphon-three-engine`.
- Benchmark implementation commit: `210769650badb3594c7a346a6715ad8326bbe64e`.
- Workflow commit: `48dc242aad9f9fb86a22338daed5ead819e53d4d`.
- Exact-head Actions run [42305096950 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42305096950).
- Aggregate artifact [mekongphon-three-engine-aggregate](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42305096950/artifacts/13545467628), expires 2027-02-04. ZIP SHA-256: `3b159eb7763dfb38dab9dbae3cc094d34523a5f08cbae522baa2da8c22b5ee2e`.
- The artifact contains aggregate metrics and environment/model provenance only, not the 100 source entries or per-item predictions.

## Remaining work

- **TODO:** run a second diagnostic against `pron_no_tones` to separate segmental mismatches from tone mismatches, and report covered-subset scores alongside full-denominator scores.
- **BLOCKED:** independent Lao phonetics adjudication and dialect/convention approval remain required before any project accuracy claim. Existing project gold remains empty.
- **TODO:** investigate ClippyFirst's 54 `PARTIAL` cases by parser/phonology failure category, then review disagreements with a qualified Lao phonetics reviewer before changing rules.
- **BLOCKED / separate current-main issue:** Verify run [42303239593](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42303239593) on main `f40c1128302486b3589da9b16bae198ef3ad1d81` failed three browser tests: modern Lao `ຣ` expected `la` but returned null; two IPA-adapter tests expected unsupported/withheld status but got a supported result. This benchmark workflow does not run or resolve the full Verify suite.

## Readiness judgement

The comparative benchmark itself is reproducible and **DONE_VERIFIED**. The ClippyFirst engine remains a **research prototype, not accuracy-validated or release-ready**. MekongPhon Neural is the best-performing candidate on this 100-word test; Lao2IPA is the fastest practical deterministic comparator. No default replacement is authorized by this evidence alone.



## Exact PR-head verification follow-up

The full repository Verify workflow was triggered by PR #137 on exact head `a4216332341c977661de5a238be8df244e76b357`: [run 42305484657](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42305484657) **FAILURE**. Python tests and earlier workflow steps completed; the Browser engine tests step failed with the same three regressions already observed on main:
- `modern Lao ຣ defaults to l but remains analysis-dependent`: expected `la`, actual `null`;
- `browser IPA adapter withholds uncertain phonetic results`: expected `la`, actual `null`;
- `browser IPA adapter withholds incomplete IPA rather than adapting a prefix`: expected `UNSUPPORTED`, actual `SUPPORTED`.

The benchmark-specific workflow [42305096950](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42305096950) remains **SUCCESS**. The PR is left open and unmerged; the three browser failures are a separate implementation blocker and were not masked or changed as part of this benchmark.


## Final PR-head check

After the documentation reconciliation, the current PR head `1658ec5e9a70848530a5e074d3be8728eb77ecd2` was checked by Verify run [42305592423](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42305592423): **FAILURE**, again only at Browser engine tests, with the same three cases (modern `ຣ` returns null instead of `la`; uncertain IPA adapter returns null instead of `la`; incomplete IPA adapter returns `SUPPORTED` instead of `UNSUPPORTED`). Benchmark-specific run 42305096950 remains successful. This PR remains unmerged.
## Deterministic engine improvements and benchmark schema 3.0 — 2026-11-07

### What changed in ClippyFirst

- Added deterministic dynamic-programming syllabification for unspaced Lao orthographic words. Lao spaces remain phrase boundaries; candidate syllables are parsed against the existing vowel, consonant, coda and onset-cluster registries. Unsupported graphemes are retained, not deleted.
- Tone-mark multiplicity and placement are now checked per candidate syllable rather than across an entire unspaced word. Multiple valid syllables can therefore each carry one tone mark; a tone mark that cannot be consumed by a complete syllable still withholds the original token.
- Short A2 coda requirements are checked at syllable boundaries. A valid closed short-vowel syllable can now be followed by another syllable without the whole word being rejected.
- Browser syllable segmentation now depends on source-side IPA completeness, not on whether the separate Ukrainian target adapter has a mapping. This preserves the intended orthography → source phonology/IPA → Ukrainian adaptation boundary.
- Corrected Vientiane tone-contour strings to the documented conversion of Ueda's numeric contours [24], [34], [33], [21], [52] into IPA tone letters ˨˦, ˧˦, ˧, ˨˩, ˥˨. The conversion is explicitly source-scoped to Ueda's one-informant central-Vientiane study; it is not presented as a universal Lao contour model.
- Added separate segmental, tonal, tone-only and tone-category benchmark metrics. The MekongPhon contour conversion used for the benchmark is an evaluation-only adapter; it does not replace ClippyFirst's Ueda-based production contour metadata.

### Schema 3.0 results

Same 100-entry held-out lexicon, same dataset revision and SHA-256 as above. Segmental scoring uses `pron_no_tones`; full tonal scoring uses `pron_with_tones`. Coverage is the proportion of non-empty predictions; missing outputs remain in the full 100-item denominator.

| Engine / metric | CER or category error ↓ | Exact | Coverage / subset |
|---|---:|---:|---:|
| ClippyFirst segmental IPA | CER 12.79% | 64/100 | 97%; covered-subset CER 7.89% on 97 |
| Lao2IPA segmental IPA | CER 8.97% | 68/100 | 100% |
| MekongPhon Neural segmental IPA | CER 6.64% | 82/100 | 100% |
| ClippyFirst Ueda-contour tonal IPA | CER 27.16% | 19/100 | 97% |
| ClippyFirst tonal IPA rendered in MekongPhon contour convention (evaluation only) | CER 15.19% | 52/100 | 97%; covered-subset CER 10.67% on 97 |
| Lao2IPA tonal IPA | CER 11.97% | 56/100 | 100% |
| MekongPhon Neural tonal IPA | CER 8.29% | 74/100 | 100% |

On the exact same 97 words for which both engines return output, ClippyFirst is close to Lao2IPA but does not yet beat it: segmental CER 7.89% vs 7.72%, and benchmark-convention tonal CER 10.67% vs 10.42%. Exact matches are 64/97 vs 68/97 segmentally and 52/97 vs 56/97 tonally. Full-denominator ClippyFirst CER is higher still because it withholds three items.

Tone-category comparison is restricted to segmental-exact items and to reference tone suffixes that can be parsed by the documented MekongPhon contour mapping:

| Engine | Tone-category exact | Category error rate | Compared items |
|---|---:|---:|---:|
| ClippyFirst | 83.33% | 16.09% | 60 |
| Lao2IPA | 87.50% | 9.68% | 64 |
| MekongPhon Neural | 95.65% | 2.86% | 69 |

The raw Ueda-contour score and the benchmark-convention score answer different questions. The former preserves ClippyFirst's source-scoped production profile; the latter maps the same tone categories to the reference corpus's contour notation solely for evaluation. Do not substitute one for the other in production.

### Reproducibility and limitations

- Successful benchmark workflow with cross-engine shared-subset scoring: [run 42309545197](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309545197); aggregate-only artifact [13547168327](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309545197/artifacts/13547168327), SHA-256 `8267e0cf28b2bd9722a35c233efc76e3b379d47b133198c5603c48edada3e5a6`.
- Dataset revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`; dataset SHA-256 `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`.
- Neural models were resolved and recorded by exact revision: `byumatrixlab/lao-ipa-nontonal` at `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`; `byumatrixlab/lao-ipa-tonal` at `e02608cfcb18abfe6b1916f5f4774bfac9ac788d`.
- Runtime errors: zero for all three engines. ClippyFirst statuses: 95 `OK`, 5 `PARTIAL`; 97% non-empty IPA coverage.
- Remaining unresolved source-side material comprises two unconsumed vowel-tail patterns and one non-core Lao Pali/archaic consonant. The latter is intentionally withheld rather than guessed. These are the next parser/evidence review targets.
- Four segmental-exact ClippyFirst items could not be included in the tone-category subset because their reference tone suffixes did not match the currently declared five-contour Mekong mapping. This is a limitation of the comparison adapter, not silently assigned a tone.
- The upstream MekongPhon repository snapshot used here exposes no repository-root LICENSE file. The dataset is fetched only at workflow runtime; no source rows, references or per-item predictions are committed or included in the artifact. Dataset reuse/redistribution rights remain unverified and must be cleared before any corpus redistribution or training use.
- The 100-word lexicon is not the paper's 13,442-sentence test set and is not independently re-adjudicated project gold. The project still has zero independently adjudicated IPA gold records. No production default was switched to a neural model or external dependency.

**Current conclusion:** ClippyFirst is now close to Lao2IPA on the identical 97-item covered subset, but remains slightly behind it on both segmental and benchmark-normalized tonal CER. It is not yet the best complete rule engine: three items remain withheld, its tone-category error rate is higher than Lao2IPA's, and the neural MekongPhon model remains the strongest system on this split.
### Identical-subset comparison

The schema 3.0 report stores cross-engine shared-coverage metrics so a 97-item ClippyFirst subset is compared with the same 97 items from each baseline, rather than comparing 97 covered items against a 100-item baseline:

| Metric on the shared 97 items | ClippyFirst | Lao2IPA | MekongPhon Neural |
|---|---:|---:|---:|
| Segmental CER | 7.89% | 7.72% | 5.79% |
| Segmental exact | 64/97 | 68/97 | 81/97 |
| Mekong-convention tonal CER | 10.67% | 10.42% | 6.30% |
| Mekong-convention tonal exact | 52/97 | 56/97 | 73/97 |

This removes the denominator mismatch in the earlier covered-subset observation. ClippyFirst is within 0.17 percentage points of Lao2IPA segmentally and 0.25 points tonally on identical items, but is not yet ahead.

### Aggregate parser-tail diagnostic — 2026-11-07

The schema 3.0 aggregate-only diagnostic recorded the Unicode-name sequences of the two unconsumed vowel tails without retaining source words or per-item predictions:

- `LAO LETTER LO LING + LAO LETTER KO + LAO LETTER LO LING + LAO VOWEL SIGN AA + LAO LETTER MO` (one occurrence).
- `LAO LETTER MO + LAO LETTER HO SUNG + LAO VOWEL SIGN AA + LAO LETTER WO + LAO LETTER HO SUNG + LAO VOWEL SIGN MAI KAN + LAO LETTER NO` (one occurrence).
- A separate single-grapheme tail is `LAO LETTER KHO SUNG` (one occurrence). This is an onset consonant, not an established coda in the current registry.
- One additional case has malformed tone-mark order.

These shapes are diagnostics, not linguistic analyses. They do not establish that any sequence is a valid syllable boundary, consonant cluster, coda or loan spelling. The two multigrapheme tails are not covered by existing onset/vowel/coda rules, and the KHO SUNG tail cannot safely be reclassified as a coda. Keep all affected outputs withheld until a primary orthography source or qualified Vientiane reviewer establishes the exact structure. No parser relaxation or new consonant value is justified by this aggregate alone.

Diagnostic workflow [42357836206](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42357836206) SUCCESS; aggregate-only artifact [13568064669](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42357836206/artifacts/13568064669), SHA-256 `0c8e23f5bb752804cef3deb270ee762509b9de150253347528eed335d61f0ae3`.

### Tone-category error attribution — aggregate, no lexical rows

A subsequent benchmark pass attributes tone-category substitutions to the ClippyFirst rule context while still withholding all source words and per-item predictions. Among aligned syllable positions, five substitutions were observed:

| Reference → ClippyFirst | Count | ClippyFirst selector context |
|---|---:|---|
| high-mid → low-rising | 2 | high-class, live, unmarked; vowels O and UU, coda ŋ; `VNT-H-LIVE-NONE` |
| low-falling → high-mid | 2 | low-class, dead short unmarked (`VNT-L-DEAD-SHORT-NONE`); low-class, live with mai ek (`VNT-L-LIVE-EK`) |
| low-falling → low-rising | 1 | high-class, live, unmarked; `VNT-H-LIVE-NONE` |

There are also eight word-level category-sequence length mismatches and four reference-alignment failures in the ClippyFirst category subset. The five aligned substitutions do **not** justify changing the general Vientiane rule table: each ClippyFirst selector is already source-linked to the Ueda/SEAsite central-Vientiane model, whereas the MekongPhon reference may contain lexical, dialectal, annotation-convention or stress/context differences. The held-out set must not be used as training data or as a source of ad hoc exception rules. A correction requires an independent lexical source or expert adjudication, and a separate development set—not tuning on this test split.

Tone confusion/context aggregate run [42358185703](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358185703) SUCCESS; artifact [13568751034](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358185703/artifacts/13568751034), SHA-256 `0a5e89667072e58f721929f535423c0278042a615a99c29d989505e63de5c73b`.

### CPU latency after one-pass accounting correction

Final benchmark workflow [42358468909](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909) SUCCESS; aggregate artifact [13568264361](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42358468909/artifacts/13568264361), SHA-256 `8dbbd4d4043cea01d961d8cccad542ad9f1406c4a6245f64bac7ed9e3517af39`.

| Engine | Segmental availability, mean CPU ms/input | Tonal availability, mean CPU ms/input |
|---|---:|---:|
| ClippyFirst | 12.309 | 12.309 |
| Lao2IPA 1.0.0 | 0.009 | 0.020 |
| MekongPhon Neural | 68.401 | 83.735 |

ClippyFirst computes segmental IPA and tone in one `analyze()` pass, so both outputs become available at the same latency; these two values must not be summed. Lao2IPA and MekongPhon are measured as separate segmental and tonal calls. Model loading is excluded; these are single-run hosted CPU timing diagnostics, not stable cross-machine performance guarantees. ClippyFirst is substantially faster than the neural model on this runner, but much slower than Lao2IPA's lightweight transliteration function. This is an optimization lead, not a correctness criterion.


## Immutable two-model inference rerun — 2026-11-07

**DONE_VERIFIED — both MekongPhon neural checkpoints were downloaded and executed from explicit immutable Hub commits, alongside the ClippyFirst deterministic rule engine and Lao2IPA.**

- Dedicated branch: `benchmark/mekongphon-immutable-inference-20261107`.
- Benchmark workflow run [42371584765 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42371584765), exact code head `cef976a2ecb4e0318ff91f8f1d928dbb4750749e`.
- Aggregate-only artifact: [mekongphon-three-engine-aggregate](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42371584765/artifacts/13574335831); SHA-256 `e5bf7e5482f5d82fe0b3983696ac3f4e084a2f52cc01c85618c182bdbcf4dd2f`. No source rows, references or per-item predictions are included.
- Dataset: exact MekongPhon upstream revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`; 100 held-out lexemes; SHA-256 `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`.
- Tonal model: `byumatrixlab/lao-ipa-tonal@e02608cfcb18abfe6b1916f5f4774bfac9ac788d`.
- Non-tonal model: `byumatrixlab/lao-ipa-nontonal@d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`.
- Runtime: Python 3.12.16, CPU PyTorch 2.6.0, Transformers 4.49.0, Hugging Face Hub 0.29.3, SacreBLEU 2.5.1; beam=5; maximum input 128 tokens; truncation disabled. The script asserts the Hub SHA and loaded model config revision match the pins.
- Both models returned outputs for all 100 inputs; runtime errors=0. Rule engine returned segmental IPA for 97/100; its three withheld items remain missing in full-denominator scores.

### Results

All CER values below are corpus-level Unicode code-point edit distance divided by reference length. Exact means full-string IPA equality. The two models are scored against their matching reference columns: non-tonal model against `pron_no_tones`, tonal model against `pron_with_tones`.

| Engine / output | CER ↓ | Exact | Coverage |
|---|---:|---:|---:|
| ClippyFirst segmental IPA | 12.79% | 64/100 | 97% |
| Lao2IPA segmental IPA | 8.97% | 68/100 | 100% |
| MekongPhon non-tonal model | **6.64%** | **82/100** | 100% |
| ClippyFirst tonal IPA, native Ueda contour convention | 27.16% | 19/100 | 97% |
| ClippyFirst tonal IPA, MekongPhon contour convention (evaluation-only) | 15.19% | 52/100 | 97% |
| Lao2IPA tonal IPA | 11.97% | 56/100 | 100% |
| MekongPhon tonal model | **8.29%** | **74/100** | 100% |

On the **same 97 inputs** where ClippyFirst returned segmental IPA, the non-tonal model scored CER 5.79% and 81/97 exact, versus ClippyFirst 7.89% and 64/97 exact. For tonal IPA under the benchmark's MekongPhon contour convention, the tonal model scored CER 6.30% and 73/97 exact, versus ClippyFirst 10.67% and 52/97 exact. These shared-subset comparisons avoid rewarding the neural model merely for having full coverage.

For the tone-category diagnostic, restricted to segmental-exact items with alignable reference contours: ClippyFirst exact category match 83.33% (50/60), Lao2IPA 87.50% (56/64), and MekongPhon tonal 95.65% (66/69). This is a narrower conditional subset, not a corpus-wide tone accuracy score.

### Interpretation and limits

- On this frozen 100-word lexical reference, **MekongPhon wins the measured IPA CER and exact-match metrics** in both non-tonal and tonal modes. Its result is materially better than the current deterministic engine.
- ClippyFirst remains valuable as a deterministic, inspectable, low-latency, fail-closed implementation; this run does not justify replacing its architecture with a neural dependency or changing its default.
- The ClippyFirst native Ueda-contour score is not directly convention-equivalent to the MekongPhon tonal reference. The separately reported MekongPhon-contour rendering is evaluation-only and does not modify production tone metadata.
- This lexicon is dictionary-seeded and not independently re-adjudicated by this project. It is not the paper's 13,442-sentence test set and not project-certified gold. Independent expert-adjudicated IPA gold remains 0; do not convert model output into gold.
- The repository owner confirms that the project's MekongPhon rights were fully resolved in the prior project conversation. The workflow downloads the published model artifacts and benchmark CSV at runtime and publishes aggregate metrics only; it does not redistribute source rows, predictions, upstream code or corpus data.
- No source-language rules, Ukrainian correspondence registry, model adapter runtime default or UI behavior changed in this benchmark-only branch.

### Follow-up ledger

- **DONE_VERIFIED:** exact immutable revisions for both model checkpoints; runtime inference for 100/100 inputs per model; exact-head hosted benchmark; aggregate artifact and provenance.
- **PARTIAL:** numerical comparison against the published seed-lexicon reference only; no independent expert gold.
- **BLOCKED:** broad linguistic accuracy claims until dialect/IPA convention approval and independent expert double annotation/adjudication of a rights-cleared gold set.
- **TODO:** review the three rule-engine withheld structures and the segmental/tone disagreements with a qualified Lao phonetics reviewer before changing deterministic rules.


## Error-pattern analysis and deterministic-engine refinement — 2026-11-07

This checkpoint follows the immutable neural inference run and adds aggregate-only edit diagnostics, syllable-position context, a conservative minor-syllable uncertainty flag, and canonical tied IPA for the Lao affricate /t͡ɕ/.

- Exact-head benchmark workflow [42374547901 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901), code head `411c4e0b6f9bf2775585b65f09fd5c0531808d6d`.
- Aggregate artifact [13575161811](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901/artifacts/13575161811), SHA-256 `813073f4207d51d93ead737623b5bad744618d197caf20c95473fe60c787e42b`.
- Same 100-word dataset, exact dataset SHA and immutable neural model revisions as the preceding section. No per-word inputs, references, or predictions were exported.

### Updated metrics

| Engine / output | CER ↓ | Exact | Coverage |
|---|---:|---:|---:|
| ClippyFirst segmental IPA, canonical tied affricate | **11.46%** | **69/100** | 97% |
| ClippyFirst segmental, optional tie-bar normalization diagnostic | 11.62% | 69/100 | 97% |
| Lao2IPA segmental IPA | 8.97% | 68/100 | 100% |
| MekongPhon non-tonal model | 6.64% | 82/100 | 100% |
| ClippyFirst tonal IPA, native Ueda contour convention | 32.45% | 20/100 | 91% |
| ClippyFirst tonal IPA, MekongPhon contour convention (evaluation-only) | 10.20% on shared 91 | 52/91 | 91 shared |
| Lao2IPA tonal IPA | 11.97% overall; 10.86% on shared 91 | 53/91 on shared 91 | 100% |
| MekongPhon tonal model | 8.29% overall; 6.75% on shared 91 | 68/91 on shared 91 | 100% |

On the same **97 segmental items** covered by ClippyFirst, it now scores CER 6.49% and 69/97 exact, compared with Lao2IPA's 7.72% and 68/97 exact, and MekongPhon's 5.79% and 81/97 exact. Thus ClippyFirst is now slightly ahead of Lao2IPA on this shared segmental subset, but it still has lower full-set coverage and higher CER than the neural model.

For tonal outputs on the same **91 items** where ClippyFirst supplied a complete tone sequence, its evaluation-only MekongPhon-convention CER is 10.20% (52/91 exact), versus Lao2IPA 10.86% (53/91) and MekongPhon neural 6.75% (68/91). Do not compare this shared-subset score with full-set CER without also reporting coverage.

The tone-category diagnostic on segmental-exact items has 51/64 exact word-level sequences (79.69%) and a category error rate of 18.95% over 95 reference categories. Six initial short-open-/a/ shapes before a major-weighted syllable are flagged as possible minor syllables; three additional tone contexts remain unresolved for other evidence-limited reasons. The engine preserves segmental IPA but withholds the independent tone for these candidates. This is a precision/coverage decision, not a claimed accuracy gain against the dictionary reference.

### What the error profile says

- Canonicalizing Lao ຈ to tied affricate IPA `t͡ɕ` changed raw ClippyFirst segmental CER from 12.79% to 11.46% and exact matches from 64 to 69. The browser data mirror, Python registry, shared fixture, and target adapter were updated together. Untied `tɕ` remains accepted as an IPA adapter alias.
- The most frequent remaining aligned code-point substitutions include `j→i` (6), `w→ʋ` (5), `ː→ə` (5), `a→ː` (5), and `o→w` (4). The `w→ʋ` discrepancy also occurs in Lao2IPA (6 cases), indicating a likely reference/transcription-convention issue rather than a ClippyFirst-only defect. Do not collapse initial /ʋ/ and coda /w/ or rewrite diphthongs/length from this aggregate alone.
- The remaining five-tone matrix disagreements are concentrated in high-class live unmarked /oŋ, uːŋ/, low-class live /iː/ with mai ek, and high-class live unmarked /aː/. Their rule outputs match the source-scoped Vientiane matrix; the dictionary reference differs. No tone matrix retuning was made.
- Two multigrapheme unconsumed tails, one standalone KHO SUNG tail, and one malformed tone-mark-order case remain fail-closed. They do not justify new onset/coda rules.

### Linguistic basis and safety of the minor-syllable handling

Ueda (1994, p. 113) describes an exceptional non-final open /a/ syllable in central Vientiane polysyllabic words as unstressed and tone-neutral; the article is based on one 46-year-old Haysok informant. Enfield (2007, §3.1, pp. 33–34) models the minor syllable as initial C₀V₀, says it has no distinctive tone independent of the major syllable, restricts V₀ to short /a, i, u/ with no length contrast, and notes that C₀ is a restricted onset subset (palatal/velar nasals absent; b rare). Because the orthographic shape alone cannot prove that a candidate is truly minor (and Enfield's full C₀ inventory cannot be inferred from the parser), ClippyFirst does **not** assign a neutral tone. It flags only an initial unmarked short-open-/a/ candidate with a supported/core onset, excluding the explicitly disallowed palatal/velar nasal onsets, followed by a supported major-weighted syllable; it preserves segmental IPA and marks tone as analysis-dependent. The special selector is separate from the five-tone matrix.

### Interpretation and next steps

- **DONE_VERIFIED:** aggregate error diagnostics, tie-bar canonicalization, source-backed minor-syllable uncertainty handling, and exact-head benchmark execution.
- **PARTIAL:** ClippyFirst now edges Lao2IPA on the shared segmental subset and is close on shared tonal CER; full-set coverage and the neural benchmark remain better.
- **BLOCKED:** broad accuracy claims remain blocked by the non-adjudicated dictionary reference and zero independent project IPA gold.
- **TODO:** obtain a Lao phonetics review of the six minor-syllable candidates and remaining vowel/offglide disagreements; build a rights-cleared, independently adjudicated gold set before expanding rules.


### Runtime parity follow-up — 2026-11-07

The potential minor-syllable tone-unresolved selector is now mirrored in the browser engine. Both Python and browser retain segmental IPA and Ukrainian adaptation while setting the independent tone to unresolved/analysis-dependent for the same initial short-open-/a/ candidate. Regression tests cover the positive candidate and a short-open-/a/ sequence without a major-weighted following syllable, which must retain its ordinary matrix tone.

Exact-head full Verify [42375716368 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42375716368) on code/test head `b325a5f91a3fdf063f231537d1550a140cb2eff8`. Python tests, repository/data audit, external-G2P CLI, browser engine tests, generated-data reproducibility, Chromium UI and built-page checks all passed; tone-category and provenance fields are aligned across runtimes. This parity change does not alter the 100-word benchmark metrics above.


### Selector precision and diagnostic alignment — 2026-11-07

The production selector is intentionally narrower than the broad C₀V₀ diagnostic shape. It requires an initial, unmarked, short open /a/ with no parser warnings, a supported/core onset and segmental IPA, and a following major-weighted syllable in the same unspaced orthographic token. A following syllable is major-weighted when it has a long vowel, diphthong or coda. Explicit whitespace blocks the selector. The engine retains the segmental IPA and Ukrainian adaptation but withholds only the independent tone as analysis-dependent.

The browser implementation already requires supported segmental IPA; the Python implementation was tightened to the same gate. New regressions cover the candidate, non-major following syllable, explicit space and analysis-dependent onset. The benchmark now reports broad C₀V₀ shapes separately from the narrower open-/a/ selector and includes diphthong-weighted following syllables in its aggregate contexts. This is not evidence that every selected orthographic shape is lexically minor; a qualified Vientiane reviewer must review the six candidates before the selector can be considered linguistically accepted.

Exact-head full Verify [42381443428](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42381443428) is queued for `759091f28cc57a746df549ac573067af9be922ab`. Earlier success does not verify these latest changes.


### Schema 4.0: missing-tone-aware category evaluation — 2026-11-07

A review of the schema 3.0 artifact found that nullable ClippyFirst tone categories were converted to the literal string `"None"`. This inflated apparent category coverage and polluted the confusion matrix. Schema 4.0 preserves nulls, compares known syllable-aligned categories only, excludes unresolved tones from the confusion matrix, and reports category-level coverage, unresolved categories/words, complete-word rate and word-length mismatches separately.

On the 64-word segmental-exact subset:
- ClippyFirst: 79/95 categories covered (83.16%); 4 selector categories unresolved and 12 categories withheld by 8 word-length mismatches; 4 actual errors among 79 covered categories (5.06%); 51/64 exact words.
- Lao2IPA: 81/93 categories covered (87.10%); 0 errors among covered categories; 8 word-length mismatches; 56/64 exact words.
- MekongPhon neural: 105/105 categories covered; 3 errors among 105 (2.86%); 66/69 exact words.

The six possible minor open-/a/ cases in the full 100-word sample are distributed across high (1), low (2) and middle (3) onset classes. Four occur in the segmental-exact tone subset. Their tones remain withheld, not replaced with a neutral contour.

Four remaining known ClippyFirst tone discrepancies are localized: two high-class live unmarked /O, UU/ + coda ງ contexts (engine low-rising vs dictionary high-mid), one low-class live /II/ + mai-ek (engine high-mid vs dictionary low-falling), and one high-class live long /AA/ unmarked context (engine low-rising vs dictionary low-falling). These are not enough to retune the source-scoped Vientiane tone matrix without independent expert adjudication.

The leading segmental character-edit pairs are `j=>i` (6), `w=>ʋ` (5), `ː=>ə` (5), `a=>ː` (5), `o=>w` (4). The same `w=>ʋ` substitution occurs in Lao2IPA (6), so it may be a reference-convention difference. No global /w/↔/ʋ/ normalization was introduced.

Exact benchmark run [42382431568 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382431568), aggregate artifact [13577779873](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382431568/artifacts/13577779873), SHA-256 `dff1a93a429e590e791147f856e867eb508db555d53e35e10f5bedc0c4ce530d`. Full Verify [42382503937 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382503937).


### Registry reuse and observed latency — 2026-11-07

The Python analyzer now loads its linguistic registry once per input analysis and passes it through syllable segmentation/parsing, avoiding repeated CSV reads for every token and syllable. This is a performance-only change; the schema 4.0 accuracy and coverage metrics did not change.

Full Verify [42382964250 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382964250) and benchmark [42382960457 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382960457), artifact [13578092183](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42382960457/artifacts/13578092183). Mean ClippyFirst per-item latency was 14.207 ms before and 4.724 ms after the change on the same hosted 100-word benchmark setup (model loading excluded). Treat this as a single-run observation, not a statistically established speedup.


## Current MekongPhon rights disposition — owner confirmation — 2026-11-07

The repository owner confirms that the full MekongPhon rights question was resolved in the prior project conversation. Record `LIC-001 = DONE_VERIFIED (owner-confirmed)` for the authorized project use. This supersedes preliminary `UNKNOWN`/`BLOCKED` rights language elsewhere in the historical report; it is not an independent legal opinion. The 100-word lexicon remains dictionary-seeded secondary reference material, not independent project gold. Independent adjudicated Lao IPA gold remains 0.

## Production-adapter benchmark path

Both immutable model checkpoints are now invoked through the production `MekongPhonEngine.predict_raw_ipa()` path; one full `transcribe()` smoke per model checks pinned revision, non-empty raw IPA retention, typed parsing and fail-closed Ukrainian adaptation. Hub resolution is checked against tonal `e02608cfcb18abfe6b1916f5f4774bfac9ac788d` and non-tonal `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`. Raw inference timing excludes typed IPA parsing and target adaptation.

The optional IPA affricate tie-bar normalization is a notation-convention correction, not a phonological accuracy gain. The 100-word comparison was used to expose this allograph difference; it should not be described as an untouched test for that notational dimension. Other rule changes remain source-gated and are not justified by tuning on the 100-word eval split.


## Latest exact production-adapter comparator run — 2026-11-07

- Run [42416252986 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416252986), code checkpoint 5abb431598900e5545a3e73f07c97f2ab319dd4d; artifact [13591561425](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416252986/artifacts/13591561425), SHA-256 df3250e4b4e35e41d6a1c718221c0bab1e8e681a854fd30adec900309192376d. Dataset SHA-256 5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241.
- ClippyFirst rules: segmental CER 11.46%, tie-bar-normalized exact matches 69/100, segmental coverage 97%; tonal CER 32.45%, tonal coverage 91%, tone-only CER 62.35%; aligned tone-category error 5.06%, category coverage 79/95 (83.16%), 12 unresolved words and 8 word-length mismatches; zero runtime errors.
- Lao2IPA: segmental CER 8.97%, tie-bar-normalized exact matches 73/100, full segmental/tonal coverage; aligned tone-category error 0% among covered categories (81/93 covered).
- MekongPhon neural: segmental CER 6.64%, tie-bar-normalized exact matches 82/100, full segmental/tonal coverage; tone-category error 2.86%, 105/105 categories covered.
- These are 100-word dictionary-seeded comparator results, not independently adjudicated gold or unbiased population accuracy. The held-out list is not a tuning target. The rule engine's lower coverage and tone error remain visible; do not claim parity with the neural model or Lao2IPA.
- The project /w/→в practical orthography policy does not alter the raw IPA comparator's w/ʋ distinction. No source phonology rule was retuned from this run.



## Latest three-engine production-adapter benchmark — run 42416252986, inspected 2026-11-08

The latest successful workflow run before the merge used code checkpoint `5abb431598900e5545a3e73f07c97f2ab319dd4d` and produced aggregate artifact [13591561425](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42416252986/artifacts/13591561425). The artifact ZIP SHA-256 is `df3250e4b4e35e41d6a1c718221c0bab1e8e681a854fd30adec900309192376d`. Dataset SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`. All three engines completed with zero runtime errors.

### Full 100-item scores

| Engine | Segmental CER ↓ | Segmental exact | Segmental coverage | Tonal CER ↓ | Tonal exact | Tonal coverage |
|---|---:|---:|---:|---:|---:|---:|
| ClippyFirst rule engine | 11.46% | 69/100 | 97% | 32.45% native Ueda contour; 21.98% Mekong-convention evaluation | 20/100 native; 52/100 Mekong-convention | 91% |
| Lao2IPA 1.0.0 | 8.97% | 68/100 | 100% | 11.97% | 56/100 | 100% |
| MekongPhon neural | **6.64%** | **82/100** | **100%** | **8.29%** | **74/100** | **100%** |

ClippyFirst's Mekong-convention tonal rendering is evaluation-only; the native production tone contours remain source-scoped to Ueda. Do not compare the native Ueda raw-contour CER as if it used the same contour notation as the reference.

### Identical-coverage comparisons

| Same covered items | ClippyFirst | Lao2IPA | MekongPhon neural |
|---|---:|---:|---:|
| Segmental CER, shared n=97 | 6.49% (69 exact) | 7.72% (68 exact) | **5.79% (81 exact)** |
| Tonal CER, shared n=91, Mekong contour convention | 10.20% (52 exact) | 10.86% (53 exact) | **6.75% (68 exact)** |

ClippyFirst narrowly beats Lao2IPA on this run's shared segmental and evaluation-convention tonal CER, but MekongPhon neural remains stronger on both shared subsets. This is a dictionary-seeded 100-word comparison, not independent project gold or a population accuracy estimate.

### Tone-category diagnostics

- ClippyFirst: 51/64 exact word-level sequences (79.69%); 4 errors among 79 covered categories (5.06%); 79/95 categories covered; 16 unresolved.
- Lao2IPA: 56/64 exact sequences (87.50%); 0 errors among 81 covered categories; 81/93 categories covered; 12 unresolved.
- MekongPhon neural: 66/69 exact sequences (95.65%); 3 errors among 105 covered categories (2.86%); 105/105 categories covered.

These metrics are conditional on segmental-exact alignments and parseable reference contours; they are not whole-language tone accuracy.

### Single-run CPU timing (model loading excluded)

| Engine | Segmental mean latency | Tonal mean latency |
|---|---:|---:|
| ClippyFirst | 1.308 ms | 1.308 ms |
| Lao2IPA 1.0.0 | 0.006 ms | 0.013 ms |
| MekongPhon neural | 60.220 ms | 73.269 ms |

ClippyFirst emits segmental and tonal fields from one analysis pass, so its equal latency figures are not additive. These are one hosted CPU run, not statistically stable cross-machine performance guarantees.

### Environment and interpretation

Python 3.12.16; CPU PyTorch 2.6.0; Transformers 4.49.0; SacreBLEU 2.5.1. MekongPhon uses immutable tonal revision `e02608cfcb18abfe6b1916f5f4774bfac9ac788d` and non-tonal revision `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`, beam=5, 128-token maximum and truncation disabled.

**Conclusion:** MekongPhon neural is the best measured system on this reference set; Lao2IPA is fastest; ClippyFirst is inspectable and fail-closed, and on this particular run slightly outperforms Lao2IPA on identical-coverage subsets but still trails MekongPhon. No engine default should be changed on this evidence alone. Independent project IPA gold remains 0, so empirical linguistic accuracy remains unvalidated.


## Full-output coverage contract and schema 6.0 results — 2026-11-09

The previous 97% segmental / 91% tonal figures described **confidence-gated complete IPA availability**, not whether the engine returned a visible result. This distinction did not align with the product requirement that lower-confidence output must still be emitted and visibly marked. Schema 6.0 therefore changes the comparison contract:

- Every parsed syllable emits a segmental result: accepted IPA, an explicitly PROVISIONAL grapheme-derived hint, or ? at an unknown position.
- Every parsed syllable emits a tonal result: the available contour or an explicit ? when no tone contour can responsibly be supplied.
- ? is not a tone or phone prediction. It is a visible unknown marker and is included in the full-set CER denominator as an edit-bearing output.
- Output coverage and confidence coverage are both reported. A provisional result or ? satisfies output coverage but never upgrades accepted-IPA confidence or tone-category coverage.

The pinned 100-word benchmark [run #42654328706 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42654328706), schema 6.0, reports:

| Engine | Segmental CER | Segmental exact | Segmental output coverage | Tonal CER | Tonal exact | Tonal output coverage |
|---|---:|---:|---:|---:|---:|---:|
| ClippyFirst hybrid | **6.15%** | **90/100** | **100%** | 22.90% native contour; 11.39% Mekong convention | 25/100 native; 69/100 Mekong convention | **100%** |
| MekongPhon Neural | 6.64% | 82/100 | 100% | **8.29%** | **74/100** | 100% |
| Lao2IPA | 8.97% | 68/100 | 100% | 11.97% | 56/100 | 100% |

ClippyFirst rendered **100/100 inputs and 169/169 syllable units**. Of the 169 units, 165 were SUPPORTED, 1 UNCERTAIN and 3 PROVISIONAL; 3 units include explicit unknown segment markers. Fully accepted segmental IPA was available for 97/100 inputs and fully accepted tone contours for 91/100 inputs. The remaining inputs nevertheless receive visible output. Tone contour data was present for 160/169 units; missing contours are rendered as ?, not guessed.

On this dictionary-seeded split, ClippyFirst now has the lowest full-set segmental CER, even with provisional and unknown markers included. Its Mekong-convention tonal CER is slightly better than Lao2IPA, but its native-contour tonal CER remains much worse and it still trails MekongPhon Neural on tonal CER. Tone-category error is 3.81% over 105 covered categories, with 105/126 (83.33%) category coverage. This is not evidence of independent phonetic accuracy: the reference lexicon contributed to validation-sentence generation/checkpoint selection and has not been independently re-adjudicated by this project. Independent adjudicated IPA gold remains 0.

Implementation and tests:
- renderable_segmental_ipa() and renderable_tonal_ipa() keep provisional sequences and explicit unknown markers in the output path.
- render_mekong_tonal() emits ? for unresolved tone categories instead of returning an empty string.
- The core hybrid target adapter now emits ? when any typed result cannot be adapted, while preserving source IPA and confidence metadata.
- Exact-head Verify [#42654358111 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42654358111) on ef58962bd5228ff96acacf8b63c4a6593ca12440: 327 Python tests, 147 Node tests and 19 Chromium tests passed; all configured build, evidence, data and site checks passed.

**Acceptance:** 100% output coverage is DONE_VERIFIED on this 100-word set. 97% segmental and 91% tonal confidence coverage remain explicit quality metrics, not output blockers. Phonetic accuracy remains research-limited until independent expert-adjudicated IPA gold is available.

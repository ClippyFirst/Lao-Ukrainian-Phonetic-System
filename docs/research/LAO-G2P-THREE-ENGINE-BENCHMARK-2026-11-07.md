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
- **BLOCKED:** independent Lao phonetics adjudication, item-level rights clearance and dialect/convention approval remain required before any project accuracy claim. Existing project gold remains empty.
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

On the 97 words for which ClippyFirst returns segmental IPA, its segmental CER (7.89%) is lower than Lao2IPA's full-set CER (8.97%). On the same 97 covered words, the benchmark-convention tonal CER is 10.67%, also lower than Lao2IPA's full-set 11.97%. These are covered-subset comparisons, not a claim that ClippyFirst wins on the complete test: full-denominator ClippyFirst CER remains higher because it withholds three items.

Tone-category comparison is restricted to segmental-exact items and to reference tone suffixes that can be parsed by the documented MekongPhon contour mapping:

| Engine | Tone-category exact | Category error rate | Compared items |
|---|---:|---:|---:|
| ClippyFirst | 83.33% | 16.09% | 60 |
| Lao2IPA | 87.50% | 9.68% | 64 |
| MekongPhon Neural | 95.65% | 2.86% | 69 |

The raw Ueda-contour score and the benchmark-convention score answer different questions. The former preserves ClippyFirst's source-scoped production profile; the latter maps the same tone categories to the reference corpus's contour notation solely for evaluation. Do not substitute one for the other in production.

### Reproducibility and limitations

- Successful benchmark workflow: [run 42309241958](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309241958); aggregate-only artifact [13547403094](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309241958/artifacts/13547403094), SHA-256 `fb9ff14dc2e61808ae2a5d76e89cfecd38f78939b316cd9ca19e3f0879fa5e4a`.
- Dataset revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`; dataset SHA-256 `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`.
- Neural models were resolved and recorded by exact revision: `byumatrixlab/lao-ipa-nontonal` at `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`; `byumatrixlab/lao-ipa-tonal` at `e02608cfcb18abfe6b1916f5f4774bfac9ac788d`.
- Runtime errors: zero for all three engines. ClippyFirst statuses: 95 `OK`, 5 `PARTIAL`; 97% non-empty IPA coverage.
- Remaining unresolved source-side material comprises two unconsumed vowel-tail patterns and one non-core Lao Pali/archaic consonant. The latter is intentionally withheld rather than guessed. These are the next parser/evidence review targets.
- Four segmental-exact ClippyFirst items could not be included in the tone-category subset because their reference tone suffixes did not match the currently declared five-contour Mekong mapping. This is a limitation of the comparison adapter, not silently assigned a tone.
- The upstream MekongPhon repository snapshot used here exposes no repository-root LICENSE file. The dataset is fetched only at workflow runtime; no source rows, references or per-item predictions are committed or included in the artifact. Dataset reuse/redistribution rights remain unverified and must be cleared before any corpus redistribution or training use.
- The 100-word lexicon is not the paper's 13,442-sentence test set and is not independently re-adjudicated project gold. The project still has zero independently adjudicated IPA gold records. No production default was switched to a neural model or external dependency.

**Current conclusion:** ClippyFirst is now competitive with the best measured deterministic baseline on the words it can fully parse, and its covered-subset segmental and benchmark-normalized tonal CER are slightly better than Lao2IPA. It is not yet the best complete rule engine: three items remain withheld, its tone-category error rate is higher than Lao2IPA's, and the neural MekongPhon model remains the strongest system on this split.

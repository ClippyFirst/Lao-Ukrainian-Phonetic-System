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

## Results

All metrics are corpus-level over the same 100 word inputs. CER is Unicode code-point Levenshtein edits divided by total reference code points. chrF++ uses SacreBLEU CHRF with word_order=2. NFC normalization and outer whitespace trim only; tone and length marks remain significant.

| Engine | CER ↓ | chrF++ ↑ | Exact matches | Coverage | Mean latency | Throughput |
|---|---:|---:|---:|---:|---:|---:|
| MekongPhon Neural | **8.29%** | **84.98** | **74/100 (74%)** | 100% | 85.905 ms | 11.64 words/s |
| Lao2IPA 1.0.0 | 11.97% | 73.85 | 56/100 (56%) | 100% | 0.021 ms | 47,530.93 words/s |
| ClippyFirst | 81.47% | 8.43 | 2/100 (2%) | 46% | 6.171 ms | 162.06 words/s |

ClippyFirst returned a complete `OK` analysis for 46 items and `PARTIAL` for 54. Those 54 withheld outputs remain in the denominator as misses; coverage is reported separately. No runtime errors occurred for any engine.

## Interpretation

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

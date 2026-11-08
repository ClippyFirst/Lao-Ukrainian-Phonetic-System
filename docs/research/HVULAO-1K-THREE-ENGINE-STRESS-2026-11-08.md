# HVULao 1k three-engine sentence-domain stress benchmark — 2026-11-08

## Scope and evidence boundary

This benchmark runs the ClippyFirst default Vientiane rules, the opt-in deterministic `mekongphon-reference` rules, and the pinned MekongPhon non-tonal neural model over all 1,000 rows in the independent HVULao_NLP raw-text test split.

- Dataset repository: [HaHVU/HVULao_NLP](https://github.com/HaHVU/HVULao_NLP)
- Immutable source revision: `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`
- File: `Datatest1k/testorgin1000.txt`
- Git blob SHA-1: `947448807484bb994877ae5d32cba1cfdd5e2d9b`
- Dataset release: [Mendeley Data v2, DOI 10.17632/5zwym7kwn8.2](https://doi.org/10.17632/5zwym7kwn8.2)
- License recorded by the dataset publisher: CC BY 4.0.
- The paired reference annotations concern word segmentation/POS, not IPA.

**This is a sentence-domain stress, coverage, runtime and output-disagreement test. It is not an IPA accuracy benchmark.** There is no IPA gold reference, so no gold CER, phonetic accuracy, or ranking by correctness can be inferred. Pairwise disagreement only measures how different two outputs are.

The benchmark preserves all 1,000 source rows, verifies the exact Git blob bytes, and writes aggregate metrics only. No source rows or per-row IPA predictions are persisted.

## Reproducibility

- Corrected-metric executions on the same code commit `61b21237d57fc519dfff40ee22ed0649df2050e0`:
  - Push run [#42488814477 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488814477), artifact [13620542012](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488814477/artifacts/13620542012), SHA-256 `cf7df0db5181de3d7a4b70e2cfb96f092510efdd7107a13b238c2e53fac626d8`.
  - Pull-request run [#42488818208 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488818208), artifact [13621285664](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488818208/artifacts/13621285664), SHA-256 `d5ebe048e328e06b9b107062433a1b3f191f039c77ed56142d88704727fc325a`.
- Python 3.12; CPU PyTorch 2.6.0; Transformers 4.49.0; Hugging Face Hub 0.29.3.
- Neural model: `byumatrixlab/lao-ipa-nontonal`, immutable revision `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`, beam width 5, CPU.
- Schema 1.1 records two latency views: all 1,000 attempts (including explicit input rejections) and successful inference calls only. Model loading and initial smoke inference are excluded. The earlier schema 1.0 latency figures are superseded because they timed only successful neural calls but all rule-engine calls.
- Exact-head repository Verify [#42488814424 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42488814424) on the same code commit: 271 Python, 129 Node, 17 Chromium tests, corpus/audit/install/build/generated-data and built-site checks all passed.

## Results

| Metric | Vientiane rules | MekongPhon-reference rules | MekongPhon Neural |
|---|---:|---:|---:|
| Complete sentence outputs | 35 / 1,000 | 35 / 1,000 | 888 / 1,000 |
| Complete sentence coverage | 3.5% | 3.5% | 88.8% |
| Syllables with constructed IPA | 16,047 / 20,150 | 16,047 / 20,150 | Not measured |
| Rule-engine syllable IPA coverage | 79.64% | 79.64% | Not applicable |
| Mean time, all 1,000 attempts | 13.50–13.53 ms | 13.24–13.34 ms | 209.58–262.84 ms |
| Median time, all 1,000 attempts | 12.81–12.87 ms | 12.53–12.72 ms | 202.98–256.59 ms |
| p95 time, all 1,000 attempts | 26.00–26.17 ms | 25.72–26.00 ms | 430.65–533.69 ms |
| Unexpected runtime errors | 0 | 0 | 0 |

The deterministic engines construct IPA for 79.64% of the syllables they analyze, but a sentence is counted as complete only if every syllable has a constructed IPA result. This strict all-or-nothing sentence measure therefore yields 3.5% complete outputs. The benchmark intentionally does not turn a partially analyzed sentence into a complete-looking transcription.

The all-attempt latency is the fairest end-to-end comparison because every engine receives all 1,000 rows. Two complete executions on separate hosted runners were performed against the same code commit; the table reports the observed range, not an average. Neural successful-inference-only latency (n=888) ranged across the two runs from mean 236.00–295.97 ms, median 218.89–276.26 ms, p95 435.22–542.77 ms. The all-attempt measure also includes the 112 explicit input rejections. The range demonstrates meaningful hosted-CPU variability; treat these as indicative measurements, not hardware-independent throughput guarantees.

The two rule profiles have identical syllable IPA coverage on this corpus. The reference profile changes phonetic outputs and status distribution but does not expand the number of syllables for which IPA can be constructed:
- Vientiane statuses: ESTABLISHED 15,838; ANALYSIS DEPENDENT 3,839; EVIDENCE LIMITED 337; analysis-dependent 136.
- MekongPhon-reference statuses: ESTABLISHED 15,275; ANALYSIS DEPENDENT 3,839; EVIDENCE LIMITED 900; analysis-dependent 136.

## Neural input rejections

The neural wrapper rejected 112 inputs before inference, with no unexpected runtime exceptions:
- 56 inputs exceeded the wrapper's 128-code-point source limit.
- 56 inputs contained characters rejected by the current Unicode input validator.

The validator permits Lao-block characters, whitespace, and a narrow ASCII set; it rejects typographic/non-Lao characters rather than normalizing or silently deleting them. The corpus contains typographic punctuation and zero-width formatting characters (for example curly quotation marks, en dash, ellipsis, bullet and U+200B). These are input-contract rejections, not model runtime failures. The two rejection counts are the wrapper's first-applicable reason categories, not a claim that the source categories are disjoint in the raw data.

Do not silently strip punctuation, split overlength rows, or normalize unsupported code points without a separately specified and tested input-normalization policy. Those changes could alter source structure or meaning.

## Output disagreement on shared complete sentences

Only 35 sentences produced complete IPA from all three engines. Pairwise comparisons below use that shared subset, remove whitespace, and retain tone and length marks.

| Comparison | Shared sentences | Edit distance | Disagreement CER against right-hand output |
|---|---:|---:|---:|
| Vientiane vs MekongPhon-reference | 35 | 168 | 7.75% |
| Vientiane vs MekongPhon Neural | 35 | 300 | 13.67% |
| MekongPhon-reference vs MekongPhon Neural | 35 | 142 | 6.47% |

The reference rules are closer to the neural output than the default rules are on this 35-sentence subset. This is output agreement only; neither system is established as correct by this comparison.

## Interpretation and follow-up

1. **Neural engine has substantially higher full-sentence coverage** on this raw sentence corpus (88.8% vs 3.5%), while retaining explicit input guards. Its 11.2% rejected inputs expose wrapper-level length and Unicode-acceptance limitations.
2. **Rule engines remain conservative at sentence level.** Their 79.64% syllable-level IPA construction rate is materially higher than their 3.5% complete-sentence rate; the strict sentence measure exposes error propagation from any unsupported syllable.
3. **The deterministic reference profile does not improve structural coverage** on this corpus. It changes output conventions/statuses, but not the count of syllables with a constructed IPA result.
4. The 35-sentence shared subset is too small to support a broad comparative linguistic conclusion.
5. The dataset cannot replace the independent adjudicated IPA gold corpus. That corpus remains at 0 records and empirical linguistic accuracy remains unmeasured.

### Task ledger

| Task | Status | Acceptance boundary |
|---|---|---|
| Pin and integrity-check independent 1k text split | DONE_VERIFIED | Immutable revision and exact Git blob SHA-1 checked in successful run |
| Execute all three engines on 1,000 rows | DONE_VERIFIED (engineering stress test) | Run #42486829108; 0 unexpected runtime errors |
| Aggregate sentence/syllable coverage and dual latency measures | DONE_VERIFIED | Schema 1.1 artifacts 13620542012 and 13621285664; two same-commit runs; all-attempt and successful-inference denominators explicit; aggregate-only |
| Pairwise output disagreement | DONE_VERIFIED (comparative only) | Shared n=35; not accuracy |
| Broaden neural input acceptance safely | TODO / evidence-limited | Define and test Unicode/punctuation and long-input policy; no silent stripping/truncation |
| Improve deterministic sentence-level coverage | TODO / evidence-limited | Analyze unsupported categories with primary Lao orthography/phonology evidence and regression cases; do not guess |
| Independent adjudicated IPA gold | BLOCKED | Requires qualified independent annotation/adjudication; current count 0 |
| Production linguistic acceptance | BLOCKED | No gold IPA accuracy evidence or qualified specialist sign-off |

## Readiness

This benchmark is engineering-verified and reproducible. It shows the neural wrapper has much higher full-sentence coverage on this dataset, while deterministic rules remain conservative. The repository remains a research prototype, not independently accuracy-validated or production/release-ready.


## Hybrid deterministic profile and punctuation-safe input contract — exact-head run 2026-11-08

The benchmark was rerun on the final hybrid branch head `c705cf8ad782246c2d72c0d789a5e44e5196eca6`.

- GitHub Actions [run #42508759241 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241).
- Aggregate-only artifact [13628229661](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42508759241/artifacts/13628229661), SHA-256 `145966638988265a8f255163288e48de4fa8a0293941f0ec26643c7211fe7149`.
- Schema 1.2 explicitly excludes preserved ASCII/punctuation passthrough units from syllable IPA coverage. They are copied unchanged and are not assigned IPA.

| Engine | Complete sentences | Sentence coverage | Mean all-attempt latency | p95 all-attempt latency | Syllable IPA coverage |
|---|---:|---:|---:|---:|---:|
| Vientiane rules | 669/1,000 | 66.9% | 16.33 ms | 30.20 ms | 97.85% |
| MekongPhon-reference rules | 669/1,000 | 66.9% | 15.95 ms | 29.84 ms | 97.85% |
| Hybrid deterministic rules | 669/1,000 | 66.9% | 16.28 ms | 30.32 ms | 97.85% |
| MekongPhon Neural | 930/1,000 | 93.0% | 375.98 ms | 725.19 ms | not comparable in this schema |

All four engines reported zero unexpected runtime errors. Neural explicitly rejected 70 inputs (61 source-length-limit and 9 unsupported-character rejections). The deterministic engines preserve 4,146 non-Lao ASCII/punctuation units as passthrough rather than assigning them fabricated IPA.

### Interpretation

- This is an improvement in **input acceptance and mixed-text preservation**, not a 63.4-point gain in Lao phonetic coverage. The older 3.5% sentence result used the narrower input contract; the new contract explicitly preserves common ASCII and corpus-observed punctuation.
- The three deterministic profiles have identical 66.9% sentence coverage and 97.85% IPA construction across Lao syllables. The hybrid selector changes phonetic profile outputs but does not yet resolve additional structural/parser cases.
- The Neural engine remains 26.1 percentage points ahead in complete-sentence coverage on this stress set, at roughly 23 times the hybrid's mean all-attempt latency on this run.
- This dataset has no IPA gold. Neither output agreement nor coverage establishes phonetic accuracy.

### Updated task ledger

| Task | Status | Evidence / acceptance |
|---|---|---|
| Punctuation/ASCII passthrough contract | DONE_VERIFIED | Exact-head Verify #42508759262; explicit PASSTHROUGH units; punctuation regression tests |
| Hybrid 1k benchmark | DONE_VERIFIED (stress only) | Exact-head run #42508759241, artifact 13628229661 |
| Deterministic sentence coverage parity with Neural | TODO | 66.9% vs 93.0%; requires source-grounded structural parsing improvements |
| Independent IPA accuracy comparison | BLOCKED | No IPA reference in HVULao; independent adjudicated gold remains 0 |

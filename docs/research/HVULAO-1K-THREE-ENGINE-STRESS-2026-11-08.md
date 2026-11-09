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


## Schema 1.5 — full visible output and separate confidence accounting (2026-11-09)

Latest exact code run: [#42653641804 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804), aggregate artifact [#13691297821](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42653641804/artifacts/13691297821). Pinned 1,000-row corpus, 0 runtime errors.

| Engine | IPA-complete sentences | Complete IPA sentence coverage | Visible rendering coverage | Syllable IPA coverage |
|---|---:|---:|---:|---:|
| Vientiane rules | 661/1,000 | 66.1% | 62.5% | 97.71% |
| MekongPhon-reference rules | 661/1,000 | 66.1% | 34.1% | 97.71% |
| Hybrid deterministic rules | 661/1,000 | 66.1% | **100% (1,000/1,000)** | 97.71% |
| MekongPhon Neural | 934/1,000 | 93.4% | not scored in this schema | not comparable |

For the hybrid, all **21,534/21,534 analyzed units** have a visible Ukrainian-side rendering. The source-side distribution is 16,936 SUPPORTED IPA units, 19 UNCERTAIN IPA units and 398 PROVISIONAL units. Of these, 607 units lack a Ukrainian target correspondence and receive an explicit target-side ?; 398 units have provisional grapheme hints/unknown markers. The 607 target-side gaps are not counted as missing source IPA. The hybrid has 0 unrendered or failed valid inputs.

This demonstrates 100% practical rendering on this pinned text-domain set, not 100% accepted IPA: 661/1,000 sentences have a complete accepted IPA result and syllable-level accepted IPA coverage is 97.71%. The neural engine completes 934/1,000 IPA outputs but rejects 66 inputs under its source-length/character limits. The corpus contains no IPA reference, so the run measures input handling, rendering, completeness and runtime only—not pronunciation accuracy.

**Updated ledger:**
- Hybrid visible output coverage on HVULao 1k: DONE_VERIFIED (1,000/1,000 rows; 21,534/21,534 units; zero runtime errors).
- Confidence-gated source IPA completeness: PARTIAL (661/1,000 complete sentences; 97.71% syllable coverage).
- Independent phonetic accuracy: BLOCKED (no IPA gold in this dataset; project-adjudicated gold remains 0).
- Neural complete-sentence coverage parity: TODO / research task (93.4% neural vs 66.1% hybrid on this set); improvements require source-grounded structural rules, not invented pronunciations.


## Hybrid v2 — independent HVULao 1k sentence-domain stress result (2026-11-09)

Exact-head run: [Hybrid v2 HVULao 1k #42676571999 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42676571999), on code head `89311c56b89dfbaaecc40bac9eaa500304a26647`. Aggregate-only artifact [#13701372050](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42676571999/artifacts/13701372050), SHA-256 `2adad0071919f499900c37c36bf3c80f827db1c89bc0eae012cf086a29400991`.

| Hybrid v2 measure | Result |
|---|---:|
| Ukrainian rendering | **1,000/1,000 rows (100%)** |
| Rendered source units | **21,534/21,534 (100%)** |
| Complete segmental IPA sentences | 661/1,000 (66.1%) |
| Segmental IPA units | 16,955/17,353 (97.706%) |
| SUPPORTED segmental units | 16,936 |
| UNCERTAIN segmental units | 19 |
| Raw neural tonal IPA outputs | 934/1,000 (93.4%) |
| Parseable tonal IPA outputs | 228/1,000 (22.8%) |
| Rows with fully order-aligned tone associations | 10/1,000 (1.0%) |
| Rows with partial tone associations | 4/1,000 (0.4%) |
| Neural tone predictions | 200/17,353 phonetic units (1.153%) |
| Unexpected runtime errors | **0** |

Tone alignment status counts: NOT_ALIGNED 920, ORDER_ALIGNED 10, PARTIAL 4. The neural model explicitly rejected 66 inputs (61 source-codepoint-limit; 5 unsupported-character). Tone predictions remain UNCERTAIN; no tone category is promoted to adjudicated truth.

**Interpretation:** Hybrid v2 preserves 100% Ukrainian-side rendering on this corpus, but this is not 100% accepted IPA or 100% pronunciation coverage. Complete sentence IPA is 66.1%; syllable-level segmental IPA coverage is 97.706%. Parseable full tonal IPA is only 22.8%, and per-syllable tone association is sparse (200 units). The HVULao split contains no IPA gold, so these are engineering coverage/parseability metrics, not phonetic accuracy. The 100% rendering count includes typed PROVISIONAL units and explicit unknown target markers; it must never be represented as 100% verified phonetic transcription.

**Task ledger:** Hybrid v2 1k sentence-domain run DONE_VERIFIED (stress/coverage only); 100% Ukrainian rendering DONE_VERIFIED; complete segmental IPA PARTIAL; parseable tonal IPA PARTIAL; per-syllable tone association PARTIAL; independent IPA accuracy BLOCKED (requires independently adjudicated IPA gold); neural input acceptance TODO/evidence-limited (define safe policy for 66 explicit rejections; never truncate or strip silently). Browser integration remains DEFERRED until a supported inference backend is available.

The dedicated workflow `hybrid-v2-hvulao-1k.yml` and script `benchmark_hybrid_v2_hvulao_1k.py` already implement this test. Do not duplicate it inside the older three-engine benchmark workflow.

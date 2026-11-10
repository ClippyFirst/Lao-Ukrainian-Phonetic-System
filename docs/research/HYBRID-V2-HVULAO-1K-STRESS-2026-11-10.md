# Hybrid v2 — HVULao 1k sentence-domain stress — 2026-11-10

## Evidence

- Mainline run: [#42860129905 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860129905).
- Aggregate-only artifact: [13784553637](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42860129905/artifacts/13784553637).
- Main commit: 795aa159dce25477491f71d23c03f11fc48801db.
- Dataset: [HaHVU/HVULao_NLP](https://github.com/HaHVU/HVULao_NLP), immutable revision ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568, Datatest1k/testorgin1000.txt, 1,000 raw Lao sentences, Git blob SHA-1 947448807484bb994877ae5d32cba1cfdd5e2d9b.
- Dataset release: [Mendeley Data v2, DOI 10.17632/5zwym7kwn8.2](https://doi.org/10.17632/5zwym7kwn8.2), CC BY 4.0.

This is a sentence-domain stress/coverage/runtime test, not an IPA accuracy benchmark. The dataset has no IPA reference.

## Contract

- Segmental IPA and Ukrainian rendering come from the ClippyFirst deterministic hybrid. Neural segmental output does not replace that lane.
- The tonal lane is the untouched output of byumatrixlab/lao-ipa-tonal at immutable revision e02608cfcb18abfe6b1916f5f4774bfac9ac788d, beam width 5, CPU.
- Syllable-level neural tone metadata is attached only when a unique ordered contour decomposition matches deterministic syllable count. Predictions remain UNCERTAIN.
- No synthetic fused IPA string is constructed.
- Automatic truncation is disabled. Explicit model input rejections are reported.

## Results

| Metric | Result |
|---|---:|
| Input rows | 1,000 |
| Ukrainian-side rendering | **1,000/1,000 (100%)** |
| Complete segmental IPA sentences | 661/1,000 (66.1%) |
| Neural tonal model outputs returned | 934/1,000 (93.4%) |
| Parseable tonal IPA | 228/1,000 (22.8%) |
| Tone sequences fully order-aligned | 10 rows |
| Tone sequences partially aligned | 4 rows |
| Tone alignment NOT_ALIGNED | 920 rows |
| Supported / unsupported tonal IPA | 228 / 706 |
| Neural tone predictions associated | 200 / 17,353 phonetic units (1.15%) |
| Explicit unknown marker units | 398 |
| Passthrough units | 4,181 |
| Unexpected runtime errors | **0** |

The model rejected 66 inputs: 61 exceeded the source code-point limit and 5 contained unsupported characters. It did not silently truncate. Deterministic hybrid latency averaged 13.17 ms per input (median 12.25 ms, p95 24.00 ms). Successful neural calls averaged 541.02 ms (median 503.35 ms, p95 987.04 ms); across all attempts the mean was 519.26 ms (median 490.54 ms, p95 1,002.80 ms).

## Interpretation

The 100% Ukrainian rendering figure is a product/engineering coverage result, not evidence that every input has fully supported IPA. The deterministic segmental lane was complete on 661 sentences; the remaining inputs retain explicit provisional/unknown states or passthrough rather than being presented as confident IPA.

Only 14 rows received any syllable-level neural tone association (10 full and 4 partial), and 706 returned tonal outputs were unsupported by the current typed IPA inventory. The raw tonal IPA remains preserved separately, but the current adapter cannot safely associate most long sentence outputs with deterministic syllables. This is why the hybrid does not concatenate or vote across lanes.

No IPA gold is supplied for HVULao. These figures establish stress behavior, explicit rejection, coverage and runtime only; they do not establish which engine is more accurate. The separate 100-word MekongPhon held-out lexicon report is a dictionary-reference diagnostic and must not be conflated with this sentence-domain stress test.

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

- Successful workflow: [GitHub Actions run #42486829108](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42486829108)
- Code commit: `535d55e169ed518eb54113cb1980347e62240539`
- Aggregate artifact: [`hvulao-1k-three-engine-stress`, artifact ID 13620465276](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42486829108/artifacts/13620465276)
- Artifact SHA-256: `b0daf8011612c86d970d5e482d0f4f9a747c59a68fa58c4afb37c039026305a3`
- Python 3.12; CPU PyTorch 2.6.0; Transformers 4.49.0; Hugging Face Hub 0.29.3.
- Neural model: `byumatrixlab/lao-ipa-nontonal`, immutable revision `d6ea20cb73eaab8f3adc4eb044e61bdb9bef3f5b`, beam width 5, CPU.
- One hosted CPU run. Model loading and initial smoke inference are excluded from per-input latency.

## Results

| Metric | Vientiane rules | MekongPhon-reference rules | MekongPhon Neural |
|---|---:|---:|---:|
| Complete sentence outputs | 35 / 1,000 | 35 / 1,000 | 888 / 1,000 |
| Complete sentence coverage | 3.5% | 3.5% | 88.8% |
| Syllables with constructed IPA | 16,047 / 20,150 | 16,047 / 20,150 | Not measured |
| Rule-engine syllable IPA coverage | 79.64% | 79.64% | Not applicable |
| Mean inference time | 15.82 ms | 15.43 ms | 405.70 ms |
| Median inference time | 15.04 ms | 14.59 ms | 380.27 ms |
| p95 inference time | 30.25 ms | 30.05 ms | 732.66 ms |
| Unexpected runtime errors | 0 | 0 | 0 |

The deterministic engines construct IPA for 79.64% of the syllables they analyze, but a sentence is counted as complete only if every syllable has a constructed IPA result. This strict all-or-nothing sentence measure therefore yields 3.5% complete outputs. The benchmark intentionally does not turn a partially analyzed sentence into a complete-looking transcription.

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
| Aggregate sentence/syllable coverage and latency | DONE_VERIFIED | Artifact 13620465276; aggregate-only |
| Pairwise output disagreement | DONE_VERIFIED (comparative only) | Shared n=35; not accuracy |
| Broaden neural input acceptance safely | TODO / evidence-limited | Define and test Unicode/punctuation and long-input policy; no silent stripping/truncation |
| Improve deterministic sentence-level coverage | TODO / evidence-limited | Analyze unsupported categories with primary Lao orthography/phonology evidence and regression cases; do not guess |
| Independent adjudicated IPA gold | BLOCKED | Requires qualified independent annotation/adjudication; current count 0 |
| Production linguistic acceptance | BLOCKED | No gold IPA accuracy evidence or qualified specialist sign-off |

## Readiness

This benchmark is engineering-verified and reproducible. It shows the neural wrapper has much higher full-sentence coverage on this dataset, while deterministic rules remain conservative. The repository remains a research prototype, not independently accuracy-validated or production/release-ready.

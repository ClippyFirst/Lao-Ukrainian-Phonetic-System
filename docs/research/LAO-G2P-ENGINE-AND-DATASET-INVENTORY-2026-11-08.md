# Lao G2P engine and dataset inventory — 2026-11-08

## Scope and scoring contract

This inventory extends the existing ClippyFirst benchmark; it does not replace the production engine or promote any external engine.

- Lexical comparison source: [MekongPhon](https://github.com/byu-matrix-lab/MekongPhon), pinned dataset revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`, 100 held-out rows in `data/splits/lao_eval.csv`.
- Dataset SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`; the benchmark workflow verifies the immutable revision and records the actual SHA-256.
- Segmental reference: `pron_no_tones`; tonal reference: `pron_with_tones`. NFC normalization and outer-whitespace trimming only; no silent tone, length, or tie-bar normalization.
- Accuracy metrics accept only typed `SUPPORTED` or `UNCERTAIN` IPA. `PROVISIONAL` grapheme hints are **excluded** from IPA CER/exact-match scoring and counted separately in rendering coverage. A unit can therefore render in Ukrainian without being counted as verified IPA.
- All 100-row figures below are dictionary-seeded source concordance, **not independent expert accuracy**. Independent expert-adjudicated Lao IPA gold in this repository remains 0.

## Same-set engine comparison

| Engine | Segmental exact / CER | Segmental coverage | Tonal exact / CER | Interpretation |
|---|---:|---:|---:|---|
| ClippyFirst hybrid (current default) | 85/100 · 14.45% | 91% typed IPA | 23/100 · 34.06% native contour; 66/100 · 24.28% after evaluation-only Mekong contour conversion | 100% Ukrainian rendering; 9 provisional IPA-hint units are not scored as IPA |
| MekongPhon-reference deterministic rules profile | 90/100 · 6.64% | 97% typed IPA | Not scored in this segmental profile artifact | 90% Ukrainian rendering; no provisional fallback |
| Vientiane baseline rules profile | 69/100 · 11.46% | 97% typed IPA | Not scored in this segmental profile artifact | 95% Ukrainian rendering |
| MekongPhon Neural | 82/100 · 6.64% | 100% | 74/100 · 8.29% | Best full-coverage segmental and tonal concordance on this reference split |
| Lao2IPA 1.0.0 | 68/100 · 8.97% | 100% | 56/100 · 11.97% | Fast, broad-output baseline |
| Epitran 1.35.3 (`lao-Laoo`) | 71/100 · 10.96% | 100% | 4/100 · 36.94% | Segmental baseline; tonal output is not competitive on this convention |
| orthography2ipa (`lo` spec; upstream commit `32b66b0b1a4b66f7267790d7ec1f346460f8d814`) | 32/100 · 19.60% | 100% | 2/100 · 37.51% | Negative-control baseline; high output coverage does not imply good IPA |
| LanguageNet Phonetisaurus Lao FST | 0/100 · 78.90% | 100% | Not available | Model loaded successfully; very poor concordance on this split; no tone evaluation |
| Goruut runtime | 3–6/100 exact on all three repeats across three exact-head runs; 9–10/100 exact on at least one repeat; 8–12 unstable inputs | 81/100 responses; only 47/100 complete source coverage | Not scored | Runtime is nondeterministic/incomplete; not a production candidate on this evidence |

### ClippyFirst rendering versus IPA coverage

The current hybrid rendered all 100/100 inputs and all 169/169 analyzed units in Ukrainian. Of those units, 159 had supported IPA, 1 had explicitly uncertain IPA, and 9 were provisional grapheme hints; 9 units retained unknown markers. The separate MekongPhon-reference rules profile rendered 90/100 inputs (159/169 units); the Vientiane baseline rendered 95/100 inputs (164/169 units). Thus:

- Ukrainian rendering coverage: 100%.
- Typed IPA coverage: 91% of words in the 100-word comparison.
- Provisional hints are useful fallbacks, not confirmed phonological analyses.

The earlier 90/100 exact, 97% IPA-coverage figure in the 2026-11-07 report was attributed to the hybrid but was not a valid hybrid score. The confidence-gated rerun shows that 90/100, 6.64% CER and 97% IPA coverage belong to the separate MekongPhon-reference rules profile, which renders 90% of inputs. The hybrid is 85/100 exact, 14.45% CER and 91% typed IPA coverage, while rendering 100% of inputs through provisional hints. The legacy helper could count provisional preview values as accepted IPA; the shared benchmark contract and regression test now gate scores on `SUPPORTED` / `UNCERTAIN` only.

### Tone-category diagnostics

- ClippyFirst: 65/80 exact word-level category sequences; 102/120 reference categories covered; 18 unresolved categories; 10 word-length mismatches. Category error rate 3.92% on the 102 covered categories.
- Lao2IPA: 56/64 exact sequences; 81/93 categories covered; 12 unresolved; zero errors on covered categories.
- MekongPhon Neural: 66/69 exact sequences; 105/105 categories covered; 3 errors (2.86%).

These are conditional on segmental-exact alignment and parseable reference contours; they are not whole-language tone accuracy.

### Latency

Single hosted CPU run, model loading excluded where applicable:

| Engine | Segmental mean | Tonal mean |
|---|---:|---:|
| ClippyFirst | 1.292 ms | 1.292 ms |
| Lao2IPA 1.0.0 | 0.007 ms | 0.014 ms |
| MekongPhon Neural | 32.017 ms | 37.910 ms |
| Epitran | 0.022 ms | 0.020 ms |
| orthography2ipa | 1.104 ms | 1.104 ms |

Phonetisaurus timing includes model download and Docker startup and is not comparable. These are single-run diagnostics, not stable performance guarantees.

## HVULao 1k sentence-domain stress test

Pinned split: `HaHVU/HVULao_NLP` revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`, `Datatest1k/testorgin1000.txt`, 1,000 sentences, Git blob SHA-1 `947448807484bb994877ae5d32cba1cfdd5e2d9b`. This corpus has no IPA reference; the following are completeness and runtime metrics, not accuracy.

| Engine/profile | IPA-complete sentences | Ukrainian rendering | Syllable IPA coverage | Mean latency |
|---|---:|---:|---:|---:|
| Vientiane rules | 676/1,000 · 67.6% | 625/1,000 · 62.5% | 97.85% | 9.12 ms |
| MekongPhon-reference rules | 676/1,000 · 67.6% | 337/1,000 · 33.7% | 97.85% | 8.66 ms |
| ClippyFirst hybrid | 341/1,000 · 34.1% | **1,000/1,000 · 100%** | 94.14% | 8.87 ms |
| MekongPhon Neural | 934/1,000 · 93.4% | Not applicable (IPA-only) | Not reported in this stress harness | 241.42 ms per successful sentence |

The neural model rejected 66 rows (61 source-codepoint-limit, 5 unsupported-character). The hybrid rendered all 21,680 analyzed units; 1,025 units were provisional hints. Pairwise disagreement on 332 shared complete sentences: Vientiane vs MekongPhon-reference 7.39% CER; MekongPhon-reference vs Neural 11.78%; Hybrid vs Neural 11.78%; MekongPhon-reference vs Hybrid 0.00%. Disagreement does not identify which output is correct.

The older 66.9% hybrid IPA-complete sentence figure is superseded: it counted provisional preview values as accepted IPA. The confidence-gated rerun gives 34.1% IPA-complete sentences while preserving 100% Ukrainian rendering. This is the intended distinction between a readable fallback and a fully supported phonetic analysis.

## Additional engines and exclusions

- [Epitran](https://github.com/dmort27/epitran) contains a Lao mapping, but upstream issue [#186](https://github.com/dmort27/epitran/issues/186) documents a Lao coda/diphthong problem and issue [#180](https://github.com/dmort27/epitran/issues/180) concerns tone handling. Our same-split test confirms that tonal output is weak relative to the reference convention.
- [orthography2ipa](https://github.com/TigreGotico/orthography2ipa) includes a Lao `lo` spec. Its upstream Lao scoreboard reports 99.3% coverage but PER 72.25%; the same-set run here also shows weak concordance. Treat it as a negative control, not a reference.
- [LanguageNet G2P / Phonetisaurus](https://github.com/uiuc-sst/g2ps) contains a Lao FST. The pinned FST was run ephemerally in a pinned container; the model and per-item predictions were not committed. Repository-level licensing does not establish rights to redistribute any underlying Appen/Babel-derived model assets; keep test-only unless rights are confirmed.
- [Goruut](https://github.com/neurlang/goruut) was re-run against the same held-out set with three repeats. It returned 81 outputs, but only 47 had complete source coverage; 12 inputs were unstable across repeats. Its Lao asset warning reports a missing `weights9` asset. The related [neurlang Lao lexicon](https://github.com/neurlang/dataset) is not independent gold for Goruut and its Lao-specific provenance/licensing is not sufficiently clear for import.
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md) has no Lao voice entry in its current language list, so it is not a runnable Lao G2P comparator.
- CLDR Lao–Latin transliteration is orthographic transliteration, not pronunciation-to-IPA G2P; it remains a separate route and is not scored as a phonetic engine.

## Dataset inventory and fitness

| Resource | What it provides | License / access | Best use and limitations |
|---|---|---|---|
| [MekongPhon](https://github.com/byu-matrix-lab/MekongPhon) | About 367k Lao orthography–IPA pairs plus published tonal/non-tonal neural models | Public project data/model release; use the pinned repository revision | Best currently available IPA reference resource. The 100-row split is dictionary-seeded, not independent expert gold; do not conflate it with the paper's larger held-out evaluation. |
| [FLEURS](https://huggingface.co/datasets/google/fleurs) | Lao audio and text in a 102-language parallel speech corpus (about 2,009 parallel sentences per language) | CC-BY-4.0 | Best next source for acoustic validation and creation of a blinded expert IPA subset. Audio/text are not IPA labels. |
| [Mozilla Common Voice 27.0](https://commonvoice.mozilla.org/en/datasets) | Lao read speech; the current catalog lists 223 clips, 16 speakers and about 0.35 validated hours | CC0 | Useful small speaker/audio sanity set; too small and not IPA-annotated for a broad G2P gold benchmark. |
| [FLORES+](https://github.com/facebookresearch/flores) | Human-translated Lao text, including dev/devtest sentence sets | CC-BY-SA-4.0 | Sentence coverage and robustness stress; no audio or IPA gold. |
| [HPLT Lao](https://hplt-project.org/datasets/v2.0) | Cleaned Lao web text; v2.0 catalog lists about 232.58 MB, 262k words, 245 documents and 10.83k segments | CC0 for the listed v2.0 corpus | Large natural-text coverage/stress test; not a pronunciation reference. |
| [HVULao_NLP 1k](https://github.com/HaHVU/HVULao_NLP) | 1,000 raw Lao sentences, pinned revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568` | CC-BY-4.0 (Mendeley Data version 2) | Sentence-domain stress/coverage only; no IPA reference. |
| [IARPA Babel Lao language pack](https://catalog.ldc.upenn.edu/LDC2017S08) | About 207 hours of conversational/telephone speech and transcripts | LDC-controlled licensed access | Valuable acoustic corpus if licensed; transcripts are not IPA. |
| [Wiktionary Lao IPA](https://en.wiktionary.org/wiki/Category:Lao_terms_with_IPA_pronunciation) | Roughly 2,324 pages with IPA entries | Wikimedia terms and per-entry attribution apply | Secondary lexicon only. Many forms use the `lo-pron` template/rule generator; not independently adjudicated gold. |
| [neurlang/dataset Lao](https://github.com/neurlang/dataset/tree/master/lao) | A small IPA-like Lao lexicon (about 151 KB) | Lao-specific provenance/license not established | Do not use as independent gold: it is associated with the Goruut ecosystem and may share its lexical source. |

## Task ledger

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Add Epitran and orthography2ipa as pinned same-split comparators | DONE_VERIFIED | Aggregate-only CI artifact; package/spec revisions and hashes recorded |
| Add ephemeral LanguageNet Phonetisaurus FST probe | DONE_VERIFIED | Pinned model blob and container; 100/100 outputs, 0 exact, 78.90% CER; test-only |
| Re-run Goruut with repeatability/source-coverage diagnostics | DONE_VERIFIED | Final exact-head three-repeat artifact; 5 strict exact (preceding rerun: 3), 10 any-repeat exact, 47 complete-source outputs |
| Gate IPA accuracy against typed confidence status | DONE_VERIFIED | Shared helper and unit tests; provisional hints excluded from IPA accuracy and counted in rendering coverage |
| Run full 1k HVULao sentence stress benchmark with the same confidence gate | DONE_VERIFIED | 1,000 rows; hybrid 100% rendering, 34.1% IPA-complete sentences, 94.14% syllable IPA; Neural 93.4% complete sentences with 66 source-limit/unsupported rejections; no IPA gold |
| Build independent expert-adjudicated Lao IPA gold | BLOCKED / evidence-limited | No expert gold corpus exists in repository; FLEURS/Common Voice audio requires expert IPA annotation |
| Reuse neurlang/Appen-derived data as open gold or redistribute model assets | BLOCKED | Lao-specific source/license evidence insufficient; no import or redistribution |
| Promote any external engine to production | DEFERRED | No candidate meets both confidence, source coverage, and tone requirements; production hybrid remains unchanged |

## Reproducibility and artifacts

- All benchmarks run on dedicated branch `benchmark/additional-lao-g2p-20261108`, based on main `819c2528b1c726adfd3062be89084fedce7ad84d`.
- Main benchmark: [workflow run](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/mekongphon-three-engine-benchmark.yml).
- Deterministic profile and HVULao 1k stress results are uploaded as aggregate-only GitHub Actions artifacts; no raw dataset rows or prediction lists are committed.
- The dedicated PR remains draft because active open PRs #137–#148 touch overlapping benchmark workflows/scripts and canonical audit/handoff files. Do not merge this branch until those stacks are reconciled.

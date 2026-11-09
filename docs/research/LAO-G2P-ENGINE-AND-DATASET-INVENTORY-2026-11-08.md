# Lao G2P engine and dataset inventory — 2026-11-08

## Scope and scoring contract

This inventory extends the existing ClippyFirst benchmark; it does not replace the production engine or promote any external engine.

- Lexical comparison source: [MekongPhon](https://github.com/byu-matrix-lab/MekongPhon), pinned dataset revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`, 100 held-out rows in `data/splits/lao_eval.csv`.
- Dataset SHA-256: `5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241`; the benchmark workflow verifies the immutable revision and records the actual SHA-256.
- Segmental reference: `pron_no_tones`; tonal reference: `pron_with_tones`. NFC normalization and outer-whitespace trimming only; no silent tone, length, or tie-bar normalization.
- Accuracy metrics accept only typed `SUPPORTED` or `UNCERTAIN` IPA. `PROVISIONAL` grapheme hints are **excluded** from IPA CER/exact-match scoring and counted separately in rendering coverage. A unit can therefore render in Ukrainian without being counted as verified IPA.
- All 100-row figures below are dictionary-seeded source concordance, **not independent expert accuracy**. Independent expert-adjudicated Lao IPA gold in this repository remains 0.

## Published external baselines

- The [MekongPhon LREC 2026 paper](https://aclanthology.org/2026.lrec-1.129/) reports 367k Lao orthography–IPA pairs and under 2% CER on its own held-out evaluation. Its published result is not directly comparable to this repository's 100-row `lao_eval.csv` subset; the local 6.64% CER is a distinct evaluation slice and inference configuration.
- [Transphone's published supervised evaluation](https://github.com/xinjli/transphone/blob/main/doc/performance/supervised.md) lists Lao (`lao`) at PER 0.084 and phonological distance 0.046 on its Wiktionary-derived test split. On our distinct MekongPhon 100-row set, direct supervised-Lao inference scored 19/100 exact (24.25% CER) and 2/100 tonal exact (46.49% CER). This demonstrates substantial dataset/reference-convention sensitivity; neither score is independent expert accuracy.

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
| Transphone 1.5.3 supervised Lao G2P | 19/100 · 24.25% | 100% | 2/100 · 46.49% | Full output coverage but weak concordance on this MekongPhon split; zero runtime errors |
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
| ClippyFirst hybrid | 2.807 ms | 2.807 ms |
| Lao2IPA 1.0.0 | 0.010 ms | 0.020 ms |
| MekongPhon Neural | 66.866 ms | 81.786 ms |
| Epitran 1.35.3 | 0.030 ms | 0.028 ms |
| orthography2ipa | 1.517 ms | 1.517 ms |
| Transphone 1.5.3 | 86.299 ms | 86.299 ms |

Phonetisaurus timing includes model download and Docker startup and is not comparable. These are single-run diagnostics, not stable performance guarantees.

## HVULao 1k sentence-domain stress test

Pinned split: `HaHVU/HVULao_NLP` revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`, `Datatest1k/testorgin1000.txt`, 1,000 sentences, Git blob SHA-1 `947448807484bb994877ae5d32cba1cfdd5e2d9b`. This corpus has no IPA reference; the following are completeness and runtime metrics, not accuracy.

| Engine/profile | IPA-complete sentences | Ukrainian rendering | Syllable IPA coverage | Mean latency |
|---|---:|---:|---:|---:|
| Vientiane rules | 676/1,000 · 67.6% | 625/1,000 · 62.5% | 97.85% | 8.75 ms |
| MekongPhon-reference rules | 676/1,000 · 67.6% | 337/1,000 · 33.7% | 97.85% | 8.33 ms |
| ClippyFirst hybrid | 341/1,000 · 34.1% | **1,000/1,000 · 100%** | 94.14% | 8.52 ms |
| MekongPhon Neural | 934/1,000 · 93.4% | Not applicable (IPA-only) | Not reported in this stress harness | 234.93 ms per successful sentence |

The neural model rejected 66 rows (61 source-codepoint-limit, 5 unsupported-character). The hybrid rendered all 21,680 analyzed units; 1,025 units were provisional hints. Pairwise disagreement on 332 shared complete sentences: Vientiane vs MekongPhon-reference 7.39% CER; MekongPhon-reference vs Neural 11.78%; Hybrid vs Neural 11.78%; MekongPhon-reference vs Hybrid 0.00%. Disagreement does not identify which output is correct.

The older 66.9% hybrid IPA-complete sentence figure is superseded: it counted provisional preview values as accepted IPA. The confidence-gated rerun gives 34.1% IPA-complete sentences while preserving 100% Ukrainian rendering. This is the intended distinction between a readable fallback and a fully supported phonetic analysis.

## Additional engines and exclusions

- [Epitran](https://github.com/dmort27/epitran) contains a Lao mapping, but upstream issue [#186](https://github.com/dmort27/epitran/issues/186) documents a Lao coda/diphthong problem and issue [#180](https://github.com/dmort27/epitran/issues/180) concerns tone handling. Our same-split test confirms that tonal output is weak relative to the reference convention.
- [orthography2ipa](https://github.com/TigreGotico/orthography2ipa) includes a Lao `lo` spec. Its upstream Lao scoreboard reports 99.3% coverage but PER 72.25%; the same-set run here also shows weak concordance. Treat it as a negative control, not a reference.
- [Transphone](https://github.com/xinjli/transphone) explicitly lists Lao (`lao`) as a supervised language; its published test table reports PER 0.084 on a different Wiktionary-derived split. Our direct same-set run uses upstream code commit `7769dec083b90dab072fc7e4c592744592a35736`, release `v1.0/latest.tar.gz`, and checkpoint SHA-256 `03541a366ee44f01e35a138df731cd5be3ffd2016270dc787bd58040d8f45985`. The model was run ephemerally; the asset's separate redistribution terms were not established, so no weights are imported or redistributed. Same-set concordance is 19/100 exact (24.25% CER), showing that published results on a different split do not transfer automatically.
- [LanguageNet G2P / Phonetisaurus](https://github.com/uiuc-sst/g2ps) contains a Lao FST. The pinned FST was run ephemerally in a pinned container; the model and per-item predictions were not committed. Repository-level licensing does not establish rights to redistribute any underlying Appen/Babel-derived model assets; keep test-only unless rights are confirmed.
- [Goruut](https://github.com/neurlang/goruut) was re-run against the same held-out set with three repeats. It returned 81 outputs, but only 47 had complete source coverage; across three runs, 8–12 inputs were unstable; all runs retained 17 inputs with randomization metadata. Its Lao asset warning reports a missing `weights9` asset. The related [neurlang Lao lexicon](https://github.com/neurlang/dataset) is not independent gold for Goruut and its Lao-specific provenance/licensing is not sufficiently clear for import.
- [eSpeak NG](https://github.com/espeak-ng/espeak-ng/blob/master/docs/languages.md) has no Lao voice entry in its current language list, so it is not a runnable Lao G2P comparator.
- CLDR Lao–Latin transliteration is orthographic transliteration, not pronunciation-to-IPA G2P; it remains a separate route and is not scored as a phonetic engine.

## Dataset inventory and fitness

| Resource | What it provides | License / access | Best use and limitations |
|---|---|---|---|
| [MekongPhon](https://github.com/byu-matrix-lab/MekongPhon) | About 367k Lao orthography–IPA pairs plus published tonal/non-tonal neural models | Public project data/model release; use the pinned repository revision | Best currently available IPA reference resource. The 100-row split is dictionary-seeded, not independent expert gold; do not conflate it with the paper's larger held-out evaluation. |
| [FLEURS](https://huggingface.co/datasets/google/fleurs) | Lao audio and text in a 102-language parallel speech corpus (about 2,009 parallel sentences per language) | CC-BY-4.0 | Best next source for acoustic validation and creation of a blinded expert IPA subset. Audio/text are not IPA labels. |
| [Mozilla Common Voice 26.0 Lao](https://mozilladatacollective.com/datasets/cmqiaq1nn007znr07qss7tcb5) | 223 clips, 16 speakers, about 0.4 hours total / 0.35 validated (8.93 MB) | CC0-1.0 | Useful small speaker/audio sanity set; too small and not IPA-annotated for a broad G2P gold benchmark. The dataset card forbids re-hosting or re-sharing the corpus. |
| [FLORES+](https://github.com/facebookresearch/flores) | Human-translated Lao text, including dev/devtest sentence sets | CC-BY-SA-4.0 | Sentence coverage and robustness stress; no audio or IPA gold. |
| [HPLT Lao](https://hplt-project.org/datasets/v2.0) | v2.0 cleaned corpus: 232.58 MB, 190.37k documents, 19.93M words and 3.19M segments; deduplicated: 2.40 GB, 624.70k docs, 66.19M words and 9.36M segments | CC0 for the packaged corpus | Large natural-text coverage/stress test; not a pronunciation reference. |
| [HVULao_NLP 1k](https://github.com/HaHVU/HVULao_NLP) | 1,000 raw Lao sentences, pinned revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568` | CC-BY-4.0 (Mendeley Data version 2) | Sentence-domain stress/coverage only; no IPA reference. |
| [IARPA Babel Lao language pack](https://catalog.ldc.upenn.edu/LDC2017S08) | About 207 hours of conversational/telephone speech and transcripts | LDC-controlled licensed access | Valuable acoustic corpus if licensed; transcripts are not IPA. |
| [Wiktionary Lao IPA](https://en.wiktionary.org/wiki/Category:Lao_terms_with_IPA_pronunciation) | Roughly 2,324 pages with IPA entries | Wikimedia terms and per-entry attribution apply | Secondary lexicon only. Many forms use the `lo-pron` template/rule generator; not independently adjudicated gold. |
| [neurlang/dataset Lao](https://github.com/neurlang/dataset/tree/master/lao) | A small IPA-like Lao lexicon (about 151 KB) | Lao-specific provenance/license not established | Do not use as independent gold: it is associated with the Goruut ecosystem and may share its lexical source. |

## Task ledger

| Work item | Status | Evidence / remaining acceptance |
|---|---|---|
| Add Epitran and orthography2ipa as pinned same-split comparators | DONE_VERIFIED | Aggregate-only CI artifact; package/spec revisions and hashes recorded |
| Add ephemeral LanguageNet Phonetisaurus FST probe | DONE_VERIFIED | Pinned model blob and container; 100/100 outputs, 0 exact, 78.90% CER; test-only |
| Re-run Goruut with repeatability/source-coverage diagnostics | DONE_VERIFIED | Three exact-head three-repeat artifacts; 3–6 strict exact, 9–10 any-repeat exact, 47 complete-source outputs; latest run 6 strict / 9 any-repeat / 8 unstable |
| Gate IPA accuracy against typed confidence status | DONE_VERIFIED | Shared helper and unit tests; provisional hints excluded from IPA accuracy and counted in rendering coverage |
| Run full 1k HVULao sentence stress benchmark with the same confidence gate | DONE_VERIFIED | 1,000 rows; hybrid 100% rendering, 34.1% IPA-complete sentences, 94.14% syllable IPA; Neural 93.4% complete sentences with 66 source-limit/unsupported rejections; no IPA gold |
| Build independent expert-adjudicated Lao IPA gold | BLOCKED / evidence-limited | No expert gold corpus exists in repository; FLEURS/Common Voice audio requires expert IPA annotation |
| Reuse neurlang/Appen-derived data as open gold or redistribute model assets | BLOCKED | Lao-specific source/license evidence insufficient; no import or redistribution |
| Promote any external engine to production | DEFERRED | No candidate meets both confidence, source coverage, and tone requirements; production hybrid remains unchanged |

## Reproducibility and artifacts

- All benchmarks run on dedicated branch `benchmark/additional-lao-g2p-20261108`, based on main `819c2528b1c726adfd3062be89084fedce7ad84d`.
- Main benchmark: [workflow run](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/workflows/mekongphon-three-engine-benchmark.yml).
- Deterministic profile and HVULao 1k stress results are uploaded as aggregate-only GitHub Actions artifacts; no raw dataset rows or prediction lists are committed. Latest confidence-gated HVULao 1k run: [#42574809147](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42574809147), artifact [#13654703651](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42574809147/artifacts/13654703651).
- The dedicated PR remains draft because active open PRs #137–#148 touch overlapping benchmark workflows/scripts and canonical audit/handoff files. Do not merge this branch until those stacks are reconciled.

## Additional literature and protocol findings — 2026-11-09

### Graphoneme alignment is a real Lao G2P research candidate

Hansakunbuntheung & Thatphithakkul (O-COCOSDA 2016, DOI 10.1109/ICSDA.2016.7919010) evaluate unsupervised many-to-many graphoneme alignment on four Asian-language pronunciation dictionaries, including Lao. The abstract reports **91.28% Lao word accuracy** on that paper's own dictionary. Its method explicitly addresses cross-syllable and intra-syllable grapheme–phoneme alignment and implicit tone assignment, making it structurally relevant to Lao.

**Disposition: RESEARCH_CANDIDATE, not runnable baseline.** The accessible publication record does not establish the Lao dictionary size, exact train/test split, dialect, tone convention, data rights, released predictions or executable implementation. Do not compare 91.28% directly with the repository's MekongPhon 100-word results. Next acceptance: obtain full paper and cited dataset/code; recover exact evaluation protocol; reproduce on a rights-cleared split before adding an engine adapter.

### CharsiuG2P / multilingual ByT5 requires a support check

Zhu, Zhang & Jurgens (Interspeech 2022, DOI 10.48550/arXiv.2204.03067) describe multilingual ByT5 G2P and release code/models. At inspected upstream commit `0c929390759fb94f8ecdfc05cc0bc5f2ff2dc0f4`, the repository contains `sources/info/wikipron/lao_laoo_broad_info.txt`, which points to CUNY-CL WikiPron's Lao broad-IPA TSV and declares Apache-2.0 for that source metadata.

A recursive inspection of the same upstream commit's complete tree found no Lao file under `data/train`, `data/dev` or `data/test`, and no Lao entry in the checked-in split inventories; Khmer is present. Thus CharsiuG2P is **not a trained/evaluated Lao G2P baseline on this revision** and must not be counted as a runnable Lao baseline. A future zero-shot output, if inference permits, is exploratory only.

### SIGMORPHON is a protocol reference, not a Lao benchmark

SIGMORPHON 2022 defines three resource settings: cross-lingual transfer (100 target training examples plus 1,000 donor-language examples), very-low-resource (100 target examples), and low-resource (1,000 target examples), using a common target test set. The official task's published languages do not provide a Lao target evaluation. The 2021 task paper is likewise a methodological source, not a Lao gold set.

A Lao adaptation must be named **SIGMORPHON-inspired**, never official SIGMORPHON. It requires a fixed held-out Lao test split, nested 100/1,000 target training subsets, explicit donor-language rationale, immutable data/model revisions and separate strict/convention-normalized IPA metrics. Thai transfer is a distinct experiment: typological relatedness does not make Thai graphemes identical to Lao graphemes.

### New evidence-gated task ledger

| Task | Status | Acceptance / blocker |
|---|---|---|
| Register graphoneme alignment paper and reported Lao result | DONE_VERIFIED (source registry) | Source and claim IDs `SRC-HANSAKUNBUNTHEUNG-GRAPHONEME-2016`, `CLM-LAO-GRAPHONEME-ALIGNMENT-RESEARCH); 91.28% remains paper-reported, not reproduced |
| Register SIGMORPHON 2021/2022 protocol sources | DONE_VERIFIED (source registry) | Source IDs `SRC-SIGMORPHON-2021-G2P`, `SRC-SIGMORPHON-2022-G2P`; no official Lao test set |
| Register CharsiuG2P multilingual ByT5 candidate | DONE_VERIFIED (source registry) | Source/claim record captures Lao WikiPron metadata; actual model-language support remains BLOCKED pending manifest/model inspection |
| Implement graphoneme candidate | BLOCKED / evidence-limited | Full paper, original Lao dictionary, rights and runnable implementation not yet verified |
| Add CharsiuG2P as same-split benchmark engine | BLOCKED / evidence-limited | Need proof Lao is supported by the selected model/checkpoint and a reproducible inference route |
| Create SIGMORPHON-inspired Lao 100/1,000/transfer experiment | TODO / design-gated | Requires a frozen test set independent of tuning and an auditable nested split; transfer donor must be justified |

## Written-evidence continuation — no-audio improvement path (2026-11-09)

The user cannot provide audio. This does not prevent useful engineering work, but it changes the acceptance contract: improve the deterministic hybrid using inspectable written evidence, and do not claim acoustic or independently adjudicated accuracy.

### New written sources and what they can support

- **Enfield (2007), *A Grammar of Lao*, §3.1, pp. 33–34**: gives the C0V0C1V1V2C2 word template. Optional minor C0V0 has no distinctive tone independent of its major syllable; in Enfield's described variety V0 is short /a, i, u/ with no length contrast, and C0 is a restricted onset subset. However, the preface describes everyday informal speech from semi-rural villagers, not a narrowly defined standard Vientiane sample. This is strong phonological structure evidence but must not be copied wholesale into the Vientiane-specific tone engine.
- **Ueda (1994)**: central Vientiane-specific description reports five tones and one exceptional non-final open /a/ minor syllable that is unstressed and tone-neutral. The current implementation's narrow potential-minor-open-A warning is consistent with this bounded statement; do not expand it to all /a i u/ merely from Enfield's distinct sample.
- **Osatananda (1997), *Tone in Vientiane Lao***: analyzes one Vientiane variety with five lexical tones, final stress and underlying lexical tone on every syllable, rather than tone mechanically derived by grapheme-class rules. This is a serious alternative phonological analysis. It means the current orthographic tone table should be described as a deterministic spelling-to-tone prediction convention/profile, not a complete universal account of lexical tone. It supports conservative uncertainty and lexical overrides where independently documented; it does not justify changing every existing rule without an aligned lexicon.
- **Phissamay et al. (2007), *Syllabification of Lao Script for Line Breaking***: documents a rule-based orthographic syllable segmentation procedure and reports more than 98% results, but the accessible paper does not provide enough split/evaluation detail for reproduction. It is about syllable boundaries for line breaking, not lexical word segmentation or IPA. LaoNLP implements a related regex method based on this paper.
- **LaoNLP 1.3.0**: package code is Apache-2.0. Its syllable tokenizer publishes the exact example 'ພາສາລາວໃນປັດຈຸບັນ' → 'ພາ | ສາ | ລາວ | ໃນ | ປັດ | ຈຸ | ບັນ'; this is now a regression fixture for segmentation parity, not pronunciation gold. The bundled lao-eng-dictionary.csv has a separate MIT license notice from the E-Government Center, Ministry of Posts and Telecommunications of Laos. It is a lexical resource, not an IPA dictionary.
- **Kaikki/Wiktextract Lao dictionary**: the current page reports a 5.2 MB machine-readable Lao dictionary extracted from the 2026-10-01 English Wiktionary dump. It contains pronunciation fields, but Wiktextract explicitly expands programmatic Lua pronunciation modules as well as manually entered pronunciations. Therefore it is a secondary diagnostic source, not a uniform independent IPA gold set. Underlying Wiktionary content is CC BY-SA 4.0/GFDL; attribution and share-alike obligations apply to redistributed derivative material.
- **Wiktionary lo-pron**: a Lao pronunciation/rhyme/hyphenation generator. Compare its behavior only as a second implementation; do not treat agreement with it as independent evidence because it is rule-generated.

### Practical changes made

- Added source records for Osatananda, Phissamay et al., LaoNLP, the separately licensed LaoNLP dictionary, Kaikki/Wiktextract, and Wiktionary lo-pron.
- Added evidence claims that explicitly preserve dialect, analysis, and provenance boundaries.
- Added the LaoNLP-published segmentation example to tests/test_multisyllable_segmentation.py. The test requires both the parser segmentation and full analysis to retain all seven syllables with IPA output. It is a structural parity fixture only.
- No new IPA values, tone categories, Ukrainian outputs, or lexical pronunciations were invented or copied from non-reusable dictionaries.

### Next useful text-only engineering steps

1. Run the new published-example regression against Python and browser implementations; fix only reproducible segmentation defects.
2. Inspect the MIT LaoNLP dictionary as a candidate lexical word-boundary resource after verifying its file-specific license and schema. Do not treat its headwords as pronunciation records.
3. Extract a small Wiktionary/Kaikki diagnostic sample and classify each IPA record by provenance: explicit human IPA vs lo-pron template-generated vs other. Keep these as secondary concordance only, not gold.
4. Add lexical exceptions only when the spelling-to-pronunciation mapping is explicitly supported by a reusable source and its dialect/variant is known.
5. Keep phrase-level tone sandhi, stress and reduced-minor-syllable behavior analysis-dependent unless the written source gives an exact, testable condition.

### Methodological boundary

No-audio does not mean no verification. We can verify orthographic coverage, syllable segmentation, deterministic reproducibility, consistency against multiple written descriptions, and exact concordance with attributed written lexical records. We cannot honestly claim acoustic fidelity, prosodic naturalness, or independent phonetic accuracy from those checks alone.

### Additional dialect, stress and lexical-history evidence

The completed Undermind review surfaced several useful written studies:

- **Lew (2014), DOI 10.1080/17586801.2013.846843**: analyzes Lao grapheme–phoneme correspondences and orthographic structure, while stressing that Lao dialects differ in lexicon, vowels and especially tones. Supports the IPA-first graphemic architecture but also explicit dialect scope.
- **Lao Language Specific Peculiarities — Dialects (2015)**: reports that ໃ and ໄ are pronounced the same in Vientiane but differently in Luang Prabang. The existing Vientiane vowel registry maps both spellings to the same /ai/ nucleus while retaining distinct source graphemes; this is consistent with that written profile. Do not reuse this equivalence for Luang Prabang.
- **Enfield (2020), “Word in Lao,” DOI 10.1093/oso/9780198865681.003.0007**: describes phonological feet, each with one stressed tone-bearing syllable and one or more dependent unstressed syllables. Grammatical-word boundaries do not always coincide with phonological-word boundaries. This strengthens the case for keeping phrase/word-level stress and dependent-syllable interpretation separate from syllable parsing.
- **Davis (2015), “The Story of Lao r”**: describes historical /r/ loss, /r/ becoming /h/ in some conditions and /l/ elsewhere, plus cluster loss and loanword complications. Keep ຣ as analysis-dependent/lexeme-sensitive where the modern reading cannot be resolved from the grapheme alone; do not impose a universal unconditional mapping.
- **Sengsoulin (2009), “Pali and Sanskrit words in Lao language”**: supports a distinct historical/orthographic loanword layer. Modern native-Lao tone and coda rules should not be mechanically applied to Indic etymological spelling without a word-specific modern reading.
- **Yanagimura (2011), “Contextual Tonal Variations in Vientiane Lao”**: studies all 25 bitonal sequences from five lexical tones and reports stronger carryover than anticipatory effects in F0 realization. The engine's isolated lexical tone label is not a full phrase-level phonetic contour; keep contextual realization outside the current spelling-only contract.
- **WikiPron (Lee et al., 2020)**: a Wiktionary-derived multilingual pronunciation resource. Lao-specific coverage, annotation provenance and dialect still need verification; do not count it as a Lao baseline or gold set yet.

These sources reinforce three conservative implementation principles: (1) maintain a declared Vientiane profile; (2) preserve lexeme-level uncertainty for historical and Indic loan spellings; and (3) do not infer phrase-level stress or contextual tone contours from isolated orthographic syllables alone.

### LaoNLP lexical resources: exact scope and access boundary

- Inspected `laonlp/corpus/Lao-Dictionary.txt` from LaoNLP. Its header attributes the 2013 word list to Brian Eugene Wilson and Robert Martin Campbell, with thanks to Arlyta Keosamone and Bualong Nyoukmai. It contains a BSD-style redistribution notice, is about 77 KB, and says it was created for word wrapping with compound words mostly reduced to their component parts. It contains orthographic items, names and borrowed forms but no IPA. Treat it as a candidate lexical hint list, not a complete word-boundary gold set.
- Separately, `laonlp/corpus/lao-eng-dictionary.csv` has its own MIT notice from the E-Government Center, Ministry of Posts and Telecommunications of Laos. The GitHub contents endpoint does not expose the 2.73 MB file body in this connector session, and the connected Firecrawl account had no credits for the raw-file inspection. Its header/schema/rows therefore remain uninspected; do not integrate it or claim its fields until a reproducible fetch is available.
- The two resources have different origins and licenses; neither license should be inferred from the LaoNLP package's Apache-2.0 code license.


### Soft lexical-boundary hint prototype — 2026-11-09

The upstream BSD word list was fetched in full (77,274 UTF-8 characters; 11,208 non-comment entries in this pinned response; upstream blob SHA-1 `ca5346a1971a7712ac3c50988140c376859174e3`). Its original attribution and BSD-style notice are retained verbatim in `data/lao/lexical-hints/Lao-Dictionary.txt`.

Added an optional diagnostic-only matcher in `src/lao_ukrainian/lexical_hints.py`. It joins contiguous syllable spans and returns every matching orthographic entry with zero-based, end-exclusive offsets. It retains overlapping alternatives, labels them `SOFT_HINT_ONLY`, and never chooses word boundaries. It is not imported by the production parser, IPA/G2P path, target adapter, or browser bundle.

The source list's word-wrapping purpose and compound reduction make it unsuitable as lexical segmentation gold. The diagnostic can expose candidate spans for later review, but cannot establish that a listed string is a lexical word in a given context. Its inclusion is permitted under the retained BSD-style notice. The separate 2.73 MB MIT CSV remains excluded until a complete reproducible fetch and schema inspection are available.

Acceptance: unit tests prove multi-match overlap retention, default exclusion of single-syllable entries, and no mutation of the syllable sequence. These are software-contract tests, not linguistic accuracy measurements.


### Exact-head verification status for the lexical-hint prototype

The lexical-hint helper and tests are committed, but the GitHub connector did not trigger Actions after updating the branch ref. Five isolated behavioral checks passed; this is not repository CI. The implementation remains PARTIAL until the full Verify workflow passes on the branch head. Do not transfer the previous branch-head test counts to this commit.

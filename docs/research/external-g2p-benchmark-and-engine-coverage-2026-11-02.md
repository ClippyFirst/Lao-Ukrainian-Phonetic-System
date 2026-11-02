# External G2P benchmarks and engine coverage audit — 2026-11-02

## Scope and interpretation

This is a source-backed research audit, not an accuracy claim for this repository. Published benchmarks are not directly comparable unless their variety, text normalization, IPA convention, segmentation, tone policy, test split, and scoring normalization match. No external corpus has been copied into project gold. No benchmark score is assigned to this repository.

## Relevant benchmark evidence

### MekongPhon (LREC 2026)

Shurtz, Richardson & Richardson, “MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer”, LREC 2026, pp. 1650–1658, DOI 10.63317/4bb9rvdshu4z.

The paper abstract reports 367,000 Lao orthographic–IPA pairs and a Transformer result below 2% character error rate on held-out test sets. It also reports that linguistically informed Lao/Khmer transliteration tools outperform Epitran by 6–71 CER points, trading some accuracy for speed. The abstract does not establish that the benchmark's Lao variety, IPA convention, segmentation policy, or tone annotation exactly matches this repository's Vientiane-oriented target profile. Treat the result as a strong external baseline, not as a transferable score.

Reference: https://aclanthology.org/2026.lrec-1.129/

## Engine coverage audit

| Engine | Declared Lao support | What is established | Important gaps / cautions |
|---|---|---|---|
| Epitran | `lao-Laoo`, `lao-Laoo-prereform` | Package publishes a Lao-script mapping. | Package support is not proof of dialect-aware Vientiane phonology, tone correctness, vowel quantity, syllable boundaries, or exact IPA convention. Its `tones` option defaults to false; default output can therefore discard tone marks. |
| Goruut | Lao | README lists Lao and advertises IPA output and five tone-level symbols. | README says syllable tokens are not supported and tie bars are not supported. Five generic tone levels do not by themselves prove correct Lao lexical tone categories/contours or live/dead-conditioned tone assignment. |
| MekongPhon models/tools | Lao | Dedicated Lao orthography–IPA resource and reported held-out CER benchmark. | Must verify the exact model release, profile, tokenization, tone/length policy, and test protocol before integrating. Benchmark CER is not an adjudicated score for Ukrainian adaptation. |

Sources: https://pypi.org/project/epitran/ ; https://github.com/neurlang/goruut ; https://aclanthology.org/2026.lrec-1.129/

## Feature coverage required by this project

A usable comparator must be tested for: onset class and aspiration; consonant clusters and high-class nasal/sonorant ligatures; vowel identity and quantity; coda class; live/dead syllable structure; Vientiane tone category and contour; syllable boundaries; IPA segment identity and tie-bar conventions; uncertainty/unsupported forms. Tone and length must be scored separately from segmental CER.

## Current assessment

- Epitran: useful baseline comparator; **PARTIAL**, not a source of gold. Explicitly set and record tone configuration in any experiment.
- Goruut: useful second comparator; **PARTIAL**, not proven complete for the project's tonal/structural contract.
- MekongPhon: **PRIORITY BENCHMARK / CANDIDATE BASELINE**. Its results are highly relevant, but require a profile-compatibility audit before model adoption.
- This repository: no empirical accuracy claim; its adjudicated IPA gold remains governed by the existing blind collection protocol.

## Next reproducible experiment

1. Obtain the official MekongPhon release and record immutable revision, model checksum, data provenance, licence/terms, and exact inference command.
2. Freeze a held-out Lao subset by lexical group and variety; do not mix training data or duplicate entries across splits.
3. Normalize Unicode only under a documented policy; preserve tone, length, syllable boundaries, and tie bars in the raw prediction.
4. Run Epitran with explicit tone settings, Goruut with pinned version, and the MekongPhon baseline on identical inputs.
5. Report segmental CER, tone error, vowel-length error, syllable-boundary F1, exact IPA match, unsupported/error rate, and runtime separately.
6. Have qualified annotators adjudicate mismatches. Never convert engine output into gold labels.

## Evidence limitations

The cited MekongPhon abstract gives corpus size and aggregate CER but not enough detail to assert complete coverage of this repository's target profile. The Epitran and Goruut language lists are vendor/project declarations, not independent linguistic evaluations. No new runtime benchmark was executed in this documentation-only audit.

## Hosted raw-output diagnostics on the audit branch — 2026-11-02

Exact branch-head runs (documentation commits included):
- Project verification: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41409083919 — SUCCESS.
- Pinned `lao2ipa==1.0.0` comparison: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41409083914 — SUCCESS as a diagnostic job. On 37 engineering fixtures, project fixture matches=37/37, external fixture matches=0/37, exact agreement between implementations=0/37. Heuristic decomposition: 31 tone-suffix-only, 2 diphthong offglide convention, 4 segmental/vowel-sequence differences. Removing tone letters yields 31/37 (83.8%) diagnostic-only agreement; this is emphatically not an accuracy score because Lao tone is contrastive. Independent gold=0; accuracy=null.
- Goruut source snapshot `b224bde` raw-output probe: https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41409083978 — SUCCESS as a raw-output collection job. On the source-attested 100-row diagnostic, exact matches=4/100 (4%), successful outputs=81, failed outputs=19, complete source coverage=47, partial=34, unknown=19, unphonemized fragments=2; 14 outputs were unstable in the engineering probe. A notation-normalized diagnostic also yielded 4/100. The run logged a missing `weights9.bin.zlib` file; this must be resolved before treating the runtime as a stable comparator.

All comparisons are explicitly `NOT_SCORED_NO_INDEPENDENT_GOLD`. The 37-case `lao2ipa` set is an engineering fixture, not a blind expert gold set. These results establish that the current external engines do not yet demonstrate adequate agreement/coverage for this project's needs; they do not establish the project's own accuracy or which output is correct.


## Upstream Goruut asset inventory follow-up — 2026-11-02

The warning for `weights9.bin.zlib` was checked against the exact Goruut source snapshot used in the optional probes (`b224bde02151f8f86d0fe260804e4ca743bda620`). The upstream Git tree has no such file in the language-specific dictionary directories: `dicts/lao/`, `dicts/khmer/central/`, and `dicts/burmese/`. Each directory does contain earlier model assets (including the `weights7` and `weights8` files). The warning therefore reflects an asset absent from this pinned upstream snapshot, not a failed checkout of a file that exists in the repository. The probe still completed and returned raw outputs. The impact of this absent asset on ranking, coverage, or accuracy is not quantified; treat it as a model-bundle limitation and do not create substitute weights or infer a quality delta without upstream implementation evidence and a valid gold set.


## Additional published sequence-to-sequence baselines — 2026-11-02

The BYU MATRIX Lab publishes two separate 33.6M-parameter Lao-to-IPA checkpoints trained from MekongPhon:

- [`byumatrixlab/lao-ipa-tonal`](https://huggingface.co/byumatrixlab/lao-ipa-tonal) explicitly includes tone markers (model card reports best eval loss 0.5318 at checkpoint 4000, approximately six epochs).
- [`byumatrixlab/lao-ipa-nontonal`](https://huggingface.co/byumatrixlab/lao-ipa-nontonal) explicitly excludes tone markers (model card reports best eval loss 0.7419 at checkpoint 4000, approximately six epochs).

Both use a BERT encoder–decoder with separate character-level Lao and IPA tokenizers and a maximum sequence length of 128. The non-tonal checkpoint is structurally unsuitable as a complete comparator for a Vientiane Lao target that requires lexical tone. The tonal checkpoint is a priority comparator, but its presence of tone marks does not prove that its tone categories, contours, vowel quantity, coda conditioning, dialect, or IPA convention match this project's profile. The two reported evaluation losses are not comparable accuracy scores and are not transferred to this project.

The model cards point to MekongPhon as the training-data/code source. Before a reproducible run, pin each Hugging Face model revision and weight checksum, inspect the dataset split and profile, run identical inputs through both checkpoints, and report tone-bearing and segmental errors separately. Preserve raw outputs; do not use either model as gold.

**Assessment:** tonal checkpoint = PRIORITY BASELINE / NOT YET VERIFIED; non-tonal checkpoint = useful ablation only / INCOMPLETE FOR TONAL IPA. Neither changes the independent-gold count (0) or empirical accuracy (null).

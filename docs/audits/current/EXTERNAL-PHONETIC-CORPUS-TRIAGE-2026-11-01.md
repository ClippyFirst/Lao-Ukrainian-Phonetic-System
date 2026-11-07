# External phonetic corpus/source triage — Lao — 2026-11-01

## Candidate: MekongPhon (LREC 2026)

**Disposition (updated 2026-11-07): research use is in scope under the authors' explicit public-release statement; NOT independent gold and NOT imported as a product corpus or model-training set.** The paper reports 367,000 Lao orthography–IPA pairs and sub-2% CER on held-out data. It also reports a 1.3M Khmer set. These are paper-reported figures, not results independently reproduced by this repository.

- Paper: https://aclanthology.org/2026.lrec-1.129/
- Project: https://github.com/byu-matrix-lab/MekongPhon
- Inspected upstream main commit: `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Files include `data/lexicons/lao_lexicon.csv`, `data/splits/lao_train.csv`, `data/splits/lao_eval.csv`, and a 500-sentence qualitative sample.
- The project repository metadata has `license: null`; its tree has no LICENSE/COPYING file. The paper explicitly says all data, code and pretrained models are publicly released to support future research and development. We treat that statement as support for non-redistributive research use, not as a blanket formal license for redistribution, sublicensing or commercial reuse. The LREC proceedings license is separate from the corpus.
- The documented pipeline scrapes the SEAlang Lao dictionary, normalizes IPA tone marks, downloads OPUS parallel text, and applies a greedy lexicon transliterator. Sentences with out-of-lexicon tokens are filtered out. Thus the sentence IPA is dictionary-generated, not an independently hand-transcribed sentence-level reference.
- The committed split script uses `random.seed(1234)` and reserves only 100 lexicon lines for evaluation. This is a held-out lexical split, not evidence of independent expert adjudication or robust dialect-balanced coverage.
- The paper's “verified” claim is worth investigating, but the accessible project README/pipeline does not document annotator identities, adjudication protocol, dialect stratification, or data licensing at the per-entry level.

## Other candidate: Goruut

The source code is MIT, but the corresponding `neurlang/dataset/lao/` lexicon has no declared repository license, and no per-language rights statement was found. Its derived model assets remain blocked pending provenance/license clarification. See `docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md`.

## Full train-split diagnostic and rule-baseline comparison — 2026-11-07

The pinned train file has raw SHA-256 `2d0f68989009620980ced3386f11a640e6167404308eeb6a79efc52bc8e40ee0`. First complete run: [42386956616](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42386956616); aggregate artifact SHA-256 `1598ee5f23ea9bfdba6c4eacbb4f53cc377900565a91054d4b96c354c2dd24`.

- Segmental: 6,219 rows, 93.58% coverage, 3,885 exact matches (62.47% of the full denominator), full-denominator CER 16.70%.
- Tone categories: 4,152/8,761 covered (47.39%); 132/4,152 category disagreements (3.18%) on the covered segmental-exact subset; 616 category-length mismatches and 133 reference-alignment failures.
- 88 of the 132 disagreements are concentrated in two reference→engine pairs: 50 high-mid→low-rising and 38 low-falling→high-mid. MekongPhon's own deterministic baseline at the pinned revision maps high-class live unmarked syllables to low-rising and low-class short-dead unmarked syllables to high-mid, the same categories as ClippyFirst's corresponding rules. The seed-lexicon references therefore diverge from the corpus project's own rule baseline in these frequent contexts. This is evidence of reference/convention sensitivity, not proof of which transcription is correct.
- No tone rule was changed from these train-split labels. Keep the six previously flagged minor-syllable candidates and any new tonal disagreements pending qualified Vientiane review.
- The final diagnostic extension (exact source hash/duplicate guards, IPA-inventory-token edit profile and non-established-syllable filtering) passed [run 42388029325](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388029325) and full [Verify 42388033575](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42388033575) on code commit `3efc0ccb54887830157915e8b4b84ad9177e1720`. Artifact SHA-256: `a9cb3e0a98b3a47532871d170f14d38415be8c57d093af92f8b02f84ce9232b3`.
- IPA-inventory-token edit distance: 5,531/28,992 reference tokens (19.08% full-denominator token error rate). Leading substitutions: `aː→ə` 507, `j→i` 365, `w→ʋ` 327, `u→uː` 279, `o→w` 246, `i→iː` 237, `r→l` 171. These comparisons expose source-sensitive vowel, glide and approximant/rhotic conventions; they are not independent gold or evidence to change rules without a profile-specific primary source.
- The 100-row eval split remains separate and is not used for tuning.

## Current use boundaries — 2026-11-07

1. Use the pinned public corpus for research, error analysis and rule discovery; cite Shurtz et al. (2026) and record the exact upstream revision and file hash.
2. Use the 6,219-row train split only for development diagnostics. Keep the 100-row eval split separate for comparator reporting; do not tune on eval.
3. Do not promote any MekongPhon row to independent ClippyFirst gold. The source lexicon and generated sentence references remain external reference material, not blind adjudication.
4. Do not commit or re-host raw corpus rows, IPA references or per-item predictions. Obtain explicit component terms before mirroring, redistribution, sublicensing or commercial reuse.
5. Keep tone, vowel length, syllable boundaries and uncertainty intact. Do not normalize away tonal distinctions to improve agreement.

Current independent, project-owned, expert-adjudicated Lao gold remains 0. No MekongPhon/Goruut accuracy claim is added to this repository.


## Test-only Goruut runtime evaluation

Added an optional, test-only HTTP runtime probe for Goruut at pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620`. It explicitly enables `Lao` in Goruut's `BuiltinDictLanguages`, builds the upstream Go binary, starts the documented HTTP service and records every raw JSON response for source-engineering probes (including multiword/punctuation cases). `scripts/benchmark_goruut.py` records engine commit, language identifier, input SHA-256, raw response, token outputs and errors. It performs no IPA normalization and always reports `accuracy: null`, independent gold=0. Workflow: `.github/workflows/optional-goruut-runtime.yml`; artifact retention 30 days. Project fixtures are engineering probes, not adjudicated gold.

The earlier asset-license blocker applies to copying, redistribution and production integration. The owner has authorized use for testing only; therefore the optional CI probe may check out and execute the pinned upstream source transiently. It does not persist upstream assets, does not bundle them, and does not approve a production dependency. Linguistic gold and accuracy remain unestablished.


## Goruut runtime evidence update — 2026-11-01

The pinned Goruut runtime was executed, not merely inspected. Go 1.23.12, Lao explicitly enabled; 23 engineering probes yielded 18 usable outputs/5 empty; 100 MekongPhon eval rows yielded 81 usable outputs/19 empty. Strict NFC+outer-whitespace source-attested concordance was 8/100 (8%); heuristic diagnostic: 13 tone-only, 1 tone/length, 59 segmental/format, 19 no output. This is NOT accuracy or gold: MekongPhon sentence IPA is lexicon-generated and its eval is not independent expert adjudication. Server log repeatedly reports missing `weights9.bin.zlib`. Do not promote. Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.

Testing-only owner authorization was used to execute the pinned upstream source in ephemeral CI. No external asset was copied into the repository or production artifact. Full report: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.


## Repeatability findings — 2026-11-01

Three-repeat re-evaluation supersedes one-shot counts: engineering probes 18/23 usable, with 7/18 usable outputs unstable across repetitions; MekongPhon 81/100 usable, with 13/81 unstable; only 4/100 source-attested rows matched exactly across all three repetitions (10/100 matched at least once). Example `ຄົນ` alternated between `kʰon˩˨` and `kʰon˧˥`. This demonstrates a serious tone/reproducibility defect. It remains source-attested concordance, not accuracy. See runtime evaluation audit.

The three-repeat raw outputs are preserved in workflow artifacts and summarized in `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`. Do not treat these results as gold or as a production approval.


## Cross-engine comparison update

Additional optional lao2ipa 1.0.0 run on the 37-case engineering fixture: 0/37 exact string agreements, 31 tone-suffix-only, 2 diphthong-offglide, 4 segmental/vowel-sequence differences; zero runtime errors. The local engine matched its own fixture 37/37, but that fixture is not gold. This points to a major tone-convention difference and six cases requiring segmental review, not a winner. Latest Goruut three-repeat: 18/23 engineering outputs, 12 stable/6 unstable; 81/100 MekongPhon outputs, 70 stable/11 unstable; 5/100 all-repeat source-attested exact/notation matches, 10/100 at least one repeat. Accuracy remains null.


## MekongPhon primary-artifact and rights audit — 2026-11-03

MekongPhon is now a high-priority external baseline candidate, not an unavailable lead. Shurtz et al. (2026), [MekongPhon: A Large-Scale Parallel IPA Corpus for Lao and Khmer](https://doi.org/10.63317/4bb9rvdshu4z), reports 367,000 Lao and 1.3m Khmer orthography–IPA pairs and under 2% CER on its held-out sets. LREC proceedings are CC BY-NC 4.0; this is not proof of the separate dataset license.

Artifact review: [BYU MATRIX Lab repository](https://github.com/byu-matrix-lab/MekongPhon), main tree SHA f80f6c1840c4818b51e05f2e00cded4701a5b662, has no tracked LICENSE file. The Lao word lexicon has 6,319 rows (6,316 unique spellings); split files have 6,219 train + 100 eval, with three duplicate train spellings and zero train/eval overlap. The scraper uses SEAlang source kerr72 and first matching entry. The checked-in splitter writes *_train_cleaned.csv / *_eval_cleaned.csv, but the sentence converter uses different absent paths and points evaluation mapping to the full lexicon. OPUS sentence corpora are downloaded externally, not tracked. The repo therefore does not demonstrate that the 100-word lexeme holdout produced the published held-out CER.

The [Lao tonal](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and [non-tonal](https://huggingface.co/byumatrixlab/lao-ipa-nontonal) model cards declare Apache-2.0 for model artifacts. That does not clear scraped SEAlang or corpus rights or establish profile/IPA compatibility. Use only as an external candidate prediction after pinning the model revision and validating output convention; never gold. No data imported; accuracy remains null.

## Common Voice v27.0 Lao manifest audit — 2026-11-03

The official release manifest `cv-corpus-27.0-2026-09-11.json` records 223 Lao clips, 193 validated clips, 16 contributor IDs, 0.35 validated hours (0.40 total). The Lao locale has no accent/variant metadata; gender/age fields are incomplete and skewed. Manifest checksum: `3fe87d019e65ac7e97806390698804bb60dec02444cba372706739dd8fb260c6`; manifest Git blob SHA: `e401c4a8e923cad5c8baacb6120c095b1e1bd561`. This is a small scripted-sentence audio lead, not IPA-labelled data, not a citation-form lexicon, and not evidence of Vientiane variety. It can be used only after a Lao specialist approves the target profile and individual clips/lexemes are manually verified; otherwise recruit controlled citation-form speakers.


## Common Voice 27.0 Lao — rights and intake audit (2026-11-04)

The exact Mozilla Data Collective record is https://mozilladatacollective.com/datasets/cmu5odnv300xnmh070xkxthxo. It declares **CC0-1.0**, but its dataset-specific forbidden-use terms still prohibit attempts to identify speakers and prohibit re-hosting/re-sharing. It describes 223 clips / 0.40h, of which 193 clips / 0.35h are validated, from 16 speakers; the source text pool contains 11,071 sentences. Only 48 clips from four speakers have an accent entry, but the accent value is blank; gender and age are incomplete. The release metadata does not establish Vientiane or any other specific Lao variety.

**Disposition: candidate external audio for specialist screening, not gold and not an unrestricted mirrorable corpus.** Use the provider-hosted data and opaque clip IDs/locators; do not copy audio into this repository, re-host it, or attempt speaker identification. A specialist must determine whether any clip fits the chosen Vientiane citation-form profile. The very small 0.35h validated subset and unknown variety make this inadequate as a stand-alone language-wide benchmark. The 2026-11-03 manifest audit remains the canonical count/hash record; this update adds the provider's current licensing/usage terms.


## Candidate: IARPA Babel Lao Language Pack (LDC2017S08) — 2026-11-04

**Disposition: high-value, profile-aligned Vientiane audio/transcript corpus; access and agreement required; NOT IPA gold.**

- Official catalog: https://catalog.ldc.upenn.edu/LDC2017S08
- DOI: https://doi.org/10.35111/bq21-kf58
- The LDC catalog describes approximately **207 hours** of Lao conversational and scripted telephone speech collected in 2013 with corresponding UTF-8 transcripts. It explicitly identifies the speech as representing the **Vientiane dialect region**.
- Audio is available in 8 kHz 8-bit A-law SPHERE and 48 kHz 24-bit PCM WAV formats. The documentation describes a roughly equal gender distribution and ages 16–60, with recordings across phones and varied environments.
- The catalog lists separate for-profit, non-member and not-for-profit license agreements and directs users to LDC subscription/licensing instructions; the applicable fee is shown after login. Portions are © 2015 U.S. Government; the catalog says the U.S. Government acquired the data from Appen and Appen assigned copyright to the U.S. Government.
- The transcripts are orthographic/romanized, not IPA. The corpus is telephone speech and includes both conversational and scripted material, so it is not a citation-form dictionary and must not be treated as uniform careful speech.

**Why this is useful:** unlike the small Common Voice Lao set, the catalog explicitly states Vientiane-region speech and provides substantial audio plus transcripts. If the project can lawfully obtain access, it is a stronger candidate for a controlled Vientiane speaker/audio pilot and human IPA annotation.

**Acceptance before use:**
1. Confirm whether the owner has LDC membership or a suitable non-member agreement and obtain the exact license terms before download.
2. Preserve LDC catalog number, DOI, package version, manifest, checksums, speaker IDs as anonymized source IDs, transcript IDs and exact audio time spans.
3. Separate scripted and conversational conditions; the project's citation-form benchmark should use only specialist-approved scripted/careful tokens, with conversational speech retained as a separate register.
4. Have qualified Lao phoneticians perform two independent blind IPA annotations and separate adjudication; preserve tone, vowel length, offglides and uncertainty.
5. Do not redistribute the corpus or derived materials unless the signed LDC agreement permits it.

The source is now registered as `SRC-LDC-BABEL-LAO-2017`. This is a source discovery/access lead only: no audio or transcript data were copied, independent adjudicated Lao IPA gold remains 0, and accuracy remains null.


## Research-use implementation update — 2026-11-07

The paper abstract states that all data, code and pretrained models are publicly released to support future research and development ([ACL Anthology record](https://aclanthology.org/2026.lrec-1.129/), abstract). Following the project owner's instruction, ClippyFirst now uses MekongPhon as a research comparator and rule-discovery resource. A pinned aggregate-only diagnostic reads `data/splits/lao_train.csv` at upstream commit `f80f6c1840c4818b51e05f2e00cded4701a5b662`; CI stores only summary metrics and aggregated error contexts. The train split is not a held-out test or independent gold. The 100-row eval split remains separate.

# Controlled IPA gold acquisition — Lao

**Status:** protocol ready for a human pilot; this document admits no gold labels.  
**Scope:** a controlled Lao pilot followed by a versioned, independently adjudicated benchmark.

## Evidence boundary

A pronunciation from this repository, a G2P system, romanizer, dictionary, language model, or annotator memory is not gold merely because it is plausible. Keep source evidence, expert judgments, and engine predictions separate. Never seed an annotation with model output or infer complete IPA from spelling alone.

Choose one target profile before recruitment. Recommended pilot profile: contemporary Vientiane Lao, careful citation forms, with one approved broad-phonemic or broad-phonetic convention. Do not combine Vientiane, Luang Prabang, Nam Pua, and other varieties in one undifferentiated score.

## Roles and blindness

1. **Curator:** selects lexemes, checks sources/rights, assigns opaque IDs, prepares packets; does not annotate.
2. **Annotators A and B:** independently transcribe identical packets. They see orthography, disambiguating gloss/context, target variety, and source/audio evidence, but never each other's work or engine predictions.
3. **Adjudicator C:** receives both locked submissions only after both arrive; cannot be A or B; records decision and rationale.
4. **Release maintainer:** validates provenance, rights, schema, split integrity, and export.

Use stable pseudonymous IDs in Git. Keep identity mappings and contact details outside the repository. Never place private audio or personal data in public issues or PRs.

## Pilot sampling

Start with **30 lexeme groups** as a process pilot, not an accuracy benchmark. Select attested items to cover, where supported by the chosen variety and sources:

- all attested tone categories and contour contrasts;
- short/long vowel contrasts and relevant diphthongs;
- onset classes and aspiration/voicing contrasts;
- open vs checked syllables and oral, nasal, or glottal codas;
- common syllable templates and a few multisyllabic forms;
- source disagreements and cases the engine marks uncertain.

Do not generate a theoretical Cartesian product. Every item must be an attested lexeme with an exact source locator. Record selection rationale and uncovered cells. Keep pilot items out of held-out evaluation if they are used to revise the engine.

## Lao convention sheet

Before annotation, approve a versioned sheet specifying target variety, speaker/recording context, citation vs connected speech, IPA kind, tone notation, contour representation, vowel length, diphthongs/offglides, syllable boundaries, glottalization, uncertainty, and variant policy.

Lao tone is lexically contrastive; tonal contours also vary with tonal context. Keep citation-form lexical tone distinct from contextual F0 realization. Yanagimura (2013) reports carryover and anticipatory contextual effects: https://so03.tci-thaijo.org/index.php/mekongjournal/article/view/6739. Published inventories differ by variety; EURPhon provides distinct Vientiane and Luang Prabang profiles: https://eurphon.info/languages/html?lang_id=214 and https://eurphon.info/languages/html?lang_id=467.

## Candidate external reference: MekongPhon

MekongPhon (LREC 2026) reports 367,000 Lao and 1.3 million Khmer orthography–IPA pairs: https://lrec.elra.info/lrec2026-main-129 (DOI https://doi.org/10.63317/4bb9rvdshu4z). It is a **candidate external reference**, not admitted gold. Before importing or using entries as validation evidence, verify the dataset download/repository and exact version/checksum; dataset-specific license and redistribution/derivative rights; Lao variety; source lexicon; normalization and IPA convention; what “verified” means; source locators; duplicate/variant policy; and overlap with our development sources.

The LREC proceedings' CC BY-NC-4.0 license does not establish the dataset's own license. Until the checks above are complete, classify MekongPhon as candidate / rights_unverified / methodology_unverified. Do not populate records.jsonl or gold.tsv from it.

## Controlled workflow

1. Curator freezes the pilot list and records source provenance and rights before annotation.
2. Curator generates opaque IDs and two separate packets with identical evidence and conventions, but no model output or competing IPA.
3. A and B submit separately. Curator timestamps and locks both before either annotator can see the other.
4. C reviews both locked submissions and the source packet. C records AGREEMENT, RESOLVED, or UNRESOLVED. RESOLVED requires final IPA and a written evidence-based rationale; do not force agreement.
5. Curator validates schema, cross-file links, duplicates, rights, and the blind-process checklist. Unresolved items remain outside gold.
6. Export only rights-cleared adjudicated records. Keep restricted source material external; store exact locators/checksums where permitted.
7. Freeze a versioned manifest before benchmarking.

## Annotation packet

Each packet must include opaque record ID; target profile; orthography and NFC form; gloss/minimal context; source title/provider/version/page/entry/audio locator; rights evidence; lawful audio access and recording context; pseudonymous speaker ID; IPA kind and convention-sheet version; fields for literal IPA, syllable boundaries, tone, length, phonation, confidence, uncertainty, and comments.

## Acceptance gates

- **Pilot can start:** target variety and convention sheet approved; two qualified annotators and one independent adjudicator confirmed; rights-cleared packets ready; blind intake dry-run passed.
- **Pilot accepted:** 30 items have two independent submissions; all disagreements are adjudicated or explicitly unresolved; provenance and rights are complete; blindness is evidenced; validation passes.
- **Benchmark-ready:** expanded stratified corpus; frozen train/dev/test manifest; no lexeme leakage; held-out test untouched during tuning; coverage report for tone × rhyme/coda × length and onset contrasts; rights and reproducibility review passed.

Existing numeric thresholds (100 train / 25 dev / 25 test) are minimum engineering gates, not a statistical sufficiency guarantee. Coverage and independent review remain mandatory.

## Current blockers

- **BLOCKED:** qualified Lao annotators and an independent adjudicator have not been recruited/confirmed.
- **BLOCKED:** item-level rights review for the pilot source list is incomplete.
- **BLOCKED:** MekongPhon dataset license, variety, and annotation methodology are unverified.
- **TODO:** approve the Lao convention sheet and freeze the 30-item pilot.
- **TODO:** complete a blind dry-run with one non-gold practice item.

## References

- Shurtz, Richardson & Richardson (2026), MekongPhon, LREC 2026: https://lrec.elra.info/lrec2026-main-129
- Yanagimura (2013), Contextual Tonal Variations in Vientiane Lao: https://so03.tci-thaijo.org/index.php/mekongjournal/article/view/6739
- EURPhon, Lao Vientiane: https://eurphon.info/languages/html?lang_id=214
- EURPhon, Lao Luang Prabang: https://eurphon.info/languages/html?lang_id=467


## MekongPhon repository inspection — 2026-11-01

The upstream repository is https://github.com/byu-matrix-lab/MekongPhon. Its README describes data/ as lexicons, OPUS download scripts, sampled sentences and train/eval splits. pipeline/README.md describes: SEAlang frequency lists → IPA scraping via scrape.py → minor lexicon post-processing (including Lao tone-mark conversion) → OPUS sentence download → lexicon split → trie-based word lookup to convert sentences, filtering sentences containing out-of-lexicon tokens. This is an important provenance clue: sentence IPA is composed from a scraped word lexicon, not necessarily independently transcribed sentence-level phonetic gold.

The repository root LICENSE path was not present when inspected. No dataset-specific redistribution license has therefore been verified. The paper's claim that pairs are aligned and verified and the proceedings' CC BY-NC-4.0 license do not substitute for the dataset license, per-entry source provenance, or a description of human verification. Do not import or redistribute any MekongPhon records yet. First inspect the exact lexicon files, scraping source/terms, correction protocol, variety and tone conventions, split construction, and data permissions; contact maintainers if these remain ambiguous. The public model cards' Apache-2.0 model license must not be assumed to license training data.


## Audio-source shortlist — reviewed 2026-11-01

These are **audio/transcript candidates**, not IPA gold. The distinction matters: the engine's lexical G2P contract is best evaluated against a declared citation-form pronunciation. A sentence-level corpus records contextual tokens, often with coarticulation and prosodic effects; it cannot silently stand in for citation-form lexicon entries.

### Common Voice Scripted Speech 27.0 — Lao

- Official catalog: https://commonvoice.allizom.org/en/datasets (catalog lists “Common Voice Scripted Speech 27.0 - Lao”, locale `lo`, CC0-1.0, MP3, 8.93 MB).
- Dataset/version documentation: https://github.com/common-voice/cv-dataset/tree/main/datasets/scripted-speech. Scripted Speech consists of contributors reading pre-written sentences; community members validate recordings. The v27.0 release is dated 2026-09-11 in the current release history.
- The catalog's 8.93 MB is a compressed dataset size, **not** a clip/speaker count. Exact validated clip count, speaker count, sentence coverage and metadata must be computed from the v27.0 manifest before sampling.
- No IPA labels are supplied. The language code alone does not establish Vientiane variety, register or speaker background. Do not infer the desired Vientiane-oriented profile from the catalog label.
- Recommended use: a supplementary contextual-audio source and a way to identify possible lexical prompts. For citation-form lexical gold, prefer consented recordings elicited from speakers whose target variety has been confirmed. If Common Voice is used, retain the clip ID, transcript, time interval and source/version metadata; do not attempt to identify speakers.

### Collection decision

Common Voice v27.0 is the best currently identified small, publicly catalogued Lao audio lead, but it is **not yet accepted as the 30-item lexical pilot source**. First inspect its actual v27.0 manifest and determine whether enough target-variety speakers and contrast-bearing tokens exist. If not, recruit speakers for controlled citation-form recordings. Do not use MekongPhon or any G2P output as a substitute for independent expert transcription.


### Exact v27.0 manifest audit

The official Common Voice release manifest has now been inspected: [`cv-corpus-27.0-2026-09-11.json`](https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json).

- Lao locale entry: **223 clips**, **193 validated clips**, **16 contributor/user IDs**, **0.35 validated hours** (0.40 total hours).
- The manifest provides no named accent category for Lao (the accent key is empty); the variant dimension is empty. Gender metadata is 88.79% male and 11.21% unspecified; ages are 55.61% thirties, 32.74% twenties, 0.45% forties and 11.21% unspecified.
- Manifest locale checksum field: `3fe87d019e65ac7e97806390698804bb60dec02444cba372706739dd8fb260b6`. Manifest file blob SHA: `e401c4a8e923cad5c8baacb6120c095b1e1bd561`.

This is a small, demographically narrow sample with **no dialect evidence**. It is not a sound basis for asserting Vientiane coverage or a balanced lexical benchmark. It may support a 30-token process pilot only if the actual validated transcripts contain 30 suitable lexemes and a specialist explicitly approves the contextual profile. It does not replace controlled citation-form elicitation.

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

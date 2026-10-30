# Final scientific audit

## Reconstructed state

The repository is now one coherent Lao → Ukrainian research project. The active architecture contains implementation, canonical Lao registries, a canonical Ukrainian correspondence registry, comparative evidence, provenance data, tests, and explicit research documentation.

No obsolete/foreign/temporary files were identified in the inspected tree. The repository did not contain a separate historical research corpus that required destructive deletion; therefore no research evidence was archived or deleted during this pass.

## Corrective work

- Replaced the initial substring-based vowel detection with explicit structural Lao vowel patterns.
- Corrected the distinction between short and long preposed vowels such as ເກະ vs ເກ.
- Corrected long /ɔː/ representation through ກໍ / the Niggahita-based pattern.
- Added a Vientiane live-syllable tone fallback independent of short/long vowel length when a sonorant coda is present.
- Treated ອ as a tone-class vowel carrier rather than automatically inserting an IPA /ʔ/ before every overt vowel.
- Added deterministic repository auditing and derived-data generation scripts.
- Expanded public documentation and explicit limitations.
- Strengthened source provenance with Unicode, W3C Lao layout guidance and Ueda's DOI.

## Not claimed

- an official Ukrainian national standard;
- complete automatic segmentation of unspaced Lao text;
- complete initial-cluster analysis;
- complete independent tonal rules for every use of ໜ/ໝ;
- a full Pali/Sanskrit transcription system;
- calibrated probabilities or empirical accuracy percentages;
- a complete lexical corpus or expert-adjudicated gold standard.

The Russian system remains a comparator, not an intermediate representation. Serbian and Bulgarian remain target-script controls rather than invented Lao-specific standards.

## Current quality judgement

**🟡 Usable but needs finalization.**

The repository is substantially more defensible and reproducible than the initial research foundation, but publication-grade status requires a representative corpus, fuller syllable/cluster grammar, independent verification of edge cases, and expert adjudication of the Ukrainian target correspondences.


## External IPA and benchmark audit — 2026-10-24

- The external comparator `lao2ipa 1.0.0` has a reproducible 36-probe smoke run with 0 runtime errors. Latest categorized artifact: [run 40122329060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/40122329060), SHA-256 `2b7f3c5e3c02814413e42b9f2031849c21630fba9958a7e6a38de92f7a63ff55`.
- Strict raw IPA agreement is 0/36. A separate tone-letter-stripped diagnostic matches 29/36 (80.6%), leaving 7 tone/length/segmental/offglide cases for review. This is a string-difference diagnostic, not accuracy; Lao tone can be contrastive and must not be stripped from production IPA.
- The benchmark gold-provenance guard is merged: every ADJUDICATED row requires non-empty IPA, source_id and profile. The independent gold corpus remains empty, so accuracy is null.
- External systems remain optional. Epitran (`lao-Laoo`) and Goruut are upstream support candidates only, not yet executed in this repository. Remaining acceptance criteria: expert-adjudicated lexical IPA, documented tone convention, and source-based review of the seven non-tone/format cases.


## Ukrainian target-policy audit — 2026-10-30

**Scoped status: DONE_VERIFIED.** The IPA-to-Ukrainian correspondence registry, Python adapter, generated browser data and tests now preserve aspiration and distinguish the requested Ukrainian consonants.

- Aspiration: /kʰ tʰ pʰ/ → к' т' п'; source IPA retains the aspiration feature.
- Distinctions: /h/ → г, /ɡ/ → ґ, /x/ → х.
- Affricates: /t͡s/ → ц, /d͡z/ → дз, /t͡ʃ/ → ч, /d͡ʒ/ → дж; Lao /tɕ/ and documented alveolo-palatal aliases map to ч/дж as explicit approximations.
- Palatalized consonants use Ukrainian soft-sign sequences only when the source analysis establishes palatalization. /ʔ/ is not aspiration.
- Canonical CSV → generated browser-data parity was checked; exact-head workflow [41075912762](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41075912762) passed.
- Changes are in draft PR #56; no merge or deployment was performed.

This does not establish a normative Ukrainian transcription standard or improve the independent Lao pronunciation gold set. The research corpus still has no independently adjudicated lexical IPA gold and accuracy remains unmeasured. The broader limitations listed above remain open.


## Optional romanization-to-Ukrainian result mode — 2026-10-30

- Added a two-method selector inside the primary Ukrainian result card. The IPA-first phonetic output remains the default and is unchanged.
- The first revision used a character-level Latin adapter. That revision is **superseded** after user review; do not treat its mapping table as the current implementation.
- Current implementation uses `web/romanization-syllable-engine.js`: it parses romanized onset, vowel nucleus and coda, applies position-sensitive coda correspondences, and assembles Ukrainian syllables. The compatibility file `web/romanization-ukrainian.js` re-exports this engine and no longer implements character-by-character substitution.
- Project invariant: `h → г` in every position, including inside `kh`, `th`, and `ph`. Ambiguous or unsupported syllable segmentation is retained in visible brackets and marked partial.
- Evidence sources for the romanization layer are registered in `data/evidence/sources.csv`: the provisional CLDR transform and the EKI/UNGEGN report for BGN/PCGN 1966. The report states that Lao has no UN-approved romanization system and no national romanization system. The CLDR transform itself leaves special final-consonant handling as TODO.
- Exact-head engineering verification: **DONE_VERIFIED** for commit `02dd2bfe24e09a10fdb08265a4074aedbce97c8c`; [workflow 41123807011](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41123807011) passed repository data/evidence audit (43 consonants, 34 vowels, 17 tone rules, 69 UA mappings, 19 sources, 33 claims with all references resolved), Python (92), browser engine (46), romanization transform/compatibility (9), syllable-engine (9), web-layout (5), external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/asset checks.
- This verifies deterministic behavior for the implemented subset, not linguistic accuracy or full CLDR coverage. It does not change the independent IPA gold-corpus count (still zero). Manual visual/keyboard QA remains open; PR #65 remains unmerged and the feature has not been deployed.

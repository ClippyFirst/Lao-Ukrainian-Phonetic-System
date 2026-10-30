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

- Added a second selectable method inside the Ukrainian result card. Phonetic IPA-first output remains the default and unchanged.
- The new adapter consumes only the provisional CLDR Lao-Latin/UNGEGN output and applies an explicit project orthographic mapping. It is not a phonological engine and cannot restore tone, length or other information absent from romanization.
- Unknown characters are preserved and flagged partial. The romanization intermediate remains independently visible and copyable; the main copy action follows the selected Ukrainian method.
- Engineering acceptance: **DONE_VERIFIED** for branch head `cfa95799c47eb683e590b061e4f40b6b4f154737`; exact-head workflow [41119525542](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41119525542) passed Python (92), browser engine (46), romanization (8), web-layout (5), build, generated-data reproducibility and built-page/asset checks. This feature does not change the scientific status of the Lao phonology model, the provisional CLDR profile, or the independent gold-corpus count (still zero). Manual visual/keyboard QA remains open.

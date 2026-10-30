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
- Current implementation uses `web/romanization-syllable-engine.js`: it parses romanized onset, vowel nucleus and coda, validates each onset against the original Lao consonant grapheme, validates the nucleus against the source vowel ID, checks supported coda graphemes against CLDR forms, applies position-sensitive coda correspondences, and assembles Ukrainian syllables. The compatibility file `web/romanization-ukrainian.js` re-exports this engine and no longer implements character-by-character substitution.
- Corrected source-aware policy: BGN/PCGN `kh/th/ph` spell aspirated Lao stops and map to `к'/т'/п'`; standalone Lao `h` (/h/, ຫ/ຮ) maps to `г`. The BGN `x` spelling for ຊ maps to `с`, not `кс`; final `h` is rejected because it is not a supported Lao coda. BGN/PCGN note 5 explicitly says silent ຫ is omitted before sonorants and that ໜ/ໝ are abbreviated forms of ຫນ/ຫມ; the adapter therefore maps them through `n/m` to `н/м`, not through an audible `h`. Ambiguous, mismatched or unsupported syllable segmentation is retained in visible brackets and marked partial.
- Evidence sources for the romanization layer are registered in `data/evidence/sources.csv`: the provisional CLDR transform and the EKI/UNGEGN report for BGN/PCGN 1966. The report states that Lao has no UN-approved romanization system and no national romanization system. The CLDR transform itself leaves special final-consonant handling as TODO.
- The earlier engineering verification at commit `753b82c89076b2e23fbbcd937df45bf4289b7dfc` remains historical evidence for the prior adapter only. The corrected source-vowel and nasal-ligature crosswalk is verified at implementation head `d0b9a585a3edf2ad0c89ba9f9b10fcbc35aa62e6` by [workflow 41137893545](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41137893545): repository audit passed (43 consonant rows, 34 vowel rows, 17 tone rules, 69 Ukrainian mappings, 20 evidence sources and 44 claims; all references resolved); Python 92; browser engine 46; romanization integration 19; syllable crosswalk 27; web layout 5; external-G2P harness syntax/CLI, build, generated-data reproducibility and built-page/relative-asset checks all passed. The workflow assertion for the versioned app module URL was updated to accept the cache-busting query string; the built relative path remains verified.
- This verifies deterministic behavior for the implemented subset, not linguistic accuracy or full CLDR coverage. It does not change the independent IPA gold-corpus count (still zero). Manual visual/keyboard QA remains open; PR #65 remains unmerged and the feature has not been deployed.


### Source-vowel and high-class nasal crosswalk — 2026-10-31

- Added `LAO_VOWEL_TO_CLDR` source mapping for the implemented vowel subset. The browser app passes the IPA-first structural parser's `VOWEL:<ID>` rule identity as evidence; the romanization result itself is still generated independently from CLDR syllable parsing and does not consume IPA.
- The crosswalk checks source onset, source vowel ID and supported source coda. It resolves homographic `kam` from source structure (A + coda m versus AM nucleus), and resolves `niav` as ໜ + IA_LONG + final ວ only when the Lao syllable evidence is available. Without that evidence, ambiguous parses remain PARTIAL.
- Added the official UK government BGN/PCGN 1966 agreement to the evidence registry. Its note 5 establishes silent-`h` omission and the abbreviated ligature forms ໜ/ໝ; these are now correctly treated as n/m, not as h+n/h+m.
- Added explicit tests for source vowel mismatch, nasal ligature mapping, source-resolved `niav`, and the full `ເຂົ້າໜຽວ` source. The exact-head workflow above passes all gates.
- This remains a bounded romanization adapter, not an accuracy-certified transcription standard. The romanization collapses vowel length and does not preserve tone; unsupported source vowel patterns remain partial. Manual visual/keyboard QA and an independently adjudicated linguistic gold corpus remain open.

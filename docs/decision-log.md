# Decision log

## D-001 — IPA before Ukrainian Cyrillic

**Decision:** The Ukrainian output is derived from Lao phonological analysis and IPA, never from Russian Cyrillic.

**Reason:** This prevents target-language orthography from becoming a hidden intermediate representation.

## D-002 — Russian as comparator

**Decision:** Russian Lao practical transcription is retained as a historical/practical comparator.

**Reason:** It is valuable evidence, but its `кх/пх/тх`, `х`, `ы`, `ть` and vowel-doubling conventions are partly consequences of Russian phonology/orthography and cannot be assumed optimal for Ukrainian.

## D-003 — Serbian/Bulgarian as controls

**Decision:** Serbian and Bulgarian are target-script controls, not Lao-specific normative systems.

**Reason:** Official geographical-name examples demonstrate that the same Lao names can be adapted differently to different Cyrillic target languages.

## D-004 — Tone separate from Ukrainian stress

**Decision:** Lao tone is retained in analysis but is not automatically converted to Ukrainian stress.

**Reason:** Tone and Ukrainian lexical stress are different prosodic systems.

## D-005 — Vowel length is analytical

**Decision:** Short/long quantity remains in the source analysis but is normally neutralized in practical Ukrainian output.

**Reason:** Automatic doubled vowels would import a Russian/romanization convention without a demonstrated Ukrainian orthographic benefit.

## D-006 — Uncertainty is explicit

**Decision:** Analysis-dependent and evidence-limited cases are not forced into a false definitive mapping.

**Reason:** Research reproducibility requires the distinction between established evidence and project policy.


## D-007 — Romanization fallback is a separate optional method

**Decision:** Keep the IPA-first phonetic method as the default and add a user-selected, independent syllable-level adapter from the provisional CLDR Lao-Latin/BGN romanization to Ukrainian. The adapter parses onset, vowel nucleus and coda, then assembles a Ukrainian syllable. This decision's initial blanket `h → г` mapping for `kh/th/ph` was superseded by D-008 after phonological source review. The original decision to keep the mode optional, syllable-based and separate from the IPA-first pipeline remains in force.

**Reason:** The two paths answer different questions. The phonetic path models pronunciation through IPA; the second method adapts the written romanization through a separate orthographic syllable model. It must not be a character-by-character Latin-to-Cyrillic substitution, must not consume IPA, and must not silently switch methods. The BGN/PCGN source distinguishes initial and final consonant forms; the provisional CLDR transform does not implement every final-position rule, so the adapter documents its project policy and its limits.


## D-008 — Cross-check Lao graphemes before adapting romanization onsets

**Decision:** Validate each romanized onset against the corresponding original Lao onset grapheme. BGN/PCGN spellings kh/th/ph from ຂ/ຄ, ຖ/ທ and ຜ/ພ represent aspirated stops and map to к'/т'/п'. Independent Lao /h/ from ຫ/ຮ maps to г. BGN x from ຊ represents /s/ and maps to с. Reject final h because it is not a supported Lao coda. Withhold mismatched or unaligned source/romanization pairs.

**Reason:** The letter h inside an established romanization digraph is not a separate /h/ phoneme. Richard Ishida's Lao Orthography Notes distinguishes /kʰ tʰ pʰ/ from /h/ and identifies their source graphemes; the EKI/UNGEGN report supplies the BGN/PCGN Latin spellings. A blanket h → г rule confuses aspiration with an independent consonant and produces the wrong Ukrainian result. The crosswalk uses original Lao grapheme evidence without routing the romanization mode through the IPA-first result pipeline.

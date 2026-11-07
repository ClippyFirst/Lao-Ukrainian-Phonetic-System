# MekongPhon Lao grapheme-context analysis — 2026-11-07

## Purpose and rule-engine contract

This work studies **which Lao grapheme element has which phonetic realization in which structural position and context**. It does not create a word-to-IPA lookup table, copy dictionary entries into ClippyFirst, or train the production engine to memorize whole words.

The production pipeline remains:

`Lao orthography → structural syllable parsing → onset/vowel/coda roles → source IPA → Ukrainian adaptation`

The runtime rules are positional and compositional:

- `data/lao/consonants.csv`: separate `ipa_initial` and `ipa_final` values;
- `src/lao_ukrainian/parser.py` and `data/lao/vowels.csv`: resolve the complete written vowel pattern, including preposed, above, below, postposed and multi-sign structures;
- `data/lao/onset_clusters.csv`: treat documented multi-grapheme onsets as joint onset units;
- `data/lao/tone_rules.csv`: derive tone from consonant class, live/dead rhyme, vowel length and tone mark;
- `src/lao_ukrainian/phonetic_result.py`: preserve the typed IPA boundary before Ukrainian adaptation.

A vowel sign is not assigned an invented independent phoneme when it contributes jointly to a multi-sign nucleus. The analysis records the grapheme element, its role, the complete orthographic unit, and whether the associated sound is scoped to that whole unit.

## Dataset and reproducibility

- Source: [MekongPhon](https://github.com/byu-matrix-lab/MekongPhon), pinned revision `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Split: 6,219 word-level seed-lexicon train rows only.
- SHA-256: `2d0f68989009620980ced3386f11a640e6167404308eeb6a79efc52bc8e40ee0`.
- Diagnostic: [run 42390734319 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42390734319).
- Code/test checkpoint: `16d267664beb25a9e26e9639aace42a2975582d1`.
- Aggregate artifact SHA-256: `7d51559fc9d5ef7d173850d9237cbd62577c2b7b890e96d1e73a6f113d46938a`.
- Verification boundary: this linked artifact is from the base context analyzer at `16d267...`. The later direct-position and broader phonological-context output arrays are present in code/test checkpoint `b376296947c93b1ab01a4a26bdd5afcfc2e756db`; its exact-head diagnostic and Verify were still pending when this report revision was written.

No raw source words, reference strings or per-item predictions are written to the artifact. The report contains aggregate grapheme/context distributions and structural-unit alignment counts only. The 100-row eval split is not used for discovery or rule tuning.

## Method

1. NFC-normalize each source row and run the ClippyFirst syllable segmenter.
2. Parse every syllable into onset, vowel structure and coda. Any row containing an unparsed or malformed syllable is withheld rather than partially guessed.
3. Track Lao Unicode code points separately. Combining vowel and tone signs retain their own positions and structural roles.
4. Classify each element as onset base, high-class modifier, labialization modifier, preposed vowel sign, above/below/postposed vowel sign, coda or tone mark.
5. Tokenize engine and reference IPA using the longest-match typed IPA inventory; align the sequences with deterministic Levenshtein backtrace.
6. Aggregate both **engine IPA** and **reference-aligned IPA** by:
   - grapheme and structural role;
   - initial/medial/final syllable position within the source token;
   - previous and next grapheme elements;
   - onset class, vowel ID, live/dead type, coda and tone mark.
7. Keep a multi-grapheme vowel or onset cluster as a joint unit. Do not claim that every constituent sign independently produces the whole sound.

The JSON output distinguishes:
- `grapheme_position_rules`: grapheme + role + syllable position;
- `phonological_context_rules`: the same mapping conditioned on onset class, vowel, rhyme and tone context;
- `candidate_contextual_rules`: the more local previous/next-grapheme context;
- `structural_unit_alignments`: engine IPA versus reference-aligned IPA for complete structural units;
- `tone_mark_contexts`: aggregate tone-mark environments, kept separate from segmental sound mappings.

## Coverage and diagnostic result

| Measure | Result |
|---|---:|
| Train rows | 6,219 |
| Fully structurally parsed rows | 5,820 (93.58%) |
| Withheld rows | 399 (6.42%) |
| Parsed syllables | 9,883 |
| Exact engine/reference IPA strings among parsed rows | 3,885 / 5,820 (66.75%) |
| Reference IPA tokens | 26,155 |
| Alignment edits | 2,857 |
| Alignment insertions | 163 |

The 66.75% figure is **reference concordance conditional on ClippyFirst parsing**, not empirical accuracy. MekongPhon is a dictionary-seeded development source, not independently adjudicated ClippyFirst gold.

The 399 withheld rows are dominated by:
- 266 `UNCONSUMED_AFTER_VOWEL`;
- 60 `VOWEL-STRUCTURE-NOT-ESTABLISHED`;
- 46 `NO-MODERN-LAO-ONSET`;
- 44 `MALFORMED_TONE_MARK_POSITION`;
- 37 `AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY`;
- 30 `SHORT_VOWEL_REQUIRES_CODA`;
- 17 `MULTIPLE_TONE_MARKS`;
- 15 `MALFORMED_TONE_MARK_ORDER`;
- 2 `UNCONSUMED_BEFORE_ONSET`;
- 1 `LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL`.

These cases remain fail-closed. Increasing coverage by guessing would corrupt the very grapheme-position evidence this study is meant to establish.

## Examples of positional rules already implemented and regression-tested

| Lao element | Structural role | ClippyFirst IPA |
|---|---|---|
| `ວ` | onset | /ʋ/ |
| `ວ` | coda | /w/ |
| `ດ` | onset | /d/ |
| `ດ` | coda | /t/ |
| `ບ` | onset | /b/ |
| `ບ` | coda | /p/ |
| `ອ` | silent vowel carrier before an overt vowel | no separate segment |
| `ອ` | component of the `AWW_MEDIAL` vowel structure | /ɔː/ |
| `ເ` + short-vowel structure | preposed vowel sign | /e/ |
| `ເ` + long-vowel structure | preposed vowel sign | /eː/ |

The same grapheme is not globally assigned one sound. Its parsed role and the surrounding structure determine which registry entry applies.

## High-frequency source-profile differences

The largest recurring structural-unit differences are:

| Orthographic unit / role | ClippyFirst IPA | MekongPhon reference-aligned IPA | Count pattern |
|---|---|---|---:|
| `ວ`, onset | /ʋ/ | /w/ | 163 initial, 101 final, 28 medial |
| `ຽ`, vowel structure | /iːə/ | /iaː/ | 129 initial, 69 final, 5 medial |
| `ເົາ`, vowel structure | /aw/ | /ao/ | 124 initial, 42 final, 12 medial |
| `ວ` in `UO_LONG`, vowel structure | /uːə/ | /uaː/ | 116 initial, 62 final, 15 medial |
| `ເືອ`, vowel structure | /ɯːə/ | /ɯːə̯/ | 111 initial, 38 final, 4 medial |
| `ໄ` / `ໃ`, vowel structure | /ai/ | /aj/ | 363 combined across spellings/positions |
| `ຣ`, onset | /l/ | /r/ | 81 final, 58 medial, 33 initial |
| `ເີ`, vowel structure | /ɤː/ | /əː/ | 75 initial, 30 final |

These are **investigation leads, not automatic corrections**. They may reflect transcription convention, dialect/profile, phonetic detail or lexical class. In particular:
- initial /ʋ/ versus /w/ is already explicitly source-profile-sensitive in the project;
- /iːə/ versus /iaː/, /aw/ versus /ao/, /uːə/ versus /uaː/, and /ai/ versus /aj/ require source-convention review before changing vowel rules;
- `ຣ` /l/ versus /r/ is potentially loanword/historical-reading dependent and cannot be solved by a blind global replacement;
- a coda /w/ aligned with an /o/-like reference offglide may be a rhyme/transcription convention, not evidence that the coda grapheme independently means /o/.

No production grapheme-to-IPA rule was changed merely to maximize agreement with these unadjudicated dictionary references.

## IPA adapter corrections

The typed IPA inventory now treats the engine's documented labialized onset units as single consonant segments (`tʷʰ`, `kʷʰ`, `kʷ`, `tɕʷ`, `ʔʷ`, `sʷ`, `ŋʷ`, `lʷ`) and recognizes long schwa `əː` and the non-syllabic schwa offglide `ə̯`.

This prevents modifier-bearing consonants and vowel offglides from being fragmented into unsupported code points at the IPA boundary. It does **not** silently invent Ukrainian correspondences: where the target correspondence table has no approved mapping, Ukrainian adaptation remains fail-closed.

## What this changes in the engine

- The production engine continues to resolve **grapheme role and structural position**, not word identity.
- Regression tests now explicitly cover onset/coda alternations (`ວ`, `ດ`), short/long preposed `ເ`, silent-carrier versus vowel-sign `ອ`, high-class digraphs, labialized onsets and IPA token integrity.
- The MekongPhon diagnostic now emits three aggregate levels of positional/contextual rule candidates with both engine and reference IPA shown separately.
- The research split does not modify the 100-row eval set and does not populate the independent gold corpus.

## Next evidence gates

1. Review the 399 parser-withheld rows by warning family; only implement structures supported by primary orthographic/phonological sources.
2. Ask a qualified Vientiane Lao reviewer to adjudicate the source-profile differences above.
3. Build the independent, blind-reviewed IPA gold corpus; it remains at 0 independently adjudicated records.
4. Only after those gates, promote a contextual rule into the canonical registries and add independent fixtures.


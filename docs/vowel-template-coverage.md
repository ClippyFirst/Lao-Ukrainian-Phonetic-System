# Vowel-template coverage matrix

This is an executable regression coverage matrix for the current Python parser's `STRUCTURES` table. It describes parser behavior, not an expert-adjudicated Lao lexicon. Synthetic forms isolate grapheme patterns; only the named lexical/source-backed examples in `tests/fixtures/vowel_precedence_cases.json` should be read as explicit IPA assertions, and that fixture is still an engineering regression set rather than a gold corpus.

## Per-template positive and negative controls

`tests/test_structural_vowels.py::TestEveryVowelStructureHasPositiveAndNegativeControls` iterates every row in `STRUCTURES`, asserts the synthetic positive parses to the declared vowel ID, then removes one grapheme from the suffix (or substitutes a different preposed sign for empty-suffix templates) and asserts the near-miss does not parse as the same vowel ID.

| Template | Preposed grapheme | Postposed sequence | Vowel ID | Synthetic positive | Negative control |
|---|---|---|---|---|---|
| `pre_e_short` | ເ | ະ | `E` | `ເກະ` | Remove the last suffix grapheme; for empty-suffix templates substitute another preposed sign; must not resolve to `E` |
| `pre_e_short_kan` | ເ | ັ | `E` | `ເກັ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `E` |
| `pre_e_long` | ເ | ∅ | `EE` | `ເກ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `EE` |
| `pre_ae_short` | ແ | ະ | `AE` | `ແກະ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AE` |
| `pre_ae_short_kan` | ແ | ັ | `AE` | `ແກັ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AE` |
| `pre_ae_long` | ແ | ∅ | `AEE` | `ແກ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AEE` |
| `pre_o_short` | ໂ | ະ | `O` | `ໂກະ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `O` |
| `pre_o_short_mai_kon` | ໂ | ົ | `O` | `ໂກົ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `O` |
| `pre_o_long` | ໂ | ∅ | `OO` | `ໂກ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `OO` |
| `pre_oe_short` | ເ | ິ | `OE` | `ເກິ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `OE` |
| `pre_oe_long` | ເ | ີ | `OEE` | `ເກີ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `OEE` |
| `pre_ia_short` | ເ | ັຽ | `IA` | `ເກັຽ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `IA` |
| `pre_ia_short_nyo` | ເ | ັຍ | `IA` | `ເກັຍ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `IA` |
| `pre_ia_long` | ເ | ຽ | `IA_LONG` | `ເກຽ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `IA_LONG` |
| `pre_ia_long_nyo` | ເ | ຍ | `IA_LONG` | `ເກຍ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `IA_LONG` |
| `pre_ua_short` | ເ | ຶອ | `UA` | `ເກຶອ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UA` |
| `pre_ua_long` | ເ | ືອ | `UA_LONG` | `ເກືອ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UA_LONG` |
| `pre_aw` | ເ | ົາ | `AW_LONG` | `ເກົາ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AW_LONG` |
| `pre_ai` | ໄ | ∅ | `AI` | `ໄກ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AI` |
| `pre_ay` | ໃ | ∅ | `AI2` | `ໃກ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AI2` |
| `post_a_short` | ∅ | ະ | `A` | `ກະ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `A` |
| `post_a_short_kan` | ∅ | ັ | `A2` | `ກັ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `A2` |
| `post_aa` | ∅ | າ | `AA` | `ກາ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AA` |
| `post_i` | ∅ | ິ | `I` | `ກິ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `I` |
| `post_ii` | ∅ | ີ | `II` | `ກີ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `II` |
| `post_o_short_closed` | ∅ | ົ | `O` | `ກົ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `O` |
| `post_y` | ∅ | ຶ | `Y` | `ກຶ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `Y` |
| `post_yy` | ∅ | ື | `YY` | `ກື` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `YY` |
| `post_u` | ∅ | ຸ | `U` | `ກຸ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `U` |
| `post_uu` | ∅ | ູ | `UU` | `ກູ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UU` |
| `post_o_short_alt` | ∅ | ັອ | `AWW_SHORT_ALT` | `ກັອ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AWW_SHORT_ALT` |
| `post_o_long_medial` | ∅ | ອ | `AWW_MEDIAL` | `ກອ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AWW_MEDIAL` |
| `post_o_long_open` | ∅ | ໍ | `AWW` | `ກໍ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AWW` |
| `post_am` | ∅ | ຳ | `AM` | `ກຳ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AM` |
| `post_ua_short_alt` | ∅ | ັວ | `UO_SHORT_ALT` | `ກັວ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UO_SHORT_ALT` |
| `post_ua_short` | ∅ | ົວະ | `UO` | `ກົວະ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UO` |
| `post_ua_long` | ∅ | ົວ | `UO_LONG` | `ກົວ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UO_LONG` |
| `post_ua_long_closed_alt` | ∅ | ວ | `UO_LONG_ALT` | `ກວ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UO_LONG_ALT` |
| `post_ua_long_open_alt` | ∅ | ວາ | `UO_LONG_OPEN` | `ກວາ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `UO_LONG_OPEN` |
| `post_ia_long_standalone` | ∅ | ຽ | `IA_LONG` | `ກຽ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `IA_LONG` |
| `short_o_around` | ເ | າະ | `AW` | `ເກາະ` | Remove the last suffix grapheme (or prefix for empty suffix); must not resolve to `AW` |

## High-risk precedence contrasts

The hand-authored contrast test also verifies that adjacent spellings which overlap under generic-prefix matching remain distinct:

| Contrast family | Positive A → ID | Contrast B → ID | Regression prevented |
|---|---|---|---|
| Preposed E | `ເກະ` → `E` | `ເກ` → `EE` | Short suffix not shadowed by empty-suffix long form |
| Preposed AE | `ແກະ` → `AE` | `ແກ` → `AEE` | Short/long AE collision |
| Preposed O | `ໂກະ` → `O` | `ໂກ` → `OO` | Short/long O collision |
| Preposed OE | `ເກິ` → `OE` | `ເກ` → `EE` | OE short not shadowed by generic long E |
| Preposed OEE | `ເກີ` → `OEE` | `ເກ` → `EE` | OE long not shadowed by generic long E |
| Preposed IA | `ເກັຽ` → `IA` | `ເກຽ` → `IA_LONG` | Quantity marker preserved |
| Preposed UA | `ເກຶອ` → `UA` | `ເກືອ` → `UA_LONG` | Quantity marker preserved |
| Preposed AW | `ເກາະ` → `AW` | `ເກົາ` → `AW_LONG` | Distinct vowel spellings preserved |
| Postposed UO | `ກົວະ` → `UO` | `ກົວ` → `UO_LONG` | Browser/Python must not split short UO into two segments |
| Postposed O | `ກັອບ` → `AWW_SHORT_ALT` | `ກໍ` → `AWW` | Short closed variant not confused with long open form |
| Postposed UO alternative | `ກັວບ` → `UO_SHORT_ALT` | `ກວງ` → `UO_LONG_ALT` | Alternative spelling and quantity distinguished |

## Invalid/ambiguous structure controls

- `ກັ`: short A2 without a coda must carry `SHORT_VOWEL_REQUIRES_CODA:A2` and yield partial/evidence-limited status.
- `ກັອ`: short alternative O without a coda must carry `SHORT_VOWEL_REQUIRES_CODA:AWW_SHORT_ALT`.
- `ກາງເ`: a legal final may not be accepted before trailing unconsumed graphemes.
- `ເກິະ` and `ເກີະ`: appended vowel material must not be silently treated as a complete established syllable.
- Unregistered final `ສ` is not accepted as a coda.

## Scope and limitations

The browser engine has its own explicit matcher rather than consuming Python's `STRUCTURES` table. Shared IPA fixtures keep both engines aligned on the same expected outputs, but the per-template synthetic matrix directly enumerates Python structures. Browser-specific near-neighbour and malformed-input controls remain separate tests in `web/engine.test.js`. Passing deterministic tests does not prove that every pattern is licensed in every Lao dialect or lexical context.

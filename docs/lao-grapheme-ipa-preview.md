# Lao grapheme-level IPA preview and conservative fallback

## Contract

The ordinary path remains `Lao orthography → structural syllable parse → source phonology → typed IPA → Ukrainian adaptation`.

A grapheme-level preview is a separate diagnostic result, generated only when the full parser/phonology path withholds IPA. It is **not** an alternative accepted pronunciation and is never sent to the Ukrainian adapter.

## Output levels

- `SUPPORTED`: complete IPA from the established structural and phonological path.
- `PROVISIONAL`: a partial segmental IPA hint assembled only from registered positional correspondences and a partial parse. Missing or ambiguous graphemes remain visible; tone is never inferred by this fallback.
- `UNRESOLVED`: no safe segmental hint can be produced. Original graphemes remain available with unresolved roles.

The preview is exposed by the Python analysis API and CLI JSON output and by the browser engine/UI. Both runtimes label it PROVISIONAL, preserve unresolved graphemes and withhold accepted IPA/Ukrainian output. The preview's typed `PhoneticResult` is marked `PROVISIONAL` at result and segment level. The normal target adapter accepts only `SUPPORTED` results, so preview IPA cannot silently become Ukrainian output.

## What the fallback may use

- Existing onset registry values, including position-sensitive onset IPA.
- Explicitly registered onset-cluster units.
- Known silent high-class modifiers and the following consonant.
- A vowel IPA value only when the main parser has matched a registered complete vowel structure.
- A coda IPA value only when the parser has identified a legal coda.

It does not infer a vowel from an isolated sign, guess a consonant's role from its shape alone, derive tone, or turn Pali/Sanskrit letters into modern Lao phonemes. Unknown material remains unresolved.

## Examples

- `ກາລ`: the known prefix may preview as `kaː`; final `ລ` remains unresolved in that syllable context.
- `ຂ່້າ`: the segmental hint `kʰaː` may be shown, but malformed multiple tone marks still withhold normal IPA and Ukrainian output.
- `ຂເ`: the known onset `kʰ` may be previewed; the preposed vowel sign remains unresolved because the complete vowel structure is absent.
- `ຆາ`: no modern-Lao IPA is invented for the non-core Pali grapheme.

## Inventory scope

The canonical Unicode inventory is `data/lao/grapheme_inventory.csv`. It catalogs every assigned character in the Unicode 18 Lao block, while distinguishing modern Lao core letters from Pali/Sanskrit extensions, Khmu-specific letters, punctuation, repetition marks, digits and structural signs. The Unicode block is a codepoint range, not a claim that every character belongs to modern Lao phonology. The [Unicode 18 Lao Names List](https://www.unicode.org/Public/18.0.0/charts/nameslist/0e80/) establishes codepoint identities and names; the [W3C Lao script overview](https://www.w3.org/International/sealreq/lao/) describes the structural role of composite vowels, tone classes and the restricted subjoined consonant convention.

## Coverage policy

A grapheme inventory and the fallback's role inventory are different measures. A grapheme can be recognized structurally without having a standalone IPA value; a multi-sign vowel is a joint unit, not a sequence of independent phonemes. Coverage reports must distinguish Unicode recognition, structural role recognition, source-attested correspondence, full-parser acceptance, and preview-only combinations. The inventory is codepoint-complete for assigned characters in Unicode 18 Lao; phonetic coverage is intentionally narrower and remains incomplete for Indic and Khmu extensions.

This is an engineering affordance, not an accuracy claim. Independent adjudicated Lao IPA gold remains required for empirical accuracy claims and promotion of new rules.


The acceptance target for the Unicode 18 Lao block is **100% codepoint recognition and visible handling**: every assigned inventory character must either receive a typed grapheme role or be explicitly passed through as orthographic/numeric punctuation. This does not mean 100% of codepoints have an independent sound, nor that all combinations have a confirmed pronunciation. Pali/Sanskrit and Khmu characters remain recognized but outside the modern-Lao phonetic profile.

## Expanded grapheme and composite-vowel handling

The canonical Unicode inventory remains the authority for every assigned Lao-block codepoint. The hybrid distinguishes modern-Lao phonetic material from structural marks, repetition, punctuation, digits, Pali/Sanskrit extensions and Khmu-specific letters; recognition is not the same as a standalone phonetic value. `ຽ` is context-sensitive: it can form the /iːə̯/ rhyme or act as a final /j/ glide. The parser now includes six additional source-attested composite patterns (`ເ◌ີຍ` /ɤːj/, `ໂ◌ຍ` /oːj/, `ແ◌ວ` /ɛːw/, `◌ອຍ` /ɔːj/, `◌າຽ` /aːj/, and medial `◌ັຽ` /iə̯/) in both Python and browser runtimes. The Lao ellipsis `ຯ` is preserved as punctuation, not misclassified as a phoneme. Source: [Richard Ishida, Lao Orthography Notes (28 April 2026)](https://r12a.github.io/scripts/laoo/lo), especially the character index, composite-vowel list and IPA mapping tables. Pali/Sanskrit, Khmu and obsolete marks remain explicitly out of modern-Lao phonetic scope rather than receiving invented IPA.

## Automated verification

- Exact-head Verify 42416380324 passed on commit 4d2ebc2c9348ac4952869492095e82d0a22dcdc4: 260 Python tests, 126 Node tests and 10 Chromium tests.
- The browser UI shows the provisional preview separately from accepted IPA/Ukrainian output. A malformed-tone case recovers only segmental structure from the tone-stripped surface; the preview never infers tone.
- The Unicode inventory mirror is generated from the canonical CSV and checked for reproducibility in CI.
- Manual assistive-technology and physical-device QA remains part of UI-001; automated browser tests are not represented as manual screen-reader certification.

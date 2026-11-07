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

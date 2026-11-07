# Typed IPA → Ukrainian adapter contract

## Purpose

The phonetic Ukrainian output is generated only from a typed phonetic result. The Lao parser and phonology own source-language analysis; the Ukrainian adapter owns target-language rendering. They communicate through `PhoneticResult`, not through Lao graphemes, vowel IDs, coda IDs or source-language parser objects.

This follows the executable boundary used by the Thai–Ukrainian repository. It is a software architecture contract, not evidence that the phonological analysis or every Ukrainian correspondence is linguistically validated.

## Pipeline

```text
Lao orthography
  → normalization and graphemic/syllable analysis
  → Lao phonology and tone
  → phonemic IPA
  → PhoneticResult
  → Ukrainian IPA adapter
  → practical Ukrainian orthography
```

The optional romanization route remains separate. It does not call this adapter and must not be used as a fallback when IPA is uncertain or unsupported.

## Typed result

The IPA segment tokenizer uses a source-side IPA inventory independent of the Ukrainian correspondence table. The target adapter then performs its own longest-match pass over the concatenated typed segments; this permits an orthographic target unit such as /ʃt͡ʃ/ → щ without making it one source IPA phoneme.

The Python `PhoneticResult` and browser `phoneticResult` carry:

| Field | Meaning |
|---|---|
| `phonemic_ipa` / `phonemicIpa` | Canonical phonemic IPA supplied by the Lao phonology stage |
| `broad_surface_ipa` / `broadSurfaceIpa` | Reserved, currently null; no independent broad-surface layer is claimed |
| `external_ipa` / `externalIpa` | Reserved, currently null; external engine output is not silently promoted |
| `segments` | Longest-match IPA tokens, each typed as vowel or consonant and carrying provenance |
| `syllable_boundaries` / `syllableBoundaries` | Segment offsets for the syllable represented by this result |
| `vowel_length` / `vowelLength` | Source vowel quantity metadata, separate from the segmental target |
| `tone_category` / `toneCategory` | Resolved Lao tone category, if established |
| `tone_contour_ipa` / `toneContourIpa` | The contour associated with the matched project rule, if available |
| `status` | `SUPPORTED`, `UNCERTAIN` or `UNSUPPORTED` |
| `provenance` | Phonological rule identifiers that produced the result |
| `uncertainty` | Parser/phonology warnings and unsupported-segment notes |

The current Lao engine produces phonemic IPA only. The surface and external fields are explicit empty slots, not inferred copies of phonemic IPA.

## Adapter contract

- Python `adapt_phonetic_result(PhoneticResult)` and browser `adaptPhoneticResult(result)` accept a typed result, not a string or Lao input.
- `SUPPORTED` means the segmental phonemic IPA is complete and mappable; it does not imply that every suprasegmental feature is resolved.
- Only `SUPPORTED` results with a complete sequence of registered IPA segments can produce Ukrainian output.
- `UNCERTAIN` segmental readings and `UNSUPPORTED` IPA are withheld. An unresolved tone alone is recorded in `uncertainty` while a supported segmental result may still be adapted. A plausible IPA prefix must never be rendered as if it represented the complete source syllable.
- The adapter reads only typed IPA segments and the canonical `data/lao/ukrainian_correspondences.csv` mirror. It does not inspect Lao source graphemes or source vowel/coda identifiers.
- Longest-match segmentation is performed before adaptation, preserving exact registered sequences such as /ʃt͡ʃ/ → щ.
- The IPA result represents one parsed syllable. When its first typed segment is /j/ and the next is a supported vowel, the Ukrainian adapter applies the syllable-initial йотація policy (/ja/ → я, /je jɛ/ → є, /ji/ → ї, /jo jɔ/ → йо, /ju/ → ю; /jɯ/ → йи; /jɤ/ → йе). Medial/coda /j/ remains й. Python and browser adapters implement the same rule and tests.
- The source glide /w/ is always adapted as Ukrainian в, including the /aw/ rime → ав; it is not changed to у in coda position.
- Tone and vowel quantity remain visible in metadata. Their neutralization in practical Ukrainian spelling is an explicit target policy, not silent loss at the interface.
- The Python and browser implementations are independently implemented and must be checked by the same contract tests and shared output fixtures.

## Current limits

- There is no independently validated broad-surface IPA layer yet.
- A typed object and passing software tests do not validate the Lao phonological rules or Ukrainian target choices.
- The independent adjudicated Lao IPA gold corpus remains empty; corpus accuracy is therefore not established.
- Some source analyses are deliberately marked uncertain. Under this contract they no longer receive a Ukrainian phonetic output merely because a string mapping could be produced.

## Verification

The contract is protected by Python tests for typed-only adapter input, metadata retention, unsupported IPA and uncertainty abstention, plus browser tests for the equivalent behavior. Full acceptance also requires the repository audit, Python tests, browser tests, generated-data reproducibility and built-site Chromium suite on the exact commit.

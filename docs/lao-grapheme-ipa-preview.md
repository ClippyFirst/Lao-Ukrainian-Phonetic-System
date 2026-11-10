# Lao grapheme fallback and low-confidence Ukrainian output

## Purpose and contract

The primary processing path remains:

`Lao orthography → structural analysis → Lao phonology → typed IPA → Ukrainian target adaptation → practical Ukrainian orthography`.

The deterministic hybrid must still produce a visible Ukrainian-side result when the full structural/phonological path cannot establish a complete reading. This is a **rendering-coverage contract**, not a promise that every grapheme has an independently established pronunciation.

The fallback is not a second direct Lao-to-Ukrainian transliterator. It builds a typed `PROVISIONAL` IPA sequence from registered grapheme-position hints and explicit unknown segments, then sends that sequence through the **same typed IPA → Ukrainian adapter** used by the normal path. The adapter does not inspect Lao source graphemes. Known provisional IPA runs use the canonical Ukrainian correspondence registry; unresolved units produce visible `?` markers.

## Output and confidence levels

| Level | Meaning | Ukrainian rendering |
|---|---|---|
| `SUPPORTED` | Complete segmental IPA established by the structural and phonological path | Normal target adaptation |
| `UNCERTAIN` | Complete segmental IPA exists, but one or more phonological features remain uncertain | Target adaptation is allowed in the primary hybrid; uncertainty is retained |
| `PROVISIONAL` | Last-resort typed segmental hints; grapheme position, syllable structure, vowel interpretation or other context is not fully established | Known IPA portions are adapted through the same target adapter; unresolved source positions are shown as `?` |
| `UNRESOLVED` | No defensible IPA hint can be supplied for a source unit | The source unit remains visible and receives an explicit `?` in the Ukrainian-side output |

A result marked `PROVISIONAL` or `EVIDENCE LIMITED` is **low confidence**. The UI and text CLI must say so explicitly. A visible Ukrainian rendering must never be mistaken for a confirmed pronunciation.

## What the fallback may use

- Registered onset values, including position-sensitive onset IPA.
- Explicitly registered onset-cluster units and their component roles.
- Known silent high-class modifiers and the following consonant.
- Parser-confirmed vowel structures and registered provisional vowel-grapheme hints when structure is unresolved.
- A registered coda value when the parser has identified a legal coda.
- Explicit unknown markers for graphemes or positions that cannot be mapped safely.

The fallback must preserve the source grapheme sequence and must not silently drop unresolved units. It does not infer tone. A tone mark can remain visible as structural evidence, but the fallback does not manufacture a tone category or contour. Pali/Sanskrit and Khmu-only graphemes are recognized as out-of-scope where appropriate; they do not receive invented modern-Lao phonemes and remain represented by an unknown marker if no target convention exists.

## Adapter boundary and provenance

The Python path uses `preview_from_graphemes()`, a typed provisional `PhoneticResult`, and `adapt_phonetic_result()`. The browser path mirrors this in `previewFromGraphemes()`, `adaptPhoneticResult()`, and the hybrid `analyze()` orchestration.

- Every provisional IPA segment remains marked `PROVISIONAL` in the enclosing result.
- Provisional IPA is not promoted to `SUPPORTED`; a local adapter mapping step does not change the source result's confidence.
- Unknown segments are explicit typed units, not guessed phones.
- Tone remains unresolved; no tone contour is assigned by the grapheme fallback.
- Provenance identifies the fallback path and uncertainty warnings remain attached to the result.
- Frozen compatibility profiles retain their documented abstention behavior. Full-coverage provisional rendering belongs to the primary `hybrid-deterministic` profile.
- Romanization remains a separate, lower-information orthographic method. It is not used as a fallback for failed IPA analysis.

## Examples

- `ກາລ`: the available provisional hints can produce a low-confidence Ukrainian rendering such as `кал?`; the final unresolved marker remains visible rather than silently dropping the tail.
- `ຂ່້າ`: the segmental hint can produce `к'а`, but malformed multiple tone marks remain unresolved; the fallback does not infer a tone.
- `ຂເ`: the known onset and available vowel hint can be rendered provisionally while the incomplete vowel structure remains marked as uncertain.
- `ຆາ`: the known vowel may be represented provisionally, but the non-core Pali consonant is not assigned a fabricated modern-Lao sound and remains unknown.

Exact outputs are regression contracts only where they are pinned in the corresponding tests. They are not independent phonetic gold labels.

## UI and CLI presentation

For a provisional result, the detailed result panel must show:
1. the available IPA hint, labelled as provisional / low confidence;
2. the Ukrainian practical rendering, including any `?` markers;
3. the unresolved source graphemes or positions;
4. an explicit note that the reading is low confidence and tone was not inferred.

The Python text CLI must similarly print the Ukrainian result, provisional IPA preview, unresolved graphemes and a low-confidence note. JSON/API results retain typed status, segment certainty, provenance and uncertainty fields.


## Long unresolved spans and IPA summary behavior

The main IPA field must not discard a typed provisional preview merely because the full syllable parser did not establish a complete phonemic IPA result. For each non-passthrough unit, display in this order:

1. accepted `syllable.ipa` when present;
2. otherwise `graphemePreview.ipaPreview`, explicitly labelled provisional in the detailed analysis;
3. otherwise a single `?`.

When a provisional preview also contains unresolved source positions, the IPA summary appends a visible uncertainty marker. The Ukrainian adapter likewise retains the provisional IPA-derived material and adds an uncertainty marker. A contiguous unresolved region is represented by one `?` for a single unresolved grapheme, or at most `???` for a longer unresolved run. The marker count is deliberately not a grapheme count: it communicates confidence, not source length. This prevents long unsupported names from producing visually meaningless tails of dozens of question marks while preserving a clear distinction between provisional IPA and confirmed IPA.

Regression target: `ພຣະຣາຊອານາຈັກຣ໌ລາວ`. The test contract is that available registered hints remain visible in the IPA field, the Ukrainian result does not contain a run longer than three question marks, and the result remains low-confidence with no inferred tone. This is a rendering/uncertainty contract, not an adjudicated pronunciation of the phrase.

## Inventory scope

The canonical Unicode inventory is `data/lao/grapheme_inventory.csv`. It catalogs assigned characters in the Unicode 18 Lao block while distinguishing modern Lao core letters from Pali/Sanskrit extensions, Khmu-specific letters, punctuation, repetition marks, digits and structural signs. Unicode recognition is not proof of a modern-Lao phonetic value. The [Unicode 18 Lao Names List](https://www.unicode.org/Public/18.0.0/charts/nameslist/0e80/) establishes codepoint identities and names; the [W3C Lao script overview](https://www.w3.org/International/sealreq/lao/) describes composite vowels, tone classes and script structure.

## Coverage and acceptance

Report these measures separately:

- **Unicode recognition:** whether an assigned codepoint is recognized.
- **Visible rendering:** whether each valid source unit contributes to a visible Ukrainian-side output, including explicit `?` markers and passthrough.
- **Typed IPA coverage:** whether a unit has accepted `SUPPORTED` or `UNCERTAIN` typed IPA under the benchmark contract.
- **Phonetic accuracy:** agreement with an independently annotated and adjudicated reference.

A 100% visible-rendering result does not imply 100% IPA coverage, supported pronunciation, lexical segmentation, or phonetic accuracy. The independent adjudicated Lao IPA gold corpus remains empty at the current checkpoint; no empirical accuracy claim is justified.

## Verification

The contract is covered by:
- `tests/test_grapheme_preview.py` for Python fallback, adapter output and CLI details;
- `web/engine.test.js` for browser-side typed provisional behavior and cross-runtime expectations;
- `tests/browser/site.spec.js` for visible low-confidence notes and actual Ukrainian output;
- the repository Verify workflow for Python, Node, generated-data reproducibility, Chromium UI and built-site checks.

Manual screen-reader, keyboard, mobile-device and physical-device QA remains a separate acceptance item. Passing automated tests does not establish linguistic accuracy or manual accessibility certification.

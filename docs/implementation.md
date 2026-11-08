# Implementation

## Architecture

- `normalize.py` — NFC normalization and mixed-script validation; U+200B is accepted as a Lao word boundary and normalized to a token separator before parsing.
- `parser.py` — Lao graphemic syllable parsing and structural vowel recognition.
- `phonology.py` — live/dead classification, tone lookup and phonemic IPA construction.
- `phonetic_result.py` — typed `PhoneticResult` boundary: source-inventory IPA tokenization, syllable offsets, length, tone, provenance and uncertainty; tokenization is independent of target correspondence keys.
- `target.py` — typed-result-only IPA-to-Ukrainian adapter and candidate ranking; only the primary hybrid profile may adapt UNCERTAIN IPA without upgrading its status, and its explicit PROVISIONAL unknown segment renders as ?.
- `core.py` — public analysis orchestration.
- `model.py` — serializable analysis dataclasses.
- `data.py` — registry loading.
- `cli.py` — command-line entry point.

## Reproducibility

- Run: `PYTHONPATH=src python -m unittest discover -s tests -v`
- The package metadata also exposes a `lao-ua` console entry point when installed in an environment with the declared build dependency.

## Important boundary

The parser now uses deterministic dynamic programming to segment supported orthographic syllable candidates within each unspaced token. This is structural syllable segmentation, not lexical word segmentation: Lao spaces remain phrase boundaries, and the parser does not infer lexical word boundaries or silently discard unparsed material.

## Failure discipline

Unknown Unicode, unknown vowel structures, and unsupported phonological combinations produce explicit status/warning information rather than silently inventing a correspondence.


## Browser romanization fallback

- `web/romanization.js` — constrained provisional CLDR Lao-Latin/UNGEGN conversion.
- `web/romanization-syllable-engine.js` — parser for romanized syllable onset, nucleus and coda, with a source-Lao onset, vowel-ID and coda crosswalk that distinguishes aspirated digraphs from independent /h/, preserves written onset forms, applies the supported silent-hoa sonorant rule, validates supported CLDR vowel/coda aliases, and withholds mismatched structures before Ukrainian syllable assembly; ambiguous or mismatched parses are withheld.
- `web/romanization-ukrainian.js` — compatibility export for the syllable engine; it no longer contains a letter-by-letter mapping.
- `web/app.js` — the Ukrainian result selector, selected-result copy action, and method-specific disclosure.

The hybrid deterministic phonetic engine is the default. Its Ukrainian output is produced only from the typed PhoneticResult: structurally complete UNCERTAIN IPA can be rendered with its uncertainty preserved, while unresolved units use a typed PROVISIONAL sequence built from diagnostic grapheme-position IPA hints plus explicit unknown markers, rendered through the same adapter. This guarantees rendering coverage without claiming an IPA value or accuracy. Frozen compatibility profiles keep their prior withholding behavior. The second method uses an independent romanized-syllable parser and is not a pronunciation analysis. See [methodology](methodology.md#optional-romanization-to-ukrainian-mode) for the grapheme/romanization/target crosswalk, aspiration policy, and information-loss boundary.

See [the typed IPA → Ukrainian adapter contract](ipa-to-ukrainian-adapter.md) for the executable boundary, status semantics and verification.

## Ukrainian IPA target sequence handling

The canonical IPA correspondence registry is shared by the Python target adapter and generated browser engine. Longest-match selection maps the exact Ukrainian sequence /ʃt͡ʃ/ to щ before considering the shorter /ʃ/ → ш and /t͡ʃ/ → ч entries. This does not merge arbitrary consonants: the exact ordered sequence is a documented target orthographic unit. The remaining distinctions /h, ɦ/ → г, /ɡ/ → ґ, /x/ → х, /d͡ʒ/ → дж, /d͡z/ → дз and /t͡s/ → ц are preserved in the same canonical table.

## Static web build clarification — 2026-11-06

The current web implementation is framework-free: index.html and system.html load native ES modules from web/. scripts/generate_web_data.py writes the canonical CSV mirror web/data.js; scripts/build_web.py copies both pages and the runtime into dist/. There is no Vite dependency or bundler in package.json. Node tooling is used for tests and Playwright, not for bundling the application. See [web architecture](web-architecture.md).


## Integrated segmentation, provisional preview and optional neural provider — 2026-11-08

- `parser.py` performs deterministic dynamic segmentation of unspaced Lao into structurally parsed syllable candidates while preserving unparsed material. It is not a lexical word segmenter; ambiguous or unsupported structures remain visible and phonetic output is withheld.
- Tone-mark storage-order validation is per syllable. A malformed mark or unresolved structural suffix must not retain a confident tone or a misleading IPA prefix.
- `phonetic_result.py` tokenizes source IPA against its own IPA inventory, independent of Ukrainian correspondence keys. `target.py` consumes the typed result. In hybrid only, uncertain but complete IPA can be rendered with its status intact; unsupported units receive a typed unknown placeholder. No grapheme-preview hint is promoted to SUPPORTED IPA or mapped directly from Lao spelling; fallback hints are explicitly typed PROVISIONAL segments and pass through the ordinary IPA adapter.
- `grapheme_preview.py` provides a diagnostic provisional segmental preview from registered positional grapheme correspondences and parser-confirmed vowel/coda structures. It never infers tone or becomes supported IPA. In the primary hybrid fallback, its hints are wrapped in a separate PROVISIONAL PhoneticResult, unresolved graphemes become typed unknown segments, and the ordinary IPA-to-Ukrainian adapter renders the provisional sequence.
- `mekongphon.py` is an optional, explicitly selected neural provider. The hybrid deterministic engine remains the default; model revisions are immutable, automatic truncation is disabled, raw IPA/provenance are retained, and unknown symbols fail closed.
- The benchmark scripts and reports are comparative diagnostics. The 100-entry external dictionary reference and training-split aggregates are not independent project IPA gold and must not be used as accuracy claims.
- Exact integrated engineering verification: [Verify 42460320528](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42460320528), exact head `dd07adcd7d709ea5e1b8f94c3556965eefda73c9`.

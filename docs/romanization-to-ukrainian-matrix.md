# Lao romanization → Ukrainian orthographic matrix

**Status:** PARTIAL — direct Latin input is now supported for the BGN/PCGN-derived CLDR profile and a bounded ALA-LC 2012 subset; ambiguity, unsupported spellings and missing distinctions remain explicit.
**Primary variety:** contemporary Standard Lao; Vientiane-oriented phonetic mode remains separate.

## Standard selection

Use the **BGN/PCGN 1966 Lao romanization convention as represented by the Unicode CLDR Lao-Latin transform** as the project's operational romanization profile. This is the best-supported practical choice for a reproducible romanization route, not an assertion that Laos has an official national romanization standard.

The UK Government/PCGN Laos Toponymic Factfile (2023) explicitly says there is no official romanization system in use for current Lao orthography; it states that the BGN/PCGN system agreed in 1966 continues to be used by PCGN in the absence of a domestic official system. The project therefore retains the label **provisional BGN/PCGN-derived CLDR Lao-Latin**, not “official Lao”.

Sources:
- https://www.gov.uk/government/publications/romanization-systems
- https://assets.publishing.service.gov.uk/media/64f9c99f7a4b4f0012f6d8a5/Laos_Toponymic_Factfile.pdf

## Route separation

- **Romanization mode:** Lao orthographic syllable → CLDR Lao-Latin → source-aware onset/nucleus/coda crosswalk → Ukrainian practical syllable. It does not infer pronunciation, tone or length that the romanization does not encode.
- **Phonetic mode:** Lao orthographic analysis → source phonology → IPA → Ukrainian target adaptation. It may withhold unsupported units.
- The romanization route must not consume IPA as its source and must not fall back to the phonetic result.

## Direct romanization input

The browser now accepts a romanized Lao string directly; the user does not need to provide Lao script first. The input profile can be selected as **BGN/PCGN 1966 / CLDR Lao-Latin**, **ALA-LC 2012**, or **automatic**. Automatic selection uses distinctive ALA-LC diacritics, modifier-apostrophe vowels, `oe`, and the ALA-LC palatal-nasal spelling before a vowel; otherwise it selects the BGN/PCGN-derived profile. This is a convenience heuristic, not a complete standard classifier: when the source convention is known, users should select it explicitly.

The BGN/PCGN profile uses the existing onset–nucleus–coda parser. The ALA-LC profile normalizes the table's implemented vowel spellings: `u`/`ū`, `uʼ`/`ūʼ`, `e`/`ē`, `æ`/`ǣ`, `oe`/`ōe`, `ia`/`īa`, `ua`/`ūa`, `ai`/`āi`, `ao` and `am`. Quantity is collapsed in Ukrainian output. `ny` remains the ALA-LC palatal-nasal onset and is not rewritten to BGN/PCGN `gn`. Its final parser is separate from BGN/PCGN: finals are `k`, `ng`, `t`, `p`, `n`, `m`, plus `o` after a vowel for final `ວ`. The LOC table's parenthesized final values are romanized as the value shown in parentheses (e.g. final `ຣ/ລ` appear as `n`, not `r/l`), so the source consonant cannot be recovered from Latin text alone. This is **not** a complete ALA-LC implementation. Initial `ʻ` has no approved Ukrainian target mapping yet; medial `w` clusters, contextual `ວ` behavior and loanword/word-boundary rules remain unsupported or partial. A table spelling such as `būak` can remain ambiguous between one `ūa` syllable and multiple syllables without source boundaries, so it is withheld. The normalizer never claims that a normalized form is the original romanization.

For direct BGN/PCGN input, strict boundary mode applies PCGN note 4: an initial onsetless vowel may appear at the beginning of a word, while a medial onsetless syllable requires the prescribed hyphen. This resolves the documented official example Viangchan as v + ia + ng / ch + a + n without allowing a competing unmarked medial vowel-only parse. Explicit hyphens remain boundaries, not decorative punctuation. See the [PCGN 1966 agreement, note 4](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/693731/ROMANIZATION_OF_LAO.pdf) and the [2023 Laos Toponymic Factfile example](https://assets.publishing.service.gov.uk/media/654cff895d6095000dbec8b1/Laos_Toponymic_Factfile.pdf).

The engine preserves punctuation and whitespace, reports the detected/selected profile, and leaves ambiguous or unsupported spans in visible `⟦…⟧` brackets. The ALA-LC parser rejects BGN-only aliases such as `x` and `gn`, and does not accept `s`, `v`, `r` or `l` as final spellings. Without the original Lao syllable structure, a Latin string such as `kam` may have more than one valid analysis; it is withheld rather than guessed. Romanization-only input does not produce IPA, and it cannot recover tone, vowel length or consonant-class distinctions that the chosen romanization omits.

**RTGS note:** the LDC Lao language-specific document lists RTGS among schemes that have been used for Lao, but it does not provide a normative, complete RTGS-for-Lao mapping table in the cited section. RTGS is primarily the Royal Thai General System of Transcription. The project therefore does not label the current parser as RTGS and does not silently interpret every RTGS-like spelling as Lao. A dedicated profile requires a specific Lao adaptation table and reviewed examples. Informal French-style, karaoke and mixed spellings likewise remain evidence-limited.

Sources: [ALA-LC Lao Romanization Table (2012)](https://www.loc.gov/catdir/cpso/romanization/lao.pdf); [LDC Language Specific Peculiarities Document for Lao](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf); [PCGN Laos Toponymic Factfile (2023)](https://assets.publishing.service.gov.uk/media/64f9c99f7a4b4f0012f6d8a5/Laos_Toponymic_Factfile.pdf).

## ALA-LC 2012 inventory boundary

The LOC table is broader than the currently implemented normalizer. The implemented subset is limited to `u/ū`, `uʼ/ūʼ`, `e/ē`, `æ/ǣ`, `oe/ōe`, `ia/īa`, `ua/ūa`, `ai/āi`, `ao` and `am`, plus the onset/final subset documented above. This list must not be read as full ALA-LC vowel coverage.

The LOC table also specifies the following forms, which remain unsupported by the Ukrainian adapter: `ư`, `ư̄`, `œ`, `œ̄`, `ǫ`, `ǭ`, `ưa`, `ư̄a`, `iu`, `īu` and `īeo`. Note 2 treats final `ຍ` as the closing `i` of the `ai`/`āi` diphthong, not as a consonant coda; the source-aware crosswalk now preserves that distinction. Note 4 additionally defines medial-`ວ` behavior: `w` in clusters before a vowel (e.g. `khwā`, `khwǣng`), `ūa` before a final consonant (e.g. `būak`, `dūai`), and `o` after a vowel in final position (e.g. `nāo`, `kǣo`); the final-`o` pattern can now be crosswalked when source syllable structure is supplied; standalone strings that admit competing vowel/coda parses remain PARTIAL. Medial `w` clusters and the `ūa` alternation remain unsupported. Note 5 suppresses `ຫ` before specified sonorants and permits ligature forms; Note 6 uses initial `ʻ` for vowel-initial syllables but treats medial `ອ` as a vowel. Notes 2, 3 and 7–10 cover final `ຍ`, subscript `ລ`, vowel placement, numerals, word segmentation/loanword boundaries, tone marks and double-function consonants. These rules are not all recoverable from a bare Latin string, and are not claimed as implemented.

A concrete false-positive risk exists when an unsupported ALA-LC sequence such as `iu` could be split by the generic parser into two ordinary vowel nuclei. The direct-input adapter now detects the unsupported LOC sequences and withholds the entire whitespace-/hyphen-delimited fragment as PARTIAL rather than returning a fabricated syllable sequence. This is a conservative guard, not support for those vowels. The original text remains visible in `⟦…⟧` brackets.

Source: [Library of Congress, ALA-LC Lao Romanization Table (2012), pp. 1–3, especially Notes 2–10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).

## Canonical correspondence table

The existing implementation's detailed, position-sensitive crosswalk is maintained in methodology.md under “Optional romanization-to-Ukrainian mode” and in:
- web/romanization-syllable-engine.js
- web/romanization-ukrainian.js
- data/lao/ukrainian_correspondences.csv
- tests/romanization-syllable-engine.test.mjs

Representative rows:

| Lao source grapheme / structure | CLDR romanization unit | Ukrainian unit | Status / condition |
|---|---|---|---|
| ກ onset | k | к | supported onset |
| ຂ / ຄ onset | kh | к' | aspiration digraph; not standalone h |
| ງ onset | ng | нг | supported onset |
| ຈ onset | ch | ч | supported onset |
| ຖ / ທ onset | th | т' | aspiration digraph; not standalone h |
| ຜ / ພ onset | ph | п' | aspiration digraph; not standalone h |
| ຫ / ຮ onset | h | г | standalone /h/ only |
| ໜ / ໝ | n / m | н / м | silent-hoa ligature; source-aware |
| A nucleus + final ມ | am-shaped sequence | ам | validated against source vowel ID; not interchangeable with AM nucleus |
| AM nucleus | am | ам | source vowel ID required |
| ນ / ມ coda | n / m | н / м | supported coda |
| unsupported or mismatched source/Latin unit | — | withheld | PARTIAL; no guessed syllable |

## Coverage and acceptance

The Romanization method's contract is **complete coverage of the supported orthographic input inventory**, not guaranteed full Unicode reversibility and not phonetic completeness. Every recognized source unit must either map through a source-attested romanization row and an explicit Ukrainian project row, or be retained as a visible PARTIAL / UNSUPPORTED diagnostic without fabricating a Ukrainian syllable.

A future table expansion must add source grapheme/structure, CLDR output, Ukrainian syllable, context, source locator, evidence status, test fixture and reviewer decision. No row may be promoted from a generated CLDR string alone.

## Existing implementation preserved

The syllable-level parser and source-aware checks are retained. It checks onset, source vowel ID and supported coda, distinguishes kam ambiguities when Lao source structure is available, handles supported silent-hoa forms, and refuses ambiguous/mismatched syllables. A separate direct-input path now reuses the parser without inventing source-side Lao evidence. Do not replace either route with character-by-character Latin-to-Cyrillic replacement.

## Remaining tasks

| ID | Status | Acceptance |
|---|---|---|
| LAO-ROM-STD-001 | DONE_VERIFIED (documented selection) | PCGN 1966 / CLDR profile accurately labelled provisional; no claim of official national standard |
| LAO-ROM-MATRIX-001 | PARTIAL | Every supported Lao orthographic syllable has source → Latin → Ukrainian rows and fixtures |
| LAO-ROM-DIRECT-001 | PARTIAL | Direct BGN/PCGN input and bounded ALA-LC 2012 normalization are implemented; exact-head CI, full contextual ALA-LC rules and broader fixture coverage remain required |
| LAO-ROM-RTGS-001 | BLOCKED | Requires an exact Lao-specific RTGS adaptation table and reviewed sample strings; Thai RTGS alone is not sufficient |
| LAO-ROM-COVERAGE-001 | PARTIAL | Inventory audit proves no supported grapheme class is silently dropped |
| LAO-ROM-REVIEW-001 | BLOCKED | Independent Lao specialist review of ambiguous nuclei, conventional names and loanword namespaces |


## Sentence and mixed-text regression checkpoint — 2026-10-31

The current `main` head `2ae2971c2526cba57504e294f37caf64c964c3f6` passed exact-main workflow [41243897060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41243897060). Regression coverage includes the full greeting sentence through the syllable-level CLDR → Ukrainian adapter, preservation of explicit spaces and punctuation, Latin mixed text, ASCII digits and native Lao numerals. Numerals without an evidenced Ukrainian mapping remain visible and explicitly partial; they are not silently deleted or assigned guessed output. These fixtures establish integration/input integrity, not independent linguistic gold. Exhaustive matrix coverage and specialist review remain PARTIAL/BLOCKED as recorded above.


## Post-merge engineering verification — 2026-10-31

PR #90 is merged as `69fa43e7d66e2c4c6468945497ff5a1b1ab7b717`; exact-main workflow [41246317109](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41246317109) passed. This confirms the documented whole-sentence and mixed-text regression set remains green on main. It does not promote the PARTIAL source-to-CLDR-to-Ukrainian inventory to complete or establish independently adjudicated phonetic accuracy.

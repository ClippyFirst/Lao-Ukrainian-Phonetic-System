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


## D-009 — Validate supported coda graphemes against CLDR output

**Decision:** The romanization route must validate both the original Lao onset and any supported Lao coda against the corresponding CLDR romanized elements before emitting a Ukrainian syllable. The supported coda crosswalk is intentionally bounded to ກ→k, ງ→ng, ດ→d, ບ→b, ນ→n, ມ→m, ຍ→gn and ວ→v. The adapter then applies its position-sensitive Ukrainian coda targets (including d→т, b→п, gn→й and v→о/оу). Unsupported or mismatched source codas are withheld rather than inferred from a Latin string.

**Reason:** The provisional CLDR transform applies mostly context-insensitive grapheme substitutions and explicitly leaves special final-consonant handling incomplete. The source Lao coda is available in the analysis result; checking it prevents a plausible-looking but incorrect final from being emitted. The EKI/UNGEGN BGN/PCGN report documents position-dependent final forms, while the pinned CLDR transform documents the upstream aliases used by this adapter.


## D-010 — Validate source vowel nuclei and high-class nasal ligatures

**Decision:** The romanization route validates the source vowel ID against the parsed CLDR nucleus in addition to the onset and supported coda. The supported vowel map is an explicit subset; distinctions collapsed by romanization (including vowel length) are not reconstructed, and source patterns deleted or not represented by the CLDR subset are withheld. BGN/PCGN 1966 note 5 identifies ໜ/ໝ as abbreviated forms of silent ຫ + ນ/ມ and says silent ຫ is generally omitted before sonorants. The implementation applies this to supported written forms ຫງ, ຫຍ, ຫນ, ຫມ, ຫລ, ຫຼ and ຫວ as well as atomic ໜ/ໝ; their romanized onsets retain the underlying sonorant, not an audible /h/. The BGN /r/ case remains unsupported until the structural parser models ຫຣ.

**Reason:** Latin spelling alone can be ambiguous: `kam` may encode A + coda m or the AM nucleus, and `niav` has competing syllabifications. The original Lao parser already retains vowel IDs and atomic high-class nasal graphemes, so this information should be used as evidence rather than guessed or discarded. The official PCGN copy of the BGN/PCGN 1966 agreement and the EKI/UNGEGN report document the vowel table and silent-`h` note; the source-aware adapter can now resolve the corresponding cases while keeping the IPA-first method independent.

## D-011 — Preserve Ukrainian /ʃt͡ʃ/ as the grapheme щ

**Decision:** Add the exact ordered IPA sequence /ʃt͡ʃ/ → Ukrainian щ to the canonical target correspondence registry. Keep the individual mappings /ʃ/ → ш and /t͡ʃ/ → ч, as well as /d͡ʒ/ → дж, /d͡z/ → дз, /t͡s/ → ц, /ɡ/ → ґ, /ɦ/ → г and /x/ → х.

**Reason:** Modern Ukrainian щ represents the fricative-plus-affricate sequence [ш]+[ч], not a single affricate. The Encyclopedia of Modern Ukraine and the Journal of the IPA Ukrainian description document this correspondence. The existing longest-match adapter can preserve the exact sequence without changing isolated segment mappings. This is target orthography, not a Lao phonological claim.

**Evidence:** SRC-ESU-SHCH, SRC-JIPA-UKRAINIAN; claim CLM-UA-SHCH-SEQUENCE.

## D-012 — Canonical tied IPA for the Lao alveolo-palatal affricate

**Decision:** Render the core Lao affricate ຈ as `t͡ɕ` in ClippyFirst's canonical IPA output. Continue accepting un-tied `tɕ` as an IPA correspondence alias for adapter inputs and external references.

**Reason:** The IPA chart uses tie-bar notation to represent an affricate as a single segment. ClippyFirst therefore adopts `t͡ɕ` as the canonical source IPA for ຈ and continues accepting untied `tɕ` as an input alias. The 100-word reference comparison exposed a notational mismatch; the resulting raw CER/exact-match change is a notation-normalization effect, not evidence of improved phonological accuracy. Future comparator reporting normalizes optional tie bars and keeps the raw allograph difference separately visible.

**Evidence:** SRC-IPA-CHART; claim CLM-IPA-AFFRICATE-TIE-BAR; benchmark [42374547901](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42374547901).

## D-013 — Withhold independent tone for potential initial minor /a/ syllables

**Decision:** When an initial unmarked short open-/a/ syllable is followed by a major-weighted syllable in the same unspaced orthographic token, preserve segmental IPA but mark its independent tone as analysis-dependent. Do not assign a neutral tone category or invent a tone contour from orthographic shape alone.

**Reason:** Ueda (1994, p. 113) describes an exceptional non-final open /a/ syllable in central Vientiane polysyllabic words as unstressed and tone-neutral (the article is based on one 46-year-old Haysok informant). Enfield (2007, §3.1, pp. 33–34) models minor C₀V₀ syllables as lacking distinctive tone independent of the major syllable, restricts V₀ to short /a, i, u/, and notes a restricted C₀ onset subset with palatal/velar nasals absent. The orthographic parser cannot prove lexical minor-syllable status or the full C₀ inventory. The implementation therefore flags only a conservative structural candidate, excludes known palatal/velar nasal onsets, and withholds tone rather than asserting that every matching spelling is definitely minor.

**Evidence:** SRC-UEDA; SRC-ENFIELD; claim CLM-LAO-POTENTIAL-MINOR-OPEN-A; regression tests for the candidate selector and monosyllabic/following-weight counterexample.


## D-014 — Hybrid deterministic profile is the primary ClippyFirst engine

**Decision:** Make `hybrid-deterministic` the default profile for the Python API, CLI rules path and browser engine. Keep Vientiane phonology as the base analysis and apply only the explicit, deterministic, evidence-gated MekongPhon aggregate correspondences. Retain `vientiane` and `mekongphon-reference` as explicit compatibility/comparison profiles. The optional Neural adapter is not part of the default transcription path.

**Reason:** The hybrid profile combines the Vientiane-oriented structural and tonal analysis with the already reviewed train-split aggregate correspondences, without runtime model downloads, word-level dictionary lookups or neural inference. The 100-entry benchmark supports reference-relative performance on that bounded set, but does not establish independent phonetic accuracy or universal Neural-level performance. Unknown or unsupported cases remain fail-closed.

**Acceptance:** Python API, CLI and browser defaults all select `hybrid-deterministic`; explicit Vientiane selection reproduces the prior baseline; regression tests and exact-head hosted Verify pass. This is an engine-default decision, not a linguistic release approval.

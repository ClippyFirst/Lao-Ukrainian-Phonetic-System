# Ukrainian target

The canonical Ukrainian inventory is external: ClippyFirst/Ukrainian-Phonetic-Inventory. This repository does not duplicate it.

Pipeline:

**Lao orthography → Lao phonology → IPA → Ukrainian feature space → candidate ranking → Ukrainian orthography**

not:

**Lao → Russian Cyrillic → Ukrainian Cyrillic**.

## Shared Ukrainian practical conventions

These are project-wide target-language decisions applied only after source phonology has produced IPA or an explicitly typed phonetic result. They are not direct source-grapheme substitutions and do not claim to be a new official Ukrainian standard.

- Aspiration is retained with the ASCII apostrophe after the corresponding Ukrainian consonant: /kʰ tʰ pʰ/ → к' т' п'. The source IPA continues to preserve aspiration independently.
- Foreign /h/ → г; hard /ɡ/ → ґ; genuine /x/ → х. These distinctions must not be collapsed.
- /t͡s/ → ц; /d͡z/ → дз; /t͡ʃ/ → ч; /d͡ʒ/ → дж.
- Alveolo-palatal /tɕ/ (also /t͡ɕ/) → ч; voiced /dʑ/ (also /d͡ʑ/) → дж as explicit target approximations.
- Postalveolar fricatives /ʃ ʒ/ → ш ж.
- Contrastive palatalization is preserved where Ukrainian orthography supports it: /tʲ dʲ nʲ lʲ rʲ/ → ть дь нь ль рь. Exact word-level spelling may require contextual Ukrainian orthographic rules.
- A glottal stop /ʔ/ is not aspiration and does not trigger the apostrophe rule.
- Do not turn a sequence of two consonants into an affricate unless the source phonological analysis identifies an affricate.
- Tone, vowel length and syllable boundaries remain explicit in the analysis; they are not silently reinterpreted as Ukrainian stress or doubled letters.

## Lao-specific decisions

- /ŋ/ → нг.
- /tɕ/ → ч; this is the current Lao palatal-affricate project correspondence.
- /ɯ/ → и as a project approximation; uncertainty remains visible in the IPA layer.
- Vowel quantity remains analytical rather than automatically doubling vowels.
- /h/ → г is a target-language approximation, not a claim that Lao /h/ and Ukrainian /ɦ/ are phonetically identical.

The Russian system remains a comparator, never the source of Ukrainian output.

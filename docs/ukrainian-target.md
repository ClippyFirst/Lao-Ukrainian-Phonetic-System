# Ukrainian target

The canonical Ukrainian inventory is external: ClippyFirst/Ukrainian-Phonetic-Inventory. This repository does not duplicate it.

Pipeline:

**Lao orthography → Lao phonology → IPA → Ukrainian feature space → candidate ranking → Ukrainian orthography**

not:

**Lao → Russian Cyrillic → Ukrainian Cyrillic**.

Main project-level refinements:

- /kʰ pʰ tʰ/ → к п т rather than Russian кх пх тх;
- /h/ → г as a project-specific practical approximation;
- /ŋ/ → нг;
- /tɕ/ → ч rather than Russian ть;
- /ɯ/ → и rather than Russian ы;
- vowel quantity remains analytical rather than automatically doubling vowels.

Tone is retained as a separate suprasegmental field and is not converted automatically into Ukrainian stress.

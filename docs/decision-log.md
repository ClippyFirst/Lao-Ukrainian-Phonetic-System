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

**Decision:** Keep the IPA-first phonetic method as the default and add a user-selected, independent orthographic adapter from the provisional CLDR Lao-Latin/UNGEGN string to Ukrainian. Do not feed romanization into the phonetic IPA adapter or silently switch methods.

**Reason:** The two paths answer different questions. The phonetic path models pronunciation; the fallback renders a Latin spelling when a user wants a deterministic but less informative alternative. Explicit separation prevents a romanized spelling from being presented as verified pronunciation.

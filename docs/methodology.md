# Methodology

Primary scope: contemporary Standard Lao with a Vientiane-oriented reference model where supported. Regional, historical and Tai varieties are not silently mixed into the core.

Pipeline:

**Unicode → normalization → graphemic parsing → syllable structure → consonant class → vowel/length → live/dead → tone → phonology → IPA → Ukrainian target → practical orthography**

Critical separations:

- grapheme ≠ phoneme;
- consonant class ≠ phonetic realization;
- tone mark ≠ tone;
- tone ≠ Ukrainian stress;
- Unicode order ≠ phonological order;
- structural generation ≠ lexical attestation;
- phonemic IPA ≠ surface phonetics;
- Russian/Serbian/Bulgarian output ≠ Ukrainian source-of-truth.

Lao-specific handling includes context-sensitive ອ, structural ຳ, sequence-like ໜ/ໝ, and a separate Pali/Sanskrit namespace.

The Ukrainian target is the external canonical inventory. Comparative Cyrillic systems are evidence and diagnostics, not hidden source-of-truth tables.


## Optional romanization-to-Ukrainian mode

The service offers a second, explicitly lower-information route alongside the primary phonetic method:

- **Phonetic (default):** Lao → structural/phonological analysis → IPA → Ukrainian practical adaptation.
- **By romanization:** Lao → the existing provisional CLDR Lao-Latin/UNGEGN string → a separate Latin-spelling-to-Ukrainian orthographic adapter.

The optional adapter consumes only the output of `romanizeLao()`. It does not feed, replace, or modify the IPA-first phonetic engine. The user selects the method in the Ukrainian result card; the service does not silently switch methods. The copy action copies the currently selected Ukrainian result, while the romanization intermediate and IPA remain separately inspectable.

The adapter applies longest sequences first: `kh → кх`, `th → тх`, `ph → пх`, `ch → ч`, `ng → нг`. Individual letters map as follows: `a а, b б, c к, d д, e е, f ф, g ґ, h г, i і, j дж, k к, l л, m м, n н, o о, p п, q к, r р, s с, t т, u у, v в, w в, x кс, y й, z з`. The CLDR marked vowels `é`, `è`, and `ô` map to `е`, `е`, and `о`. Punctuation, whitespace and digits are preserved; unsupported characters remain visible and produce a partial status.

These are project-defined orthographic correspondences for the Latin spelling, not an official Ukrainian standard and not phonetic equivalences. The romanization route cannot restore tone, vowel length, pronunciation, or context that the Latin representation does not encode. The upstream CLDR implementation is itself a constrained provisional subset, not a full ICU transform interpreter. A complete romanization result therefore does not imply a verified pronunciation.

The adapter and selector are covered by deterministic unit and structural UI tests. Those tests establish software behavior, not linguistic accuracy or completeness of the provisional CLDR profile.

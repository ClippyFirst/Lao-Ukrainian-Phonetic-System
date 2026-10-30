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

The service offers a second, explicitly lower-information method alongside the primary phonetic method:

- **Phonetic (default):** Lao → structural/phonological analysis → IPA → Ukrainian practical adaptation.
- **By romanization:** Lao → provisional CLDR Lao-Latin/BGN transform (with the profile currently identified as UNGEGN) → independent romanized-syllable parser → Ukrainian syllable assembly.

The second route is not a letter-by-letter Latin-to-Cyrillic transliterator. Its adapter consumes only the romanized string and attempts to parse each segment into a **syllable onset, vowel nucleus and coda**. The target Ukrainian syllable is assembled from those three components. It does not consume IPA, call the phonetic target adapter, or change the IPA-first engine. The user selects the method explicitly; there is no silent fallback. Input rejected by Lao validation is not passed through the romanization method. The main copy action follows the selected Ukrainian result.

### Syllable-level mapping policy

The current [CLDR Lao-Latin transform](https://github.com/unicode-org/cldr/blob/main/common/transforms/Lao-Latin.xml) is provisional and based on the BGN/PCGN 1966 Lao romanization material reproduced in the [Estonian Institute of Language / UNGEGN status report](https://eki.ee/wgrs/rom2_lo.pdf). That report explicitly distinguishes syllable-initial and syllable-final consonant spellings, and documents the vowel nuclei. It also states that no Lao romanization system has been approved at UN conferences and that Laos has no national romanization system. Accordingly, the project labels this route as a provisional romanization-based method, not as an official or universal standard.

The project mapping table is position-sensitive:

| Component | Romanized form | Ukrainian target |
|---|---|---|
| Onset | `kh`, `th`, `ph` | `кг`, `тг`, `пг` |
| Onset | `ch`, `ng`, `gn` | `ч`, `нг`, `нь` |
| Onset | `k s x d t n b p f m y r l v h` | `к с кс д т н б п ф м й р л в г` |
| Nucleus | `a i u ou o é è ô eu` | `а і и у о е е о е` |
| Nucleus | `ia ua oua ai ao am` | `іа уа уа ай ао ам` |
| Coda | `k ng y t n p m r l` | `к нг й т н п м р л` |
| Coda | `d b` | `т п` |
| Coda | `v` | `о` (or `оу` after `i`) |
| Coda | `h` | `г` |

**The project-wide romanization policy is `h → г` in every position.** It is not overridden inside `kh`, `th`, or `ph`: those onsets are assembled as `кг`, `тг`, and `пг`. This rule applies only to the romanization route; the phonetic route continues to use the existing IPA-to-Ukrainian target correspondences.

For preposed Lao vowels, the CLDR output can retain vowel-before-consonant order. The syllable adapter recognizes the documented preposed-vowel patterns and assembles Ukrainian in onset-before-vowel order. The short `a` left after some literal CLDR transforms is treated as a transform artefact only in those recognized preposed patterns. Position-sensitive final mappings follow the cited BGN/PCGN table; in particular, `d` and `b` become `t` and `p` in coda position, and final `v` is rendered as `o` (or `ou` after `i`).

The segmenter uses dynamic parsing of the romanized string. If a complete unique syllable parse is not available, or if multiple parses are possible, the affected segment is retained in visible brackets and the result is marked `PARTIAL`. It does not guess word boundaries from spaces: Lao spaces are phrase-level, and romanization can be ambiguous when multiple syllables are concatenated without a delimiter. This remains a constrained syllable adapter, not a validated lexical segmenter.

These mappings are explicit project policy for the romanized spelling, not a claim that the romanization preserves pronunciation. This route cannot restore tone, vowel length, consonant-class distinctions, or any other information absent from the Latin form. The upstream CLDR implementation is itself a constrained provisional subset, not a full ICU transform interpreter. A complete software parse therefore does not imply a verified pronunciation.

The adapter and selector are covered by deterministic tests for onset/nucleus/coda parsing, position-sensitive finals, preposed vowels, the `h → г` invariant, ambiguity withholding, and UI wiring. These tests establish software behavior for the implemented subset, not linguistic accuracy or completeness of the CLDR profile.

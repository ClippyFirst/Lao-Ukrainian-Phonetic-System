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
- **By romanization:** Lao → provisional CLDR Lao-Latin/BGN transform → source-grapheme/romanization crosswalk → independent romanized-syllable parser → Ukrainian syllable assembly.

The second route is not a letter-by-letter Latin-to-Cyrillic transliterator. It parses the romanized string into a **syllable onset, vowel nucleus and coda**, while checking each parsed onset against the original Lao onset grapheme. This crosswalk is essential because a Latin digraph can encode one Lao phoneme rather than two independent consonants. The route does not consume the IPA string or call the phonetic target adapter; it uses the source grapheme registry and documented phonological correspondences to validate the romanized onset. The IPA-first engine remains unchanged. The user selects the method explicitly; there is no silent fallback. Input rejected by Lao validation is not passed through the romanization method. The main copy action follows the selected Ukrainian result.

### Syllable-level mapping policy

The current [CLDR Lao-Latin transform](https://github.com/unicode-org/cldr/blob/main/common/transforms/Lao-Latin.xml) is provisional and based on the BGN/PCGN 1966 Lao romanization material reproduced in the [Estonian Institute of Language / UNGEGN status report](https://eki.ee/wgrs/rom2_lo.pdf). That report explicitly distinguishes syllable-initial and syllable-final consonant spellings, and documents the vowel nuclei. It also states that no Lao romanization system has been approved at UN conferences and that Laos has no national romanization system. Accordingly, the project labels this route as a provisional romanization-based method, not as an official or universal standard.

The project mapping table is position-sensitive:

| Component | Romanized form | Ukrainian target |
|---|---|---|
| Onset | `kh` from ຂ/ຄ | `к'` (aspirated /kʰ/) |
| Onset | `th` from ຖ/ທ | `т'` (aspirated /tʰ/) |
| Onset | `ph` from ຜ/ພ | `п'` (aspirated /pʰ/) |
| Onset | `h` from ຫ/ຮ | `г` (/h/) |
| Onset | `ch`, `ng`, `gn` | `ч`, `нг`, `нь` |
| Onset | `k s x d t n b p f m y r l v` | `к с с д т н б п ф м й л л в` |
| Onset | `x` from ຊ | `с` (the BGN letter `x` is not /ks/) |
| Nucleus | `a i u ou o é è ô eu` | `а і и у о е е о е` |
| Nucleus | `ia ua oua ai ao am` | `іа уа уа ай ао ам` |
| Coda | `k ng y t n p m r l` | `к нг й т н п м р л` |
| Coda | `d b` | `т п` |
| Coda | `v` | `о` (or `оу` after `i`) |
| Coda | `h` | `г` |

**The former blanket rule `h → г` was linguistically wrong for BGN digraphs.** In `kh`, `th`, and `ph`, the letter `h` is part of the conventional spelling of aspirated Lao stops, not a separate /h/ segment. The correct project outputs are therefore `к'`, `т'`, and `п'`. A standalone `h` from Lao ຫ or ຮ represents /h/ and maps to `г`. The source-to-romanization check must agree before the Ukrainian onset is emitted; a mismatch or missing alignment is withheld as `PARTIAL`.

The CLDR transform also maps ຊ to `x`, but this `x` represents Lao /s/ and therefore maps to Ukrainian `с`, not `кс`. Modern ຣ defaults to /l/ in the project source registry and is rendered `л`; a historical or loanword /r/ reading is not guessed from the romanized letter alone. The crosswalk preserves the source grapheme so these aliases are not mistaken for literal Latin sounds.

The Lao syllable model does not license an arbitrary /k/+ /h/ onset cluster: the cited orthography reference describes only restricted labialized onsets as productive audible clusters and separately describes written high-class sequences with ຫ. Consequently, `kh` must not be expanded into `кг`; a genuine /h/ is rendered `г` only when the Lao source identifies an /h/ onset. The adapter does not invent a single-syllable `кг` sequence to satisfy a literal reading of Latin letters. Final `h` is not accepted as a Lao coda.

For preposed Lao vowels, the CLDR output can retain vowel-before-consonant order and can also leave a preposed marker before a postposed vowel nucleus (for example, `ékhôa`); the syllable adapter recognizes these patterns and assembles Ukrainian in onset-before-vowel order. The short `a` left after some literal CLDR transforms is treated as a transform artefact only in those recognized preposed patterns. The adapter parses the individual CLDR syllable forms `ékhôa` (`kh + ôa` → `кгао`) and `niav` (`n + ia + v` → `ніао`). When concatenated as `ékhôaniav` (as in `ເຂົ້າໜຽວ`), the boundary is ambiguous: `n` may be read as the preceding coda or the next onset, so the whole segment is withheld. An explicit boundary such as `ékhôa-niav` yields `кгао-ніао`. It also withholds `éku` because the provisional CLDR transform has deleted the Lao `ອ` that would distinguish the relevant vowel sequence. Position-sensitive final mappings follow the cited BGN/PCGN table; in particular, `d` and `b` become `t` and `p` in coda position, and final `v` is rendered as `o` (or `ou` after `i`).

The segmenter uses dynamic parsing of the romanized string. If a complete unique syllable parse is not available, or if multiple parses are possible, the affected segment is retained in visible brackets and the result is marked `PARTIAL`. It does not guess word boundaries from spaces: Lao spaces are phrase-level, and romanization can be ambiguous when multiple syllables are concatenated without a delimiter. This remains a constrained syllable adapter, not a validated lexical segmenter.

These mappings are explicit project policy for the romanized spelling, not a claim that the romanization preserves pronunciation. This route cannot restore tone, vowel length, consonant-class distinctions, or any other information absent from the Latin form. The upstream CLDR implementation is itself a constrained provisional subset, not a full ICU transform interpreter. A complete software parse therefore does not imply a verified pronunciation.

The adapter and selector are covered by deterministic tests for onset/nucleus/coda parsing, position-sensitive finals, preposed vowels, source-grapheme cross-checks, aspiration versus /h/, invalid final `h`, alias normalization, ambiguity withholding, and UI wiring. These tests establish software behavior for the implemented subset, not linguistic accuracy or completeness of the CLDR profile.

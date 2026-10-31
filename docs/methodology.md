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

## Tone-mark selector domain

The Vientiane-oriented selector applies written tone-mark rules only to **live/open syllables**. A marked dead/checked syllable (short-vowel syllable or a syllable closed by a stop) does not receive a tone from this matrix; its tone remains unresolved and the analysis is marked `ANALYSIS DEPENDENT`. This is a conservative domain restriction, not a claim that every possible string containing a tone mark is a well-formed Lao syllable.

The two common marks, `mai ek` (່) and `mai tho` (້), retain their class-dependent live-syllable mappings. The less common `mai ti` (໊) and `mai catawa` (໋) are represented only for middle-class onsets: high-falling and low-rising, respectively. Appen Butler Hill's *Language Specific Peculiarities Document for Lao as Spoken in Laos* (p. 14) explicitly describes all tone marks as used with open syllables and identifies the latter two as rare in modern writing and restricted to mid-class consonants. The SEAsite Vientiane chart independently places its two common tone-mark columns under live syllables. See the source-linked claims `CLM-LAO-VIENTIANE-TONE-MATRIX` and `CLM-LAO-TONE-RARE-MARKS` in the evidence registry.

For tone classification, **phonetic vowel length and rhyme type are separate properties**. A short diphthong can form an open/live rhyme; the short/long label alone must not force it into the dead class. The `AM` spelling includes a nasal coda and is live for the same reason as an overt sonorant-final syllable. The canonical vowel registry records `nucleus_type` and `coda_class`, and both engines use those fields before falling back to monophthong length. Ueda (1994, pp. 96–97) describes VV rhymes as permitting an absent coda and contrasts them with short monophthongs, which generally require a coda; the source-linked implementation claim is `CLM-LAO-OPEN-RHYMES`.


The Ukrainian target is the external canonical inventory. Comparative Cyrillic systems are evidence and diagnostics, not hidden source-of-truth tables.


## Optional romanization-to-Ukrainian mode

The service offers a second, explicitly lower-information method alongside the primary phonetic method:

- **Phonetic (default):** Lao → structural/phonological analysis → IPA → Ukrainian practical adaptation.
- **By romanization:** Lao → provisional CLDR Lao-Latin/BGN transform → source-grapheme/romanization crosswalk → independent romanized-syllable parser → Ukrainian syllable assembly.

The second route is not a letter-by-letter Latin-to-Cyrillic transliterator. It parses the romanized string into a **syllable onset, vowel nucleus and coda**, then checks all three against the original Lao syllable: the onset grapheme must agree with the romanized onset, the source vowel-structure ID must permit the parsed CLDR nucleus, and a supported coda grapheme must agree with the CLDR coda output. This source evidence can resolve ambiguities that Latin spelling alone cannot, including `kam` as either `ka+m` (an A nucleus plus final ມ) or `k+am` (the single AM vowel nucleus). Without the original Lao structure, the ambiguous romanized form remains partial. A Latin digraph can encode one Lao phoneme rather than two independent consonants, and CLDR's transform is not position-sensitive for every consonant. The route does not consume the IPA string or call the phonetic target adapter; it uses the source grapheme and vowel registries plus documented orthographic correspondences to validate onset, nucleus and supported coda. The IPA-first engine remains unchanged. The user selects the method explicitly; there is no silent fallback. Input rejected by Lao validation is not passed through the romanization method. The main copy action follows the selected Ukrainian result.

### Syllable-level mapping policy

The current [CLDR Lao-Latin transform](https://github.com/unicode-org/cldr/blob/7afa5cdb6b7fe7ae65f934c6dbaa374f25b5a616/common/transforms/Lao-Latin.xml) is provisional and based on the BGN/PCGN 1966 Lao romanization material reproduced in the [Estonian Institute of Language / UNGEGN status report](https://eki.ee/wgrs/rom2_lo.pdf). That report explicitly distinguishes syllable-initial and syllable-final consonant spellings, and documents the vowel nuclei. It also states that no Lao romanization system has been approved at UN conferences and that Laos has no national romanization system. Accordingly, the project labels this route as a provisional romanization-based method, not as an official or universal standard.

The project mapping table is position-sensitive:

| Position | Lao source grapheme | CLDR form | Ukrainian target |
|---|---|---|---|
| Onset | ກ | `k` | `к` |
| Onset | ຂ/ຄ | `kh` | `к'` (aspirated /kʰ/) |
| Onset | ງ | `ng` | `нг` |
| Onset | ຈ | `ch` | `ч` |
| Onset | ສ | `s` | `с` |
| Onset | ຊ | `x` | `с` (not literal /ks/) |
| Onset | ຍ | `gn` | `нь` |
| Onset | ດ/ຕ | `d/t` | `д/т` |
| Onset | ຖ/ທ | `th` | `т'` (aspirated /tʰ/) |
| Onset | ນ | `n` | `н` |
| Onset | ບ/ປ | `b/p` | `б/п` |
| Onset | ຜ/ພ | `ph` | `п'` (aspirated /pʰ/) |
| Onset | ຝ/ຟ | `f` | `ф` |
| Onset | ມ | `m` | `м` |
| Onset | ຢ | `y` | `й` |
| Onset | ຣ/ລ | `r/l` | `л` (modern default for ຣ) |
| Onset | ວ | `v` | `в` |
| Onset | ຫ/ຮ | `h` | `г` (/h/, not aspiration) |
| Onset | ໜ | `n` | `н` (silent ຫ + ນ) |
| Onset | ໝ | `m` | `м` (silent ຫ + ມ) |
| Nucleus | vowel combinations | CLDR sequences | project-defined Ukrainian vowel complexes |
| Coda | ກ/ງ | `k/ng` | `к/нг` |
| Coda | ດ/ບ | `d/b` | `т/п` |
| Coda | ນ/ມ | `n/m` | `н/м` |
| Coda | ຍ | `gn` (CLDR alias; BGN final form is `y`) | `й` |
| Coda | ວ | `v` | `о` (or `оу` after `i`) |

**The former blanket rule `h → г` was linguistically wrong for BGN digraphs.** In `kh`, `th`, and `ph`, the letter `h` is part of the conventional spelling of aspirated Lao stops, not a separate /h/ segment. The correct project outputs are therefore `к'`, `т'`, and `п'`. A standalone `h` from Lao ຫ or ຮ represents /h/ and maps to `г`. The source-to-romanization check must agree for onset, source vowel ID and supported coda before the Ukrainian syllable is emitted; a mismatch or missing alignment is withheld as `PARTIAL`.

The vowel crosswalk is also position-aware and is checked against the source parser's `VOWEL:<ID>` trace:

| Source vowel IDs | CLDR nucleus accepted by the adapter | Ukrainian nucleus |
|---|---|---|
| A, A2, AA | `a` | а |
| I, II | `i` | і |
| Y, YY | `u` | и |
| U, UU | `ou` | у |
| E, EE | `é` | е |
| AE, AEE | `è` | е |
| O, OO | `ô` | о |
| AW, AWW_SHORT_ALT, AWW | `o` | о |
| OE, OEE | `eu` | е |
| IA, IA_LONG | `ia` | іа |
| UA, UA_LONG | `ua` | уа |
| UO, UO_LONG, UO_SHORT_ALT | `oua` | уа |
| AI, AI2 | `ai` | ай |
| AW_LONG | `ao` or transform-shaped `ôa` | ао |
| AM | `am` | ам |

The romanization collapses distinctions such as short versus long vowels; this table validates the represented nucleus but does not reconstruct lost length. Source IDs whose material is deleted or not represented by the supported CLDR subset (for example, medial `ອ` cases) are withheld rather than inferred. The target vowel spelling is an explicit project orthographic policy, not a claim of phonetic equivalence.

The CLDR transform also maps ຊ to `x`, but this `x` represents Lao /s/ and therefore maps to Ukrainian `с`, not `кс`. Modern ຣ defaults to /l/ in the project source registry and is rendered `л`; a historical or loanword /r/ reading is not guessed from the romanized letter alone. The crosswalk preserves the source grapheme so these aliases are not mistaken for literal Latin sounds.

The Lao syllable model does not license an arbitrary /k/+ /h/ onset cluster: [Richard Ishida's Lao Orthography Notes](https://r12a.github.io/scripts/laoo/lo.html) describes only restricted labialized onsets as productive audible clusters and separately describes written high-class sequences with ຫ. Consequently, `kh` must not be expanded into `кг`; a genuine /h/ is rendered `г` only when the Lao source identifies an /h/ onset. The adapter does not invent a single-syllable `кг` sequence to satisfy a literal reading of Latin letters. A genuine /k/ syllable followed by an independent /h/ onset remains two syllables: the supported Lao sequence `ກາຮາ` → `kaha` is assembled as `кага`, not reinterpreted as aspirated `kha`. Final `h` is not accepted as a Lao coda. **Important exception:** BGN/PCGN 1966 note 5 explicitly says that silent ຫ is generally omitted before sonorants and that ໜ/ໝ are abbreviated forms of ຫນ/ຫມ. The romanizer therefore removes the silent marker in the supported expanded forms ຫງ, ຫຍ, ຫນ, ຫມ, ຫລ and ຫວ, and treats ຫຼ as the /l/ form; the source parser preserves the written onset form while the crosswalk checks its underlying onset. The atomic ໜ/ໝ likewise cross-check as `n/m` → Ukrainian `н/м`, never as audible /h+n/ or /h+m/. BGN note 5 also lists an /r/ environment, but the current structural parser does not yet model ຫຣ as a high-class onset, so that case is deliberately not normalized by this implementation.

For preposed Lao vowels, the CLDR output can retain vowel-before-consonant order and can also leave a preposed marker before a postposed vowel nucleus (for example, `ékhôa`); the syllable adapter recognizes these patterns and assembles Ukrainian in onset-before-vowel order. The short `a` left after some literal CLDR transforms is treated as a transform artefact only in those recognized preposed patterns. The adapter parses the individual CLDR syllable forms `ékhôa` (`kh + ôa` → `к'ао`) and `niav` (`n + ia + v` → `ніао`). Without source evidence, `niav` has competing parses (`n + ia + v` versus `n + i` + `av`) and is withheld. With the original Lao syllable group, the crosswalk confirms ໜ as `n`, the `IA_LONG` nucleus as `ia`, and final ວ as `v`; the full `ເຂົ້າໜຽວ` sequence can therefore be resolved without inserting a guessed word boundary. The explicitly hyphenated romanization `ékhôa-niav` likewise yields `к'ао-ніао` when source syllable evidence is supplied. It also withholds `éku` because the provisional CLDR transform has deleted the Lao `ອ` that would distinguish the relevant vowel sequence. Position-sensitive final mappings follow the cited BGN/PCGN table; in particular, `d` and `b` become `t` and `p` in coda position, and final `v` is rendered as `o` (or `ou` after `i`).

The segmenter uses dynamic parsing of the romanized string. If a complete unique syllable parse is not available, or if multiple parses are possible, the affected segment is retained in visible brackets and the result is marked `PARTIAL`. It does not guess word boundaries from spaces: Lao spaces are phrase-level, and romanization can be ambiguous when multiple syllables are concatenated without a delimiter. This remains a constrained syllable adapter, not a validated lexical segmenter.

These mappings are explicit project policy for the romanized spelling, not a claim that the romanization preserves pronunciation. This route cannot restore tone, vowel length, consonant-class distinctions, or any other information absent from the Latin form. The upstream CLDR implementation is itself a constrained provisional subset, not a full ICU transform interpreter. A complete software parse therefore does not imply a verified pronunciation.

The adapter and selector are covered by deterministic tests for onset/nucleus/coda parsing, position-sensitive finals, preposed vowels, source-grapheme cross-checks, aspiration versus /h/, invalid final `h`, alias normalization, ambiguity withholding, and UI wiring. These tests establish software behavior for the implemented subset, not linguistic accuracy or completeness of the CLDR profile.


## Lao tone-mark storage order

The Lao orthography reference specifies that tone marks are stored after the base consonant or a superscript vowel sign; when an onset is written with multiple characters, the mark is attached to the second character. The AM sign `ຳ` is a spacing letter, so the tone mark precedes it (for example, `ກ່ຳ`). This storage order is distinct from the visual stacking performed by fonts. The parser now rejects a mark placed before a following combining vowel sign, after AM, after a coda, or before the onset. For malformed placement, it withholds IPA, tone, and Ukrainian output rather than normalizing the sequence into a plausible result. Valid forms such as `ກ່າ`, `ກິ່`, `ກ່ຳ`, `ຂວັ່ນ`, and `ຫຍ້າ` are preserved. This is an orthographic validation rule; it does not establish acoustic tone contours or independent pronunciation accuracy. Source: [Richard Ishida, Lao Orthography Notes](https://r12a.github.io/scripts/laoo/lo), sections on tone and code-point sequences.

## Restricted labialized onset inventory

The orthographic reference describes modern Lao syllables as `(C)w?V(C)`: one restricted onset class is written as a base consonant followed by `ວ`, with secondary labialization (`ʷ`) on the onset. The source lists eight phonological values: `tʷʰ`, `tɕʷ`, `kʷ`, `kʷʰ`, `ʔʷ`, `sʷ`, `ŋʷ`, and `lʷ`. The canonical `data/lao/onset_clusters.csv` registry records the eleven high/mid/low-class spellings and keeps tone class tied to the first consonant.

Clusters are accepted only when the following nucleus is unrounded. Where both a base-onset plus UO-long-open rhyme and a labialized-onset plus AA rhyme consume the same `Cວາ` spelling, the parser returns `AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY` and withholds IPA, tone, and target output. Rounded-nucleus cluster candidates are rejected. Preposed vowels are analyzed before the complete onset; silent high-class `ຫ` digraphs are recognized after the preposed vowel.

The IPA adapter preserves the source's superscript-labialization notation. No Ukrainian correspondence is registered for these `ʷ` sequences, so the system deliberately exposes the IPA analysis but withholds Ukrainian output (`EVIDENCE LIMITED`). This is a target-adaptation gap, not a claim that a Ukrainian spelling has been validated. The cluster fixture is a structural grammar control, not independent pronunciation gold.

Source: Richard Ishida, *Lao Orthography Notes*, syllable structure and onset sections (phonological inventory, spelling as base consonant + `ວ`, and tone-mark placement on the second character): https://r12a.github.io/scripts/laoo/lo.

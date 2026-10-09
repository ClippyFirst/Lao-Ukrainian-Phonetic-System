# Lao phonetic/transcription audit

## Scope

This audit targets failure modes that can produce a plausible-looking but wrong Ukrainian reading:

1. tone-class confusion;
2. silent high-class ຫ digraphs;
3. atomic ligatures ໜ / ໝ;
4. the dual role of ວ;
5. medial ອ as /ɔː/;
6. the restricted inventory of final consonants;
7. modern ຣ;
8. Ukrainian practical mapping of Lao /h/.
9. standalone ຽ and syllable-boundary preservation.

The project remains Vientiane-oriented. Lao tone values vary by dialect, and sources disagree on whether Vientiane should be analysed as five or six phonological tones. The system therefore exposes the tone rule used rather than pretending that one contour is universal.

## Findings and repairs

### 1. Inherent tone rules

The previous rule set incorrectly assigned the same unmarked live tone to middle- and high-class consonants and used an overly simplified dead-syllable matrix.

The revised rules follow the Vientiane-oriented teaching chart used by Northern Illinois University's Lao materials:

- high class + live → low-rising;
- middle class + live → low-rising;
- low class + live → high-rising;
- high/middle + dead short → high-rising;
- low + dead short → high-mid;
- high/middle + dead long → low-falling;
- low + dead long → high-falling;
- mai ek → high-mid;
- mai tho → low-falling for high class, high-falling for middle/low class;
- mai ti and mai catawa are restricted to the relevant middle-class pattern.

These are Vientiane-oriented phonological rules, not universal rules for every Lao variety.

### 2. Silent high-class digraphs

Forms such as ຫງ, ຫຍ, ຫນ, ຫມ, ຫລ/ຫຼ, and ຫວ contain a silent ຫ. It changes the tone class but does not add /h/ to the pronunciation.

Therefore:

- ຫນ... → /n.../, not /hn.../;
- ໜ... → /n.../;
- ຫມ... / ໝ... → /m.../;
- ຫຍ... → /ɲ.../;
- ຫງ... → /ŋ.../;
- ຫລ... / ຫຼ... → /l.../;
- ຫວ... → /ʋ.../.

### 3. ວ is not only /w/

Initial ວ is represented here as /ʋ/ with Ukrainian practical output в. Final ວ is /w/. In closed syllables, standalone ວ can also be part of the vowel /uːə/.

The engine now distinguishes initial /ʋ/, final /w/, the closed /uːə/ spelling, and the corresponding open spelling.

### 4. Medial ອ

ອ is normally a silent vowel carrier in onset position, but after another consonant it can represent long /ɔː/.

Examples used in adversarial tests include ອາ → /aː/, ອໍ → /ɔː/, ຈອກ → /tɕɔːk/, and ຫນອງ → /nɔːŋ/.

### 5. Final consonants

The final inventory was too permissive. Modern Lao does not use arbitrary consonant letters as codas.

The canonical registry now limits final consonants to the attested set: /p/ ບ, /t/ ດ, /k/ ກ, /m/ ມ, /n/ ນ, /ŋ/ ງ, /w/ ວ, /j/ ຍ, and /n/ ຣ in the loan/extended spelling context.

This prevents consonants such as ສ or ລ from being silently accepted as normal finals.

### 6. Modern ຣ

Modern Lao does not have a stable native /r/ reading for ຣ. It is associated with loans, historical spelling, and variant usage; /l/ is documented for modern Lao readings.

The system therefore uses /l/ as the default phonological value but marks ຣ as analysis-dependent, leaving /r/ available for explicitly foreign/historical cases.

### 7. Ukrainian practical output for /h/

The project policy maps Lao /h/ to Ukrainian г, rather than х. This is a phonetic/practical-transcription decision, not a claim that Ukrainian has a perfect one-to-one phoneme equivalent.

## Adversarial regression set

The regression suite now explicitly checks:

- ຂາ — high-class live syllable;
- ກາ — middle-class live syllable;
- ຄາ — low-class live syllable;
- ກ່າ, ກ້າ, ຄ້າ — tone-mark contrasts;
- ກັບ — checked short syllable with stop coda;
- ດວງ — closed /uːə/ spelling;
- ກວາງ — open /uːə/ spelling;
- ຫນອງ — silent high-class digraph;
- ໜາ — atomic high-class ligature;
- ຣະ — analysis-dependent modern ຣ;
- ຫາ — /h/ → Ukrainian г;
- carrier and invalid mixed-script cases.

## Source basis

The orthographic/phonological audit was checked against Richard Ishida's Lao orthography notes and character database, Northern Illinois University's SEAsite Lao teaching materials and Vientiane tone charts, and Lao phonology summaries documenting dialectal variation.

The implementation intentionally separates source evidence, IPA analysis, and Ukrainian practical-transcription policy so that a policy choice cannot masquerade as a Lao phonological fact.


### 8. Standalone ຽ and syllable boundaries

The vowel sign ຽ can occur without the preposed ເ in forms such as ວຽງ. The browser parser recognizes this structure as /iːə/ and parses ວຽງ as one syllable. Segmentation also rejects a postposed vowel sign as if it were a valid prefix before a later onset, and penalizes a false coda boundary when the following character is a vowel sign attached to the next onset. These are orthographic heuristics, not a substitute for lexical analysis.

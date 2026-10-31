# Sources and evidence

The source registry is data/evidence/sources.csv and claims are in data/evidence/claims.csv.

Priority:

1. Unicode Standard for encoding and orthographic structure;
2. descriptive grammars and phonological studies;
3. authoritative dictionaries and geographical-name references;
4. established Vientiane educational descriptions;
5. official Serbian/Bulgarian geographical-name sources as target-script controls;
6. secondary web reproductions only for locating and cross-checking legacy tables.

The Russian practical table is treated as a historical/practical source, not as phonological truth.

## Tone-mark evidence

The Vientiane tone selector's marked-syllable domain is source-gated rather than inferred from code. Appen Butler Hill's *Language Specific Peculiarities Document for Lao as Spoken in Laos* (2017), page 14, states that tone marks are used with open syllables; it identifies `໊` (`mai ti`) and `໋` (`mai catawa`) as rare in modern writing and limits them to mid-class onsets, with high-falling and low-rising values respectively. The SEAsite Vientiane tone chart shows the common `mai ek` and `mai tho` columns in the live-syllable portion of the matrix. These sources support selector conditions and categories, not acoustic measurements of individual speakers' surface contours. The canonical records are `SRC-LDC-LAO-LSP`, `SRC-SEASITE-TONECHART`, and `SRC-UEDA`; the implementation claims are `CLM-LAO-VIENTIANE-TONE-MATRIX` and `CLM-LAO-TONE-RARE-MARKS`.

Ueda's Vientiane study (1994, pp. 96–97) distinguishes VV rhymes (long vowels or diphthongs), which can occur without a final consonant, from short monophthongal rhymes, which generally require a final consonant. This is relevant to live/dead classification: an open diphthong must not be classified as dead merely because its nucleus lacks a monophthongal length marker. The project also treats the AM rhyme as live because its canonical row records a nasal coda. This is encoded in `nucleus_type` and `coda_class`, and guarded by `CLM-LAO-OPEN-RHYMES`.

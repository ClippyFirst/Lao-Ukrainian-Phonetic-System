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


## Unicode grapheme inventory

SRC-UNICODE-CHART-2026 is the Unicode Consortium's Unicode 18 Lao Names List. It establishes codepoint identity and official character names, not pronunciation. CLM-LAO-UNICODE-INVENTORY-2026 therefore supports inventory completeness and scope classification only. Modern Lao phonetic roles are separately grounded in SRC-ISHIDA-ORTHO-2026 and language-specific phonological sources; Pali/Sanskrit and Khmu entries are not promoted to modern Lao pronunciation rules.


## Independent sentence-domain stress corpus (not IPA evidence)

The HVULao_NLP 1,000-row raw-text split is used only to measure sentence-domain engine coverage, input rejection, runtime and output disagreement. The pinned source is [HaHVU/HVULao_NLP](https://github.com/HaHVU/HVULao_NLP) revision `ec8be4f1a541f3a5c76b4ebda39a9b2795d5c568`, file `Datatest1k/testorgin1000.txt`, Git blob SHA-1 `947448807484bb994877ae5d32cba1cfdd5e2d9b`; the dataset release is [Mendeley Data v2, DOI 10.17632/5zwym7kwn8.2](https://doi.org/10.17632/5zwym7kwn8.2), published under CC BY 4.0. Its paired annotations concern word segmentation/POS and do not provide IPA. Therefore it is not a phonetic gold source and must not support CER, accuracy or correctness claims. Reproducible aggregate results are documented in [the HVULao 1k three-engine stress report](research/HVULAO-1K-THREE-ENGINE-STRESS-2026-11-08.md).


## Native Lao digits and non-phonetic inline content

The W3C Lao Script Resources overview notes that Lao native digits are commonly used. The implementation preserves U+0ED0–U+0ED9 unchanged as explicit passthrough units. This is a handling policy, not a pronunciation rule: digits receive no IPA and do not enter the Ukrainian phonetic adapter. The source establishes the script usage; the passthrough behavior is a project decision recorded as `CLM-LAO-DIGITS-PASSTHROUGH`.

## Minor syllable scope

Ueda (1994, p. 112) describes a restricted non-final CV- light syllable in polysyllabic Vientiane words, with short open /a/ and no final consonant; it is unstressed and lacks a distinctive lexical tone contour. Enfield (2007, §3.1, pp. 33–34) describes a related C0V0 minor-syllable slot, with restricted consonant and vowel inventories and no independent tone contrast. The sources differ in corpus and scope: Ueda's study is a single central-Vientiane informant, while Enfield's grammar describes semi-rural conversational speech. The current engine therefore flags only its narrow potential initial open-/a/ pattern as unresolved; it does not assign a neutral tone or generalize the pattern to every open short vowel. The corresponding claim is `CLM-LAO-POTENTIAL-MINOR-OPEN-A`.


## Coda-role cross-check: Ishida (2026) and the Lao Script Generation Panel (2017)

The Ishida orthography notes contain an internal discrepancy: the consonant-class chart includes ຢ in the coda area, while the explicit final-position list omits it and the IPA correspondence table assigns final /j/ to ຍ. A separate community-reviewed Lao Script Generation Panel proposal (ICANN, 2017) provides a useful, but domain-scoped, cross-check. Section 5.1 (printed p. 4) enumerates 14 final consonant graphemes and excludes ຢ; Appendix C (printed p. 23), developed by the Lao Text-to-Speech team at the e-Government Center of the Ministry of Posts and Telecommunications, maps initial /j/ to ຢ and final /j/ to ຍ. The proposal also explains that orthographic reforms reduced some Indic-loan final spellings relative to the phonology of spoken Lao.

This supports the conservative parser decision to withhold ຢ as a coda (including the spelling ກາຢ). It does not make the ICANN list a general Lao phonological inventory: it is a DNS root-zone label specification, includes additional finals such as ຊ ທ ຟ ສ ລ, and explicitly simplifies or omits language spelling constraints. Keep the nine-item Ishida modern orthographic profile, the broader ICANN DNS-label repertoire, and historical/loanword spellings as separate evidence domains until a modern Lao spelling authority or specialist adjudicates their relation. No production inventory or runtime behavior changes. Claims: CLM-LAO-ICANN-CODA-ROLE-SCOPE and CLM-LAO-ISHIDA-CODA-CHART-CONFLICT.

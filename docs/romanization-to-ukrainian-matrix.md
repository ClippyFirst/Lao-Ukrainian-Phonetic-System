# Lao romanization → Ukrainian orthographic matrix

**Status:** PARTIAL — direct Latin input is now supported for the BGN/PCGN-derived CLDR profile and a bounded ALA-LC 2012 subset; ambiguity, unsupported spellings and missing distinctions remain explicit.
**Primary variety:** contemporary Standard Lao; Vientiane-oriented phonetic mode remains separate.

## Standard selection

Use the **BGN/PCGN 1966 Lao romanization convention as represented by the Unicode CLDR Lao-Latin transform** as the project's operational romanization profile. This is the best-supported practical choice for a reproducible romanization route, not an assertion that Laos has an official national romanization standard.

The UK Government/PCGN Laos Toponymic Factfile (2023) explicitly says there is no official romanization system in use for current Lao orthography; it states that the BGN/PCGN system agreed in 1966 continues to be used by PCGN in the absence of a domestic official system. The project therefore retains the label **provisional BGN/PCGN-derived CLDR Lao-Latin**, not “official Lao”.

Sources:
- https://www.gov.uk/government/publications/romanization-systems
- https://assets.publishing.service.gov.uk/media/64f9c99f7a4b4f0012f6d8a5/Laos_Toponymic_Factfile.pdf



### Current national-standard development status (UNGEGN 2025)

The earlier 2023 PCGN Factfile statement that UNGEGN was working with Lao authorities is now superseded by a more specific 2025 Working Group on Romanization Systems report. The report says that, as reported at the 2023 session, WGRS had been invited to review a draft Lao Romanization System prepared by the National Geographic Department of Lao PDR and had made recommendations. It further records that, as of July 2024, Lao PDR was finalising a draft of toponymy guidelines; WGRS hoped the system would be submitted for consideration at the 2027 UNGEGN session. This is evidence of an active government-led draft process, **not evidence that a final national or UN-endorsed system had already been adopted**. The project must continue to label BGN/PCGN-derived CLDR as provisional and must not pre-empt the draft's eventual contents. Re-check the WGRS/UNGEGN record when a newer submission or decision appears.

Primary source: [UNGEGN Working Group on Romanization Systems, GEGN.2/2025/26/CRP.26, “Progress on romanization systems” (Lao section)](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_26_CRP26_item5c.pdf). The [2025 session summary](https://digitallibrary.un.org/record/4076754/files/GEGN.2_2025_26-EN.pdf) confirms that the Working Group's report covered Lao developments.



### Lao draft chronology and UNGEGN status distinction

The record is longer-running than the 2025 report alone suggests. Earlier WGRS records show that a draft instruction on toponymy containing romanization guidelines was awaiting Lao approval in 2016; WGRS reviewed a National Geographic Department draft in 2018 and raised concrete technical questions (including the use of y for lengthened i, syllable-final voicing after long vowels, and possible table errors); the 2019 and 2021 WGRS reports record recommendations and continuing Lao-government consideration; the 2023 session records a draft Toponymic Guidelines in two parts and a request for inter-ministerial feedback; and the 2025 WGRS report says that, as of July 2024, Lao PDR was finalising a draft of the guidelines, with hoped-for UNGEGN plenary consideration in 2027. This is a continuing draft-development process, not a newly created 2025 system and not proof of national adoption.

A second distinction is essential: the current UNGEGN romanization-status page places Lao under **“Other languages/scripts”**, not among the 30 systems it identifies as recommended by the United Nations. Its linked Lao status paper is Version 4.0 (September 2013) and explicitly says that no Lao romanization system had been approved at UN conferences and that Laos had no national romanization system at that time; it describes the BGN/PCGN 1966 system. Thus the presence of a Lao entry in the UNGEGN status index must not be misreported as UN approval. The UNGEGN process page states that a proposed system becomes a UN standard only after the formal review, plenary endorsement and ECOSOC adoption stages.

Sources:
- [UNGEGN WGRS Lao status paper, Version 4.0 (September 2013)](https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/wgrr4lao.pdf), especially p. 1.
- [WGRS meeting report, 20 March 2018](https://arhiiv.eki.ee/wgrs/wgr18rep.htm), Lao section.
- [WGRS report, 2019 session, GEGN.2/2019/11/CRP.11](https://unstats.un.org/UNSD/geoinfo/UNGEGN/docs/1st-session/GEGN.2_2019_11_CRP.11_WG_Romanization_Systems-full-report.pdf), Lao section.
- [WGRS report, 2021 session, GEGN.2/2021/93/CRP.93](https://unstats.un.org/unsd/ungegn/sessions/2nd_session_2021/documents/GEGN.2_2021_93_CRP93_15_WGRSreport.pdf), Lao section.
- [WGRS minutes, 3 May 2023](https://unstats.un.org/unsd/ungegn/working_groups/wg5/documents/WGRS_minutes_3_May_2023.pdf), Lao section.
- [WGRS report, 2025 session, GEGN.2/2025/26/CRP.26](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_26_CRP26_item5c.pdf), Lao section.
- [UNGEGN romanization-status index](https://unstats.un.org/unsd/ungegn/romanization/) and [UNGEGN approval process](https://unstats.un.org/unsd/ungegn/meetings/Bureau_Divisions/documents/UNGEGN_WGRS_Approval_process-WG_Reviewed_28_May_26.pdf).

**Project consequence:** keep BGN/PCGN-derived CLDR explicitly provisional and distinct from the draft under development. Do not implement the Lao draft until an authoritative current table and evidence of its national status are available; do not label it UN-approved merely because the UNGEGN index links a 2013 Lao status paper.


## Route separation

- **Romanization mode:** Lao orthographic syllable → CLDR Lao-Latin → source-aware onset/nucleus/coda crosswalk → Ukrainian practical syllable. It does not infer pronunciation, tone or length that the romanization does not encode.
- **Phonetic mode:** Lao orthographic analysis → source phonology → IPA → Ukrainian target adaptation. It may withhold unsupported units.
- The romanization route must not consume IPA as its source and must not fall back to the phonetic result.

## Direct romanization input

The browser now accepts a romanized Lao string directly; the user does not need to provide Lao script first. The input profile can be selected as **BGN/PCGN 1966 / CLDR Lao-Latin**, **ALA-LC 2012**, or **automatic**. Automatic selection uses distinctive ALA-LC diacritics, modifier-apostrophe vowels, `oe`, and the ALA-LC palatal-nasal spelling before a vowel; otherwise it selects the BGN/PCGN-derived profile. This is a convenience heuristic, not a complete standard classifier: when the source convention is known, users should select it explicitly.

The BGN/PCGN profile uses the existing onset–nucleus–coda parser. The ALA-LC profile normalizes the table's implemented vowel spellings: `u`/`ū`, `uʼ`/`ūʼ`, `e`/`ē`, `æ`/`ǣ`, `oe`/`ōe`, `ia`/`īa`, `ua`/`ūa`, `ai`/`āi`, `ao` and `am`. Quantity is collapsed in Ukrainian output. `ny` remains the ALA-LC palatal-nasal onset and is not rewritten to BGN/PCGN `gn`. Its final parser is separate from BGN/PCGN: finals are `k`, `ng`, `t`, `p`, `n`, `m`, plus `o` after a vowel for final `ວ`. The LOC table's parenthesized final values are romanized as the value shown in parentheses (e.g. final `ຣ/ລ` appear as `n`, not `r/l`), so the source consonant cannot be recovered from Latin text alone. Source-aware ALA-LC validation uses the LOC initial spellings as well (`ຊ` → `s`, `ຍ` → `ny`) rather than the BGN/CLDR aliases (`x`, `gn`). This is **not** a complete ALA-LC implementation. Initial `ʻ` has no approved Ukrainian target mapping yet; medial `w` clusters, contextual `ວ` behavior and loanword/word-boundary rules remain unsupported or partial. A table spelling such as `būak` can remain ambiguous between one `ūa` syllable and multiple syllables without source boundaries, so it is withheld. The normalizer never claims that a normalized form is the original romanization.

For direct BGN/PCGN input, strict boundary mode applies PCGN note 4: an initial onsetless vowel may appear at the beginning of a word, while a medial onsetless syllable requires the prescribed hyphen. This resolves the documented official example Viangchan as v + ia + ng / ch + a + n without allowing a competing unmarked medial vowel-only parse. Explicit hyphens remain boundaries, not decorative punctuation. See the [PCGN 1966 agreement, note 4](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/693731/ROMANIZATION_OF_LAO.pdf) and the [2023 Laos Toponymic Factfile example](https://assets.publishing.service.gov.uk/media/654cff895d6095000dbec8b1/Laos_Toponymic_Factfile.pdf).

The engine preserves punctuation and whitespace, reports the detected/selected profile, and leaves ambiguous or unsupported spans in visible `⟦…⟧` brackets. The ALA-LC parser rejects BGN-only aliases such as `x` and `gn`, and does not accept `s`, `v`, `r` or `l` as final spellings. Without the original Lao syllable structure, a Latin string such as `kam` may have more than one valid analysis; it is withheld rather than guessed. Romanization-only input does not produce IPA, and it cannot recover tone, vowel length or consonant-class distinctions that the chosen romanization omits.

**RTGS note:** the LDC Lao language-specific document lists RTGS among schemes that have been used for Lao, but it does not provide a normative, complete RTGS-for-Lao mapping table in the cited section. RTGS is primarily the Royal Thai General System of Transcription. The project therefore does not label the current parser as RTGS and does not silently interpret every RTGS-like spelling as Lao. A dedicated profile requires a specific Lao adaptation table and reviewed examples. Informal French-style, karaoke and mixed spellings likewise remain evidence-limited.

Sources: [ALA-LC Lao Romanization Table (2012)](https://www.loc.gov/catdir/cpso/romanization/lao.pdf); [LDC Language Specific Peculiarities Document for Lao](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf); [PCGN Laos Toponymic Factfile (2023)](https://assets.publishing.service.gov.uk/media/64f9c99f7a4b4f0012f6d8a5/Laos_Toponymic_Factfile.pdf).



## Additional documented romanization profile: DLLM collection convention (research only)

A source review found a distinct, documented Lao romanisation convention used by the Digital Library of Lao Manuscripts (DLLM), hosted by CrossAsia. CrossAsia describes it as closely following the revised Royal Thai General System of Transcription for Central Thai, with three explicit Lao-specific changes: syllable-initial Lao ວ is written `v` rather than Thai-style `w`; initial ຍ is written `ny` for Lao [ɲ]; and initial ຈ is written `c` rather than `ch`. The convention is broad and phonetic in orientation and does not distinguish vowel length or tone. CrossAsia also publishes a one-page consonant/vowel table, including position-sensitive finals and additional vowel sequences.

**Scope warning:** this is the DLLM catalogue's practical romanisation for Lao-language manuscript titles, designed to make catalogue records easy to find. CrossAsia explicitly says Lao has no official romanisation system and notes that spellings of common names vary. Its inventory also preserves historical Indic loanword forms in some contexts. Therefore DLLM is not a national Lao standard, not the Royal Thai RTGS applied unchanged, and not interchangeable with BGN/PCGN or ALA-LC. The source table must be reviewed as its own profile before implementation.

**Implementation status: RESEARCH CANDIDATE / NOT SUPPORTED.** Do not auto-detect this profile, merge its spellings into BGN/PCGN or ALA-LC, or infer Ukrainian forms from the three headline substitutions. Before adding a distinct `dllm` profile, acceptance requires: (1) a full, independently transcribed and checked table with all vowel/final contexts and source examples; (2) a reuse/licensing determination for the published CrossAsia table (the cited page states CrossAsia copyright but exposes no explicit open-data licence); (3) explicit Ukrainian target decisions for every supported unit; (4) source-backed regression fixtures and a Lao-specialist review. Until then the current parser remains limited to its two declared profiles.

Sources: [CrossAsia DLLM romanisation description](https://digital.crossasia.org/digital-library-of-lao-manuscripts-about-dllm-collection/?lang=en) (especially its “Lao Orthography and Romanisation” section); [CrossAsia DLLM consonant/vowel table (PDF)](https://digital.crossasia.org/wp-content/uploads/2021/10/DLLM_laoromanisation.pdf). The [LDC Lao Language Specific Peculiarities Document](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf) independently lists RTGS among schemes used for Lao, but does not make the DLLM adaptation a national standard.

## ALA-LC 2012 Note 8 — Lao-source numeral conversion

**Implementation on PR #241 branch:** a separate typed helper, `romanizeAlaLcNumerals(input)`, maps only the ten Lao digits `໐–໙` (U+0ED0–U+0ED9) to ASCII/Arabic numerals `0–9`. It preserves all other code points, punctuation, whitespace, line endings and mixed-script content verbatim. The result identifies its direction (`Lao-script→Arabic numerals`), profile, Note 8 rule and mapped-digit count.

The service exposes this as a distinct output panel labelled **Цифри · ALA-LC 2012, Note 8**. It is not the phonetic route, not the CLDR BGN/PCGN romanizer, and not a claim that the surrounding Lao text has been fully romanized under ALA-LC. The existing phonetic parser continues to preserve Lao numerals as passthrough; direct Latin ALA-LC input remains a separate route.

**Status:** DONE_VERIFIED on PR #241 exact head; Verify #4383 / [run 43918104933 — SUCCESS](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43918104933) passed 350 Python, 204 Node and 30 Chromium tests and all configured audits/build checks. PR #241 merged as `841826ce9981b1c09aa98179c790c63db1b2c982`; post-merge main verification remains.

Primary source: [Library of Congress, ALA-LC Lao Romanization Table (2012), Note 8](https://www.loc.gov/catdir/cpso/romanization/lao.pdf), which explicitly maps `໐–໙` to `0–9`.

## ALA-LC 2012 inventory boundary

The LOC table is broader than the currently implemented normalizer. The implemented subset is limited to `u/ū`, `uʼ/ūʼ`, `e/ē`, `æ/ǣ`, `oe/ōe`, `ia/īa`, `ua/ūa`, `ai/āi`, `ao` and `am`, plus the onset/final subset documented above. This list must not be read as full ALA-LC vowel coverage.

The LOC table also specifies the following forms, which remain unsupported by the Ukrainian adapter: `ư`, `ư̄`, `œ`, `œ̄`, `ǫ`, `ǭ`, `ưa`, `ư̄a`, `iu`, `īu` and `īeo`. Note 2 treats final `ຍ` as the closing `i` of the `ai`/`āi` diphthong, not as a consonant coda; the source-aware crosswalk now preserves that distinction. Note 4 additionally defines medial-`ວ` behavior: `w` in clusters before a vowel (e.g. `khwā`, `khwǣng`), `ūa` before a final consonant (e.g. `būak`, `dūai`), and `o` after a vowel in final position (e.g. `nāo`, `kǣo`); the final-`o` pattern can now be crosswalked when source syllable structure is supplied; standalone strings that admit competing vowel/coda parses remain PARTIAL. Medial `w` clusters and the `ūa` alternation remain unsupported. Note 5 suppresses `ຫ` before specified sonorants and permits ligature forms; Note 6 uses initial `ʻ` for vowel-initial syllables but treats medial `ອ` as a vowel. Notes 2, 3 and 7–10 cover final `ຍ`, subscript `ລ`, vowel placement, numerals, word segmentation/loanword boundaries, tone marks and double-function consonants. These rules are not all recoverable from a bare Latin string, and are not claimed as implemented.

A concrete false-positive risk exists when an unsupported ALA-LC sequence such as `iu` could be split by the generic parser into two ordinary vowel nuclei. The direct-input adapter now detects the unsupported LOC sequences and withholds the entire whitespace-/hyphen-delimited fragment as PARTIAL rather than returning a fabricated syllable sequence. This is a conservative guard, not support for those vowels. The original text remains visible in `⟦…⟧` brackets.

Source: [Library of Congress, ALA-LC Lao Romanization Table (2012), pp. 1–3, especially Notes 2–10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).

## Canonical correspondence table

The existing implementation's detailed, position-sensitive crosswalk is maintained in methodology.md under “Optional romanization-to-Ukrainian mode” and in:
- web/romanization-syllable-engine.js
- web/romanization-ukrainian.js
- data/lao/ukrainian_correspondences.csv
- tests/romanization-syllable-engine.test.mjs

Representative rows:

| Lao source grapheme / structure | CLDR romanization unit | Ukrainian unit | Status / condition |
|---|---|---|---|
| ກ onset | k | к | supported onset |
| ຂ / ຄ onset | kh | к' | aspiration digraph; not standalone h |
| ງ onset | ng | нг | supported onset |
| ຈ onset | ch | ч | supported onset |
| ຖ / ທ onset | th | т' | aspiration digraph; not standalone h |
| ຜ / ພ onset | ph | п' | aspiration digraph; not standalone h |
| ຫ / ຮ onset | h | г | standalone /h/ only |
| ໜ / ໝ | n / m | н / м | silent-hoa ligature; source-aware |
| A nucleus + final ມ | am-shaped sequence | ам | validated against source vowel ID; not interchangeable with AM nucleus |
| AM nucleus | am | ам | source vowel ID required |
| ນ / ມ coda | n / m | н / м | supported coda |
| unsupported or mismatched source/Latin unit | — | withheld | PARTIAL; no guessed syllable |

## Coverage and acceptance

The Romanization method's contract is **complete coverage of the supported orthographic input inventory**, not guaranteed full Unicode reversibility and not phonetic completeness. Every recognized source unit must either map through a source-attested romanization row and an explicit Ukrainian project row, or be retained as a visible PARTIAL / UNSUPPORTED diagnostic without fabricating a Ukrainian syllable.

A future table expansion must add source grapheme/structure, CLDR output, Ukrainian syllable, context, source locator, evidence status, test fixture and reviewer decision. No row may be promoted from a generated CLDR string alone.

## Existing implementation preserved

The syllable-level parser and source-aware checks are retained. It checks onset, source vowel ID and supported coda, distinguishes kam ambiguities when Lao source structure is available, handles supported silent-hoa forms, and refuses ambiguous/mismatched syllables. A separate direct-input path now reuses the parser without inventing source-side Lao evidence. Do not replace either route with character-by-character Latin-to-Cyrillic replacement.

## Remaining tasks

| ID | Status | Acceptance |
|---|---|---|
| LAO-ROM-STD-001 | DONE_VERIFIED (documented selection) | PCGN 1966 / CLDR profile accurately labelled provisional; no claim of official national standard |
| LAO-ROM-MATRIX-001 | PARTIAL | Every supported Lao orthographic syllable has source → Latin → Ukrainian rows and fixtures |
| LAO-ROM-DIRECT-001 | PARTIAL | Direct BGN/PCGN input and bounded ALA-LC 2012 normalization are implemented; PR #182 verifies LOC-specific source-aware onsets/finals and Notes 2/4 (exact-head Verify #4128, post-merge Verify #4131 and Pages #98 passed); full contextual ALA-LC rules and broader corpus coverage remain required |
| LAO-ROM-RTGS-001 | BLOCKED | No generic/national Lao RTGS standard established. CrossAsia DLLM is a separate documented collection convention based on revised Thai RTGS with three Lao-specific changes; keep it as a research-only candidate until full table review, reuse rights, Ukrainian decisions and specialist fixtures are complete |
| LAO-ROM-COVERAGE-001 | PARTIAL | Inventory audit proves no supported grapheme class is silently dropped |
| LAO-ROM-REVIEW-001 | BLOCKED | Independent Lao specialist review of ambiguous nuclei, conventional names and loanword namespaces |
| LAO-ROM-API-001 | DONE_VERIFIED | Explicit unknown profile values return PARTIAL / UNSUPPORTED_PROFILE and preserve input; null/omitted selection retains auto detection; PR #192 merged as `6bca3d2`; exact-head Verify #4163, post-merge Verify #4164 and Pages #99 passed |


## Sentence and mixed-text regression checkpoint — 2026-10-31

The current `main` head `2ae2971c2526cba57504e294f37caf64c964c3f6` passed exact-main workflow [41243897060](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41243897060). Regression coverage includes the full greeting sentence through the syllable-level CLDR → Ukrainian adapter, preservation of explicit spaces and punctuation, Latin mixed text, ASCII digits and native Lao numerals. Numerals without an evidenced Ukrainian mapping remain visible and explicitly partial; they are not silently deleted or assigned guessed output. These fixtures establish integration/input integrity, not independent linguistic gold. Exhaustive matrix coverage and specialist review remain PARTIAL/BLOCKED as recorded above.


## Post-merge engineering verification — 2026-10-31

PR #90 is merged as `69fa43e7d66e2c4c6468945497ff5a1b1ab7b717`; exact-main workflow [41246317109](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/41246317109) passed. This confirms the documented whole-sentence and mixed-text regression set remains green on main. It does not promote the PARTIAL source-to-CLDR-to-Ukrainian inventory to complete or establish independently adjudicated phonetic accuracy.


## Source-aware hyphen alignment regression — 2026-11-15

The Lao → CLDR Lao-Latin → Ukrainian path can emit a hyphen inside a whitespace-delimited Lao token to mark a medial onsetless syllable (BGN/PCGN note 4). The source-side crosswalk groups syllables by the original Lao token. Splitting that generated Latin token again at the hyphen incorrectly advanced the source-group cursor, so subsequent fragments were compared with the next Lao word and valid syllables were withheld as `⟦…⟧`.

PR #214 changes source-aware parsing to keep the hyphen inside the current token, consume no source syllable for the boundary, and preserve the hyphen in Ukrainian output. The hyphen remains an ordinary token boundary in direct Latin-only input, where no Lao source group is available. A regression test covers a single source word containing three romanized syllables with a medial onsetless syllable. This is a parser-alignment correction; it adds no new Lao phonological or Ukrainian correspondence rule.

### Source-backed recovery when CLDR elides a medial vowel — 2026-11-15

The official Lao PDR motto contains the word `ວັດທະນາຖາວອນ`. In its final syllable, the source analyzer identifies onset `ວ`, vowel ID `AWW_MEDIAL` and coda `ນ`, while the implemented CLDR transform emits `v-n`: the vowel is absent from the Latin output. This is distinct from an ordinary hyphen boundary such as `é-kalad`.

The source-aware adapter now permits a narrowly bounded repair: when (1) the original Lao syllable is present, (2) its onset and coda map exactly to the Latin material on either side of the hyphen, and (3) its vowel ID has exactly one supported target nucleus, that nucleus is restored from the Lao source. For `AWW_MEDIAL`, the existing target mapping is `о`. The repaired unit is marked `sourceRestoredVowel` in the analysis trace. No such restoration is available in direct Latin-only mode: `vadthanathav-n` remains PARTIAL because the missing vowel cannot be inferred from the Latin string alone.

An end-to-end regression uses the official Lao PDR motto, whose text is printed in [the National Assembly's 2017 Statistics Law PDF](https://na.gov.la/wp-content/uploads/2021/11/40.-%E0%BA%81%E0%BA%BB%E0%BA%94%E0%BB%9D%E0%BA%B2%E0%BA%8D%E0%BA%A7%E0%BB%88%E0%BA%B2%E0%BA%94%E0%BB%89%E0%BA%A7%E0%BA%8D%E0%BA%AA%E0%BA%B0%E0%BA%96%E0%BA%B4%E0%BA%95%E0%BA%B4-2017.pdf) and a [2025 government-hosted statistical-office document](https://www.lsb.gov.la/wp-content/uploads/2025/04/01_%E0%BA%82%E0%BB%8D%E0%BB%89%E0%BA%95%E0%BA%BB%E0%BA%81%E0%BA%A5%E0%BA%BB%E0%BA%87%E0%BA%A7%E0%BB%88%E0%BA%B2%E0%BA%94%E0%BB%89%E0%BA%A7%E0%BA%8D%E0%BA%81%E0%BA%B2%E0%BA%99%E0%BA%88%E0%BA%B1%E0%BA%94%E0%BA%95%E0%BA%B1%E0%BB%89%E0%BA%87-%E0%BB%81%E0%BA%A5%E0%BA%B0-%E0%BB%80%E0%BA%84%E0%BB%87%E0%BB%88%E0%BA%AD%E0%BA%99%E0%BB%84%E0%BA%AB%E0%BA%A7-%E0%BA%AB%E0%BB%89%E0%BA%AD%E0%BA%87%E0%BA%81%E0%BA%B2%E0%BA%99-%E0%BA%AA%E0%BA%96%E0%BA%95-0761.08%E0%BA%95%E0%BA%B5%E0%BA%A5%E0%BA%B2-2022.pdf). PR [#218](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/218) was squash-merged as `fe435317dcb69cd43f0409ca85e9b617b334a584`; exact-head Verify [#4265](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753154383) passed all configured gates. This is source-backed orthographic recovery in the romanization route, not IPA validation or a claim that CLDR is reversible. The runtime commit was deployed to GitHub Pages by run [#101](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43753235467); both deploy and post-deploy smoke-test jobs succeeded.


### Source vowel inventory boundary — 2026-11-15

The canonical source vowel registry (`data/lao/vowels.csv`) contains seven core IDs that do not yet have a confirmed one-to-one crosswalk in the current CLDR Lao-Latin adapter: `UO_LONG_ALT`, `UO_LONG_OPEN`, `OEY`, `OOY`, `AEW`, `AOY` and `AAJ`. The adapter now reports the exact source vowel ID and withholds the Ukrainian result when one of these structures is encountered in source-aware mode. It does not guess a Latin nucleus or a Ukrainian output.

This is intentionally a coverage boundary, not a declaration that CLDR has no possible spelling for these structures. The upstream CLDR [Lao-Latin transform](https://github.com/unicode-org/cldr/blob/main/common/transforms/Lao-Latin.xml) is marked provisional, identifies its variant as UNGEGN with a BGN alias, and retains a TODO concerning special handling of consonants at word ends. Its context rules must be checked against the exact Lao source spelling before a new row is promoted. The source registry's presence of a vowel ID alone is not evidence of a reversible CLDR mapping.

Regression coverage asserts that all seven source IDs remain visible as PARTIAL with a specific warning, while direct Latin-only `kha` remains unchanged. Acceptance for each future mapping: exact CLDR transform output for a source-attested spelling, source syllable boundary/coda interpretation, Ukrainian target decision, positive and negative tests, and Lao-specialist review.


## CLDR upstream rule check for uncovered source vowels — 2026-11-15

The current upstream [CLDR Lao-Latin transform](https://github.com/unicode-org/cldr/blob/abbf1914a169f334dd43b3f00fce186360950b1e/common/transforms/Lao-Latin.xml) is provisional and retains a final-consonant TODO. It actively maps `ວ` as `v`; the alternative vowel mapping `#ວ → oua` is commented out. Its separate character rules do not provide an explicit, validated compound-vowel crosswalk for `UO_LONG_ALT`, `UO_LONG_OPEN`, `OEY`, `OOY`, `AEW`, `AOY` or `AAJ`. These seven IDs therefore remain PARTIAL in source-aware mode. Do not infer compound output by concatenating CLDR character rules; each promoted row needs an exact source-attested transform result, source-structure check, Ukrainian decision, regression fixtures and Lao-specialist review.


## ALA-LC 2012 Note 4 regression boundary — 2026-11-16

The LOC Note 4 has distinct contextual spellings for ວ. The bounded adapter now has explicit regression fixtures for the already implemented `ūa`-before-final pattern (`būak`, source-aware) and final-`o` pattern (`nāo`, source-aware). The medial-`w` cluster examples `khwā` and `khwāng` are asserted to remain PARTIAL; this is intentional until a reviewed Ukrainian cluster adaptation is specified. Note 4's `iú`, `īu` and `īeo` forms also remain unsupported under the existing fail-closed guard. This is regression coverage of a bounded subset, not full ALA-LC conformance.

Source: [Library of Congress, ALA-LC Lao Romanization Table (2012), Note 4, page 3](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).


## PR #223 engineering verification — 2026-11-16

PR [#223](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/223) merged as `05644cbece3395122c18fb390aceba80013104cb`. Exact-head Verify #4291 and post-merge Verify #4292 passed 350 Python, 195 Node and 28 Chromium tests, plus data/evidence audit, build and generated-data reproducibility. The Note 4 fixtures establish source-aware behavior for `būak` and `nāo`; Latin-only inputs remain PARTIAL when ambiguous. The medial-`w` cluster examples remain PARTIAL. This is bounded engineering verification, not full ALA-LC conformance or linguistic gold validation.

## ALA-LC 2012 contextual notes 5–10 — conformance boundary (2026-11-16)

The complete Library of Congress table notes are not equivalent to a complete direct-input implementation. The current implementation is still a bounded subset; the following dispositions keep each note's actual contract visible.

| LOC note | Rule | Current disposition |
|---|---|---|
| 5 | Silent initial ຫ before ຍ/ny, ນ, ມ, ຣ, ລ and ວ; ໜ/ໝ are common ligatures | Source-aware crosswalk covers the underlying onset values and retains expanded `onsetForm` provenance in regression fixtures. Standalone romanization cannot recover the silent source letter. |
| 6 | Initial ອ marks a vowel-initial syllable (`ʻ`); medial ອ functions as a vowel component | Source-aware parsing now recognizes initial `ʻ` against Lao onset ອ and retains the source/vowel trace, but returns `UNSUPPORTED_ALA_LC_INITIAL_AYN` / PARTIAL because no Ukrainian target value is approved. Latin-only `ʻ` remains withheld. The LOC `ǫ`, `ǭ`, `ưa`, `ư̄a` forms remain fail-closed. |
| 7 | Romanized vowel spelling follows the romanized consonant even where Lao vowel signs are preposed in Unicode | The syllable parser consumes onset-first ALA-LC spellings and source-aware vowel IDs; regression coverage confirms `kē` with source vowel ID `EE`. This does not imply all LOC vowel classes are implemented. |
| 8 | Lao numerals ໐–໙ correspond to 0–9 | PARTIAL / route distinction: the browser's Lao-to-Ukrainian phonetic path preserves Lao digits as non-phonetic passthrough. It does not implement the LOC ALA-LC Lao-source-to-Arabic-numeral romanization rule. The direct ALA-LC input mode accepts already-romanized Latin text, so its ASCII-digit passthrough is not evidence of Note 8 conformance. |
| 9 | Lao word boundaries are not explicit; romanization uses shortest standalone written forms and separate rules for Pali/Sanskrit and other loanwords; tone marks are omitted | PARTIAL / BLOCKED. The parser preserves supplied whitespace and punctuation but has no LOC-conformant lexical segmenter. LaoNLP maximum matching is not equivalent. HVULao_NLP v2 is a stronger general segmentation candidate but does not specify LOC's Indic/other-loan clauses, and source-item rights need reconciliation. An offline ICU word-break-list experiment on 839/1,000 exactly aligned sentence pairs (49,608 within-Lao candidate boundaries) produced longest-prefix F1 0.8636 and naive shortest-prefix F1 0.5129; neither is comparable to the paper's 0.75 model score or implements LOC Note 9. No corpus/dictionary data or model is imported. A reviewed LOC-specific policy, rights-cleared examples and Lao-specialist adjudication remain required. Tone marks are omitted by the romanization convention; tone and quantity absent from romanization are not reconstructed. |
| 10 | A consonant serving as the coda of one syllable and onset of the next is romanized twice | The source-aware syllable crosswalk has a positive/negative synthetic fixture for the LOC romanized example `khitsatān`, with source roles manually supplied. The browser regression using `ຄິຼສຕຽນ` is only a mode-separation check: Lao script entered in Latin romanization mode remains PARTIAL; it is not the LOC Note 10 example and does not test automatic Lao source segmentation. LOC 2012 Notes 3 and 10 give the romanized example `khitsatān`; the exact Lao glyph sequence is unresolved because the available PDF text extraction returns `ຂິດສະຕານ` but the rendered glyphs have not been confidently read, and the preferred Word source remains unavailable. The earlier exact-form assertion `ຫຼັກສາດ` and the 1997 glyph attribution are both withdrawn pending direct Word-source or Lao-specialist verification. Automatic LOC source-role derivation remains PARTIAL, and full Note 10 conformance is not claimed. |

The Note 5 source-aware fixtures exercise all six listed underlying sonorant onset values (`ຍ`, `ນ`, `ມ`, `ຣ`, `ລ`, `ວ`) with expanded `onsetForm` provenance. They do not claim that the Latin string can reveal the silent `ຫ`. Note 7 receives a separate source-vowel identity regression. Note 6 now has a fail-closed source-aware initial-ayn trace, not a Ukrainian target mapping. Note 10 has an engineering regression for the manually supplied double role using `khitsatān`; this does not prove that the browser's upstream Lao parser derives the exact LOC source-script syllabification or that every lexical boundary case is handled. The `ຄິຼສຕຽນ` browser test is a mode-separation guard only.

Primary source: [Library of Congress, ALA-LC Lao Romanization Table (2012), Notes 5–10](https://www.loc.gov/catdir/cpso/romanization/lao.pdf). The table is an orthographic romanization source; it does not prescribe this project's Ukrainian target output.

**Engineering evidence for Notes 5 and 7:** PR [#225](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/225), exact-head Verify [#4295](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43840762990) and post-merge main Verify [#4296](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43840888440) passed 350 Python, 198 Node and 28 Chromium tests in each run. This closes the engineering-fixture task only; it does not close the linguistic review or full-conformance rows above.

**Engineering evidence for Notes 6 and 10:** PR [#228](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/pull/228) merged as `44b5fa2ebc4380bd9fa4b201e8c8eb52a7ccd900`. Exact-head Verify #4313 / [run 43849117284](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849117284) and post-merge main Verify #4314 / [run 43849485259](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849485259) each passed 350 Python, 201 Node and 28 Chromium tests, plus schema, repository/evidence, external-G2P, build, reproducibility and built-page checks. Pages Deploy #103 / [run 43849485210](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/43849485210) published the runtime commit and passed the built-site Chromium suite and post-deployment smoke test. The Note 10 regression validates supplied source roles; automatic Lao segmentation of the LOC example remains unverified.

## ALA-LC Note 9 — HVULao_NLP as comparative candidate (2026-11-16)

HVULao_NLP v2 publishes a human-reviewed general Lao word-segmentation guideline: minimal orthographic units carrying lexical/grammatical meaning, smallest consistent segmentation, context-sensitive disambiguation, separation of function words/particles, and a test for whether compound components can be independently modified or replaced. This is relevant evidence for candidate boundary analysis, but it is not an LOC-specific standard. The guideline does not specify the LOC treatment of Pali/Sanskrit loans or original-language boundaries for other loanwords. A subsequent offline ICU dictionary baseline experiment is recorded in the direct-input audit; its greedy longest/shortest prefix scores are exploratory and neither implements the LOC rule. Keep Note 9 PARTIAL; do not treat the corpus, dictionary or trained model as a resolver or as pronunciation evidence.

The Mendeley v2 record lists CC BY 4.0, while the article's ethical statement says the source websites permitted research/non-commercial reuse. Resolve rights at the source-item level before copying corpus sentences or using them commercially. No HVULao data/model is included in this repository.

Sources: [Informatica 2025 paper, Appendix B](https://www.informatica.si/index.php/informatica/article/download/11195/5975); [Mendeley Data v2](https://data.mendeley.com/datasets/5zwym7kwn8/2); [LOC ALA-LC Lao table, Note 9](https://www.loc.gov/catdir/cpso/romanization/lao.pdf).

**Loanword evidence refinement:** the LDC Lao language-specific document distinguishes Pali/Sanskrit borrowings from recent foreign loans in orthographic use of ລ/ຣ, while CrossAsia DLLM records historically conservative Indic forms and modernized spellings for common lexicalized loans. These are context-specific orthographic observations, not a deterministic origin classifier. A future resolver must carry lexeme-level origin and lexicalization provenance and keep LOC Note 9's source-language division as a separately reviewed rule. Sources: [LDC Lao LSP](https://catalog.ldc.upenn.edu/docs/LDC2017S08/LSP_203_final.pdf); [CrossAsia DLLM](https://digital.crossasia.org/digital-library-of-lao-manuscripts-about-dllm-collection/?lang=en).


## Vientiane Lao written sequences vs spoken phonological clusters — 2026-11-16

Ueda (1994, §2.3, printed pp. 100–101) explicitly reports no phonological consonant clusters in the described Vientiane spoken dialect despite consonant-letter sequences in the orthography. The paper's examples show written `w` corresponding to spoken /ua/ or to no independent segment. Its onset/coda inventories are positional and overlap for some consonants. This is a direct warning that adjacent written consonant letters cannot simply be concatenated into an IPA onset cluster.

**Implementation boundary:** retain orthographic parsing as a distinct stage; derive spoken onset/rhyme/coda only through documented correspondences and preserve null/multisegment realizations and provenance. Ueda does not supply a complete orthographic syllabifier, so this evidence does not close Note 10 automatic source-role derivation. Scope is the described central Vientiane variety, not all Lao dialects.

Source: Ueda (1994), DOI [10.11435/GENGO1939.1994.106_95](https://doi.org/10.11435/GENGO1939.1994.106_95); claim `CLM-LAO-ORTHOGRAPHIC-SEQUENCES-NOT-PHONOLOGICAL-CLUSTERS` / source `SRC-UEDA`.


## Historical Lao orthographic syllable grammar and ambiguity — 2026-11-17

Berment (2004, Part III §§III.2.3–III.2.6; Annexes A.11/A.14) documents a historical explicit Lao orthographic syllable grammar: initial consonant/consonant groups, positional vowel patterns assembled from signs around the onset, optional accent, and restricted coda. It reports 56,670 generated candidate strings and a 33-state/480-transition automaton, but also warns that the grammar accepts theoretical unattested forms (e.g. `ມວອ`) and simplifies accent placement. Exact terminals in the OCR-extracted production listing are incomplete; do not reconstruct missing Lao glyphs by guesswork. No code is copied and no license for Sylla/Prolog code is assumed.

Berment models all candidate syllables as edges in a position graph, complete segmentations as paths, and prunes dead branches that cannot belong to a complete path. Ambiguous regions remain explicit. The historical longest-candidate rule was a local UI selection heuristic with user cycling, not a global linguistic resolution rule. Del Vigna & Berment (2003) separately formalize irreducible ambiguity for a historical Lao syllable dictionary; its counts are not interchangeable with the thesis's generated-grammar counts.

**Project disposition:** historical grammar found = `DONE_VERIFIED` as source evidence; current Lao orthographic grammar = `PARTIAL/TODO`; ambiguity lattice/dead-branch pruning = `PARTIAL/TODO`; lexical/semantic resolution = `BLOCKED/evidence-limited`. Next acceptance requires exact production transcription from page images/Annex A.14, modern Unicode and dialect reconciliation, candidate-lattice tests including ambiguous `ແຂກະ`, unattested `ມວອ`, invalid mark sequences and dead branches, plus independent Lao-specialist adjudication. Keep orthographic candidates separate from downstream spoken IPA analysis (Ueda 1994); keep LOC Note 10 exact glyph and repeated-role derivation unresolved.

Sources: [Berment (2004) full thesis](https://www.tagmatica.fr/doc/these-vincent-berment.pdf); [Del Vigna & Berment (2003), DOI 10.36045/bbms/1074791326](https://doi.org/10.36045/bbms/1074791326); registry IDs `SRC-BERMENT-THESIS-2004`, `SRC-DEL-VIGNA-BERMENT-2003`.

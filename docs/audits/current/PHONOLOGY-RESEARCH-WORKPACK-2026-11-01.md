# Lao phonology research workpack

**Scope:** central/Vientiane-oriented Standard Lao only unless a separate profile is created. No rule is promoted from a comparator dialect without explicit evidence.

## Evidence already located

1. Reiko Ueda (1994), “The Phonology of the Vientiane Dialect of Lao,” *Gengo Kenkyu* 106, 95–115, DOI [10.11435/gengo1939.1994.106_95](https://doi.org/10.11435/gengo1939.1994.106_95). The paper analyzes syllables as consonant + rhyme + tone; reports short/long vowel contrasts, nine finals and five tone categories for central Vientiane, while noting variation inside the low-rising category. Primary access: [J-STAGE article and PDF](https://www.jstage.jst.go.jp/article/gengo1939/1994/106/1994_106_95/_article).
2. N. J. Enfield (2007), *A Grammar of Lao*, Mouton Grammar Library 38, especially Chapter 3 “Phonology.” Treat this as the principal Vientiane-oriented descriptive reference; exact page-level claims still need checking against the full book.
3. Gedney & Hudak (1997) and Enfield (2007) are reported with different treatment of initial /kw, kʰw/ in the [EURPhon Lao (Vientiane) summary](https://eurphon.info/languages/html?lang_id=214). This is a conflict lead, not a final ruling: inspect both primary descriptions before choosing phonemic /kw/, /kʷ/, /kʰw/ or a sequence analysis.
4. The [SEASite live/dead syllable and tone chart](https://seasite.niu.edu/lao/LaoLanguage/LaoTones/tone_chart.htm) is a useful teaching comparator, not the sole phonetic authority. Ueda's dialect-specific account takes precedence where they differ.

## Required research matrix

| Workstream | Required matrix | Acceptance evidence |
|---|---|---|
| Tone × rhyme | Initial consonant class × tone mark × live/dead × vowel length × coda × diphthong × lexical profile | Primary-source locator for each rule; attested lexical examples; explicit unattested/contradictory cells |
| Tone contours | Five-category reference plus within-category phonetic variation | Audio or instrumental evidence, speaker/profile metadata, contour annotation convention |
| Rhyme | Monophthong/diphthong × short/long × nine coda classes × exceptional unstressed non-final syllable | Every supported cell traced to source or recorded elicitation; no extrapolation from orthographic form |
| Labialized velars | /kw, kʰw/ vs /kʷ, kʷʰ/ vs /k+w/; place/manner and aspiration timing | Direct comparison of Enfield and Gedney/Hudak, speaker evidence, narrow IPA and phonemic analysis kept separate |
| Ukrainian adaptation | IPA /w/, /ʋ/, /kʷ/, /kʰw/ and sequences | Separate candidate rows for each IPA input; expert Ukrainian review; no orthographic romanization shortcut |

## Highest-risk questions

1. Do the project’s five tone labels align one-to-one with Ueda’s categories, and how is the reported non-phonemic variation inside low-rising represented?
2. Which tone restrictions depend on rhyme weight/coda and which are merely orthographic tone-mark rules?
3. Are /kw/ and /kʰw/ productive onset clusters in the chosen Vientiane profile, or are some apparent cases /kʷ/ or /kʷʰ/? The sources conflict; do not hard-code a single answer.
4. How should minor/unstressed syllables be represented without assigning them a lexical tone that the evidence does not support?
5. Which features of aspiration and labialization can Ukrainian orthography preserve without implying a false consonant sequence?

## Execution order

- [ ] Extract Ueda's full segmental and tone tables with exact page/section locators.
- [ ] Read Enfield Chapter 3 and Gedney/Hudak directly; create a claim-by-claim conflict table.
- [ ] Audit the existing Lao tone and rhyme CSV registries against that table; mark every unsupported rule `EVIDENCE_LIMITED`.
- [ ] Build a minimal-pair/lexical probe list stratified by rhyme and tone; source-attested entries are probes, not gold.
- [ ] Obtain recordings/elicitation with dialect, speaker and recording rights; two annotators independently label phonemic and phonetic IPA.
- [ ] Review Ukrainian candidates only after the source IPA decision is adjudicated.

**Current status:** PARTIAL. Existing tone/rhyme logic and tests are retained. Independent lexical gold is still 0. No new Lao IPA labels are added in this workpack.


## Verified source audit — 2026-11-01

### Central Vientiane tone/rhyme baseline

Ueda (1994), J-STAGE article abstract and bibliographic record (pp. 95–115; [DOI](https://doi.org/10.11435/gengo1939.1994.106_95)), explicitly models syllables as consonant + rhyme + tone. For the central Vientiane variety it reports nine finals, short/long vowel contrast, three diphthongs, and five lexical tone categories: low-rising, high-rising, high-mid level, low-falling and high-falling. It also flags non-phonemic variation within the low-rising category and an exceptional unstressed, tone-neutral non-final /a/ syllable. This is sufficient to preserve a five-category Vientiane profile baseline; it is not a word-level pronunciation corpus or a complete tone-mark × coda rule table.

### Labialized consonants

Blaine Erickson (1996), “On the Origins of Labialized Consonants in Lao,” [full paper](https://sealang.net/sala/archives/pdf8/erickson2001origins.pdf), argues that Lao labialized consonants should be treated as unit phonemes rather than consonant–glide sequences. The paper describes restricted distribution, absence before rounded vowels, and a skewed inventory (all velars, some alveolars, one palatal). It also cites a six-tone description from Hoshino & Marcus / Morev, which must not be silently merged with Ueda's five-category central Vientiane model. The two sources differ in analytical scope and underlying reference materials; create separate profile/source claims rather than averaging the tone inventories.

### Ukrainian adaptation consequence

Keep a labialized input such as /kʷ/ typed as a unit IPA segment through the adapter boundary. Writing it as an unqualified Ukrainian sequence «кв» may falsely imply two independently timed consonants; writing a diacritic or another practical convention requires an explicit target-language decision and Ukrainian phonetic review. No Ukrainian spelling has been promoted from this source alone.

**Status update:** tone/rhyme baseline is better sourced but the full lexical matrix and acoustic coverage remain PARTIAL. Labialized onset representation is now source-supported as a unit analysis in Erickson's account, while its compatibility with the selected Vientiane profile and Ukrainian output remains evidence-limited. No IPA gold labels were added.


See the source-grounded [Lao tone–rhyme evidence matrix](LAO-TONE-RHYME-EVIDENCE-MATRIX-2026-11-01.md) for the Vientiane inventory baseline, unfilled tone × coda cells, labialized-onset analysis and Ukrainian-adapter blockers.


### Erickson source correction and tone/rhyme cross-check

The SEA-language archive PDF filename contains “2001”, but its bibliographic publication is Erickson (1996), *Papers from the Sixth Annual Meeting of the Southeast Asian Linguistics Society*, pp. 135–148. The source's own §2.4 adopts a six-tone description from Hoshino & Marcus (1981) / Morev et al. (1979): all six tones may occur in open syllables; glottal-stop codas occur only with short vowels and two tones; other stop codas occur with four tones. This is a distinct source framework from Ueda's five-tone central Vientiane description and must remain a separate profile/analysis column.

Erickson's synchronic argument that labialized consonants are unit phonemes is explicit (§3, pp. 138–139). The proposed historical derivation from earlier CuV sequences is explicitly tentative in §5.1 and the conclusion (pp. 142–143); do not treat that diachronic hypothesis as established fact.

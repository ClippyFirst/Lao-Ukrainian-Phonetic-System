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

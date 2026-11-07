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


### Full-text Ueda (1994) extraction — tone/rhyme audit

The full J-STAGE PDF confirms more than the abstract. Ueda's sample is one 46-year-old woman born and raised in Haysok, central Vientiane (p. 96), so the description is a high-value speaker-specific baseline, not a multi-speaker population consensus.

Ueda separates plain rhymes (open or sonorant/glide-final: no coda, /m,n,ŋ,j,w/) from checked rhymes (/p,t,k,ʔ/). Short vowels normally require a coda; only long vowels/diphthongs form open syllables. Front vowels do not occur with /j/ coda and back vowels do not occur with /w/ coda (pp. 96, 104–105).

The basic five-tone system is fully conditioned by rhyme type:
- Plain rhymes: all five tones.
- Long checked rhymes: only low-falling [21] and high-falling [52].
- Short checked rhymes: only high-rising [34] and mid-level [33].

The five basic contours are full-rising [24], high-rising [34], mid-level [33], low-falling [21] and full-falling [52] (pp. 106–108). Ueda also documents restricted five-/six-tone variability: a low-level [22] realization is limited to a subset of onsets and overlaps substantially with full-rising; connected/non-final contexts may show [24], [23] or [22] (pp. 106–110). This is not evidence for a robust six-way lexical contrast.

Ueda §2.3 (pp. 100–101) explicitly rejects phonological consonant clusters in spoken Vientiane: written C-w sequences can surface as a rhyme /-ua-/ or lose /w/. This conflicts with Erickson's unit-labialized-phoneme analysis and must remain profile/lexeme-conditioned. Do not automatically map a written C-w sequence to /Cʷ/ or Ukrainian «кв».

## MekongPhon-informed deterministic Lao engine checkpoint — 2026-11-07

The MekongPhon paper and its reproducible 100-word held-out seed lexicon were used to study a high-performing neural G2P system without importing neural inference into ClippyFirst. The implementation response was to strengthen the deterministic orthographic parser and keep source IPA, tone categories, contour notation and Ukrainian adaptation as separate layers.

### Reusable design principles observed

1. **Syllable/rhyme/tone decomposition:** treat the syllable as onset + rhyme + tone rather than applying a direct grapheme-to-Ukrainian substitution.
2. **Separate segmental and tonal evaluation:** compare `pron_no_tones` and `pron_with_tones` independently; otherwise a contour convention mismatch contaminates segmental CER.
3. **Typed tone categories:** score the tone category separately from its surface contour notation. A tone label is not interchangeable with a contour string.
4. **Fail-closed unsupported structures:** high accuracy on covered cases does not justify fabricating IPA for unanalysed input.
5. **Version and profile explicitness:** exact model/data revisions and a source-scoped Vientiane profile are necessary for reproducible comparison.

### Deterministic changes verified

- Dynamic-programming segmentation for unspaced Lao lexical words while preserving phrase spaces and unparsed material.
- Per-syllable tone-mark placement/order validation.
- Syllable-local short-A coda checks.
- Typed segmental IPA and tone category output, with an evaluation-only adapter to MekongPhon's contour notation.
- Ueda (1994) numeric contour levels converted to IPA tone letters within the one-informant central-Vientiane scope.

Exact PR-head Verify [42309845373](https://github.com/ClippyFirst/Lao-Ukrainian-Phonetic-System/actions/runs/42309845373) passed Python, browser engine, generated-data reproducibility, Chromium UI and built-site checks.

### Comparative result and remaining gap

On the same 97 items covered by both deterministic engines, ClippyFirst is close to Lao2IPA but still slightly behind: segmental CER 7.89% vs 7.72%; tonal CER in the Mekong reference convention 10.67% vs 10.42%. ClippyFirst's full-set coverage is 97%; tone-category exact is 83.33%, versus 87.50% for Lao2IPA. MekongPhon Neural remains the strongest measured engine on the 100-word split.

Three entries remain withheld. Two contain unconsumed material after the vowel; one contains an unsupported consonant or malformed tone-mark placement. No raw lexicon rows or per-item predictions are committed. The current follow-up adds aggregate Unicode-name shapes for parser tails, so any future rule can be reviewed against exact orthographic structures without redistributing the underlying benchmark records.

**Research conclusion:** MekongPhon's most useful transferable ideas are decomposition, explicit tone/rhyme conditioning, typed outputs, and evaluation separation—not neural weights. ClippyFirst has adopted these engineering principles, but it has not yet surpassed Lao2IPA and has no independently adjudicated project IPA gold. Do not claim that it is the best deterministic Lao G2P system yet.

### MekongPhon model architecture notes

The BYU MATRIX Lab model card describes the tonal Lao system as an `EncoderDecoderModel` with a BERT encoder and BERT decoder, 512-dimensional hidden states, six encoder and six decoder layers, eight attention heads, a 1,024-unit feed-forward layer, and character-level tokenizers for both Lao input and IPA-plus-tone output. The non-tonal companion is separately trained with an IPA output vocabulary without tone diacritics. Its documented inference path uses autoregressive generation with beam search (`num_beams=4` in the example) and a maximum sequence length of 128. The model card lists 33.6M parameters and Apache-2.0 for the tonal model. See the [tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-tonal) and [non-tonal model card](https://huggingface.co/byumatrixlab/lao-ipa-nontonal).

The paper reports 367,000 Lao orthographic–IPA pairs and Transformer sequence-to-sequence performance below 2% CER on its held-out test set. Its rule-based tools trade some accuracy for speed. The useful deterministic transfer is not to imitate the neural network with a lookup-free grapheme rewrite; it is to make the rule engine's own intermediate representations similarly explicit: character normalization, structural candidate generation, syllable/rhyme parsing, independent tone assignment, typed IPA output, and separate evaluation contracts. The benchmark's 100-word split is much smaller and different from the paper's sentence-level evaluation; the two scores are not interchangeable. See [Shurtz et al. (LREC 2026)](https://aclanthology.org/2026.lrec-1.129/).

The published model card's architecture does not establish a particular rule for any individual Lao word. It is engineering evidence about tokenization, contextual sequence modeling and separation of tonal/non-tonal tasks—not a source for new phonological correspondences.

### Deterministic comparator design review: lao2ipa 1.0.0

The pinned Apache-2.0 comparator source was reviewed as a separate deterministic reference. It normalizes preposed vowels into post-onset order, merges selected consonant pairs and compound vowel tokens, uses explicit intermediate vowel states, assembles syllable objects, and applies bounded lookahead to reposition tone marks before attaching onset/tone/coda components. Its `Syllable` object separates onset, vowel, coda and tone and applies a Vientiane-oriented live/dead × class × length table. It also carries a broader set of consonant combinations for loan/extended spellings than ClippyFirst's conservative core registry.

Transferable ideas already reflected in ClippyFirst are explicit vowel-token recognition, syllable-level representation, separate tone assignment, and explicit tone placement validation. Do not copy its permissive naive fallback or automatically promote every listed consonant combination into the modern Vientiane core inventory. The comparator's own README describes its grouping and tone placement as heuristics, and its source contains a mix of ordinary Lao and loan/extended clusters; every added form still needs a source/profile claim and tests. The exact upstream source inspected was `byu-matrix-lab/lao2ipa` main at source blob `7b758db2b8c2de2947c0582e7af68a49bbd9e408`; package comparator remains pinned at version 1.0.0 in the hosted benchmark.

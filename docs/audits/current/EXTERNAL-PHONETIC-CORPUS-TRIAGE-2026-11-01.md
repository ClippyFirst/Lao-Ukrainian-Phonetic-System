# External phonetic corpus/source triage — Lao — 2026-11-01

## Candidate: MekongPhon (LREC 2026)

**Disposition: high-priority research lead; NOT imported as gold or training data.** The paper reports 367,000 Lao orthography–IPA pairs and sub-2% CER on held-out data. It also reports a 1.3M Khmer set. These are paper-reported figures, not results independently reproduced by this repository.

- Paper: https://aclanthology.org/2026.lrec-1.129/
- Project: https://github.com/byu-matrix-lab/MekongPhon
- Inspected upstream main commit: `f80f6c1840c4818b51e05f2e00cded4701a5b662`.
- Files include `data/lexicons/lao_lexicon.csv`, `data/splits/lao_train.csv`, `data/splits/lao_eval.csv`, and a 500-sentence qualitative sample.
- The project repository metadata has `license: null`; its tree has no LICENSE/COPYING file. The LREC proceedings page states CC BY-NC 4.0 for proceedings, but that does not automatically license the separate corpus, source lexicon, OPUS data or trained models.
- The documented pipeline scrapes the SEAlang Lao dictionary, normalizes IPA tone marks, downloads OPUS parallel text, and applies a greedy lexicon transliterator. Sentences with out-of-lexicon tokens are filtered out. Thus the sentence IPA is dictionary-generated, not an independently hand-transcribed sentence-level reference.
- The committed split script uses `random.seed(1234)` and reserves only 100 lexicon lines for evaluation. This is a held-out lexical split, not evidence of independent expert adjudication or robust dialect-balanced coverage.
- The paper's “verified” claim is worth investigating, but the accessible project README/pipeline does not document annotator identities, adjudication protocol, dialect stratification, or data licensing at the per-entry level.

## Other candidate: Goruut

The source code is MIT, but the corresponding `neurlang/dataset/lao/` lexicon has no declared repository license, and no per-language rights statement was found. Its derived model assets remain blocked pending provenance/license clarification. See `docs/audits/current/GORUUT-ASSET-LICENSE-REVIEW-2026-11-01.md`.

## Acceptance before use

1. Obtain explicit corpus/lexicon/model license terms and provenance for each component (SEAlang, OPUS corpora, derived IPA, model weights).
2. Obtain the paper and inspect the annotation/verification protocol, dialect profile, IPA conventions, tone treatment and held-out split design.
3. Establish whether the 100-word eval split is independently adjudicated; if not, keep it as a comparator split only.
4. Import no rows until each row has a stable source locator, profile, adjudication status and provenance; retain original IPA exactly.
5. Keep tone, vowel length, syllable boundaries and uncertain readings intact. Do not normalize away tonal distinctions to improve agreement.

Current independent, project-owned, expert-adjudicated Lao gold remains 0. No MekongPhon/Goruut accuracy claim is added to this repository.


## Test-only Goruut runtime evaluation

Added an optional, test-only HTTP runtime probe for Goruut at pinned upstream commit `b224bde02151f8f86d0fe260804e4ca743bda620`. It explicitly enables `Lao` in Goruut's `BuiltinDictLanguages`, builds the upstream Go binary, starts the documented HTTP service and records every raw JSON response for source-engineering probes (including multiword/punctuation cases). `scripts/benchmark_goruut.py` records engine commit, language identifier, input SHA-256, raw response, token outputs and errors. It performs no IPA normalization and always reports `accuracy: null`, independent gold=0. Workflow: `.github/workflows/optional-goruut-runtime.yml`; artifact retention 30 days. Project fixtures are engineering probes, not adjudicated gold.

The earlier asset-license blocker applies to copying, redistribution and production integration. The owner has authorized use for testing only; therefore the optional CI probe may check out and execute the pinned upstream source transiently. It does not persist upstream assets, does not bundle them, and does not approve a production dependency. Linguistic gold and accuracy remain unestablished.


## Goruut runtime evidence update — 2026-11-01

The pinned Goruut runtime was executed, not merely inspected. Go 1.23.12, Lao explicitly enabled; 23 engineering probes yielded 18 usable outputs/5 empty; 100 MekongPhon eval rows yielded 81 usable outputs/19 empty. Strict NFC+outer-whitespace source-attested concordance was 8/100 (8%); heuristic diagnostic: 13 tone-only, 1 tone/length, 59 segmental/format, 19 no output. This is NOT accuracy or gold: MekongPhon sentence IPA is lexicon-generated and its eval is not independent expert adjudication. Server log repeatedly reports missing `weights9.bin.zlib`. Do not promote. Full evidence: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.

Testing-only owner authorization was used to execute the pinned upstream source in ephemeral CI. No external asset was copied into the repository or production artifact. Full report: `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`.


## Repeatability findings — 2026-11-01

Three-repeat re-evaluation supersedes one-shot counts: engineering probes 18/23 usable, with 7/18 usable outputs unstable across repetitions; MekongPhon 81/100 usable, with 13/81 unstable; only 4/100 source-attested rows matched exactly across all three repetitions (10/100 matched at least once). Example `ຄົນ` alternated between `kʰon˩˨` and `kʰon˧˥`. This demonstrates a serious tone/reproducibility defect. It remains source-attested concordance, not accuracy. See runtime evaluation audit.

The three-repeat raw outputs are preserved in workflow artifacts and summarized in `docs/audits/current/GORUUT-RUNTIME-EVALUATION-2026-11-01.md`. Do not treat these results as gold or as a production approval.


## Cross-engine comparison update

Additional optional lao2ipa 1.0.0 run on the 37-case engineering fixture: 0/37 exact string agreements, 31 tone-suffix-only, 2 diphthong-offglide, 4 segmental/vowel-sequence differences; zero runtime errors. The local engine matched its own fixture 37/37, but that fixture is not gold. This points to a major tone-convention difference and six cases requiring segmental review, not a winner. Latest Goruut three-repeat: 18/23 engineering outputs, 12 stable/6 unstable; 81/100 MekongPhon outputs, 70 stable/11 unstable; 5/100 all-repeat source-attested exact/notation matches, 10/100 at least one repeat. Accuracy remains null.

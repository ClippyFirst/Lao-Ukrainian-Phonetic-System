# Lao → Ukrainian project glossary

This glossary defines repository terms. It does not replace the cited Lao phonology literature or turn project policy into a linguistic fact.

| Term | Meaning in this repository |
|---|---|
| **Source orthography** | The original Lao Unicode text supplied by the user. Preserve it under the declared normalization contract. |
| **Orthographic syllable** | A structurally parsed Lao unit. The parser is syllable-oriented; it is not a lexical word segmenter. |
| **Nucleus** | The vowel structure identified by a canonical vowel registry row, including its nucleus type and quantity. |
| **Rhyme** | The vowel nucleus together with any coda. Rhyme structure, not a length label alone, determines the live/dead classification used by the tone model. |
| **Coda** | The final consonantal element of a syllable, including its source registry classification and IPA realization when established. |
| **Live / dead syllable** | Project phonological classes used by the Vientiane-oriented tone model. Open diphthong and nasal-final AM rhymes are live; stop codas are dead in the documented model. |
| **Tone selector / tone mark** | A written Lao tone mark. Its encoded position and onset/rhyme environment are validated before tone or IPA is emitted. |
| **Tone contour** | The source-language tonal realization recorded separately from Ukrainian spelling. Tone differences are not cosmetic string variants. |
| **IPA adapter boundary** | The inspectable result of Lao phonological analysis consumed by the Ukrainian target adapter. The primary phonetic route must pass through this boundary. |
| **Ukrainian practical form** | A project-specific readable Ukrainian rendering derived from established IPA correspondences; not an official national standard. |
| **Romanization route** | A separate, lower-information orthographic route (CLDR/BGN-oriented) with source-aware syllable checks. It is not a pronunciation substitute and cannot reconstruct tone. |
| **Structural fixture** | An engineering regression case for parsing, Unicode or source integrity. It is not lexical IPA gold. |
| **Independent IPA gold** | A rights-cleared, source-located, independently annotated and adjudicated record eligible for held-out scoring. The corpus remains empty until the human workflow completes. |
| **Reference profile** | The bounded pilot target: contemporary central Vientiane Lao, careful citation-form speech (lao-vientiane-careful-citation-v1). It is not a universal Lao dialect claim. |

## Canonical decisions and evidence

- Research decisions: docs/decision-log.md.
- Current execution and blockers: docs/MASTER-EXECUTION-PLAN-AND-CHAT-HANDOFF.md.
- Phonology and corpus evidence: docs/audits/current/.
- Canonical source registries: data/lao/*.csv; generated browser mirror: web/data.js.

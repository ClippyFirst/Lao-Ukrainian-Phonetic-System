# Independent IPA gold corpus

**Status: infrastructure implemented; linguistic gold remains empty and release gate is intentionally closed.**

This workflow adds an auditable lifecycle around the existing `scripts/benchmark_ipa.py` scorer. It does not create IPA labels, derive labels from orthography, or promote Goruut, Epitran, myG2P, romanizers or other engine output to gold.

## Data model

The corpus is JSON Lines so that IPA features remain typed and inspectable:

| File | Purpose |
|---|---|
| `records.jsonl` | Source orthography, lexeme grouping, pronunciation profile, provenance and rights |
| `annotations.jsonl` | Two independent expert IPA annotations per adjudicated item |
| `adjudications.jsonl` | Third-person adjudication, decision, final IPA and rationale |
| `splits.jsonl` | Frozen, deterministic train/dev/test assignment |
| `gold.tsv` | Generated export consumed by the existing IPA benchmark; never hand-edit |
| `predictions.tsv` | Candidate outputs, retaining raw output and explicit IPA kind |

JSON Schemas are in `schemas/ipa-gold-*.schema.json`. The standard-library validator is the executable cross-file contract.

### Record

Every record carries:
- stable `record_id`, `language`, source orthography and normalized orthography;
- `lexeme_group_id`, used to prevent lexical leakage across data splits;
- a pronunciation `profile` (variety and optional region, register, pseudonymous speaker/audio IDs);
- source citation, exact page/entry/audio locator, license identifier, rights status, redistribution permission and optional SHA-256.

Do not put speaker names, contact details or other personal data in the public corpus. Use pseudonymous IDs. Store audio only when the source rights and consent permit it; otherwise keep an exact external locator and checksum where available.

### IPA annotation

Each annotation has a distinct annotation ID and annotator ID, confidence, uncertainty notes and date. IPA is typed as:
- `PHONEMIC`;
- `PHONETIC_BROAD`;
- `PHONETIC_NARROW`.

The IPA object preserves its literal value plus syllable boundaries, tone, vowel length and phonation where applicable. These fields are not collapsed into a single untyped string. The validator requires NFC and refuses to silently rewrite the IPA.

### Double annotation and adjudication

An adjudicated record requires:
1. exactly two annotations by distinct annotators;
2. an adjudicator whose ID differs from both annotators;
3. explicit references to both annotation IDs;
4. a documented decision:
   - `AGREEMENT`: both annotations and final IPA must match exactly, including IPA kind;
   - `RESOLVED`: the annotations differ and the adjudicator records a final IPA plus a rationale;
   - `UNRESOLVED`: final IPA must be null; the record is not gold.

**Blindness is an operational requirement, not something Git can guarantee.** Collect the two submissions independently in a controlled intake channel. Do not expose annotator A's IPA to annotator B before both submissions are locked. Merge the two submissions only after that point, then give them to the independent adjudicator. Do not use public PRs or a public shared working copy as the blind collection channel.

Annotator IDs should be stable pseudonyms; keep the identity mapping outside this public repository. Annotations should cite evidence and mark uncertainty rather than silently resolving disputed pronunciations.

## Splits and leakage

Run:

```bash
python scripts/ipa_gold_corpus.py assign-splits --seed clippyfirst-ipa-gold-v1
python scripts/ipa_gold_corpus.py validate --language LANGUAGE
```

The assignment uses SHA-256 of the fixed seed and `lexeme_group_id`, with an 80/10/10 train/dev/test target. Existing assignments are preserved when new records are added. All records in one lexical group must remain in one split. Never change the seed or rewrite the frozen manifest after model development begins; create a new versioned corpus release if a split redesign is scientifically necessary.

This initial manifest prevents lexical-item leakage. It is not yet a speaker-held-out acoustic evaluation protocol. If the research question requires generalization to unseen speakers, create a separate speaker-disjoint evaluation manifest rather than claiming the lexical split tests speaker generalization.

## Commands

Validate the structure and evidence links without claiming accuracy:

```bash
python scripts/ipa_gold_corpus.py validate --language LANGUAGE
```

Export only `AGREEMENT` or `RESOLVED` records whose source is marked redistributable:

```bash
python scripts/ipa_gold_corpus.py export-gold --language LANGUAGE
```

Check release-gold readiness:

```bash
python scripts/ipa_gold_corpus.py gate --language LANGUAGE --min-train 100 --min-dev 25 --min-test 25
```

The initial gate policy requires at least 100 adjudicated train items, 25 dev items and 25 test items, all with frozen splits and redistributable source rights. These are project release thresholds, not a universal statistical sufficiency claim. The corpus must also cover the phonological contrasts relevant to the language-specific research profile; row counts alone are not enough.

## Benchmark semantics

The generated TSV keeps the existing scorer contract and adds `ipa_kind`. A candidate prediction with the same symbol string but a different or missing IPA kind is not an exact match. Tone, length, syllable boundaries and phonation remain significant in the actual IPA string; no tone-stripping or broad-to-narrow coercion is performed.

The existing code-point CER remains a string-distance diagnostic, not a phonetic-feature metric. Report exact-match denominators, missing predictions, type mismatches, profiles and versions. Do not present a small curated sample as population accuracy.

## CI and release policy

- Normal CI runs structural validation. An empty corpus is valid as a research state and reports `NOT_READY_NO_ADJUDICATED_GOLD`.
- `.github/workflows/ipa-gold-release-gate.yml` runs on version tags and manual dispatch. It fails closed until the adjudicated, redistributable, split gold thresholds are met.
- This workflow does not change repository rulesets or branch protection. Repository owners must require the release-gate check in their release/tag procedure; the workflow runs after a tag is pushed and cannot itself prevent a person with permission from creating a tag.
- Passing this gold-data gate does not, by itself, establish that a language engine or Ukrainian adapter is accurate or production-ready. Feature-stratified phonological evaluation and a separately approved product-quality threshold remain required.

## Current corpus status

The four JSONL files are intentionally empty. `gold.tsv` remains header-only. No expert IPA labels have been fabricated. The release gate must fail today.

## Rights verification

The source `license_id` must exist in `data/benchmark/licenses.json`; an arbitrary free-text license label is rejected. Each record also needs `rights_evidence` with a basis, exact locator, verifier pseudonym and verification date. A source cannot be marked redistributable when its registered license disallows redistribution, or when rights are restricted/unknown. The non-commercial CC BY-NC-SA 4.0 entry is explicitly non-redistributable for this product corpus. Project-created material is also non-redistributable by default until the owner approves a corpus license and contributor permissions.

The generated `gold.tsv` carries `license_id` and `rights_evidence_locator` alongside `source_id`, and the benchmark report preserves these fields. CC BY-SA share-alike and attribution duties still need to be honored in the distribution package; the registry records those terms rather than silently waiving them.


### Runtime/schema parity checkpoint — 2026-11-01

The standard-library validator now enforces the schema's closed top-level record, annotation, adjudication and split objects; the IPA object rejects unknown properties; required annotation notes and string-array uncertainty are checked; and rights-verification, annotation and adjudication dates must be canonical ISO calendar dates. Optional segmentation/profile/source fields are type-checked. The benchmark requires a valid ipa_kind for every adjudicated gold row and a prediction kind column; a non-empty prediction with a missing or different kind is not comparable for exact match or code-point CER. These checks are covered by regression tests and exact-head CI.

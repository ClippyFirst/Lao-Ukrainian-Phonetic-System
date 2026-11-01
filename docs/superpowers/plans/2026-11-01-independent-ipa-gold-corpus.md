# Independent IPA Gold Corpus Implementation Plan

> Executed autonomously under the repository continuation instruction. Tests-first implementation; do not create IPA labels or infer gold.

**Goal:** Add an auditable, independently annotated IPA gold-corpus lifecycle and release gate while reusing the existing `benchmark_ipa.py` scorer.

**Architecture:** Standard-library Python CLI validates JSONL records, independent annotations, adjudications and frozen group-aware split manifests. Only adjudicated, redistributable records are exported into the existing TSV scorer. Normal CI validates structure without claiming readiness; tag/manual release CI fails closed until policy thresholds are met.

**Tech Stack:** Python 3.12 standard library, JSONL, JSON Schema 2020-12, GitHub Actions.

**Spec:** Existing `docs/benchmarking-and-external-ipa.md`, `data/benchmark/gold.tsv`, `scripts/benchmark_ipa.py`, and the current language-specific phonology/evidence audits.

## Global Constraints
- Preserve the source orthography → structural analysis → language phonology → typed IPA → Ukrainian adaptation pipeline.
- IPA is typed as phonemic, broad phonetic or narrow phonetic; never silently normalize tone, length, boundaries or phonation away.
- Two distinct annotators and a third adjudicator are required for an adjudicated record.
- Source provenance and redistribution rights are mandatory; restricted material must not enter the public gold export.
- Split by lexeme group with deterministic hashing and frozen assignments; prevent train/dev/test leakage.
- Existing benchmark scorer remains the scoring implementation; no synthetic data enters the real corpus.
- External G2P outputs remain candidate predictions, never gold.

## Tasks
1. Add failing CLI integration tests for double annotation, adjudication, split leakage, deterministic assignment, rights gating, export and empty-gold release rejection.
2. Implement the JSONL validator and deterministic split assignment with standard library only.
3. Add versioned JSON Schemas and empty corpus templates; retain the current header-only gold TSV.
4. Add a strict gold export path into the existing benchmark TSV contract.
5. Add normal-CI structural validation and a tag/manual release workflow with minimum split thresholds.
6. Add language-specific phonology research backlogs and evidence rules without inventing linguistic labels.
7. Update master matrix and handoff, run the full CI workflows on the exact PR head, inspect results and open PRs.

## Acceptance
- Synthetic fixtures test mechanics only and are explicitly labelled as synthetic test fixtures.
- The real corpus remains empty until expert work supplies admissible records.
- Validation reports NOT_READY rather than zero accuracy when no adjudicated rows exist.
- Release gate cannot pass without minimum adjudicated train/dev/test coverage, two annotators, separate adjudicator, source rights and frozen splits.
- All existing repository tests/build checks remain green.

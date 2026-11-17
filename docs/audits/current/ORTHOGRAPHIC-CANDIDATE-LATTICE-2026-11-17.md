# Lao orthographic candidate lattice — 2026-11-17

## Purpose

Add an inspectable, fail-closed candidate graph for syllable boundaries in one NFC-normalized Lao token. This is a separate analysis API; it does not replace the existing production segmentation policy.

## Implementation

- `src/lao_ukrainian/orthographic_lattice.py` enumerates every non-empty code-point span and asks the existing `parse_syllable()` recognizer whether that span is a complete supported syllable.
- Candidate spans become directed edges between Python Unicode code-point offsets.
- Forward reachability and backward reachability remove dead edges that cannot participate in any complete path.
- A dynamic program counts complete paths with saturation at 2. The result distinguishes `NO_COMPLETE_PATH`, `UNIQUE`, and `AMBIGUOUS` without enumerating exponentially many paths.
- The function returns live and dead candidates, source spans, the unique path only when exactly one path exists, and explicit limitations.
- Input must be one NFC-normalized token. The API does not silently normalize or strip whitespace/ZWSP, so returned offsets remain tied to the supplied text.

## Deliberate boundaries

This is a candidate graph over the repository's *current* single-syllable recognizer, not a complete modern Lao orthographic grammar. It inherits that recognizer's inventory and constraints. A unique path means unique under this current candidate inventory only; it is not proof of linguistic uniqueness.

The implementation does not:
- model a grapheme that serves overlapping coda and onset roles;
- resolve lexical or Pali/Sanskrit loanword boundaries;
- select a pronunciation or infer IPA from orthographic segmentation;
- add the historical Berment grammar's OCR-damaged terminals;
- change `segment_syllables()`, the public conversion pipeline, or generated data.

LOC Note 10 therefore remains separately unresolved: the exact current Word-source spelling `ຄຼິສຕຽນ` is expected to have no complete path under the present recognizer, and this API does not assign its shared `ສ` roles.

## Tests

`tests/test_orthographic_lattice.py` covers:
- a unique graph path and pruning of a dead edge;
- preservation of multiple complete paths as `AMBIGUOUS`;
- no-path behavior;
- path-count saturation at 2;
- a known multi-syllable Lao token;
- fail-closed behavior for the exact LOC Note 10 token;
- one-token and NFC input contracts.

CI verification is pending at the time this note is authored. No local test result is claimed.

## Evidence and next acceptance

The graph shape follows Berment (2004), Part III §§III.2.3–III.2.6 and Annex A.11/A.14, as recorded in the Undermind research note `orthographic-parsing-boundaries-2026-11-16.md`. Berment's historical grammar is evidence for candidate-lattice and dead-branch concepts, not a validated modern rule set. The exact Lao terminals must still be transcribed from page images/Prolog source, reconciled with current Unicode and modern orthography, and reviewed by a qualified Lao specialist.

Next acceptance:
1. independently validate candidate spans against modern, source-located Lao examples;
2. add adversarial cases for preposed/above/below/postposed vowel components, tone marks, high-class digraphs, and Pali/loan spellings;
3. determine whether shared coda/onset roles need a distinct overlapping-role edge representation;
4. obtain Lao-specialist adjudication before considering any production segmentation-policy change.

Status: candidate graph implementation = engineering prototype pending CI; current orthographic grammar = PARTIAL / TODO; global ambiguity resolution = BLOCKED / evidence-limited; LOC Note 10 automatic source-role derivation = PARTIAL / BLOCKED.

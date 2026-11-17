# Lao orthographic candidate lattice — 2026-11-17

## Purpose

Add an inspectable, fail-closed candidate graph for syllable boundaries in one NFC-normalized Lao token. This is a separate analysis API; it does not replace the existing production segmentation policy.

## Implementation

- `src/lao_ukrainian/orthographic_lattice.py` enumerates every non-empty code-point span and asks the existing `parse_syllable()` recognizer whether that span is a complete supported syllable.
- Candidate spans become directed edges between Python Unicode code-point offsets.
- Forward reachability and backward reachability remove dead edges that cannot participate in any complete path.
- Exact dynamic-programming path counts identify convergence offsets (vertices traversed by every complete path); the public count is capped to 0, 1, or 2 (meaning 2+). Consecutive convergence offsets bound ambiguity eyes, whose candidate edges and capped local path count are returned. No paths are enumerated.
- The function returns live and dead candidates, source spans, convergence offsets, ambiguity eyes, the unique path only when exactly one path exists, and explicit limitations.
- Input must be one NFC-normalized token. The API does not silently normalize or strip whitespace/ZWSP, so returned offsets remain tied to the supplied text.

## Primary-source refinement — Berment (2004)

The primary thesis PDF was retrieved from the author's/publisher-hosted URL and inspected on 2026-11-17. Printed pages (not PDF viewer page indices) provide the following evidence:

- p. 132 (§III.2.3.2): the historical Lao grammar enumerates nine final consonant graphemes and explicitly describes vowel components before, after, above or below the onset. Exact glyph transcription should be checked against the thesis page image or Prolog annex; OCR can damage Lao glyphs.
- p. 133: Berment warns that the simplified grammar accepts theoretical unattested forms (example ມວອ) and simplifies accent placement. It is a historical candidate grammar, not a contemporary spelling validator.
- p. 145 (§III.2.5.1): the thesis gives ແຂກະ as an irreducible ambiguity: a one-syllable analysis and the two-syllable analysis ແຂ + ກະ.
- pp. 146–147: syllable candidates are graph edges over text positions; complete segmentations are start-to-end paths; dead edges cannot participate in a complete path; convergence points are offsets traversed by all complete segmentations.
- p. 148 (§III.2.5.2): “eyes” are ambiguous path regions between consecutive convergence points. Longest-candidate selection is a local UI selection heuristic, not a global linguistic segmentation rule.

The current API now computes convergence offsets and ambiguity eyes, but its candidate inventory is still the repository's present parse_syllable() recognizer. The source's one-syllable reading of ແຂກະ has not yet been demonstrated by that recognizer. Add a modern, source-validated positive candidate and its competing segmentation before treating this source example as implemented.

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
- convergence offsets and ambiguity eyes, including two ambiguous regions separated by a convergence point;
- preservation of multiple complete paths as `AMBIGUOUS`;
- no-path behavior;
- path-count saturation at 2;
- a known multi-syllable Lao token;
- fail-closed behavior for the exact LOC Note 10 token;
- one-token and NFC input contracts.

The first PR-head Verify passed before the convergence/eye extension. Exact-head CI for the extension is pending; no local test result is claimed.

## Evidence and next acceptance

The graph shape follows Berment (2004), printed pp. 132–133 and 145–148, Part III §§III.2.3–III.2.6, and Annexes A.11/A.14, as recorded in the Undermind research note `orthographic-parsing-boundaries-2026-11-16.md`. Berment's historical grammar is evidence for candidate-lattice and dead-branch concepts, not a validated modern rule set. The exact Lao terminals must still be transcribed from page images/Prolog source, reconciled with current Unicode and modern orthography, and reviewed by a qualified Lao specialist.

Next acceptance:
1. independently validate candidate spans against modern, source-located Lao examples;
2. add adversarial cases for preposed/above/below/postposed vowel components, tone marks, high-class digraphs, and Pali/loan spellings;
3. determine whether shared coda/onset roles need a distinct overlapping-role edge representation;
4. obtain Lao-specialist adjudication before considering any production segmentation-policy change.

Status: candidate graph plus convergence/eye extraction = DONE_VERIFIED as a bounded engineering API (PR #261; exact PR-head and exact-main Verify passed); current orthographic grammar = PARTIAL / TODO; global ambiguity resolution = BLOCKED / evidence-limited; LOC Note 10 automatic source-role derivation = PARTIAL / BLOCKED.

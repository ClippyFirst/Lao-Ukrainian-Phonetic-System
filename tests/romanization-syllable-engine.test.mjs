import test from "node:test";
import assert from "node:assert/strict";
import { analyzeRomanization } from "../web/romanization-syllable-engine.js";

test("romanization engine parses a syllable into onset, nucleus and coda", () => {
  const result = analyzeRomanization("kha");
  assert.equal(result.status, "OK");
  assert.equal(result.output, "кга");
  assert.deepEqual(result.syllables.map(({ onset, nucleus, coda, ukrainian }) =>
    ({ onset, nucleus, coda, ukrainian })), [
      { onset: "kh", nucleus: "a", coda: "", ukrainian: "кга" },
    ]);
});

test("h is consistently adapted as Ukrainian г, including within romanization digraphs", () => {
  assert.equal(analyzeRomanization("ha kha tha pha").output, "га кга тга пга");
});

test("the engine handles CLDR preposed-vowel syllable patterns in Ukrainian syllable order", () => {
  assert.equal(analyzeRomanization("éka aik").output, "ке кай");
});

test("the engine uses position-aware coda mappings", () => {
  assert.equal(analyzeRomanization("khat khap khang").output, "кгат кгап кганг");
});

test("spaces and punctuation remain intact around analyzed syllables", () => {
  assert.equal(analyzeRomanization("kha, tha!").output, "кга, тга!");
});

test("ambiguous continuous romanization is withheld rather than arbitrarily segmented", () => {
  const result = analyzeRomanization("khakha");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦khakha⟧");
  assert.equal(result.syllables[0].status, "AMBIGUOUS");
});

test("unsupported romanization remains visible and is flagged partial", () => {
  const result = analyzeRomanization("kha ໞ");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "кга ⟦ໞ⟧");
});

test("h remains г even in a syllable-final position", () => {
  assert.equal(analyzeRomanization("ah").output, "аг");
});

test("the coda-vowel correspondence follows the documented BGN/PCGN context", () => {
  assert.equal(analyzeRomanization("kiv kav").output, "кіоу кав");
});

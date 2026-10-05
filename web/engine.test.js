import test from "node:test";
import assert from "node:assert/strict";
import { analyze } from "./engine.js";

test("basic long syllable", () => {
  const r = analyze("ຂາ");
  assert.equal(r.status, "OK");
  assert.equal(r.syllables[0].ipa, "kʰaː");
  assert.equal(r.output, "ка");
});

test("preposed vowel is analysed with following onset", () => {
  const r = analyze("ໄກ່");
  assert.ok(r.syllables[0].ipa);
  assert.equal(r.syllables[0].ukrainian, "кай");
});

test("voiced onset has Ukrainian target", () => {
  const r = analyze("ດາ");
  assert.equal(r.syllables[0].ipa, "daː");
  assert.equal(r.syllables[0].ukrainian, "да");
});

test("structural ໜ is not split as an ordinary first code point", () => {
  const r = analyze("ໜາ");
  assert.equal(r.syllables[0].onset, "ໜ");
  assert.equal(r.syllables[0].ipa, "hnaː");
  assert.equal(r.syllables[0].status, "ANALYSIS DEPENDENT");
});

test("uncertainty is explicit", () => {
  const r = analyze("ຂ");
  assert.equal(r.status, "PARTIAL");
  assert.ok(r.warnings.length);
});

test("empty input", () => assert.equal(analyze("").status, "EMPTY"));

import test from "node:test";
import assert from "node:assert/strict";
import { analyze } from "./engine.js";

test("basic long syllable", () => {
  const r = analyze("ຂາ");
  assert.equal(r.status, "OK");
  assert.equal(r.syllables[0].ipa, "kʰaː");
  assert.equal(r.output, "ка");
});

test("preposed long and short e are distinguished", () => {
  assert.equal(analyze("ເກ").syllables[0].ipa, "keː");
  assert.equal(analyze("ເກະ").syllables[0].ipa, "ke");
});

test("preposed ai with tone mark", () => {
  const r = analyze("ໄກ່");
  assert.equal(r.syllables[0].ipa, "kai");
  assert.equal(r.syllables[0].ukrainian, "кай");
  assert.equal(r.syllables[0].tone, "high-mid");
});

test("voiced onset has Ukrainian target", () => {
  const r = analyze("ດາ");
  assert.equal(r.syllables[0].ipa, "daː");
  assert.equal(r.syllables[0].ukrainian, "да");
});

test("vowel carrier does not inject glottal stop into IPA", () => {
  const r = analyze("ອາ");
  assert.equal(r.syllables[0].ipa, "aː");
  assert.equal(r.output, "а");
});

test("checked coda is dead", () => {
  const r = analyze("ກັບ");
  assert.equal(r.syllables[0].ipa, "kap");
  assert.equal(r.syllables[0].syllableType, "dead");
  assert.equal(r.output, "кап");
});

test("long open o carrier is recognised", () => {
  const r = analyze("ອໍ");
  assert.equal(r.syllables[0].ipa, "ɔː");
  assert.equal(r.output, "о");
});

test("structural ໜ remains explicitly uncertain", () => {
  const r = analyze("ໜາ");
  assert.equal(r.syllables[0].onset, "ໜ");
  assert.equal(r.syllables[0].ipa, "hnaː");
  assert.equal(r.syllables[0].status, "ANALYSIS DEPENDENT");
});

test("invalid mixed script is rejected", () => {
  const r = analyze("ກа");
  assert.equal(r.status, "INVALID");
  assert.equal(r.output, "");
});

test("empty input", () => assert.equal(analyze("").status, "EMPTY"));

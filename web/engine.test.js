import test from "node:test";
import assert from "node:assert/strict";
import { analyze } from "./engine.js";

test("basic long syllable", () => {
  const r = analyze("ຂາ");
  assert.equal(r.status, "OK");
  assert.equal(r.syllables[0].ipa, "kʰaː");
  assert.equal(r.output, "ка");
});

test("middle and low class inherent tones differ", () => {
  assert.equal(analyze("ກາ").syllables[0].tone, "low-rising");
  assert.equal(analyze("ຄາ").syllables[0].tone, "high-rising");
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

test("Lao h maps to Ukrainian г in the project policy", () => {
  const r = analyze("ຫາ");
  assert.equal(r.syllables[0].ipa, "haː");
  assert.equal(r.syllables[0].ukrainian, "га");
});

test("checked coda is dead", () => {
  const r = analyze("ກັບ");
  assert.equal(r.syllables[0].ipa, "kap");
  assert.equal(r.syllables[0].syllableType, "dead");
  assert.equal(r.output, "кап");
});

test("closed uo spelling is recognised", () => {
  const r = analyze("ດວງ");
  assert.equal(r.syllables[0].ipa, "duːəŋ");
  assert.equal(r.output, "дуанг");
});

test("open uo spelling is recognised", () => {
  const r = analyze("ກວາງ");
  assert.equal(r.syllables[0].ipa, "kuːəŋ");
  assert.equal(r.output, "куанг");
});

test("medial ອ is long ɔ", () => {
  const r = analyze("ຈອກ");
  assert.equal(r.syllables[0].ipa, "tɕɔːk");
  assert.equal(r.output, "чок");
});

test("mai ti and mai catawa are not dropped", () => {
  assert.equal(analyze("ກ໊າ").syllables[0].tone, "high-falling");
  assert.equal(analyze("ກ໋າ").syllables[0].tone, "low-rising");
});

test("silent high-class digraph is phonologically n", () => {
  const r = analyze("ຫນອງ");
  assert.equal(r.syllables[0].ipa, "nɔːŋ");
  assert.equal(r.syllables[0].class, "high");
  assert.equal(r.syllables[0].tone, "low-rising");
});

test("atomic high-class ໜ is phonologically n", () => {
  const r = analyze("ໜາ");
  assert.equal(r.syllables[0].ipa, "naː");
  assert.equal(r.syllables[0].class, "high");
  assert.equal(r.syllables[0].tone, "low-rising");
});

test("modern Lao ຣ defaults to l but remains analysis-dependent", () => {
  const r = analyze("ຣະ");
  assert.equal(r.syllables[0].ipa, "la");
  assert.equal(r.syllables[0].status, "ANALYSIS DEPENDENT");
});

test("carrier does not inject glottal stop", () => {
  const r = analyze("ອາ");
  assert.equal(r.syllables[0].ipa, "aː");
  assert.equal(r.output, "а");
});

test("long open o carrier is recognised", () => {
  const r = analyze("ອໍ");
  assert.equal(r.syllables[0].ipa, "ɔː");
  assert.equal(r.output, "о");
});

test("invalid mixed script is rejected", () => {
  const r = analyze("ກа");
  assert.equal(r.status, "INVALID");
  assert.equal(r.output, "");
});

test("empty input", () => assert.equal(analyze("").status, "EMPTY"));

test("multisyllabic Lao text is segmented without dropping syllables", () => {
  const r = analyze("ພາສາລາວ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ພາ|ສາ|ລາວ");
  assert.equal(r.output, "паса лав");
  assert.equal(r.syllables.every((s) => s.ipa), true);
});

test("short o in a closed syllable is recognised", () => {
  const r = analyze("ຄົນ");
  assert.equal(r.syllables[0].ipa, "kʰon");
  assert.equal(r.output, "кон");
});

test("compound greeting is segmented into all syllables", () => {
  const r = analyze("ສະບາຍດີ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ສະ|ບາຍ|ດີ");
  assert.equal(r.output, "са бай ді");
});

test("multi-syllable place-name phrase is not truncated", () => {
  const r = analyze("ຂອບໃຈ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ຂອບ|ໃຈ");
  assert.equal(r.output, "коп чай");
});

test("unparsed characters remain visible instead of being silently dropped", () => {
  const r = analyze("ຄົນ🙂");
  assert.match(r.output, /⟦🙂⟧/);
  assert.equal(r.status, "PARTIAL");
});

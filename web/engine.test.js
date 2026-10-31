import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { analyze } from "./engine.js";
import { CORRESPONDENCES } from "./data.js";

test("basic long syllable", () => {
  const r = analyze("ຂາ");
  assert.equal(r.status, "OK");
  assert.equal(r.syllables[0].ipa, "kʰaː");
  assert.equal(r.output, "к\u0027а");
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

test("multiple adjacent tone marks withhold the entire malformed token", () => {
  const r = analyze("ກ່້າ");
  assert.equal(r.status, "PARTIAL");
  assert.equal(r.syllables.length, 1);
  assert.equal(r.syllables[0].ipa, null);
  assert.equal(r.syllables[0].ukrainian, null);
  assert.ok(r.syllables[0].warnings.some((w) => w.startsWith("MULTIPLE_TONE_MARKS")));
  assert.equal(r.output, "⟦ກ່້າ⟧");
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

test("CRLF is accepted as line whitespace", () => {
  const r = analyze("ກາ\r\nຂາ");
  assert.notEqual(r.status, "INVALID");
  assert.equal(r.output, "ка к\u0027а");
});

test("zero-width space is rejected rather than silently removed", () => {
  const r = analyze("ກ\u200bຂ");
  assert.equal(r.status, "INVALID");
  assert.equal(r.output, "");
});

test("empty input", () => assert.equal(analyze("").status, "EMPTY"));

test("multisyllabic Lao text is segmented without dropping syllables", () => {
  const r = analyze("ພາສາລາວ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ພາ|ສາ|ລາວ");
  assert.equal(r.output, "п\u0027асалав");
  assert.equal(r.syllables.every((s) => s.ipa), true);
});

test("unclosed short vowels withhold IPA, Ukrainian output and tone", () => {
  for (const surface of ["ກັ", "ກັອ"]) {
    const result = analyze(surface);
    const syllable = result.syllables[0];
    assert.equal(syllable.status, "EVIDENCE LIMITED");
    assert.equal(syllable.ipa, null);
    assert.equal(syllable.ukrainian, null);
    assert.equal(syllable.tone, null);
    assert.equal(syllable.toneContour, null);
    assert.ok(syllable.rules.includes("TONE-RULE:TONE-NOT-ESTABLISHED-FOR-COMBINATION"));
  }
});

test("matched tone rule exposes its contour", () => {
  assert.equal(analyze("ຂາ").syllables[0].tone, "low-rising");
  assert.equal(analyze("ຂາ").syllables[0].toneContour, "˩˥");
});

test("shared tone contour and structural withholding fixture", () => {
  const fixturePath = resolve(dirname(fileURLToPath(import.meta.url)), "../tests/fixtures/tone_contour_cases.json");
  const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));
  assert.equal(fixture.schema_version, 1);
  for (const item of fixture.cases) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    const syllable = result.syllables[0];
    assert.equal(syllable.tone, item.tone, item.id);
    assert.equal(syllable.toneContour, item.tone_contour, item.id);
    assert.equal(syllable.ipa, item.ipa, item.id);
    assert.equal(syllable.ukrainian, item.ukrainian, item.id);
    assert.equal(syllable.status, item.status, item.id);
  }
});

test("short o in a closed syllable is recognised", () => {
  const r = analyze("ຄົນ");
  assert.equal(r.syllables[0].ipa, "kʰon");
  assert.equal(r.output, "к\u0027он");
});

test("compound greeting is segmented into all syllables", () => {
  const r = analyze("ສະບາຍດີ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ສະ|ບາຍ|ດີ");
  assert.equal(r.output, "сабайді");
});

test("multi-syllable place-name phrase is not truncated", () => {
  const r = analyze("ຂອບໃຈ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ຂອບ|ໃຈ");
  assert.equal(r.output, "к\u0027опчай");
});

test("unparsed characters remain visible instead of being silently dropped", () => {
  const r = analyze("ຄົນຆ");
  assert.match(r.output, /⟦ຆ⟧/);
  assert.equal(r.status, "PARTIAL");
});

test("standalone ຽ vowel sign is parsed in ວຽງ", () => {
  const r = analyze("ວຽງ");
  assert.equal(r.status, "OK");
  assert.equal(r.syllables.length, 1);
  assert.equal(r.syllables[0].ipa, "ʋiːəŋ");
  assert.equal(r.output, "віанг");
});

test("Vientiane place name does not leave ວ ຽ ງ unresolved", () => {
  const r = analyze("ວຽງຈັນ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ວຽງ|ຈັນ");
  assert.equal(r.output, "віангчан");
  assert.equal(r.status, "OK");
});

test("postposed vowel sign before an onset remains an unresolved whole token", () => {
  const surface = "ະຄອນ";
  const r = analyze(surface);
  assert.equal(r.status, "PARTIAL");
  assert.equal(r.syllables.length, 1);
  assert.equal(r.syllables[0].surface, surface);
  assert.equal(r.syllables[0].ipa, null);
  assert.equal(r.syllables[0].ukrainian, null);
  assert.equal(r.output, "⟦" + surface + "⟧");
});

test("syllable boundary avoids consuming next onset as coda before vowel sign", () => {
  const r = analyze("ພະນະຄອນ");
  assert.equal(r.syllables.map((s) => s.surface).join("|"), "ພະ|ນະ|ຄອນ");
  assert.equal(r.output, "п\u0027анак\u0027он");
});


test("preposed oe short and long vowel complexes are distinguished", () => {
  const short = analyze("ເກິ");
  const long = analyze("ເກີ");
  assert.equal(short.syllables[0].vowel, "ɤ");
  assert.equal(short.syllables[0].ipa, "kɤ");
  assert.equal(long.syllables[0].vowel, "ɤː");
  assert.equal(long.syllables[0].ipa, "kɤː");
});

test("preposed long IA spellings match the source-indexed patterns", () => {
  for (const surface of ["ເກັຽ", "ເກຍ"]) {
    const r = analyze(surface);
    assert.equal(r.syllables[0].vowel, "iːə", surface);
    assert.equal(r.syllables[0].ipa, "kiːə", surface);
  }
});

test("preposed short IA is distinct from long IA", () => {
  const r = analyze("ເກັຍ");
  assert.equal(r.syllables[0].vowel, "iə");
  assert.equal(r.syllables[0].ipa, "kiə");
});

test("unattested preposed ເ◌ຽ remains one unresolved token", () => {
  const surface = "ເກຽ";
  const r = analyze(surface);
  assert.equal(r.status, "PARTIAL");
  assert.equal(r.syllables.length, 1);
  assert.equal(r.syllables[0].surface, surface);
  assert.equal(r.syllables[0].ipa, null);
  assert.equal(r.syllables[0].ukrainian, null);
  assert.ok(r.syllables[0].warnings.length > 0);
  assert.equal(r.output, "⟦" + surface + "⟧");
});


test("shared vowel precedence fixtures match browser phonemic IPA", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const fixture = JSON.parse(readFileSync(resolve(here, "../tests/fixtures/vowel_precedence_cases.json"), "utf8"));
  assert.equal(fixture.schema_version, 1);
  for (const item of fixture.cases) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, `${item.id}: fixture must remain one syllable`);
    assert.equal(result.syllables[0].surface, item.surface, item.id);
    assert.equal(result.syllables[0].ipa, item.phonemic_ipa, item.id);
  }
});


test("short Lao vowel signs require a coda when specified by the spelling", () => {
  assert.equal(analyze("ກັ").status, "PARTIAL");
  const closedO = analyze("ກັອບ");
  assert.equal(closedO.syllables[0].ipa, "kɔp");
  assert.equal(closedO.status, "OK");
});


test("coda must be the final grapheme of syllable material", () => {
  const result = analyze("ກາງເ");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.syllables.some((s) => s.surface === "ກາງເ" && s.coda === "ງ"), false);
});


test("shared legal coda inventory matches browser phonemic IPA", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const fixture = JSON.parse(readFileSync(resolve(here, "../tests/fixtures/coda_cases.json"), "utf8"));
  for (const item of fixture.cases) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.equal(result.syllables[0].ipa, item.phonemic_ipa, item.id);
    assert.equal(result.syllables[0].coda, item.coda, item.id);
  }
});

test("unregistered final consonant is not accepted as a coda", () => {
  const result = analyze("ກາສ");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.syllables.some((s) => s.surface === "ກາສ" && s.coda === "ສ"), false);
});


test("shared IPA-to-Ukrainian target fixtures match browser adapter", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const fixture = JSON.parse(readFileSync(resolve(here, "../tests/fixtures/target_output_cases.json"), "utf8"));
  assert.equal(fixture.schema_version, 1);
  for (const item of fixture.cases) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.equal(result.syllables[0].ipa, item.phonemic_ipa, item.id);
    assert.equal(result.syllables[0].ukrainian, item.ukrainian, item.id);
  }
});


test("unconsumed prefix before a preposed Lao vowel is not segmented away", () => {
  const surface = "xເເກ";
  const result = analyze(surface);
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.syllables.length, 1, "malformed token must remain one unresolved unit");
  assert.equal(result.syllables[0].surface, surface, "no source characters may be discarded");
  assert.ok(!result.syllables[0].ipa, "unresolved browser analysis must not expose IPA");
  assert.ok(!result.syllables[0].ukrainian, "unresolved browser analysis must not expose Ukrainian output");
  assert.ok(result.syllables[0].warnings.some((w) => w.includes("Непідтримуваний фрагмент перед початковим приголосним")));
  assert.equal(result.output, "⟦" + surface + "⟧");
});


test("DEL and C1 controls are rejected in browser input", () => {
  for (const control of ["\u007f", "\u0085", "\u009f"]) {
    const result = analyze("ກ" + control + "ຂ");
    assert.equal(result.status, "INVALID", "control " + control.codePointAt(0).toString(16));
    assert.equal(result.output, "");
    assert.ok(result.warnings.some((warning) => warning.includes("керівний символ")));
  }
});


test("shared Ukrainian target distinguishes aspiration, h, g, x and affricates", () => {
  assert.equal(analyze("ຂາ").output, "к'а");
  assert.equal(analyze("ຫາ").output, "га");
  assert.equal(CORRESPONDENCES["ɡ"], "ґ");
  assert.equal(CORRESPONDENCES["x"], "х");
  assert.equal(CORRESPONDENCES["t͡s"], "ц");
  assert.equal(CORRESPONDENCES["t͡ɕ"], "ч");
  assert.equal(CORRESPONDENCES["dʑ"], "дж");
  assert.equal(CORRESPONDENCES["d͡ʑ"], "дж");
  assert.equal(CORRESPONDENCES["d͡z"], "дз");
  assert.equal(CORRESPONDENCES["t͡ʃ"], "ч");
  assert.equal(CORRESPONDENCES["d͡ʒ"], "дж");
});

test("generated Ukrainian target map preserves the shch sequence and consonant distinctions", () => {
  assert.equal(CORRESPONDENCES.h, "г");
  assert.equal(CORRESPONDENCES["ɦ"], "г");
  assert.equal(CORRESPONDENCES["ɡ"], "ґ");
  assert.equal(CORRESPONDENCES.x, "х");
  assert.equal(CORRESPONDENCES["ʃ"], "ш");
  assert.equal(CORRESPONDENCES["ʃt͡ʃ"], "щ");
  assert.equal(CORRESPONDENCES["t͡ʃ"], "ч");
  assert.equal(CORRESPONDENCES["d͡ʒ"], "дж");
  assert.equal(CORRESPONDENCES["d͡z"], "дз");
});

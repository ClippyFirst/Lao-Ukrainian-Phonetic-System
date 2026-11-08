import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { analyze as analyzeDefault } from "./engine.js";

// Existing browser fixtures pin the explicit Vientiane baseline. Default
// profile selection is covered separately so profile changes stay deliberate.
function analyze(text, options = {}) {
  return analyzeDefault(text, { ipaProfile: options.ipaProfile ?? "vientiane" });
}

test("browser engine defaults to the hybrid deterministic profile", () => {
  const result = analyzeDefault("ດວງ");
  assert.equal(result.syllables[0].ipa, "duaːŋ");
  assert.ok(result.syllables[0].rules.includes("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT"));
});

test("hybrid renders Lao spans inside mixed-script text and preserves unsupported visible units", () => {
  const source = "«ຂາ» — українська 08:05 / 08:50 🙂";
  const result = analyzeDefault(source);
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "«к'а» — українська 08:05 / 08:50 🙂");
  assert.ok(result.syllables.some((unit) => unit.ipa === "kʰaː"));
  assert.ok(result.warnings.some((warning) => warning.includes("Непідтримуваний символ")));
});

test("hybrid mixed-script handling does not weaken frozen compatibility profiles", () => {
  const result = analyzeDefault("ກа", { ipaProfile: "vientiane" });
  assert.equal(result.status, "INVALID");
  assert.equal(result.output, "");
});
import { CORRESPONDENCES, SPECIAL_TONE_RULES } from "./data.js";

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
  const r = analyze("ດວາງ");
  assert.equal(r.syllables[0].ipa, "duːəŋ");
  assert.equal(r.output, "дуанг");
});


test("shared Lao labialized onset cluster fixture", () => {
  const fixturePath = resolve(dirname(fileURLToPath(import.meta.url)), "../tests/fixtures/onset_cluster_cases.json");
  const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));
  for (const item of fixture.clusters) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.equal(result.syllables[0].onsetForm, item.onset_form, item.id);
    assert.equal(result.syllables[0].ipa, item.ipa, item.id);
    assert.equal(result.syllables[0].ukrainian, null, item.id);
    assert.equal(result.syllables[0].status, "EVIDENCE LIMITED", item.id);
  }
  for (const item of fixture.constructed_cluster_controls) {
    const result = analyze(item.surface);
    assert.equal(result.syllables[0].onsetForm, item.onset_form, item.id);
    assert.equal(result.syllables[0].ipa, item.ipa, item.id);
    assert.equal(result.syllables[0].ukrainian, null, item.id);
  }
  for (const item of [...fixture.ambiguous, ...fixture.rounded_rejected]) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.equal(result.syllables[0].ipa, null, item.id);
    assert.equal(result.syllables[0].ukrainian, null, item.id);
    assert.ok(result.syllables[0].warnings.some((warning) => warning.startsWith(item.warning)), item.id);
  }
  for (const item of fixture.high_class_digraphs) {
    const result = analyze(item.surface);
    assert.equal(result.syllables[0].onsetForm, item.onset_form, item.id);
    assert.equal(result.syllables[0].class, item.onset_class, item.id);
    assert.equal(result.syllables[0].ipa, item.ipa, item.id);
  }
});

test("medial ອ is long ɔ", () => {
  const r = analyze("ຈອກ");
  assert.equal(r.syllables[0].ipa, "t͡ɕɔːk");
  assert.equal(r.output, "чок");
});

test("mai ti and mai catawa are not dropped", () => {
  assert.equal(analyze("ກ໊າ").syllables[0].tone, "high-falling");
  assert.equal(analyze("ກ໋າ").syllables[0].tone, "low-rising");
});

test("potential initial minor open-A tone is withheld in browser and segmental IPA retained", () => {
  const result = analyze("ຄະຄາ");
  const first = result.syllables[0];
  assert.equal(result.status, "PARTIAL");
  assert.ok(first.ipa);
  assert.ok(first.ukrainian);
  assert.equal(first.tone, null);
  assert.equal(first.toneContour, null);
  assert.equal(first.toneStatus, "ANALYSIS DEPENDENT");
  assert.ok(first.phoneticResult.uncertainty.includes("TONE-UNRESOLVED"));
  assert.ok(first.phoneticResult.provenance.includes("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"));
  assert.ok(first.phoneticResult.provenance.includes("TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED"));
  assert.ok(first.rules.includes("TONE-RULE:VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"));
});

test("minor-A candidate requires a major-weighted following syllable", () => {
  const result = analyze("ຄະຄະ");
  assert.equal(result.syllables.length, 2);
  assert.equal(result.syllables[0].tone, "high-mid");
  assert.equal(result.syllables[0].toneStatus, "ESTABLISHED");
});

test("shared Lao tone-mark storage-order fixture", () => {
  const fixturePath = resolve(dirname(fileURLToPath(import.meta.url)), "../tests/fixtures/tone_mark_order_cases.json");
  const fixture = JSON.parse(readFileSync(fixturePath, "utf8"));
  assert.equal(fixture.schema_version, 1);
  for (const item of fixture.valid) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.ok(result.syllables[0].ipa, item.id);
    assert.ok(!result.syllables[0].warnings.some((warning) => warning.startsWith("MALFORMED_TONE_MARK_")), item.id);
  }
  for (const item of fixture.invalid) {
    const result = analyze(item.surface);
    assert.equal(result.syllables.length, 1, item.id);
    assert.equal(result.syllables[0].ipa, null, item.id);
    assert.equal(result.syllables[0].ukrainian, null, item.id);
    assert.equal(result.syllables[0].tone, null, item.id);
    assert.equal(result.status, "PARTIAL", item.id);
    assert.ok(result.syllables[0].warnings.some((warning) => warning.startsWith("MALFORMED_TONE_MARK_")), item.id);
  }
});

test("short A2 syllable coda is validated before the next syllable", () => {
  const result = analyze("ກັນກາ");
  assert.equal(result.syllables.map((s) => s.surface).join("|"), "ກັນ|ກາ");
  assert.equal(result.syllables.every((s) => s.ipa), true);
});

test("tone marks are validated per syllable inside an unspaced word", () => {
  const result = analyze("ກ່າຂ່າ");
  assert.equal(result.syllables.map((s) => s.surface).join("|"), "ກ່າ|ຂ່າ");
  assert.equal(result.syllables.every((s) => s.ipa), true);
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

test("browser strips only a leading text-stream BOM", () => {
  const bom = String.fromCharCode(0xfeff);
  const clean = analyze("ກາ", { ipaProfile: "hybrid-deterministic" });
  const prefixed = analyze(bom + "ກາ", { ipaProfile: "hybrid-deterministic" });
  assert.deepEqual(prefixed.syllables.map((unit) => unit.surface), clean.syllables.map((unit) => unit.surface));
  assert.equal(analyze("ກ" + bom + "າ", { ipaProfile: "hybrid-deterministic" }).status, "INVALID");
});

test("zero-width space is accepted as a Lao syllable boundary", () => {
  const r = analyze("ກ\u200bຂ", { ipaProfile: "hybrid-deterministic" });
  assert.notEqual(r.status, "INVALID");
  assert.deepEqual(r.syllables.map((unit) => unit.surface), ["ກ", "ຂ"]);
  assert.ok(r.syllables.every((unit) => typeof unit.ukrainian === "string" && unit.ukrainian.length > 0));
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
  assert.equal(analyze("ຂາ").syllables[0].toneContour, "˨˦");
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
  assert.ok(!result.syllables[0].ukrainian, "frozen Vientiane profile still withholds unresolved output");
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

test("long Lao greeting sentence preserves every non-whitespace source unit", () => {
  const sentence = "ສະບາຍດີ! ຂ້ອຍຊື່ ນາລີ. ຂ້ອຍມາຈາກປະເທດລາວ ແລະມັກຮຽນພາສາໃໝ່.";
  const result = analyze(sentence);
  assert.notEqual(result.status, "INVALID");
  assert.ok(result.syllables.length > 0);
  assert.equal(result.syllables.map((unit) => unit.surface).join(""), sentence.replace(/\s/gu, ""));
  assert.ok(result.output.length > 0);
});


test("browser Ukrainian adaptation consumes a typed IPA result", () => {
  const result = analyze("ຂາ");
  const syllable = result.syllables[0];
  assert.equal(syllable.phoneticResult.phonemicIpa, "kʰaː");
  assert.deepEqual(syllable.phoneticResult.syllableBoundaries, [0, 2]);
  assert.deepEqual(syllable.phoneticResult.segments.map((segment) => segment.ipa), ["kʰ", "aː"]);
  assert.equal(syllable.phoneticResult.vowelLength, "long");
  assert.equal(syllable.phoneticResult.toneCategory, "low-rising");
  assert.equal(syllable.phoneticResult.status, "SUPPORTED");
  assert.equal(syllable.phoneticResult.broadSurfaceIpa, null);
  assert.equal(syllable.phoneticResult.externalIpa, null);
  assert.equal(syllable.ukrainian, "к'а");
});

test("browser hybrid adapter renders uncertain IPA without upgrading its status", () => {
  const result = analyze("ຣະ", { ipaProfile: "hybrid-deterministic" });
  const syllable = result.syllables[0];
  assert.equal(syllable.ipa, "ra");
  assert.equal(syllable.phoneticResult.status, "UNCERTAIN");
  assert.equal(syllable.ukrainian, "ра");
  assert.equal(syllable.status, "ANALYSIS DEPENDENT");
});

test("frozen Vientiane browser adapter withholds incomplete IPA rather than adapting a prefix", () => {
  const result = analyze("ກາລ");
  const syllable = result.syllables[0];
  assert.equal(syllable.phoneticResult.status, "UNSUPPORTED");
  assert.equal(syllable.ipa, null);
  assert.equal(syllable.ukrainian, null);
});


test("browser retains Ukrainian adaptation when only tone is unresolved", () => {
  const syllable = analyze("ຂັ່ບ").syllables[0];
  assert.equal(syllable.ipa, "kʰap");
  assert.equal(syllable.phoneticResult.status, "SUPPORTED");
  assert.equal(syllable.phoneticResult.toneCategory, null);
  assert.ok(syllable.phoneticResult.uncertainty.includes("TONE-UNRESOLVED"));
  assert.equal(syllable.ukrainian, "к'ап");
  assert.equal(syllable.status, "ANALYSIS DEPENDENT");
});

test("browser withholds tone for a supported potential initial minor open-A syllable", () => {
  const result = analyze("ຄະຄາ");
  const first = result.syllables[0];
  assert.equal(first.ipa, "kʰa");
  assert.equal(first.phoneticResult.status, "SUPPORTED");
  assert.equal(first.phoneticResult.toneCategory, null);
  assert.equal(first.toneContour, null);
  assert.equal(first.ukrainian, "к'а");
  assert.ok(first.rules.includes("TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED"));
});

test("browser does not apply potential minor selector across spaces or uncertain onsets", () => {
  const spaced = analyze("ຄະ ຄາ");
  assert.equal(spaced.syllables[0].tone, "high-mid");
  assert.ok(!spaced.syllables[0].rules.includes("TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED"));

  const uncertain = analyze("ຣະຄາ");
  assert.equal(uncertain.syllables[0].phoneticResult.status, "UNCERTAIN");
  assert.ok(!uncertain.syllables[0].rules.includes("TONE-POTENTIAL-MINOR-SYLLABLE-UNRESOLVED"));
});


test("browser IPA tokenization is independent of target sequence matching", () => {
  const syllable = analyze("ຂາ").syllables[0];
  assert.deepEqual(syllable.phoneticResult.segments.map((segment) => segment.ipa), ["kʰ", "aː"]);
  assert.equal(syllable.ukrainian, "к'а");
});

test("browser special-tone selector is generated from the canonical evidence registry", () => {
  assert.equal(SPECIAL_TONE_RULES.length, 1);
  assert.deepEqual(SPECIAL_TONE_RULES[0], [
    "VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED",
    "initial-open-short-a-unmarked-followed-by-major-weighted-syllable",
    "",
    "",
    "analysis-dependent",
    "Vientiane",
    "CLM-LAO-POTENTIAL-MINOR-OPEN-A"
  ]);
});


test("minor-syllable candidate requires a supported following onset", () => {
  const result = analyze("ຄະຣາ");
  assert.ok(result.syllables.length >= 1);
  assert.ok(!result.syllables[0].rules.includes("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"));
});

test("minor-syllable candidate excludes known palatal and velar nasal C0 onsets", () => {
  for (const word of ["ງະຄາ", "ຍະຄາ"]) {
    const result = analyze(word);
    assert.ok(result.syllables.length >= 1);
    assert.ok(!result.syllables[0].rules.includes("VNT-POTENTIAL-MINOR-OPEN-A-UNRESOLVED"));
  }
});


test("browser IPA adapter applies initial yodation and Lao /w/ mapping", () => {
  assert.equal(analyze("ຢາ").output, "я");
  assert.equal(analyze("ເຢ").output, "є");
  assert.equal(analyze("ຢີ").output, "ї");
  assert.equal(analyze("ຢູ").output, "ю");
  assert.equal(analyze("ເຂົາ").output, "к'ав");
});

test("browser IPA adapter preserves medial yod and does not collapse a diphthong", () => {
  assert.equal(analyze("ຂາຍ").output, "к'ай");
  assert.equal(analyze("ຢຽ").output, "йіа");
});


test("hybrid browser grapheme preview stays diagnostic beside typed placeholder output", () => {
  const syllable = analyze("ກາລ", { ipaProfile: "hybrid-deterministic" }).syllables[0];
  assert.equal(syllable.ipa, null);
  assert.equal(syllable.ukrainian, "ка?");
  assert.equal(syllable.phoneticResult.status, "PROVISIONAL");
  assert.equal(syllable.graphemePreview.ipaPreview, "kaː");
  assert.equal(syllable.graphemePreview.status, "PROVISIONAL");
  assert.deepEqual(syllable.graphemePreview.unresolvedGraphemes, ["ລ"]);
  assert.equal(syllable.graphemePreview.phoneticResult.status, "PROVISIONAL");
  assert.ok(syllable.graphemePreview.phoneticResult.segments.every((segment) => segment.certainty === "PROVISIONAL"));
});

test("browser grapheme preview never infers tone and withholds non-core Pali values", () => {
  const malformed = analyze("ຂ່້າ").syllables[0].graphemePreview;
  assert.equal(malformed.ipaPreview, "kʰaː");
  assert.ok(malformed.warnings.includes("TONE_NOT_INFERRED_BY_GRAPHEME_PREVIEW"));
  assert.equal(malformed.phoneticResult.toneCategory, null);
  const pali = analyze("ຆາ").syllables[0].graphemePreview;
  assert.equal(pali.ipaPreview, null);
  assert.equal(pali.status, "UNRESOLVED");
});


test("browser engine supports the deterministic MekongPhon-reference IPA profile", () => {
  const baseline = analyze("ດວງ");
  const compatible = analyze("ດວງ", { ipaProfile: "mekongphon-reference" });
  assert.equal(baseline.syllables[0].ipa, "duːəŋ");
  assert.equal(compatible.syllables[0].ipa, "duaːŋ");
  assert.equal(compatible.syllables[0].phoneticResult.status, "SUPPORTED");
  assert.equal(compatible.syllables[0].phoneticResult.phonemicIpa, "duaːŋ");
  assert.equal(compatible.syllables[0].ukrainian, "дуанг");
  assert.ok(compatible.syllables[0].rules.includes("IPA-PROFILE-MEKONGPHON-VOWEL:UO_LONG_ALT"));
  assert.ok(compatible.syllables[0].phoneticResult.provenance.includes("IPA-PROFILE-MEKONGPHON-VOWEL:UO_LONG_ALT"));
  assert.equal(compatible.syllables[0].tone, baseline.syllables[0].tone);
});

test("browser MekongPhon-reference profile keeps onset and uncertainty boundaries", () => {
  const baseline = analyze("ວັນ");
  const compatible = analyze("ວັນ", { ipaProfile: "mekongphon-reference" });
  assert.equal(baseline.syllables[0].ipa, "ʋan");
  assert.equal(compatible.syllables[0].ipa, "wan");
  assert.equal(compatible.syllables[0].ukrainian, "ван");
  assert.ok(compatible.syllables[0].rules.includes("IPA-PROFILE-MEKONGPHON-ONSET:ວ"));

  const rhotic = analyze("ຣະ", { ipaProfile: "mekongphon-reference" });
  assert.equal(rhotic.syllables[0].ipa, "ra");
  assert.equal(rhotic.syllables[0].phoneticResult.status, "UNCERTAIN");
  assert.equal(rhotic.syllables[0].ukrainian, null);
});

test("hybrid browser renders unresolved Lao units through a typed provisional placeholder", () => {
  const result = analyze("ກາລ", { ipaProfile: "hybrid-deterministic" });
  const syllable = result.syllables[0];
  assert.equal(result.status, "PARTIAL");
  assert.equal(syllable.ipa, null);
  assert.equal(syllable.ukrainian, "ка?");
  assert.equal(syllable.phoneticResult.status, "PROVISIONAL");
  assert.equal(syllable.phoneticResult.vowelLength, "long");
  assert.equal(syllable.phoneticResult.toneCategory, null);
  assert.equal(syllable.phoneticResult.segments.length, 3);
  assert.equal(syllable.phoneticResult.segments.at(-1).kind, "unknown");
  assert.ok(syllable.phoneticResult.segments.every((segment) => segment.certainty === "PROVISIONAL"));
});

test("hybrid renders uncertain phonetic readings without upgrading confidence", () => {
  const syllable = analyze("ຣະ", { ipaProfile: "hybrid-deterministic" }).syllables[0];
  assert.equal(syllable.ipa, "ra");
  assert.equal(syllable.ukrainian, "ра");
  assert.equal(syllable.phoneticResult.status, "UNCERTAIN");
  assert.equal(syllable.status, "ANALYSIS DEPENDENT");
});

test("hybrid browser renders every assigned Lao-block codepoint", () => {
  for (let codepoint = 0x0e80; codepoint < 0x0f00; codepoint += 1) {
    const character = String.fromCodePoint(codepoint);
    if (!/\p{Assigned}/u.test(character) || /\s/u.test(character)) continue;
    const result = analyzeDefault(character, { ipaProfile: "hybrid-deterministic" });
    assert.notEqual(result.status, "INVALID", "U+" + codepoint.toString(16));
    assert.ok(result.syllables.length > 0, "accepted Lao input must not disappear: U+" + codepoint.toString(16));
    for (const unit of result.syllables) {
      assert.notEqual(unit.ukrainian, null, "missing rendering for U+" + codepoint.toString(16));
    }
  }
});

test("browser engine rejects unknown deterministic IPA profiles", () => {
  assert.throws(() => analyze("ຂາ", { ipaProfile: "invented" }), RangeError);
});


test("browser hybrid deterministic profile composes Vientiane baseline with MekongPhon evidence rules", () => {
  const baseline = analyze("ດວງ");
  const reference = analyze("ດວງ", { ipaProfile: "mekongphon-reference" });
  const hybrid = analyze("ດວງ", { ipaProfile: "hybrid-deterministic" });
  assert.equal(hybrid.syllables[0].ipa, reference.syllables[0].ipa);
  assert.equal(hybrid.syllables[0].ukrainian, reference.syllables[0].ukrainian);
  assert.notEqual(hybrid.syllables[0].ipa, baseline.syllables[0].ipa);
  assert.ok(hybrid.syllables[0].rules.includes("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT"));
  assert.ok(hybrid.syllables[0].phoneticResult.provenance.includes("HYBRID-RULE:HYB-MPH-VOWEL-UO_LONG_ALT"));
  assert.equal(hybrid.syllables[0].tone, baseline.syllables[0].tone);
});

test("browser hybrid profile preserves Vientiane fallthrough and uncertain onset status", () => {
  const baseline = analyze("ຂາ");
  const hybrid = analyze("ຂາ", { ipaProfile: "hybrid-deterministic" });
  assert.equal(hybrid.syllables[0].ipa, baseline.syllables[0].ipa);
  assert.ok(!hybrid.syllables[0].rules.some((rule) => rule.startsWith("HYBRID-RULE:")));
  const rhotic = analyze("ຣະ", { ipaProfile: "hybrid-deterministic" });
  assert.equal(rhotic.syllables[0].ipa, "ra");
  assert.equal(rhotic.syllables[0].phoneticResult.status, "UNCERTAIN");
  assert.equal(rhotic.syllables[0].ukrainian, "ра");
});

test("browser engine rejects unknown hybrid rule profiles", () => {
  assert.throws(() => analyze("ຂາ", { ipaProfile: "not-a-profile" }), RangeError);
});

test("browser engine preserves corpus-observed punctuation as explicit passthrough", () => {
  const symbols = "&%–…#/" + String.fromCharCode(96) + "+•";
  const result = analyze("ຂາ" + symbols);
  const passthrough = result.syllables.filter((item) => item.passthrough);
  assert.equal(passthrough.map((item) => item.surface).join(""), symbols);
  assert.ok(passthrough.every((item) => item.ipa === "" && item.ukrainian === item.surface));
});

test("browser engine segments supported passthrough prefixes before Lao syllables", () => {
  const result = analyze("(ຂາ");
  assert.equal(result.syllables[0].passthrough, true);
  assert.equal(result.syllables[0].ukrainian, "(");
  assert.equal(result.syllables[1].ipa, "kʰaː");
  assert.equal(result.status, "OK");
});

test("browser engine preserves Lao native digits as non-IPA passthrough", () => {
  const result = analyze("ຂາ໑໒໓");
  const digits = result.syllables.filter((item) => item.surface.length === 1 && item.surface.codePointAt(0) >= 0x0ED0 && item.surface.codePointAt(0) <= 0x0ED9);
  assert.equal(digits.map((item) => item.surface).join(""), "໑໒໓");
  assert.ok(digits.every((item) => item.passthrough && item.ipa === "" && item.ukrainian === item.surface));
  assert.equal(result.syllables[0].ipa, "kʰaː");
});

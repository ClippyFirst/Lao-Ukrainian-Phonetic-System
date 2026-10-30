import test from "node:test";
import assert from "node:assert/strict";
import { analyzeRomanization } from "../web/romanization-syllable-engine.js";

test("romanization engine parses a syllable into onset, nucleus and coda", () => {
  const result = analyzeRomanization("kha");
  assert.equal(result.status, "OK");
  assert.equal(result.output, "к'а");
  assert.deepEqual(result.syllables.map(({ onset, nucleus, coda, ukrainian }) =>
    ({ onset, nucleus, coda, ukrainian })), [
      { onset: "kh", nucleus: "a", coda: "", ukrainian: "к'а" },
    ]);
});

test("aspiration digraphs are not mistaken for the independent Lao h consonant", () => {
  assert.equal(analyzeRomanization("ha kha tha pha").output, "га к'а т'а п'а");
});

test("the engine handles CLDR preposed-vowel syllable patterns in Ukrainian syllable order", () => {
  assert.equal(analyzeRomanization("éka aik").output, "ке кай");
});

test("the engine uses position-aware coda mappings", () => {
  assert.equal(analyzeRomanization("khat khap khang").output, "к'ат к'ап к'анг");
});

test("spaces and punctuation remain intact around analyzed syllables", () => {
  assert.equal(analyzeRomanization("kha, tha!").output, "к'а, т'а!");
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
  assert.equal(result.output, "к'а ⟦ໞ⟧");
});

test("h is not accepted as a Lao coda because the coda inventory excludes it", () => {
  const result = analyzeRomanization("ah");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦ah⟧");
});

test("the coda-vowel correspondence follows the documented BGN/PCGN context", () => {
  assert.equal(analyzeRomanization("kiv kav").output, "кіоу као");
});

test("the parser resolves CLDR preposed markers and postposed nuclei at syllable level", () => {
  const first = analyzeRomanization("ékhôa");
  const second = analyzeRomanization("niav");
  assert.equal(first.status, "OK");
  assert.equal(first.output, "к'ао");
  assert.deepEqual(first.syllables.map(({ onset, nucleus, coda }) => ({ onset, nucleus, coda })), [
    { onset: "kh", nucleus: "ôa", coda: "" },
  ]);
  assert.equal(second.status, "OK");
  assert.equal(second.output, "ніао");
  assert.deepEqual(second.syllables.map(({ onset, nucleus, coda }) => ({ onset, nucleus, coda })), [
    { onset: "n", nucleus: "ia", coda: "v" },
  ]);
  assert.equal(analyzeRomanization("ékhôa-niav").output, "к'ао-ніао");
});

test("concatenated multi-syllable romanization with competing parses is withheld", () => {
  const result = analyzeRomanization("ékhôaniav");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦ékhôaniav⟧");
  assert.equal(result.syllables[0].status, "AMBIGUOUS");
});

test("the parser withholds a vowel sequence whose CLDR transform lost a distinguishing character", () => {
  const result = analyzeRomanization("éku");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦éku⟧");
});


test("aspiration digraphs are interpreted through the source Lao consonant, not as literal h", () => {
  assert.equal(analyzeRomanization("kha", { sourceOnsets: ["ຂ"] }).output, "к'а");
  assert.equal(analyzeRomanization("kha", { sourceOnsets: ["ຄ"] }).output, "к'а");
  assert.equal(analyzeRomanization("tha", { sourceOnsets: ["ຖ"] }).output, "т'а");
  assert.equal(analyzeRomanization("tha", { sourceOnsets: ["ທ"] }).output, "т'а");
  assert.equal(analyzeRomanization("pha", { sourceOnsets: ["ຜ"] }).output, "п'а");
  assert.equal(analyzeRomanization("pha", { sourceOnsets: ["ພ"] }).output, "п'а");
});

test("a genuine Lao h onset remains г and is not confused with aspiration spelling", () => {
  assert.equal(analyzeRomanization("ha", { sourceOnsets: ["ຮ"] }).output, "га");
  assert.equal(analyzeRomanization("ha", { sourceOnsets: ["ຫ"] }).output, "га");
});

test("a romanization onset that conflicts with the original Lao grapheme is withheld", () => {
  const result = analyzeRomanization("kha", { sourceOnsets: ["ກ"] });
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦kha⟧");
  assert.match(result.warnings.join(" "), /не відповідає/iu);
});

test("the source-to-romanization crosswalk requires one-to-one syllable alignment", () => {
  const result = analyzeRomanization("khakha", { sourceOnsets: ["ຂ"] });
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦khakha⟧");
});


test("source graphemes correct romanization-specific consonant aliases", () => {
  assert.equal(analyzeRomanization("xa", { sourceOnsets: ["ຊ"] }).output, "са");
  assert.equal(analyzeRomanization("ra", { sourceOnsets: ["ຣ"] }).output, "ла");
});


test("a real k syllable followed by an h-onset syllable keeps both consonants", () => {
  const result = analyzeRomanization("kaha", { sourceOnsets: ["ກ", "ຮ"] });
  assert.equal(result.status, "OK");
  assert.equal(result.output, "кага");
  assert.deepEqual(result.syllables.map(({ onset, sourceOnset, ukrainian }) =>
    ({ onset, sourceOnset, ukrainian })), [
      { onset: "k", sourceOnset: "ກ", ukrainian: "ка" },
      { onset: "h", sourceOnset: "ຮ", ukrainian: "га" },
    ]);
});


test("atomic high-class nasal graphemes absent from the BGN onset table are withheld", () => {
  for (const sourceOnset of ["ໜ", "ໝ"]) {
    const result = analyzeRomanization("na", { sourceOnsets: [sourceOnset] });
    assert.equal(result.status, "PARTIAL");
    assert.equal(result.output, "⟦na⟧");
  }
});


test("an ambiguous earlier word does not shift later source-onset groups", () => {
  const result = analyzeRomanization("khakha kha", {
    sourceSyllableGroups: [[{ onset: "ຂ", coda: "" }, { onset: "ຂ", coda: "" }], [{ onset: "ຂ", coda: "" }]],
  });
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦khakha⟧ к'а");
  assert.equal(result.syllables[1].sourceOnset, "ຂ");
  assert.match(result.warnings.join(" "), /межі складів неоднозначні/iu);
});


test("the source coda grapheme must agree with the CLDR romanized coda", () => {
  const valid = analyzeRomanization("kad", {
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ດ" }]],
  });
  assert.equal(valid.status, "OK");
  assert.equal(valid.output, "кат");
  const mismatch = analyzeRomanization("kad", {
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ບ" }]],
  });
  assert.equal(mismatch.status, "PARTIAL");
  assert.equal(mismatch.output, "⟦kad⟧");
});

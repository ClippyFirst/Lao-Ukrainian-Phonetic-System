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
  const secondWithSource = analyzeRomanization("niav", {
    sourceSyllableGroups: [[{ onset: "ໜ", coda: "ວ" }]],
  });
  assert.equal(first.status, "OK");
  assert.equal(first.output, "к'ао");
  assert.deepEqual(first.syllables.map(({ onset, nucleus, coda }) => ({ onset, nucleus, coda })), [
    { onset: "kh", nucleus: "ôa", coda: "" },
  ]);
  assert.equal(second.status, "PARTIAL");
  assert.equal(second.output, "⟦niav⟧");
  assert.equal(secondWithSource.status, "OK");
  assert.equal(secondWithSource.output, "ніао");
  assert.deepEqual(secondWithSource.syllables.map(({ onset, nucleus, coda }) => ({ onset, nucleus, coda })), [
    { onset: "n", nucleus: "ia", coda: "v" },
  ]);
  const phraseWithSource = analyzeRomanization("ékhôa-niav", {
    sourceSyllableGroups: [
      [{ onset: "ຂ", coda: "", vowelId: "AW_LONG" }],
      [{ onset: "ໜ", coda: "ວ", vowelId: "IA_LONG" }],
    ],
  });
  assert.equal(phraseWithSource.status, "OK");
  assert.equal(phraseWithSource.output, "к'ао-ніао");
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
  assert.match(result.warnings.join(" "), /не відповіда/iu);
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


test("atomic high-class nasal ligatures are romanized as n and m without audible h", () => {
  const nasal = analyzeRomanization("na", { sourceOnsets: ["ໜ"] });
  const labial = analyzeRomanization("ma", { sourceOnsets: ["ໝ"] });
  assert.equal(nasal.status, "OK");
  assert.equal(nasal.output, "на");
  assert.equal(labial.status, "OK");
  assert.equal(labial.output, "ма");
});


test("source evidence resolves an ambiguous word without shifting later syllable groups", () => {
  const result = analyzeRomanization("khakha kha", {
    sourceSyllableGroups: [[{ onset: "ຂ", coda: "" }, { onset: "ຂ", coda: "" }], [{ onset: "ຂ", coda: "" }]],
  });
  assert.equal(result.status, "OK");
  assert.equal(result.output, "к'ак'а к'а");
  assert.equal(result.syllables[2].sourceOnset, "ຂ");
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


test("a rejected source syllable keeps its Lao and romanized graphemes visible in the trace", () => {
  const result = analyzeRomanization("kha", {
    sourceSyllableGroups: [[{ onset: "ກ", coda: "" }]],
  });
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦kha⟧");
  assert.equal(result.syllables[0].sourceOnset, "ກ");
  assert.equal(result.syllables[0].onset, "kh");
  assert.equal(result.syllables[0].sourceCoda, "");
  assert.equal(result.syllables[0].coda, "");
});


test("a romanized string with competing vowel-versus-coda parses is withheld without source evidence", () => {
  const result = analyzeRomanization("kam");
  assert.equal(result.status, "PARTIAL");
  assert.equal(result.output, "⟦kam⟧");
});


test("nullable optional crosswalk settings do not break standalone romanization", () => {
  assert.equal(analyzeRomanization("kha", null).output, "к'а");
});

test("atomic high-class nasal ligatures crosswalk through their underlying onset", () => {
  const nasal = analyzeRomanization("niav", {
    sourceSyllableGroups: [[{ onset: "ໜ", coda: "ວ", vowelId: "IA_LONG" }]],
  });
  const labial = analyzeRomanization("ma", {
    sourceSyllableGroups: [[{ onset: "ໝ", coda: "", vowelId: "AA" }]],
  });
  assert.equal(nasal.status, "OK");
  assert.equal(nasal.output, "ніао");
  assert.equal(nasal.syllables[0].sourceOnset, "ໜ");
  assert.equal(labial.status, "OK");
  assert.equal(labial.output, "ма");
});

test("source vowel identity must agree with the romanized nucleus", () => {
  const valid = analyzeRomanization("kha", {
    sourceSyllableGroups: [[{ onset: "ຂ", coda: "", vowelId: "AA" }]],
  });
  const mismatch = analyzeRomanization("kha", {
    sourceSyllableGroups: [[{ onset: "ຂ", coda: "", vowelId: "II" }]],
  });
  assert.equal(valid.status, "OK");
  assert.equal(valid.output, "к'а");
  assert.equal(mismatch.status, "PARTIAL");
  assert.equal(mismatch.output, "⟦kha⟧");
});


test("source vowel identity distinguishes A plus final m from the AM nucleus", () => {
  const aPlusM = analyzeRomanization("kam", {
    sourceSyllableGroups: [[{ onset: "ກ", vowelId: "AA", coda: "ມ" }]],
  });
  const amNucleus = analyzeRomanization("kam", {
    sourceSyllableGroups: [[{ onset: "ກ", vowelId: "AM", coda: "" }]],
  });
  assert.equal(aPlusM.status, "OK");
  assert.equal(amNucleus.status, "OK");
  assert.equal(aPlusM.output, "кам");
  assert.equal(amNucleus.output, "кам");
  assert.deepEqual(
    [aPlusM.syllables[0].sourceVowelId, aPlusM.syllables[0].nucleus, aPlusM.syllables[0].coda],
    ["AA", "a", "m"],
  );
  assert.deepEqual(
    [amNucleus.syllables[0].sourceVowelId, amNucleus.syllables[0].nucleus, amNucleus.syllables[0].coda],
    ["AM", "am", ""],
  );
});


test("standalone BGN/PCGN romanization can be converted without Lao-script side data", () => {
  const result = analyzeRomanization("Viangchan", { strictBoundaries: true });
  assert.equal(result.profile, "bgn-pcgn");
  assert.equal(result.status, "OK");
  assert.equal(result.output, "Віангчан");
});

test("ALA-LC macrons and palatal nasal spelling normalize through a bounded syllable adapter", () => {
  const result = analyzeRomanization("nyā", { profile: "ala-lc" });
  assert.equal(result.profile, "ala-lc");
  assert.equal(result.normalizedInput, "nya");
  assert.equal(result.status, "OK");
  assert.equal(result.output, "ньа");
});

test("ALA-LC short and long back vowels preserve the table's u versus ū distinction internally", () => {
  assert.equal(analyzeRomanization("ku", { profile: "ala-lc" }).output, "ки");
  assert.equal(analyzeRomanization("kū", { profile: "ala-lc" }).output, "ку");
  assert.equal(analyzeRomanization("kuʼ", { profile: "ala-lc" }).output, "ки");
  assert.equal(analyzeRomanization("kūʼ", { profile: "ala-lc" }).output, "ку");
});

test("ALA-LC final stops use the table's written final values", () => {
  const result = analyzeRomanization("kāt", { profile: "ala-lc" });
  assert.equal(result.status, "OK");
  assert.equal(result.output, "кат");
  assert.equal(analyzeRomanization("kās", { profile: "ala-lc" }).status, "PARTIAL");
});

test("auto profile detection recognizes ALA-LC diacritics but does not rewrite ordinary BGN text", () => {
  assert.equal(analyzeRomanization("nyā").profile, "ala-lc");
  assert.equal(analyzeRomanization("kha").profile, "bgn-pcgn");
});

test("unknown explicit romanization profiles fail closed instead of falling back to BGN/PCGN", () => {
  for (const profile of ["ala-lc-2012", "ALA-LC", ""]) {
    const result = analyzeRomanization("kha", { profile });
    assert.equal(result.profile, "unsupported", profile);
    assert.equal(result.status, "PARTIAL", profile);
    assert.equal(result.output, "⟦kha⟧", profile);
    assert.equal(result.syllables[0].status, "UNSUPPORTED_PROFILE", profile);
    assert.match(result.warnings[0], /невідомий профіль романізації/iu);
  }
  assert.equal(analyzeRomanization("kha", { profile: null }).profile, "bgn-pcgn");
});

test("title-case and all-caps romanization preserve initial capitalization", () => {
  assert.equal(analyzeRomanization("Viangchan", { strictBoundaries: true }).output, "Віангчан");
  assert.equal(analyzeRomanization("KHA", { strictBoundaries: true }).output, "К'А");
});

test("unsupported ALA-LC glottal notation remains visible instead of being guessed", () => {
  const result = analyzeRomanization("ʻīk", { profile: "ala-lc" });
  assert.equal(result.status, "PARTIAL");
  assert.match(result.output, /⟦ʻīk⟧/u);
});


test("strict BGN/PCGN mode requires a hyphen before a medial onsetless syllable", () => {
  const strict = analyzeRomanization("Viangchan", { strictBoundaries: true });
  const permissive = analyzeRomanization("Viangchan", { strictBoundaries: false });
  assert.equal(strict.status, "OK");
  assert.equal(strict.output, "Віангчан");
  assert.equal(permissive.status, "PARTIAL");
});

test("source-aware crosswalk keeps internal hyphens within one Lao word and aligns all syllables", () => {
  const result = analyzeRomanization("ka-é-kha", {
    profile: "bgn-pcgn",
    strictBoundaries: true,
    sourceSyllableGroups: [[
      { onset: "ກ", coda: "", vowelId: "A" },
      { onset: "ອ", coda: "", vowelId: "EE" },
      { onset: "ຂ", coda: "", vowelId: "A" },
    ]],
  });
  assert.equal(result.status, "OK");
  assert.equal(result.output, "ка-е-к'а");
  assert.equal(result.syllables.length, 3);
  assert.deepEqual(result.syllables.map((unit) => unit.surface), ["ka", "é", "kha"]);
});


test("ALA-LC short and long e spellings normalize to the same Ukrainian vowel class", () => {
  assert.equal(analyzeRomanization("ke", { profile: "ala-lc" }).output, "ке");
  assert.equal(analyzeRomanization("kē", { profile: "ala-lc" }).output, "ке");
});

test("ALA-LC parenthesized source finals are represented by their listed romanized value", () => {
  // LOC lists final r/l as (n): the romanized text therefore contains n,
  // not r/l. The romanization alone cannot recover which Lao final was used.
  assert.equal(analyzeRomanization("kan", { profile: "ala-lc" }).output, "кан");
  assert.equal(analyzeRomanization("kar", { profile: "ala-lc" }).status, "PARTIAL");
  assert.equal(analyzeRomanization("kal", { profile: "ala-lc" }).status, "PARTIAL");
});


test("ALA-LC short u is not rewritten as long ū", () => {
  assert.equal(analyzeRomanization("ku", { profile: "ala-lc" }).normalizedInput, "ku");
  assert.equal(analyzeRomanization("kū", { profile: "ala-lc" }).normalizedInput, "kou");
});

test("ALA-LC oe and ōe map to the documented vowel class", () => {
  assert.equal(analyzeRomanization("koe", { profile: "ala-lc" }).output, "ке");
  assert.equal(analyzeRomanization("kōe", { profile: "ala-lc" }).output, "ке");
});

test("ALA-LC ny is a palatal nasal onset and is not normalized to BGN gn", () => {
  assert.equal(analyzeRomanization("nyā", { profile: "ala-lc" }).normalizedInput, "nya");
  assert.equal(analyzeRomanization("nyā", { profile: "ala-lc" }).output, "ньа");
  assert.equal(analyzeRomanization("nya", { profile: "bgn-pcgn" }).status, "PARTIAL");
});

test("ALA-LC profile rejects BGN-only x and gn aliases", () => {
  assert.equal(analyzeRomanization("xa", { profile: "bgn-pcgn" }).output, "са");
  assert.equal(analyzeRomanization("xa", { profile: "ala-lc" }).status, "PARTIAL");
  assert.equal(analyzeRomanization("gna", { profile: "ala-lc" }).status, "PARTIAL");
});

test("ALA-LC final w is represented as o, with ambiguous ao forms withheld", () => {
  const ambiguous = analyzeRomanization("nāo", { profile: "ala-lc" });
  assert.equal(ambiguous.status, "PARTIAL");
  assert.equal(ambiguous.output, "⟦nāo⟧");
  const finalW = analyzeRomanization("kǣo", { profile: "ala-lc" });
  assert.equal(finalW.status, "OK");
  assert.equal(finalW.output, "кео");
});

test("ALA-LC final v and r/l spellings are not accepted as final consonants", () => {
  assert.equal(analyzeRomanization("kav", { profile: "ala-lc" }).status, "PARTIAL");
  assert.equal(analyzeRomanization("kar", { profile: "ala-lc" }).status, "PARTIAL");
});


test("ALA-LC official vat example is supported and ambiguous būak syllable division is withheld", () => {
  assert.equal(analyzeRomanization("vat", { profile: "ala-lc" }).output, "ват");
  const medialW = analyzeRomanization("būak", { profile: "ala-lc" });
  assert.equal(medialW.status, "PARTIAL");
  assert.equal(medialW.output, "⟦būak⟧");
});


test("auto profile detection recognizes ALA-LC modifier apostrophe and oe", () => {
  assert.equal(analyzeRomanization("kuʼ").profile, "ala-lc");
  assert.equal(analyzeRomanization("koe").profile, "ala-lc");
  assert.equal(analyzeRomanization("ku").profile, "bgn-pcgn");
});


test("ALA-LC 2012 vowel forms outside the implemented subset are withheld as whole words", () => {
  const unsupported = [
    "kiu", "kīu", "kīeo", "kieo", "kưa", "kư̄a",
    "kư", "kư̄", "kœ", "kœ̄", "kǫ", "kǭ",
  ];
  for (const input of unsupported) {
    const result = analyzeRomanization(input, { profile: "ala-lc" });
    assert.equal(result.status, "PARTIAL", input);
    assert.equal(result.output, `⟦${input}⟧`, input);
    assert.equal(result.syllables[0].status, "UNSUPPORTED_ALA_LC_VOWEL", input);
  }
});

test("ALA-LC medial w clusters and the special ūa example remain visibly partial", () => {
  for (const input of ["khwā", "khwǣng", "būak"]) {
    const result = analyzeRomanization(input, { profile: "ala-lc" });
    assert.equal(result.status, "PARTIAL", input);
    assert.equal(result.output, `⟦${input}⟧`, input);
  }
});

test("ALA-LC final consonants crosswalk with LOC final-position values", () => {
  const finalD = analyzeRomanization("kāt", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ດ", vowelId: "AA" }]],
  });
  const finalB = analyzeRomanization("kāp", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ບ", vowelId: "AA" }]],
  });
  assert.equal(finalD.status, "OK");
  assert.equal(finalD.output, "кат");
  assert.equal(finalB.status, "OK");
  assert.equal(finalB.output, "кап");
});

test("ALA-LC final ວ uses Note 4 o while BGN/CLDR keeps its v crosswalk", () => {
  const alaLc = analyzeRomanization("nāo", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ນ", coda: "ວ", vowelId: "AA" }]],
  });
  const bgnPcgn = analyzeRomanization("kav", {
    profile: "bgn-pcgn",
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ວ", vowelId: "A" }]],
  });
  assert.equal(alaLc.status, "OK");
  assert.equal(alaLc.output, "нао");
  assert.equal(alaLc.syllables[0].coda, "o");
  assert.equal(bgnPcgn.status, "OK");
  assert.equal(bgnPcgn.output, "као");
  assert.equal(bgnPcgn.syllables[0].coda, "v");
});

test("ALA-LC final ຍ closes the ai diphthong instead of becoming a consonant coda", () => {
  const result = analyzeRomanization("kāi", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ກ", coda: "ຍ", vowelId: "AI" }]],
  });
  assert.equal(result.status, "OK");
  assert.equal(result.output, "кай");
  assert.equal(result.syllables[0].nucleus, "ai");
  assert.equal(result.syllables[0].coda, "");
});

test("ALA-LC source-aware onset crosswalk uses s for ຊ and ny for ຍ", () => {
  const sibilant = analyzeRomanization("sa", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ຊ", coda: "", vowelId: "AA" }]],
  });
  const palatalNasal = analyzeRomanization("nyā", {
    profile: "ala-lc",
    sourceSyllableGroups: [[{ onset: "ຍ", coda: "", vowelId: "AA" }]],
  });
  assert.equal(sibilant.status, "OK");
  assert.equal(sibilant.output, "са");
  assert.equal(palatalNasal.status, "OK");
  assert.equal(palatalNasal.output, "ньа");
  assert.equal(palatalNasal.syllables[0].onset, "ny");
});

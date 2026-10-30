// Syllable-level adapter for the provisional CLDR Lao-Latin/UNGEGN string.
// This is an orthographic parsing policy, not an IPA or pronunciation engine.
// It analyzes onset + vowel nucleus + coda and deliberately withholds ambiguous parses.
const ONSETS = new Map([
  ["kh", "кг"], ["th", "тг"], ["ph", "пг"], ["ch", "ч"],
  ["ng", "нг"], ["gn", "нь"],
  ["k", "к"], ["s", "с"], ["x", "кс"], ["d", "д"], ["t", "т"],
  ["n", "н"], ["b", "б"], ["p", "п"], ["f", "ф"], ["m", "м"],
  ["y", "й"], ["r", "р"], ["l", "л"], ["v", "в"], ["h", "г"],
]);

const NUCLEI = new Map([
  ["oua", "уа"], ["ia", "іа"], ["ua", "уа"], ["ao", "ао"],
  ["eu", "е"], ["é", "е"], ["è", "е"], ["ô", "о"],
  ["ai", "ай"], ["am", "ам"], ["ou", "у"],
  ["a", "а"], ["i", "і"], ["u", "и"], ["o", "о"],
]);

// BGN/PCGN distinguishes several consonant spellings in syllable-final
// position. These position-sensitive values are taken from the CLDR source's
// cited EKI/UNGEGN table; the provisional CLDR transform itself does not
// implement all of these contextual distinctions.
const CODAS = new Map([
  ["ng", "нг"], ["gn", "й"], ["k", "к"], ["d", "т"], ["t", "т"],
  ["n", "н"], ["b", "п"], ["p", "п"], ["m", "м"],
  ["r", "р"], ["l", "л"], ["v", "о"], ["y", "й"], ["h", "г"],
]);

const PREPOSED_NUCLEI = new Set(["oua", "ia", "ua", "ao", "eu", "é", "è", "ô", "ai"]);
const SHORT_PREPOSED = new Set(["eu", "é", "è", "ô"]);
const SORTED_ONSETS = [...ONSETS.keys()].sort((a, b) => b.length - a.length);
const SORTED_NUCLEI = [...NUCLEI.keys()].sort((a, b) => b.length - a.length);
const SORTED_CODAS = [...CODAS.keys()].sort((a, b) => b.length - a.length);
const SEPARATORS = /^(\s+|[,.!?;:()[\]{}"“”]+|-+)$/u;

function codaTarget(coda, nucleus) {
  if (coda === "v") return nucleus === "i" ? "оу" : "о";
  return CODAS.get(coda);
}

function mapCase(value, source) {
  return source && source === source.toUpperCase() ? value.toUpperCase() : value;
}

function matchesAt(source, index, tokens) {
  return tokens.filter((token) => source.startsWith(token, index));
}

function candidatesAt(source, index) {
  const candidates = [];

  // Ordinary Latin order: onset + nucleus + optional coda.
  for (const onset of matchesAt(source, index, SORTED_ONSETS)) {
    const onsetEnd = index + onset.length;
    for (const nucleus of matchesAt(source, onsetEnd, SORTED_NUCLEI)) {
      const nucleusEnd = onsetEnd + nucleus.length;
      candidates.push({
        start: index, end: nucleusEnd, surface: source.slice(index, nucleusEnd),
        onset, nucleus, coda: "", order: "onset-first",
        ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus),
      });
      for (const coda of matchesAt(source, nucleusEnd, SORTED_CODAS)) {
        const end = nucleusEnd + coda.length;
        candidates.push({
          start: index, end, surface: source.slice(index, end),
          onset, nucleus, coda, order: "onset-first",
          ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus) + codaTarget(coda, nucleus),
        });
      }
    }
  }

  // CLDR keeps Lao preposed vowels before the consonant in Latin output.
  // Short preposed vowels may carry a trailing "a" from the literal transform;
  // that final a is a spelling artefact of the provisional transform, not a
  // second syllable nucleus in the BGN/PCGN syllable table.
  for (const nucleus of matchesAt(source, index, SORTED_NUCLEI)) {
    if (!PREPOSED_NUCLEI.has(nucleus)) continue;
    const onsetStart = index + nucleus.length;
    for (const onset of matchesAt(source, onsetStart, SORTED_ONSETS)) {
      let end = onsetStart + onset.length;
      if (SHORT_PREPOSED.has(nucleus) && source.startsWith("a", end)) end += 1;
      const base = {
        start: index, end, surface: source.slice(index, end),
        onset, nucleus, coda: "", order: "vowel-first",
        ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus),
      };
      candidates.push(base);
      for (const coda of matchesAt(source, end, SORTED_CODAS)) {
        const codaEnd = end + coda.length;
        candidates.push({
          ...base, end: codaEnd, surface: source.slice(index, codaEnd),
          coda, ukrainian: base.ukrainian + CODAS.get(coda),
        });
      }
    }
    // A vowel-only syllable is possible where the Lao onset is omitted by
    // romanization, but not when the next consonant can be the onset following
    // this preposed vowel (that is the normal CLDR order for Lao).
    const nextHasOnset = matchesAt(source, onsetStart, SORTED_ONSETS).length > 0;
    if (!nextHasOnset) {
      candidates.push({
        start: index, end: index + nucleus.length,
        surface: source.slice(index, index + nucleus.length),
        onset: "", nucleus, coda: "", order: "vowel-only",
        ukrainian: NUCLEI.get(nucleus),
      });
    }
  }

  // Vowel + coda, for onsetless syllables.
  for (const nucleus of matchesAt(source, index, SORTED_NUCLEI)) {
    if (PREPOSED_NUCLEI.has(nucleus)) continue;
    const nucleusEnd = index + nucleus.length;
    for (const coda of matchesAt(source, nucleusEnd, SORTED_CODAS)) {
      const end = nucleusEnd + coda.length;
      candidates.push({
        start: index, end, surface: source.slice(index, end),
        onset: "", nucleus, coda, order: "vowel-only",
        ukrainian: NUCLEI.get(nucleus) + CODAS.get(coda),
      });
    }
  }
  return candidates;
}

function parseWord(word) {
  const memo = new Map();
  function solve(index) {
    if (index === word.length) return { count: 1, path: [] };
    if (memo.has(index)) return memo.get(index);
    let count = 0;
    let path = null;
    for (const candidate of candidatesAt(word, index)) {
      const next = solve(candidate.end);
      if (!next.count) continue;
      if (count === 0 && next.count === 1) path = [candidate, ...next.path];
      else path = null;
      count = Math.min(2, count + next.count);
      if (count > 1) break;
    }
    const result = { count, path };
    memo.set(index, result);
    return result;
  }
  return solve(0);
}

function unresolved(surface, status = "UNRESOLVED") {
  return {
    surface, onset: "", nucleus: "", coda: "", ukrainian: "⟦" + surface + "⟧",
    status, warning: status === "AMBIGUOUS"
      ? "Межі складів неоднозначні; автоматичне складання результату утримано."
      : "Не вдалося розібрати фрагмент за підтримуваною структурою романізованого складу.",
  };
}

export function analyzeRomanization(input) {
  const source = String(input ?? "").normalize("NFC");
  const parts = source.split(/(\s+|[,.!?;:()[\]{}"“”]+|-+)/u).filter(Boolean);
  const syllables = [];
  let output = "";
  let partial = false;

  for (const part of parts) {
    if (SEPARATORS.test(part) || /^[0-9]+$/u.test(part)) {
      output += part;
      continue;
    }
    const parsed = parseWord(part);
    if (parsed.count === 1 && parsed.path) {
      const units = parsed.path.map((unit) => ({
        ...unit,
        ukrainian: mapCase(unit.ukrainian, unit.surface),
        status: "OK",
        warning: "",
      }));
      syllables.push(...units);
      output += units.map((unit) => unit.ukrainian).join("");
    } else {
      const item = unresolved(part, parsed.count > 1 ? "AMBIGUOUS" : "UNRESOLVED");
      syllables.push(item);
      output += item.ukrainian;
      partial = true;
    }
  }

  return {
    input: source,
    output,
    status: partial ? "PARTIAL" : "OK",
    syllables,
    warnings: syllables.filter((unit) => unit.warning).map((unit) => unit.warning),
    source: "CLDR Lao-Latin/UNGEGN → project syllable-level Ukrainian adapter",
  };
}

export function romanizationToUkrainian(input) {
  const result = analyzeRomanization(input);
  return { output: result.output, status: result.status, syllables: result.syllables, source: result.source, warnings: result.warnings };
}

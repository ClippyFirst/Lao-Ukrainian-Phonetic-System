// Syllable-level adapter for the provisional CLDR Lao-Latin/UNGEGN string.
// This is an orthographic parsing policy, not an IPA or pronunciation engine.
// It analyzes onset + vowel nucleus + coda and deliberately withholds ambiguous parses.
const ONSETS = new Map([
  ["kh", "к'"], ["th", "т'"], ["ph", "п'"], ["ch", "ч"],
  ["ng", "нг"], ["gn", "нь"],
  ["k", "к"], ["s", "с"], ["x", "с"], ["d", "д"], ["t", "т"],
  ["n", "н"], ["b", "б"], ["p", "п"], ["f", "ф"], ["m", "м"],
  ["y", "й"], ["r", "л"], ["l", "л"], ["v", "в"], ["h", "г"],
]);

const NUCLEI = new Map([
  ["oua", "уа"], ["ia", "іа"], ["ua", "уа"], ["ao", "ао"], ["ôa", "ао"],
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
  ["r", "л"], ["l", "л"], ["v", "о"], ["y", "й"],
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

function longestMatchesAt(source, index, tokens) {
  const matches = matchesAt(source, index, tokens);
  if (!matches.length) return [];
  const longest = matches[0].length;
  return matches.filter((token) => token.length === longest);
}

function candidatesAt(source, index) {
  const candidates = [];

  // Ordinary Latin order: onset + nucleus + optional coda.
  for (const onset of longestMatchesAt(source, index, SORTED_ONSETS)) {
    const onsetEnd = index + onset.length;
    for (const nucleus of longestMatchesAt(source, onsetEnd, SORTED_NUCLEI)) {
      const nucleusEnd = onsetEnd + nucleus.length;
      candidates.push({
        start: index, end: nucleusEnd, surface: source.slice(index, nucleusEnd),
        onset, nucleus, coda: "", order: "onset-first",
        ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus),
      });
      for (const coda of longestMatchesAt(source, nucleusEnd, SORTED_CODAS)) {
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
  for (const nucleus of longestMatchesAt(source, index, SORTED_NUCLEI)) {
    if (!PREPOSED_NUCLEI.has(nucleus)) continue;
    const onsetStart = index + nucleus.length;
    for (const onset of longestMatchesAt(source, onsetStart, SORTED_ONSETS)) {
      let outputNucleus = nucleus;
      let end = onsetStart + onset.length;
      if (["é", "è", "ô"].includes(nucleus)) {
        const followingNucleus = longestMatchesAt(source, end, SORTED_NUCLEI)[0] || "";
        if (followingNucleus && followingNucleus !== "a") {
          // In the provisional literal CLDR transform, the preposed vowel
          // marker remains visible before the onset while the actual nucleus
          // is also emitted after it (e.g. ékhôa for the EKI nucleus ao).
          // A bare u after this marker is ambiguous because the transform
          // deletes Lao ອ; withhold it instead of inventing the missing diphthong.
          if (followingNucleus === "u") continue;
          outputNucleus = followingNucleus;
          end += followingNucleus.length;
        } else {
          outputNucleus = nucleus;
          if (followingNucleus === "a") end += 1;
        }
      }
      const base = {
        start: index, end, surface: source.slice(index, end),
        onset, nucleus: outputNucleus, coda: "", order: "vowel-first",
        ukrainian: ONSETS.get(onset) + NUCLEI.get(outputNucleus),
      };
      candidates.push(base);
      for (const coda of longestMatchesAt(source, end, SORTED_CODAS)) {
        const codaEnd = end + coda.length;
        candidates.push({
          ...base, end: codaEnd, surface: source.slice(index, codaEnd),
          coda, ukrainian: base.ukrainian + codaTarget(coda, outputNucleus),
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
    for (const coda of longestMatchesAt(source, nucleusEnd, SORTED_CODAS)) {
      const end = nucleusEnd + coda.length;
      candidates.push({
        start: index, end, surface: source.slice(index, end),
        onset: "", nucleus, coda, order: "vowel-only",
        ukrainian: NUCLEI.get(nucleus) + codaTarget(coda, nucleus),
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

const LAO_ONSET_TO_ROMANIZATION = new Map([
  ["ກ", "k"], ["ຂ", "kh"], ["ຄ", "kh"], ["ງ", "ng"], ["ຈ", "ch"],
  ["ສ", "s"], ["ຊ", "x"], ["ຍ", "gn"], ["ດ", "d"], ["ຕ", "t"],
  ["ຖ", "th"], ["ທ", "th"], ["ນ", "n"], ["ບ", "b"], ["ປ", "p"],
  ["ຜ", "ph"], ["ຝ", "f"], ["ພ", "ph"], ["ຟ", "f"], ["ມ", "m"],
  ["ຢ", "y"], ["ຣ", "r"], ["ລ", "l"], ["ວ", "v"], ["ຫ", "h"],
  ["ຮ", "h"], ["ອ", ""],
]);

const LAO_ONSET_TARGETS = new Map([
  ["ກ", "к"], ["ຂ", "к'"], ["ຄ", "к'"], ["ງ", "нг"], ["ຈ", "ч"],
  ["ສ", "с"], ["ຊ", "с"], ["ຍ", "нь"], ["ດ", "д"], ["ຕ", "т"],
  ["ຖ", "т'"], ["ທ", "т'"], ["ນ", "н"], ["ບ", "б"], ["ປ", "п"],
  ["ຜ", "п'"], ["ຝ", "ф"], ["ພ", "п'"], ["ຟ", "ф"], ["ມ", "м"],
  ["ຢ", "й"], ["ຣ", "л"], ["ລ", "л"], ["ວ", "в"], ["ຫ", "г"],
  ["ຮ", "г"], ["ອ", ""],
]);

function crosswalkUnit(unit, sourceOnset) {
  const expectedRomanization = LAO_ONSET_TO_ROMANIZATION.get(sourceOnset);
  if (expectedRomanization === undefined || expectedRomanization !== unit.onset) return null;
  const onsetTarget = LAO_ONSET_TARGETS.get(sourceOnset);
  return {
    ...unit,
    ukrainian: onsetTarget + NUCLEI.get(unit.nucleus) +
      (unit.coda ? codaTarget(unit.coda, unit.nucleus) : ""),
    sourceOnset,
    crosswalk: "LAO_GRAPHEME↔BGN_ROMANIZATION↔UKRAINIAN",
  };
}

export function analyzeRomanization(input, options = {}) {
  const source = String(input ?? "").normalize("NFC");
  const parts = source.split(/(\s+|[,.!?;:()[\]{}"“”]+|-+)/u).filter(Boolean);
  const syllables = [];
  let output = "";
  let partial = false;
  const sourceOnsetGroups = Array.isArray(options.sourceOnsetGroups) ? options.sourceOnsetGroups : null;
  const sourceOnsets = sourceOnsetGroups ? null
    : Array.isArray(options.sourceOnsets) ? options.sourceOnsets : null;
  let sourceIndex = 0;
  let sourceGroupIndex = 0;

  for (const part of parts) {
    if (SEPARATORS.test(part) || /^[0-9]+$/u.test(part)) {
      output += part;
      continue;
    }
    const sourceGroup = sourceOnsetGroups ? (sourceOnsetGroups[sourceGroupIndex++] || []) : null;
    const parsed = parseWord(part);
    if (parsed.count === 1 && parsed.path) {
      const sourceSlice = sourceOnsetGroups ? sourceGroup : sourceOnsets
        ? sourceOnsets.slice(sourceIndex, sourceIndex + parsed.path.length)
        : null;
      const hasCrosswalk = Boolean(sourceOnsetGroups || sourceOnsets);
      const aligned = !hasCrosswalk || sourceSlice.length === parsed.path.length;
      const crossed = aligned && hasCrosswalk
        ? parsed.path.map((unit, index) => crosswalkUnit(unit, sourceSlice[index]))
        : parsed.path;
      const validCrosswalk = aligned && crossed.every(Boolean);
      if (validCrosswalk) {
        const units = crossed.map((unit) => ({
          ...unit,
          ukrainian: mapCase(unit.ukrainian, unit.surface),
          status: "OK",
          warning: "",
        }));
        syllables.push(...units);
        output += units.map((unit) => unit.ukrainian).join("");
        if (sourceOnsets) sourceIndex += parsed.path.length;
      } else {
        const item = unresolved(part, "UNRESOLVED");
        item.warning = aligned
          ? "Романізований початковий елемент не відповідає лаоській графемі; український результат утримано."
          : "Кількість розібраних романізованих складів не збігається з кількістю лаоських складових одиниць; звірку утримано.";
        syllables.push(item);
        output += item.ukrainian;
        partial = true;
        if (sourceOnsets) sourceIndex += sourceSlice.length;
      }
    } else {
      const item = unresolved(part, parsed.count > 1 ? "AMBIGUOUS" : "UNRESOLVED");
      syllables.push(item);
      output += item.ukrainian;
      partial = true;
    }
  }

  const warnings = syllables.filter((unit) => unit.warning).map((unit) => unit.warning);
  if (sourceOnsets && sourceIndex !== sourceOnsets.length) {
    partial = true;
    warnings.push("Кількість лаоських початкових графем і романізованих складів не збігається; повну звірку не виконано.");
  }
  if (sourceOnsetGroups && sourceGroupIndex !== sourceOnsetGroups.length) {
    partial = true;
    warnings.push("Кількість лаоських фрагментів і романізованих фрагментів не збігається; повну звірку не виконано.");
  }

  return {
    input: source,
    output,
    status: partial ? "PARTIAL" : "OK",
    syllables,
    warnings,
    source: "CLDR Lao-Latin (provisional; BGN/PCGN 1966 basis) → Lao-grapheme crosswalk → Ukrainian syllable adapter",
  };
}

export function romanizationToUkrainian(input, options = {}) {
  const result = analyzeRomanization(input, options);
  return { output: result.output, status: result.status, syllables: result.syllables, source: result.source, warnings: result.warnings };
}

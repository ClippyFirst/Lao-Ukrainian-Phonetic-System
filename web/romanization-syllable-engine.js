// Syllable-level adapter for the provisional CLDR Lao-Latin transform with a BGN/PCGN-aligned subset.
// This is an orthographic parsing policy, not an IPA or pronunciation engine.
// It analyzes onset + vowel nucleus + coda and deliberately withholds ambiguous parses.
const ONSETS = new Map([
  ["kh", "к'"], ["th", "т'"], ["ph", "п'"], ["ch", "ч"],
  ["ng", "нг"], ["gn", "нь"], ["ny", "нь"],
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
  ["ng", "нг"], ["gn", "й"], ["k", "к"], ["d", "т"], ["t", "т"], ["s", "т"],
  ["n", "н"], ["b", "п"], ["p", "п"], ["m", "м"],
  ["r", "л"], ["l", "л"], ["v", "о"], ["y", "й"], ["o", "о"],
]);

const PREPOSED_NUCLEI = new Set(["oua", "ia", "ua", "ao", "eu", "é", "è", "ô", "ai"]);
const SHORT_PREPOSED = new Set(["eu", "é", "è", "ô"]);
const SORTED_ONSETS = [...ONSETS.keys()].sort((a, b) => b.length - a.length);
const SORTED_NUCLEI = [...NUCLEI.keys()].sort((a, b) => b.length - a.length);
const SORTED_CODAS = [...CODAS.keys()].sort((a, b) => b.length - a.length);
const SEPARATORS = /^(\s+|[,.!?;:()[\]{}"“”]+|-+)$/u;

function codaTarget(coda, nucleus, profile = "bgn-pcgn") {
  if (coda === "v") return nucleus === "i" ? "оу" : "о";
  return CODAS.get(coda);
}

function mapCase(value, source) {
  if (!source) return value;
  if (source === source.toUpperCase()) return value.toUpperCase();
  if (source[0] && source[0] === source[0].toUpperCase() && source[0] !== source[0].toLowerCase()) {
    return value[0].toUpperCase() + value.slice(1);
  }
  return value;
}

// Exact ALA-LC 2012 vowel spellings, normalized only where the shared
// syllable parser has an equivalent internal nucleus. Quantity is intentionally
// collapsed in the Ukrainian output; the original input remains available.
const ALA_LC_REPLACEMENTS = new Map([
  ["ūa", "oua"], ["īa", "ia"], ["āi", "ai"], ["ōe", "eu"], ["oe", "eu"],
  ["ǣ", "è"], ["æ", "è"], ["ūʼ", "ou"], ["uʼ", "u"], ["e", "é"],
  ["ū", "ou"], ["ā", "a"], ["ī", "i"], ["ē", "é"], ["ō", "ô"],
]);

function replacePreservingCase(token, replacement) {
  if (token === token.toUpperCase()) return replacement.toUpperCase();
  if (token[0] === token[0].toUpperCase() && token[0] !== token[0].toLowerCase()) {
    return replacement[0].toUpperCase() + replacement.slice(1);
  }
  return replacement;
}

// LOC ALA-LC 2012 Note 4 lists additional vowel forms that the shared
// parser does not yet model (including iu/īu and īeo). Without an explicit
// syllable boundary, the generic parser could split these sequences into
// multiple ordinary nuclei and return a misleading OK result. Keep the entire
// word PARTIAL until a source-reviewed target adapter exists.
const ALA_LC_UNSUPPORTED_SEQUENCES = [
  "ư̄a", "ưa", "īeo", "ieo", "īu", "iu", "œ̄", "œ", "ǭ", "ǫ", "ư̄", "ư",
];

function hasUnsupportedAlaLcSequence(rawPart, normalizedPart) {
  return ALA_LC_UNSUPPORTED_SEQUENCES.some((token) =>
    rawPart.toLowerCase().includes(token) || normalizedPart.toLowerCase().includes(token)
  );
}

function normalizeAlaLc(input) {
  const source = input.toLowerCase();
  const tokens = [...ALA_LC_REPLACEMENTS.keys()].sort((a, b) => b.length - a.length);
  let normalized = "";
  for (let index = 0; index < source.length;) {
    const token = tokens.find((candidate) => source.startsWith(candidate, index));
    if (token) {
      normalized += ALA_LC_REPLACEMENTS.get(token);
      index += token.length;
    } else {
      normalized += source[index];
      index += 1;
    }
  }
  return normalized;
}

function detectRomanizationProfile(input, requested = "auto") {
  if (requested === "bgn-pcgn" || requested === "ala-lc") return requested;
  if (requested !== "auto") return null;
  return /[āīūēōæǣʼʻ]/iu.test(input) || /oe/iu.test(input) || /ny(?=[aeiouāīūēōæǣʼ])/iu.test(input) ? "ala-lc" : "bgn-pcgn";
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

function candidatesAt(source, index, profile = "bgn-pcgn", strictBoundaries = false, explicitBoundary = false) {
  const candidates = [];
  const onsetTokens = profile === "ala-lc"
    ? [...ONSETS.keys()].filter((token) => token !== "x" && token !== "gn").sort((a, b) => b.length - a.length)
    : SORTED_ONSETS.filter((token) => token !== "ny");
  // ALA-LC finals are written with their final-position values: k, ng, t,
  // p, n, m; final ວ is represented by o after the vowel (Note 4).
  const codaTokens = profile === "ala-lc"
    ? ["ng", "k", "t", "p", "n", "m", "o"]
    : SORTED_CODAS.filter((token) => token !== "s" && token !== "w" && token !== "o");

  // Ordinary Latin order: onset + nucleus + optional coda.
  for (const onset of longestMatchesAt(source, index, onsetTokens)) {
    const onsetEnd = index + onset.length;
    for (const nucleus of matchesAt(source, onsetEnd, SORTED_NUCLEI)) {
      const nucleusEnd = onsetEnd + nucleus.length;
      candidates.push({
        start: index, end: nucleusEnd, surface: source.slice(index, nucleusEnd),
        onset, nucleus, coda: "", order: "onset-first",
        ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus),
      });
      for (const coda of matchesAt(source, nucleusEnd, codaTokens)) {
        const end = nucleusEnd + coda.length;
        candidates.push({
          start: index, end, surface: source.slice(index, end),
          onset, nucleus, coda, order: "onset-first",
          ukrainian: ONSETS.get(onset) + NUCLEI.get(nucleus) + codaTarget(coda, nucleus, profile),
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
    for (const onset of longestMatchesAt(source, onsetStart, onsetTokens)) {
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
      for (const coda of longestMatchesAt(source, end, codaTokens)) {
        const codaEnd = end + coda.length;
        candidates.push({
          ...base, end: codaEnd, surface: source.slice(index, codaEnd),
          coda, ukrainian: base.ukrainian + codaTarget(coda, outputNucleus, profile),
        });
      }
    }
    // A vowel-only syllable is possible where the Lao onset is omitted by
    // romanization, but not when the next consonant can be the onset following
    // this preposed vowel (that is the normal CLDR order for Lao).
    const nextHasOnset = matchesAt(source, onsetStart, onsetTokens).length > 0;
    if ((!strictBoundaries || index === 0 || explicitBoundary) && !nextHasOnset) {
      candidates.push({
        start: index, end: index + nucleus.length,
        surface: source.slice(index, index + nucleus.length),
        onset: "", nucleus, coda: "", order: "vowel-only",
        ukrainian: NUCLEI.get(nucleus),
      });
    }
  }

  // Vowel + coda, for onsetless syllables. In strict direct-input mode, an
  // unmarked onsetless syllable is allowed only at the beginning of a
  // hyphen-delimited word; BGN/PCGN note 4 requires a hyphen for medial ອ.
  if (!strictBoundaries || index === 0 || explicitBoundary) {
    for (const nucleus of matchesAt(source, index, SORTED_NUCLEI)) {
      if (PREPOSED_NUCLEI.has(nucleus)) continue;
      const nucleusEnd = index + nucleus.length;
      for (const coda of longestMatchesAt(source, nucleusEnd, codaTokens)) {
        const end = nucleusEnd + coda.length;
        candidates.push({
          start: index, end, surface: source.slice(index, end),
          onset: "", nucleus, coda, order: "vowel-only",
          ukrainian: NUCLEI.get(nucleus) + codaTarget(coda, nucleus, profile),
        });
      }
    }
  }
  return candidates;
}

function parseWord(word, sourceGroup = null, profile = "bgn-pcgn", strictBoundaries = false) {
  const memo = new Map();
  function solve(index, sourceIndex) {
    if (index === word.length) {
      if (sourceGroup && sourceIndex !== sourceGroup.length) return { count: 0, path: null };
      return { count: 1, path: [] };
    }
    const key = sourceGroup ? `${index}:${sourceIndex}` : String(index);
    if (memo.has(key)) return memo.get(key);

    // In source-aware Lao → romanization crosswalking, a hyphen is an
    // internal syllable boundary (not a new whitespace-delimited source word).
    // Keep it in the output path without consuming a Lao syllable.
    if (sourceGroup && word[index] === "-") {
      const next = solve(index + 1, sourceIndex);
      const result = next.count
        ? { count: next.count, path: next.path
          ? [{ kind: "separator", surface: "-", ukrainian: "-" }, ...next.path]
          : null }
        : next;
      memo.set(key, result);
      return result;
    }

    let count = 0;
    let path = null;
    const explicitBoundary = index > 0 && word[index - 1] === "-";
    for (const candidate of candidatesAt(word, index, profile, strictBoundaries, explicitBoundary)) {
      if (sourceGroup && !crosswalkUnit(candidate, sourceGroup[sourceIndex], profile)) continue;
      const next = solve(candidate.end, sourceIndex + 1);
      if (!next.count) continue;
      if (count === 0 && next.count === 1) path = [candidate, ...next.path];
      else path = null;
      count = Math.min(2, count + next.count);
      if (count > 1) break;
    }
    const result = { count, path };
    memo.set(key, result);
    return result;
  }
  return solve(0, 0);
}
function unresolved(surface, status = "UNRESOLVED") {
  return {
    surface, onset: "", nucleus: "", coda: "", ukrainian: "⟦" + surface + "⟧",
    status, warning: status === "AMBIGUOUS"
      ? "Межі складів неоднозначні; автоматичне складання результату утримано."
      : "Не вдалося розібрати фрагмент за підтримуваною структурою романізованого складу.",
  };
}

// ALA-LC initial spellings differ from BGN/CLDR for ຊ (s) and ຍ (ny).
// Keep this source crosswalk separate from the CLDR-derived inventory.
const LAO_ONSET_TO_ALA_LC = new Map([
  ["ກ", { romanization: "k", ukrainian: "к" }],
  ["ຂ", { romanization: "kh", ukrainian: "к'" }],
  ["ຄ", { romanization: "kh", ukrainian: "к'" }],
  ["ງ", { romanization: "ng", ukrainian: "нг" }],
  ["ຈ", { romanization: "ch", ukrainian: "ч" }],
  ["ສ", { romanization: "s", ukrainian: "с" }],
  ["ຊ", { romanization: "s", ukrainian: "с" }],
  ["ຍ", { romanization: "ny", ukrainian: "нь" }],
  ["ດ", { romanization: "d", ukrainian: "д" }],
  ["ຕ", { romanization: "t", ukrainian: "т" }],
  ["ຖ", { romanization: "th", ukrainian: "т'" }],
  ["ທ", { romanization: "th", ukrainian: "т'" }],
  ["ນ", { romanization: "n", ukrainian: "н" }],
  ["ບ", { romanization: "b", ukrainian: "б" }],
  ["ປ", { romanization: "p", ukrainian: "п" }],
  ["ຜ", { romanization: "ph", ukrainian: "п'" }],
  ["ຝ", { romanization: "f", ukrainian: "ф" }],
  ["ພ", { romanization: "ph", ukrainian: "п'" }],
  ["ຟ", { romanization: "f", ukrainian: "ф" }],
  ["ມ", { romanization: "m", ukrainian: "м" }],
  ["ຢ", { romanization: "y", ukrainian: "й" }],
  ["ຣ", { romanization: "r", ukrainian: "л" }],
  ["ລ", { romanization: "l", ukrainian: "л" }],
  ["ວ", { romanization: "v", ukrainian: "в" }],
  ["ຫ", { romanization: "h", ukrainian: "г" }],
  ["ຮ", { romanization: "h", ukrainian: "г" }],
  ["ໜ", { romanization: "n", ukrainian: "н" }],
  ["ໝ", { romanization: "m", ukrainian: "м" }],
]);
const LAO_ONSET_CROSSWALK = new Map([
  ["ກ", { romanization: "k", ukrainian: "к" }],
  ["ຂ", { romanization: "kh", ukrainian: "к'" }],
  ["ຄ", { romanization: "kh", ukrainian: "к'" }],
  ["ງ", { romanization: "ng", ukrainian: "нг" }],
  ["ຈ", { romanization: "ch", ukrainian: "ч" }],
  ["ສ", { romanization: "s", ukrainian: "с" }],
  ["ຊ", { romanization: "x", ukrainian: "с" }],
  ["ຍ", { romanization: "gn", ukrainian: "нь" }],
  ["ດ", { romanization: "d", ukrainian: "д" }],
  ["ຕ", { romanization: "t", ukrainian: "т" }],
  ["ຖ", { romanization: "th", ukrainian: "т'" }],
  ["ທ", { romanization: "th", ukrainian: "т'" }],
  ["ນ", { romanization: "n", ukrainian: "н" }],
  ["ບ", { romanization: "b", ukrainian: "б" }],
  ["ປ", { romanization: "p", ukrainian: "п" }],
  ["ຜ", { romanization: "ph", ukrainian: "п'" }],
  ["ຝ", { romanization: "f", ukrainian: "ф" }],
  ["ພ", { romanization: "ph", ukrainian: "п'" }],
  ["ຟ", { romanization: "f", ukrainian: "ф" }],
  ["ມ", { romanization: "m", ukrainian: "м" }],
  ["ຢ", { romanization: "y", ukrainian: "й" }],
  ["ຣ", { romanization: "r", ukrainian: "л" }],
  ["ລ", { romanization: "l", ukrainian: "л" }],
  ["ວ", { romanization: "v", ukrainian: "в" }],
  ["ຫ", { romanization: "h", ukrainian: "г" }],
  ["ຮ", { romanization: "h", ukrainian: "г" }],
  // BGN/PCGN silent-hoa note (numbering differs across copies): ໜ/ໝ are ligature forms of silent ຫ + ນ/ມ.
  // The silent high-class marker is not romanized; the nasal is.
  ["ໜ", { romanization: "n", ukrainian: "н" }],
  ["ໝ", { romanization: "m", ukrainian: "м" }],
  ["ອ", { romanization: "", ukrainian: "" }],
]);
const LAO_CODA_TO_CLDR = new Map([
  ["ກ", "k"], ["ງ", "ng"], ["ດ", "d"], ["ບ", "b"], ["ນ", "n"],
  ["ມ", "m"], ["ຍ", "gn"], ["ວ", "v"],
]);
// ALA-LC 2012 uses final-position values that differ from BGN/CLDR.
// LOC Notes 2 and 4 are handled separately below.
const LAO_CODA_TO_ALA_LC = new Map([
  ["ກ", "k"], ["ຂ", "k"], ["ຄ", "k"], ["ງ", "ng"],
  ["ຈ", "t"], ["ສ", "t"], ["ຊ", "t"], ["ດ", "t"],
  ["ຕ", "t"], ["ຖ", "t"], ["ທ", "t"], ["ນ", "n"],
  ["ບ", "p"], ["ປ", "p"], ["ຜ", "p"], ["ຝ", "p"],
  ["ພ", "p"], ["ຟ", "p"], ["ມ", "m"], ["ຣ", "n"],
  ["ລ", "n"], ["ວ", "o"],
]);

// The source vowel parser retains distinctions that the romanization can
// collapse (notably length). These aliases validate the represented nucleus;
// unsupported/lost source vowels are deliberately withheld.
const LAO_VOWEL_TO_CLDR = new Map([
  ["A", ["a"]], ["A2", ["a"]], ["AA", ["a"]],
  ["I", ["i"]], ["II", ["i"]],
  ["Y", ["u"]], ["YY", ["u"]],
  ["U", ["ou"]], ["UU", ["ou"]],
  ["E", ["é"]], ["EE", ["é"]],
  ["AE", ["è"]], ["AEE", ["è"]],
  ["O", ["ô"]], ["OO", ["ô"]],
  ["AW", ["o"]],
  ["AWW_SHORT_ALT", ["o"]], ["AWW", ["o"]],
  ["OE", ["eu"]], ["OEE", ["eu"]],
  ["IA", ["ia"]], ["IA_LONG", ["ia"]],
  ["UA", ["ua"]], ["UA_LONG", ["ua"]],
  ["UO", ["oua"]], ["UO_LONG", ["oua"]], ["UO_SHORT_ALT", ["oua"]],
  ["AI", ["ai"]], ["AI2", ["ai"]],
  ["AW_LONG", ["ao", "ôa"]],
  ["AM", ["am"]],
]);

function crosswalkUnit(unit, sourceSyllable, profile = "bgn-pcgn") {
  const sourceOnset = typeof sourceSyllable === "string"
    ? sourceSyllable
    : sourceSyllable?.onset;
  const sourceOnsetForm = typeof sourceSyllable === "object" && sourceSyllable !== null
    ? sourceSyllable.onsetForm || sourceOnset
    : sourceOnset;
  const rawSourceCoda = typeof sourceSyllable === "object" && sourceSyllable !== null
    ? sourceSyllable.coda
    : undefined;
  const sourceCoda = rawSourceCoda === "—" ? "" : rawSourceCoda;
  const correspondence = profile === "ala-lc"
    ? LAO_ONSET_TO_ALA_LC.get(sourceOnset)
    : LAO_ONSET_CROSSWALK.get(sourceOnset);
  if (!correspondence || correspondence.romanization !== unit.onset) return null;
  const hasSourceVowel = typeof sourceSyllable === "object" && sourceSyllable !== null
    && Object.prototype.hasOwnProperty.call(sourceSyllable, "vowelId");
  if (hasSourceVowel) {
    const expectedNuclei = LAO_VOWEL_TO_CLDR.get(sourceSyllable.vowelId);
    if (!expectedNuclei || !expectedNuclei.includes(unit.nucleus)) return null;
  }
  if (sourceCoda !== undefined) {
    // LOC ALA-LC Note 2 treats final ຍ as the closing /i/ of the diphthong,
    // not as a separately romanized consonant coda.
    const finalNyInDiphthong = profile === "ala-lc"
      && sourceCoda === "ຍ" && unit.nucleus === "ai" && unit.coda === "";
    const expectedCoda = sourceCoda === "" || finalNyInDiphthong ? ""
      : (profile === "ala-lc"
        ? LAO_CODA_TO_ALA_LC.get(sourceCoda)
        : LAO_CODA_TO_CLDR.get(sourceCoda));
    if (expectedCoda === undefined || expectedCoda !== unit.coda) return null;
  }
  return {
    ...unit,
    ukrainian: correspondence.ukrainian + NUCLEI.get(unit.nucleus) +
      (unit.coda ? codaTarget(unit.coda, unit.nucleus) : ""),
    sourceOnset: sourceOnsetForm,
    sourceOnsetKey: sourceOnset,
    sourceCoda,
    sourceVowelId: hasSourceVowel ? sourceSyllable.vowelId : undefined,
    crosswalk: sourceCoda !== undefined
      ? "LAO_SYLLABLE_STRUCTURE↔CLDR_ROMANIZATION↔UKRAINIAN"
      : "LAO_ONSET_GRAPHEME↔CLDR_ROMANIZATION↔UKRAINIAN",
  };
}

export function analyzeRomanization(input, options = {}) {
  const settings = options && typeof options === "object" ? options : {};
  const rawSource = String(input ?? "").normalize("NFC");
  const requestedProfile = settings.profile ?? "auto";
  const profile = detectRomanizationProfile(rawSource, requestedProfile);
  if (!profile) {
    const item = unresolved(rawSource, "UNSUPPORTED_PROFILE");
    item.warning = `Невідомий профіль романізації "${String(requestedProfile)}"; виберіть auto, bgn-pcgn або ala-lc. Вхідний текст залишено без перетворення.`;
    return {
      input: rawSource,
      normalizedInput: rawSource,
      profile: "unsupported",
      output: rawSource ? item.ukrainian : "",
      status: "PARTIAL",
      syllables: rawSource ? [item] : [],
      warnings: [item.warning],
      source: "Unsupported romanization profile; input withheld",
    };
  }
  const source = profile === "ala-lc" ? normalizeAlaLc(rawSource) : rawSource;
  const sourceSyllableGroups = Array.isArray(settings.sourceSyllableGroups) ? settings.sourceSyllableGroups : null;
  const sourceOnsets = sourceSyllableGroups ? null
    : Array.isArray(settings.sourceOnsets) ? settings.sourceOnsets : null;
  // A source-aware crosswalk has one Lao syllable group per whitespace-
  // delimited source token. Keep internal hyphens in that token so they do
  // not advance the source-group cursor onto the next Lao word.
  const separators = sourceSyllableGroups
    ? /(\s+|[,.!?;:()[\]{}"“”]+)/u
    : /(\s+|[,.!?;:()[\]{}"“”]+|-+)/u;
  const parts = source.split(separators).filter(Boolean);
  const rawParts = rawSource.split(separators).filter(Boolean);
  const syllables = [];
  let output = "";
  let partial = false;
  let sourceIndex = 0;
  let sourceGroupIndex = 0;

  for (let partIndex = 0; partIndex < parts.length; partIndex += 1) {
    const part = parts[partIndex];
    const originalPart = rawParts[partIndex] ?? part;
    if (SEPARATORS.test(part) || /^[0-9\u0ED0-\u0ED9]+$/u.test(part)) {
      output += part;
      continue;
    }
    const sourceGroup = sourceSyllableGroups ? (sourceSyllableGroups[sourceGroupIndex++] || []) : null;
    const strictBoundaries = settings.strictBoundaries === true;
    if (profile === "ala-lc" && hasUnsupportedAlaLcSequence(originalPart, part)) {
      const item = unresolved(originalPart, "UNSUPPORTED_ALA_LC_VOWEL");
      item.warning = "ALA-LC 2012 містить голосну послідовність або голосний знак, для якого ще немає перевіреного складового й українського відповідника; фрагмент залишено без здогаду.";
      syllables.push(item);
      output += item.ukrainian;
      partial = true;
      continue;
    }
    const parsed = parseWord(part.toLowerCase(), sourceSyllableGroups ? sourceGroup : null, profile, strictBoundaries);
    if (parsed.count === 1 && parsed.path) {
      const syllablePath = parsed.path.filter((unit) => unit.kind !== "separator");
      const sourceSlice = sourceSyllableGroups ? sourceGroup : sourceOnsets
        ? sourceOnsets.slice(sourceIndex, sourceIndex + syllablePath.length)
        : null;
      const hasCrosswalk = Boolean(sourceSyllableGroups || sourceOnsets);
      const aligned = !hasCrosswalk || sourceSlice.length === syllablePath.length;
      let sourceOffset = 0;
      const crossed = aligned && hasCrosswalk
        ? parsed.path.map((unit) => unit.kind === "separator"
          ? unit
          : crosswalkUnit(unit, sourceSlice[sourceOffset++], profile))
        : parsed.path;
      const validCrosswalk = aligned && crossed.every(Boolean);
      if (validCrosswalk) {
        const units = crossed.map((unit, index) => ({
          ...unit,
          originalSurface: originalPart,
          ukrainian: mapCase(unit.ukrainian, originalPart === originalPart.toUpperCase() || index === 0 ? originalPart : ""),
          status: "OK",
          warning: "",
        }));
        syllables.push(...units.filter((unit) => unit.kind !== "separator"));
        output += units.map((unit) => unit.ukrainian).join("");
        if (sourceOnsets) sourceIndex += syllablePath.length;
      } else {
        const item = unresolved(originalPart, "UNRESOLVED");
        if (aligned && sourceSlice?.length === 1 && parsed.path.length === 1) {
          const sourceUnit = sourceSlice[0];
          item.sourceOnset = typeof sourceUnit === "string" ? sourceUnit : sourceUnit?.onsetForm || sourceUnit?.onset;
          item.sourceOnsetKey = typeof sourceUnit === "string" ? sourceUnit : sourceUnit?.onset;
          item.sourceCoda = typeof sourceUnit === "object" && sourceUnit !== null
            ? sourceUnit.coda
            : undefined;
          item.sourceVowelId = typeof sourceUnit === "object" && sourceUnit !== null
            ? sourceUnit.vowelId
            : undefined;
          item.onset = parsed.path[0].onset;
          item.nucleus = parsed.path[0].nucleus;
          item.coda = parsed.path[0].coda;
        }
        item.warning = aligned
          ? "Романізований початок, голосний комплекс або фіналь не відповідають лаоським графемам; український результат утримано."
          : "Кількість розібраних романізованих складів не збігається з кількістю лаоських складових одиниць; звірку утримано.";
        syllables.push(item);
        output += item.ukrainian;
        partial = true;
        if (sourceOnsets) sourceIndex += sourceSlice.length;
      }
    } else {
      const unrestricted = sourceSyllableGroups && parsed.count === 0 ? parseWord(part.toLowerCase(), null, profile, strictBoundaries) : null;
      const sourceMismatch = Boolean(unrestricted?.count);
      const item = unresolved(originalPart, parsed.count > 1 ? "AMBIGUOUS" : "UNRESOLVED");
      if (sourceMismatch) {
        item.warning = "Романізований склад можна розібрати, але його початок, голосний комплекс або фіналь не відповідають лаоським графемам; український результат утримано.";
        if (sourceGroup.length === 1 && unrestricted.count === 1) {
          item.sourceOnset = sourceGroup[0]?.onset;
          item.sourceCoda = sourceGroup[0]?.coda;
          item.onset = unrestricted.path[0].onset;
          item.nucleus = unrestricted.path[0].nucleus;
          item.coda = unrestricted.path[0].coda;
        }
      }
      syllables.push(item);
      output += item.ukrainian;
      partial = true;
    }
  }

  const warnings = syllables.filter((unit) => unit.warning).map((unit) => unit.warning);
  if (sourceOnsets && sourceIndex !== sourceOnsets.length) {
    partial = true;
    warnings.push("Кількість лаоських початкових графем і романізованих складів не збігається; звірку не виконано.");
  }
  if (sourceSyllableGroups && sourceGroupIndex !== sourceSyllableGroups.length) {
    partial = true;
    warnings.push("Кількість лаоських складових груп і романізованих фрагментів не збігається; повну звірку не виконано.");
  }

  return {
    input: rawSource,
    normalizedInput: source,
    profile,
    output,
    status: partial ? "PARTIAL" : "OK",
    syllables,
    warnings,
    source: profile === "ala-lc"
      ? "ALA-LC 2012 → normalized syllable profile → Ukrainian practical syllable adapter (partial where distinctions are not represented)"
      : "BGN/PCGN 1966 / CLDR Lao-Latin romanization → Ukrainian syllable adapter",
  };
}

export function romanizationToUkrainian(input, options = {}) {
  const result = analyzeRomanization(input, options);
  return { output: result.output, status: result.status, syllables: result.syllables, source: result.source, profile: result.profile, normalizedInput: result.normalizedInput, warnings: result.warnings };
}

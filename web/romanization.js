// Lao-Latin/UNGEGN transform from Unicode CLDR (provisional).
// Source: https://github.com/unicode-org/cldr/blob/main/common/transforms/Lao-Latin.xml
// Copyright © 1991-2013 Unicode, Inc.; see https://www.unicode.org/copyright.html
// This is a deliberately small, ordered implementation of the simple literal rules.
// Context-sensitive ICU rules are handled only where explicitly documented below.
const SEQUENCES = [
  ["ເັຽະ","ia"],["ເຶອະ","ua"],["ເາະ","o"],["ເິະ","eu"],
  ["ເັຽ","ia"],["ເຶອ","ua"],["ເືອ","ua"],["ົວະ","oua"],["ເົາ","ao"],
  ["ຣ໌ ","r "],["ເະ","é"],["ເັ","é"],["ແະ","è"],["ແັ","è"],
  ["ໂະ","ô"],["ັອ","o"],["ເິ","eu"],["ເີ","eu"],["ເື","eu"],
  ["ັຽ","ia"],["ັວ","oua"],["ົວ","oua"]
];
const MAP = new Map(Object.entries({
  "ກ":"k","ຂ":"kh","ຄ":"kh","ງ":"ng","ຈ":"ch","ສ":"s","ຊ":"x","ຍ":"gn",
  "ດ":"d","ຕ":"t","ຖ":"th","ທ":"th","ນ":"n","ບ":"b","ປ":"p","ຜ":"ph",
  "ຝ":"f","ພ":"ph","ຟ":"f","ມ":"m","ຢ":"y","ຣ":"r","ລ":"l","ວ":"v","ຫ":"h","ຮ":"h",
  "ະ":"a","ັ":"a","າ":"a","ິ":"i","ີ":"i","ຶ":"u","ື":"u","ຸ":"ou","ູ":"ou",
  "ເ":"é","ແ":"è","ົ":"ô","ໂ":"ô","ໍ":"o","ຽ":"ia","ໄ":"ai","ໃ":"ai","ຳ":"am",
  "່":"","້":"","໊":"","໋":"","ຯ":"…","ฯ":"…","ໆ":"⓶","ຼ":"o","໌":"","ໜ":"n","ໝ":"n",
  "ອ":""
}));
const LAO_RE = /[\u0E80-\u0EFF]/u;
export function romanizeLao(input) {
  const source = String(input ?? "").normalize("NFC");
  let output = source;
  for (const [from, to] of SEQUENCES) output = output.split(from).join(to);
  // BGN/PCGN's silent-hoa note: ຫ before a supported sonorant onset is a high-class
  // marker, not a pronounced /h/. The ຫຼ ligature is likewise romanized l.
  output = output.replace(/ຫຼ/gu, "ລ");
  output = output.replace(/ຫ(?=[ງຍນມລວ])/gu, "");
  // CLDR's contextual rule maps an ອ following a letter/mark to a hyphen;
  // other ອ instances are deleted by the next literal rule.
  output = output.replace(/([\p{L}\p{M}])ອ/gu, "$1-");
  output = [...output].map(ch => MAP.has(ch) ? MAP.get(ch) : ch).join("");
  const remainingLao = LAO_RE.test(output);
  return { output, status: remainingLao ? "PARTIAL" : "PROVISIONAL", source: "CLDR Lao-Latin (provisional; BGN/PCGN-aligned subset)" };
}


// ALA-LC 2012 Note 8 is a Lao-source orthographic numeral conversion.
// Keep it separate from the provisional BGN/PCGN CLDR syllable romanizer:
// only Lao digits U+0ED0–U+0ED9 are converted; all other code points,
// punctuation and separators are preserved verbatim.
const ALA_LC_LAO_DIGITS = "໐໑໒໓໔໕໖໗໘໙";

export function romanizeAlaLcNumerals(input) {
  const source = String(input ?? "");
  let mappedCount = 0;
  const output = [...source].map((character) => {
    const digit = ALA_LC_LAO_DIGITS.indexOf(character);
    if (digit < 0) return character;
    mappedCount += 1;
    return String(digit);
  }).join("");
  return {
    input: source,
    output,
    profile: "ALA-LC 2012",
    rule: "Note 8",
    direction: "Lao-script→Arabic numerals",
    mappedCount,
    status: mappedCount > 0 ? "OK" : "NO_LAO_NUMERALS",
    source: "Library of Congress, ALA-LC Lao Romanization Table (2012), Note 8",
  };
}

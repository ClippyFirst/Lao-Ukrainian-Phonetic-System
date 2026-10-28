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
  // CLDR's contextual rule maps an ອ following a letter/mark to a hyphen;
  // other ອ instances are deleted by the next literal rule.
  output = output.replace(/([\p{L}\p{M}])ອ/gu, "$1-");
  output = [...output].map(ch => MAP.has(ch) ? MAP.get(ch) : ch).join("");
  const remainingLao = LAO_RE.test(output);
  return { output, status: remainingLao ? "PARTIAL" : "PROVISIONAL", source: "CLDR Lao-Latin/UNGEGN (provisional)" };
}

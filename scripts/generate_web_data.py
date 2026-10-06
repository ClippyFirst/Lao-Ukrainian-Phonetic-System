"""Generate the browser data mirror from canonical Lao CSV registries."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "lao"
OUT = ROOT / "web" / "data.js"

def rows(name):
    with (DATA / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

consonant_rows = rows("consonants.csv")
corr = {r["ipa"]: r["candidates"].split("|")[0] for r in rows("ukrainian_correspondences.csv")}

cons = {}
for r in consonant_rows:
    if r["status"] not in {"core", "analysis-dependent"}:
        continue
    cons[r["grapheme"]] = [r["class"], r["ipa_initial"], r["status"], corr.get(r["ipa_initial"], "")]

vowels = [
    [r["id"], r["pattern"], r["ipa"], r["length"], r["position"], r["status"]]
    for r in rows("vowels.csv")
    if r["status"] in {"core", "well-supported"}
]

codas = {
    r["grapheme"]: r["ipa_final"]
    for r in consonant_rows
    if r["status"] in {"core", "analysis-dependent"} and r["ipa_final"]
}

marks = {"່": "mai_ek", "້": "mai_tho", "໊": "mai_ti", "໋": "mai_catawa"}

rules = [
    [r["class"], r["syllable_type"], r["length"], r["tone_mark"], r["tone"], r["contour"], r["rule_id"]]
    for r in rows("tone_rules.csv")
    if r["status"] in {"core", "well-supported"}
]

out = "// Generated from data/lao/*.csv. Do not edit by hand.\n"
out += "export const CONSONANTS=" + json.dumps(cons, ensure_ascii=False, separators=(",", ":")) + ";\n"
out += "export const VOWELS=" + json.dumps(vowels, ensure_ascii=False, separators=(",", ":")) + ";\n"
out += "export const CODAS=" + json.dumps(codas, ensure_ascii=False, separators=(",", ":")) + ";\n"
out += "export const CORRESPONDENCES=" + json.dumps(corr, ensure_ascii=False, separators=(",", ":")) + ";\n"
out += "export const TONE_MARKS=" + json.dumps(marks, ensure_ascii=False, separators=(",", ":")) + ";\n"
out += "export const TONE_RULES=" + json.dumps(rules, ensure_ascii=False, separators=(",", ":")) + ";\n"
OUT.write_text(out, encoding="utf-8")

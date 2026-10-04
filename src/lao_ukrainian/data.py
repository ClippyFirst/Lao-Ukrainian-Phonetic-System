import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "lao"

def csv_rows(name: str):
    with (DATA / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def json_data(name: str):
    with (DATA / name).open(encoding="utf-8") as f:
        return json.load(f)

def load_registry():
    return {
        "consonants": {r["grapheme"]: r for r in csv_rows("consonants.csv")},
        "vowels": csv_rows("vowels.csv"),
        "tone_rules": csv_rows("tone_rules.csv"),
        "codas": {r["phoneme"]: r for r in csv_rows("codas.csv")},
        "correspondences": {r["ipa"]: r for r in csv_rows("ukrainian_correspondences.csv")},
        "comparative": csv_rows("../comparative/cyrillic_comparison.csv"),
    }

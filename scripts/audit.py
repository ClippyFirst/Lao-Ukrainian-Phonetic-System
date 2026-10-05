"""Repository-level deterministic audit with no third-party dependencies."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def main():
    consonants=read_csv(ROOT/"data/lao/consonants.csv")
    vowels=read_csv(ROOT/"data/lao/vowels.csv")
    tones=read_csv(ROOT/"data/lao/tone_rules.csv")
    ua=read_csv(ROOT/"data/lao/ukrainian_correspondences.csv")

    assert len({r["grapheme"] for r in consonants})==len(consonants), "duplicate consonant grapheme"
    assert len({r["id"] for r in vowels})==len(vowels), "duplicate vowel id"
    assert len({r["rule_id"] for r in tones})==len(tones), "duplicate tone rule"
    assert len({r["ipa"] for r in ua})==len(ua), "duplicate IPA mapping"
    for row in consonants:
        cp=int(row["codepoint"].replace("U+",""),16)
        assert 0x0E80 <= cp <= 0x0EFF, f"non-Lao codepoint: {row}"
    print(f"OK: {len(consonants)} consonant rows; {len(vowels)} vowel rows; {len(tones)} tone rules; {len(ua)} UA mappings")

if __name__=="__main__":
    main()

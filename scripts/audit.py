"""Repository-level deterministic audit with no third-party dependencies."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def main():
    consonants=read_csv(ROOT/"data/lao/consonants.csv")
    onset_clusters=read_csv(ROOT/"data/lao/onset_clusters.csv")
    vowels=read_csv(ROOT/"data/lao/vowels.csv")
    tones=read_csv(ROOT/"data/lao/tone_rules.csv")
    ua=read_csv(ROOT/"data/lao/ukrainian_correspondences.csv")
    sources=read_csv(ROOT/"data/evidence/sources.csv")
    claims=read_csv(ROOT/"data/evidence/claims.csv")

    assert len({r["grapheme"] for r in consonants})==len(consonants), "duplicate consonant grapheme"
    assert len({r["grapheme"] for r in onset_clusters})==len(onset_clusters), "duplicate onset cluster grapheme"
    assert len({r["id"] for r in vowels})==len(vowels), "duplicate vowel id"
    for row in vowels:
        assert row["nucleus_type"] in {"monophthong", "diphthong"}, f"unknown nucleus type: {row['id']}"
    assert len({r["rule_id"] for r in tones})==len(tones), "duplicate tone rule"
    for row in tones:
        if row["tone_mark"] != "none":
            assert row["syllable_type"] == "live", f"tone mark on non-live syllable selector: {row['rule_id']}"
        if row["tone_mark"] == "mai_ti":
            assert row["class"] == "middle" and row["tone"] == "high-falling", f"invalid mai ti selector: {row['rule_id']}"
        if row["tone_mark"] == "mai_catawa":
            assert row["class"] == "middle" and row["tone"] == "low-rising", f"invalid mai catawa selector: {row['rule_id']}"
    assert len({r["ipa"] for r in ua})==len(ua), "duplicate IPA mapping"
    assert len({r["source_id"] for r in sources})==len(sources), "duplicate evidence source id"
    assert len({r["claim_id"] for r in claims})==len(claims), "duplicate evidence claim id"
    source_ids={r["source_id"] for r in sources}
    claim_ids={r["claim_id"] for r in claims}
    consonant_by_grapheme={r["grapheme"]: r for r in consonants}
    allowed_labialized_ipa={"tʷʰ", "tɕʷ", "kʷ", "kʷʰ", "ʔʷ", "sʷ", "ŋʷ", "lʷ"}
    for row in onset_clusters:
        base=consonant_by_grapheme.get(row["base"])
        assert base, f"unknown onset cluster base: {row['grapheme']}"
        assert row["grapheme"] == row["base"] + "ວ", f"invalid labialized onset spelling: {row['grapheme']}"
        assert row["class"] == base["class"], f"onset cluster class mismatch: {row['grapheme']}"
        assert row["ipa_initial"] in allowed_labialized_ipa, f"unsupported labialized IPA: {row['grapheme']}"
        assert row["status"] == "well-supported", f"unexpected onset cluster status: {row['grapheme']}"
        assert row["source_id"] in source_ids, f"unknown onset cluster source: {row['grapheme']}"
        assert row["claim_id"] in claim_ids, f"unknown onset cluster claim: {row['grapheme']}"
    for row in claims:
        evidence_ids={item for item in row["evidence_ids"].split(";") if item}
        assert evidence_ids, f"claim without evidence: {row['claim_id']}"
        assert evidence_ids <= source_ids, f"claim references unknown sources: {row['claim_id']} {sorted(evidence_ids-source_ids)}"
    for row in consonants:
        cp=int(row["codepoint"].replace("U+",""),16)
        assert 0x0E80 <= cp <= 0x0EFF, f"non-Lao codepoint: {row}"
    print(f"OK: {len(consonants)} consonant rows; {len(vowels)} vowel rows; {len(tones)} tone rules; {len(ua)} UA mappings; {len(sources)} evidence sources; {len(claims)} evidence claims")

if __name__=="__main__":
    main()

"""Repository-level deterministic audit with no third-party dependencies."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def main():
    inventory=read_csv(ROOT/"data/lao/grapheme_inventory.csv")
    consonants=read_csv(ROOT/"data/lao/consonants.csv")
    onset_clusters=read_csv(ROOT/"data/lao/onset_clusters.csv")
    vowels=read_csv(ROOT/"data/lao/vowels.csv")
    tones=read_csv(ROOT/"data/lao/tone_rules.csv")
    special_tones=read_csv(ROOT/"data/lao/special_tone_rules.csv")
    ua=read_csv(ROOT/"data/lao/ukrainian_correspondences.csv")
    sources=read_csv(ROOT/"data/evidence/sources.csv")
    claims=read_csv(ROOT/"data/evidence/claims.csv")

    assert len({r["codepoint"] for r in inventory})==len(inventory), "duplicate inventory codepoint"
    assert len({r["grapheme"] for r in inventory})==len(inventory), "duplicate inventory grapheme"
    source_ids={r["source_id"] for r in sources}
    claim_ids={r["claim_id"] for r in claims}
    inventory_by_grapheme={r["grapheme"]:r for r in inventory}
    for row in inventory:
        cp=int(row["codepoint"].replace("U+",""),16)
        assert len(row["grapheme"])==1 and ord(row["grapheme"])==cp, f"grapheme/codepoint mismatch: {row}"
        assert row["source_id"] in source_ids, f"unknown inventory source: {row}"
        assert row["claim_id"] in claim_ids, f"unknown inventory claim: {row}"
    assert set(r["grapheme"] for r in consonants) <= set(inventory_by_grapheme), "consonant registry missing from grapheme inventory"
    assert len({r["grapheme"] for r in consonants})==len(consonants), "duplicate consonant grapheme"
    assert len({r["grapheme"] for r in onset_clusters})==len(onset_clusters), "duplicate onset cluster grapheme"
    assert len({r["id"] for r in vowels})==len(vowels), "duplicate vowel id"
    for row in vowels:
        assert row["nucleus_type"] in {"monophthong","diphthong"}, f"unknown nucleus type: {row['id']}"
    assert len({r["rule_id"] for r in tones})==len(tones), "duplicate tone rule"
    assert len({r["rule_id"] for r in special_tones})==len(special_tones), "duplicate special tone rule"
    for row in tones:
        if row["tone_mark"]!="none":
            assert row["syllable_type"]=="live", f"tone mark on non-live syllable selector: {row['rule_id']}"
        if row["tone_mark"]=="mai_ti":
            assert row["class"]=="middle" and row["tone"]=="high-falling", f"invalid mai ti selector: {row['rule_id']}"
        if row["tone_mark"]=="mai_catawa":
            assert row["class"]=="middle" and row["tone"]=="low-rising", f"invalid mai catawa selector: {row['rule_id']}"
    assert len({r["ipa"] for r in ua})==len(ua), "duplicate IPA mapping"
    assert len({r["source_id"] for r in sources})==len(sources), "duplicate evidence source id"
    assert len({r["claim_id"] for r in claims})==len(claims), "duplicate evidence claim id"
    for row in special_tones:
        assert row["profile"]=="Vientiane", f"unknown special tone profile: {row['rule_id']}"
        assert not row["tone"] and not row["contour"], f"invalid unresolved special tone selector: {row['rule_id']}"
        assert row["status"]=="analysis-dependent", f"unsupported special tone status: {row['rule_id']}"
        assert row["evidence_id"] in claim_ids, f"unknown special tone claim: {row['rule_id']}"
    consonant_by_grapheme={r["grapheme"]:r for r in consonants}
    allowed_labialized_ipa={"tʷʰ","tɕʷ","kʷ","kʷʰ","ʔʷ","sʷ","ŋʷ","lʷ"}
    for row in onset_clusters:
        base=consonant_by_grapheme.get(row["base"])
        assert base, f"unknown onset cluster base: {row['grapheme']}"
        assert row["grapheme"]==row["base"]+"ວ", f"invalid labialized onset spelling: {row['grapheme']}"
        assert row["class"]==base["class"], f"onset cluster class mismatch: {row['grapheme']}"
        assert row["ipa_initial"] in allowed_labialized_ipa, f"unsupported labialized IPA: {row['grapheme']}"
        assert row["status"]=="well-supported", f"unexpected labialized onset status: {row['grapheme']}"
        assert row["source_id"] in source_ids, f"unknown onset cluster source: {row['grapheme']}"
        assert row["claim_id"] in claim_ids, f"unknown onset cluster claim: {row['grapheme']}"
    for row in claims:
        evidence_ids={x for x in row["evidence_ids"].split(";") if x}
        assert evidence_ids, f"claim without evidence: {row['claim_id']}"
        assert evidence_ids <= source_ids, f"unknown claim sources: {row['claim_id']}"
    for row in consonants:
        cp=int(row["codepoint"].replace("U+",""),16)
        assert 0x0E80<=cp<=0x0EFF, f"non-Lao codepoint: {row}"
    print(f"OK: {len(inventory)} Unicode Lao-block graphemes; {len(consonants)} consonant rows; {len(onset_clusters)} onset clusters; {len(vowels)} vowel rows; {len(tones)} tone rules; {len(special_tones)} special tone rules; {len(ua)} UA mappings; {len(sources)} sources; {len(claims)} claims")

if __name__=="__main__":
    main()

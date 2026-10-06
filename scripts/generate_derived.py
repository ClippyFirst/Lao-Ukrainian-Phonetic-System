"""Generate the compact derived IPA → Ukrainian table from the canonical mapping."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/lao/ukrainian_correspondences.csv"
DST=ROOT/"data/derived/lao_ukrainian_practical_correspondence.csv"

def main():
    with SRC.open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    fields=["ipa","ukrainian_practical","alternatives","rationale","status"]
    with DST.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for row in rows:
            candidates=row["candidates"].split("|")
            w.writerow({
                "ipa":row["ipa"],
                "ukrainian_practical":candidates[0],
                "alternatives":"|".join(candidates),
                "rationale":row["rationale"],
                "status":row["status"],
            })
    print(f"generated {DST.relative_to(ROOT)} from {SRC.relative_to(ROOT)}")

if __name__=="__main__":
    main()

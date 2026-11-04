"""Source-registry contract for the LDC Babel Lao audio candidate.

The catalog entry is a research lead, not an enabled runtime dependency or IPA gold.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ldc_babel_lao_source_is_profiled_and_access_gated():
    with (ROOT / "data" / "evidence" / "sources.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    ids = [row["source_id"] for row in rows]
    assert len(ids) == len(set(ids))
    source = next(row for row in rows if row["source_id"] == "SRC-LDC-BABEL-LAO-2017")

    assert source["url"] == "https://catalog.ldc.upenn.edu/LDC2017S08"
    assert "207 hours" in source["scope"]
    assert "Vientiane-region" in source["scope"]
    assert "LDC access agreement" in source["scope"]
    assert "not IPA labels" in source["scope"]
    assert "U.S. Government" in source["scope"]

"""Contract tests for the optional Lao external-G2P diagnostic harness.

These tests validate reproducibility safeguards, not pronunciation accuracy.
"""
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = runpy.run_path(str(ROOT / "scripts" / "compare_external_g2p.py"))
nfc = HARNESS["nfc"]


def test_nfc_normalization_preserves_phonetic_distinctions():
    # Canonical Unicode equivalence is allowed; tone, length and syllable
    # boundaries must not be stripped to inflate exact-match rates.
    assert nfc("  kʰaː˥.ŋ  ") == "  kʰaː˥.ŋ  "
    assert nfc("a\u0304") == "ā"
    assert nfc(None) is None


def test_comparison_fixture_is_explicitly_engineering_only():
    fixture = json.loads(
        (ROOT / "tests" / "fixtures" / "vowel_precedence_cases.json").read_text(
            encoding="utf-8"
        )
    )
    assert fixture["cases"]
    purpose = fixture.get("purpose", "").lower()
    assert "engineering" in purpose or "regression" in purpose
    # This fixture cannot be misrepresented as independently adjudicated gold.
    assert "gold" not in purpose or "not" in purpose or "not an" in purpose


def test_harness_keeps_nfc_as_its_only_normalization():
    source = (ROOT / "scripts" / "compare_external_g2p.py").read_text(
        encoding="utf-8"
    )
    assert "unicodedata.normalize(\"NFC\", value)" in source
    assert "ignore_tones=True" not in source
    assert "replace(\"ː\", \"\")" not in source

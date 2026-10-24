from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ipa_output_has_language_and_display_fallback():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
    assert 'id="ipa" class="ipa" lang="und-fonipa"' in html
    assert '[lang="und-fonipa"]' in css
    for font in ('"Charis SIL"', '"Doulos SIL"', '"DejaVu Sans"'):
        assert font in css
    for feature in ('"ccmp"', '"mark"', '"mkmk"'):
        assert feature in css
    assert "unicode-bidi: isolate" in css
    assert "@import" not in css.lower()
    assert "url(http" not in css.lower()

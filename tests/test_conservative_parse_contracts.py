"""Conservative parser contracts; these tests are not a pronunciation gold set."""

from lao_ukrainian.parser import parse_syllable


def test_trailing_vowel_after_legal_final_is_not_silently_discarded():
    result = parse_syllable("ກາງະ")

    assert result["coda"] is None
    assert any(
        warning.startswith("UNCONSUMED_AFTER_VOWEL:")
        for warning in result["warnings"]
    )


def test_legal_final_coda_is_recognized_at_the_end_of_the_syllable():
    result = parse_syllable("ການ")

    assert result["coda"] == "ນ"
    assert not any(
        warning.startswith("UNCONSUMED_AFTER_VOWEL:")
        for warning in result["warnings"]
    )

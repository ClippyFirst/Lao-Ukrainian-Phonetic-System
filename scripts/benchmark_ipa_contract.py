"""Shared confidence gate for Lao G2P benchmark IPA accuracy scoring.

A provisional grapheme preview is a rendering aid, not accepted IPA. Keep
rendering coverage separate from IPA accuracy and never score PROVISIONAL
segments against an IPA reference.
"""


def accepted_phonetic_ipa(result) -> bool:
    return bool(
        result is not None
        and getattr(result, "status", None) in {"SUPPORTED", "UNCERTAIN"}
        and getattr(result, "phonemic_ipa", None)
    )

from .data import load_registry
from .model import PhoneticResult, PhoneticSegment

VOWEL_INITIALS = frozenset("aeiouɯɤɛɔəɪʊ")


def from_phonology(
    ipa: str | None,
    *,
    vowel_length: str | None = None,
    tone: str | None = None,
    tone_contour: str | None = None,
    status: str = "SUPPORTED",
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> PhoneticResult:
    """Create the typed, inspectable IPA boundary for one analysed Lao syllable."""
    registry = load_registry()["correspondences"]
    if not ipa:
        return PhoneticResult(
            None, (), (0,), vowel_length, tone, tone_contour,
            "UNSUPPORTED", provenance, uncertainty,
        )
    keys = sorted(registry, key=len, reverse=True)
    segments: list[PhoneticSegment] = []
    index = 0
    while index < len(ipa):
        match = next((key for key in keys if ipa.startswith(key, index)), None)
        if match is None:
            return PhoneticResult(
                ipa, tuple(segments), (0, len(segments)), vowel_length, tone,
                tone_contour, "UNSUPPORTED", provenance,
                (*uncertainty, f"Unsupported IPA segment at offset {index}: {ipa[index:]!r}"),
            )
        kind = "vowel" if match[0] in VOWEL_INITIALS else "consonant"
        segments.append(PhoneticSegment(match, kind, provenance))
        index += len(match)
    return PhoneticResult(
        ipa, tuple(segments), (0, len(segments)), vowel_length, tone,
        tone_contour, status, provenance, uncertainty,
    )

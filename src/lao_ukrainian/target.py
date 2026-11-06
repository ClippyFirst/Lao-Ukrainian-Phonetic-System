from .data import load_registry
from .model import PhoneticResult, PhoneticSegment

VOWEL_INITIALS = frozenset("aeiouɯɤɛɔəɪʊ")


def phonetic_result_from_ipa(
    ipa: str | None,
    *,
    vowel_length: str | None = None,
    tone: str | None = None,
    tone_contour: str | None = None,
    status: str = "SUPPORTED",
    provenance: tuple[str, ...] = (),
    uncertainty: tuple[str, ...] = (),
) -> PhoneticResult:
    """Build the typed IPA adapter contract from an already analysed syllable."""
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


def adapt_phonetic_result(result: PhoneticResult) -> str | None:
    """Adapt only a supported typed phonetic result; uncertain IPA fails closed."""
    if not isinstance(result, PhoneticResult):
        raise TypeError("Ukrainian adaptation requires a PhoneticResult")
    if result.status != "SUPPORTED" or not result.segments:
        return None
    registry = load_registry()["correspondences"]
    output: list[str] = []
    for segment in result.segments:
        row = registry.get(segment.ipa)
        if row is None:
            return None
        output.append(row["candidates"].split("|")[0])
    return "".join(output)


def practical_from_ipa(result: PhoneticResult) -> str | None:
    """Compatibility name retained with the new typed-only input contract."""
    return adapt_phonetic_result(result)


def rank_ukrainian_candidates(result: PhoneticResult):
    """Return exact whole-IPA candidates only for supported typed results."""
    if not isinstance(result, PhoneticResult):
        raise TypeError("Candidate ranking requires a PhoneticResult")
    if result.status != "SUPPORTED" or not result.phonemic_ipa:
        return []
    row = load_registry()["correspondences"].get(result.phonemic_ipa)
    if not row:
        return []
    values = row["candidates"].split("|")
    return [
        (value, float(row["preferred_score"]) - index * 0.1, row["rationale"])
        for index, value in enumerate(values)
    ]

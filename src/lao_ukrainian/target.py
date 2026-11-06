from .data import load_registry
from .model import PhoneticResult
from .phonetic_result import from_phonology, from_phonology as phonetic_result_from_ipa


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

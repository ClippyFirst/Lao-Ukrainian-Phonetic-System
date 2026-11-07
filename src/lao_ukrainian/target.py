from .data import load_registry
from .model import PhoneticResult
from .phonetic_result import from_phonology, from_phonology as phonetic_result_from_ipa


def adapt_phonetic_result(result: PhoneticResult, registry=None) -> str | None:
    """Adapt only a supported typed phonetic result; uncertain IPA fails closed."""
    if not isinstance(result, PhoneticResult):
        raise TypeError("Ukrainian adaptation requires a PhoneticResult")
    if result.status != "SUPPORTED" or not result.segments:
        return None
    if any(segment.certainty != "SUPPORTED" for segment in result.segments):
        return None
    registry = (registry if registry is not None else load_registry())["correspondences"]
    ipa = "".join(segment.ipa for segment in result.segments)
    keys = sorted(registry, key=len, reverse=True)
    output: list[str] = []
    index = 0

    # Ukrainian йотовані letters are a syllable-onset convention, not a
    # global replacement for every /j/. PhoneticResult represents one
    # analyzed syllable, so this rule is safe only at its first segment.
    initial_yodated = {
        "a": "я", "aː": "я",
        "e": "є", "eː": "є", "ɛ": "є", "ɛː": "є",
        "i": "ї", "iː": "ї",
        "o": "йо", "oː": "йо", "ɔ": "йо", "ɔː": "йо",
        "u": "ю", "uː": "ю",
        "ɯ": "йи", "ɯː": "йи",
        "ɤ": "йе", "ɤː": "йе",
    }
    if (len(result.segments) >= 2
            and result.segments[0].ipa == "j"
            and result.segments[1].kind == "vowel"
            and result.segments[1].ipa in initial_yodated):
        output.append(initial_yodated[result.segments[1].ipa])
        index = len(result.segments[0].ipa) + len(result.segments[1].ipa)

    while index < len(ipa):
        match = next((key for key in keys if ipa.startswith(key, index)), None)
        if match is None:
            return None
        output.append(registry[match]["candidates"].split("|")[0])
        index += len(match)
    return "".join(output)


def practical_from_ipa(result: PhoneticResult, registry=None) -> str | None:
    """Compatibility name retained with the new typed-only input contract."""
    return adapt_phonetic_result(result, registry)


def rank_ukrainian_candidates(result: PhoneticResult, registry=None):
    """Return exact whole-IPA candidates only for supported typed results."""
    if not isinstance(result, PhoneticResult):
        raise TypeError("Candidate ranking requires a PhoneticResult")
    if result.status != "SUPPORTED" or not result.phonemic_ipa:
        return []
    registry = registry if registry is not None else load_registry()
    row = registry["correspondences"].get(result.phonemic_ipa)
    if not row:
        return []
    values = row["candidates"].split("|")
    return [
        (value, float(row["preferred_score"]) - index * 0.1, row["rationale"])
        for index, value in enumerate(values)
    ]

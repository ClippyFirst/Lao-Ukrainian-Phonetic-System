from .data import load_registry
from .model import PhoneticResult
from .phonetic_result import from_phonology as phonetic_result_from_ipa

# Project-specific Ukrainian orthography policy for a syllable-initial /j/.
# A multi-vowel nucleus is deliberately not collapsed into a monophthongal
# yodated letter unless a separately evidenced sequence rule is added.
INITIAL_YODATED = {
    "a": "я", "aː": "я",
    "e": "є", "eː": "є", "ɛ": "є", "ɛː": "є",
    "i": "ї", "iː": "ї",
    "o": "йо", "oː": "йо", "ɔ": "йо", "ɔː": "йо",
    "u": "ю", "uː": "ю",
    "ɯ": "йи", "ɯː": "йи",
    "ɤ": "йе", "ɤː": "йе",
}


def _segmental_syllables(result: PhoneticResult):
    """Return segmental segments and syllable spans after removing typed tones."""
    segments = tuple(segment for segment in result.segments if segment.kind != "tone")
    prefix_counts = [0]
    for segment in result.segments:
        prefix_counts.append(prefix_counts[-1] + (segment.kind != "tone"))

    raw_boundaries = result.syllable_boundaries or (0,)
    boundaries = sorted({
        prefix_counts[index]
        for index in raw_boundaries
        if isinstance(index, int) and 0 <= index <= len(result.segments)
    })
    if not boundaries or boundaries[0] != 0:
        boundaries.insert(0, 0)
    if boundaries[-1] != len(segments):
        boundaries.append(len(segments))

    spans = [
        (start, end)
        for start, end in zip(boundaries, boundaries[1:])
        if end > start
    ]
    return segments, spans


def _map_ipa_sequence(ipa: str, registry: dict[str, dict[str, str]]) -> str | None:
    keys = sorted(registry, key=len, reverse=True)
    output: list[str] = []
    index = 0
    while index < len(ipa):
        match = next((key for key in keys if ipa.startswith(key, index)), None)
        if match is None:
            return None
        output.append(registry[match]["candidates"].split("|")[0])
        index += len(match)
    return "".join(output)


def adapt_phonetic_result(result: PhoneticResult, registry=None) -> str | None:
    """Adapt supported typed IPA, applying yodation at explicit syllable starts."""
    if not isinstance(result, PhoneticResult):
        raise TypeError("Ukrainian adaptation requires a PhoneticResult")
    if result.status != "SUPPORTED" or not result.segments:
        return None
    if any(segment.certainty != "SUPPORTED" for segment in result.segments):
        return None

    correspondence_registry = (
        registry if registry is not None else load_registry()
    )["correspondences"]
    segments, spans = _segmental_syllables(result)
    if not segments or not spans:
        return None

    output: list[str] = []
    for start, end in spans:
        syllable = segments[start:end]
        ipa = "".join(segment.ipa for segment in syllable)
        index = 0
        if (
            len(syllable) >= 2
            and syllable[0].ipa == "j"
            and syllable[1].kind == "vowel"
            and syllable[1].ipa in INITIAL_YODATED
            and (len(syllable) == 2 or syllable[2].kind != "vowel")
        ):
            output.append(INITIAL_YODATED[syllable[1].ipa])
            index = len(syllable[0].ipa) + len(syllable[1].ipa)

        mapped = _map_ipa_sequence(ipa[index:], correspondence_registry)
        if mapped is None:
            return None
        output.append(mapped)

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

from .model import PhoneticResult, PhoneticSegment

# Source IPA inventory, independent of the Ukrainian correspondence table.
# Multi-character phonemes and long vowels are single segment tokens; vowel
# sequences remain separate segments and can be combined by the target adapter.
IPA_SYMBOLS = (
    "t͡ɕ", "t͡ʃ", "t͡s", "d͡z", "d͡ʒ", "d͡ʑ", "tɕʰ", "tɕ", "dʑ", "ɲ",
    "kʰ", "pʰ", "tʰ", "nʲ", "lʲ", "rʲ", "tʲ", "dʲ",
    "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː",
    "k", "p", "t", "d", "b", "ŋ", "m", "n", "s", "f",
    "h", "ɡ", "g", "x", "ɦ", "r", "l", "j", "ʋ", "w", "ʔ",
    "ʃ", "ʒ", "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
)
VOWEL_SYMBOLS = frozenset({
    "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː",
    "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
})


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
    """Create the typed IPA boundary using a source IPA inventory, not target mappings."""
    if not ipa:
        return PhoneticResult(
            None, (), (0,), vowel_length, tone, tone_contour,
            "UNSUPPORTED", provenance, uncertainty,
        )
    symbols = sorted(IPA_SYMBOLS, key=len, reverse=True)
    segments: list[PhoneticSegment] = []
    index = 0
    unsupported = False
    while index < len(ipa):
        match = next((symbol for symbol in symbols if ipa.startswith(symbol, index)), None)
        if match is None:
            unsupported = True
            segments.append(PhoneticSegment(ipa[index], "unknown", provenance, "UNSUPPORTED"))
            index += 1
            continue
        kind = "vowel" if match in VOWEL_SYMBOLS else "consonant"
        segments.append(PhoneticSegment(match, kind, provenance))
        index += len(match)
    result_status = "UNSUPPORTED" if unsupported else status
    notes = (*uncertainty, *(("UNSUPPORTED-IPA-SEGMENT",) if unsupported else ()))
    return PhoneticResult(
        ipa, tuple(segments), (0, len(segments)), vowel_length, tone,
        tone_contour, result_status, provenance, notes,
    )

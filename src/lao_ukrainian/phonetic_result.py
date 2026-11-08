from .model import PhoneticResult, PhoneticSegment

# Source IPA inventory, independent of the Ukrainian correspondence table.
# Multi-character phonemes and long vowels are single segment tokens; vowel
# sequences remain separate segments and can be combined by the target adapter.
IPA_SYMBOLS = (
    "t͡ɕ", "t͡ʃ", "t͡s", "d͡z", "d͡ʒ", "d͡ʑ", "tɕʰ", "tɕʷ", "tɕ", "dʑ", "ɲ",
    "kʷʰ", "tʷʰ", "kʷ", "ʔʷ", "sʷ", "ŋʷ", "lʷ",
    "kʰ", "pʰ", "tʰ", "nʲ", "lʲ", "rʲ", "tʲ", "dʲ",
    "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː", "ə̯",
    "k", "p", "t", "d", "b", "ŋ", "m", "n", "s", "f",
    "h", "ɡ", "g", "x", "ɦ", "r", "l", "j", "ʋ", "w", "ʔ",
    "ʃ", "ʒ", "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə",
)
VOWEL_SYMBOLS = frozenset({
    "aː", "iː", "ɯː", "uː", "eː", "ɛː", "oː", "ɔː", "ɤː", "əː",
    "a", "i", "ɯ", "u", "e", "ɛ", "o", "ɔ", "ɤ", "ə", "ə̯",
})
IPA_TONE_LETTERS = frozenset("˥˦˧˨˩")


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


def from_external_ipa(
    ipa: str,
    *,
    provenance: tuple[str, ...] = (),
) -> PhoneticResult:
    """Parse raw model IPA conservatively; unknown phones fail closed.

    Tone letters are retained as typed tone segments at their original
    positions. Their alignment to syllables is not inferred from a flat string.
    """
    import unicodedata

    raw = unicodedata.normalize("NFC", ipa).strip()
    if not raw:
        return PhoneticResult(
            None, (), (0,), status="UNSUPPORTED", provenance=provenance,
            uncertainty=("EMPTY-EXTERNAL-IPA",), external_ipa=ipa,
        )

    symbols = sorted(IPA_SYMBOLS, key=len, reverse=True)
    segments: list[PhoneticSegment] = []
    boundaries = [0]
    tone_letters: list[str] = []
    index = 0
    unsupported = False
    separators = frozenset(" .·‧")
    while index < len(raw):
        char = raw[index]
        if char in separators:
            if boundaries[-1] != len(segments):
                boundaries.append(len(segments))
            index += 1
            continue
        if char in IPA_TONE_LETTERS:
            tone_letters.append(char)
            segments.append(PhoneticSegment(char, "tone", provenance))
            index += 1
            continue
        match = next((symbol for symbol in symbols if raw.startswith(symbol, index)), None)
        if match is None:
            unsupported = True
            segments.append(PhoneticSegment(char, "unknown", provenance, "UNSUPPORTED"))
            index += 1
            continue
        kind = "vowel" if match in VOWEL_SYMBOLS else "consonant"
        segments.append(PhoneticSegment(match, kind, provenance))
        index += len(match)

    segmental_ipa = "".join(
        segment.ipa for segment in segments if segment.kind != "tone"
    )
    if not segmental_ipa:
        unsupported = True
    if boundaries[-1] != len(segments):
        boundaries.append(len(segments))
    uncertainty = ("UNSUPPORTED-EXTERNAL-IPA-SYMBOLS",) if unsupported else ()
    return PhoneticResult(
        phonemic_ipa=segmental_ipa or None,
        segments=tuple(segments),
        syllable_boundaries=tuple(boundaries),
        vowel_length="long" if "ː" in segmental_ipa else None,
        tone_category=None,
        tone_contour_ipa="".join(tone_letters) or None,
        status="UNSUPPORTED" if unsupported else "SUPPORTED",
        provenance=provenance,
        uncertainty=uncertainty,
        external_ipa=raw,
    )

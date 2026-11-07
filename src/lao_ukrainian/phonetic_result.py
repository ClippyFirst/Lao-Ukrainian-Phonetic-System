from .model import PhoneticResult, PhoneticSegment

# Source IPA inventory, independent of the Ukrainian correspondence table.
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
    """Parse raw model IPA conservatively; unknown phones fail closed."""
    import unicodedata

    raw = unicodedata.normalize("NFC", ipa).strip()
    if not raw:
        return PhoneticResult(
            None, (), (0,), status="UNSUPPORTED", provenance=provenance,
            uncertainty=("EMPTY-EXTERNAL-IPA",), external_ipa=ipa,
        )

    body = raw
    tone_contour = ""
    while body and body[-1] in IPA_TONE_LETTERS:
        tone_contour = body[-1] + tone_contour
        body = body[:-1]
    body = body.rstrip()

    symbols = sorted(IPA_SYMBOLS, key=len, reverse=True)
    segments: list[PhoneticSegment] = []
    boundaries = [0]
    index = 0
    unsupported = False
    separators = frozenset(" .·‧")
    while index < len(body):
        char = body[index]
        if char in separators:
            if boundaries[-1] != len(segments):
                boundaries.append(len(segments))
            index += 1
            continue
        match = next((symbol for symbol in symbols if body.startswith(symbol, index)), None)
        if match is None:
            unsupported = True
            segments.append(PhoneticSegment(char, "unknown", provenance, "UNSUPPORTED"))
            index += 1
            continue
        kind = "vowel" if match in VOWEL_SYMBOLS else "consonant"
        segments.append(PhoneticSegment(match, kind, provenance))
        index += len(match)

    if not segments:
        unsupported = True
    if boundaries[-1] != len(segments):
        boundaries.append(len(segments))
    segmental_ipa = "".join(segment.ipa for segment in segments)
    uncertainty = ("UNSUPPORTED-EXTERNAL-IPA-SYMBOLS",) if unsupported else ()
    return PhoneticResult(
        phonemic_ipa=segmental_ipa or None,
        segments=tuple(segments),
        syllable_boundaries=tuple(boundaries),
        vowel_length="long" if "ː" in segmental_ipa else None,
        tone_category=None,
        tone_contour_ipa=tone_contour or None,
        status="UNSUPPORTED" if unsupported else "SUPPORTED",
        provenance=provenance,
        uncertainty=uncertainty,
        external_ipa=raw,
    )

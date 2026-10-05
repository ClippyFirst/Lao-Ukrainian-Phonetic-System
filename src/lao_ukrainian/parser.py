"""Unicode-aware Lao syllable parser.

The parser is intentionally syllable-oriented rather than word-oriented:
Lao spaces separate phrases, not lexical words.  A caller may therefore pass
one syllable, a phrase with explicit spaces, or a ZWSP-delimited sequence.
The implementation recognizes the modern orthographic vowel structures listed
by Unicode and keeps ambiguous/legacy structures explicit rather than guessing.
"""
from .data import load_registry

TONE_MARKS = {"່": "mai_ek", "້": "mai_tho", "໊": "mai_ti", "໋": "mai_catawa"}
PREPOSED = {"ເ", "ແ", "ໂ", "ໃ", "ໄ"}

# Ordered from most specific to least specific.  The values are registry IDs.
# The strings are the material occurring after the onset consonant.
STRUCTURES = (
    ("pre_e_short", "ເ", "ະ", "E"),
    ("pre_e_short_kan", "ເ", "ັ", "E"),
    ("pre_e_long", "ເ", "", "EE"),
    ("pre_ae_short", "ແ", "ະ", "AE"),
    ("pre_ae_short_kan", "ແ", "ັ", "AE"),
    ("pre_ae_long", "ແ", "", "AEE"),
    ("pre_o_short", "ໂ", "ະ", "O"),
    ("pre_o_short_mai_kon", "ໂ", "ົ", "O"),
    ("pre_o_long", "ໂ", "", "OO"),
    ("pre_oe_short", "ເ", "ິ", "OE"),
    ("pre_oe_long", "ເ", "ີ", "OEE"),
    ("pre_ia_short", "ເ", "ັຽ", "IA"),
    ("pre_ia_short_nyo", "ເ", "ັຍ", "IA"),
    ("pre_ia_long", "ເ", "ຽ", "IA_LONG"),
    ("pre_ia_long_nyo", "ເ", "ຍ", "IA_LONG"),
    ("pre_ua_short", "ເ", "ຶອ", "UA"),
    ("pre_ua_long", "ເ", "ືອ", "UA_LONG"),
    ("pre_aw", "ເ", "ົາ", "AW"),
    ("pre_ai", "ໄ", "", "AI"),
    ("pre_ay", "ໃ", "", "AI"),
    ("post_a_short", "", "ະ", "A"),
    ("post_a_short_kan", "", "ັ", "A"),
    ("post_aa", "", "າ", "AA"),
    ("post_i", "", "ິ", "I"),
    ("post_ii", "", "ີ", "II"),
    ("post_y", "", "ຶ", "Y"),
    ("post_yy", "", "ື", "YY"),
    ("post_u", "", "ຸ", "U"),
    ("post_uu", "", "ູ", "UU"),
    ("post_o_long_open", "", "ໍ", "AWW"),
    ("post_am", "", "ຳ", "AM"),
    ("post_ua_short", "", "ົວະ", "UO"),
    ("post_ua_long", "", "ົວ", "UO_LONG"),
    ("post_ua_long_alt", "", "ວາ", "UO_LONG_ALT"),
    ("short_o_around", "ເ", "າະ", "AW"),
)

def segment_syllables(text: str) -> list[str]:
    """Return explicit whitespace/ZWSP chunks.

    This function deliberately does not pretend that Lao spaces are word
    boundaries.  Automatic syllable segmentation of unspaced text is a
    separate problem and is reported as such in the public documentation.
    """
    return [x for x in text.replace("\u200b", " ").split() if x]

def _strip_tone_marks(surface: str) -> str:
    return "".join(ch for ch in surface if ch not in TONE_MARKS)

def _find_onset(s: str):
    r = load_registry()["consonants"]
    # Preposed vowels occur before the onset in logical order.
    for i, ch in enumerate(s):
        if ch in r and r[ch]["status"] in {"core", "analysis-dependent"}:
            return ch, i
    return None, None

def _match_vowel(surface: str, onset_i: int, registry: dict):
    s = _strip_tone_marks(surface)
    before = s[:onset_i]
    after = s[onset_i + 1:]

    for _, pre, suffix, vowel_id in STRUCTURES:
        if before.endswith(pre) and after.startswith(suffix):
            row = next((v for v in registry["vowels"] if v["id"] == vowel_id), None)
            if row is not None:
                consumed = len(suffix)
                return row, consumed

    # Long/short ɔ and rare orthographic alternatives.
    if before.endswith("ເ") and after.startswith("ອ"):
        row = next(v for v in registry["vowels"] if v["id"] == "AW"), None
        if row:
            return row, 1

    return None, 0

def _find_coda(after_vowel: str, registry: dict):
    # Only modern Lao final consonant letters are considered here.
    finals = {g: r for g, r in registry["consonants"].items() if r.get("ipa_final")}
    for ch in reversed(after_vowel):
        if ch in finals:
            return ch
    return None

def parse_syllable(surface: str):
    registry = load_registry()
    s = _strip_tone_marks(surface)
    onset, onset_i = _find_onset(s)
    tone_mark = next((g for g in TONE_MARKS if g in surface), None)

    if onset is None:
        return {
            "surface": surface, "onset": None, "vowel": None, "coda": None,
            "tone_mark": tone_mark, "warnings": ["NO-MODERN-LAO-ONSET"]
        }

    vowel, consumed = _match_vowel(s, onset_i, registry)
    if vowel is None:
        return {
            "surface": surface, "onset": onset, "vowel": None, "coda": None,
            "tone_mark": tone_mark, "warnings": ["VOWEL-STRUCTURE-NOT-ESTABLISHED"]
        }

    after = s[onset_i + 1:]
    # Remove the vowel's orthographic suffix before looking for a coda.
    suffix = ""
    if after:
        for _, pre, candidate_suffix, vowel_id in STRUCTURES:
            if vowel_id == vowel["id"] and s[:onset_i].endswith(pre) and after.startswith(candidate_suffix):
                suffix = candidate_suffix
                break
        if vowel["id"] == "AWW" and after.startswith("ໍ"):
            suffix = "ໍ"
        elif vowel["id"] == "AM" and after.startswith("ຳ"):
            suffix = "ຳ"
        elif vowel["id"] == "AW" and after.startswith("າະ"):
            suffix = "າະ"
    remainder = after[len(suffix):]
    coda = _find_coda(remainder, registry)

    warnings = []
    if coda is None and remainder:
        # Some semivowel letters can be vowel components rather than codas;
        # preserve the material instead of silently discarding it.
        warnings.append(f"UNCONSUMED_AFTER_VOWEL:{remainder}")

    return {
        "surface": surface,
        "onset": onset,
        "vowel": vowel,
        "coda": coda,
        "tone_mark": tone_mark,
        "warnings": warnings,
    }

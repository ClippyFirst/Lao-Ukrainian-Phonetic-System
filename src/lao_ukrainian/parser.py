"""Unicode-aware Lao syllable parser.

The parser is intentionally syllable-oriented rather than word-oriented:
Lao spaces separate phrases, not lexical words. A caller may therefore pass
one syllable, a phrase with explicit spaces, or a ZWSP-delimited sequence.
"""

from .data import load_registry

TONE_MARKS = {"່": "mai_ek", "້": "mai_tho", "໊": "mai_ti", "໋": "mai_catawa"}

# The initial ຫ is silent in these combinations. It changes the tone class
# of the following low-class sonorant to high class.
HIGH_DIGRAPHS = {
    "ຫງ": "ງ",
    "ຫຍ": "ຍ",
    "ຫນ": "ນ",
    "ຫມ": "ມ",
    "ຫລ": "ລ",
    "ຫຼ": "ລ",
    "ຫວ": "ວ",
}

# Ishida's Lao Orthography Notes specifies that tone marks follow the base
# consonant (or a superscript vowel sign), and precede the spacing AM letter.
# A tone mark on the second letter of a documented onset sequence is also
# valid (e.g. ຫຍ້າ and ກວ້າງ).
VOWEL_COMBINING_MARKS = set("ັິີຶືຸູົໍ")
LABIALIZED_ONSET_BASES = set("ຖທຈກຂຄອສຊງລ")


def _tone_mark_order_warnings(surface: str, onset_i, onset_len, onset) -> list[str]:
    positions = [i for i, ch in enumerate(surface) if ch in TONE_MARKS]
    if not positions:
        return []
    if onset_i is None or onset_len is None:
        return ["MALFORMED_TONE_MARK_POSITION"]

    onset_boundary = onset_i + onset_len
    warnings = []
    for index in positions:
        after_onset = index == onset_boundary
        after_labialized_second = (
            index == onset_boundary + 1
            and surface[onset_boundary:onset_boundary + 1] == "ວ"
            and onset in LABIALIZED_ONSET_BASES
        )
        after_combining_vowel = index > 0 and surface[index - 1] in VOWEL_COMBINING_MARKS
        if any(ch in VOWEL_COMBINING_MARKS for ch in surface[index + 1:]):
            warnings.append("MALFORMED_TONE_MARK_ORDER")
        elif not (after_onset or after_labialized_second or after_combining_vowel):
            warnings.append("MALFORMED_TONE_MARK_POSITION")
    return list(dict.fromkeys(warnings))

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
    # Source-indexed spelling distinctions from Ishida (2026): ເ◌ັຽ and ເ◌ຍ
    # represent long /iːə̯/, while ເ◌ັຍ represents short /iə̯/.
    # ເ◌ຽ is not listed as a preposed IA spelling and must not be promoted
    # to a deterministic long-diphthong parse.
    ("pre_ia_long_iae", "ເ", "ັຽ", "IA_LONG"),
    ("pre_ia_short_nyo", "ເ", "ັຍ", "IA"),
    ("pre_ia_long_nyo", "ເ", "ຍ", "IA_LONG"),
    ("pre_ua_short", "ເ", "ຶອ", "UA"),
    ("pre_ua_long", "ເ", "ືອ", "UA_LONG"),
    ("pre_aw", "ເ", "ົາ", "AW_LONG"),
    ("pre_ai", "ໄ", "", "AI"),
    ("pre_ay", "ໃ", "", "AI2"),
    ("post_a_short", "", "ະ", "A"),
    ("post_a_short_kan", "", "ັ", "A2"),
    ("post_aa", "", "າ", "AA"),
    ("post_i", "", "ິ", "I"),
    ("post_ii", "", "ີ", "II"),
    ("post_o_short_closed", "", "ົ", "O"),
    ("post_y", "", "ຶ", "Y"),
    ("post_yy", "", "ື", "YY"),
    ("post_u", "", "ຸ", "U"),
    ("post_uu", "", "ູ", "UU"),
    ("post_o_short_alt", "", "ັອ", "AWW_SHORT_ALT"),
    ("post_o_long_medial", "", "ອ", "AWW_MEDIAL"),
    ("post_o_long_open", "", "ໍ", "AWW"),
    ("post_am", "", "ຳ", "AM"),
    ("post_ua_short_alt", "", "ັວ", "UO_SHORT_ALT"),
    ("post_ua_short", "", "ົວະ", "UO"),
    ("post_ua_long", "", "ົວ", "UO_LONG"),
    ("post_ua_long_closed_alt", "", "ວ", "UO_LONG_ALT"),
    ("post_ua_long_open_alt", "", "ວາ", "UO_LONG_OPEN"),
    ("post_ia_long_standalone", "", "ຽ", "IA_LONG"),
    ("short_o_around", "ເ", "າະ", "AW"),
)

def segment_syllables(text: str) -> list[str]:
    return [x for x in text.replace("\u200b", " ").split() if x]

def _strip_tone_marks(surface: str) -> str:
    return "".join(ch for ch in surface if ch not in TONE_MARKS)

def _find_onset(s: str):
    r = load_registry()["consonants"]
    for form, target in sorted(HIGH_DIGRAPHS.items(), key=lambda x: len(x[0]), reverse=True):
        if s.startswith(form):
            return target, 0, len(form), "high", form
    for i, ch in enumerate(s):
        if ch in r and r[ch]["status"] in {"core", "analysis-dependent"}:
            return ch, i, 1, r[ch]["class"], ch
    return None, None, None, None, None

def _match_vowel(surface: str, onset_i: int, onset_len: int, registry: dict):
    s = _strip_tone_marks(surface)
    before = s[:onset_i]
    after = s[onset_i + onset_len:]
    # Match specific orthographic vowel complexes before generic patterns
    # with an empty suffix (e.g. ເ◌, ແ◌, ໂ◌). Otherwise the generic
    # preposed-vowel rule can shadow ເ◌ິ, ເ◌ີ, and ເ◌ຽ.
    for _, pre, suffix, vowel_id in sorted(
        STRUCTURES, key=lambda item: (len(item[2]), len(item[1])), reverse=True
    ):
        if before == pre and after.startswith(suffix):
            return next((v for v in registry["vowels"] if v["id"] == vowel_id), None)
    return None

def _find_coda(after_vowel: str, registry: dict):
    finals = {g: r for g, r in registry["consonants"].items() if r.get("ipa_final")}
    # A coda must be the final grapheme of the remaining syllable material.
    # Searching backward for any legal final can incorrectly accept e.g.
    # ກາງະ as /kaːŋ/ while silently ignoring the trailing vowel sign.
    # A legal final is a coda only when it is the sole remaining grapheme.
    # Merely ending in a legal final must not hide preceding unconsumed material.
    if len(after_vowel) == 1 and after_vowel in finals:
        return after_vowel
    return None

def parse_syllable(surface: str):
    registry = load_registry()
    s = _strip_tone_marks(surface)
    onset, onset_i, onset_len, onset_class, onset_form = _find_onset(s)
    tone_mark = next((g for g in TONE_MARKS if g in surface), None)
    tone_warnings = ["MULTIPLE_TONE_MARKS"] if sum(ch in TONE_MARKS for ch in surface) > 1 else []
    tone_warnings.extend(_tone_mark_order_warnings(surface, onset_i, onset_len, onset))

    if onset is None:
        return {"surface": surface, "onset": None, "vowel": None, "coda": None,
                "tone_mark": tone_mark, "warnings": ["NO-MODERN-LAO-ONSET", *tone_warnings]}

    before = s[:onset_i]
    allowed_preposed = {"", "ເ", "ແ", "ໂ", "ໃ", "ໄ"}
    if before not in allowed_preposed:
        return {"surface": surface, "onset": onset, "onset_class": onset_class,
                "onset_form": onset_form, "vowel": None, "coda": None,
                "tone_mark": tone_mark,
                "warnings": [f"UNCONSUMED_BEFORE_ONSET:{before}", *tone_warnings]}

    vowel = _match_vowel(s, onset_i, onset_len, registry)
    if vowel is None:
        return {"surface": surface, "onset": onset, "onset_class": onset_class,
                "onset_form": onset_form, "vowel": None, "coda": None,
                "tone_mark": tone_mark, "warnings": ["VOWEL-STRUCTURE-NOT-ESTABLISHED", *tone_warnings]}

    after = s[onset_i + onset_len:]
    suffix = ""
    for _, pre, candidate_suffix, vowel_id in STRUCTURES:
        if vowel_id == vowel["id"] and s[:onset_i] == pre and after.startswith(candidate_suffix):
            suffix = candidate_suffix
            break
    remainder = after[len(suffix):]
    coda = _find_coda(remainder, registry)
    warnings = list(tone_warnings)
    if coda is None and remainder:
        warnings.append(f"UNCONSUMED_AFTER_VOWEL:{remainder}")
    if coda is None and vowel["id"] in {"A2", "AWW_SHORT_ALT"}:
        warnings.append(f"SHORT_VOWEL_REQUIRES_CODA:{vowel['id']}")

    return {"surface": surface, "onset": onset, "onset_class": onset_class,
            "onset_form": onset_form, "vowel": vowel, "coda": coda,
            "tone_mark": tone_mark, "warnings": warnings}

"""Unicode-aware Lao syllable parser.

The parser is intentionally syllable-oriented rather than word-oriented:
Lao spaces separate phrases, not lexical words. A caller may therefore pass
one syllable, a phrase with explicit spaces, or a ZWSP-delimited sequence.
"""

from .data import load_registry
from .normalize import PASSTHROUGH_CHARACTERS

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


def _tone_mark_order_warnings(surface: str, onset_i, onset_len, onset, registry: dict | None = None) -> list[str]:
    positions = [i for i, ch in enumerate(surface) if ch in TONE_MARKS]
    if not positions:
        return []
    if onset_i is None or onset_len is None:
        return ["MALFORMED_TONE_MARK_POSITION"]

    onset_boundary = onset_i + onset_len
    labialized_bases = {row["base"] for row in (registry or load_registry())["onset_clusters"].values()}
    warnings = []
    for index in positions:
        after_onset = index == onset_boundary
        after_labialized_second = (
            index == onset_boundary + 1
            and surface[onset_boundary:onset_boundary + 1] == "ວ"
            and onset in labialized_bases
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

def segment_syllables(text: str, registry: dict | None = None) -> list[str]:
    """Split phrase-separated Lao into structurally parsed syllables.

    Lao spaces are phrase boundaries, not dependable word/syllable boundaries.
    This deterministic dynamic program identifies complete orthographic
    syllables first, then lets the phonology layer derive IPA and tone. It
    never discards unparsed code points; unsupported material remains visible.
    """
    registry = registry or load_registry()
    words = text.replace("\u200b", " ").split()
    return [part for word in words for part in _segment_word(word, registry)]


def _segment_word(word: str, registry: dict) -> list[str]:
    chars = list(word)
    if not chars:
        return []

    whole = parse_syllable(word, registry)
    warnings = whole.get("warnings", [])
    if whole.get("vowel") is not None and not warnings:
        return [word]

    # Do not salvage a plausible prefix from known ambiguous or malformed
    # orthographic units.
    if any(
        warning in {
            "AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY",
            "LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL",
        }
        for warning in warnings
    ):
        return [word]
    unconsumed_before = next(
        (warning.split(":", 1)[1] for warning in warnings
         if warning.startswith("UNCONSUMED_BEFORE_ONSET:")),
        "",
    )
    if unconsumed_before and any(ch not in PASSTHROUGH_CHARACTERS for ch in unconsumed_before):
        return [word]

    onset = whole.get("onset")
    onset_form = whole.get("onset_form")
    if onset_form and onset_form != onset and onset_form not in HIGH_DIGRAPHS:
        return [word]

    # ເ + onset + ຽ is not an established preposed IA spelling.
    clean = _strip_tone_marks(word)
    found_onset = _find_onset(clean, registry)
    if found_onset:
        _, onset_index, onset_length, *_ = found_onset
        if onset_index is not None and onset_length is not None and clean[:onset_index] == "ເ" and clean[onset_index + onset_length:] == "ຽ":
            return [word]

    # Prefer complete syllables, but retain every unparsed code point as a
    # visible one-character unit with a strong fallback penalty. The coda
    # penalty resolves CVC|CV boundaries when a vowel sign follows the next
    # consonant.
    n = len(chars)
    best: list[tuple[int, list[str]] | None] = [None] * (n + 1)
    best[n] = (0, [])
    next_syllable_vowel_signs = set("ະັິີຶືຸູ")

    for i in range(n - 1, -1, -1):
        tail = best[i + 1]
        assert tail is not None
        best[i] = (tail[0] - 100, [chars[i], *tail[1]])

        for j in range(i + 1, min(n, i + 12) + 1):
            candidate_text = "".join(chars[i:j])
            parsed = parse_syllable(candidate_text, registry)
            if parsed.get("vowel") is None or parsed.get("warnings"):
                continue
            following = chars[j] if j < n else ""
            coda_starts_next = bool(parsed.get("coda") and following in next_syllable_vowel_signs)
            suffix = best[j]
            assert suffix is not None
            score = suffix[0] + (j - i) - (3 if coda_starts_next else 0)
            parts = [candidate_text, *suffix[1]]
            current = best[i]
            assert current is not None
            if score > current[0] or (score == current[0] and len(parts) < len(current[1])):
                best[i] = (score, parts)

    result = best[0]
    assert result is not None
    parts = result[1]
    # Tone marks are validated by each candidate syllable, not by the whole
    # space-delimited word. If a mark cannot be consumed by a complete
    # syllable, retain the whole orthographic unit rather than dropping it.
    if any(part in TONE_MARKS for part in parts):
        return [word]
    # A2 short vowels may be legal inside a closed syllable even when the
    # whole word's first-pass parse cannot see that coda. Validate the coda
    # on each candidate syllable; if DP leaves a core Lao consonant or vowel
    # sign stranded, keep the original token unresolved.
    vowel_graphemes = set("ະາຽຳເແໂໃໄວອຍ") | VOWEL_COMBINING_MARKS
    if any(
        len(part) == 1 and (
            part in vowel_graphemes
            or (
                part in registry["consonants"]
                and registry["consonants"][part].get("status") in {"core", "analysis-dependent"}
            )
        )
        for part in parts
    ):
        return [word]
    return parts

def _strip_tone_marks(surface: str) -> str:
    return "".join(ch for ch in surface if ch not in TONE_MARKS)

def _find_onset(s: str, registry: dict | None = None):
    registry = registry or load_registry()
    consonants = registry["consonants"]
    # Search after a preposed vowel as well as at index zero. In Lao, a
    # pre-base vowel is stored before the complete onset, including ຫ digraphs.
    for i, ch in enumerate(s):
        for form, target in sorted(HIGH_DIGRAPHS.items(), key=lambda x: len(x[0]), reverse=True):
            if s.startswith(form, i):
                return target, i, len(form), "high", form, None
        if ch in consonants and consonants[ch]["status"] in {"core", "analysis-dependent"}:
            return ch, i, 1, consonants[ch]["class"], ch, None
    return None, None, None, None, None, None


def _vowel_candidate(s: str, onset_i: int, onset_len: int, registry: dict):
    vowel = _match_vowel(s, onset_i, onset_len, registry)
    if vowel is None:
        return None
    after = s[onset_i + onset_len:]
    suffix = ""
    for _, pre, candidate_suffix, vowel_id in STRUCTURES:
        if vowel_id == vowel["id"] and s[:onset_i] == pre and after.startswith(candidate_suffix):
            suffix = candidate_suffix
            break
    remainder = after[len(suffix):]
    coda = _find_coda(remainder, registry)
    warnings = []
    if coda is None and remainder:
        warnings.append(f"UNCONSUMED_AFTER_VOWEL:{remainder}")
    if coda is None and vowel["id"] in {"A2", "AWW_SHORT_ALT"}:
        warnings.append(f"SHORT_VOWEL_REQUIRES_CODA:{vowel['id']}")
    return {"vowel": vowel, "coda": coda, "warnings": warnings,
            "complete": not warnings, "remainder": remainder}

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

def parse_syllable(surface: str, registry: dict | None = None):
    registry = registry or load_registry()
    s = _strip_tone_marks(surface)
    onset, onset_i, onset_len, onset_class, onset_form, onset_ipa = _find_onset(s, registry)
    tone_mark = next((g for g in TONE_MARKS if g in surface), None)
    multiple_tone_marks = sum(ch in TONE_MARKS for ch in surface) > 1

    def mark_warnings(index, length, base):
        warnings = ["MULTIPLE_TONE_MARKS"] if multiple_tone_marks else []
        warnings.extend(_tone_mark_order_warnings(surface, index, length, base, registry))
        return warnings

    if onset is None:
        tone_warnings = mark_warnings(onset_i, onset_len, onset)
        return {"surface": surface, "onset": None, "vowel": None, "coda": None,
                "tone_mark": tone_mark, "warnings": ["NO-MODERN-LAO-ONSET", *tone_warnings]}

    before = s[:onset_i]
    allowed_preposed = {"", "ເ", "ແ", "ໂ", "ໃ", "ໄ"}
    if before not in allowed_preposed:
        tone_warnings = mark_warnings(onset_i, onset_len, onset)
        return {"surface": surface, "onset": onset, "onset_class": onset_class,
                "onset_form": onset_form, "onset_ipa": onset_ipa,
                "vowel": None, "coda": None, "tone_mark": tone_mark,
                "warnings": [f"UNCONSUMED_BEFORE_ONSET:{before}", *tone_warnings]}

    base_candidate = _vowel_candidate(s, onset_i, onset_len, registry)
    selected = base_candidate
    cluster_row = registry["onset_clusters"].get(s[onset_i:onset_i + 2]) if onset_len == 1 else None

    if cluster_row:
        cluster_candidate = _vowel_candidate(s, onset_i, 2, registry)
        rounded_vowels = ("u", "o", "ɔ")
        cluster_is_rounded = bool(
            cluster_candidate and cluster_candidate["vowel"]["ipa"].startswith(rounded_vowels)
        )
        base_complete = bool(base_candidate and base_candidate["complete"])
        cluster_complete = bool(cluster_candidate and cluster_candidate["complete"])

        if cluster_is_rounded:
            if not base_complete:
                tone_warnings = mark_warnings(onset_i, 2, onset)
                return {"surface": surface, "onset": onset, "onset_class": onset_class,
                        "onset_form": cluster_row["grapheme"], "onset_ipa": None,
                        "vowel": None, "coda": None, "tone_mark": tone_mark,
                        "warnings": ["LABIALIZED_ONSET_BEFORE_ROUNDED_VOWEL", *tone_warnings]}
        elif base_complete and cluster_complete:
            tone_warnings = mark_warnings(onset_i, 2, onset)
            return {"surface": surface, "onset": onset, "onset_class": onset_class,
                    "onset_form": cluster_row["grapheme"], "onset_ipa": None,
                    "vowel": None, "coda": None, "tone_mark": tone_mark,
                    "warnings": ["AMBIGUOUS_LABIALIZED_ONSET_VOWEL_BOUNDARY", *tone_warnings]}
        elif cluster_complete or (cluster_candidate and not base_candidate):
            selected = cluster_candidate
            onset_len = 2
            onset_form = cluster_row["grapheme"]
            onset_ipa = cluster_row["ipa_initial"]
            onset_class = cluster_row["class"]
        elif base_candidate is None and cluster_candidate is not None:
            selected = cluster_candidate
            onset_len = 2
            onset_form = cluster_row["grapheme"]
            onset_ipa = cluster_row["ipa_initial"]
            onset_class = cluster_row["class"]

    if selected is None:
        tone_warnings = mark_warnings(onset_i, onset_len, onset)
        return {"surface": surface, "onset": onset, "onset_class": onset_class,
                "onset_form": onset_form, "onset_ipa": onset_ipa,
                "vowel": None, "coda": None, "tone_mark": tone_mark,
                "warnings": ["VOWEL-STRUCTURE-NOT-ESTABLISHED", *tone_warnings]}

    tone_warnings = mark_warnings(onset_i, onset_len, onset)
    warnings = [*tone_warnings, *selected["warnings"]]
    return {"surface": surface, "onset": onset, "onset_class": onset_class,
            "onset_form": onset_form, "onset_ipa": onset_ipa,
            "vowel": selected["vowel"], "coda": selected["coda"],
            "tone_mark": tone_mark, "warnings": warnings}

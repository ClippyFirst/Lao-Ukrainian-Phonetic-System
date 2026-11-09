"""Non-authoritative lexical-boundary hints from attributed orthographic word lists.

This module is separate from syllable parsing and G2P. A match means only
that a contiguous syllable span occurs in a word-wrapping list. Overlapping
matches are retained; callers must not treat them as resolved word boundaries
or pronunciation evidence.
"""
from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Iterable, Sequence


def load_orthographic_hint_entries(path: str | Path) -> tuple[str, ...]:
    """Load non-empty, non-comment orthographic entries from a UTF-8 list."""
    entries: list[str] = []
    seen: set[str] = set()
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        value = unicodedata.normalize("NFC", raw.strip())
        if not value or value.startswith("#") or value in seen:
            continue
        seen.add(value)
        entries.append(value)
    return tuple(entries)


def find_orthographic_word_hints(
    syllables: Sequence[str],
    lexicon: Iterable[str],
    *,
    min_syllables: int = 2,
) -> list[dict[str, object]]:
    """Return every matching multi-syllable span; never choose a segmentation.

    Offsets are zero-based, end-exclusive indices into syllables. Results
    intentionally retain overlaps and alternatives because the source list
    was made for line wrapping, not validated lexical word segmentation.
    """
    if min_syllables < 1:
        raise ValueError("min_syllables must be at least 1")
    units = tuple(unicodedata.normalize("NFC", item) for item in syllables)
    entries = {
        unicodedata.normalize("NFC", item.strip())
        for item in lexicon
        if item and item.strip() and not item.lstrip().startswith("#")
    }
    matches: list[dict[str, object]] = []
    for start in range(len(units)):
        joined = ""
        for end in range(start + 1, len(units) + 1):
            joined += units[end - 1]
            count = end - start
            if count >= min_syllables and joined in entries:
                matches.append({
                    "start_syllable": start,
                    "end_syllable": end,
                    "surface": joined,
                    "syllable_count": count,
                    "evidence": "ORTHOGRAPHIC_WORDLIST_MATCH",
                    "authority": "SOFT_HINT_ONLY",
                })
    return matches

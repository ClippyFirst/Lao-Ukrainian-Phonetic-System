"""Evidence-limited candidate lattice for Lao orthographic syllable boundaries.

This module enumerates complete syllable candidates using the repository's
existing single-syllable recognizer. It does not choose a pronunciation,
resolve lexical ambiguity, model shared coda/onset graphemes, or replace the
legacy segment_syllables() heuristic.
"""
from __future__ import annotations

import unicodedata
from collections import defaultdict
from typing import Any, Callable

from .data import load_registry
from .parser import parse_syllable

CandidateParser = Callable[[str, dict[str, Any]], dict[str, Any]]


def _build_candidate_lattice(
    word: str,
    candidate_parser: CandidateParser,
    registry: dict[str, Any],
) -> dict[str, Any]:
    """Build a pruned offset DAG; parser injection keeps graph logic testable."""
    size = len(word)
    candidates: list[dict[str, Any]] = []
    by_start: dict[int, list[dict[str, Any]]] = defaultdict(list)

    # Enumerate every non-empty code-point span. Offsets refer to the NFC
    # Python string supplied by the caller, not grapheme-cluster indices.
    for start in range(size):
        for end in range(start + 1, size + 1):
            surface = word[start:end]
            parsed = candidate_parser(surface, registry)
            vowel = parsed.get("vowel")
            warnings = parsed.get("warnings") or []
            if vowel is None or warnings:
                continue
            vowel_id = vowel.get("id") if isinstance(vowel, dict) else vowel
            edge = {
                "start": start,
                "end": end,
                "surface": surface,
                "onset": parsed.get("onset"),
                "onset_form": parsed.get("onset_form"),
                "vowel": vowel_id,
                "coda": parsed.get("coda"),
                "tone_mark": parsed.get("tone_mark"),
            }
            candidates.append(edge)
            by_start[start].append(edge)

    # Forward reachability: can this vertex be reached from the start?
    reachable = {0}
    for offset in range(size):
        if offset in reachable:
            reachable.update(edge["end"] for edge in by_start.get(offset, []))

    # Backward reachability: can this vertex reach the end?
    can_reach_end = {size}
    for offset in range(size - 1, -1, -1):
        if any(edge["end"] in can_reach_end for edge in by_start.get(offset, [])):
            can_reach_end.add(offset)

    live = [
        edge for edge in candidates
        if edge["start"] in reachable and edge["end"] in can_reach_end
    ]
    live_ids = {(edge["start"], edge["end"], edge["surface"]) for edge in live}
    dead = [
        edge for edge in candidates
        if (edge["start"], edge["end"], edge["surface"]) not in live_ids
    ]

    # Exact DAG path counts support convergence-point detection. We expose
    # only a 0/1/many classification, never enumerate the paths themselves.
    paths_to_end = [0] * (size + 1)
    paths_to_end[size] = 1
    for offset in range(size - 1, -1, -1):
        paths_to_end[offset] = sum(
            paths_to_end[edge["end"]] for edge in by_start.get(offset, [])
        )

    paths_from_start = [0] * (size + 1)
    paths_from_start[0] = 1
    for offset in range(size):
        for edge in by_start.get(offset, []):
            paths_from_start[edge["end"]] += paths_from_start[offset]

    total_paths = paths_to_end[0]
    path_count_capped = min(2, total_paths)
    convergence_offsets = [
        offset for offset in range(size + 1)
        if total_paths > 0
        and paths_from_start[offset] * paths_to_end[offset] == total_paths
    ]

    # An ambiguity eye is the subgraph between consecutive convergence
    # points when more than one complete local path connects them.
    ambiguity_eyes = []
    for left, right in zip(convergence_offsets, convergence_offsets[1:]):
        local_paths = [0] * (right + 1)
        local_paths[right] = 1
        for offset in range(right - 1, left - 1, -1):
            local_paths[offset] = sum(
                local_paths[edge["end"]]
                for edge in by_start.get(offset, [])
                if edge["end"] <= right
            )
        if local_paths[left] <= 1:
            continue

        local_reachable = {left}
        for offset in range(left, right):
            if offset in local_reachable:
                local_reachable.update(
                    edge["end"] for edge in by_start.get(offset, [])
                    if edge["end"] <= right
                )
        local_can_reach = {right}
        for offset in range(right - 1, left - 1, -1):
            if any(
                edge["end"] in local_can_reach
                for edge in by_start.get(offset, [])
                if edge["end"] <= right
            ):
                local_can_reach.add(offset)
        eye_edges = [
            edge for edge in candidates
            if left <= edge["start"] < edge["end"] <= right
            and edge["start"] in local_reachable
            and edge["end"] in local_can_reach
        ]
        ambiguity_eyes.append({
            "start": left,
            "end": right,
            "surface": word[left:right],
            "complete_path_count_capped": min(2, local_paths[left]),
            "candidate_count": len(eye_edges),
            "candidates": eye_edges,
        })

    unique_path = None
    if total_paths == 1:
        unique_path = []
        offset = 0
        while offset < size:
            next_edges = [
                edge for edge in by_start.get(offset, [])
                if paths_to_end[edge["end"]] > 0
            ]
            if len(next_edges) != 1:
                # Defensive invariant: a unique path must have one live edge
                # at each visited vertex.
                unique_path = None
                break
            edge = next_edges[0]
            unique_path.append(edge)
            offset = edge["end"]

    status = (
        "NO_COMPLETE_PATH" if total_paths == 0
        else "UNIQUE" if total_paths == 1
        else "AMBIGUOUS"
    )
    return {
        "text": word,
        "offset_unit": "NFC Python Unicode code points",
        "status": status,
        "complete_path_count_capped": path_count_capped,
        "convergence_offsets": convergence_offsets,
        "ambiguity_eyes": ambiguity_eyes,
        "candidate_count": len(candidates),
        "live_candidate_count": len(live),
        "dead_candidate_count": len(dead),
        "live_candidates": live,
        "dead_candidates": dead,
        "unique_path": unique_path,
        "limitations": [
            "Uses the current single-syllable recognizer; it is not a complete Lao orthographic grammar.",
            "Does not model one grapheme serving overlapping coda and onset roles.",
            "Does not resolve lexical, loanword, dialect, or pronunciation ambiguity.",
            "A unique path is unique only within the current recognizer and candidate inventory.",
            "Convergence points and ambiguity eyes are structural graph properties, not lexical or phonological resolutions.",
        ],
    }


def analyze_orthographic_word(word: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return all complete syllable-boundary analyses for one NFC Lao token.

    Whitespace and zero-width-space boundaries must be handled by the caller.
    The function preserves the supplied text and never normalizes it silently.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")
    if any(character.isspace() for character in word) or "\u200b" in word:
        raise ValueError("pass one whitespace-delimited token at a time")
    if not unicodedata.is_normalized("NFC", word):
        raise ValueError("word must be NFC-normalized; offsets refer to supplied code points")
    return _build_candidate_lattice(word, parse_syllable, registry or load_registry())

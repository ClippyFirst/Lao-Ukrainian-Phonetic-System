#!/usr/bin/env python3
"""Compare simple ICU Lao word-list baselines with an aligned segmented corpus.

This is an offline research utility. It does not implement ALA-LC Note 9 and
must not be used as a production Lao segmenter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

LAO_START = 0x0E80
LAO_END = 0x0EFF


def git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}".encode("ascii") + bytes([0])
    return hashlib.sha1(header + raw).hexdigest()


def read_verified(path: Path, expected_blob_sha1: str | None = None) -> tuple[str, str]:
    raw = path.read_bytes()
    digest = git_blob_sha1(raw)
    if expected_blob_sha1 and digest.lower() != expected_blob_sha1.lower():
        raise ValueError(
            f"Git blob SHA-1 mismatch for {path}: expected "
            f"{expected_blob_sha1}, got {digest}"
        )
    return raw.decode("utf-8-sig"), digest


def is_lao_character(character: str) -> bool:
    value = ord(character)
    return LAO_START <= value <= LAO_END


def load_dictionary(text: str) -> tuple[set[str], int]:
    entries = [
        unicodedata.normalize("NFC", line.strip())
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    words = set(entries)
    if not words:
        raise ValueError("dictionary contains no entries")
    return words, max(len(word) for word in words)


def greedy_segment(
    run: str, words: set[str], max_word_length: int, strategy: str
) -> list[str]:
    """Greedy prefix baseline; unknown characters fall back one code point."""
    if strategy not in {"longest", "shortest"}:
        raise ValueError(f"unsupported strategy: {strategy}")
    characters = list(unicodedata.normalize("NFC", run))
    result: list[str] = []
    position = 0
    while position < len(characters):
        limit = min(max_word_length, len(characters) - position)
        lengths = range(limit, 0, -1) if strategy == "longest" else range(1, limit + 1)
        match_length = next(
            (
                length
                for length in lengths
                if "".join(characters[position : position + length]) in words
            ),
            1,
        )
        result.append("".join(characters[position : position + match_length]))
        position += match_length
    return result


def score_strategy(
    raw_lines: list[str],
    segmented_lines: list[str],
    words: set[str],
    max_word_length: int,
    strategy: str,
) -> dict:
    true_positive = false_positive = false_negative = 0
    boundary_positions = aligned_sentences = unaligned_sentences = 0

    for raw_line, segmented_line in zip(raw_lines, segmented_lines):
        source = [
            character
            for character in unicodedata.normalize("NFC", raw_line)
            if not character.isspace()
        ]
        gold_tokens = [
            unicodedata.normalize("NFC", token)
            for token in segmented_line.split()
        ]
        gold_characters = list("".join(gold_tokens))
        if source != gold_characters:
            unaligned_sentences += 1
            continue
        aligned_sentences += 1

        gold_boundaries: set[int] = set()
        offset = 0
        for token in gold_tokens:
            offset += len(token)
            gold_boundaries.add(offset)

        predicted_boundaries: set[int] = set()
        position = 0
        while position < len(source):
            if not is_lao_character(source[position]):
                position += 1
                continue
            run_end = position
            while run_end < len(source) and is_lao_character(source[run_end]):
                run_end += 1
            run = "".join(source[position:run_end])
            local_offset = 0
            for token in greedy_segment(run, words, max_word_length, strategy):
                local_offset += len(token)
                predicted_boundaries.add(position + local_offset)
            position = run_end

        for boundary in range(1, len(source)):
            if not (
                is_lao_character(source[boundary - 1])
                and is_lao_character(source[boundary])
            ):
                continue
            boundary_positions += 1
            is_gold = boundary in gold_boundaries
            is_predicted = boundary in predicted_boundaries
            if is_gold and is_predicted:
                true_positive += 1
            elif is_predicted:
                false_positive += 1
            elif is_gold:
                false_negative += 1

    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    precision = (
        true_positive / precision_denominator if precision_denominator else 0.0
    )
    recall = true_positive / recall_denominator if recall_denominator else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {
        "strategy": strategy,
        "aligned_sentences": aligned_sentences,
        "unaligned_sentences": unaligned_sentences,
        "within_lao_boundary_positions": boundary_positions,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "precision": round(precision, 8),
        "recall": round(recall, 8),
        "f1": round(f1, 8),
    }


def benchmark(
    raw_text: str,
    segmented_text: str,
    dictionary_text: str,
    input_hashes: dict[str, str] | None = None,
) -> dict:
    raw_lines = raw_text.splitlines()
    segmented_lines = segmented_text.splitlines()
    if len(raw_lines) != len(segmented_lines):
        raise ValueError(
            "raw and segmented files must have the same number of lines "
            f"({len(raw_lines)} != {len(segmented_lines)})"
        )

    words, max_word_length = load_dictionary(dictionary_text)
    return {
        "scope": "exploratory lexical-boundary baseline; not ALA-LC Note 9",
        "input_sentence_pairs": len(raw_lines),
        "dictionary_entries": len(words),
        "max_dictionary_word_codepoints": max_word_length,
        "input_git_blob_sha1": input_hashes or {},
        "results": [
            score_strategy(raw_lines, segmented_lines, words, max_word_length, strategy)
            for strategy in ("longest", "shortest")
        ],
        "limitations": [
            "Only sentence pairs with exact character-stream alignment after NFC and whitespace removal are scored.",
            "Only boundaries between adjacent Lao-block code points are scored; punctuation and mixed-script boundaries are excluded.",
            "Unknown Lao characters fall back to one code point.",
            "Greedy longest/shortest prefix matching is not the LOC shortest-written-form-that-can-stand-alone rule.",
            "The external corpus is not included; verify source-item rights before redistributing any corpus text.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True, help="raw Lao sentence file")
    parser.add_argument(
        "--segmented", type=Path, required=True, help="gold segmented sentence file"
    )
    parser.add_argument(
        "--dictionary", type=Path, required=True, help="ICU laodict.txt word list"
    )
    parser.add_argument("--raw-blob-sha1", help="optional expected Git blob SHA-1")
    parser.add_argument("--segmented-blob-sha1", help="optional expected Git blob SHA-1")
    parser.add_argument("--dictionary-blob-sha1", help="optional expected Git blob SHA-1")
    args = parser.parse_args(argv)

    try:
        raw_text, raw_hash = read_verified(args.raw, args.raw_blob_sha1)
        segmented_text, segmented_hash = read_verified(
            args.segmented, args.segmented_blob_sha1
        )
        dictionary_text, dictionary_hash = read_verified(
            args.dictionary, args.dictionary_blob_sha1
        )
        report = benchmark(
            raw_text,
            segmented_text,
            dictionary_text,
            {
                "raw": raw_hash,
                "segmented": segmented_hash,
                "dictionary": dictionary_hash,
            },
        )
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

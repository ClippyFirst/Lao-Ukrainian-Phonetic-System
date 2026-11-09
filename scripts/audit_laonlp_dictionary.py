#!/usr/bin/env python3
"""Audit a pinned LaoNLP lexical CSV without importing it into the runtime."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from collections import Counter
from pathlib import Path

EXPECTED_HEADER = ["ID", "LaoWord", "English", "Pronunciation", "Type"]
UPSTREAM_COMMIT = "a914f64e38ff24d67d32e37db40dad5c368ea602"
UPSTREAM_BLOB_SHA1 = "ded14c7770becfd5c6946c6c1ce75a7dfc4d564c"


def audit_file(path: Path, expected_sha1: str | None = None) -> dict:
    raw = path.read_bytes()
    digest = hashlib.sha1(raw).hexdigest()
    git_blob_prefix = f"blob {len(raw)}".encode("ascii") + bytes([0])
    git_blob_digest = hashlib.sha1(git_blob_prefix + raw).hexdigest()
    if expected_sha1 and git_blob_digest.lower() != expected_sha1.lower():
        raise ValueError(f"Git blob SHA-1 mismatch: expected {expected_sha1}, got {git_blob_digest}")

    text = raw.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text, newline=""))
    header = next(reader, None)
    if header != EXPECTED_HEADER:
        raise ValueError(f"unexpected CSV header: {header!r}")

    total_rows = 0
    exact_repeated_headers = 0
    malformed_header_like_rows = 0
    placeholder_rows = 0
    malformed_width_rows = 0
    missing_pronunciation = 0
    blank_type = 0
    words: Counter[str] = Counter()

    for row in reader:
        total_rows += 1
        if len(row) != len(EXPECTED_HEADER):
            malformed_width_rows += 1
            continue
        # Historical copies of the header occur mid-file. Some have a blank
        # LaoWord cell or the misspelling "Pronuciation"; Type=Type is stable.
        if row[4].strip() == "Type":
            if row[1:] == EXPECTED_HEADER[1:]:
                exact_repeated_headers += 1
            else:
                malformed_header_like_rows += 1
            continue
        if all(not cell.strip() for cell in row[1:]):
            placeholder_rows += 1
            continue

        word = row[1].strip()
        if word:
            words[word] += 1
        if not row[3].strip():
            missing_pronunciation += 1
        if not row[4].strip():
            blank_type += 1

    counts = list(words.values())
    header_like_rows = exact_repeated_headers + malformed_header_like_rows
    usable_records = total_rows - header_like_rows - placeholder_rows - malformed_width_rows
    return {
        "upstream_commit": UPSTREAM_COMMIT,
        "upstream_blob_sha1": UPSTREAM_BLOB_SHA1,
        "file_sha1": digest,
        "git_blob_sha1": git_blob_digest,
        "header": header,
        "rows_after_first_header": total_rows,
        "repeated_header_rows": exact_repeated_headers,
        "malformed_header_like_rows": malformed_header_like_rows,
        "header_like_rows_total": header_like_rows,
        "id_only_placeholder_rows": placeholder_rows,
        "usable_records": usable_records,
        "unique_lao_words": len(words),
        "forms_with_multiple_records": sum(count > 1 for count in counts),
        "usable_rows_missing_pronunciation": missing_pronunciation,
        "usable_rows_with_blank_type": blank_type,
        "malformed_width_rows": malformed_width_rows,
        "pronunciation_field_interpretation": "Latin-script romanization; not IPA",
        "runtime_imported": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="local copy of lao-eng-dictionary.csv")
    parser.add_argument(
        "--expected-sha1",
        help="fail unless the file matches this SHA-1 (recommended for the pinned upstream snapshot)",
    )
    args = parser.parse_args(argv)
    try:
        result = audit_file(args.csv_path, args.expected_sha1)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compare Lao G2P engines on the MekongPhon held-out lexicon.

Segmental IPA and tonal IPA are scored separately. This matters because
ClippyFirst preserves tone contours as typed metadata rather than appending
them to its segmental phonemic_ipa string.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
from collections import Counter
import importlib.metadata
import json
import os
import platform
import statistics
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

try:
    from scripts.benchmark_ipa_contract import accepted_phonetic_ipa
except ModuleNotFoundError:
    from benchmark_ipa_contract import accepted_phonetic_ipa

DATA_REVISION = "f80f6c1840c4818b51e05f2e00cded4701a5b662"
DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    f"{DATA_REVISION}/data/splits/lao_eval.csv"
)
TRAIN_DATA_URL = (
    "https://raw.githubusercontent.com/byu-matrix-lab/MekongPhon/"
    f"{DATA_REVISION}/data/splits/lao_train.csv"
)
EXPECTED_DATA_SHA256 = "5351af5ed545f68886a99f0e8d88c91fdbdf46c4df885d40e166b8a3b32cd241"
EXPECTED_TRAIN_SHA256 = "2d0f68989009620980ced3386f11a640e6167404308eeb6a79efc52bc8e40ee0"
EXPECTED_TRAIN_ROWS = 6219
EXPECTED_TRAIN_DUPLICATE_ROWS = 3
from lao_ukrainian.mekongphon import MODEL_IDS, MODEL_REVISIONS, MODEL_WEIGHT_SHA256, MAX_SEQUENCE_LENGTH, MekongPhonEngine
from lao_ukrainian.phonetic_result import from_external_ipa

TONAL_MODEL_ID = MODEL_IDS["tonal"]
TONAL_MODEL_REVISION = MODEL_REVISIONS["tonal"]
SEGMENTAL_MODEL_ID = MODEL_IDS["nontonal"]
SEGMENTAL_MODEL_REVISION = MODEL_REVISIONS["nontonal"]
MODEL_MAX_LENGTH = MAX_SEQUENCE_LENGTH
MODEL_NUM_BEAMS = 5


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def levenshtein(a: str, b: str) -> int:
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (ca != cb),
            ))
        previous = current
    return previous[-1]


def validate_lexicon_split(
    train_rows: list[dict[str, str]], eval_rows: list[dict[str, str]]
) -> dict[str, int]:
    train_forms = {nfc(row["orth"]) for row in train_rows if row.get("orth", "").strip()}
    eval_forms = {nfc(row["orth"]) for row in eval_rows if row.get("orth", "").strip()}
    overlap = train_forms & eval_forms
    train_duplicates = len(train_rows) - len(train_forms)
    if overlap:
        raise ValueError(f"Training/evaluation lexicon overlap: {len(overlap)} forms")
    if len(eval_rows) != 100 or len(eval_forms) != 100:
        raise ValueError("Expected 100 unique held-out lexicon forms")
    if len(train_rows) != EXPECTED_TRAIN_ROWS:
        raise ValueError(f"Expected {EXPECTED_TRAIN_ROWS} training lexicon rows, received {len(train_rows)}")
    if train_duplicates != EXPECTED_TRAIN_DUPLICATE_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_TRAIN_DUPLICATE_ROWS} duplicate training rows, received {train_duplicates}"
        )
    return {
        "training_rows": len(train_rows),
        "training_unique_forms": len(train_forms),
        "training_duplicate_rows": train_duplicates,
        "held_out_rows": len(eval_rows),
        "held_out_unique_forms": len(eval_forms),
        "train_eval_overlap": len(overlap),
        "combined_unique_forms": len(train_forms | eval_forms),
    }


def fetch_csv_rows(url: str) -> tuple[bytes, list[dict[str, str]]]:
    request = urllib.request.Request(url, headers={"User-Agent": "LaoG2P-benchmark/2.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"), newline="")))
    return payload, rows


def load_dataset() -> tuple[list[dict[str, str]], dict[str, object]]:
    eval_payload, rows = fetch_csv_rows(DATA_URL)
    train_payload, train_rows = fetch_csv_rows(TRAIN_DATA_URL)
    eval_digest = hashlib.sha256(eval_payload).hexdigest()
    train_digest = hashlib.sha256(train_payload).hexdigest()
    if eval_digest != EXPECTED_DATA_SHA256:
        raise ValueError(f"Held-out dataset SHA-256 mismatch: {eval_digest}")
    if train_digest != EXPECTED_TRAIN_SHA256:
        raise ValueError(f"Training lexicon SHA-256 mismatch: {train_digest}")
    required = {"orth", "pron_no_tones", "pron_with_tones"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("MekongPhon held-out CSV is empty or has an unexpected schema")
    split = validate_lexicon_split(train_rows, rows)
    if any(not row["pron_no_tones"].strip() or not row["pron_with_tones"].strip() for row in rows):
        raise ValueError("Held-out set contains an empty IPA reference")
    split.update({
        "training_sha256": train_digest,
        "held_out_sha256": eval_digest,
        "source_revision": DATA_REVISION,
        "paper_reported_seed_lexicon_entries": 6039,
        "repository_split_unique_forms": split["combined_unique_forms"],
        "paper_vs_repository_unique_form_delta": split["combined_unique_forms"] - 6039,
    })
    return rows, split


def load_project():
    from lao_ukrainian.core import analyze
    from lao_ukrainian.data import load_registry

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        analysis = analyze(text)
        segmental_elapsed = time.perf_counter() - started

        syllables = analysis.syllables
        phonetic_syllables = [item for item in syllables if item.status != "PASSTHROUGH"]
        vowel_by_id = {row["id"]: row for row in load_registry()["vowels"]}

        def major_weighted(item) -> bool:
            return bool(
                item.coda
                or (
                    item.phonetic_result is not None
                    and item.phonetic_result.vowel_length == "long"
                )
                or vowel_by_id.get(item.vowel or "", {}).get("nucleus_type") == "diphthong"
            )

        segmental_complete = bool(phonetic_syllables) and all(accepted_phonetic_ipa(item.phonetic_result) for item in phonetic_syllables)
        tonal_complete = segmental_complete and all(item.phonetic_result.tone_contour_ipa for item in phonetic_syllables)
        segmental_parts = [item.phonetic_result.phonemic_ipa if accepted_phonetic_ipa(item.phonetic_result) else "" for item in phonetic_syllables]
        segmental = nfc("".join(segmental_parts)) if segmental_complete else ""
        tonal = (
            nfc("".join(
                item.phonetic_result.phonemic_ipa + (item.phonetic_result.tone_contour_ipa or "")
                for item in phonetic_syllables
            ))
            if tonal_complete else ""
        )
        tone_categories = [item.phonetic_result.tone_category if accepted_phonetic_ipa(item.phonetic_result) else None for item in phonetic_syllables]
        mekong_complete = segmental_complete and all(tone_categories)
        mekong_tonal = (
            render_mekong_tonal(segmental_parts, [str(value) for value in tone_categories])
            if mekong_complete else ""
        )
        rendering_coverage = {
            "complete_input": bool(syllables) and all(item.practical_ukrainian is not None for item in syllables),
            "analyzed_units": len(syllables),
            "units_with_rendering": sum(item.practical_ukrainian is not None for item in syllables),
            "supported_ipa_units": sum(item.phonetic_result is not None and item.phonetic_result.status == "SUPPORTED" for item in phonetic_syllables),
            "uncertain_ipa_units": sum(item.phonetic_result is not None and item.phonetic_result.status == "UNCERTAIN" for item in phonetic_syllables),
            "provisional_ipa_units": sum(item.phonetic_result is not None and item.phonetic_result.status == "PROVISIONAL" for item in phonetic_syllables),
            "unknown_marker_units": sum(item.phonetic_result is not None and any(segment.kind == "unknown" for segment in item.phonetic_result.segments) for item in phonetic_syllables),
            "passthrough_units": sum(item.status == "PASSTHROUGH" for item in syllables),
        }
        return {
            "segmental": segmental,
            "tonal": tonal,
            "mekong_tonal": mekong_tonal,
            "rendering_coverage": rendering_coverage,
            "status": analysis.status,
            "warnings": [
                warning
                for item in syllables
                for warning in item.warnings
            ],
            "partial_parse_shapes": [
                {
                    "onset": item.onset or "",
                    "vowel": item.vowel or "",
                    "coda": item.coda or "",
                    "tone_mark": item.tone_mark or "",
                    "syllable_type": item.syllable_type or "",
                    "rules": item.rules,
                }
                for item in syllables
                if item.status != "OK"
            ],
            "tone_categories": tone_categories,
            "tone_contexts": [
                {
                    "syllable_index": index,
                    "syllable_count": len(syllables),
                    "word_position": (
                        "initial" if index == 0 else
                        "final" if index == len(syllables) - 1 else "medial"
                    ),
                    # A candidate minor syllable is only a diagnostic hint:
                    # Enfield's C0V0 slot permits short /a, i, u/ with no coda.
                    # It is not promoted to a production tone rule here.
                    "following_major_weighted": bool(
                        index + 1 < len(syllables) and major_weighted(syllables[index + 1])
                    ),
                    "candidate_minor_shape": bool(
                        index == 0
                        and item.vowel in {"A", "I", "U"}
                        and item.phonetic_result is not None
                        and item.phonetic_result.vowel_length == "short"
                        and not item.coda
                        and not item.tone_mark
                        and not item.warnings
                        and item.phonetic_result.status == "SUPPORTED"
                        and index + 1 < len(syllables)
                        and major_weighted(syllables[index + 1])
                    ),
                    "candidate_minor_open_a_shape": bool(
                        index == 0
                        and item.vowel == "A"
                        and item.phonetic_result is not None
                        and item.phonetic_result.vowel_length == "short"
                        and not item.coda
                        and not item.tone_mark
                        and not item.warnings
                        and item.phonetic_result.status == "SUPPORTED"
                        and index + 1 < len(syllables)
                        and major_weighted(syllables[index + 1])
                    ),
                    "onset": item.onset or "",
                    "consonant_class": item.consonant_class or "",
                    "vowel": item.vowel or "",
                    "coda": item.coda or "",
                    "tone_mark": item.tone_mark or "none",
                    "syllable_type": item.syllable_type or "",
                    "tone_category": item.phonetic_result.tone_category if item.phonetic_result else "",
                    "analysis_status": item.status,
                    "tone_rule_id": next(
                        (rule for rule in item.rules if str(rule).startswith("VNT-")), ""
                    ),
                }
                for index, item in enumerate(syllables)
            ],
            # ClippyFirst emits segmental IPA and tone from one analysis pass;
            # each requested output is therefore available after the same elapsed time.
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": segmental_elapsed,
        }

    return predict


def load_lao2ipa():
    from lao2ipa import transliterate

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        segmental = transliterate(text, output="ipa", ignore_tones=True)
        segmental_elapsed = time.perf_counter() - started
        started = time.perf_counter()
        tonal = transliterate(text, output="ipa", ignore_tones=False)
        tonal_elapsed = time.perf_counter() - started
        if not isinstance(segmental, str) or not isinstance(tonal, str):
            raise TypeError("lao2ipa must return strings for both output modes")
        return {
            "segmental": nfc(segmental),
            "tonal": nfc(tonal),
            "status": "RETURNED",
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": tonal_elapsed,
        }

    return predict


def load_neural():
    """Run both immutable checkpoints through the production MekongPhon adapter."""
    import torch
    from huggingface_hub import hf_hub_download, model_info

    torch.set_num_threads(min(2, os.cpu_count() or 1))

    def load_one(model_id: str, pinned_revision: str, *, tonal: bool):
        info = model_info(model_id, revision=pinned_revision)
        if info.sha != pinned_revision:
            raise RuntimeError(
                f"Hub resolved {model_id}@{pinned_revision} to unexpected SHA {info.sha}"
            )
        model_key = "tonal" if tonal else "nontonal"
        weight_path = hf_hub_download(
            repo_id=model_id, filename="model.safetensors", revision=pinned_revision
        )
        weight_digest = hashlib.sha256(Path(weight_path).read_bytes()).hexdigest()
        expected_weight_digest = MODEL_WEIGHT_SHA256[model_key]
        if weight_digest != expected_weight_digest:
            raise RuntimeError(
                f"{model_id}: model.safetensors SHA-256 mismatch: {weight_digest}"
            )
        engine = MekongPhonEngine(
            tonal=tonal, revision=pinned_revision, device="cpu",
            num_beams=MODEL_NUM_BEAMS,
        )
        smoke = engine.transcribe("ຂາ")
        if smoke.model_revision != pinned_revision:
            raise RuntimeError(f"{model_id}: adapter returned unexpected model revision")
        if not smoke.raw_ipa.strip() or smoke.phonetic_result.external_ipa != smoke.raw_ipa:
            raise RuntimeError(f"{model_id}: adapter failed to preserve non-empty raw IPA")
        if smoke.status == "IPA_UNSUPPORTED" and smoke.ukrainian is not None:
            raise RuntimeError(f"{model_id}: unsupported IPA must not produce Ukrainian output")

        def generate(text: str) -> str:
            return nfc(engine.predict_raw_ipa(text))

        return generate, pinned_revision, weight_digest

    tonal_generate, tonal_revision, tonal_weight_sha256 = load_one(
        TONAL_MODEL_ID, TONAL_MODEL_REVISION, tonal=True
    )
    segmental_generate, segmental_revision, segmental_weight_sha256 = load_one(
        SEGMENTAL_MODEL_ID, SEGMENTAL_MODEL_REVISION, tonal=False
    )

    def predict(text: str) -> dict[str, str | float]:
        started = time.perf_counter()
        segmental = segmental_generate(text)
        segmental_elapsed = time.perf_counter() - started
        started = time.perf_counter()
        tonal = tonal_generate(text)
        tonal_elapsed = time.perf_counter() - started
        return {
            "segmental": segmental,
            "tonal": tonal,
            "status": "RETURNED",
            "segmental_seconds": segmental_elapsed,
            "tonal_seconds": tonal_elapsed,
        }

    return predict, {
        "segmental_model": SEGMENTAL_MODEL_ID,
        "segmental_revision": segmental_revision,
        "tonal_model": TONAL_MODEL_ID,
        "tonal_revision": tonal_revision,
        "segmental_model_weight_sha256": segmental_weight_sha256,
        "tonal_model_weight_sha256": tonal_weight_sha256,
        "num_beams": MODEL_NUM_BEAMS,
        "max_input_tokens": MODEL_MAX_LENGTH,
        "truncation": False,
        "inference_adapter": "lao_ukrainian.mekongphon.MekongPhonEngine",
    }



def alignment_error_profile(
    references: list[str], predictions: list[str], limit: int = 20
) -> dict[str, object]:
    """Aggregate code-point edit confusions without retaining words or outputs."""
    substitutions: Counter[str] = Counter()
    deletions: Counter[str] = Counter()
    insertions: Counter[str] = Counter()

    for reference, prediction in zip(references, predictions):
        n, m = len(reference), len(prediction)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = i
        for j in range(m + 1):
            dp[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                dp[i][j] = min(
                    dp[i - 1][j] + 1,
                    dp[i][j - 1] + 1,
                    dp[i - 1][j - 1] + (reference[i - 1] != prediction[j - 1]),
                )
        i, j = n, m
        while i or j:
            if i and j and reference[i - 1] == prediction[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
                i -= 1
                j -= 1
            elif i and j and dp[i][j] == dp[i - 1][j - 1] + 1:
                substitutions[f"{reference[i - 1]}=>{prediction[j - 1]}"] += 1
                i -= 1
                j -= 1
            elif i and dp[i][j] == dp[i - 1][j] + 1:
                deletions[reference[i - 1]] += 1
                i -= 1
            else:
                insertions[prediction[j - 1]] += 1
                j -= 1

    return {
        "unit": "Unicode code point (NFC)",
        "alignment": "Levenshtein; tie-break priority: match, substitution, deletion, insertion",
        "top_substitutions": [
            {"pair": key, "count": count}
            for key, count in substitutions.most_common(limit)
        ],
        "top_deletions": [
            {"symbol": key, "count": count}
            for key, count in deletions.most_common(limit)
        ],
        "top_insertions": [
            {"symbol": key, "count": count}
            for key, count in insertions.most_common(limit)
        ],
        "total_substitutions": sum(substitutions.values()),
        "total_deletions": sum(deletions.values()),
        "total_insertions": sum(insertions.values()),
    }


def remove_optional_ipa_tie_bars(value: str) -> str:
    """Remove only IPA affricate tie bars for a secondary allograph score."""
    return nfc(value.replace("\u0361", "").replace("\u035c", ""))


def score(references: list[str], predictions: list[str]) -> dict[str, object]:
    import sacrebleu

    def metrics(refs: list[str], preds: list[str]) -> dict[str, object]:
        edits = sum(levenshtein(ref, pred) for ref, pred in zip(refs, preds))
        chars = sum(len(ref) for ref in refs)
        exact = sum(ref == pred for ref, pred in zip(refs, preds))
        chrf = (
            sacrebleu.metrics.CHRF(word_order=2).corpus_score(preds, [refs]).score
            if refs else None
        )
        return {
            "n": len(refs),
            "exact_matches": exact,
            "exact_match_rate": exact / len(refs) if refs else None,
            "cer": edits / chars if chars else None,
            "chrf++": chrf,
        }

    covered = [(ref, pred) for ref, pred in zip(references, predictions) if pred]
    return {
        **metrics(references, predictions),
        "coverage": len(covered) / len(references) if references else 0.0,
        "missing_or_withheld": len(references) - len(covered),
        "covered_subset": metrics(
            [pair[0] for pair in covered],
            [pair[1] for pair in covered],
        ),
    }


MEKONG_CONTOUR_TO_CATEGORY = {
    "˩˧": "low-rising",
    "˧˥": "high-rising",
    "˧": "high-mid",
    "˧˩": "low-falling",
    "˥˨": "high-falling",
}
MEKONG_CATEGORY_TO_CONTOUR = {
    **{category: contour for contour, category in MEKONG_CONTOUR_TO_CATEGORY.items()},
}


def render_mekong_tonal(syllable_segmentals: list[str], categories: list[str] | None) -> str:
    """Interleave each syllable's segments and tone in benchmark notation."""
    if (
        not syllable_segmentals
        or categories is None
        or len(syllable_segmentals) != len(categories)
        or not all(syllable_segmentals)
        or not all(value in MEKONG_CATEGORY_TO_CONTOUR for value in categories)
    ):
        return ""
    return nfc("".join(
        segmental + MEKONG_CATEGORY_TO_CONTOUR[category]
        for segmental, category in zip(syllable_segmentals, categories)
    ))


def parse_mekong_tone_categories(suffix: str) -> list[str] | None:
    """Parse the explicit MekongPhon rule-baseline contour convention."""
    if not suffix:
        return []
    contours = sorted(MEKONG_CONTOUR_TO_CATEGORY, key=len, reverse=True)
    categories: list[str] = []
    index = 0
    while index < len(suffix):
        match = next((value for value in contours if suffix.startswith(value, index)), None)
        if match is None:
            return None
        categories.append(MEKONG_CONTOUR_TO_CATEGORY[match])
        index += len(match)
    return categories




def strip_tone_symbols(ipa: str) -> str:
    """Remove typed tone segments while preserving all segmental IPA."""
    if not ipa:
        return ""
    return nfc(from_external_ipa(ipa).phonemic_ipa or "")


def length_marker_metrics(references: list[str], predictions: list[str]) -> dict[str, object]:
    covered = [(ref, pred) for ref, pred in zip(references, predictions) if pred]
    ref_counts = [ref.count("ː") for ref, _ in covered]
    pred_counts = [pred.count("ː") for _, pred in covered]
    exact = sum(ref == pred for ref, pred in zip(ref_counts, pred_counts))
    presence_exact = sum((ref > 0) == (pred > 0) for ref, pred in zip(ref_counts, pred_counts))
    return {
        "n": len(references),
        "coverage": len(covered) / len(references) if references else 0.0,
        "covered_items": len(covered),
        "reference_long_vowel_marker_total": sum(ref_counts),
        "prediction_long_vowel_marker_total": sum(pred_counts),
        "items_with_exact_marker_count": exact,
        "marker_count_exact_rate_on_covered": exact / len(covered) if covered else None,
        "long_vowel_presence_exact_items": presence_exact,
        "long_vowel_presence_exact_rate_on_covered": presence_exact / len(covered) if covered else None,
        "absolute_marker_count_error_total": sum(abs(ref - pred) for ref, pred in zip(ref_counts, pred_counts)),
        "interpretation": "word-level count of ː markers only; not syllable-aligned length accuracy",
    }


def classify_word_final_coda(
    ipa: str, core_codas: set[str], analysis_dependent_codas: set[str]
) -> tuple[str, str | None] | None:
    if not ipa:
        return None
    parsed = from_external_ipa(ipa)
    if parsed.status != "SUPPORTED":
        return None
    segments = [segment for segment in parsed.segments if segment.kind != "tone"]
    if not segments:
        return None
    final = segments[-1]
    if final.kind == "vowel":
        return ("open", None)
    if final.ipa in core_codas:
        return ("closed", final.ipa)
    if final.ipa in analysis_dependent_codas:
        return None
    return None


def word_final_coda_metrics(
    references: list[str],
    predictions: list[str],
    core_codas: set[str],
    analysis_dependent_codas: set[str],
) -> dict[str, object]:
    covered = 0
    presence_correct = 0
    reference_coda_items = 0
    coda_identity_scored = 0
    coda_identity_correct = 0
    reference_coda_total = 0
    prediction_coda_total = 0
    unresolved_reference = 0
    unresolved_prediction = 0
    for reference, prediction in zip(references, predictions):
        ref_class = classify_word_final_coda(reference, core_codas, analysis_dependent_codas)
        pred_class = classify_word_final_coda(prediction, core_codas, analysis_dependent_codas)
        if ref_class is None:
            unresolved_reference += 1
            continue
        if ref_class[0] == "closed":
            reference_coda_total += 1
        if pred_class is None:
            unresolved_prediction += 1
            continue
        if pred_class[0] == "closed":
            prediction_coda_total += 1
        covered += 1
        if ref_class[0] == pred_class[0]:
            presence_correct += 1
        if ref_class[0] == "closed":
            reference_coda_items += 1
            coda_identity_scored += 1
            if pred_class[0] == "closed" and pred_class[1] == ref_class[1]:
                coda_identity_correct += 1
    return {
        "n": len(references),
        "scorable_items": covered,
        "coverage": covered / len(references) if references else 0.0,
        "reference_word_final_coda_items": reference_coda_total,
        "prediction_word_final_coda_items": prediction_coda_total,
        "word_final_coda_presence_exact_items": presence_correct,
        "word_final_coda_presence_accuracy": presence_correct / covered if covered else None,
        "reference_coda_identity_items": reference_coda_items,
        "coda_identity_exact_items": coda_identity_correct,
        "coda_identity_accuracy": coda_identity_correct / coda_identity_scored if coda_identity_scored else None,
        "unresolved_reference_items": unresolved_reference,
        "unresolved_prediction_items": unresolved_prediction,
        "interpretation": "word-final coda only; core inventory only; analysis-dependent l/r and unknown IPA are unresolved",
    }


def syllable_boundary_availability(
    segmental_references: list[str], tonal_references: list[str]
) -> dict[str, object]:
    separators = frozenset(" .·‧")
    segmental_annotated = sum(any(char in separators for char in value) for value in segmental_references)
    tonal_annotated = sum(any(char in separators for char in value) for value in tonal_references)
    return {
        "status": "NOT_SCORABLE",
        "n": len(segmental_references),
        "segmental_reference_items_with_explicit_boundaries": segmental_annotated,
        "tonal_reference_items_with_explicit_boundaries": tonal_annotated,
        "reason": "The 100-word reference IPA strings contain no explicit syllable-boundary delimiters or annotations. Tone contours are not a reliable boundary proxy.",
    }


def score_tone_categories(
    references: list[list[str]],
    predictions: list[list[str | None]],
) -> dict[str, object]:
    """Score only known aligned categories; report unresolved coverage separately."""
    covered = 0
    errors = 0
    unresolved = 0
    unresolved_words = 0
    exact_words = 0
    complete_words = 0
    length_mismatches = 0
    total = sum(len(row) for row in references)

    for reference, prediction in zip(references, predictions):
        if len(reference) != len(prediction):
            length_mismatches += 1
            unresolved += len(reference)
            unresolved_words += 1
            continue
        word_complete = True
        word_exact = True
        for expected, actual in zip(reference, prediction):
            if actual is None or not str(actual).strip():
                unresolved += 1
                word_complete = False
                word_exact = False
                continue
            covered += 1
            if actual != expected:
                errors += 1
                word_exact = False
        if word_complete:
            complete_words += 1
            if word_exact:
                exact_words += 1
        else:
            unresolved_words += 1

    return {
        "n": len(references),
        "exact_matches": exact_words,
        "exact_match_rate": exact_words / len(references) if references else None,
        "complete_words": complete_words,
        "complete_word_rate": complete_words / len(references) if references else None,
        "category_error_rate": errors / covered if covered else None,
        "coverage": covered / total if total else 0.0,
        "covered_categories": covered,
        "reference_categories": total,
        "unresolved_categories": unresolved,
        "unresolved_words": unresolved_words,
        "word_length_mismatches": length_mismatches,
    }


def extract_tone_suffix(segmental: str, tonal: str) -> str | None:
    """Extract inserted tone symbols when the segmental string is an exact subsequence."""
    if not tonal:
        return ""
    index = 0
    tone_symbols: list[str] = []
    for char in tonal:
        if index < len(segmental) and char == segmental[index]:
            index += 1
        else:
            tone_symbols.append(char)
    return "".join(tone_symbols) if index == len(segmental) else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=Path("artifacts/mekongphon-100-word-benchmark.json"),
    )
    args = parser.parse_args()

    rows, dataset_provenance = load_dataset()
    dataset_sha = str(dataset_provenance['held_out_sha256'])
    sources = [nfc(row["orth"]) for row in rows]
    segmental_references = [nfc(row["pron_no_tones"]) for row in rows]
    tonal_references = [nfc(row["pron_with_tones"]) for row in rows]

    neural_predict, neural_provenance = load_neural()
    coda_registry = load_registry()["codas"]
    core_codas = {row["ipa"] for row in coda_registry.values() if row["status"] == "core"}
    analysis_dependent_codas = {row["ipa"] for row in coda_registry.values() if row["status"] != "core"}
    boundary_availability = syllable_boundary_availability(
        segmental_references, tonal_references
    )
    engines = {
        "clippyfirst_rule_engine": (load_project(), "repository source"),
        "lao2ipa": (load_lao2ipa(), importlib.metadata.version("lao2ipa")),
        "mekongphon_neural": (neural_predict, neural_provenance),
    }

    results: dict[str, object] = {}
    engine_predictions: dict[str, dict[str, list[str]]] = {}
    for name, (predict, version) in engines.items():
        segmental_outputs: list[str] = []
        tonal_outputs: list[str] = []
        statuses: dict[str, int] = {}
        segmental_durations: list[float] = []
        tonal_durations: list[float] = []
        errors = 0
        warning_counts: dict[str, int] = {}
        partial_shape_counts: dict[str, int] = {}
        partial_warning_shape_counts: dict[str, int] = {}
        segmental_withheld = 0
        tonal_withheld = 0
        engine_tone_categories: list[list[str | None] | None] = []
        engine_tone_contexts: list[list[dict[str, str]] | None] = []
        mekong_convention_tonal_outputs: list[str] = []
        rendering_rows: list[dict[str, int | bool]] = []

        for source in sources:
            try:
                output = predict(source)
                segmental = nfc(str(output["segmental"]))
                tonal = nfc(str(output["tonal"]))
                status = str(output["status"])
                raw_categories = output.get("tone_categories")
                engine_tone_categories.append(
                    list(raw_categories) if raw_categories is not None else None
                )
                raw_contexts = output.get("tone_contexts")
                engine_tone_contexts.append(
                    [
                        {str(key): str(value) for key, value in context.items()}
                        for context in raw_contexts
                    ]
                    if raw_contexts is not None else None
                )
                raw_mekong_tonal = output.get("mekong_tonal")
                mekong_tonal = (
                    nfc(str(raw_mekong_tonal))
                    if raw_mekong_tonal is not None else tonal
                )
                mekong_convention_tonal_outputs.append(nfc(mekong_tonal))
                raw_rendering = output.get("rendering_coverage")
                if isinstance(raw_rendering, dict):
                    rendering_rows.append(raw_rendering)
                for shape in output.get("partial_parse_shapes", []):
                    shape_key = "|".join([
                        str(shape.get("onset", "")),
                        str(shape.get("vowel", "")),
                        str(shape.get("coda", "")),
                        str(shape.get("tone_mark", "")),
                        str(shape.get("syllable_type", "")),
                        ",".join(str(rule) for rule in shape.get("rules", [])),
                    ])
                    partial_shape_counts[shape_key] = partial_shape_counts.get(shape_key, 0) + 1
                for warning in output.get("warnings", []):
                    warning = str(warning)
                    warning_code, _, detail = warning.partition(":")
                    if warning_code == "SHORT_VOWEL_REQUIRES_CODA":
                        warning_code = f"{warning_code}:{detail}"
                    elif warning_code == "UNCONSUMED_AFTER_VOWEL":
                        tail = detail
                        tail_shape = " + ".join(
                            unicodedata.name(char, "UNKNOWN-CODEPOINT")
                            for char in tail
                        )
                        partial_warning_shape_counts[tail_shape] = (
                            partial_warning_shape_counts.get(tail_shape, 0) + 1
                        )
                        if any(ch in "່້໊໋" for ch in tail):
                            shape = "contains-tone-mark"
                        elif tail.startswith(("ເ", "ແ", "ໂ", "ໃ", "ໄ")):
                            shape = "starts-preposed-vowel"
                        elif len(tail) == 1:
                            shape = "single-grapheme"
                        elif any(ch in "ະັາິີຶືຸູົຽໍຳວອຍ" for ch in tail):
                            shape = "contains-vowel-material"
                        else:
                            shape = "other-multigrapheme"
                        first_name = unicodedata.name(tail[0], "UNKNOWN").replace(" ", "_")
                        warning_code = f"{warning_code}:{shape}:first={first_name}:length={len(tail)}"
                    warning_counts[warning_code] = warning_counts.get(warning_code, 0) + 1
                segmental_durations.append(float(output["segmental_seconds"]))
                tonal_durations.append(float(output["tonal_seconds"]))
            except Exception as exc:
                segmental = ""
                tonal = ""
                status = f"ERROR:{type(exc).__name__}"
                segmental_durations.append(0.0)
                tonal_durations.append(0.0)
                errors += 1
                engine_tone_categories.append(None)
                engine_tone_contexts.append(None)
                mekong_convention_tonal_outputs.append("")
            segmental_outputs.append(segmental)
            tonal_outputs.append(tonal)
            segmental_withheld += not bool(segmental)
            tonal_withheld += not bool(tonal)
            statuses[status] = statuses.get(status, 0) + 1

        segmental_metrics = score(segmental_references, segmental_outputs)
        tonal_metrics = score(tonal_references, tonal_outputs)
        tonal_segmental_outputs = [strip_tone_symbols(value) for value in tonal_outputs]
        tonal_segmental_metrics = score(segmental_references, tonal_segmental_outputs)
        segmental_length_metrics = length_marker_metrics(segmental_references, segmental_outputs)
        tonal_length_metrics = length_marker_metrics(segmental_references, tonal_segmental_outputs)
        segmental_coda_metrics = word_final_coda_metrics(
            segmental_references, segmental_outputs, core_codas, analysis_dependent_codas
        )
        tonal_coda_metrics = word_final_coda_metrics(
            segmental_references, tonal_segmental_outputs, core_codas, analysis_dependent_codas
        )
        mekong_convention_tonal_metrics = score(
            tonal_references, mekong_convention_tonal_outputs
        )
        tone_references: list[str] = []
        tone_predictions: list[str] = []
        tone_alignment_failures = 0
        for ref_segmental, ref_tonal, pred_segmental, pred_tonal in zip(
            segmental_references, tonal_references, segmental_outputs, tonal_outputs
        ):
            if pred_segmental != ref_segmental:
                continue
            ref_tone = extract_tone_suffix(ref_segmental, ref_tonal)
            pred_tone = extract_tone_suffix(pred_segmental, pred_tonal)
            if ref_tone is None or pred_tone is None:
                tone_alignment_failures += 1
                continue
            tone_references.append(ref_tone)
            tone_predictions.append(pred_tone)
        tone_only_metrics = score(tone_references, tone_predictions)
        tone_category_references: list[list[str]] = []
        tone_category_predictions: list[list[str | None]] = []
        tone_category_alignment_failures = 0
        tone_category_confusion: dict[str, int] = {}
        tone_category_error_contexts: dict[str, int] = {}
        tone_unresolved_contexts: dict[str, int] = {}
        tone_category_length_mismatches = 0
        for index, (ref_segmental, ref_tonal, pred_segmental, pred_tonal) in enumerate(zip(
            segmental_references, tonal_references, segmental_outputs, tonal_outputs
        )):
            if pred_segmental != ref_segmental:
                continue
            ref_suffix = extract_tone_suffix(ref_segmental, ref_tonal)
            ref_categories = parse_mekong_tone_categories(ref_suffix or "")
            if ref_suffix is None or not ref_categories:
                tone_category_alignment_failures += 1
                continue
            raw_categories = engine_tone_categories[index]
            if raw_categories is not None:
                pred_categories = raw_categories
            else:
                pred_suffix = extract_tone_suffix(pred_segmental, pred_tonal)
                parsed_categories = parse_mekong_tone_categories(pred_suffix or "")
                if pred_suffix is None or parsed_categories is None:
                    tone_category_alignment_failures += 1
                    continue
                pred_categories = parsed_categories
            tone_category_references.append(ref_categories)
            tone_category_predictions.append(pred_categories)
            if len(ref_categories) != len(pred_categories):
                tone_category_length_mismatches += 1
            else:
                contexts = engine_tone_contexts[index] or []
                for category_index, (expected, actual) in enumerate(zip(ref_categories, pred_categories)):
                    if actual is None or not str(actual).strip():
                        continue
                    key = f"{expected}=>{actual}"
                    tone_category_confusion[key] = tone_category_confusion.get(key, 0) + 1
                    if expected != actual and category_index < len(contexts):
                        context = contexts[category_index]
                        context_key = "|".join([
                            key,
                            f"class={context.get('consonant_class', '')}",
                            f"type={context.get('syllable_type', '')}",
                            f"vowel={context.get('vowel', '')}",
                            f"coda={context.get('coda', '')}",
                            f"mark={context.get('tone_mark', '')}",
                            f"rule={context.get('tone_rule_id', '')}",
                            f"position={context.get('word_position', '')}",
                            f"candidate_minor={context.get('candidate_minor_shape', False)}",
                            f"syllable_index={context.get('syllable_index', '')}",
                            f"syllable_count={context.get('syllable_count', '')}",
                        ])
                        tone_category_error_contexts[context_key] = (
                            tone_category_error_contexts.get(context_key, 0) + 1
                        )
        for contexts in engine_tone_contexts:
            for context in contexts or []:
                if context.get("tone_category") not in {"", "None"}:
                    continue
                context_key = "|".join([
                    f"class={context.get('consonant_class', '')}",
                    f"type={context.get('syllable_type', '')}",
                    f"vowel={context.get('vowel', '')}",
                    f"coda={context.get('coda', '')}",
                    f"mark={context.get('tone_mark', '')}",
                    f"rule={context.get('tone_rule_id', '')}",
                    f"position={context.get('word_position', '')}",
                    f"candidate_minor={context.get('candidate_minor_shape', False)}",
                    f"candidate_minor_open_a={context.get('candidate_minor_open_a_shape', False)}",
                    f"following_major_weighted={context.get('following_major_weighted', False)}",
                    f"status={context.get('analysis_status', '')}",
                ])
                tone_unresolved_contexts[context_key] = tone_unresolved_contexts.get(context_key, 0) + 1

        tone_category_metrics = score_tone_categories(
            tone_category_references, tone_category_predictions
        )
        engine_predictions[name] = {
            "segmental": segmental_outputs,
            "tonal": tonal_outputs,
            "mekong_tonal": mekong_convention_tonal_outputs,
        }
        rendering_summary = None
        if rendering_rows:
            rendering_summary = {
                "complete_inputs": sum(bool(row["complete_input"]) for row in rendering_rows),
                "input_coverage": sum(bool(row["complete_input"]) for row in rendering_rows) / len(rows),
                "analyzed_units": sum(int(row["analyzed_units"]) for row in rendering_rows),
                "units_with_rendering": sum(int(row["units_with_rendering"]) for row in rendering_rows),
                "supported_ipa_units": sum(int(row["supported_ipa_units"]) for row in rendering_rows),
                "uncertain_ipa_units": sum(int(row["uncertain_ipa_units"]) for row in rendering_rows),
                "provisional_ipa_units": sum(int(row["provisional_ipa_units"]) for row in rendering_rows),
                "unknown_marker_units": sum(int(row["unknown_marker_units"]) for row in rendering_rows),
                "passthrough_units": sum(int(row["passthrough_units"]) for row in rendering_rows),
            }
        results[name] = {
            "version_or_revision": version,
            "rendering_coverage": rendering_summary,
            "segmental_vs_pron_no_tones": segmental_metrics,
            "tonal_model_segmental_vs_pron_no_tones": tonal_segmental_metrics,
            "segmental_vowel_length_markers": segmental_length_metrics,
            "tonal_model_vowel_length_markers": tonal_length_metrics,
            "segmental_word_final_coda": segmental_coda_metrics,
            "tonal_model_word_final_coda": tonal_coda_metrics,
            "syllable_boundary_evaluation": boundary_availability,
            "segmental_edit_profile": alignment_error_profile(
                segmental_references, segmental_outputs
            ),
            "segmental_optional_tie_bar_normalized": score(
                [remove_optional_ipa_tie_bars(value) for value in segmental_references],
                [remove_optional_ipa_tie_bars(value) for value in segmental_outputs],
            ),
            "tonal_optional_tie_bar_normalized": score(
                [remove_optional_ipa_tie_bars(value) for value in tonal_references],
                [remove_optional_ipa_tie_bars(value) for value in tonal_outputs],
            ),
            "tonal_vs_pron_with_tones": tonal_metrics,
            "tonal_mekong_convention_vs_pron_with_tones": mekong_convention_tonal_metrics,
            "tone_only_on_segmental_exact_subset": tone_only_metrics,
            "tone_category_on_segmental_exact_subset": tone_category_metrics,
            "tone_category_confusion_aligned_words": dict(sorted(tone_category_confusion.items())),
            "tone_category_error_contexts": dict(sorted(tone_category_error_contexts.items())),
            "tone_unresolved_contexts": dict(sorted(tone_unresolved_contexts.items())),
            "tone_category_word_length_mismatches": tone_category_length_mismatches,
            "segmental_exact_subset_n": len(tone_references),
            "tone_only_alignment_failures": tone_alignment_failures,
            "tone_category_alignment_failures": tone_category_alignment_failures,
            "runtime_errors": errors,
            "status_counts": statuses,
            "segmental_withheld_items": segmental_withheld,
            "tonal_withheld_items": tonal_withheld,
            "warning_counts": dict(sorted(warning_counts.items())),
            "partial_parse_shape_counts": dict(sorted(partial_shape_counts.items())),
            "partial_warning_shape_counts": dict(sorted(partial_warning_shape_counts.items())),
            "segmental_mean_latency_ms": round(statistics.mean(segmental_durations) * 1000, 3),
            "tonal_mean_latency_ms": round(statistics.mean(tonal_durations) * 1000, 3),
            "segmental_throughput_items_per_second": (
                round(len(segmental_durations) / sum(segmental_durations), 3)
                if sum(segmental_durations) else None
            ),
            "tonal_throughput_items_per_second": (
                round(len(tonal_durations) / sum(tonal_durations), 3)
                if sum(tonal_durations) else None
            ),
        }

    shared_comparisons: dict[str, object] = {}
    clippy = engine_predictions["clippyfirst_rule_engine"]
    for comparator in ("lao2ipa", "mekongphon_neural"):
        baseline = engine_predictions[comparator]
        shared_segmental_indices = [
            i for i in range(len(sources))
            if clippy["segmental"][i] and baseline["segmental"][i]
        ]
        shared_tonal_indices = [
            i for i in range(len(sources))
            if clippy["mekong_tonal"][i] and baseline["tonal"][i]
        ]
        shared_comparisons[comparator] = {
            "segmental_shared_n": len(shared_segmental_indices),
            "clippyfirst_segmental": score(
                [segmental_references[i] for i in shared_segmental_indices],
                [clippy["segmental"][i] for i in shared_segmental_indices],
            ),
            "comparator_segmental": score(
                [segmental_references[i] for i in shared_segmental_indices],
                [baseline["segmental"][i] for i in shared_segmental_indices],
            ),
            "tonal_shared_n": len(shared_tonal_indices),
            "clippyfirst_mekong_convention_tonal": score(
                [tonal_references[i] for i in shared_tonal_indices],
                [clippy["mekong_tonal"][i] for i in shared_tonal_indices],
            ),
            "comparator_tonal": score(
                [tonal_references[i] for i in shared_tonal_indices],
                [baseline["tonal"][i] for i in shared_tonal_indices],
            ),
        }

    report = {
        "schema_version": "4.0",
        "cross_engine_shared_coverage": shared_comparisons,
        "benchmark": "MekongPhon held-out Lao lexicon, 100 words",
        "dataset": {
            "url": DATA_URL,
            "source_revision": DATA_REVISION,
            "sha256": dataset_sha,
            "split_audit": dataset_provenance,
            "n": len(rows),
            "segmental_reference_column": "pron_no_tones",
            "tonal_reference_column": "pron_with_tones",
            "profile": "Lao, Vientiane tone convention as described in MekongPhon",
            "redistribution": "No source rows, references or per-item predictions are included in this report.",
        },
        "method": {
            "normalization": "Unicode NFC and outer whitespace trim only",
            "segmental_comparison": "typed SUPPORTED/UNCERTAIN IPA only; PROVISIONAL grapheme hints are excluded and reported separately in rendering_coverage",
            "tonal_comparison": "segmental IPA plus per-syllable tone contour against pron_with_tones",
            "tone_only": "segmental-exact items only; tone symbols are extracted by aligning tonal and segmental strings",
            "tone_category": "segmental-exact items only; MekongPhon baseline contours ˩˧, ˧˥, ˧, ˧˩, ˥˨ map to named tone categories and are compared as syllable-level tokens",
            "error_analysis": "Top segmental insertions/deletions/substitutions are aggregate NFC code-point alignments; tone disagreements include syllable position and a non-operative candidate-minor-shape diagnostic. Secondary IPA scores remove only optional affricate tie bars U+0361/U+035C; raw scores remain primary. Potential minor-syllable tones are withheld and aggregated separately, not guessed. No source words or complete predictions are retained in the artifact.",
            "contour_convention": "ClippyFirst production contours follow the source-scoped Ueda (1994) numeric-to-IPA conversion; raw contour CER is convention-sensitive and is reported separately from category accuracy",
        "potential_minor_syllable_tone": "An initial unmarked short open /a/ shape may be a minor syllable; because orthography alone cannot prove that status, the engine withholds tone rather than inventing a neutral contour.",
            "mekong_convention_conversion": "For comparison only, ClippyFirst tone categories are re-rendered with the MekongPhon rule-baseline contour notation; this does not change production IPA or tone rules",
            "cer": "Unicode code-point Levenshtein distance summed over all items, divided by total reference code points",
            "chrf++": "SacreBLEU CHRF with word_order=2, corpus-level",
            "exact_match": "strict full-string IPA comparison",
            "vowel_length": "word-level count/presence of IPA ː markers; no syllable-aligned positions are available",
            "word_final_coda": "word-final open/closed status and core-coda identity from the project IPA/coda inventories; analysis-dependent l/r excluded",
            "syllable_boundaries": "not scorable: neither reference column contains explicit syllable-boundary annotations; tone marks are not used as boundary proxies",
            "missing_output": "empty output remains in the denominator and incurs full reference deletion cost",
            "clippyfirst_tone_contract": "tone contour is stored separately in typed PhoneticResult metadata; tonal score composes it after each syllable's segmental IPA",
            "latency": "per-item inference; model loading excluded; CPU runner, sequential items. ClippyFirst emits segmental and tonal fields in one analysis pass, so both availability latencies are equal and must not be summed; Lao2IPA and MekongPhon use separate segmental and tonal calls",
            "scope_warning": "This is the 100 held-out seed-lexicon word set, not the paper's 13,442-sentence test. It cannot be compared numerically with the paper's sentence-level Table 4.",
            "gold_warning": "The source paper describes the seed lexicon as derived from human-annotated IPA in Kerr (1972), with a 500-entry manual review; it also reports 14/500 Lao inaccuracies. This benchmark is not independently re-adjudicated gold for this project.",
            "historical_note": "Schema 1.0 compared ClippyFirst segmental IPA to the tonal reference and mixed output contracts. Schema 2.0 separated segmental and tonal scoring. Schema 3.0 additionally reports covered-subset metrics, isolated tone-symbol metrics, and tone-category metrics. Schema 4.0 scores only known syllable-aligned tone categories and reports unresolved-category coverage separately; unknown tone is never serialized as a literal category. Do not compare CER or tone-category rates across schema versions without accounting for their different scoring contracts.",
        },
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "torch": importlib.metadata.version("torch"),
            "transformers": importlib.metadata.version("transformers"),
            "sacrebleu": importlib.metadata.version("sacrebleu"),
        },
        "engines": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "benchmark": report["benchmark"],
        "dataset_sha256": dataset_sha,
        "engines": {
            name: {
                "segmental_cer": result["segmental_vs_pron_no_tones"]["cer"],
                "tonal_model_segmental_cer": result["tonal_model_segmental_vs_pron_no_tones"]["cer"],
                "segmental_length_marker_count_exact": result["segmental_vowel_length_markers"]["marker_count_exact_rate_on_covered"],
                "tonal_model_length_marker_count_exact": result["tonal_model_vowel_length_markers"]["marker_count_exact_rate_on_covered"],
                "segmental_word_final_coda_presence_accuracy": result["segmental_word_final_coda"]["word_final_coda_presence_accuracy"],
                "tonal_word_final_coda_presence_accuracy": result["tonal_model_word_final_coda"]["word_final_coda_presence_accuracy"],
                "segmental_tie_bar_normalized_cer": result["segmental_optional_tie_bar_normalized"]["cer"],
                "segmental_tie_bar_normalized_exact": result["segmental_optional_tie_bar_normalized"]["exact_matches"],
                "segmental_coverage": result["segmental_vs_pron_no_tones"]["coverage"],
                "tonal_cer": result["tonal_vs_pron_with_tones"]["cer"],
                "tonal_coverage": result["tonal_vs_pron_with_tones"]["coverage"],
                "tonal_mekong_convention_cer": result["tonal_mekong_convention_vs_pron_with_tones"]["cer"],
                "tone_only_cer_on_segmental_exact": result["tone_only_on_segmental_exact_subset"]["cer"],
                "tone_only_coverage": result["tone_only_on_segmental_exact_subset"]["coverage"],
                "tone_category_error_rate": result["tone_category_on_segmental_exact_subset"]["category_error_rate"],
                "tone_category_exact": result["tone_category_on_segmental_exact_subset"]["exact_match_rate"],
                "tone_category_confusion_aligned_words": result["tone_category_confusion_aligned_words"],
                "tone_category_error_contexts": result["tone_category_error_contexts"],
                "tone_category_word_length_mismatches": result["tone_category_word_length_mismatches"],
                "tone_category_unresolved_words": result["tone_category_on_segmental_exact_subset"]["unresolved_words"],
                "tone_category_coverage": result["tone_category_on_segmental_exact_subset"]["coverage"],
                "tone_category_covered_categories": result["tone_category_on_segmental_exact_subset"]["covered_categories"],
                "tone_category_unresolved_categories": result["tone_category_on_segmental_exact_subset"]["unresolved_categories"],
                "runtime_errors": result["runtime_errors"],
                "status_counts": result["status_counts"],
                "warning_counts": result["warning_counts"],
            }
            for name, result in results.items()
        },
        "report": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 1 if any(result["runtime_errors"] for result in results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())

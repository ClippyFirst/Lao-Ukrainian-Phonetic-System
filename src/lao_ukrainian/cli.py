import argparse
import json
from dataclasses import asdict

from .core import analyze
from .mekongphon_reference_profile import DEFAULT_ENGINE_PROFILE


def main():
    ap = argparse.ArgumentParser(description="Lao → Ukrainian phonetic-graphemic analyzer")
    ap.add_argument("text")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ipa-profile", choices=("vientiane", "mekongphon-reference", "hybrid-deterministic"), default=DEFAULT_ENGINE_PROFILE, help="deterministic source-IPA convention (default: hybrid-deterministic); vientiane selects the explicit Vientiane baseline and mekongphon-reference selects the compatibility profile")
    ap.add_argument(
        "--engine",
        choices=("rules", "mekongphon-tonal", "mekongphon-nontonal", "hybrid-v2"),
        default="rules",
        help="rules is the default; MekongPhon downloads optional neural weights on first use",
    )
    ap.add_argument("--revision", help="Hugging Face model commit SHA (recommended for reproducibility)")
    ap.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    ap.add_argument("--num-beams", type=int, default=5)
    args = ap.parse_args()

    if args.engine == "rules":
        result = analyze(args.text, ipa_profile=args.ipa_profile)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            return
        print(f"Input: {result.input}\nStatus: {result.status}")
        for syllable in result.syllables:
            print(
                f"{syllable.surface}: IPA={syllable.phonemic_ipa} "
                f"→ UA={syllable.practical_ukrainian} [{syllable.status}]"
            )
            if syllable.grapheme_preview is not None:
                preview = syllable.grapheme_preview
                unresolved = "".join(preview.unresolved_graphemes) or "none"
                print(f"  IPA preview={preview.ipa_preview or '—'} [{preview.status}]; unresolved={unresolved}")
        return

    if args.engine == "hybrid-v2":
        if args.ipa_profile != DEFAULT_ENGINE_PROFILE:
            ap.error("--ipa-profile applies only to the deterministic hybrid-v2 base")
        from .hybrid_v2 import run_hybrid_v2
        result = run_hybrid_v2(
            args.text, revision=args.revision, device=args.device,
            num_beams=args.num_beams,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
            return
        print(f"Input: {result.analysis.input}\\nEngine: hybrid-v2")
        print(f"Neural model: {result.model_id}@{result.model_revision}")
        print(f"Neural IPA: {result.neural_raw_ipa}")
        print(f"Tone association: {result.tone_alignment_status}; syllable predictions: {len(result.tone_predictions)}")
        print(f"Ukrainian (deterministic IPA lane): {result.ukrainian}")
        print(f"Tonal IPA (untouched neural lane): {result.tonal_ipa}")
        for prediction in result.tone_predictions:
            print(f"  syllable {prediction.syllable_index + 1} {prediction.source_surface}: {prediction.contour} ({prediction.category}, {prediction.certainty})")
        for syllable in result.analysis.syllables:
            print(
                f"{syllable.surface}: IPA={syllable.phonemic_ipa} "
                f"→ UA={syllable.practical_ukrainian} "
                f"[tone={syllable.tone or '?'}; contour={syllable.tone_contour or '?'}]"
            )
        if result.warnings:
            print("Warnings: " + "; ".join(result.warnings))
        return

    if args.ipa_profile != DEFAULT_ENGINE_PROFILE:
        ap.error("--ipa-profile applies only to --engine rules")

    from .mekongphon import transcribe_lao

    result = transcribe_lao(
        args.text,
        tonal=args.engine == "mekongphon-tonal",
        revision=args.revision,
        device=args.device,
        num_beams=args.num_beams,
    )
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return
    print(f"Input: {result.input}\nEngine: {result.model_id}")
    print(f"Model revision: {result.model_revision}")
    print(f"IPA: {result.raw_ipa}")
    print(f"Ukrainian: {result.ukrainian or 'NOT MAPPED'} [{result.status}]")
    if result.warnings:
        print("Warnings: " + ", ".join(result.warnings))

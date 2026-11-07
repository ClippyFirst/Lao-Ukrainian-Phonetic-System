import argparse
import json
from dataclasses import asdict

from .core import analyze


def main():
    ap = argparse.ArgumentParser(description="Lao → Ukrainian phonetic-graphemic analyzer")
    ap.add_argument("text")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--segment-unspaced", action="store_true", help="infer unique syllable boundaries inside unspaced Lao tokens; ambiguous tokens remain unsplit")
    ap.add_argument(
        "--engine",
        choices=("rules", "mekongphon-tonal", "mekongphon-nontonal"),
        default="rules",
        help="rules is the default; MekongPhon downloads optional neural weights on first use",
    )
    ap.add_argument("--revision", help="Hugging Face model commit SHA (recommended for reproducibility)")
    ap.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    ap.add_argument("--num-beams", type=int, default=4)
    args = ap.parse_args()
    if args.segment_unspaced and args.engine != "rules":
        ap.error("--segment-unspaced is available only with --engine rules")

    if args.engine == "rules":
        result = analyze(args.text, infer_unspaced=args.segment_unspaced)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
            return
        print(f"Input: {result.input}\nStatus: {result.status}")
        for syllable in result.syllables:
            print(
                f"{syllable.surface}: IPA={syllable.phonemic_ipa} "
                f"→ UA={syllable.practical_ukrainian} [{syllable.status}]"
            )
        return

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

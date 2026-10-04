import argparse, json
from dataclasses import asdict
from .core import analyze

def main():
    ap=argparse.ArgumentParser(description="Lao → Ukrainian phonetic-graphemic analyzer")
    ap.add_argument("text"); ap.add_argument("--json",action="store_true")
    args=ap.parse_args(); a=analyze(args.text)
    if args.json:
        print(json.dumps(asdict(a),ensure_ascii=False,indent=2)); return
    print(f"Input: {a.input}\nStatus: {a.status}")
    for s in a.syllables:
        print(f"{s.surface}: IPA={s.phonemic_ipa} → UA={s.practical_ukrainian} [{s.status}]")

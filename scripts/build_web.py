"""Create a static Pages artifact and bundle the optional local Hybrid v2 runtime."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)
for name in ("index.html", "system.html"):
    shutil.copy2(ROOT / name, DIST / name)
shutil.copytree(ROOT / "web", DIST / "web")

ESBUILD = ROOT / "node_modules" / ".bin" / "esbuild"
ORT_DIST = ROOT / "node_modules" / "onnxruntime-web" / "dist"
BUNDLE = DIST / "web" / "hybrid-v2-inference.bundle.js"
if ESBUILD.exists() and ORT_DIST.exists():
    subprocess.run(
        [
            str(ESBUILD),
            str(ROOT / "web" / "hybrid-v2-inference.js"),
            "--bundle",
            "--format=esm",
            "--platform=browser",
            "--target=es2022",
            f"--outfile={BUNDLE}",
        ],
        cwd=ROOT,
        check=True,
    )
    vendor = DIST / "web" / "vendor"
    vendor.mkdir(parents=True, exist_ok=True)
    wasm_files = list(ORT_DIST.rglob("*.wasm"))
    if not wasm_files:
        raise SystemExit("onnxruntime-web installed but no WASM runtime assets were found")
    for source in wasm_files:
        shutil.copy2(source, vendor / source.name)
else:
    # Keep deterministic-only local builds usable without optional model tooling.
    # The deployed Pages and CI workflows install the pinned runtime packages.
    BUNDLE.write_text(
        'export function createHybridV2Inference() { '
        'throw new Error("Hybrid v2 browser runtime dependencies are not installed in this build."); }\n',
        encoding="utf-8",
    )

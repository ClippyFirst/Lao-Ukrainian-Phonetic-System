"""Build the static GitHub Pages site and its generated browser data."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)

for name in ("index.html", "system.html"):
    shutil.copy2(ROOT / name, DIST / name)
shutil.copytree(ROOT / "web", DIST / "web")

# The public service is deterministic/browser-native. Model inference and
# large ONNX/WASM assets are deliberately excluded from the Pages artifact.

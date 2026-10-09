"""Create a minimal static deployment artifact without bundling or rewriting paths."""
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

"""Create a static Pages artifact and bundle the optional local Hybrid v2 runtime."""
from pathlib import Path
import json
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
    metafile = DIST / "hybrid-v2-inference.meta.json"
    subprocess.run(
        [
            str(ESBUILD),
            str(ROOT / "web" / "hybrid-v2-inference.js"),
            "--bundle",
            "--format=esm",
            "--platform=browser",
            "--target=es2022",
            f"--outfile={BUNDLE}",
            f"--metafile={metafile}",
        ],
        cwd=ROOT,
        check=True,
    )
    build_metadata = json.loads(metafile.read_text(encoding="utf-8"))
    metafile.unlink()

    # Preserve the license texts for every npm package actually included in
    # the browser bundle. Build-only tools (for example esbuild) are excluded.
    package_names = set()
    for input_name in build_metadata.get("inputs", {}):
        parts = Path(input_name).parts
        node_modules_indices = [i for i, part in enumerate(parts) if part == "node_modules"]
        if not node_modules_indices:
            continue
        index = node_modules_indices[-1]
        if index + 1 >= len(parts):
            continue
        if parts[index + 1].startswith("@"):
            if index + 2 < len(parts):
                package_names.add("/".join(parts[index + 1:index + 3]))
        else:
            package_names.add(parts[index + 1])

    license_dir = DIST / "web" / "vendor" / "licenses"
    license_dir.mkdir(parents=True, exist_ok=True)
    notice_lines = [
        "# Third-party runtime notices",
        "",
        "The following npm packages are bundled into hybrid-v2-inference.bundle.js.",
        "Their license texts are copied into this directory.",
        "",
    ]
    for package_name in sorted(package_names):
        package_root = ROOT / "node_modules" / package_name
        if not package_root.is_dir():
            raise SystemExit(f"Bundled npm package directory is missing: {package_name}")
        package_metadata = json.loads(
            (package_root / "package.json").read_text(encoding="utf-8")
        )
        license_files = sorted(
            path for path in package_root.iterdir()
            if path.is_file() and (
                path.name.lower().startswith("license")
                or path.name.lower().startswith("notice")
            )
        )
        if not license_files:
            raise SystemExit(
                f"No top-level LICENSE/NOTICE file found for bundled package {package_name}"
            )
        safe_name = package_name.replace("/", "__")
        copied_names = []
        for license_file in license_files:
            target_name = f"{safe_name}-{license_file.name}"
            shutil.copy2(license_file, license_dir / target_name)
            copied_names.append(f"licenses/{target_name}")
        notice_lines.append(
            f"- {package_name}@{package_metadata.get('version', 'unknown')} "
            f"— {package_metadata.get('license', 'UNSPECIFIED')}: "
            + ", ".join(copied_names)
        )
    (DIST / "web" / "vendor" / "THIRD-PARTY-NOTICES.md").write_text(
        "\n".join(notice_lines) + "\n",
        encoding="utf-8",
    )

    vendor = DIST / "web" / "vendor"
    vendor.mkdir(parents=True, exist_ok=True)
    # The application pins the WASM execution provider. Ship only its loader
    # and binary; JSEP/WebGPU, asyncify and JSPI variants are not requested.
    runtime_names = (
        "ort-wasm-simd-threaded.mjs",
        "ort-wasm-simd-threaded.wasm",
    )
    for filename in runtime_names:
        matches = list(ORT_DIST.rglob(filename))
        if len(matches) != 1:
            raise SystemExit(
                f"Expected exactly one ONNX Runtime WASM asset {filename}; found {len(matches)}"
            )
        shutil.copy2(matches[0], vendor / filename)
else:
    # Keep deterministic-only local builds usable without optional model tooling.
    # The deployed Pages and CI workflows install the pinned runtime packages.
    BUNDLE.write_text(
        'export function createHybridV2Inference() { '
        'throw new Error("Hybrid v2 browser runtime dependencies are not installed in this build."); }\n',
        encoding="utf-8",
    )

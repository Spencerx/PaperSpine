#!/usr/bin/env python3
"""Assemble the static V5 website without fetching remote resources."""

from __future__ import annotations

import json
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "website"
OUTPUT = ROOT / "build" / "v5-site"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def public_asset(showcase: Path, relative: str) -> Path:
    path = (showcase / relative).resolve()
    try:
        path.relative_to(showcase.resolve())
    except ValueError as error:
        raise RuntimeError(f"figure asset escapes public showcase: {relative}") from error
    require(path.is_file(), f"missing figure asset: {relative}")
    return path


def verify_figure_showcase() -> dict[str, int | str]:
    showcase = SOURCE / "assets" / "figure-showcase"
    expected_directories = {"01_pdf", "02_images", "03_mobile"}
    actual_directories = {path.name for path in showcase.iterdir() if path.is_dir()}
    require(actual_directories == expected_directories, "unexpected figure-showcase directory set")

    manifest = json.loads((showcase / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("schema") == "paperspine5.figure-showcase/3.0", "invalid figure manifest schema")
    boundary = manifest.get("public_claim_boundary", "").lower()
    require("no literature figure" in boundary and "reference metadata" in boundary, "missing public claim boundary")

    items = manifest.get("items", [])
    require([item["task"]["id"] for item in items] == [str(value) for value in range(301, 309)], "figure IDs must be 301-308")
    kinds = [item["task"]["kind"] for item in items]
    require(kinds.count("SCHEMATIC") == 4 and kinds.count("DATA FIGURE") == 4, "figure kind split must be 4 + 4")

    expected_keys = {"paperspine_png", "paperspine_svg", "mobile_detail"}
    for item in items:
        task_id = item["task"]["id"]
        require(set(item["assets"]) == expected_keys, f"unexpected public asset set: {task_id}")
        for label, relative in item["assets"].items():
            path = public_asset(showcase, relative)
            require(sha256(path) == item["sha256"][label], f"figure asset checksum drift: {task_id}/{label}")

    walls = manifest.get("mobile_surfaces", {}).get("walls", [])
    require(len(walls) == 4, "mobile wall count must be four")
    for wall in walls:
        path = public_asset(showcase, wall["path"])
        require(sha256(path) == wall["sha256"], f"mobile wall checksum drift: {wall['path']}")

    combined = manifest.get("combined_pdf", {})
    require(combined.get("pages") == 8, "combined vector PDF must contain eight declared pages")
    pdf = public_asset(showcase, combined["path"])
    require(sha256(pdf) == combined["sha256"], "combined vector PDF checksum drift")

    main_surfaces = [SOURCE / "index.html", SOURCE / "en" / "index.html"]
    for page in main_surfaces:
        content = page.read_text(encoding="utf-8")
        require(content.count('id="official-reference"') == 1, f"missing official reference section: {page}")
        require(content.count('class="pdf-reference-object"') == 1, f"missing embedded PDF reader: {page}")
        require("paperspine5-figure-studies-publication.pdf" in content, f"missing PDF download link: {page}")

    gallery_surfaces = [SOURCE / "figure-studies" / "index.html", SOURCE / "en" / "figure-studies" / "index.html"]
    require(all(page.is_file() for page in gallery_surfaces), "missing bilingual figure gallery")
    require(len([path for path in showcase.rglob("*") if path.is_file()]) == 32, "public figure package must contain exactly 32 files")
    return {"items": 8, "pdf_pages": 8, "files": 32, "pdf_sha256": combined["sha256"]}


def main() -> int:
    manifest = json.loads((SOURCE / "downloads" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("product") != "PaperSpine5" or len(manifest.get("artifacts", [])) != 4:
        raise RuntimeError("refusing to build from an invalid PaperSpine5 manifest")
    figure_evidence = verify_figure_showcase()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    print(json.dumps({"site": str(OUTPUT), "figure_showcase": figure_evidence}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

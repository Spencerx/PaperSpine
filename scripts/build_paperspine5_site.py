#!/usr/bin/env python3
"""Assemble the static V5 website without fetching remote resources."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "website"
OUTPUT = ROOT / "build" / "v5-site"


def main() -> int:
    manifest = json.loads((SOURCE / "downloads" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("product") != "PaperSpine5" or len(manifest.get("artifacts", [])) != 4:
        raise RuntimeError("refusing to build from an invalid PaperSpine5 manifest")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(SOURCE, OUTPUT)
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

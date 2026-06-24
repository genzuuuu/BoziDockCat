#!/usr/bin/env python3
"""Build a minimal .icns from a 1024x1024 PNG source."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

SIZES = [16, 32, 64, 128, 256, 512, 1024]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: make_app_icon_icns.py <source.png> <output.icns>")

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    src = Image.open(source).convert("RGBA")

    with tempfile.TemporaryDirectory() as tmp:
        iconset = Path(tmp) / "AppIcon.iconset"
        iconset.mkdir()
        for size in SIZES:
            resized = src.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(iconset / f"icon_{size}x{size}.png")
            if size <= 512:
                resized.save(iconset / f"icon_{size}x{size}@2x.png")
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset), "-o", str(output)],
            check=True,
        )


if __name__ == "__main__":
    main()

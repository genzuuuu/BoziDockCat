#!/usr/bin/env python3
"""Remove magenta chroma key background and export DockCat-ready PNG assets."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path("/Users/zu/.cursor/projects/Users-zu-Dropbox-DockCat/assets")
DEFAULT_CAT = ROOT / "DockCatApp/DockCat/Resources/DefaultCat"
CAT_PACK = ROOT / "CatPacks/bozi"
MANIFEST_TEMPLATE = ROOT / "CatPacks/bozi/manifest.json"

MAPPING = {
    "bozi_dialogue_v2.png": "poses/dialogue/stand.png",
    "bozi_side_v2.png": "poses/resting/side.png",
    "bozi_loaf_v2.png": "poses/resting/loaf.png",
    "bozi_spluff.png": "poses/resting/spluff.png",
    "bozi_held_v2.png": "poses/held/held.png",
    "bozi_stretch_v2.png": "poses/transition/stretch.png",
    "bozi_walk_01.png": "animations/walk/walk_01.png",
    "bozi_walk_02.png": "animations/walk/walk_02.png",
    "bozi_walk_03.png": "animations/walk/walk_03.png",
    "bozi_walk_04.png": "animations/walk/walk_04.png",
    "bozi_icon_sleep.png": "app_icons/icon_sleep.png",
    "bozi_icon_empty.png": "app_icons/icon_empty.png",
}


def chroma_key_magenta(img: Image.Image, tolerance: int = 55) -> Image.Image:
    rgba = img.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if r > 255 - tolerance and g < tolerance and b > 255 - tolerance:
                pixels[x, y] = (r, g, b, 0)
            elif r > 200 and g < 80 and b > 200:
                pixels[x, y] = (r, g, b, 0)
    return rgba


def fit_canvas(img: Image.Image, size: int = 1024) -> Image.Image:
    rgba = img.convert("RGBA")
    bbox = rgba.getbbox()
    if not bbox:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cropped = rgba.crop(bbox)
    scale = min(size * 0.84 / cropped.width, size * 0.84 / cropped.height)
    new_w = max(1, int(cropped.width * scale))
    new_h = max(1, int(cropped.height * scale))
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - new_w) // 2, size - new_h - int(size * 0.08))
    canvas.paste(resized, offset, resized)
    return canvas


def export_pack(target_root: Path, manifest_src: Path) -> None:
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_src, target_root / "manifest.json")
    for src_name, rel_path in MAPPING.items():
        src = ASSETS / src_name
        if not src.exists():
            raise FileNotFoundError(src)
        dst = target_root / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        processed = fit_canvas(chroma_key_magenta(Image.open(src)))
        processed.save(dst, "PNG")


def main() -> None:
    if not MANIFEST_TEMPLATE.exists():
        raise FileNotFoundError(MANIFEST_TEMPLATE)
    export_pack(DEFAULT_CAT, MANIFEST_TEMPLATE)
    export_pack(CAT_PACK, MANIFEST_TEMPLATE)
    print(f"Exported Bozi assets to {DEFAULT_CAT} and {CAT_PACK}")


if __name__ == "__main__":
    main()

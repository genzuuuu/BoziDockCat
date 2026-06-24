#!/usr/bin/env python3
"""Compose BoziDockCat README preview images from sprite assets."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "README_figs"
ASSETS = ROOT / "DockCatApp/DockCat/Resources/DefaultCat"
REFS = ROOT / "bozi/references/IMG_2425.JPG"

W, H = 780, 520
DOCK_H = 92
BG = (28, 30, 38)
DOCK = (52, 54, 62, 235)
DOCK_LINE = (90, 92, 102)


def load_sprite(rel: str, scale: float = 0.42) -> Image.Image:
    img = Image.open(ASSETS / rel).convert("RGBA")
    nw = max(1, int(img.width * scale))
    nh = max(1, int(img.height * scale))
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def canvas() -> Image.Image:
    base = Image.new("RGBA", (W, H), BG + (255,))
    draw = ImageDraw.Draw(base)
    draw.rectangle((0, H - DOCK_H, W, H), fill=DOCK)
    draw.line((0, H - DOCK_H, W, H - DOCK_H), fill=DOCK_LINE, width=2)
    for x in range(24, W, 58):
        draw.ellipse((x, H - 24, x + 10, H - 14), fill=(120, 122, 132, 180))
    return base


def paste_cat(base: Image.Image, sprite: Image.Image, x: int, ground_y: int) -> None:
    base.paste(sprite, (x, ground_y - sprite.height), sprite)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def speech_bubble(draw: ImageDraw.ImageDraw, x: int, y: int, text: str) -> None:
    f = font(28)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 22, 16
    rect = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    draw.rounded_rectangle(rect, radius=18, fill=(255, 255, 255, 245), outline=(210, 210, 220))
    draw.polygon([(x + 36, rect[3] - 1), (x + 24, rect[3] + 16), (x + 58, rect[3] - 1)], fill=(255, 255, 255, 245))
    draw.text((x + pad_x, y + pad_y - 2), text, fill=(40, 40, 48), font=f)


def save_jpg(img: Image.Image, path: Path) -> None:
    rgb = Image.new("RGB", img.size, BG)
    rgb.paste(img, mask=img.split()[3])
    rgb.save(path, "JPEG", quality=92)


def make_stretch() -> None:
    base = canvas()
    sprite = load_sprite("poses/transition/stretch.png", 0.4)
    paste_cat(base, sprite, 300, H - DOCK_H - 8)
    save_jpg(base, FIGS / "bozi_stretch.jpg")


def make_walk() -> None:
    base = canvas()
    sprite = load_sprite("animations/walk/walk_02.png", 0.36)
    paste_cat(base, sprite, 360, H - DOCK_H - 6)
    save_jpg(base, FIGS / "bozi_walk.jpg")


def make_reminder() -> None:
    base = canvas()
    sprite = load_sprite("poses/dialogue/stand.png", 0.38)
    paste_cat(base, sprite, 310, H - DOCK_H - 6)
    draw = ImageDraw.Draw(base)
    speech_bubble(draw, 180, 90, "妈妈，该喝水啦")
    save_jpg(base, FIGS / "bozi_water_reminder.jpg")


def make_portrait() -> None:
    ref = Image.open(REFS).convert("RGB")
    ref.thumbnail((360, 360), Image.Resampling.LANCZOS)
    base = Image.new("RGBA", (400, 400), (245, 247, 252, 255))
    offset = ((400 - ref.width) // 2, (400 - ref.height) // 2)
    base.paste(ref, offset)
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((0, 0, 399, 399), radius=24, outline=(210, 214, 224), width=3)
    f = font(34)
    draw.text((18, 350), "波子", fill=(50, 50, 60), font=f)
    base.convert("RGB").save(FIGS / "bozi_portrait.jpg", "JPEG", quality=92)


def main() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    make_stretch()
    make_walk()
    make_reminder()
    make_portrait()
    print(f"Wrote README figures to {FIGS}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Copyright (C) 2026 Danny Nunez
"""Render deterministic native-resolution browser UI concepts for Phase 1."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 240
HEIGHT = 160
DOCK_TOP = 140

# These are the 20 background colors available to the production UI. Cove
# artwork continues to use background palette indices 20-239.
UI_COLORS = {
    "navy": "#061A4A",
    "deep_blue": "#07336E",
    "blue": "#07509A",
    "stripe": "#0B68B8",
    "stripe_light": "#1380CC",
    "card": "#CDEFF3",
    "card_light": "#F1FFFF",
    "card_shadow": "#05295D",
    "card_edge": "#4BB4D4",
    "orange": "#FF6B2C",
    "orange_shadow": "#A9371E",
    "cyan": "#1FC4D4",
    "cyan_dark": "#087E9B",
    "lime": "#A5D92B",
    "white": "#FFFFFF",
    "muted": "#78A9B8",
    "yellow": "#FFD050",
    "danger": "#E44A4A",
    "disabled": "#718493",
    "black": "#000000",
}

GLOW_VARIANTS = {
    "cyan": ("#1FC4D4", "#087E9B"),
    "lime": ("#B8F23A", "#4E8519"),
    "ice": ("#FFFFFF", "#78A9B8"),
}


GAMES = [
    "Metal Slug Advance",
    "The Minish Cap",
    "Mario Kart - Super Circuit",
    "Metroid Fusion",
    "Castlevania - Aria of Sorrow",
    "Advance Wars",
]


def box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str,
        outline: str, shadow: str | None = None, glow: bool = False) -> None:
    """Draw a two-pixel chamfered handheld-style panel."""
    x0, y0, x1, y1 = xy
    if glow and shadow:
        draw.rectangle((x0 - 2, y0 - 2, x1 + 2, y1 + 2), outline=shadow)
        draw.rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), outline=outline)
    if shadow:
        draw.polygon(
            [(x0 + 3, y0 + 2), (x1 - 1, y0 + 2), (x1 + 2, y0 + 5),
             (x1 + 2, y1 - 1), (x1 - 1, y1 + 2), (x0 + 3, y1 + 2),
             (x0, y1 - 1), (x0, y0 + 5)],
            fill=shadow,
        )
    draw.polygon(
        [(x0 + 3, y0), (x1 - 3, y0), (x1, y0 + 3), (x1, y1 - 3),
         (x1 - 3, y1), (x0 + 3, y1), (x0, y1 - 3), (x0, y0 + 3)],
        fill=outline,
    )
    draw.polygon(
        [(x0 + 4, y0 + 2), (x1 - 4, y0 + 2), (x1 - 2, y0 + 4),
         (x1 - 2, y1 - 4), (x1 - 4, y1 - 2), (x0 + 4, y1 - 2),
         (x0 + 2, y1 - 4), (x0 + 2, y0 + 4)],
        fill=fill,
    )


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def fit_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont,
             max_width: int) -> str:
    if text_width(draw, text, font) <= max_width:
        return text
    suffix = "..."
    while text and text_width(draw, text + suffix, font) > max_width:
        text = text[:-1]
    return text + suffix


def draw_background(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, WIDTH - 1, DOCK_TOP - 1), fill=UI_COLORS["blue"])
    for y in range(1, DOCK_TOP, 4):
        draw.line((0, y, WIDTH - 1, y), fill=UI_COLORS["stripe"])
    for y in range(3, DOCK_TOP, 8):
        draw.line((0, y, WIDTH - 1, y), fill=UI_COLORS["stripe_light"])


def draw_cover(image: Image.Image, draw: ImageDraw.ImageDraw, cover: Image.Image,
               state: str = "ready", glow: tuple[str, str] | None = None) -> None:
    x, y = 6, 34
    edge, shadow = glow or (UI_COLORS["orange"], UI_COLORS["orange_shadow"])
    box(draw, (4, 32, 79, 107), UI_COLORS["card_light"], edge, shadow,
        glow=glow is not None)
    if state == "ready":
        image.paste(cover.resize((72, 72), Image.Resampling.NEAREST), (x, y))
    elif state == "folder":
        draw.rectangle((20, 58, 63, 89), fill=UI_COLORS["yellow"])
        draw.rectangle((24, 54, 41, 59), fill=UI_COLORS["yellow"])
        draw.rectangle((24, 64, 59, 83), outline=UI_COLORS["orange_shadow"], width=2)
    else:
        draw.rectangle((x, y, x + 71, y + 71), fill=UI_COLORS["deep_blue"])
        label = "NO COVER" if state == "missing" else "INVALID"
        fill = UI_COLORS["muted"] if state == "missing" else UI_COLORS["danger"]
        font = ImageFont.load_default()
        w = text_width(draw, label, font)
        draw.text((42 - w // 2, 62), label, font=font, fill=fill)


def draw_file_badge(draw: ImageDraw.ImageDraw, x: int, y: int, state: str) -> None:
    if state == "folder":
        draw.rectangle((x, y + 3, x + 9, y + 9), fill=UI_COLORS["yellow"])
        draw.rectangle((x + 1, y + 1, x + 5, y + 4), fill=UI_COLORS["yellow"])
    elif state == "unsupported":
        draw.rectangle((x, y, x + 8, y + 10), fill=UI_COLORS["disabled"])
        draw.line((x + 2, y + 3, x + 6, y + 7), fill=UI_COLORS["danger"])
        draw.line((x + 6, y + 3, x + 2, y + 7), fill=UI_COLORS["danger"])
    else:
        draw.rectangle((x, y + 1, x + 9, y + 9), fill=UI_COLORS["lime"])
        draw.rectangle((x + 2, y + 3, x + 7, y + 7), fill=UI_COLORS["deep_blue"])


def draw_rows(draw: ImageDraw.ImageDraw, row_count: int, state_sheet: bool = False,
              glow: tuple[str, str] | None = None) -> None:
    list_left, list_right = 86, 235
    if row_count == 5:
        top, height, gap = 4, 24, 3
    elif row_count == 6:
        top, height, gap = 4, 19, 3
    else:
        raise ValueError("row_count must be 5 or 6")

    font = ImageFont.load_default()
    states = ["game", "folder", "parent", "unsupported", "game", "game"] if state_sheet else ["game"] * 6
    names = [
        "Metal Slug Advance",
        "Action Games",
        ".. Parent Folder",
        "Readme.txt",
        "Castlevania - Aria of Sorrow",
        "Advance Wars",
    ] if state_sheet else GAMES
    selected_edge, selected_shadow = glow or (
        UI_COLORS["orange"], UI_COLORS["orange_shadow"]
    )

    for index in range(row_count):
        y0 = top + index * (height + gap)
        y1 = y0 + height - 1
        selected = index == 0
        fill = UI_COLORS["card_light"] if selected else UI_COLORS["card"]
        edge = selected_edge if selected else UI_COLORS["card_edge"]
        shadow = selected_shadow if selected else UI_COLORS["card_shadow"]
        box(draw, (list_left, y0, list_right, y1), fill, edge, shadow,
            glow=selected and glow is not None)

        state = states[index]
        badge_state = "folder" if state in {"folder", "parent"} else state
        draw_file_badge(draw, list_left + 6, y0 + max(2, (height - 11) // 2), badge_state)

        max_width = list_right - (list_left + 23) - 5
        shown = fit_text(draw, names[index], font, max_width)
        text_y = y0 + (height - 8) // 2 - 1
        color = UI_COLORS["navy"] if state != "unsupported" else UI_COLORS["disabled"]
        draw.text((list_left + 22, text_y), shown, font=font, fill=color)

        if selected:
            draw.polygon(
                [(list_left - 5, y0 + height // 2), (list_left - 1, y0 + height // 2 - 4),
                 (list_left - 1, y0 + height // 2 + 4)],
                fill=selected_edge,
            )


def draw_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, y: int, active: bool) -> None:
    color = UI_COLORS["white"] if active else UI_COLORS["muted"]
    accent = UI_COLORS["lime"] if active else UI_COLORS["cyan_dark"]
    if kind == "browse":
        draw.ellipse((cx - 5, y, cx + 2, y + 7), outline=color, width=2)
        draw.line((cx + 1, y + 7, cx + 5, y + 11), fill=accent, width=2)
    elif kind == "recent":
        draw.ellipse((cx - 5, y, cx + 5, y + 10), outline=color, width=2)
        draw.line((cx, y + 5, cx, y + 1), fill=accent)
        draw.line((cx, y + 5, cx + 3, y + 6), fill=accent)
    elif kind == "settings":
        draw.rectangle((cx - 4, y + 1, cx + 4, y + 9), outline=color)
        draw.line((cx - 6, y + 3, cx + 6, y + 3), fill=accent)
        draw.line((cx - 6, y + 7, cx + 6, y + 7), fill=accent)
    else:
        draw.line((cx - 5, y + 1, cx + 5, y + 10), fill=color, width=2)
        draw.line((cx + 4, y + 1, cx - 5, y + 10), fill=accent, width=2)


def draw_dock(draw: ImageDraw.ImageDraw, selected: int = 0,
              glow: tuple[str, str] | None = None) -> None:
    draw.rectangle((0, DOCK_TOP, WIDTH - 1, HEIGHT - 1), fill=UI_COLORS["navy"])
    draw.line((0, DOCK_TOP, WIDTH - 1, DOCK_TOP), fill=UI_COLORS["cyan"])
    labels = [("browse", "BROWSE"), ("recent", "RECENT"),
              ("settings", "SETUP"), ("tools", "TOOLS")]
    active_edge, active_fill = glow or (UI_COLORS["cyan"], UI_COLORS["cyan_dark"])
    font = ImageFont.load_default()
    for index, (kind, label) in enumerate(labels):
        x0 = index * 60
        if index == selected:
            draw.rectangle((x0 + 1, DOCK_TOP + 2, x0 + 58, HEIGHT - 2), fill=active_fill)
            draw.line((x0 + 2, DOCK_TOP + 2, x0 + 57, DOCK_TOP + 2), fill=active_edge)
            draw.line((x0 + 2, HEIGHT - 2, x0 + 57, HEIGHT - 2), fill=active_edge)
        if index:
            draw.line((x0, DOCK_TOP + 3, x0, HEIGHT - 3), fill=UI_COLORS["deep_blue"])
        icon_center = x0 + 10
        draw_icon(draw, kind, icon_center, DOCK_TOP + 4, index == selected)
        label_width = text_width(draw, label, font)
        draw.text((x0 + 19, DOCK_TOP + 5), label, font=font,
                  fill=UI_COLORS["white"] if index == selected else UI_COLORS["muted"])


def render(row_count: int, cover: Image.Image, state_sheet: bool = False,
           glow: tuple[str, str] | None = None) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), UI_COLORS["blue"])
    draw = ImageDraw.Draw(image)
    # Pillow's default font can otherwise introduce antialias shades that do
    # not exist in the GBA palette. Force binary glyph coverage.
    draw.fontmode = "1"
    draw_background(draw)
    draw_cover(image, draw, cover, "folder" if state_sheet else "ready", glow)
    draw_rows(draw, row_count, state_sheet, glow)
    draw_dock(draw, glow=glow)
    return image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--glow-output-dir", type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cover = Image.open(args.cover).convert("RGB")
    outputs = {
        "browser-native-5-row.png": render(5, cover),
        "browser-native-6-row.png": render(6, cover),
        "browser-native-states.png": render(5, cover, state_sheet=True),
    }
    for name, image in outputs.items():
        image.save(args.output_dir / name, optimize=True)
        enlarged = image.resize((WIDTH * 4, HEIGHT * 4), Image.Resampling.NEAREST)
        enlarged.save(args.output_dir / name.replace(".png", "-4x.png"), optimize=True)

    if args.glow_output_dir:
        args.glow_output_dir.mkdir(parents=True, exist_ok=True)
        for name, glow in GLOW_VARIANTS.items():
            image = render(6, cover, glow=glow)
            image.save(args.glow_output_dir / f"{name}-glow.png", optimize=True)
            enlarged = image.resize((WIDTH * 4, HEIGHT * 4), Image.Resampling.NEAREST)
            enlarged.save(args.glow_output_dir / f"{name}-glow-4x.png", optimize=True)


if __name__ == "__main__":
    main()

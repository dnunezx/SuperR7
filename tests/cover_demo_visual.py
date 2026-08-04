from __future__ import annotations

from pathlib import Path
import os

from PIL import Image, ImageChops


SCREENSHOT_DIR = Path(os.environ.get("COVER_DEMO_SCREENSHOTS", "artifacts/cover-demo"))
PANEL_BOX = (164, 42, 240, 118)
PANEL_IMAGE = (166, 44, 238, 116)
FRAME_SIZE = 512 + 240 * 160


def render_frame(path: Path) -> Image.Image:
    data = path.read_bytes()
    if len(data) != FRAME_SIZE:
        raise AssertionError(f"{path.name} is {len(data)} bytes, expected {FRAME_SIZE}")

    palette = []
    for offset in range(0, 512, 2):
        color = int.from_bytes(data[offset : offset + 2], "little")
        palette.append(
            (
                (color & 0x1F) * 255 // 31,
                ((color >> 5) & 0x1F) * 255 // 31,
                ((color >> 10) & 0x1F) * 255 // 31,
            )
        )

    image = Image.new("RGB", (240, 160))
    image.putdata([palette[index] for index in data[512:]])
    return image


def load(name: str) -> Image.Image:
    path = SCREENSHOT_DIR / f"{name}.png"
    frame_path = SCREENSHOT_DIR / f"{name}.frame"
    if frame_path.exists():
        image = render_frame(frame_path)
        image.save(path)
    elif path.exists():
        image = Image.open(path).convert("RGB")
    else:
        raise AssertionError(f"missing emulator frame dump: {frame_path}")
    if image.size != (240, 160):
        raise AssertionError(f"{path.name} is {image.size}, expected native 240x160")
    return image


def changed_pixels(first: Image.Image, second: Image.Image) -> int:
    difference = ImageChops.difference(first, second)
    return sum(pixel != (0, 0, 0) for pixel in difference.getdata())


def assert_outside_panel_equal(first: Image.Image, second: Image.Image) -> None:
    regions = (
        (0, 0, 240, PANEL_BOX[1]),
        (0, PANEL_BOX[3], 240, 160),
        (0, PANEL_BOX[1], PANEL_BOX[0], PANEL_BOX[3]),
    )
    for region in regions:
        if ImageChops.difference(first.crop(region), second.crop(region)).getbbox():
            raise AssertionError(f"framebuffer changed outside cover panel at {region}")


def main() -> None:
    aurora = load("browse-aurora-ready")
    pending = load("browse-checker-pending")
    checker = load("browse-checker-ready")
    stable = load("browse-checker-stable")
    missing = load("browse-missing")
    invalid = load("browse-invalid")
    recent = load("recent-aurora-ready")

    aurora_panel = aurora.crop(PANEL_IMAGE)
    checker_panel = checker.crop(PANEL_IMAGE)
    if len(aurora_panel.getcolors(maxcolors=4096) or ()) < 7:
        raise AssertionError("Aurora cover did not render its expected color range")
    if len(checker_panel.getcolors(maxcolors=4096) or ()) < 7:
        raise AssertionError("Checker cover did not render its expected color range")
    if changed_pixels(aurora_panel, checker_panel) < 2500:
        raise AssertionError("navigation did not replace the first cover with the second")

    assert_outside_panel_equal(pending, checker)
    if ImageChops.difference(checker, stable).getbbox():
        raise AssertionError("two settled frames differ; possible partial update or flicker")

    missing_panel = missing.crop(PANEL_IMAGE)
    invalid_panel = invalid.crop(PANEL_IMAGE)
    if len(missing_panel.getcolors(maxcolors=32) or ()) > 3:
        raise AssertionError("missing-cover placeholder contains unexpected palette colors")
    if len(invalid_panel.getcolors(maxcolors=32) or ()) > 3:
        raise AssertionError("invalid-cover placeholder contains unexpected palette colors")
    if changed_pixels(missing_panel, invalid_panel) < 10:
        raise AssertionError("missing and corrupt covers did not produce distinct placeholders")

    if ImageChops.difference(aurora_panel, recent.crop(PANEL_IMAGE)).getbbox():
        raise AssertionError("Recent Games did not render the same cached-format Aurora cover")

    print("mGBA cover-art visual checks passed")


if __name__ == "__main__":
    main()

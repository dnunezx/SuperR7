# Copyright (C) 2026 Danny Nunez

from __future__ import annotations

from pathlib import Path

import cover_demo_visual as visual


CAPTURES = Path("artifacts/phase5-loading-v3")
FRAME_SIZE = 512 + 240 * 160
LOADING_NAMES = (
    "loading-electric-blue",
    "loading-mutant-green",
    "loading-chrome-silver",
)


def frame(name: str) -> bytes:
    data = (CAPTURES / f"{name}.frame").read_bytes()
    if len(data) != FRAME_SIZE:
        raise AssertionError(f"{name} frame has {len(data)} bytes")
    return data


def pixel(data: bytes, x: int, y: int) -> int:
    return data[512 + y * 240 + x]


def palette(data: bytes, index: int) -> int:
    return int.from_bytes(data[index * 2:index * 2 + 2], "little")


def gba_bgr555(rgb: int) -> int:
    return ((rgb >> 19) & 0x1F) | ((rgb >> 6) & 0x3E0) | ((rgb << 7) & 0x7C00)


def main() -> None:
    expected = {
        "loading-electric-blue": (0x071424, 0x3B82FF, 0x00E5FF),
        "loading-mutant-green": (0x171A21, 0x39FF70, 0x39FF70),
        "loading-chrome-silver": (0xD7DCE5, 0x171A21, 0xFFFFFF),
    }
    for name, (background, accent, selection) in expected.items():
        data = frame(name)
        if palette(data, 2) != gba_bgr555(background):
            raise AssertionError(f"{name} lost its themed background")
        if palette(data, 11) != gba_bgr555(accent):
            raise AssertionError(f"{name} lost its themed progress fill")
        if palette(data, 9) != gba_bgr555(selection):
            raise AssertionError(f"{name} lost its themed selection glow")

        if pixel(data, 100, 80) != 11:
            raise AssertionError(f"{name} progress fill does not use Accent")
        if pixel(data, 220, 80) != 5:
            raise AssertionError(f"{name} progress track does not use Card")
        if pixel(data, 88, 80) != 9:
            raise AssertionError(f"{name} progress border does not use Selection")
        if pixel(data, 0, 144) != 11 or pixel(data, 125, 150) != 1:
            raise AssertionError(f"{name} loading footer is not theme-aware")

        visual.render_frame(CAPTURES / f"{name}.frame").save(
            CAPTURES / f"{name}.png"
        )

    if len({frame(name)[512:] for name in LOADING_NAMES}) != len(LOADING_NAMES):
        raise AssertionError("loading preset captures are not visually distinct")

    returned = frame("loading-returned-to-launch")
    if pixel(returned, 88, 40) != 6:
        raise AssertionError("B did not return from loading to Quick Launch")
    visual.render_frame(CAPTURES / "loading-returned-to-launch.frame").save(
        CAPTURES / "loading-returned-to-launch.png"
    )

    print("Phase 5 themed loading visual checks passed")


if __name__ == "__main__":
    main()

# Copyright (C) 2026 Danny Nunez

from __future__ import annotations

from pathlib import Path

import cover_demo_visual as visual


CAPTURES = Path("artifacts/ingame-menu")
FRAME_SIZE = 512 + 240 * 160
NAMES = (
    "main", "reset", "save", "rtc", "rtc-update-selected",
    "rtc-updated-popup", "savestates", "cheats",
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


def main() -> None:
    for name in NAMES:
        visual.render_frame(CAPTURES / f"{name}.frame").save(
            CAPTURES / f"{name}.png"
        )

    main_frame = frame("main")
    # Appearance roles are copied to palette indices 16..35.
    if palette(main_frame, 16 + 2) != 0x1040:
        raise AssertionError("in-game background did not inherit Electric Blue navy")
    if palette(main_frame, 16 + 11) != 0x7E07:
        raise AssertionError("in-game accent did not inherit Electric Blue blue")
    if palette(main_frame, 16 + 9) != 0x7F80:
        raise AssertionError("in-game selection did not inherit Electric Blue cyan")

    selected = 16 + 6
    card = 16 + 5
    if pixel(main_frame, 120, 30) != selected:
        raise AssertionError("main selected row is not a selected card")
    for row in range(1, 6):
        if pixel(main_frame, 120, 30 + row * 19) != card:
            raise AssertionError(f"main row {row + 1} is not an unselected card")
    if pixel(main_frame, 120, 150) != 16 + 1:
        raise AssertionError("in-game footer did not use the derived deep color")

    states = [frame(name)[512:] for name in NAMES]
    if len(set(states)) != len(states):
        raise AssertionError("in-game menu states are not visually distinct")
    if pixel(frame("rtc-update-selected"), 120, 116) != 16 + 6:
        raise AssertionError("RTC update action did not receive selected-card styling")
    if pixel(frame("rtc-updated-popup"), 11, 58) != 16 + 9:
        raise AssertionError("RTC confirmation did not render the card dialog edge")
    if pixel(frame("savestates"), 120, 30) != 16 + 6:
        raise AssertionError("savestate carousel did not use selected-card styling")
    if pixel(frame("cheats"), 120, 35) != 16 + 6:
        raise AssertionError("cheat list did not use selected-card styling")

    print("SuperR7 in-game menu visual checks passed")


if __name__ == "__main__":
    main()

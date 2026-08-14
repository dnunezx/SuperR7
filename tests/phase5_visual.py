# Copyright (C) 2026 Danny Nunez (dnunezx)

from __future__ import annotations

from pathlib import Path

import cover_demo_visual as visual


CAPTURES = Path("artifacts/phase5-v3")
FRAME_SIZE = 512 + 240 * 160
CAPTURE_NAMES = (
    "interface", "settings-start", "settings-save",
    "info-superr7", "info-flash", "info-patch-db", "info-sd-card",
)


def frame(name: str) -> bytes:
    data = (CAPTURES / f"{name}.frame").read_bytes()
    if len(data) != FRAME_SIZE:
        raise AssertionError(f"{name} frame has {len(data)} bytes")
    return data


def pixel(data: bytes, x: int, y: int) -> int:
    return data[512 + y * 240 + x]


def assert_rows(name: str, count: int, selected: int) -> None:
    data = frame(name)
    for row in range(count):
        expected = 6 if row == selected else 5
        actual = pixel(data, 120, 10 + row * 20)
        if actual != expected:
            raise AssertionError(
                f"{name} row {row + 1} uses {actual}, expected {expected}"
            )
    for y in (21, 41, 61, 81, 101, 121, 141):
        if pixel(data, 10, y) in (5, 6):
            raise AssertionError(f"{name} card extends into row gap y={y}")


def main() -> None:
    assert_rows("interface", 5, 0)
    assert_rows("settings-start", 7, 1)
    assert_rows("settings-save", 7, 6)
    assert_rows("info-superr7", 5, 0)
    assert_rows("info-flash", 4, 0)
    assert_rows("info-patch-db", 3, 0)
    assert_rows("info-sd-card", 4, 0)

    info = [frame(name)[512:] for name in (
        "info-superr7", "info-flash", "info-patch-db", "info-sd-card"
    )]
    if len(set(info)) != 4:
        raise AssertionError("System Information pages are not visually distinct")

    for name in CAPTURE_NAMES:
        data = frame(name)
        if pixel(data, 185, 150) != 12:
            raise AssertionError(f"{name} does not keep Tools selected in the dock")
        if pixel(data, 11, 148) != 13:
            raise AssertionError(f"{name} lost readable unselected dock text")

        visual.render_frame(CAPTURES / f"{name}.frame").save(
            CAPTURES / f"{name}.png"
        )

    print("Phase 5 secondary-screen visual checks passed")


if __name__ == "__main__":
    main()

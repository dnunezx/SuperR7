# Copyright (C) 2026 Danny Nunez

from __future__ import annotations

from pathlib import Path

import cover_demo_visual as visual


CAPTURES = Path("artifacts/phase5-popups-v3")
FRAME_SIZE = 512 + 240 * 160
CAPTURE_NAMES = (
    "launch-quick", "launch-quick-options", "launch-quick-details",
    "launch-details", "launch-options", "launch-advanced",
    "save-actions", "file-actions", "firmware-update",
    "confirm-no", "confirm-yes", "rtc-year", "rtc-month",
    "settings-alert",
)


def frame(name: str) -> bytes:
    data = (CAPTURES / f"{name}.frame").read_bytes()
    if len(data) != FRAME_SIZE:
        raise AssertionError(f"{name} frame has {len(data)} bytes")
    return data


def pixel(data: bytes, x: int, y: int) -> int:
    return data[512 + y * 240 + x]


def assert_rows(
    name: str, count: int, selected: int | None, row_top: int = 0
) -> None:
    data = frame(name)
    for row in range(count):
        expected = 6 if selected is not None and row == selected else 5
        actual = pixel(data, 6, row_top + 10 + row * 20)
        if actual != expected:
            raise AssertionError(
                f"{name} row {row + 1} uses {actual}, expected {expected}"
            )


def assert_launch(name: str, selected: int) -> None:
    data = frame(name)
    centers = (12, 40, 74, 105)
    for row, y in enumerate(centers):
        expected = 6 if row == selected else 5
        actual = pixel(data, 6 if row == 0 else 88, y)
        if actual != expected:
            raise AssertionError(
                f"{name} launch card {row + 1} uses {actual}, expected {expected}"
            )


def main() -> None:
    assert_launch("launch-quick", 1)
    assert_launch("launch-quick-options", 2)
    assert_launch("launch-quick-details", 3)
    assert_rows("launch-details", 6, None)
    assert_rows("launch-options", 6, 1)
    assert_rows("launch-advanced", 6, 1)
    assert_rows("save-actions", 4, 0, 18)
    assert_rows("file-actions", 2, 0, 18)
    assert_rows("firmware-update", 3, 2, 28)
    assert_rows("confirm-no", 3, 1, 28)
    assert_rows("confirm-yes", 3, 2, 28)
    assert_rows("rtc-year", 3, 1, 28)
    assert_rows("rtc-month", 3, 1, 28)
    assert_rows("settings-alert", 2, 1, 40)

    if frame("confirm-no")[512:] == frame("confirm-yes")[512:]:
        raise AssertionError("confirmation selection did not move")
    if frame("rtc-year")[512:] == frame("rtc-month")[512:]:
        raise AssertionError("RTC field selection did not move")

    quick_states = (
        frame("launch-quick"), frame("launch-quick-options"),
        frame("launch-quick-details"),
    )
    covers = []
    for data in quick_states:
        covers.append(bytes(
            pixel(data, x, y)
            for y in range(33, 109)
            for x in range(4, 80)
        ))
    if len(set(covers)) != 1:
        raise AssertionError("Quick Launch selection changed the cover artwork")

    launch_screens = CAPTURE_NAMES[:6]
    for name in launch_screens:
        data = frame(name)
        if pixel(data, 0, 144) != 11 or pixel(data, 125, 150) != 1:
            raise AssertionError(f"{name} did not replace the dock with its footer")

    browse_screens = CAPTURE_NAMES[6:9]
    for name in browse_screens:
        if pixel(frame(name), 125, 150) != 12:
            raise AssertionError(f"{name} does not keep Browse active in the dock")
    for name in CAPTURE_NAMES[9:]:
        if pixel(frame(name), 185, 150) != 12:
            raise AssertionError(f"{name} does not keep Tools active in the dock")

    for name in CAPTURE_NAMES:
        visual.render_frame(CAPTURES / f"{name}.frame").save(
            CAPTURES / f"{name}.png"
        )

    print("Phase 5 popup visual checks passed")


if __name__ == "__main__":
    main()

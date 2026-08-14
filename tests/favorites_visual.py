# Copyright (C) 2026 Danny Nunez (dnunezx)

from __future__ import annotations

from pathlib import Path

import cover_demo_visual as visual


CAPTURES = Path("artifacts/favorites-v3")
FRAME_SIZE = 512 + 240 * 160
NAMES = (
    "launch-add", "launch-remove", "favorites-added",
    "favorites-remove-confirm", "favorites-empty",
)


def frame(name: str) -> bytes:
    data = (CAPTURES / f"{name}.frame").read_bytes()
    if len(data) != FRAME_SIZE:
        raise AssertionError(f"{name} frame has {len(data)} bytes")
    return data


def pixel(data: bytes, x: int, y: int) -> int:
    return data[512 + y * 240 + x]


def main() -> None:
    launch_add = frame("launch-add")
    launch_remove = frame("launch-remove")
    if pixel(launch_add, 88, 66) != 6:
        raise AssertionError("Add to Favorites is not the selected action")
    if launch_add[512:] == launch_remove[512:]:
        raise AssertionError("favorite action did not toggle to Remove")

    added = frame("favorites-added")
    if pixel(added, 90, 10) != 6:
        raise AssertionError("added game is not selected in Favorites")
    if pixel(added, 10, 150) != 12:
        raise AssertionError("Favorites dock destination is not active")

    confirm = frame("favorites-remove-confirm")
    if pixel(confirm, 6, 58) != 6:
        raise AssertionError("favorite removal confirmation is not visible")

    empty = frame("favorites-empty")
    if pixel(empty, 90, 10) == 6:
        raise AssertionError("favorite remained after confirmed removal")
    if pixel(empty, 10, 150) != 12:
        raise AssertionError("empty Favorites destination lost dock selection")

    for name in NAMES:
        visual.render_frame(CAPTURES / f"{name}.frame").save(
            CAPTURES / f"{name}.png"
        )

    print("SuperR7 Favorites visual checks passed")


if __name__ == "__main__":
    main()

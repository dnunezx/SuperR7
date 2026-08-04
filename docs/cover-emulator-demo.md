# Cover art emulator demo

The Phase 5 demo runs SuperFW's real cover parser, cache, menu renderer, and
control handling in mGBA without requiring a SuperCard. It is intended for PC
testing only. Do not flash `cover-demo.gba`; the hardware firmware remains
`superfw.gba`.

## What the demo contains

The ROM starts on a synthetic `/DEMO/` browser with these entries:

- `Aurora.gba`: valid multicolor cover.
- `Checker.gba`: a different valid multicolor cover.
- `Missing.gba`: no corresponding cover file.
- `Broken.gba`: a cover with an intentionally corrupt CRC.
- `Folder`: a non-ROM entry that does not request artwork.

Recent Games contains the same four ROM paths. Cover bytes still go through the
normal version 1 `.sfcov` validator and cache; only the demo's storage reader is
synthetic.

## Build and run locally

The build requires the repository submodules, GNU Make, Python 3, and an
`arm-none-eabi` GCC toolchain:

```sh
make BOARD=sd cover-demo.gba
```

Run the scripted check with an mGBA build that includes the headless frontend
and Lua scripting, plus Pillow for the verifier:

```sh
mkdir -p artifacts/cover-demo
timeout 15s mgba-headless --script tools/mgba-cover-demo.lua cover-demo.gba || \
  test -f artifacts/cover-demo/complete.txt
python3 tests/cover_demo_visual.py
```

The Lua script creates `.frame` files containing the 512-byte GBA palette and
the 38,400-byte visible Mode 4 framebuffer. The Python verifier converts them
to native 240-by-160 PNG screenshots in `artifacts/cover-demo/`.

The automated GitHub Actions workflow is usually the simplest reproducible
route: run **Cover art emulator** on `feature/cover-art`, then download the
`superfw-cover-art-mgba-demo` artifact. It includes the demo ROM, EWRAM ELF and
map, raw frames, and reconstructed PNGs.

## States verified

The scripted run captures:

1. Aurora ready in Browse.
2. Checker pending after navigation.
3. Checker ready.
4. A second stable Checker frame.
5. The missing-cover placeholder.
6. The corrupt-cover placeholder.
7. Aurora ready in Recent Games.

The verifier checks native resolution, palette variety, cover replacement,
panel clipping, stable double-buffered output, distinct placeholders, and
Browse/Recent consistency. Physical SD timing and real flashcard behavior are
deliberately left for Phase 6.

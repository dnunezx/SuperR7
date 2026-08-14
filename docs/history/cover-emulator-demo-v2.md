# Legacy version 2 cover emulator demo

> Historical test instructions for the superseded 72-by-72 cover path. Use the
> [current SuperR7 cover demo](../cover-emulator-demo.md) for production checks.

The Phase 5 demo runs SuperR7's inherited cover parser, cache, menu renderer, and
control handling in mGBA without requiring a SuperCard. It is intended for PC
testing only. Do not flash `cover-demo.gba`; the hardware firmware remains
the `superr7.gba` target. The `superfw.gba` name remains an inherited build and
compatibility target.

## What the demo contains

The ROM starts on a synthetic `/DEMO/` browser with these entries:

- `Aurora.gba`: valid multicolor cover.
- `Checker.gba`: a different valid multicolor cover.
- `Missing.gba`: no corresponding cover file.
- `Broken.gba`: a cover with an intentionally corrupt CRC.
- `Folder`: a non-ROM entry that does not request artwork.
- `A Very Long Adventure Game Name.gba`: a sixth-row clipping and selection
  fixture.
- `Seventh Entry.sav` and `Eighth Entry.fw`: window-advance and file-type
  fixtures beyond the six visible rows.

Recent Games contains the same four ROM paths. Cover bytes still go through the
normal version 2 `.sfcov` validator and cache; only the demo's storage reader is
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

The Phase 2 UI demo starts with cyan selection glow. Press **Select** to cycle
through cyan, lime, and ice-white without changing layout or cover data. The
script records `glow-cyan`, `glow-lime`, and `glow-ice` from the real Mode 4
framebuffer and verifies their post-BGR555 palette values and identical pixel
geometry.

## Phase 3 SD candidate (historical)

Build the opt-in Browse integration with the same compression setting used by
the hardware-verified R7 measurements:

```sh
make BOARD=sd COMPRESSION_RATIO=10 superfw-ui.gba
```

`superfw-ui.gba` uses the real SD browser and fixed cyan glow. It is separate
from `superfw.gba` and should be chain-loaded for hardware testing; do not use
it for an internal-flash update. The standard mGBA demo remains the safe way to
test layout, palette conversion, cover states, long-name movement, and list
boundaries without a SuperCard.

The automated GitHub Actions workflow is usually the simplest reproducible
route: run **SuperR7 cover art emulator**, then download the
`superr7-cover-art-mgba-demo` artifact. It includes the demo ROM, EWRAM ELF and
map, raw frames, and reconstructed PNGs.

## States verified

The scripted run captures:

1. Aurora ready on Browse row one.
2. Checker pending, ready, and stable on row two.
3. The missing-cover placeholder on row three.
4. The corrupt-cover placeholder on row four.
5. The folder illustration on row five.
6. The clipped long filename selected on row six.
7. The selected long filename after its scroll delay.
8. A six-row window advance with more than six entries.
9. Aurora ready in Recent Games.
10. Browse, Recent, Setup, and Tools dock highlights.

The verifier checks native resolution, palette variety, cover replacement,
panel clipping, all six selected-row positions, the 20-pixel dock, stable
double-buffered output, distinct placeholders, all four dock states, and
Browse/Recent consistency. Physical SD timing and real flashcard behavior are
deliberately left for Phase 6.

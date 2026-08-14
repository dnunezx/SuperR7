# SuperR7 cover emulator demo

The demo runs the production 76-by-76 cover parser, cache, and browser renderer
in mGBA without requiring a SuperCard. It is a standard GBA test ROM and must
not be flashed as firmware.

## Build

From the repository root:

```sh
make BOARD=sd cover-demo-v3.gba
```

The `v3` suffix identifies the production `.sfcov` file-format version. The
public firmware target remains `superr7.gba`.

## Capture and verify

With an mGBA headless build that supports Lua scripting:

```sh
mkdir -p artifacts/cover-demo-v3
timeout 15s mgba-headless --script tools/mgba-cover-demo-v3.lua cover-demo-v3.gba || \
  test -f artifacts/cover-demo-v3/complete.txt
PYTHONPATH=. python3 tests/cover_demo_v3_visual.py
```

The ignored `artifacts/cover-demo-v3/` directory receives raw Mode 4 frames
and reconstructed native 240-by-160 PNGs. The verifier checks cover geometry,
palette use, placeholders, selection movement, scrolling, dock states, and
Browse/Recent consistency.

Physical SD timing and flashcard behavior still require testing the exact
packaged `superr7.gba` candidate on a SuperCard SD.

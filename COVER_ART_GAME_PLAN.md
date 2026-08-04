# SuperFW SD Cover Art Game Plan

## Objective

Add responsive cover-art previews to the SuperFW ROM browser for the SuperCard
SD model without compromising game launching, save handling, or menu stability.

The first release will display artwork for the currently selected game. It will
not attempt to show a grid of multiple covers.

## MVP scope

- Target the SuperCard SD build first (`BOARD=sd`).
- Display one portrait cover beside the game list.
- Support the regular ROM browser and Recent Games.
- Store artwork on the SD card under `/.superfw/covers/`.
- Match artwork by ROM basename for the MVP.
- Use a compact, preconverted cover format rather than decoding PNG or JPEG in
  the firmware.
- Cache the selected cover and avoid SD reads during rapid scrolling.
- Fall back safely when artwork is missing, invalid, or unreadable.
- Test experimental builds by chain-loading them before flashing firmware.

## Progress

| Phase | Status | Result |
| --- | --- | --- |
| 1: Clean baseline | Complete | SD build and host tests pass; baseline sizes recorded. Physical smoke test remains pending. |
| 2: Cover format and converter | Complete | Version 2 square format, converter, batch mode, previews, strict validation, documentation, and automated tests implemented. |
| 3: Firmware loader and cache | Complete | Strict firmware parser, basename lookup, fixed SDRAM cache, deferred SD loading, Browse/Recent selection tracking, and host tests implemented. |
| 4: Browser integration | Complete | Selected covers, theme-aware placeholders, clipped selectors, and narrower Browse/Recent lists are implemented. Emulator and hardware visual verification remain in Phases 5-6. |
| 5: PC and emulator verification | Complete | A standard-GBA demo ROM now exercises the real menu in mGBA; scripted visual checks cover navigation, valid/missing/corrupt art, Browse/Recent parity, panel bounds, and stable frame swaps. |
| 6-7 | Not started | Phase 6 SuperCard SD hardware verification is next. |

## Proposed design

### Cover files

The working name for the format is `.sfcov`. Each file will contain:

- A magic value identifying it as a SuperFW cover.
- A format version.
- Image dimensions.
- A bounded palette count.
- GBA-compatible palette colors.
- Indexed pixel data.
- Length and integrity fields needed for safe validation.

The finalized target is a 72-by-72 square, matching GBA box-art proportions and
the 76-pixel-wide right-hand panel. Covers may use up to 220 colors.

Example SD layout:

```text
/.superfw/covers/
    Mario Kart - Super Circuit.sfcov
    Pokemon Emerald.sfcov
```

### Desktop converter

The converter will accept common image formats and perform all expensive image
work on the PC:

1. Crop or letterbox the source image to the selected aspect ratio.
2. Resize it to the firmware's fixed cover dimensions.
3. Reduce it to the safe GBA palette range.
4. Encode the palette and indexed pixels into `.sfcov`.
5. Optionally produce a PNG preview of the converted result.
6. Support batch conversion for an entire directory.

The first converter can be command-line based. A drag-and-drop or graphical
interface can follow once the file format is stable.

### Firmware loader

Cover handling will live in a small, isolated module rather than being mixed
directly into all browser code. The module will:

- Resolve the selected ROM's expected cover path.
- Validate the cover header before using any lengths or dimensions.
- Read into fixed-size memory; it will not require dynamic allocation.
- Cache one decoded cover.
- Distinguish loaded, missing, and invalid states.
- Expose simple render data to the menu.

Cover loading will occur only after the selection has remained stable for a
short period. This avoids opening many files while a direction button is held.

### Browser layout

The existing top tab bar and bottom directory bar will remain. The game list
will become narrower, leaving a right-hand panel for the selected cover.

The first version will prioritize readability and compatibility over additional
metadata. A missing-cover placeholder will use the normal SuperFW theme colors.

## Development phases

### Phase 1: Clean baseline

- Create a GitHub fork and a `feature/cover-art` branch.
- Create a clean checkout with all submodules.
- Install or provide the ARM firmware build prerequisites.
- Build the untouched SD firmware.
- Run the existing host-side tests.
- Record commit ID, firmware size, executable-memory usage, and test results.
- Chain-load the untouched baseline build on the target flashcard if needed to
  confirm that the local build environment produces a working image.

Acceptance criteria:

- The repository and submodules are reproducible from a clean checkout.
- `BOARD=sd` builds successfully.
- Existing tests pass.
- Baseline size measurements are recorded below.

### Phase 2: Cover format and converter

- Finalize cover dimensions, palette allocation, and the versioned file header.
- Implement single-file and batch conversion.
- Add preview generation.
- Add tests for valid, truncated, oversized, and unsupported cover files.

Acceptance criteria:

- A converted file round-trips to a pixel-identical preview.
- Invalid input cannot produce a cover exceeding firmware buffer limits.
- Representative artwork remains recognizable on a GBA-sized preview.

Phase 2 result:

- [Version 2 `.sfcov` specification](docs/cover-format.md)
- [Desktop converter instructions](docs/cover-converter.md)
- Version 2 uses fixed 72-by-72 square covers with 1-220 BGR555 colors.
- Palette indices 20-239 are reserved for direct framebuffer copies.
- Exact file length and CRC-32 validation are implemented.
- Single-file conversion, recursive batch conversion, preview generation,
  cover/contain resize modes, inspection, and overwrite protection are
  implemented.
- Twelve automated tests cover round trips, palette limits, transparency,
  letterboxing, corrupt CRCs, invalid dimensions and indices, truncated/trailing
  data, batch behavior, collisions, and overwrite safety.
- The square Metal Slug Advance test image produced a valid 5,640-byte cover
  with 212 colors.

### Phase 3: Firmware loader and cache

- Add the cover lookup, validation, read, and caching module.
- Defer loads during rapid scrolling.
- Add missing and invalid cover states.
- Keep file I/O outside the per-frame drawing path.

Acceptance criteria:

- Corrupt and missing files do not crash, hang, or leak stale artwork.
- Selecting the same game repeatedly does not reread its cover.
- Rapid scrolling remains responsive.

Phase 3 result:

- Added an isolated firmware module for cover lookup, parsing, loading, cache
  state, and render-ready palette/pixel access.
- Cover paths are derived safely from supported ROM basenames and resolved under
  `/.superfw/covers/`.
- One 5,928-byte fixed cache lives in SuperCard SDRAM; cover data does not use
  the GBA heap or add artwork to the firmware image.
- A changed selection immediately invalidates stale artwork, then waits 180 ms
  before performing one SD read outside the per-frame drawing path.
- Ready, pending, missing, invalid, and SD I/O failure states are kept separate.
- Browser folders and unsupported file types clear the cache instead of
  attempting a cover lookup.
- Host tests exercise the CRC implementation, every major malformed-header and
  payload case, path matching, missing/I/O/oversized results, cache reuse,
  delayed loading, and system-timer wraparound.
- Browse and Recent Games now schedule covers, but Phase 3 deliberately does not
  draw them or alter the menu palette; that remains Phase 4.

Phase 3 measurements for commit `85f274e1bddc122f7a1f90db79e7697379036ed5`:

| Item | Phase 2 | Phase 3 | Change |
| --- | ---: | ---: | ---: |
| Final SD firmware | 516,608 bytes | 517,632 bytes | +1,024 bytes |
| Remaining 512 KiB flash space | 7,680 bytes | 6,656 bytes | -1,024 bytes |
| Main firmware before compression | 217,100 bytes | 218,376 bytes | +1,276 bytes |
| Main firmware after compression | 103,404 bytes | 104,349 bytes | +945 bytes |
| EWRAM usage | 217,100 bytes (84.47%) | 218,376 bytes (84.96%) | +1,276 bytes |
| IWRAM usage | 11,144 bytes (34.01%) | 11,144 bytes (34.01%) | unchanged |

Verification runs:

- [Phase 3 host tests](https://github.com/dnunezx/superfw/actions/runs/30867774492)
- [Phase 3 SD firmware build and artifacts](https://github.com/dnunezx/superfw/actions/runs/30867774453)

### Phase 4: Browser integration

- Add the right-hand cover panel.
- Narrow and retest filename rendering.
- Integrate the regular browser and Recent Games.
- Preserve popup, selector, animation, and directory-bar behavior.

Acceptance criteria:

- Covers render without palette corruption or flicker.
- Long filenames remain understandable.
- Existing browser controls and popups remain functional.

Phase 4 implementation result:

- Added a 72-by-72 square cover panel at the right edge of Browse and Recent
  Games, vertically centered between the tab and directory bars,
  surrounded by a two-pixel border using the active UI theme.
- The file list now occupies the left 164 pixels. Long selected names retain
  their scrolling animation, while other long names retain ellipsis handling.
- File sizes remain right-aligned inside the narrower Browse list.
- The selection highlight stops before the cover panel, preventing the OBJ
  selector strip from tinting or obscuring artwork.
- The full-width tab bar, item count, and bottom directory bar are unchanged.
- Ready covers use aligned 16-bit DMA row copies into the Mode 4 framebuffer.
- A cover palette is installed once when loading completes, not on every frame.
- Pending, missing, invalid, and SD-error placeholders use normal theme colors;
  folders and unsupported files show an empty framed panel.
- Popups keep their existing full-screen drawing path, and covers resume when a
  popup closes.
- The cache tests now confirm that changing selection immediately hides old
  palette and pixel pointers, preventing stale artwork during the load delay.

Phase 4 measurements for commit `5ef669eb2d7074bfd8aeca6472ad080078812c5d`:

| Item | Phase 3 | Phase 4 | Change |
| --- | ---: | ---: | ---: |
| Final SD firmware | 517,632 bytes | 518,144 bytes | +512 bytes |
| Remaining 512 KiB flash space | 6,656 bytes | 6,144 bytes | -512 bytes |
| Main firmware before compression | 218,376 bytes | 218,792 bytes | +416 bytes |
| Main firmware after compression | 104,349 bytes | 104,670 bytes | +321 bytes |
| EWRAM usage | 218,376 bytes (84.96%) | 218,792 bytes (85.13%) | +416 bytes |
| IWRAM usage | 11,144 bytes (34.01%) | 11,144 bytes (34.01%) | unchanged |

Verification runs:

- [Phase 4 host tests](https://github.com/dnunezx/superfw/actions/runs/30868430594)
- [Phase 4 SD firmware build and artifacts](https://github.com/dnunezx/superfw/actions/runs/30868430600)

The ARM build and host tests verify the implementation and memory bounds. The
remaining visual acceptance checks (palette appearance, flicker, and interaction
screenshots) require the emulator demo in Phase 5 and the SD flashcard in Phase
6, as planned.

### Phase 5: PC and emulator verification

- Add desktop tests for the parser, matching rules, and cache state.
- Create an emulator-friendly demo build that bypasses proprietary SuperCard SD
  initialization and supplies synthetic browser entries.
- Run the real GBA rendering path in mGBA.
- Capture reference screenshots for visual regression checks.

Acceptance criteria:

- Menu controls, cover changes, missing art, and invalid art work in mGBA.
- No drawing occurs outside the intended panel.
- Frame swapping shows no visible partial updates.

Phase 5 implementation result:

- Added an emulator-only standard GBA ROM target that copies the real firmware
  payload to EWRAM, bypasses SuperCard probing, and enters the existing menu
  code. Compile-time guards keep all demo data and behavior out of normal
  firmware builds.
- The demo supplies synthetic Browse and Recent Games entries plus two valid
  covers, one missing cover, and one structurally valid cover with a corrupt
  CRC. A host test confirms those fixtures pass through the production parser
  and produce the intended cache states.
- Added a header-only mode to the firmware image fixer. Production images keep
  their existing SuperFW size/hash fields, while the normal GBA demo preserves
  executable code in that header-adjacent area.
- An mGBA Lua script holds real GBA controls to navigate Browse and Recent
  Games and captures seven native 240-by-160 states. It records the displayed
  Mode 4 framebuffer and palette directly; the visual test reconstructs PNG
  reference screenshots from those bytes.
- Automated assertions confirm both covers use the expected color range, cover
  changes stay inside the right-hand panel, a pending frame and its completed
  frame are identical outside that panel, two settled frames match exactly,
  missing and corrupt placeholders are distinct and theme-limited, and Recent
  Games renders the same Aurora cover as Browse.
- The demo and visual gate run with the official mGBA development headless
  frontend. See [the emulator demo guide](docs/cover-emulator-demo.md) for local
  commands and artifact details.

Phase 5 production measurements for commit
`7a7dd90b3cadcb29d95d11df2b8f5cabc023995a`:

| Item | Phase 4 | Phase 5 | Change |
| --- | ---: | ---: | ---: |
| Final SD firmware | 518,144 bytes | 517,632 bytes | -512 bytes |
| Remaining 512 KiB flash space | 6,144 bytes | 6,656 bytes | +512 bytes |
| Main firmware before compression | 218,792 bytes | 218,792 bytes | unchanged |
| Main firmware after compression | 104,670 bytes | 104,637 bytes | -33 bytes |
| EWRAM usage | 218,792 bytes (85.13%) | 218,792 bytes (85.13%) | unchanged |
| IWRAM usage | 11,144 bytes (34.01%) | 11,144 bytes (34.01%) | unchanged |

The small compressed-size change comes from per-commit version data; Phase 5's
emulator support adds no code or data to the production firmware. The separate
demo payload uses 222,584 bytes of EWRAM (86.60%) and 10,568 bytes of IWRAM
(32.25%). Its standard GBA wrapper is 206,848 bytes.

Verification runs:

- [Phase 5 host tests](https://github.com/dnunezx/superfw/actions/runs/30871187882)
- [Phase 5 mGBA demo, visual checks, ROM, and screenshots](https://github.com/dnunezx/superfw/actions/runs/30871187871)
- [Phase 5 production SD firmware build and artifacts](https://github.com/dnunezx/superfw/actions/runs/30871187868)

### Phase 6: SuperCard SD hardware verification

- Chain-load the experimental build rather than flashing it initially.
- Test small and large directories, rapid scrolling, Recent Games, long names,
  missing covers, corrupt covers, game launch, returning to the menu, and saves.
- Test repeated cold boots and extended menu use.
- Measure perceived cover-loading delay on the physical SD interface.

Initial performance goals:

- No noticeable input delay while scrolling.
- A cover appears within roughly 250 ms after the selection settles.
- No repeated reads for an unchanged selection.
- No regression in launching or saving games.

### Phase 7: Polish and release

- Add a user setting to enable or disable cover art.
- Consider GBA game-code matching as a fallback or replacement for basename
  matching.
- Improve converter usability and documentation.
- Ensure all board variants still compile.
- Add build-size checks and prepare an upstream-friendly pull request.

## Risk controls

| Risk | Control |
| --- | --- |
| Firmware exceeds the SD model's size limit | Keep artwork on the SD card, use a tiny custom decoder, and compare every build with the baseline. |
| Executable EWRAM becomes too large | Isolate the feature, avoid general-purpose image libraries, and inspect the linker map. |
| Palette conflicts with the menu | Reserve and document a verified palette range before finalizing the format. |
| Scrolling triggers excessive SD reads | Load after selection settles and cache the active cover. |
| Bad cover files destabilize firmware | Validate every field and enforce fixed maximum sizes before reading pixel data. |
| Experimental firmware causes hardware trouble | Chain-load test builds before considering permanent flashing. |
| Commercial cover licensing becomes a distribution problem | Distribute the converter and format support, not copyrighted cover packs. |

## Phase 1 baseline record

This section is updated as Phase 1 progresses.

| Item | Result |
| --- | --- |
| Upstream repository | `davidgfnet/superfw` |
| Fork | `dnunezx/superfw` |
| Development branch | `feature/cover-art` |
| Baseline commit | `cf09d09492525b84ac3bbd20db406805c7ce6242` |
| Baseline measurement commit | `85673693ec3bd4ef1467104ac6603d6b7460bf4f` (documentation and CI only; firmware sources unchanged) |
| Submodules | `apultra` checked out at `8f340057d7402c10da3d9c76c599f9ab83b8a22d` |
| SD firmware build | Passed on GitHub Actions |
| Host tests | Passed on GitHub Actions |
| Final firmware size | 516,608 bytes of 524,288 bytes; 7,680 bytes (7.5 KiB) remaining |
| Main firmware before compression | 217,100 bytes |
| Main firmware after compression | 103,397 bytes |
| EWRAM usage | 217,100 of 257,024 bytes (84.47%); 39,924 bytes remaining |
| IWRAM usage | 11,144 of 32,768 bytes (34.01%); 21,624 bytes remaining |
| Hardware smoke test | Pending |

Baseline workflow runs:

- [SD firmware build and artifacts](https://github.com/dnunezx/superfw/actions/runs/30858515467)
- [Existing SuperFW host tests](https://github.com/dnunezx/superfw/actions/runs/30858515464)

The final 512 KiB firmware image is the tighter constraint: only 7.5 KiB is
currently unused. The cover implementation must therefore avoid a general image
decoder and must track the final compressed image size on every change. The
main executable has substantially more EWRAM headroom, so a fixed cover buffer
and a small custom-format loader remain practical.

## Definition of done for the first release

The feature is ready when the SD firmware reliably displays a converted cover
for the selected game, remains responsive with large directories, handles
missing or malformed artwork safely, launches and saves games without
regression, and has passed both emulator-assisted and physical SuperCard SD
testing.

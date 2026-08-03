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

The initial target size is approximately 72 by 104 pixels. The exact dimensions
and color count will be finalized after auditing the menu palette and testing a
screen mockup.

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

### Phase 3: Firmware loader and cache

- Add the cover lookup, validation, read, and caching module.
- Defer loads during rapid scrolling.
- Add missing and invalid cover states.
- Keep file I/O outside the per-frame drawing path.

Acceptance criteria:

- Corrupt and missing files do not crash, hang, or leak stale artwork.
- Selecting the same game repeatedly does not reread its cover.
- Rapid scrolling remains responsive.

### Phase 4: Browser integration

- Add the right-hand cover panel.
- Narrow and retest filename rendering.
- Integrate the regular browser and Recent Games.
- Preserve popup, selector, animation, and directory-bar behavior.

Acceptance criteria:

- Covers render without palette corruption or flicker.
- Long filenames remain understandable.
- Existing browser controls and popups remain functional.

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
| Development branch | `feature/cover-art` |
| Baseline commit | `cf09d09492525b84ac3bbd20db406805c7ce6242` |
| Submodules | `apultra` checked out at `8f340057d7402c10da3d9c76c599f9ab83b8a22d` |
| SD firmware build | Pending |
| Host tests | Pending |
| Final firmware size | Pending |
| EWRAM usage | Pending |
| IWRAM usage | Pending |
| Hardware smoke test | Pending |

## Definition of done for the first release

The feature is ready when the SD firmware reliably displays a converted cover
for the selected game, remains responsive with large directories, handles
missing or malformed artwork safely, launches and saves games without
regression, and has passed both emulator-assisted and physical SuperCard SD
testing.

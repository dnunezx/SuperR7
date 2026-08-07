# SuperCard SD Browser UI Redesign Game Plan

## Objective

Replace the basic inherited SuperFW browser presentation with an original handheld-era
card interface while preserving the hardware-proven cover loader, ROM browser,
game launching, saves, settings, and tools.

The approved direction places the selected game's square cover on the left,
seven visible game cards on the right, and primary navigation along the
bottom. The seven-row layout has passed evaluation on a physical 240-by-160
GBA screen.

Reference concept:

- [Generated browser concept](docs/ui-mockups/cover-browser-concept-v1.png)
- The generated concept establishes the visual direction, not final pixel
  measurements or production-ready assets.

## Current checkpoint

Status as of **August 6, 2026: Phase 5 hardware accepted; SuperR7 fork started**.

- The exact cleaned Phase 5 candidate passed physical SuperCard SD validation
  and is now frozen as the functional baseline for the independent **SuperR7**
  fork, maintained by Danny Nunez.
- Frozen baseline: `releases/phase5-hardware-baseline/SuperR7-phase5-hardware-baseline.gba`,
  520,192 bytes, SHA-256
  `15A88B4F0F25B057ED4B93B4B0D855E7F3CFE67C0E7D0B7ADBA01261A6667A92`.
- SuperR7 branding and recognition are applied after that frozen checkpoint.
  Branded builds are validated separately and never overwrite the exact
  hardware-passed binary.

- Phase 0 baseline protection, Phase 1 native specification, the Phase 2
  emulator renderer, and Phase 3 Browse integration are complete. The user
  successfully chain-loaded the seven-row, native 76-by-76 version 3 build on
  physical hardware and confirmed that it boots and works correctly.
- The user has now also chain-loaded the complete Phase 4 candidate and
  confirmed that its dock, Recent integration, Appearance screen, presets,
  custom colors, and contrast modes work correctly on hardware. A problem was
  subsequently found in the Stars wallpaper: it drew only sparse pixels at the
  extreme screen edges instead of a recognizable star field.
- The user subsequently confirmed that the dock-contrast revision works
  wonderfully on hardware. Phase 4 is therefore hardware-accepted.
- A corrected Stars implementation was evaluated, but its limited visibility
  did not justify the firmware cost. By user decision, Stars has been removed
  from the renderer, settings list, emulator script, and visual checks.
- The completed UI work is being checkpointed locally as the start of
  `superr7/main`; publication to a new hosted repository remains separate.
- The inherited normal SD target still excludes the redesigned UI. The frozen,
  hardware-tested Phase 5 image remains the rollback source of truth.
- Version 3 is now the redesign's default candidate. It uses seven complete
  rows, native 76-by-76 artwork in a 78-by-78 frame, and a 16-pixel bottom
  dock. The version 2 path and its 72-by-72 files remain unchanged.
- Row icons and the selection arrow are removed. Icons appear only in the dock,
  whose visible order is Favorites, Recent, Browse, and Tools.
- The dock uses a dedicated 5-by-7 uppercase font so the full `FAVORITE` label
  fits its 60-pixel cell. Its icons are a star, clock, folder, and crossed
  tools, each verified as a distinct 8-by-8 native-resolution silhouette.
- Phase 4 adds user-facing presets, independent Background, Accent, and
  Selection controls, contrast handling, theme reset, and four procedural
  wallpaper choices: None, Weave, Grid, and Circuit.
- The preset set is now ELECTRIC BLUE, MUTANT GREEN, STEALTH BLACK, and CHROME
  SILVER. ELECTRIC BLUE is the source default.
- Hardware feedback showed that Accent and Selection colors were being muted
  too heavily by background blending. Selection fill now uses a 50-percent
  color mix, while selection and accent shadows retain 75 percent of their
  chosen colors. Selected borders and active dock highlights use the full
  chosen colors.
- A second hardware contrast report found that unselected dock labels became
  difficult to read with Purple, Amber, Green, White, Slate, and Cyan
  backgrounds. The dock now has a dedicated text color derived from the actual
  darker dock surface rather than the general muted-text color. Auto chooses
  light or dark dock text for contrast, while the explicit Dark and Light
  overrides remain respected.
- The former Lime option is now Green, using a more natural vivid green rather
  than yellow-lime. MUTANT GREEN uses the updated color for both Accent and
  Selection.
- The local WSL Ubuntu environment now contains GNU Make, ARM GCC 13.2,
  Python/Pillow, and the scripted mGBA headless test runner.
- All 23 local Python checks, the theme host tests, and the complete Phase 4
  and Phase 5 mGBA visual suites pass.
- A separate `superfw-ui.gba` target now connects the seven-row renderer to the
  real SD Browse model without enabling it in the normal `superfw.gba` target.
- Phase 5 now applies the same card renderer to Interface, Global settings,
  System information, launch options, patch options, save and file actions,
  firmware update, confirmation dialogs, RTC editing, and alerts.
- The refined Phase 5 candidate replaces the crowded launch screen with a
  progressive Quick Launch flow. Its full-width title bar centers the filename,
  `Launch game` is the single primary action, and Options, Advanced, and Details
  separate the remaining information without changing the existing handlers.
- The loading screen now follows Background, Accent, Selection, wallpaper, and
  contrast choices. It adds a theme-colored progress bar, moving highlight,
  cover-art scan line, percentage, and clean status footer while retaining the
  native 76-by-76 cover.
- The cleaned refined candidate is 520,192 bytes with a 105,745-byte ratio-10
  compressed main payload, leaving 4,096 bytes below the 512 KiB limit. Its
  SHA-256 is
  `15A88B4F0F25B057ED4B93B4B0D855E7F3CFE67C0E7D0B7ADBA01261A6667A92`.
- Candidate-only dead UI baggage has been removed from the v3 SD build: the
  classic Browse/Recent renderers, old OBJ icon atlas and palette, selector
  sprite queue, and unused classic drawing helpers are no longer linked. They
  remain available behind the normal-firmware and NOR fallback guards.
- Phase 5 is complete and its refined launch and loading screens passed
  physical chain-load validation.

### Seven-row hardware readability checkpoint

- Native row bounds are `y=2..138`, using seven 17-pixel cards on a 20-pixel
  step. The final row remains fully above the dock and retains its selection
  treatment when the list window advances.
- The dock occupies `y=144..159`, leaving a three-pixel safety gap below the
  final card's shadow/glow.
- The accepted version 3 path uses strict native 76-by-76 `.sfcov` artwork and
  copies it with the established DMA path without runtime scaling.
- The automated native-frame capture verifies all seven rows, clipped and
  scrolling names, ready/pending/missing/invalid/folder covers, stable settled
  frames, dock highlights, and red/cyan palette-only selection variants.
- Hardware acceptance passed: the user successfully chain-loaded the version 3
  candidate and confirmed that the 76-by-76 cover path boots and works.

### Version 3 76-by-76 cover checkpoint

- Version 3 uses a strict 76-by-76 `.sfcov` header and 5,776-byte pixel
  payload. It does not reinterpret or overwrite version 2 artwork.
- The separate `superfw-ui-v3.gba` and `cover-demo-v3.gba` targets enable the
  redesign without changing the normal firmware or version 2 UI targets.
- The native layout places version 3 artwork at `x=4..79`, `y=33..108`, with
  its 78-by-78 frame at `x=3..80`, `y=32..109`.
- Converter round trips, version isolation, overwrite protection, firmware
  validation, and the complete scripted mGBA visual suite pass locally.
- See [the version 3 format note](docs/cover-format-v3-76.md). Physical
  chain-load verification passed.

### Completed glow selection

- Cyan, lime, and ice-white pixel-glow mockups were generated in
  [`docs/ui-mockups/glow-comparison`](docs/ui-mockups/glow-comparison/).
- All three variants now use the C renderer's one-to-two-pixel bands and were
  captured from mGBA at 240 by 160 after GBA BGR555 conversion.
- The verifier checks exact converted palette values and proves that only the
  palette, not geometry or cover data, changes between variants.
- Cyan is selected because it preserves the clearest selected/unselected
  hierarchy without competing with the lime file badges or flattening the
  pale cards. Lime is too dominant and ice-white loses hierarchy.
- The demo starts on cyan; Select cycles cyan, lime, and ice-white. Production
  candidate code always uses cyan.

## Non-negotiable rules

- Target the SuperCard SD build first.
- Keep cover files, parsing, caching, and delayed SD reads unchanged during the
  initial renderer work.
- Keep ROM launch, save, patch, cheat, and file-manager behavior unchanged.
- Use original icons and decoration rather than artwork copied from another
  game's interface.
- Test UI changes in the standard-GBA mGBA demo before chain-loading them.
- Chain-load on hardware before considering another internal-flash update.
- Never exceed the 512 KiB SD firmware image limit.
- Five visible game rows is the minimum acceptance target.

## Proposed native layout

The current hardware prototype is:

| Region | Proposed bounds | Purpose |
| --- | --- | --- |
| Main content | `y=0..143` | Cover and seven-card game list |
| Cover frame | `x=3..80`, `y=32..109` | 78-by-78 selected frame around version 3 cover data |
| Cover artwork | `x=4..79`, `y=33..108` | Native 76-by-76 version 3 `.sfcov` artwork |
| Game list | `x=85..236`, cards at `y=2..138` | Seven stacked 17-pixel cards |
| Navigation dock | `y=144..159` | Compact Favorites, Recent, Browse, and Tools bar |

The selected filename may scroll horizontally. Unselected rows use a static
clipped name. Folder, parent-directory, unsupported-file, missing-cover, and
invalid-cover states remain visually distinct.

The first navigation dock maps existing functionality into four primary areas:

1. **Favorites** - visible destination with an empty state; persistent
   add/remove behavior remains a tracked follow-up.
2. **Recent** - recently launched games.
3. **Browse** - ROM and file browser.
4. **Tools** - advanced tools, settings, and firmware information in Phase 4.

## Phase 0: Protect and record the baseline

Status: **Complete locally**

- Hardware-verified source commit: `90de4fb54255dcd7e42e08bbfe70f678915bfd29`.
- Local baseline tag: `cover-art-baseline-r7`.
- UI development branch: `feature/ui-browser`.
- Final SD firmware: 518,144 of 524,288 bytes.
- Remaining final-image space: 6,144 bytes.
- Main firmware binary: 219,380 bytes.
- Compressed main firmware: 105,129 bytes.
- Main firmware EWRAM allocation: 225,308 of 257,024 bytes (87.66%).
- Main firmware IWRAM allocation: 11,672 of 32,768 bytes (35.62%).
- Firmware SHA-256:
  `93EDC36DCF92D054834CE101DA735049EF3A48FA7794EF8FAC185189950FBA01`.
- R7 boots from internal flash, reads covers exclusively from the canonical
  organized folder, displays covers in Browse and Recent, launches games, and
  preserves save behavior on physical hardware.

The tag and branch are local until the standalone repository decision is
completed. The verified R7 firmware and build reports remain archived outside
the checkout under `phase6-hardware-test/R7_ARTIFACT`.

## Phase 1: Native-resolution specification

Status: **Complete**

- Rebuild the concept at exactly 240 by 160 pixels.
- Produce five-row and six-row variants at actual display size.
- View both variants without enlargement and select the most readable one.
- Fix exact cover, list, card, footer, icon, and text bounds.
- Allocate the background palette around the existing cover range.
- Define selected, unselected, folder, empty, missing, invalid, and disabled
  states.
- Define long-name movement and page-scroll behavior.

Acceptance criteria:

- At least five complete game rows are visible.
- Long titles remain identifiable.
- The cover remains square and unobstructed.
- The navigation dock is understandable without memorizing its icons.
- The design remains attractive at native GBA size, not only when enlarged.

Phase 1 result:

- Produced deterministic native 240-by-160 five-row and six-row variants.
- Selected six rows for the Phase 2 emulator prototype because the 19-pixel
  cards and bitmap text remain readable while increasing visible games.
- Reduced the navigation dock from 28 pixels to 20 pixels and placed each icon
  beside its label.
- Retained five 24-pixel rows as a compile-time fallback for physical-screen
  testing.
- Fixed cover, list, dock, row, icon, and text bounds.
- Defined a complete 20-color UI palette that preserves indices 20-239 for
  cover artwork.
- Defined ready, pending, folder, missing, invalid, SD-error, unsupported,
  selected, unselected, and disabled states.
- Documented filename clipping and existing selected-name scrolling behavior.
- See [the native Phase 1 specification](docs/ui-phase1-spec.md).

## Phase 2: Static mGBA renderer prototype

Status: **Complete locally**

- Add the new renderer behind an emulator/demo-only build flag.
- Use synthetic entries and existing valid, missing, and corrupt cover fixtures.
- Draw stripes, frames, and highlights procedurally where this saves space.
- Use small original sprite icons with their own constrained palette.
- Capture selected-row positions, both cover states, folders, and each dock item.
- Add visual assertions for bounds, stable frame swaps, and palette separation.

Acceptance criteria:

- The emulator screen matches the approved native specification.
- No new UI element draws over the cover or outside its assigned bounds.
- Six-row navigation works at every visible position.
- Production firmware behavior is unchanged because integration is not active.

Phase 2 result:

- Added a native Mode 4 renderer with six 19-pixel game cards, a square
  72-by-72 cover, procedural blue stripes, and a compact 20-pixel dock.
- Kept the renderer behind `UI_BROWSER_V2`, which was enabled only by the
  `cover-demo.gba` target.
- Kept background palette indices 0-19 separate from cover indices 20-239.
- Verified all six selected-row positions, ready, pending, missing, invalid,
  folder, and long-filename states in scripted mGBA captures.
- Verified Browse, Recent, Setup, and Tools dock highlights and Browse/Recent
  cover consistency.
- Passed all 19 local Python checks and the mGBA framebuffer verifier.
- Confirmed the normal SD build is byte-for-byte identical to hardware-tested
  R7: 518,144 bytes with SHA-256
  `93EDC36DCF92D054834CE101DA735049EF3A48FA7794EF8FAC185189950FBA01`.
- Reference captures are stored in
  [`docs/ui-mockups/phase2`](docs/ui-mockups/phase2/).

## Phase 3: Browse integration

Status: **Complete; version 3 chain-load validation passed**

- Connect the renderer to the real ROM browser without changing its file model.
- Replace the current eight-row presentation with a five-or-more-row card
  window.
- Preserve folders, parent navigation, file types, selection state, and long
  filenames.
- Reuse the current cover request, delay, validation, and EWRAM cache paths.
- Preserve every existing Browse button action.

Acceptance criteria:

- Large directories remain responsive during rapid scrolling.
- The list window advances correctly above and below every boundary.
- The selected cover follows the selected filename without stale frames.
- Existing popups, launching, and returning to Browse still work.

Phase 3 implementation result so far:

- Added a separate `superfw-ui.gba` SD target; `superfw.gba` does not link the
  new renderer.
- Connected the selected entry, six-entry window, cover cache state, cover
  pixels, hidden attribute, and animation counter to the existing browser
  model without changing SD reads, cache behavior, or launch actions.
- Changed Browse paging and boundary calculations from eight visible rows to
  six only when `UI_BROWSER_V2` is enabled.
- Added distinct game, folder, parent, save, firmware, generic-file, hidden,
  and unsupported visual treatments.
- Preserved delayed selected-name scrolling and clipped unselected names.
- Verified the sixth row, an eight-entry window shift, scrolling long name,
  cover states, and cyan/lime/ice palettes in scripted mGBA frames.
- Ratio-10 build measurements: 224,068-byte main binary, 108,775-byte
  compressed payload, 229,996 of 257,024 EWRAM bytes, 11,672 of 32,768 IWRAM
  bytes, and a 522,240-byte final candidate with 2,048 bytes free.
- The user successfully chain-loaded the seven-row version 3 candidate and
  confirmed that it boots and works with native 76-by-76 covers.

## Phase 4: Recent and navigation dock integration

Status: **Complete; hardware validation passed**

- Apply the same card list to Recent Games.
- Replace the top icon strip with the bottom navigation dock.
- Use L/R for primary-area switching.
- Route current UI/language settings through Settings.
- Route current Info through Tools.
- Preserve each area's last selection when switching.

Acceptance criteria:

- Browse and Recent show identical covers for the same ROM.
- Every existing top-level function remains reachable.
- The selected dock item and button hints are always unambiguous.

Phase 4 implementation result so far:

- Applied the same seven-card renderer and cover path to Recent Games.
- Replaced primary navigation with the compact four-item dock: Favorite,
  Recent, Browse, and Tools. L/R changes primary destinations, while each
  destination retains its own selection state.
- Routed Appearance, Interface & language, Global settings, and System
  information through Tools so the existing top-level functions remain
  reachable.
- Added an Appearance screen with the exact user-facing controls: Preset,
  Wallpaper, Background, Accent, Selection, Contrast, and Reset theme.
- Added ELECTRIC BLUE, MUTANT GREEN, STEALTH BLACK, and CHROME SILVER presets
  plus None, Weave, Grid, and Circuit wallpapers. The selected values persist
  in settings.
- Background automatically derives the screen, cards, dock, stripes, edges,
  and shadows. Accent controls the active dock item and highlights. Selection
  controls the selected game's border, fill, and shadow.
- Increased visible color separation after hardware feedback: selected fills
  use a stronger 50-percent Selection mix, selected and accent shadows preserve
  75 percent of their chosen colors, game highlights use full Accent, and the
  bright Cyan, Blue, Purple, Red, Amber, and Green source colors are more
  saturated.
- Added a dedicated dock-text palette role without increasing the 20-color UI
  palette. Unselected dock labels now contrast against the derived dock shade;
  regression tests cover Purple, Amber, Green, White, Slate, and Cyan.
- Contrast defaults to Auto with Dark and Light overrides. Readable text and
  muted text are derived automatically; folder amber, error red, and disabled
  gray remain protected rather than exposed as user controls.
- Reset theme restores the current preset's full values.
- Favorites is a visible dock destination with an empty-state screen; its
  backing favorites library and add/remove behavior are still future work.
- Scripted mGBA checks cover all four wallpapers, all four presets, every
  independent color control, contrast overrides, reset behavior, seven-row
  layouts, all four dock selections, and Browse/Recent cover consistency.
- Ratio-10 measurements: 226,976-byte main binary, 110,196-byte compressed
  payload, 233,496 of 257,024 EWRAM bytes, 11,704 of 32,768 IWRAM bytes, and a
  523,264-byte final candidate with 1,024 bytes free.
- Candidate SHA-256:
  `597ABCB25DC95E7EBDC7FA4C999F32541A6B96483B4F16CD98CEEA00DE06C22E`.
- Physical result: the user chain-loaded this exact Phase 4 candidate and
  confirmed that its dock, theme settings, and wallpaper selection controls
  work. The Stars rendering defect was found afterward.
- Final Stars decision: remove the option rather than spend additional firmware
  space on a wallpaper with little visible area. Existing saved Stars value 4
  safely sanitizes to None now that four wallpaper choices remain.
- Vibrant candidate measurements: 226,824-byte main binary, 110,150-byte
  compressed payload, and a 523,264-byte final image with 1,024 bytes free.
- Vibrant candidate SHA-256:
  `C60A095B73F4F207C8F0516CA0C4DF3604783FD51A04982542B8D468E075573F`.
- The vibrant candidate passes the full native 240-by-160 mGBA sequence;
  hardware feedback identified the unselected dock-label contrast issue.
- Dock-contrast candidate measurements: 226,952-byte main binary, 110,213-byte
  compressed payload, and a 523,264-byte final image with 1,024 bytes free.
- Dock-contrast candidate SHA-256:
  `B24DDBCBCA78DD1764058BAFDD715EBF984C681056BB9D67DB703862BDD6E39D`.
- Host contrast tests and the complete native 240-by-160 mGBA sequence pass.
  The user confirmed the dock-contrast revision works correctly on hardware.
- Deferred follow-up: Favorites currently presents its designed empty state;
  persistent favorite storage and add/remove actions are not implemented yet.

## Phase 5: Secondary-screen visual consistency

Status: **Complete; hardware validation passed**

- Restyle launch options, confirmations, errors, settings, tools, and firmware
  information using the same cards, colors, and spacing.
- Keep each screen's underlying actions unchanged.
- Retain safe fallback rendering for low-memory or error states.

Acceptance criteria:

- Normal use does not unexpectedly mix old and new visual systems.
- Every confirmation and error remains readable and clearly actionable.

Phase 5 implementation result:

- Replaced the legacy Interface, Global settings, Tools information, launch,
  save, file-manager, firmware-update, confirmation, RTC, and alert layouts
  with the same full-width cards, theme palette, wallpaper, and compact dock.
- Removed the obsolete legacy Theme color row from Interface because the
  dedicated Appearance screen now owns preset and color selection.
- Global Settings section headings remain visible but are skipped by the
  selector. Saving Interface or Global settings now returns focus to the first
  actionable row rather than a heading or removed option.
- System Information is organized into four A-cycled card pages: SuperR7,
  flash information, patch database, and SD card.
- Game launch information, load/save policy, patch controls, DirectSave,
  in-game menu, RTC, cheats, and remember/build actions remain connected to
  their existing input handlers.
- The standard SD UI uses the new dialogs throughout normal use. Legacy popup
  rendering remains available as a compile-time fallback for NOR-capable
  builds that are outside this first SD-target redesign.
- Exact 240-by-160 scripted captures verify secondary screens plus launch,
  patch, save, file, firmware, confirmation No/Yes, RTC field, and alert
  states. The refined Quick Launch view uses a full-width centered title and a
  single centered `Launch game` action. Options, Advanced, and read-only Details
  pages progressively disclose the remaining controls and status information.
- The loading page is theme-aware and adds an Accent fill, Selection border and
  glow, moving bright pulse, percentage, and cover-art scan line. Scripted
  Electric Blue, Mutant Green, and Chrome Silver captures verify that each
  palette role changes independently and that B returns to Quick Launch.
- All four Phase 4/5 native visual assertion suites and all 23 Python checks
  pass.
- Final cleaned measurements: 214,176-byte main binary, 105,745-byte compressed
  main payload, 220,696 of 257,024 EWRAM bytes, 11,176 of 32,768 IWRAM bytes,
  and a 520,192-byte firmware image with 4,096 bytes free.
- Candidate SHA-256:
  `15A88B4F0F25B057ED4B93B4B0D855E7F3CFE67C0E7D0B7ADBA01261A6667A92`.
- Fresh mGBA captures from the cleaned build pass the complete Phase 4 theme,
  browser, and dock suite plus the Phase 5 secondary-screen, popup, refined
  launch, file-action, and themed-loading suites. Host theme tests also pass.
- Packaged chain-load candidate:
  `artifacts/phase5-v4-launch-loading-hardware/superfw-phase5-v4-76-launch-loading.gba`.
- Hardware result: the user chain-loaded this exact candidate and accepted the
  complete cleaned Phase 5 experience. It is preserved byte-for-byte in
  `releases/phase5-hardware-baseline/`.

## Phase 6: Firmware-size and performance gate

- Compare the final image, compressed payload, EWRAM, and IWRAM with Phase 0.
- Target no more than 2 KiB of compressed final-image growth before optimization.
- Do not add another cover-sized cache or framebuffer.
- Reuse procedural shapes, shared icons, and existing font infrastructure.
- Run the SD build, host tests, converter tests, and mGBA visual tests.

Acceptance criteria:

- Final SD image remains below 524,288 bytes with useful repair headroom.
- Menu input and rapid scrolling remain responsive.
- Cover rendering and palette installation remain unchanged and stable.

## Phase 7: Physical SuperCard SD verification

Status: **Complete for the cleaned Phase 5 baseline; hardware validation passed**

- Chain-load the UI build first.
- Test directories smaller than and larger than the visible row count.
- Test every row position, rapid scrolling, long names, folders, and all dock
  destinations.
- Test missing and corrupt covers, popups, settings, tools, game launch, saves,
  Recent Games, and returning to the menu.
- Perform repeated cold boots and extended browsing.
- The cleaned Phase 5 baseline passed the full-system hardware gate. Any later
  branded or functional build repeats the regression gate before replacing it.

Acceptance criteria:

- The five-or-more-row layout is readable on the physical display.
- No corruption, hang, stale cover, launch regression, or save regression is
  observed.
- A verified rollback image remains available before flashing.

## Definition of done

The redesign is complete when the approved original card interface is used by
Browse, Recent, Settings, Tools, and their normal secondary screens; at least
five game rows remain readable; the SD firmware stays within its size and memory
limits; and emulator plus physical-hardware testing show no regression in cover
art, navigation, launching, or saves.

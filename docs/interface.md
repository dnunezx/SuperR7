# SuperR7 interface

SuperR7 uses a native 240-by-160 card interface designed for the SuperCard SD.
The current layout presents a 76-by-76 cover beside a seven-row game list and a
four-item dock: Favorites, Recent, Browse, and Tools.

## Library navigation

- Up and Down move one item.
- Left and Right change to the previous or next fixed seven-item page and
  select its first item. Paging at the beginning or end of a list does nothing;
  the final page may contain fewer than seven items.
- A opens the normal launch flow.
- Long titles scroll inside the selected row.
- Browse, Recent, and Favorites share the same list and cover behavior.

Favorites are stored in `/.superfw/favorites.txt` and support up to 200 ROM
paths. Quick Launch provides `Add to Favorites` or `Remove Favorite`. In the
Favorites tab, Select requests confirmation before removing the selected item.

## Launch flow

Selecting a GBA game opens Quick Launch. The main action starts the game;
Options, Advanced, and Details expose the remaining controls without crowding
the first screen. Secondary screens use `B: BACK` consistently.

## Appearance

Appearance includes four presets, independent Background, Accent, and
Selection colors, contrast handling, and five procedural wallpapers: None,
Weave, Grid, Circuit, and Tech Frame. The selected palette and wallpaper are
passed to the in-game menu when a game launches.

## Compatibility paths

SuperR7 retains the `/.superfw/` directory so existing SuperFW settings, saves,
patches, cheats, and emulator files remain usable. The inherited path is a
compatibility contract, not the public project name.

For exact cover encoding, see the [cover format](cover-format.md). For the
accepted firmware lineage, see [hardware validation](hardware-validation.md).

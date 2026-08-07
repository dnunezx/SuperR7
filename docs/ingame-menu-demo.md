# SuperR7 in-game menu emulator demo

The dedicated demo runs the production in-game menu renderer as a standard GBA
ROM. It exists so card geometry, Appearance palette inheritance, wallpaper,
disabled actions, submenus, RTC controls, and dialogs can be checked without
patching or launching a commercial game.

Build it with:

```sh
make BOARD=sd ingame-menu-demo.gba
```

Capture and verify the scripted states with:

```sh
mkdir -p artifacts/ingame-menu
timeout 85s mgba-headless --script tools/mgba-ingame-menu.lua ingame-menu-demo.gba || \
  test -f artifacts/ingame-menu/complete.txt
PYTHONPATH=. python3 tests/ingame_menu_visual.py
```

The suite records the main, reset, save, RTC, selected RTC update,
confirmation-dialog, savestate, and cheat screens at the GBA's native
240-by-160 resolution. It
asserts the 20-role Appearance palette mapping, selected and unselected card
fills, footer color, distinct screen states, and card-dialog edge treatment.

This ROM is emulator-only. Hardware validation must use the packaged SuperR7
firmware candidate and enter the menu from a launched game.

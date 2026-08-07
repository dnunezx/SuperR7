/*
 * Copyright (C) 2026 Danny Nunez
 * Emulator-only harness for the SuperR7 in-game menu renderer.
 */

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#include "ingame.h"
#include "cheats.h"
#include "ui_theme.h"

typedef struct {
  uint8_t slen;
  uint8_t codelen;
  uint8_t enabled;
  uint8_t pad;
  char title[20];
} t_demo_cheat;

static struct {
  uint32_t count;
  t_demo_cheat entries[2];
} demo_cheats = {
  2,
  {
    {20, 0, 1, 0, "Infinite lives"},
    {20, 0, 0, 0, "Unlock all stages"},
  },
};

unsigned has_rtc_support = 1;
unsigned ingame_menu_lang = 0;
bool isgba = true;
bool slowsd = true;
uint32_t cheat_base_addr = 0;
uint32_t menu_anim_speed = 2;
uint16_t ingame_menu_palette[IGM_THEME_COLOR_COUNT];
uint32_t ingame_menu_wallpaper = UiWallpaperGrid;
uint32_t savefile_backups = 0;
uint32_t scratch_base = 0;
uint32_t scratch_size = 388 * 1024;
uint32_t spill_addr = 0;
char savefile_pattern[256] = "/DEMO/SAVE";
char savestate_pattern[256] = {0};
void *font_base_addr = 0;

static uint32_t demo_rtc = 45568800U;
static uint32_t demo_rtc_speed = 3;
static uint32_t demo_cheat_table[64];

void reset_game(void) {}
void reset_fw(void) {}
void set_undef_lrsp(uint32_t rtc, uint32_t speed) {
  demo_rtc = rtc;
  demo_rtc_speed = speed;
}
uint32_t get_undef_lr(void) { return demo_rtc; }
uint32_t get_undef_sp(void) { return demo_rtc_speed; }
void set_entrypoint_hook(bool process_cheats) { (void)process_cheats; }
uint32_t *get_cheat_table(void) { return demo_cheat_table; }

void fast_mem_cpy_256(void *dst, const void *src, unsigned count) {
  uint32_t *out = dst;
  const uint32_t *in = src;
  for (unsigned i = 0; i < count / 4; i++)
    out[i] = in[i];
}

void fast_mem_clr_256(void *dst, uint32_t value, unsigned count) {
  uint32_t *out = dst;
  for (unsigned i = 0; i < count / 4; i++)
    out[i] = value;
}

void ingame_menu_loop(uint32_t *use_cheats_hook);

int main(void) {
  uint32_t use_cheats_hook = 0;
  ui_theme_reset(UiThemeElectricBlue);
  ui_theme_apply_palette(ingame_menu_palette);
  ingame_menu_wallpaper = ui_wallpaper;
  cheat_base_addr = (uint32_t)&demo_cheats;
  ingame_menu_loop(&use_cheats_hook);
  return 0;
}

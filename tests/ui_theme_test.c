/* Copyright (C) 2026 Danny Nunez */

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "gbahw.h"
#include "ui_theme.h"

static uint16_t expected_mix(uint16_t first, uint16_t second, unsigned weight) {
  unsigned inv = 8 - weight;
  unsigned r = (((first & 31) * inv) + ((second & 31) * weight) + 4) >> 3;
  unsigned g = ((((first >> 5) & 31) * inv) +
                (((second >> 5) & 31) * weight) + 4) >> 3;
  unsigned b = ((((first >> 10) & 31) * inv) +
                (((second >> 10) & 31) * weight) + 4) >> 3;
  return r | (g << 5) | (b << 10);
}

static unsigned test_luminance(uint16_t color) {
  return (color & 31) * 3 + ((color >> 5) & 31) * 6 +
         ((color >> 10) & 31);
}

static void test_presets(void) {
  assert(!strcmp(ui_theme_preset_names[UiThemeElectricBlue], "ELECTRIC BLUE"));
  assert(!strcmp(ui_theme_preset_names[UiThemeMutantGreen], "MUTANT GREEN"));
  assert(!strcmp(ui_theme_preset_names[UiThemeStealthBlack], "STEALTH BLACK"));
  assert(!strcmp(ui_theme_preset_names[UiThemeChromeSilver], "CHROME SILVER"));
  assert(!strcmp(ui_theme_color_names[UiColorGreen], "Green"));

  ui_theme_reset(UiThemeElectricBlue);
  assert(ui_theme_preset == UiThemeElectricBlue);
  assert(ui_wallpaper == UiWallpaperGrid);
  assert(ui_background_color == UiColorNavy);
  assert(ui_accent_color == UiColorBlue);
  assert(ui_selection_color == UiColorCyan);
  assert(ui_contrast == UiContrastAuto);

  ui_theme_reset(UiThemeMutantGreen);
  assert(ui_wallpaper == UiWallpaperCircuit);
  assert(ui_background_color == UiColorCharcoal);
  assert(ui_accent_color == UiColorGreen);
  assert(ui_selection_color == UiColorGreen);

  ui_theme_reset(UiThemeStealthBlack);
  assert(ui_wallpaper == UiWallpaperNone);
  assert(ui_background_color == UiColorBlack);
  assert(ui_accent_color == UiColorCharcoal);
  assert(ui_selection_color == UiColorSlate);

  ui_theme_reset(UiThemeChromeSilver);
  assert(ui_wallpaper == UiWallpaperWeave);
  assert(ui_background_color == UiColorSlate);
  assert(ui_accent_color == UiColorCharcoal);
  assert(ui_selection_color == UiColorWhite);
}

static void test_derived_palette_and_safety_colors(void) {
  uint16_t dark[UiV2PaletteCount];
  uint16_t light[UiV2PaletteCount];

  ui_theme_reset(UiThemeElectricBlue);
  ui_theme_apply_palette(dark);
  ui_theme_reset(UiThemeChromeSilver);
  ui_theme_apply_palette(light);

  assert(dark[UiV2Background] != light[UiV2Background]);
  assert(dark[UiV2Card] != dark[UiV2Background]);
  assert(dark[UiV2Stripe] != dark[UiV2Background]);
  assert(dark[UiV2GlowEdge] != dark[UiV2GlowShadow]);
  assert(dark[UiV2GlowEdge] == RGB2GBA(0x00E5FF));
  assert(dark[UiV2Accent] == RGB2GBA(0x3B82FF));
  assert(dark[UiV2DockText] != dark[UiV2BackgroundDeep]);
  assert(dark[UiV2SelectedCard] ==
         expected_mix(dark[UiV2Card], dark[UiV2GlowEdge], 4));
  assert(dark[UiV2GlowShadow] ==
         expected_mix(dark[UiV2GlowEdge], RGB2GBA(0x000000), 2));
  assert(dark[UiV2AccentDark] ==
         expected_mix(dark[UiV2Accent], dark[UiV2Background], 2));
  assert(dark[UiV2Text] != light[UiV2Text]);
  assert(dark[UiV2Folder] == RGB2GBA(0xFFD45A));
  assert(light[UiV2Folder] == RGB2GBA(0xFFD45A));
  assert(dark[UiV2Danger] == RGB2GBA(0xFF4655));
  assert(light[UiV2Danger] == RGB2GBA(0xFF4655));
}

static void test_dock_contrast_on_bright_backgrounds(void) {
  static const unsigned backgrounds[] = {
    UiColorPurple, UiColorAmber, UiColorGreen,
    UiColorWhite, UiColorSlate, UiColorCyan,
  };
  uint16_t palette[UiV2PaletteCount];

  for (unsigned i = 0; i < sizeof(backgrounds) / sizeof(backgrounds[0]); i++) {
    ui_background_color = backgrounds[i];
    ui_contrast = UiContrastAuto;
    ui_theme_apply_palette(palette);
    unsigned dock_luma = test_luminance(palette[UiV2BackgroundDeep]);
    unsigned text_luma = test_luminance(palette[UiV2DockText]);
    unsigned difference = dock_luma > text_luma ? dock_luma - text_luma :
                                                   text_luma - dock_luma;
    assert(difference >= 120);
  }
}

static void test_sanitize(void) {
  ui_theme_preset = 99;
  ui_wallpaper = 99;
  ui_background_color = 99;
  ui_accent_color = 99;
  ui_selection_color = 99;
  ui_contrast = 99;
  ui_theme_sanitize();
  assert(ui_theme_preset < UiThemePresetCount);
  assert(ui_wallpaper < UiWallpaperCount);
  assert(ui_background_color < UiColorCount);
  assert(ui_accent_color < UiColorCount);
  assert(ui_selection_color < UiColorCount);
  assert(ui_contrast < UiContrastCount);
}

int main(void) {
  test_presets();
  test_derived_palette_and_safety_colors();
  test_dock_contrast_on_bright_backgrounds();
  test_sanitize();
  puts("ui theme tests passed");
  return 0;
}

/*
 * Copyright (C) 2026 Danny Nunez
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 */

#ifdef UI_BROWSER_V2

#include <stdbool.h>

#include "gbahw.h"
#include "ui_theme.h"

typedef struct {
  uint8_t wallpaper;
  uint8_t background;
  uint8_t accent;
  uint8_t selection;
  uint8_t contrast;
} t_ui_theme_preset_values;

const char *const ui_theme_preset_names[UiThemePresetCount] = {
  "ELECTRIC BLUE", "MUTANT GREEN", "STEALTH BLACK", "CHROME SILVER",
};

const char *const ui_wallpaper_names[UiWallpaperCount] = {
  "None", "Weave", "Grid", "Circuit",
};

const char *const ui_contrast_names[UiContrastCount] = {
  "Auto", "Dark", "Light",
};

const char *const ui_theme_color_names[UiColorCount] = {
  "Black", "Charcoal", "Slate", "Navy", "Teal", "Burgundy", "Cyan",
  "Blue", "Purple", "Red", "Amber", "Green", "Ice", "White",
};

static const uint16_t ui_theme_colors[UiColorCount] = {
  RGB2GBA(0x08090D), RGB2GBA(0x171A21), RGB2GBA(0xD7DCE5),
  RGB2GBA(0x071424), RGB2GBA(0x0B3336), RGB2GBA(0x25090E),
  RGB2GBA(0x00E5FF), RGB2GBA(0x3B82FF), RGB2GBA(0xB65CFF),
  RGB2GBA(0xFF2D45), RGB2GBA(0xFFD84A), RGB2GBA(0x39FF70),
  RGB2GBA(0xEAFBFF), RGB2GBA(0xFFFFFF),
};

static const t_ui_theme_preset_values ui_theme_presets[UiThemePresetCount] = {
  { UiWallpaperGrid,    UiColorNavy,     UiColorBlue,     UiColorCyan,  UiContrastAuto },
  { UiWallpaperCircuit, UiColorCharcoal, UiColorGreen,    UiColorGreen, UiContrastAuto },
  { UiWallpaperNone,    UiColorBlack,    UiColorCharcoal, UiColorSlate, UiContrastAuto },
  { UiWallpaperWeave,   UiColorSlate,    UiColorCharcoal, UiColorWhite, UiContrastAuto },
};

uint32_t ui_theme_preset = UiThemeElectricBlue;
uint32_t ui_wallpaper = UiWallpaperGrid;
uint32_t ui_background_color = UiColorNavy;
uint32_t ui_accent_color = UiColorBlue;
uint32_t ui_selection_color = UiColorCyan;
uint32_t ui_contrast = UiContrastAuto;

static uint16_t mix_color(uint16_t first, uint16_t second, unsigned weight) {
  unsigned inv = 8 - weight;
  unsigned r = (((first & 31) * inv) + ((second & 31) * weight) + 4) >> 3;
  unsigned g = ((((first >> 5) & 31) * inv) +
                (((second >> 5) & 31) * weight) + 4) >> 3;
  unsigned b = ((((first >> 10) & 31) * inv) +
                (((second >> 10) & 31) * weight) + 4) >> 3;
  return r | (g << 5) | (b << 10);
}

static unsigned luminance(uint16_t color) {
  return (color & 31) * 3 + ((color >> 5) & 31) * 6 +
         ((color >> 10) & 31);
}

void ui_theme_reset(unsigned preset) {
  if (preset >= UiThemePresetCount)
    preset = UiThemeElectricBlue;
  const t_ui_theme_preset_values *values = &ui_theme_presets[preset];
  ui_theme_preset = preset;
  ui_wallpaper = values->wallpaper;
  ui_background_color = values->background;
  ui_accent_color = values->accent;
  ui_selection_color = values->selection;
  ui_contrast = values->contrast;
}

void ui_theme_sanitize(void) {
  ui_theme_preset %= UiThemePresetCount;
  ui_wallpaper %= UiWallpaperCount;
  ui_background_color %= UiColorCount;
  ui_accent_color %= UiColorCount;
  ui_selection_color %= UiColorCount;
  ui_contrast %= UiContrastCount;
}

void ui_theme_apply_palette(volatile uint16_t *palette) {
  ui_theme_sanitize();

  const uint16_t black = RGB2GBA(0x000000);
  const uint16_t white = RGB2GBA(0xFFF8F0);
  const uint16_t background = ui_theme_colors[ui_background_color];
  const uint16_t accent = ui_theme_colors[ui_accent_color];
  const uint16_t selection = ui_theme_colors[ui_selection_color];
  bool use_light_text = ui_contrast == UiContrastLight ||
                        (ui_contrast == UiContrastAuto &&
                         luminance(background) < 155);
  const uint16_t text = use_light_text ? white : RGB2GBA(0x10131A);
  const uint16_t shade_target = use_light_text ? white : black;
  const uint16_t card = mix_color(background, shade_target, 1);
  const uint16_t dock = mix_color(background, black, 4);
  bool use_light_dock_text = ui_contrast == UiContrastLight ||
                             (ui_contrast == UiContrastAuto &&
                              luminance(dock) < 155);
  const uint16_t dock_text = use_light_dock_text ? white : RGB2GBA(0x10131A);

  palette[UiV2Text] = text;
  palette[UiV2BackgroundDeep] = dock;
  palette[UiV2Background] = background;
  palette[UiV2Stripe] = mix_color(background, shade_target, 1);
  palette[UiV2StripeLight] = mix_color(background, shade_target, 2);
  palette[UiV2Card] = card;
  palette[UiV2SelectedCard] = mix_color(card, selection, 4);
  palette[UiV2CardShadow] = mix_color(background, black, 4);
  palette[UiV2CardEdge] = mix_color(card, shade_target, 2);
  palette[UiV2GlowEdge] = selection;
  palette[UiV2GlowShadow] = mix_color(selection, black, 2);
  palette[UiV2Accent] = accent;
  palette[UiV2AccentDark] = mix_color(accent, background, 2);
  palette[UiV2DockText] = dock_text;
  palette[UiV2White] = text;
  palette[UiV2Muted] = mix_color(text, background, 3);
  palette[UiV2Folder] = RGB2GBA(0xFFD45A);
  palette[UiV2Danger] = RGB2GBA(0xFF4655);
  palette[UiV2Disabled] = mix_color(RGB2GBA(0x777777), background, 2);
  palette[UiV2FolderInset] = RGB2GBA(0x6A3510);
}

#endif

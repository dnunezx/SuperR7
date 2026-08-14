/*
 * Copyright (C) 2026 Danny Nunez (dnunezx)
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 */

#ifndef _UI_THEME_H__
#define _UI_THEME_H__

#include <stdint.h>

typedef enum {
  UiThemeElectricBlue = 0,
  UiThemeMutantGreen,
  UiThemeStealthBlack,
  UiThemeChromeSilver,
  UiThemePresetCount,
} t_ui_theme_preset;

typedef enum {
  UiWallpaperNone = 0,
  UiWallpaperWeave,
  UiWallpaperGrid,
  UiWallpaperCircuit,
  UiWallpaperTechFrame,
  UiWallpaperCount,
} t_ui_wallpaper;

typedef enum {
  UiContrastAuto = 0,
  UiContrastDark,
  UiContrastLight,
  UiContrastCount,
} t_ui_contrast;

typedef enum {
  UiColorBlack = 0,
  UiColorCharcoal,
  UiColorSlate,
  UiColorNavy,
  UiColorTeal,
  UiColorBurgundy,
  UiColorCyan,
  UiColorBlue,
  UiColorPurple,
  UiColorRed,
  UiColorAmber,
  UiColorGreen,
  UiColorIce,
  UiColorWhite,
  UiColorCount,
} t_ui_theme_color;

typedef enum {
  UiV2Text = 0,
  UiV2BackgroundDeep,
  UiV2Background,
  UiV2Stripe,
  UiV2StripeLight,
  UiV2Card,
  UiV2SelectedCard,
  UiV2CardShadow,
  UiV2CardEdge,
  UiV2GlowEdge,
  UiV2GlowShadow,
  UiV2Accent,
  UiV2AccentDark,
  UiV2DockText,
  UiV2White,
  UiV2Muted,
  UiV2Folder,
  UiV2Danger,
  UiV2Disabled,
  UiV2FolderInset,
  UiV2PaletteCount,
} t_ui_theme_palette;

extern uint32_t ui_theme_preset;
extern uint32_t ui_wallpaper;
extern uint32_t ui_background_color;
extern uint32_t ui_accent_color;
extern uint32_t ui_selection_color;
extern uint32_t ui_contrast;

extern const char *const ui_theme_preset_names[UiThemePresetCount];
extern const char *const ui_wallpaper_names[UiWallpaperCount];
extern const char *const ui_contrast_names[UiContrastCount];
extern const char *const ui_theme_color_names[UiColorCount];

void ui_theme_reset(unsigned preset);
void ui_theme_sanitize(void);
void ui_theme_apply_palette(volatile uint16_t *palette);

#endif

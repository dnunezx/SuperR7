/*
 * Copyright (C) 2026 SuperFW contributors
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 */

#ifndef _COVER_H__
#define _COVER_H__

#include <stdbool.h>
#include <stdint.h>

#define COVER_WIDTH                 72
#define COVER_HEIGHT               104
#define COVER_PIXEL_COUNT          (COVER_WIDTH * COVER_HEIGHT)
#define COVER_PALETTE_BASE          20
#define COVER_MAX_PALETTE_COLORS    220
#define COVER_HEADER_SIZE           32
#define COVER_MAX_FILE_SIZE         (COVER_HEADER_SIZE + 2 * COVER_MAX_PALETTE_COLORS + COVER_PIXEL_COUNT)
#define COVER_PATH_MAX              256
#define COVER_LOAD_DELAY_MS         180
#define COVER_DIRECTORY             "/.superfw/covers/"

typedef enum {
  CoverEmpty = 0,
  CoverPending,
  CoverReady,
  CoverMissing,
  CoverInvalid,
  CoverIoError,
} t_cover_state;

typedef enum {
  CoverReadOk = 0,
  CoverReadMissing,
  CoverReadTooLarge,
  CoverReadIoError,
} t_cover_read_result;

typedef struct {
  uint16_t palette_count;
  uint16_t palette_offset;
  uint16_t pixel_offset;
} t_cover_info;

typedef t_cover_read_result (*t_cover_reader)(const char *path, uint8_t *data,
                                               unsigned capacity, unsigned *size);

typedef struct {
  uint32_t storage[(COVER_MAX_FILE_SIZE + 3) / 4];
  char path[COVER_PATH_MAX];
  uint32_t requested_at;
  uint16_t file_size;
  t_cover_info info;
  uint8_t state;
} t_cover_cache;

uint32_t cover_crc32(const uint8_t *data, unsigned size);
bool cover_validate(const uint8_t *data, unsigned size, t_cover_info *info);
bool cover_build_path(char *output, unsigned output_size, const char *rom_path);

void cover_cache_init(t_cover_cache *cache);
void cover_cache_clear(t_cover_cache *cache);
void cover_cache_request(t_cover_cache *cache, const char *rom_path, uint32_t now);
void cover_cache_poll(t_cover_cache *cache, uint32_t now, t_cover_reader reader);

const uint16_t *cover_cache_palette(const t_cover_cache *cache);
const uint8_t *cover_cache_pixels(const t_cover_cache *cache);

#ifdef __GBA__
t_cover_read_result cover_fatfs_read(const char *path, uint8_t *data,
                                     unsigned capacity, unsigned *size);
#endif

#endif

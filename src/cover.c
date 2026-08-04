/*
 * Copyright (C) 2026 SuperFW contributors
 *
 * This program is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 */

#include <string.h>

#include "cover.h"

#ifdef __GBA__
#include "fatfs/ff.h"
#endif

static uint16_t read16le(const uint8_t *p) {
  return p[0] | ((uint16_t)p[1] << 8);
}

static uint32_t read32le(const uint8_t *p) {
  return p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

static bool ascii_equal_nocase(char a, char b) {
  if (a >= 'A' && a <= 'Z')
    a += 'a' - 'A';
  if (b >= 'A' && b <= 'Z')
    b += 'a' - 'A';
  return a == b;
}

static bool has_extension(const char *path, const char *extension) {
  unsigned plen = strlen(path);
  unsigned elen = strlen(extension);
  if (plen < elen)
    return false;
  path += plen - elen;
  for (unsigned i = 0; i < elen; i++)
    if (!ascii_equal_nocase(path[i], extension[i]))
      return false;
  return true;
}

static bool is_supported_rom(const char *path) {
  return has_extension(path, ".gba") || has_extension(path, ".gb") ||
         has_extension(path, ".gbc") || has_extension(path, ".nes") ||
         has_extension(path, ".sms");
}

uint32_t cover_crc32(const uint8_t *data, unsigned size) {
  uint32_t crc = 0xFFFFFFFF;
  for (unsigned i = 0; i < size; i++) {
    crc ^= data[i];
    for (unsigned bit = 0; bit < 8; bit++)
      crc = (crc >> 1) ^ (0xEDB88320 & (0 - (crc & 1)));
  }
  return crc ^ 0xFFFFFFFF;
}

bool cover_validate(const uint8_t *data, unsigned size, t_cover_info *info) {
  if (!data || size < COVER_HEADER_SIZE || size > COVER_MAX_FILE_SIZE)
    return false;
  if (memcmp(data, "SFCV", 4) || data[4] != 1 || data[5] != COVER_HEADER_SIZE)
    return false;
  if (read16le(&data[6]) != 0 || data[15] != 0 || read32le(&data[28]) != 0)
    return false;
  if (read16le(&data[8]) != COVER_WIDTH || read16le(&data[10]) != COVER_HEIGHT)
    return false;

  unsigned palette_count = read16le(&data[12]);
  unsigned palette_bytes = read32le(&data[16]);
  unsigned pixel_bytes = read32le(&data[20]);
  if (!palette_count || palette_count > COVER_MAX_PALETTE_COLORS)
    return false;
  if (data[14] != COVER_PALETTE_BASE || palette_bytes != palette_count * 2)
    return false;
  if (pixel_bytes != COVER_PIXEL_COUNT)
    return false;
  if (size != COVER_HEADER_SIZE + palette_bytes + pixel_bytes)
    return false;
  if (cover_crc32(&data[COVER_HEADER_SIZE], palette_bytes + pixel_bytes) != read32le(&data[24]))
    return false;

  for (unsigned i = 0; i < palette_count; i++)
    if (read16le(&data[COVER_HEADER_SIZE + i * 2]) & 0x8000)
      return false;

  unsigned pixel_offset = COVER_HEADER_SIZE + palette_bytes;
  unsigned last_color = COVER_PALETTE_BASE + palette_count - 1;
  for (unsigned i = 0; i < pixel_bytes; i++)
    if (data[pixel_offset + i] < COVER_PALETTE_BASE || data[pixel_offset + i] > last_color)
      return false;

  if (info) {
    info->palette_count = palette_count;
    info->palette_offset = COVER_HEADER_SIZE;
    info->pixel_offset = pixel_offset;
  }
  return true;
}

bool cover_build_path(char *output, unsigned output_size, const char *rom_path) {
  if (!output || !output_size || !rom_path || !is_supported_rom(rom_path))
    return false;

  const char *basename = rom_path;
  for (const char *p = rom_path; *p; p++)
    if (*p == '/' || *p == '\\')
      basename = p + 1;

  const char *dot = NULL;
  for (const char *p = basename; *p; p++)
    if (*p == '.')
      dot = p;
  if (!dot || dot == basename)
    return false;

  unsigned prefix_len = sizeof(COVER_DIRECTORY) - 1;
  unsigned stem_len = dot - basename;
  static const char suffix[] = ".sfcov";
  if (prefix_len + stem_len + sizeof(suffix) > output_size)
    return false;

  memcpy(output, COVER_DIRECTORY, prefix_len);
  memcpy(output + prefix_len, basename, stem_len);
  memcpy(output + prefix_len + stem_len, suffix, sizeof(suffix));
  return true;
}

void cover_cache_clear(t_cover_cache *cache) {
  cache->path[0] = 0;
  cache->file_size = 0;
  cache->info.palette_count = 0;
  cache->info.palette_offset = 0;
  cache->info.pixel_offset = 0;
  cache->state = CoverEmpty;
}

void cover_cache_init(t_cover_cache *cache) {
  memset(cache, 0, sizeof(*cache));
}

void cover_cache_request(t_cover_cache *cache, const char *rom_path, uint32_t now) {
  char path[COVER_PATH_MAX];
  if (!cover_build_path(path, sizeof(path), rom_path)) {
    cover_cache_clear(cache);
    return;
  }
  if (cache->state != CoverEmpty && !strcmp(cache->path, path))
    return;

  strcpy(cache->path, path);
  cache->requested_at = now;
  cache->file_size = 0;
  cache->info.palette_count = 0;
  cache->state = CoverPending;
}

void cover_cache_poll(t_cover_cache *cache, uint32_t now, t_cover_reader reader) {
  if (cache->state != CoverPending || !reader || now - cache->requested_at < COVER_LOAD_DELAY_MS)
    return;

  unsigned size = 0;
  t_cover_read_result result = reader(cache->path, (uint8_t *)cache->storage,
                                      COVER_MAX_FILE_SIZE, &size);
  cache->file_size = 0;
  cache->info.palette_count = 0;
  if (result == CoverReadMissing)
    cache->state = CoverMissing;
  else if (result == CoverReadIoError)
    cache->state = CoverIoError;
  else if (result == CoverReadTooLarge || !cover_validate((uint8_t *)cache->storage, size, &cache->info))
    cache->state = CoverInvalid;
  else {
    cache->file_size = size;
    cache->state = CoverReady;
  }
}

const uint16_t *cover_cache_palette(const t_cover_cache *cache) {
  if (cache->state != CoverReady)
    return NULL;
  return (const uint16_t *)((const uint8_t *)cache->storage + cache->info.palette_offset);
}

const uint8_t *cover_cache_pixels(const t_cover_cache *cache) {
  if (cache->state != CoverReady)
    return NULL;
  return (const uint8_t *)cache->storage + cache->info.pixel_offset;
}

#ifdef __GBA__
t_cover_read_result cover_fatfs_read(const char *path, uint8_t *data,
                                     unsigned capacity, unsigned *size) {
  FIL file;
  FRESULT result = f_open(&file, path, FA_READ);
  if (result == FR_NO_FILE || result == FR_NO_PATH)
    return CoverReadMissing;
  if (result != FR_OK)
    return CoverReadIoError;

  FSIZE_t file_size = f_size(&file);
  if (file_size > capacity) {
    f_close(&file);
    return CoverReadTooLarge;
  }

  UINT bytes_read = 0;
  result = f_read(&file, data, file_size, &bytes_read);
  FRESULT close_result = f_close(&file);
  if (result != FR_OK || close_result != FR_OK || bytes_read != file_size)
    return CoverReadIoError;
  *size = bytes_read;
  return CoverReadOk;
}
#endif

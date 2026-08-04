#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "cover.h"

static uint8_t fixture[COVER_MAX_FILE_SIZE];
static unsigned fixture_size;
static unsigned reader_calls;
static t_cover_read_result reader_result;

static void write16le(uint8_t *p, uint16_t value) {
  p[0] = value;
  p[1] = value >> 8;
}

static void write32le(uint8_t *p, uint32_t value) {
  p[0] = value;
  p[1] = value >> 8;
  p[2] = value >> 16;
  p[3] = value >> 24;
}

static void make_fixture(void) {
  const unsigned palette_count = 2;
  const unsigned palette_bytes = palette_count * 2;
  fixture_size = COVER_HEADER_SIZE + palette_bytes + COVER_PIXEL_COUNT;
  memset(fixture, 0, fixture_size);
  memcpy(fixture, "SFCV", 4);
  fixture[4] = COVER_FORMAT_VERSION;
  fixture[5] = COVER_HEADER_SIZE;
  write16le(&fixture[8], COVER_WIDTH);
  write16le(&fixture[10], COVER_HEIGHT);
  write16le(&fixture[12], palette_count);
  fixture[14] = COVER_PALETTE_BASE;
  write32le(&fixture[16], palette_bytes);
  write32le(&fixture[20], COVER_PIXEL_COUNT);
  write16le(&fixture[COVER_HEADER_SIZE], 0x001F);
  write16le(&fixture[COVER_HEADER_SIZE + 2], 0x7C00);
  memset(&fixture[COVER_HEADER_SIZE + palette_bytes], COVER_PALETTE_BASE,
         COVER_PIXEL_COUNT);
  write32le(&fixture[24], cover_crc32(&fixture[COVER_HEADER_SIZE],
                                      palette_bytes + COVER_PIXEL_COUNT));
}

static t_cover_read_result fake_reader(const char *path, uint8_t *data,
                                       unsigned capacity, unsigned *size) {
  reader_calls++;
  assert(!strcmp(path, "/.superfw/covers/Pokemon Emerald.sfcov"));
  if (reader_result != CoverReadOk)
    return reader_result;
  assert(fixture_size <= capacity);
  memcpy(data, fixture, fixture_size);
  *size = fixture_size;
  return CoverReadOk;
}

static void test_crc_and_validation(void) {
  static const uint8_t crc_text[] = "123456789";
  assert(cover_crc32(crc_text, 9) == 0xCBF43926);

  t_cover_info info;
  make_fixture();
  assert(cover_validate(fixture, fixture_size, &info));
  assert(info.palette_count == 2);
  assert(info.palette_offset == COVER_HEADER_SIZE);
  assert(info.pixel_offset == COVER_HEADER_SIZE + 4);

  fixture[0] = 'X';
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[4] = COVER_FORMAT_VERSION - 1;
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[5] = 31;
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[6] = 1;
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); write16le(&fixture[8], COVER_WIDTH + 1);
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); write16le(&fixture[12], 0);
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[14]++;
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); write32le(&fixture[16], 2);
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); write32le(&fixture[20], COVER_PIXEL_COUNT - 1);
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[24] ^= 1;
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[COVER_HEADER_SIZE + 1] |= 0x80;
  write32le(&fixture[24], cover_crc32(&fixture[COVER_HEADER_SIZE], fixture_size - COVER_HEADER_SIZE));
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture(); fixture[COVER_HEADER_SIZE + 4] = COVER_PALETTE_BASE + 2;
  write32le(&fixture[24], cover_crc32(&fixture[COVER_HEADER_SIZE], fixture_size - COVER_HEADER_SIZE));
  assert(!cover_validate(fixture, fixture_size, NULL));
  make_fixture();
  assert(!cover_validate(fixture, fixture_size - 1, NULL));
  assert(!cover_validate(fixture, fixture_size + 1, NULL));
}

static void test_path_lookup(void) {
  char path[COVER_PATH_MAX];
  assert(cover_build_path(path, sizeof(path), "/Games/Pokemon Emerald.gba"));
  assert(!strcmp(path, "/.superfw/covers/Pokemon Emerald.sfcov"));
  assert(cover_build_path(path, sizeof(path), "folder/foo.bar.GBC"));
  assert(!strcmp(path, "/.superfw/covers/foo.bar.sfcov"));
  assert(cover_build_path(path, sizeof(path), "C:\\Roms\\Zelda.gb"));
  assert(!strcmp(path, "/.superfw/covers/Zelda.sfcov"));
  assert(!cover_build_path(path, sizeof(path), "readme.txt"));
  assert(!cover_build_path(path, 12, "game.gba"));

  char fallback[COVER_PATH_MAX];
  assert(cover_build_fallback_path(
      fallback, sizeof(fallback),
      "/.superfw/covers/Metal Slug Advance (USA).sfcov"));
  assert(!strcmp(fallback, "/Metal Slug Advance (USA).sfcov"));
  assert(cover_build_fallback_path(fallback, sizeof(fallback),
                                   "/covers/Game.sfcov"));
  assert(!strcmp(fallback, "/Game.sfcov"));
  assert(cover_build_fallback_path(fallback, sizeof(fallback),
                                   "C:\\covers\\Game.sfcov"));
  assert(!strcmp(fallback, "/Game.sfcov"));
  assert(cover_build_fallback_path(
      fallback, sizeof(fallback),
      "/.superfw/covers/Legend of Zelda, The - The Minish Cap (USA).sfcov"));
  assert(!strcmp(fallback,
                 "/Legend of Zelda, The - The Minish Cap (USA).sfcov"));
  assert(!cover_build_fallback_path(fallback, sizeof(fallback),
                                    "/covers/Game.png"));
  assert(!cover_build_fallback_path(fallback, 11,
                                    "/.superfw/covers/Game.sfcov"));
  assert(cover_build_short_fallback_path(
      fallback, sizeof(fallback),
      "/.superfw/covers/Metal Slug Advance (USA).sfcov"));
  assert(!strcmp(fallback, "/24929DEE.cov"));
  assert(cover_build_short_fallback_path(
      fallback, sizeof(fallback), "/covers/Metal Slug Advance (USA).sfcov"));
  assert(!strcmp(fallback, "/24929DEE.cov"));
  assert(cover_build_short_fallback_path(
      fallback, sizeof(fallback),
      "/.superfw/covers/Legend of Zelda, The - The Minish Cap (USA).sfcov"));
  assert(!strcmp(fallback, "/A4077507.cov"));
  strcpy(path, "/.superfw/covers/Metal Slug Advance (USA).sfcov");
  assert(cover_build_short_fallback_path(path, sizeof(path), path));
  assert(!strcmp(path, "/24929DEE.cov"));
  assert(!cover_build_short_fallback_path(
      fallback, sizeof(fallback), "/.superfw/covers/Game.png"));
  assert(!cover_build_short_fallback_path(
      fallback, 12, "/.superfw/covers/Game.sfcov"));

  char long_name[300];
  memset(long_name, 'a', sizeof(long_name));
  memcpy(&long_name[sizeof(long_name) - 5], ".gba", 5);
  assert(!cover_build_path(path, sizeof(path), long_name));
}

static void test_deferred_cache(void) {
  t_cover_cache cache;
  cover_cache_init(&cache);
  assert(cache.state == CoverEmpty);
  assert(!cover_cache_palette(&cache));

  make_fixture();
  reader_calls = 0;
  reader_result = CoverReadOk;
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 1000);
  assert(cache.state == CoverPending);
  cover_cache_poll(&cache, 1179, fake_reader);
  assert(cache.state == CoverPending && reader_calls == 0);
  cover_cache_poll(&cache, 1180, fake_reader);
  assert(cache.state == CoverReady && reader_calls == 1);
  assert(cache.file_size == fixture_size);
  assert(cache.info.palette_count == 2);
  assert(cover_cache_palette(&cache)[0] == 0x001F);
  assert(cover_cache_pixels(&cache)[0] == COVER_PALETTE_BASE);

  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 2000);
  cover_cache_poll(&cache, 3000, fake_reader);
  assert(cache.state == CoverReady && reader_calls == 1);

  /* A changed selection must hide the old render data immediately. */
  cover_cache_request(&cache, "/Games/Another Game.gba", 3100);
  assert(cache.state == CoverPending);
  assert(!cover_cache_palette(&cache));
  assert(!cover_cache_pixels(&cache));

  /* Returning to the first game schedules one fresh read. */
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 3200);
  cover_cache_poll(&cache, 3380, fake_reader);
  assert(cache.state == CoverReady && reader_calls == 2);

  cover_cache_request(&cache, "notes.txt", 3000);
  assert(cache.state == CoverEmpty);
  assert(!cover_cache_pixels(&cache));

  reader_result = CoverReadMissing;
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 4000);
  cover_cache_poll(&cache, 4180, fake_reader);
  assert(cache.state == CoverMissing);

  cover_cache_clear(&cache);
  reader_result = CoverReadIoError;
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 5000);
  cover_cache_poll(&cache, 5180, fake_reader);
  assert(cache.state == CoverIoError);

  cover_cache_clear(&cache);
  reader_result = CoverReadTooLarge;
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", 6000);
  cover_cache_poll(&cache, 6180, fake_reader);
  assert(cache.state == CoverInvalid);

  cover_cache_clear(&cache);
  reader_result = CoverReadOk;
  make_fixture();
  fixture[0] = 'X';
  cover_cache_request(&cache, "/Games/Pokemon Emerald.gba", UINT32_MAX - 100);
  cover_cache_poll(&cache, 79, fake_reader);
  assert(cache.state == CoverInvalid);
}

int main(void) {
  test_crc_and_validation();
  test_path_lookup();
  test_deferred_cache();
  puts("cover tests passed");
  return 0;
}

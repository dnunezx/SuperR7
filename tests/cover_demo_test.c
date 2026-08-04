#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "cover.h"

int main(void) {
  uint8_t aurora[COVER_MAX_FILE_SIZE];
  uint8_t checker[COVER_MAX_FILE_SIZE];
  uint8_t broken[COVER_MAX_FILE_SIZE];
  unsigned aurora_size = 0, checker_size = 0, broken_size = 0;
  t_cover_info info;

  assert(cover_demo_read(COVER_DIRECTORY "Aurora.sfcov", aurora,
                         sizeof(aurora), &aurora_size) == CoverReadOk);
  assert(cover_validate(aurora, aurora_size, &info));
  assert(info.palette_count == 8);

  assert(cover_demo_read(COVER_DIRECTORY "Checker.sfcov", checker,
                         sizeof(checker), &checker_size) == CoverReadOk);
  assert(cover_validate(checker, checker_size, NULL));
  assert(checker_size == aurora_size);
  assert(memcmp(&aurora[info.pixel_offset], &checker[info.pixel_offset],
                COVER_PIXEL_COUNT));

  assert(cover_demo_read(COVER_DIRECTORY "Broken.sfcov", broken,
                         sizeof(broken), &broken_size) == CoverReadOk);
  assert(!cover_validate(broken, broken_size, NULL));
  assert(cover_demo_read(COVER_DIRECTORY "Missing.sfcov", broken,
                         sizeof(broken), &broken_size) == CoverReadMissing);

  puts("cover demo fixture tests passed");
  return 0;
}

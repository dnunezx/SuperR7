/* Copyright (C) 2026 Danny Nunez (dnunezx) */

#include <assert.h>

#include "menu_nav.h"

static void move(int *selector, int *seloff, int count,
                 int item_delta, int page_delta) {
  menu_list_navigate(selector, seloff, count, 7, item_delta, page_delta);
}

int main(void) {
  int selector = 0;
  int seloff = 0;

  /* A seven-entry list has no next page, so paging is a no-op. */
  move(&selector, &seloff, 7, 0, 1);
  assert(selector == 0);
  assert(seloff == 0);

  /* The final page may be partial and begins on a fixed boundary. */
  selector = 0;
  seloff = 0;
  move(&selector, &seloff, 8, 0, 1);
  assert(selector == 7);
  assert(seloff == 7);

  /* Item movement crosses fixed page boundaries in either direction. */
  selector = 6;
  seloff = 0;
  move(&selector, &seloff, 15, 1, 0);
  assert(selector == 7);
  assert(seloff == 7);
  move(&selector, &seloff, 15, -1, 0);
  assert(selector == 6);
  assert(seloff == 0);

  /* Page movement selects the first item on the adjacent fixed page. */
  selector = 3;
  seloff = 0;
  move(&selector, &seloff, 15, 0, 1);
  assert(selector == 7);
  assert(seloff == 7);

  /* The final partial page is stable at both navigation boundaries. */
  selector = 7;
  seloff = 7;
  move(&selector, &seloff, 15, 0, 1);
  assert(selector == 14);
  assert(seloff == 14);
  move(&selector, &seloff, 15, 0, 1);
  assert(selector == 14);
  assert(seloff == 14);
  move(&selector, &seloff, 15, 0, -1);
  assert(selector == 7);
  assert(seloff == 7);

  selector = 0;
  seloff = 0;
  move(&selector, &seloff, 15, 0, -1);
  assert(selector == 0);
  assert(seloff == 0);

  /* Page movement takes priority over a simultaneous item delta. */
  move(&selector, &seloff, 15, 1, 1);
  assert(selector == 7);
  assert(seloff == 7);

  /* Existing selections normalize to their fixed page without moving. */
  selector = 14;
  seloff = 8;
  move(&selector, &seloff, 15, 0, 0);
  assert(selector == 14);
  assert(seloff == 14);

  /* Empty lists always have a safe zero position. */
  selector = 12;
  seloff = 9;
  move(&selector, &seloff, 0, 0, 1);
  assert(selector == 0);
  assert(seloff == 0);

  return 0;
}

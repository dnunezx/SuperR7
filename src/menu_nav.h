/*
 * Copyright (C) 2026 Danny Nunez (dnunezx)
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 */

#ifndef _MENU_NAV_H__
#define _MENU_NAV_H__

static inline int menu_nav_clamp(int value, int low, int high) {
  return value < low ? low : value > high ? high : value;
}

/*
 * Keep list selection on fixed pages. Item movement crosses page boundaries,
 * while page movement selects the first item of the previous or next page.
 * The final page may contain fewer than rows entries.
 */
static inline void menu_list_navigate(int *selector, int *seloff,
                                      int maxentries, int rows,
                                      int item_delta, int page_delta) {
  if (maxentries <= 0 || rows <= 0) {
    *selector = 0;
    *seloff = 0;
    return;
  }

  *selector = menu_nav_clamp(*selector, 0, maxentries - 1);

  if (page_delta) {
    int page_count = (maxentries + rows - 1) / rows;
    int current_page = *selector / rows;
    int target_page = menu_nav_clamp(current_page + page_delta,
                                     0, page_count - 1);
    if (target_page != current_page)
      *selector = target_page * rows;
  } else {
    *selector = menu_nav_clamp(*selector + item_delta, 0, maxentries - 1);
  }

  *seloff = (*selector / rows) * rows;
}

#endif

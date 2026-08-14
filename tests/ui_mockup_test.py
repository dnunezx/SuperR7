# Copyright (C) 2026 Danny Nunez (dnunezx)

import unittest

from PIL import Image

from tools import render_ui_phase1


class UiMockupTest(unittest.TestCase):
    def setUp(self):
        self.cover_color = (18, 52, 86)
        self.cover = Image.new("RGB", (72, 72), self.cover_color)

    def test_native_variants_have_exact_gba_dimensions(self):
        for row_count in (5, 6):
            with self.subTest(row_count=row_count):
                image = render_ui_phase1.render(row_count, self.cover)
                self.assertEqual((240, 160), image.size)

    def test_ui_pixels_stay_inside_the_declared_20_color_set(self):
        image = render_ui_phase1.render(6, self.cover)
        allowed = {
            tuple(int(color[index:index + 2], 16) for index in (1, 3, 5))
            for color in render_ui_phase1.UI_COLORS.values()
        }
        for y in range(image.height):
            for x in range(image.width):
                if 6 <= x <= 77 and 34 <= y <= 105:
                    continue
                self.assertIn(image.getpixel((x, y)), allowed)

    def test_cover_pixels_are_preserved_at_native_size(self):
        image = render_ui_phase1.render(6, self.cover)
        self.assertEqual(self.cover_color, image.getpixel((6, 34)))
        self.assertEqual(self.cover_color, image.getpixel((77, 105)))

    def test_six_rows_leave_clear_space_before_the_dock(self):
        image = render_ui_phase1.render(6, self.cover)
        self.assertEqual(
            render_ui_phase1.UI_COLORS["stripe"],
            "#%02X%02X%02X" % image.getpixel((90, 137)),
        )

    def test_glow_variants_keep_native_size_and_distinct_selection_colors(self):
        seen = set()
        for name, glow in render_ui_phase1.GLOW_VARIANTS.items():
            with self.subTest(name=name):
                image = render_ui_phase1.render(6, self.cover, glow=glow)
                self.assertEqual((240, 160), image.size)
                self.assertEqual(glow[0].lower(), "#%02x%02x%02x" % image.getpixel((90, 4)))
                seen.add(image.getpixel((90, 4)))
        self.assertEqual(3, len(seen))


if __name__ == "__main__":
    unittest.main()

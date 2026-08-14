# Copyright (C) 2026 Danny Nunez (dnunezx)

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.cover_converter_v2 import image_to_cover as image_to_v2_cover
from tools.cover_converter import (
    batch_convert,
    convert_file,
    cover_to_image,
    image_to_cover,
)
from tools.sfcov_v2 import Cover as CoverV2, CoverFormatError as CoverV2Error
from tools.sfcov import (
    Cover,
    CoverFormatError,
    HEADER_SIZE,
    HEIGHT,
    PALETTE_BASE,
    PIXEL_COUNT,
    VERSION,
    WIDTH,
)


class CoverConverterTest(unittest.TestCase):
    def test_v3_round_trip_is_76_by_76(self):
        cover = image_to_cover(
            Image.new("RGB", (300, 500), (248, 32, 16)), dither="none"
        )
        self.assertEqual(VERSION, 3)
        self.assertEqual((WIDTH, HEIGHT), (76, 76))
        self.assertEqual(len(cover.pixels), PIXEL_COUNT)
        self.assertEqual(set(cover.pixels), {PALETTE_BASE})

        encoded = cover.to_bytes()
        decoded = Cover.from_bytes(encoded)
        self.assertEqual(decoded, cover)
        self.assertEqual(len(encoded), HEADER_SIZE + 2 + PIXEL_COUNT)
        self.assertEqual(cover_to_image(decoded).size, (76, 76))

    def test_v2_and_v3_readers_remain_separate(self):
        v2 = image_to_v2_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        v3 = image_to_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        with self.assertRaises(CoverFormatError):
            Cover.from_bytes(v2.to_bytes())
        with self.assertRaises(CoverV2Error):
            CoverV2.from_bytes(v3.to_bytes())

    def test_conversion_never_overwrites_existing_v2_cover(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "game.png"
            original = root / "game.sfcov"
            v3_output = root / "game-v3.sfcov"
            Image.new("RGB", (100, 100), "red").save(source)
            original.write_bytes(b"original-v2-placeholder")

            convert_file(source, v3_output)
            self.assertEqual(original.read_bytes(), b"original-v2-placeholder")
            self.assertEqual(Cover.read(v3_output).width, 76)

            with self.assertRaises(FileExistsError):
                convert_file(source, v3_output)

    def test_batch_preserves_subdirectories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inputs = root / "inputs"
            outputs = root / "v3-outputs"
            (inputs / "rpg").mkdir(parents=True)
            Image.new("RGB", (30, 50), "green").save(inputs / "rpg" / "Game.png")

            converted = batch_convert(inputs, outputs, recursive=True)
            self.assertEqual(converted, [outputs / "rpg" / "Game.sfcov"])
            self.assertEqual(Cover.read(converted[0]).height, 76)


if __name__ == "__main__":
    unittest.main()

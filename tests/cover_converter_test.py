import struct
import tempfile
import unittest
from pathlib import Path
import zlib

from PIL import Image

from tools.cover_converter import (
    batch_convert,
    convert_file,
    cover_to_image,
    image_to_cover,
)
from tools.sfcov import (
    Cover,
    CoverFormatError,
    HEADER,
    HEADER_SIZE,
    HEIGHT,
    MAX_PALETTE_COLORS,
    PALETTE_BASE,
    PIXEL_COUNT,
    WIDTH,
    bgr555_to_rgb888,
)


class CoverConverterTest(unittest.TestCase):
    def test_solid_image_round_trip(self):
        source = Image.new("RGB", (600, 900), (248, 16, 8))
        cover = image_to_cover(source, dither="none")

        self.assertEqual(len(cover.palette), 1)
        self.assertEqual(len(cover.pixels), PIXEL_COUNT)
        self.assertEqual(set(cover.pixels), {PALETTE_BASE})

        encoded = cover.to_bytes()
        decoded = Cover.from_bytes(encoded)
        self.assertEqual(decoded, cover)
        self.assertEqual(len(encoded), HEADER_SIZE + 2 + PIXEL_COUNT)

        preview = cover_to_image(decoded)
        self.assertEqual(preview.size, (WIDTH, HEIGHT))
        self.assertEqual(preview.getpixel((0, 0)), bgr555_to_rgb888(cover.palette[0]))

    def test_gradient_uses_only_reserved_palette_range(self):
        source = Image.new("RGB", (WIDTH, HEIGHT))
        source.putdata(
            [
                ((x * 255) // (WIDTH - 1), (y * 255) // (HEIGHT - 1), (x + y) & 255)
                for y in range(HEIGHT)
                for x in range(WIDTH)
            ]
        )
        cover = image_to_cover(source)

        self.assertLessEqual(len(cover.palette), MAX_PALETTE_COLORS)
        self.assertLessEqual(len(cover.to_bytes()), HEADER_SIZE + 440 + PIXEL_COUNT)
        self.assertGreaterEqual(min(cover.pixels), PALETTE_BASE)
        self.assertLessEqual(
            max(cover.pixels), PALETTE_BASE + len(cover.palette) - 1
        )
        Cover.from_bytes(cover.to_bytes())

    def test_contain_mode_letterboxes_wide_artwork(self):
        source = Image.new("RGB", (200, 20), (255, 0, 0))
        cover = image_to_cover(source, mode="contain", dither="none")
        preview = cover_to_image(cover)

        self.assertEqual(preview.getpixel((WIDTH // 2, 0)), (0, 0, 0))
        center = preview.getpixel((WIDTH // 2, HEIGHT // 2))
        self.assertGreater(center[0], 240)
        self.assertEqual(center[1:], (0, 0))

    def test_transparency_is_flattened_onto_background(self):
        source = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        cover = image_to_cover(
            source, background=(0, 248, 0), dither="none"
        )
        preview = cover_to_image(cover)
        self.assertEqual(preview.getpixel((0, 0)), (0, 255, 0))

    def test_corrupt_crc_is_rejected(self):
        cover = image_to_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        encoded = bytearray(cover.to_bytes())
        encoded[-1] ^= 1
        with self.assertRaisesRegex(CoverFormatError, "CRC-32"):
            Cover.from_bytes(bytes(encoded))

    def test_wrong_dimensions_are_rejected(self):
        cover = image_to_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        encoded = bytearray(cover.to_bytes())
        fields = list(HEADER.unpack_from(encoded))
        fields[4] = WIDTH + 1
        encoded[:HEADER_SIZE] = HEADER.pack(*fields)
        with self.assertRaisesRegex(CoverFormatError, "exactly"):
            Cover.from_bytes(bytes(encoded))

    def test_trailing_bytes_are_rejected(self):
        cover = image_to_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        with self.assertRaisesRegex(CoverFormatError, "expected"):
            Cover.from_bytes(cover.to_bytes() + b"extra")

    def test_out_of_range_pixel_is_rejected_even_with_valid_crc(self):
        cover = image_to_cover(Image.new("RGB", (1, 1), "blue"), dither="none")
        encoded = bytearray(cover.to_bytes())
        fields = list(HEADER.unpack_from(encoded))
        palette_bytes = fields[9]
        pixel_offset = HEADER_SIZE + palette_bytes
        encoded[pixel_offset] = PALETTE_BASE + len(cover.palette)
        payload = bytes(encoded[HEADER_SIZE:])
        fields[11] = zlib.crc32(payload) & 0xFFFFFFFF
        encoded[:HEADER_SIZE] = HEADER.pack(*fields)
        with self.assertRaisesRegex(CoverFormatError, "pixel indices"):
            Cover.from_bytes(bytes(encoded))

    def test_file_conversion_writes_cover_and_exact_preview(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "game.png"
            output = root / "game.sfcov"
            preview = root / "game-preview.png"
            Image.new("RGB", (100, 150), (16, 80, 248)).save(source)

            converted = convert_file(source, output, preview=preview)
            decoded = Cover.read(output)
            self.assertEqual(decoded, converted)
            with Image.open(preview) as preview_image:
                self.assertEqual(
                    preview_image.convert("RGB").tobytes(),
                    cover_to_image(decoded).tobytes(),
                )

    def test_batch_conversion_preserves_subdirectories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inputs = root / "inputs"
            outputs = root / "outputs"
            previews = root / "previews"
            (inputs / "rpg").mkdir(parents=True)
            Image.new("RGB", (20, 20), "red").save(inputs / "rpg" / "Game.png")
            (inputs / "notes.txt").write_text("not artwork", encoding="utf-8")

            converted = batch_convert(
                inputs,
                outputs,
                preview_dir=previews,
                recursive=True,
            )
            self.assertEqual(converted, [outputs / "rpg" / "Game.sfcov"])
            self.assertTrue((previews / "rpg" / "Game.png").is_file())
            Cover.read(converted[0])

    def test_batch_detects_same_stem_collisions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            inputs = root / "inputs"
            inputs.mkdir()
            Image.new("RGB", (20, 20), "red").save(inputs / "Game.png")
            Image.new("RGB", (20, 20), "blue").save(inputs / "Game.jpg")
            with self.assertRaisesRegex(FileExistsError, "same cover"):
                batch_convert(inputs, root / "outputs")
            self.assertFalse((root / "outputs").exists())

    def test_existing_output_requires_overwrite(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "game.png"
            output = root / "game.sfcov"
            Image.new("RGB", (20, 20), "red").save(source)
            output.write_bytes(b"existing")
            with self.assertRaises(FileExistsError):
                convert_file(source, output)


if __name__ == "__main__":
    unittest.main()

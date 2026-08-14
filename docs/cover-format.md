# SuperR7 cover format (`.sfcov`)

## Version 3 overview

SuperR7 stores cover artwork exactly as the GBA menu needs it. The desktop
converter performs image decoding, cropping, resizing, color reduction, and
GBA color conversion. Firmware validates the file, loads its palette, and
copies its indexed pixels into the menu framebuffer.

The production version 3 format uses:

- Fixed dimensions of 76 by 76 pixels.
- One byte per pixel.
- Between 1 and 220 palette entries.
- Little-endian GBA BGR555 colors.
- Absolute pixel indices from 20 through 239.
- CRC-32 protection for the palette and pixel payload.

Version 3 deliberately rejects older 72-by-72 version 2 files so artwork can
never be drawn using the wrong geometry.

## Main-menu palette allocation

| Indices | Owner |
| --- | --- |
| 0 | Background/transparent base |
| 1-15 | SuperR7 logo |
| 16-19 | Active UI theme |
| 20-239 | Selected-game cover |
| 240-244 | In-game-menu theme handoff |
| 245-255 | Reserved |

Cover pixels store their final absolute palette indices, allowing firmware to
copy them directly into Mode 4 video memory.

## Binary header

All multi-byte integers are little-endian. The header is exactly 32 bytes.

| Offset | Size | Field | Version 3 value |
| ---: | ---: | --- | --- |
| 0 | 4 | Magic | ASCII `SFCV` |
| 4 | 1 | Version | `3` |
| 5 | 1 | Header size | `32` |
| 6 | 2 | Flags | `0` |
| 8 | 2 | Width | `76` |
| 10 | 2 | Height | `76` |
| 12 | 2 | Palette count | `1..220` |
| 14 | 1 | Palette base | `20` |
| 15 | 1 | Reserved | `0` |
| 16 | 4 | Palette byte length | `palette_count * 2` |
| 20 | 4 | Pixel byte length | `76 * 76` (`5776`) |
| 24 | 4 | Payload CRC-32 | CRC of palette bytes followed by pixel bytes |
| 28 | 4 | Reserved | `0` |

## Payload

The header is followed by `palette_count` two-byte BGR555 colors and exactly
5,776 absolute palette indices in row-major order. Bit 15 of every palette
entry must be zero. Trailing bytes are invalid.

The smallest valid file is 5,810 bytes. The largest is 6,248 bytes.

## Lookup convention

For a ROM named `/Games/Pokemon Emerald.gba`, the canonical cover path is:

```text
/.superfw/covers/Pokemon Emerald.sfcov
```

If canonical lookup fails, firmware retries the same filename at the SD-card
root and then an 8.3-safe alias derived from the uppercase CRC-32 of the UTF-8
ROM basename.

## Validation requirements

A reader rejects a cover before drawing when magic, version, header size,
flags, reserved fields, dimensions, palette base, lengths, palette values,
pixel indices, file size, or CRC-32 do not match the version 3 rules.

Use the [SuperR7 cover converter](cover-converter.md) to create and inspect
files. The superseded format is documented under
[legacy cover format v2](legacy/cover-format-v2.md).

# SuperFW Cover Format (`.sfcov`)

## Version 2 overview

The SuperFW cover format stores artwork exactly as the GBA menu needs it. A
desktop converter performs image decoding, cropping, resizing, color reduction,
and GBA color conversion. Firmware only validates the file, loads its palette,
and copies its indexed pixels into the menu framebuffer.

Version 2 uses:

- Fixed square dimensions: 72 by 72 pixels.
- One byte per pixel.
- Between 1 and 220 palette entries.
- GBA BGR555 colors stored as little-endian 16-bit values.
- Absolute pixel indices in the range 20 through 239.
- CRC-32 protection for the palette and pixel payload.

There is no transparency or animation in version 2. Version 1 was an
unreleased 72-by-104 portrait prototype; version 2 deliberately rejects those
files so they can never be drawn with the wrong geometry.

## Main-menu palette allocation

The main menu uses one 256-entry background palette. The allocation for cover
support is:

| Indices | Owner |
| --- | --- |
| 0 | Background/transparent base |
| 1-15 | SuperFW logo |
| 16-19 | Active UI theme |
| 20-239 | Selected-game cover |
| 240-244 | In-game-menu theme handoff |
| 245-255 | Reserved |

Cover pixels store their final absolute palette indices. This lets firmware
copy them directly into Mode 4 video memory without remapping every pixel.

## Binary header

All multi-byte integers are little-endian. The header is exactly 32 bytes.

| Offset | Size | Field | Version 2 value |
| ---: | ---: | --- | --- |
| 0 | 4 | Magic | ASCII `SFCV` |
| 4 | 1 | Version | `2` |
| 5 | 1 | Header size | `32` |
| 6 | 2 | Flags | `0` |
| 8 | 2 | Width | `72` |
| 10 | 2 | Height | `72` |
| 12 | 2 | Palette count | `1..220` |
| 14 | 1 | Palette base | `20` |
| 15 | 1 | Reserved | `0` |
| 16 | 4 | Palette byte length | `palette_count * 2` |
| 20 | 4 | Pixel byte length | `72 * 72` (`5184`) |
| 24 | 4 | Payload CRC-32 | CRC of palette bytes followed by pixel bytes |
| 28 | 4 | Reserved | `0` |

## Payload

The header is immediately followed by:

1. `palette_count` BGR555 colors, two bytes each.
2. Exactly 5,184 absolute palette indices, in row-major order.

BGR555 stores five red bits in bits 0-4, five green bits in bits 5-9, and five
blue bits in bits 10-14. Bit 15 must be zero.

Every pixel must be at least `palette_base` and less than
`palette_base + palette_count`. Trailing bytes are invalid.

The smallest valid file is 5,218 bytes. The largest valid version 2 file is
5,656 bytes.

## Lookup convention

The MVP matches the ROM basename without its extension. For example:

```text
/Games/Pokemon Emerald.gba
/.superfw/covers/Pokemon Emerald.sfcov
```

Filename matching follows the filesystem behavior already used by SuperFW.
Game-code lookup may be added in a later format-independent phase.

The firmware first checks the organized `/.superfw/covers/` directory. For
compatibility with SD implementations that fail to traverse that new nested
directory, it retries the same filename directly under `/.superfw/`.

## Validation requirements

A reader must reject a cover before drawing it if any of the following is true:

- Magic, version, header size, flags, or reserved fields are unsupported.
- Dimensions or palette base differ from the version 2 constants.
- Palette count or declared payload lengths are out of range.
- Actual file length differs from the exact declared length.
- A palette entry has bit 15 set.
- A pixel references a value outside the declared cover palette.
- Payload CRC-32 does not match.

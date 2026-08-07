# SuperR7 Cover Format v3 (76 by 76)

Version 3 is an optional, parallel cover path for the seven-row UI candidate.
It does not replace or reinterpret version 2 files.

## Compatibility

| Build/tool | Accepted format | Artwork size |
| --- | --- | --- |
| Existing SuperFW and `cover_converter.py` | Version 2 | 72 by 72 |
| `superfw-ui-v3.gba` and `cover_converter_v3.py` | Version 3 | 76 by 76 |

Both formats use the `.sfcov` extension, but their header version and fixed
dimensions differ. A version 2 build deliberately rejects version 3, and the
version 3 candidate deliberately rejects version 2. Keep converted output in a
separate directory when testing the candidate.

## Version 3 constants

- Header version: `3`
- Width: `76`
- Height: `76`
- Pixel payload: `5,776` bytes
- Palette entries: `1..220`
- Palette base: `20`
- Header size: `32` bytes
- Maximum file size: `6,248` bytes

All other palette, BGR555, CRC-32, lookup, and filename rules remain the same
as version 2.

## Conversion

Convert one image into a new, explicitly named file:

```text
python tools/cover_converter_v3.py convert cover.png game-v3.sfcov --preview game-v3.png
```

Convert a directory into a separate output tree:

```text
python tools/cover_converter_v3.py batch source-covers v3-covers --recursive
```

The v3 converter refuses to overwrite existing output unless `--overwrite` is
explicitly supplied. Do not point its batch output at the version 2 cover
directory during initial hardware testing.

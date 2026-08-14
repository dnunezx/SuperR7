# Legacy SuperFW cover converter (version 2)

> Historical compatibility tool. Current SuperR7 covers should use the
> [SuperR7 converter](../cover-converter.md).

The converter turns PNG, JPEG, WebP, or BMP artwork into version 2 `.sfcov`
files. It can also write a PNG preview using the exact 15-bit colors that the
GBA will display.

## Install

Python 3.10 or newer is recommended. From the repository root:

```powershell
py -m pip install -r tools\requirements-cover.txt
```

## Convert one cover

```powershell
py tools\cover_converter_v2.py convert `
  "Pokemon Emerald.png" `
  "Pokemon Emerald.sfcov" `
  --preview "Pokemon Emerald-preview.png"
```

The default `cover` resize mode fills the 72-by-72 square canvas using a centered
crop. To preserve the entire source image with letterboxing:

```powershell
py tools\cover_converter_v2.py convert source.png output.sfcov --mode contain
```

Transparent pixels and letterboxing use black by default. Supply any
Pillow-compatible color for a different background:

```powershell
py tools\cover_converter_v2.py convert source.png output.sfcov `
  --mode contain --background "#202040"
```

Existing files are never replaced unless `--overwrite` is supplied.

## Convert a directory

```powershell
py tools\cover_converter_v2.py batch `
  "C:\My Covers" `
  "D:\.superfw\covers" `
  --preview-dir "C:\My Cover Previews" `
  --recursive
```

Recursive conversion preserves subdirectories. Output names use the source
basename with the `.sfcov` extension. If two source files would produce the
same output name, the batch is rejected before any files are written.

## Inspect or preview an existing cover

```powershell
py tools\cover_converter_v2.py inspect "Pokemon Emerald.sfcov"
py tools\cover_converter_v2.py inspect "Pokemon Emerald.sfcov" `
  --preview decoded-preview.png
```

Inspection performs the same strict validation expected from the firmware,
including dimensions, payload lengths, palette indices, and CRC-32.

## Image choices

- `--mode cover` is recommended for normal portrait box art.
- `--mode contain` is useful for screenshots or unusually shaped artwork.
- `--dither floyd-steinberg` is the default and generally preserves gradients.
- `--dither none` produces cleaner flat-color illustrations and logos.

The converter does not download artwork. Users are responsible for sourcing
images they are permitted to use.

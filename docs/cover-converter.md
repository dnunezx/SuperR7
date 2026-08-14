# SuperR7 cover converter

The converter turns PNG, JPEG, WebP, or BMP artwork into the production
version 3 `.sfcov` format. Output is fixed at 76 by 76 pixels and uses the same
15-bit colors that the GBA displays.

## Install

Python 3.10 or newer is recommended. From the repository root:

```powershell
py -m pip install -r tools\requirements-cover.txt
```

## Convert one cover

```powershell
py tools\cover_converter.py convert `
  "Pokemon Emerald.png" `
  "Pokemon Emerald.sfcov" `
  --preview "Pokemon Emerald-preview.png"
```

The default `cover` resize mode fills the square canvas using a centered crop.
Use `--mode contain` to preserve the complete source image with letterboxing.
Existing output is never replaced unless `--overwrite` is supplied.

## Convert a directory

```powershell
py tools\cover_converter.py batch `
  "C:\My Covers" `
  "D:\.superfw\covers" `
  --preview-dir "C:\My Cover Previews" `
  --recursive
```

Recursive conversion preserves subdirectories. Output names use the source
basename with the `.sfcov` extension.

## Inspect or preview a cover

```powershell
py tools\cover_converter.py inspect "Pokemon Emerald.sfcov"
py tools\cover_converter.py inspect "Pokemon Emerald.sfcov" `
  --preview decoded-preview.png
```

Inspection validates dimensions, payload lengths, palette indices, and CRC-32.
The converter does not download artwork; users are responsible for sourcing
images they are permitted to use.

The superseded 72-by-72 version 2 converter remains available as
`tools/cover_converter_v2.py` for compatibility work only.

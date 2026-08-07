#!/usr/bin/env python3
# Copyright (C) 2026 Danny Nunez
"""Convert desktop artwork into version 3 76-by-76 SuperR7 covers."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from PIL import Image, ImageOps

try:
    from .cover_converter import (
        DITHER_MODES,
        RESAMPLE,
        add_image_options,
        iter_images,
    )
    from .sfcov_v3 import (
        Cover,
        CoverFormatError,
        HEIGHT,
        MAX_PALETTE_COLORS,
        PALETTE_BASE,
        VERSION,
        WIDTH,
        bgr555_to_rgb888,
        rgb888_to_bgr555,
    )
except ImportError:  # Direct execution: python tools/cover_converter_v3.py
    from cover_converter import (  # type: ignore
        DITHER_MODES,
        RESAMPLE,
        add_image_options,
        iter_images,
    )
    from sfcov_v3 import (  # type: ignore
        Cover,
        CoverFormatError,
        HEIGHT,
        MAX_PALETTE_COLORS,
        PALETTE_BASE,
        VERSION,
        WIDTH,
        bgr555_to_rgb888,
        rgb888_to_bgr555,
    )


def prepare_image(
    image: Image.Image,
    mode: str = "cover",
    background: tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    rgba = image.convert("RGBA")
    flattened = Image.new("RGBA", rgba.size, background + (255,))
    flattened.alpha_composite(rgba)
    rgb = flattened.convert("RGB")

    if mode == "cover":
        return ImageOps.fit(rgb, (WIDTH, HEIGHT), method=RESAMPLE)
    if mode == "contain":
        contained = ImageOps.contain(rgb, (WIDTH, HEIGHT), method=RESAMPLE)
        canvas = Image.new("RGB", (WIDTH, HEIGHT), background)
        offset = ((WIDTH - contained.width) // 2, (HEIGHT - contained.height) // 2)
        canvas.paste(contained, offset)
        return canvas
    raise ValueError(f"unsupported resize mode: {mode}")


def image_to_cover(
    image: Image.Image,
    *,
    mode: str = "cover",
    background: tuple[int, int, int] = (0, 0, 0),
    dither: str = "floyd-steinberg",
) -> Cover:
    if dither not in DITHER_MODES:
        raise ValueError(f"unsupported dither mode: {dither}")

    prepared = prepare_image(image, mode=mode, background=background)
    quantized = prepared.quantize(
        colors=MAX_PALETTE_COLORS,
        method=Image.Quantize.MEDIANCUT,
        dither=DITHER_MODES[dither],
    )
    source_palette = quantized.getpalette()
    source_pixels = quantized.tobytes()
    source_to_compact: dict[int, int] = {}
    color_to_compact: dict[int, int] = {}
    compact_palette: list[int] = []

    for source_index in sorted(set(source_pixels)):
        offset = source_index * 3
        red, green, blue = source_palette[offset : offset + 3]
        gba_color = rgb888_to_bgr555(red, green, blue)
        compact_index = color_to_compact.get(gba_color)
        if compact_index is None:
            compact_index = len(compact_palette)
            color_to_compact[gba_color] = compact_index
            compact_palette.append(gba_color)
        source_to_compact[source_index] = compact_index

    pixels = bytes(
        PALETTE_BASE + source_to_compact[source_index]
        for source_index in source_pixels
    )
    return Cover(tuple(compact_palette), pixels)


def cover_to_image(cover: Cover) -> Image.Image:
    cover.validate()
    palette: list[int] = []
    for color in cover.palette:
        palette.extend(bgr555_to_rgb888(color))
    palette.extend([0] * (768 - len(palette)))

    relative_pixels = bytes(pixel - PALETTE_BASE for pixel in cover.pixels)
    preview = Image.new("P", (WIDTH, HEIGHT))
    preview.putpalette(palette)
    preview.putdata(relative_pixels)
    return preview.convert("RGB")


def convert_file(
    source: str | Path,
    output: str | Path,
    *,
    preview: str | Path | None = None,
    mode: str = "cover",
    background: tuple[int, int, int] = (0, 0, 0),
    dither: str = "floyd-steinberg",
    overwrite: bool = False,
) -> Cover:
    source_path = Path(source)
    output_path = Path(output)
    preview_path = Path(preview) if preview is not None else None
    for destination in (output_path, preview_path):
        if destination is not None and destination.exists() and not overwrite:
            raise FileExistsError(f"output already exists: {destination}")

    with Image.open(source_path) as image:
        cover = image_to_cover(
            image, mode=mode, background=background, dither=dither
        )
    cover.write(output_path)
    if preview_path is not None:
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        cover_to_image(cover).save(preview_path, format="PNG")
    return cover


def batch_convert(
    input_dir: str | Path,
    output_dir: str | Path,
    *,
    preview_dir: str | Path | None = None,
    recursive: bool = False,
    mode: str = "cover",
    background: tuple[int, int, int] = (0, 0, 0),
    dither: str = "floyd-steinberg",
    overwrite: bool = False,
) -> list[Path]:
    source_root = Path(input_dir)
    output_root = Path(output_dir)
    preview_root = Path(preview_dir) if preview_dir is not None else None
    if not source_root.is_dir():
        raise NotADirectoryError(f"input directory does not exist: {source_root}")

    plans: list[tuple[Path, Path, Path | None]] = []
    seen: set[Path] = set()
    for source in iter_images(source_root, recursive):
        relative = source.relative_to(source_root)
        output = output_root / relative.with_suffix(".sfcov")
        if output in seen:
            raise FileExistsError(
                f"multiple input images map to the same cover: {output.name}"
            )
        seen.add(output)
        preview = (
            preview_root / relative.with_suffix(".png")
            if preview_root is not None
            else None
        )
        for destination in (output, preview):
            if destination is not None and destination.exists() and not overwrite:
                raise FileExistsError(f"output already exists: {destination}")
        plans.append((source, output, preview))

    outputs: list[Path] = []
    for source, output, preview in plans:
        convert_file(
            source,
            output,
            preview=preview,
            mode=mode,
            background=background,
            dither=dither,
            overwrite=overwrite,
        )
        outputs.append(output)
    return outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert artwork to the SuperR7 v3 76x76 .sfcov format"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    convert = commands.add_parser("convert", help="convert one image")
    convert.add_argument("input", type=Path)
    convert.add_argument("output", type=Path)
    convert.add_argument("--preview", type=Path)
    add_image_options(convert)

    batch = commands.add_parser("batch", help="convert a directory")
    batch.add_argument("input_dir", type=Path)
    batch.add_argument("output_dir", type=Path)
    batch.add_argument("--preview-dir", type=Path)
    batch.add_argument("--recursive", action="store_true")
    add_image_options(batch)

    inspect = commands.add_parser("inspect", help="validate a v3 cover")
    inspect.add_argument("input", type=Path)
    inspect.add_argument("--preview", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "convert":
            cover = convert_file(
                args.input,
                args.output,
                preview=args.preview,
                mode=args.mode,
                background=args.background,
                dither=args.dither,
                overwrite=args.overwrite,
            )
            print(
                f"wrote {args.output} ({WIDTH}x{HEIGHT}, "
                f"{len(cover.palette)} colors, {len(cover.to_bytes())} bytes)"
            )
        elif args.command == "batch":
            outputs = batch_convert(
                args.input_dir,
                args.output_dir,
                preview_dir=args.preview_dir,
                recursive=args.recursive,
                mode=args.mode,
                background=args.background,
                dither=args.dither,
                overwrite=args.overwrite,
            )
            print(f"converted {len(outputs)} image(s) into {args.output_dir}")
        else:
            cover = Cover.read(args.input)
            if args.preview is not None:
                args.preview.parent.mkdir(parents=True, exist_ok=True)
                cover_to_image(cover).save(args.preview, format="PNG")
            print(
                f"{args.input}: version {VERSION}, {WIDTH}x{HEIGHT}, "
                f"{len(cover.palette)} colors, {len(cover.pixels)} pixels"
            )
    except (CoverFormatError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

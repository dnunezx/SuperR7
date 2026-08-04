#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2024 David Guillen Fandos <david@davidgf.net>
# Fixes GBA header and patches checksums and other relevant header fields

import sys, hashlib, struct

header_only = len(sys.argv) == 3 and sys.argv[1] == "--header-only"
if len(sys.argv) != (3 if header_only else 2):
  raise SystemExit(f"usage: {sys.argv[0]} [--header-only] <gba image>")

image_path = sys.argv[2] if header_only else sys.argv[1]
fwimg = open(image_path, "rb").read()

# Pad the firmware to the next 512 byte block
fwimg += b'\xff' * (512 - (len(fwimg) % 512))

# Patch GBA fwimg with a fixed checksum
crc = sum(fwimg[0xA0:0xBD])
fwimg = fwimg[:0xBD] + ((-(0x19 + crc)) & 0xFF).to_bytes(1, "little") + fwimg[0xBE:]

if not header_only:
  # Insert firmware size into the fwimg as well (so we can properly check checksum)
  fwimg = fwimg[:0xCC] + struct.pack("<I", len(fwimg)) + fwimg[0xD0:]

  # Clear the checksum before calculating it
  fwimg = fwimg[:0xE0] + (b'\x00' * 16) + fwimg[0xF0:]
  fwimg = fwimg[:0xE0] + hashlib.sha256(fwimg).digest()[:16] + fwimg[0xF0:]

open(image_path, "r+b").write(fwimg)


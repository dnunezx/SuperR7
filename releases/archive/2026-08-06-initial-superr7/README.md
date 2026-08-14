# Historical initial SuperR7 build

This is the first branded SuperR7 firmware built from source checkpoint
`3deb361`. It passed physical SuperCard SD validation on August 6, 2026 and is
the accepted branded baseline after the exact pre-branding Phase 5 ROM.

- File: `superr7-initial-branded.gba`
- GBA title: `SUPERR7`
- Embedded Build ID: `3deb361a`
- Main binary: 214,232 bytes
- Compressed main payload: 104,768 bytes
- Final image: 518,144 bytes
- Free space below 512 KiB: 6,144 bytes
- EWRAM: 220,752 of 257,024 bytes
- IWRAM: 11,176 of 32,768 bytes
- SHA-256:
  `72FCA4B89E329B9D2A4E21D5E4BB6C083E997A214C2BB0AE8373FCC0367AF61B`

Verification completed:

- All four Phase 4/5 native mGBA visual assertion suites.
- All 23 cover-converter and UI Python checks.
- Host theme test.
- Normal-firmware compatibility build and legacy-guard symbol check.
- Physical SuperCard SD chain-load validation.

The exact pre-branding hardware-passed image remains under
`../2026-08-06-phase5-baseline/` as a rollback artifact.

SuperR7 development and maintenance: Danny Nunez (dnunezx).
Upstream foundation: SuperFW by David Guillen Fandos (`davidgf`).

# SuperR7 Phase 5 hardware baseline

This directory freezes the exact cleaned Phase 5 candidate that passed
physical SuperCard SD chain-load validation on August 6, 2026. SuperR7 adopts
this image and its corresponding source state as the independent fork's
functional baseline.

- File: `SuperR7-phase5-hardware-baseline.gba`
- Size: 520,192 bytes
- Free space below 512 KiB: 4,096 bytes
- SHA-256:
  `15A88B4F0F25B057ED4B93B4B0D855E7F3CFE67C0E7D0B7ADBA01261A6667A92`
- Hardware result: chain-loaded successfully; Phase 5 launch, loading, dock,
  themes, settings, cover art, navigation, and normal operation accepted.

The binary still contains inherited SuperFW compatibility identifiers because
it is the exact pre-branding image that was tested. Do not replace this file
when later SuperR7 branding or features change the build hash.

SuperR7-specific development and recognition: Danny Nunez.
Upstream foundation: SuperFW by David Guillen Fandos (`davidgf`).

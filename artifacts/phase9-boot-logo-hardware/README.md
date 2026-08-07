# SuperR7 Phase 9 Gothic boot-logo hardware candidate

This folder contains the exact image prepared for physical SuperCard SD
chain-load validation after the monochrome Gothic boot-splash integration.

- File: `superr7-phase9-gothic-boot-1eec14f.gba`
- Source checkpoint: `1eec14f`
- Embedded build ID: `1eec14fd`
- SHA-256: `93F774D81C6DEF17125587A66B121A8CF126D87256F7F547389ACD482F49A1E5`
- Boot-logo mask: 72 by 22 pixels, 1bpp, rendered at 2x scale
- Bootloader: 2,968 / 3,072 bytes (104 bytes free)
- First-stage loader: 428 / 1,024 bytes
- In-game payload: 49,512 bytes
- Main binary: 214,236 bytes
- Compressed main payload: 104,786 bytes
- Final ROM: 518,144 bytes
- Free firmware space: 6,144 bytes
- EWRAM: 220,756 / 257,024 bytes
- IWRAM: 11,176 / 32,768 bytes

`superr7-boot-logo-mgba.png` is the native 240-by-160 framebuffer captured
from this exact candidate in headless mGBA. The capture contains only the
expected black background, white wordmark, and four grayscale bar stages.

All Phase 4/5 visual suites, the in-game visual suite, all 23 Python checks,
and the normal-firmware compatibility link passed before packaging. Chain-load
this image and verify the boot splash on physical hardware before flashing it
internally.

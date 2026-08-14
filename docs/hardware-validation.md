# SuperR7 hardware validation

This record identifies the exact firmware images that passed physical
SuperCard SD testing. SHA-256 is the authority when similarly named local
files exist.

Generated images and test captures live in the ignored local `artifacts/`
workspace. Public downloads belong on versioned GitHub Releases, not in the
source tree.

## Accepted lineage

| Date | State | Local image | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| 2026-08-14 | Current: fixed-page library navigation | `superr7-page-navigation-hardware-test.gba` | 520,192 | `DCD599CD17745FB350A7176C24257377AB9B301E6C5B661B25594E3D53E5C940` |
| 2026-08-13 | Rollback: Tech Frame wallpaper | `superr7.gba` | 520,192 | `63EE181F90C0FCACB0014D6F819B6994C26E2677A589C9DCC355718C9F1FAA4F` |
| 2026-08-12 | Rollback: stacked boot logo | `superr7-boot-logo-v2.gba` | 519,168 | `6DCDEA075A8CF04C8A4FF523F20628D5FF74AFF7126E3234F59A7B9E93A26BFC` |
| 2026-08-11 | Rollback: Launch Back footer | `superr7-phase13-launch-back-8ca8aaf2.gba` | 519,168 | `8CA8AAF27941BAE9A1DF35D3C3E88C863CEF51B4AA5C35F1F25D780F0C808A2F` |
| 2026-08-10 | Rollback: persistent Favorites | `superr7-phase11-favorites-cbdae08b.gba` | 520,704 | `CBDAE08B529566E37517776CA336B1FF070AEF4296ED09503E961577972C68B3` |
| 2026-08-07 | Historical: Gothic boot logo | `superr7-phase9-gothic-boot-1eec14f.gba` | 518,144 | `93F774D81C6DEF17125587A66B121A8CF126D87256F7F547389ACD482F49A1E5` |
| 2026-08-06 | Historical: initial SuperR7 branding | `superr7-initial-branded.gba` | 518,144 | `72FCA4B89E329B9D2A4E21D5E4BB6C083E997A214C2BB0AE8373FCC0367AF61B` |
| 2026-08-06 | Historical: pre-branding Phase 5 baseline | `superr7-phase5-baseline.gba` | 520,192 | `15A88B4F0F25B057ED4B93B4B0D855E7F3CFE67C0E7D0B7ADBA01261A6667A92` |

The August 14 image changes Browse, Recent, and Favorites to fixed seven-item
pages. Left and Right select the first item of the previous or next page,
boundary page inputs do nothing, and the final page may be partial. The exact
image above was chain-loaded and confirmed working on physical SuperCard SD
hardware.

The three oldest historical packages remain tracked under
[`releases/archive`](../releases/README.md). New public binaries should be
attached to GitHub Releases instead of committed to this repository.

## Release gates

Before publishing a firmware image:

1. Build `superr7.gba` from the intended clean source tag.
2. Confirm the final image remains below the 512 KiB limit.
3. Run the host and native mGBA regression suites.
4. Chain-load that exact image on physical SuperCard SD hardware.
5. Record its byte size and SHA-256 here.
6. Publish it as `superr7-vX.Y.Z.gba` with the matching source tag.

Internal phase names may remain in development history, but public downloads
use normal semantic release versions.

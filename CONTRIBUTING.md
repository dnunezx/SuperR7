# Contributing to SuperR7

SuperR7 is an independent GPL-3.0-or-later project maintained by Danny Nunez.

## Attribution policy

- Preserve every existing upstream and third-party copyright or license notice.
- Do not replace an upstream author's copyright when modifying their file.
- Add `Copyright (C) <year> Danny Nunez` to new SuperR7 source files and to
  upstream files that receive substantial SuperR7-specific changes.
- Use `Danny Nunez` as the Git author name for Danny's work. The repository's
  configured noreply email may continue to be used.
- Credit additional contributors by their requested name and preserve their
  Git authorship.
- Keep compatibility identifiers such as `/.superfw/` and inherited firmware
  signatures documented; they are not statements of current project ownership.

## Change gates

SuperR7 targets the SuperCard SD first. Firmware changes must remain below the
512 KiB image limit, pass host and mGBA regression checks, and be chain-loaded
on hardware before any internal-flash recommendation.

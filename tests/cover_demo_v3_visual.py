# Copyright (C) 2026 Danny Nunez (dnunezx)

from __future__ import annotations

from pathlib import Path
import os

import cover_demo_visual as visual


visual.SCREENSHOT_DIR = Path(
    os.environ.get("COVER_DEMO_V3_SCREENSHOTS", "artifacts/cover-demo-v3")
)
visual.PANEL_BOX = (1, 30, 83, 112)
visual.PANEL_IMAGE = (4, 33, 80, 109)


if __name__ == "__main__":
    visual.main()

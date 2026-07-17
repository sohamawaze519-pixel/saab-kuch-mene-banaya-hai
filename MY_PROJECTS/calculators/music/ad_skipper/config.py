"""Runtime configuration for the ad skipper."""

import os

# How often to scan for skip buttons (seconds).
POLL_INTERVAL = float(os.environ.get("YT_SKIP_POLL_INTERVAL", "0.75"))

# Minimum seconds between clicks on the same window (avoids double-clicks).
CLICK_COOLDOWN = float(os.environ.get("YT_SKIP_CLICK_COOLDOWN", "2.0"))

# Window title substrings that identify YouTube Music (case-insensitive).
YT_MUSIC_TITLE_KEYWORDS = (
    "youtube music",
    "music.youtube.com",
)

# Button / control names that indicate a skippable ad (regex, case-insensitive).
SKIP_BUTTON_PATTERNS = (
    r"skip\s*ad",
    r"skip\s*ads",
)

# Fraction of window width/height used for visual OCR fallback (bottom-right).
VISUAL_SCAN_WIDTH_RATIO = 0.45
VISUAL_SCAN_HEIGHT_RATIO = 0.35

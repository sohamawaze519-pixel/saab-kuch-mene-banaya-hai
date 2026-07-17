"""
YouTube Music background ad skipper.

Runs silently in the background, watches for YouTube Music in a browser tab
or the YouTube Music desktop app, and clicks "Skip ad" when it becomes available.

Usage:
    pip install -r requirements.txt
    python app.py

Optional: install Tesseract OCR for better detection in browsers where UI
Automation cannot see the player (https://github.com/tesseract-ocr/tesseract).
"""

from __future__ import annotations

import logging
import sys

from ad_skipper.service import run_service


def _configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def main() -> None:
    _configure_logging()
    logging.getLogger("PIL").setLevel(logging.WARNING)
    run_service()


if __name__ == "__main__":
    main()

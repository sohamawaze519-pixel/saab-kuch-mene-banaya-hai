"""Mouse automation to click skip-ad targets."""

from __future__ import annotations

import logging
import time

import pyautogui

from .detector import SkipTarget

logger = logging.getLogger(__name__)

# Fail-safe: moving mouse to a screen corner aborts pyautogui (disabled for background use).
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05


def click_skip(target: SkipTarget) -> None:
    """Move the cursor to the skip button and click."""
    logger.info(
        "Clicking skip ad at (%s, %s) via %s",
        target.x,
        target.y,
        target.method,
    )
    pyautogui.moveTo(target.x, target.y, duration=0.08)
    time.sleep(0.03)
    pyautogui.click()

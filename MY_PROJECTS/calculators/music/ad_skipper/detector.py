"""Detect skippable ad controls in YouTube Music windows."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import uiautomation as auto
from PIL import ImageGrab

from .config import (
    SKIP_BUTTON_PATTERNS,
    VISUAL_SCAN_HEIGHT_RATIO,
    VISUAL_SCAN_WIDTH_RATIO,
)
from .window_finder import MusicWindow, compile_skip_pattern

logger = logging.getLogger(__name__)

_SKIP_REGEXES = [compile_skip_pattern(p) for p in SKIP_BUTTON_PATTERNS]

# Lazy import: pytesseract needs the Tesseract binary installed separately.
_tesseract = None


def _get_tesseract():
    global _tesseract
    if _tesseract is None:
        try:
            import pytesseract

            pytesseract.get_tesseract_version()
            _tesseract = pytesseract
        except Exception:
            _tesseract = False
    return _tesseract if _tesseract is not False else None


@dataclass(frozen=True)
class SkipTarget:
    x: int
    y: int
    method: str


def _name_matches_skip(name: str) -> bool:
    if not name:
        return False
    return any(regex.search(name) for regex in _SKIP_REGEXES)


def _control_center(control: auto.Control) -> tuple[int, int] | None:
    try:
        rect = control.BoundingRectangle
        if rect.width() <= 0 or rect.height() <= 0:
            return None
        return rect.xcenter(), rect.ycenter()
    except Exception:
        return None


def _walk_for_skip(root: auto.Control, depth: int = 0, max_depth: int = 30) -> SkipTarget | None:
    if depth > max_depth:
        return None

    try:
        name = root.Name or ""
    except Exception:
        return None

    if _name_matches_skip(name):
        center = _control_center(root)
        if center:
            return SkipTarget(x=center[0], y=center[1], method="uia")

    try:
        children = root.GetChildren()
    except Exception:
        children = []

    for child in children:
        found = _walk_for_skip(child, depth + 1, max_depth)
        if found:
            return found

    return None


def _find_via_uia(window: MusicWindow) -> SkipTarget | None:
    try:
        root = auto.ControlFromHandle(window.hwnd)
        if root is None:
            return None
        return _walk_for_skip(root)
    except Exception as exc:
        logger.debug("UI Automation scan failed for %r: %s", window.title, exc)
        return None


def _visual_scan_region(window: MusicWindow) -> tuple[int, int, int, int]:
    scan_w = int(window.width * VISUAL_SCAN_WIDTH_RATIO)
    scan_h = int(window.height * VISUAL_SCAN_HEIGHT_RATIO)
    left = window.left + window.width - scan_w
    top = window.top + window.height - scan_h
    return left, top, left + scan_w, top + scan_h


def _find_via_ocr(window: MusicWindow) -> SkipTarget | None:
    tesseract = _get_tesseract()
    if tesseract is None:
        return None

    region = _visual_scan_region(window)
    try:
        image = ImageGrab.grab(bbox=region)
        data = tesseract.image_to_data(image, output_type=tesseract.Output.DICT)
    except Exception as exc:
        logger.debug("OCR scan failed for %r: %s", window.title, exc)
        return None

    skip_pattern = re.compile(r"skip", re.IGNORECASE)
    n = len(data["text"])
    for i in range(n):
        text = (data["text"][i] or "").strip()
        if not text or not skip_pattern.search(text):
            continue
        conf = int(float(data["conf"][i])) if data["conf"][i] != "-1" else 0
        if conf < 40:
            continue
        x = region[0] + data["left"][i] + data["width"][i] // 2
        y = region[1] + data["top"][i] + data["height"][i] // 2
        return SkipTarget(x=x, y=y, method="ocr")

    return None


def find_skip_target(window: MusicWindow) -> SkipTarget | None:
    """Return screen coordinates of a skip-ad control, if present."""
    target = _find_via_uia(window)
    if target:
        return target
    return _find_via_ocr(window)

"""Locate YouTube Music windows on Windows."""

from __future__ import annotations

import ctypes
import re
from dataclasses import dataclass

import win32gui

from .config import YT_MUSIC_TITLE_KEYWORDS


def enable_dpi_awareness() -> None:
    """Ensure window coordinates match physical pixels on scaled displays."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


@dataclass(frozen=True)
class MusicWindow:
    hwnd: int
    title: str
    left: int
    top: int
    width: int
    height: int

    @property
    def rect(self) -> tuple[int, int, int, int]:
        return self.left, self.top, self.left + self.width, self.top + self.height


def _is_youtube_music_title(title: str) -> bool:
    lowered = title.lower()
    return any(keyword in lowered for keyword in YT_MUSIC_TITLE_KEYWORDS)


def _get_window_rect(hwnd: int) -> tuple[int, int, int, int] | None:
    if not win32gui.IsWindowVisible(hwnd):
        return None
    if win32gui.IsIconic(hwnd):
        return None
    try:
        return win32gui.GetWindowRect(hwnd)
    except win32gui.error:
        return None


def find_youtube_music_windows() -> list[MusicWindow]:
    """Return all visible, non-minimized YouTube Music windows."""
    matches: list[MusicWindow] = []

    def callback(hwnd: int, _: object) -> None:
        title = win32gui.GetWindowText(hwnd)
        if not title or not _is_youtube_music_title(title):
            return
        rect = _get_window_rect(hwnd)
        if rect is None:
            return
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top
        if width < 200 or height < 200:
            return
        matches.append(
            MusicWindow(
                hwnd=hwnd,
                title=title,
                left=left,
                top=top,
                width=width,
                height=height,
            )
        )

    win32gui.EnumWindows(callback, None)
    return matches


def compile_skip_pattern(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)

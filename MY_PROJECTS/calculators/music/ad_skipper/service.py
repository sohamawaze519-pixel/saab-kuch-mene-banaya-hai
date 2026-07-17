"""Background service loop for skipping YouTube Music ads."""

from __future__ import annotations

import logging
import signal
import time
from typing import Callable

from .clicker import click_skip
from .config import CLICK_COOLDOWN, POLL_INTERVAL
from .detector import find_skip_target
from .window_finder import MusicWindow, enable_dpi_awareness, find_youtube_music_windows

logger = logging.getLogger(__name__)


class AdSkipperService:
    def __init__(
        self,
        poll_interval: float = POLL_INTERVAL,
        click_cooldown: float = CLICK_COOLDOWN,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.poll_interval = poll_interval
        self.click_cooldown = click_cooldown
        self._sleep = sleep_fn
        self._running = False
        self._last_click_by_hwnd: dict[int, float] = {}

    def stop(self) -> None:
        self._running = False

    def _can_click(self, hwnd: int) -> bool:
        last = self._last_click_by_hwnd.get(hwnd, 0.0)
        return (time.monotonic() - last) >= self.click_cooldown

    def _record_click(self, hwnd: int) -> None:
        self._last_click_by_hwnd[hwnd] = time.monotonic()

    def _process_window(self, window: MusicWindow) -> None:
        if not self._can_click(window.hwnd):
            return

        target = find_skip_target(window)
        if target is None:
            return

        click_skip(target)
        self._record_click(window.hwnd)

    def run(self) -> None:
        enable_dpi_awareness()
        self._running = True
        logger.info(
            "YouTube Music ad skipper started (poll=%.2fs, cooldown=%.2fs)",
            self.poll_interval,
            self.click_cooldown,
        )

        while self._running:
            windows = find_youtube_music_windows()
            if windows:
                for window in windows:
                    if not self._running:
                        break
                    try:
                        self._process_window(window)
                    except Exception:
                        logger.exception(
                            "Error while processing window %r", window.title
                        )

            self._sleep(self.poll_interval)

        logger.info("YouTube Music ad skipper stopped")


def run_service() -> None:
    service = AdSkipperService()

    def _handle_stop(_signum: int, _frame: object) -> None:
        logger.info("Shutdown signal received")
        service.stop()

    signal.signal(signal.SIGINT, _handle_stop)
    signal.signal(signal.SIGTERM, _handle_stop)

    service.run()

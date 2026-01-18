from __future__ import annotations

import atexit
import curses
from typing import Optional

_WINDOW: Optional[curses.window] = None
_INITIALIZED = False


def get_window(provided: Optional[curses.window] = None) -> curses.window:
    """Return the shared curses window, initializing if needed."""
    global _WINDOW, _INITIALIZED

    if provided is not None:
        _WINDOW = provided
    if _WINDOW is None:
        _WINDOW = curses.initscr()
    if not _INITIALIZED:
        curses.noecho()
        curses.cbreak()
        _WINDOW.keypad(True)
        _WINDOW.nodelay(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        _INITIALIZED = True
        atexit.register(shutdown)
    return _WINDOW


def shutdown() -> None:
    """Restore terminal state and end curses session."""
    global _WINDOW, _INITIALIZED

    if _WINDOW is not None:
        try:
            _WINDOW.keypad(False)
        except curses.error:
            pass
    if _INITIALIZED:
        try:
            curses.echo()
            curses.nocbreak()
        except curses.error:
            pass
    try:
        curses.endwin()
    except curses.error:
        pass
    _WINDOW = None
    _INITIALIZED = False

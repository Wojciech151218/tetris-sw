from __future__ import annotations

import curses
from typing import Optional

from action import Action
from input import Input
from curses_session import get_window


class ConsoleInput(Input):
    """Non-blocking controller that reads key presses via curses."""

    _BINDINGS = {
        ord("q"): Action.ROTATE_LEFT,
        ord("w"): Action.ROTATE_RIGHT,
        ord("a"): Action.MOVE_LEFT,
        ord("d"): Action.MOVE_RIGHT,
        ord("s"): Action.DROP,
        curses.KEY_UP: Action.ROTATE_LEFT,
        curses.KEY_DOWN: Action.DROP,
        curses.KEY_LEFT: Action.MOVE_LEFT,
        curses.KEY_RIGHT: Action.MOVE_RIGHT,
    }

    def __init__(self, window: Optional[curses.window] = None):
        self._window = get_window(window)

    def get_action(self) -> Optional[Action]:
        keypress = self._window.getch()
        if keypress == -1:
            return None
        return self._BINDINGS.get(keypress)


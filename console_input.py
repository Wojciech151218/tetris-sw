from __future__ import annotations

from typing import Optional

from blessed import Terminal
from blessed.keyboard import Keystroke

from action import Action
from input import Input


class ConsoleInput(Input):
    """Non-blocking controller that reads key presses via blessed."""

    _BINDINGS = {
        "q" : Action.ROTATE_LEFT,
        "w" : Action.ROTATE_RIGHT,
        "a" : Action.MOVE_LEFT,
        "d" : Action.MOVE_RIGHT,
        "s" : Action.DROP,

        "KEY_UP": Action.ROTATE_LEFT,
        "ctrl": Action.ROTATE_LEFT,
        "KEY_DOWN": Action.DROP,
        "KEY_LEFT": Action.MOVE_LEFT,
        "KEY_RIGHT": Action.MOVE_RIGHT,
    }

    def __init__(self, term: Optional[Terminal] = None):
        self._term = term or Terminal()

    def _normalize_key(self, keypress: Keystroke) -> Optional[str]:
        if not keypress:
            return None
        if keypress.is_sequence and keypress.name:
            return keypress.name
        text = str(keypress).strip().lower()
        return text or None

    def get_action(self) -> Optional[Action]:
        with self._term.cbreak():
            keypress = self._term.inkey(timeout=0)
        command = self._normalize_key(keypress)
        if not command:
            return None
        return self._BINDINGS.get(command)


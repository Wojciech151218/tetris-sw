import sys
import termios
import tty
import select
import logging
from typing import Optional

from action import Action
from input import Input

logging.basicConfig(level=logging.INFO, format='[ConsoleInputLight] %(message)s')

class ConsoleInputLight(Input):
    """Lightweight non-blocking console input for Debian embedded systems."""

    _BINDINGS = {
        "q": Action.ROTATE_LEFT,
        "w": Action.ROTATE_RIGHT,
        "a": Action.MOVE_LEFT,
        "d": Action.MOVE_RIGHT,
        "s": Action.DROP,
        "UP": Action.ROTATE_LEFT,
        "DOWN": Action.DROP,
        "LEFT": Action.MOVE_LEFT,
        "RIGHT": Action.MOVE_RIGHT,
    }

    def __init__(self):
        self._fd = sys.stdin.fileno()
        self._old_term = termios.tcgetattr(self._fd)
        self._buffer = ""

    def _read_key(self) -> Optional[str]:
        # Non-blocking read
        dr, _, _ = select.select([sys.stdin], [], [], 0.1)
        if not dr:
            return None

        # Read all available bytes
        while True:
            ch = sys.stdin.read(1)
            if not ch:
                break
            self._buffer += ch
            # Arrow keys start with \x1b[
            if self._buffer.startswith("\x1b[") and len(self._buffer) < 3:
                continue  # wait for full sequence
            break

        # Handle arrow keys
        if self._buffer.startswith("\x1b[") and len(self._buffer) >= 3:
            seq = self._buffer[1:]  # remove leading \x1b
            self._buffer = ""
            return {
                "[A": "UP",
                "[B": "DOWN",
                "[C": "RIGHT",
                "[D": "LEFT",
            }.get(seq)

        key = self._buffer
        self._buffer = ""
        return key.lower()

    def get_action(self) -> Optional[Action]:
        tty.setcbreak(self._fd)
        try:
            key = self._read_key()
        finally:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_term)

        if not key:
            return None

        action = self._BINDINGS.get(key)
        if action:
            logging.info(f"Action chosen: {action}")
        return action

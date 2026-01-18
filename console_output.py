from __future__ import annotations

import curses
from typing import Optional

from game import Game
from output import Output
from square import Color, Square
from curses_session import get_window

RENDER_COUNTER_FOR_BLINKING = 10

class ConsoleOutput(Output):
    """Terminal renderer that draws colored blocks using curses."""

    EMPTY_CELL = "  "

    def __init__(
        self,
        window: Optional[curses.window] = None,
    ):
        self._window = get_window(window)
        self._color_styles = self._build_color_styles()
        self._render_counter = 0

    def _build_color_styles(self) -> dict[Color, int]:
        if curses.has_colors():
            curses.start_color()
        color_pairs = {
            Color.RED: curses.COLOR_RED,
            Color.GREEN: curses.COLOR_GREEN,
            Color.BLUE: curses.COLOR_BLUE,
            Color.YELLOW: curses.COLOR_YELLOW,
            Color.PURPLE: curses.COLOR_MAGENTA,
            Color.ORANGE: curses.COLOR_YELLOW,
            Color.PINK: curses.COLOR_MAGENTA,
            Color.BROWN: curses.COLOR_YELLOW,
            Color.GRAY: curses.COLOR_WHITE,
            Color.BLACK: curses.COLOR_BLACK,
            Color.WHITE: curses.COLOR_WHITE,
        }
        styles: dict[Color, int] = {}
        for index, (color, background) in enumerate(color_pairs.items(), start=1):
            try:
                curses.init_pair(index, curses.COLOR_BLACK, background)
            except curses.error:
                continue
            styles[color] = curses.color_pair(index)
        return styles

    def _safe_addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        try:
            self._window.addstr(y, x, text, attr)
        except curses.error:
            pass

    def _get_cell_attr(self, square: Optional[Square], should_blink_white: bool) -> int:
        if square is None or square.color is None:
            return 0
        color_to_use = Color.WHITE if should_blink_white else square.color
        return self._color_styles.get(color_to_use, 0)

    def render(self, game: Game) -> None:
        lines_to_clear = game.get_lines_to_clear()
        should_blink_white = (
            len(lines_to_clear) > 0
            and (self._render_counter // RENDER_COUNTER_FOR_BLINKING) % 2 == 0
        )

        grid: list[list[Optional[Square]]] = [
            [None for _ in range(game.width)] for _ in range(game.height)
        ]
        for square in game.get_all_squares():
            if square is None:
                continue
            if not (0 <= square.x < game.width and 0 <= square.y < game.height):
                continue
            grid[square.y][square.x] = square

        # Increment render counter for blinking effect
        self._render_counter += 1

        self._window.erase()
        horizontal_border = "+" + "-" * (game.width * 2) + "+"
        self._safe_addstr(0, 0, horizontal_border)
        for row_idx, row in enumerate(grid):
            y = row_idx + 1
            self._safe_addstr(y, 0, "|")
            for col_idx, square in enumerate(row):
                x = 1 + col_idx * 2
                blink = row_idx in lines_to_clear and should_blink_white
                attr = self._get_cell_attr(square, blink)
                self._safe_addstr(y, x, self.EMPTY_CELL, attr)
            self._safe_addstr(y, 1 + game.width * 2, "|")
        self._safe_addstr(game.height + 1, 0, horizontal_border)
        self._safe_addstr(
            game.height + 3,
            0,
            "Controls: q=rotate left w=rotate right a=move left d=move right s=drop",
        )
        self._window.refresh()


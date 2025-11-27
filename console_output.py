from __future__ import annotations

import sys
from typing import Optional

from blessed import Terminal

from game import Game
from output import Output
from square import Color, Square

RENDER_COUNTER_FOR_BLINKING = 10

class ConsoleOutput(Output):
    """Terminal renderer that draws colored blocks using blessed."""

    EMPTY_CELL = "  "

    def __init__(
        self,
        term: Optional[Terminal] = None,
        output_stream=None,
    ):
        self._term = term or Terminal()
        self._output = output_stream or sys.stdout
        self._color_styles = self._build_color_styles()
        self._render_counter = 0

    def _build_color_styles(self) -> dict[Color, str]:
        term = self._term
        return {
            Color.RED: term.on_red,
            Color.GREEN: term.on_green,
            Color.BLUE: term.on_blue,
            Color.YELLOW: term.on_yellow,
            Color.PURPLE: term.on_magenta,
            Color.ORANGE: term.on_color(208),
            Color.PINK: term.on_color(205),
            Color.BROWN: term.on_color(94),
            Color.GRAY: term.on_color(245),
            Color.BLACK: term.on_black,
            Color.WHITE: term.on_white,
        }

    def _square_to_cell(self, square: Optional[Square], should_blink_white: bool = False) -> str:
        if square is None or square.color is None:
            return self.EMPTY_CELL
        # If blinking is active, use white color
        color_to_use = Color.WHITE if should_blink_white else square.color
        color_code = self._color_styles.get(color_to_use)
        if not color_code:
            return self.EMPTY_CELL
        return f"{color_code}  {self._term.normal}"

    def _build_board(self, game: Game) -> list[str]:

        lines_to_clear = game.get_lines_to_clear()
        
        # Determine if we should blink white (every 5 render calls)
        should_blink_white = len(lines_to_clear) > 0 and (self._render_counter // RENDER_COUNTER_FOR_BLINKING) % 2 == 0

        
        grid: list[list[Optional[Square]]] = [
            [None for _ in range(game.width)] for _ in range(game.height)
        ]
        for square in game.get_all_squares():
            if square is None:
                continue
            if not (0 <= square.x < game.width and 0 <= square.y < game.height):
                continue
            grid[square.y][square.x] = square

        horizontal_border = "+" + "-" * (game.width * 2) + "+"
        lines = [horizontal_border]
        for row_idx, row in enumerate(grid):
            # Check if this row is in lines_to_clear
            is_clearing_line = row_idx in lines_to_clear
            line = "|" + "".join(
                self._square_to_cell(square, should_blink_white=is_clearing_line and should_blink_white) 
                for square in row
            ) + "|"
            lines.append(line)
        lines.append(horizontal_border)
        return lines

    def render(self, game: Game) -> None:
        board_lines = self._build_board(game)
        
        # Increment render counter for blinking effect
        self._render_counter += 1
        
        with self._term.hidden_cursor():
            self._output.write(self._term.home + self._term.clear)
            self._output.write("\n".join(board_lines))
            self._output.write(
                "\nControls: q=rotate left w=rotate right a=move left d=move right s=drop\n"
            )
            self._output.flush()


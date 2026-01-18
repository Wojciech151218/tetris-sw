from __future__ import annotations

from typing import Optional

from game import Game
from output import Output
from square import Square
from websocket_input import get_shared_server


class WebSocketOutput(Output):
    """Output implementation that sends game state over websockets."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self._server = get_shared_server(host=host, port=port)

    def _serialize_square(self, square: Optional[Square]) -> Optional[dict]:
        if square is None or square.color is None:
            return None
        return {
            "x": square.x,
            "y": square.y,
            "color": square.get_color().value,
        }

    def render(self, game: Game) -> None:
        squares = []
        for square in game.get_all_squares():
            payload = self._serialize_square(square)
            if payload is not None:
                squares.append(payload)

        message = {
            "type": "state",
            "width": game.width,
            "height": game.height,
            "squares": squares,
        }
        self._server.send_state(message)

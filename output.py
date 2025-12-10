from __future__ import annotations

from abc import ABC, abstractmethod

from game import Game


class Output(ABC):
    """Base renderer for a game tick."""

    @abstractmethod
    def render(self, game: Game) -> None:
        raise NotImplementedError

class CombinedOutput(Output):
    def __init__(self, outputs: list[Output]):
        self.outputs = outputs

    def render(self, game: Game) -> None:
        for output in self.outputs:
            output.render(game)
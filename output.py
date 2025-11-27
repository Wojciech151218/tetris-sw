from __future__ import annotations

from abc import ABC, abstractmethod

from game import Game


class Output(ABC):
    """Base renderer for a game tick."""

    @abstractmethod
    def render(self, game: Game) -> None:
        raise NotImplementedError
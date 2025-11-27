from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from action import Action


class Input(ABC):
    """Base interface for anything that can provide player actions."""

    @abstractmethod
    def get_action(self) -> Optional[Action]:
        """Return the user action for the current tick or None if idle."""
        raise NotImplementedError
from __future__ import annotations

from typing import Protocol
from onitama.domain.models import GameState, Move


class UIHandler(Protocol):

    def show_state(self, state: GameState) -> None:
        raise NotImplementedError()

    def choose_move(self, state: GameState) -> Move:
        raise NotImplementedError()
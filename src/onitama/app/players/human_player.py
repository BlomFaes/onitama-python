from dataclasses import dataclass
from typing import Callable

from onitama.domain.models import GameState, Move
from .protocol import PlayerController

@dataclass
class HumanPlayer(PlayerController):
    chooser: Callable[[GameState], Move]

    def select_move(self, state: GameState) -> Move:
        return self.chooser(state)
from typing import Protocol
from onitama.domain.models import GameState, Move

class PlayerController(Protocol):
    def select_move(self, state: GameState) -> Move:
        raise NotImplementedError()
import random
from dataclasses import dataclass

from onitama.domain.models import GameState, Move
from onitama.domain.rules import generate_legal_moves
from .protocol import PlayerController

@dataclass
class RandomPlayer(PlayerController):
    seed: int | None = None

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def select_move(self, state: GameState) -> Move:
        moves = generate_legal_moves(state)
        if not moves:
            raise RuntimeError("No legal moves")
        return self._rng.choice(moves)
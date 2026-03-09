from dataclasses import dataclass

from onitama.domain.models import GameState, Move, Player
from onitama.domain.rules import generate_legal_moves
from .protocol import PlayerController

@dataclass
class MinimaxPlayer(PlayerController):
    player: Player
    depth: int = 2

    def select_move(self, state: GameState) -> Move:
        from onitama.app.minimax import minimax_alpha_beta

        result = minimax_alpha_beta(
            state=state,
            depth=self.depth,
            alpha=-10**9,
            beta=10**9,
            perspective=self.player,
        )

        if result.best_move is None:
            # Should not happen unless no legal moves or game already ended
            moves = generate_legal_moves(state)
            if not moves:
                raise RuntimeError("No legal moves for MinimaxPlayer")
            return moves[0]

        return result.best_move
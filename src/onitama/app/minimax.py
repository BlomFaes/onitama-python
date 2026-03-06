from __future__ import annotations

from dataclasses import dataclass

from onitama.domain.models import GameState, PieceKind, Player, Move
from onitama.domain.rules import apply_move, generate_legal_moves, winner

@dataclass(frozen=True)
class SearchResult:
    score: int
    best_move: Move | None


def evaluate(state: GameState, perspective: Player) -> int:
    w = winner(state)
    if w is perspective:
        return 1_000_000
    if w is perspective.other():
        return -1_000_000

    score = 0
    for piece in state.board.values():
        value = 100 if piece.kind is PieceKind.MASTER else 1
        score += value if piece.owner is perspective else -value

    my_master_sq = None
    opp_master_sq = None
    for sq, piece in state.board.items():
        if piece.kind is PieceKind.MASTER:
            if piece.owner is perspective:
                my_master_sq = sq
            else:
                opp_master_sq = sq

    # Precompute opponent moves (from opponent-to-move viewpoint)
    threat_state = GameState(
        board=state.board,
        to_move=perspective.other(),
        hand=state.hand,
        neutral=state.neutral,
    )
    opp_moves = generate_legal_moves(threat_state)

    # Opponent can capture my 'master' next move? (very bad)
    if my_master_sq is not None and any(mv.to_sq == my_master_sq for mv in opp_moves):
        score -= 5_000

    # Can I capture the opponent's 'master' next move? (very good)
    my_turn_state = GameState(
        board=state.board,
        to_move=perspective,
        hand=state.hand,
        neutral=state.neutral,
    )
    my_moves = generate_legal_moves(my_turn_state)
    if opp_master_sq is not None and any(mv.to_sq == opp_master_sq for mv in my_moves):
        score += 5_000

    # Hanging students: if opponent can capture my student immediately, small penalty
    my_student_squares = {
        sq
        for sq, piece in state.board.items()
        if piece.owner is perspective and piece.kind is not PieceKind.MASTER
    }
    capturable_students = sum(1 for mv in opp_moves if mv.to_sq in my_student_squares)
    score -= 2 * capturable_students

    # Temple progress (keep small)
    enemy_temple = (0, 2) if perspective is Player.RED else (4, 2)
    if my_master_sq is not None:
        r, c = my_master_sq
        tr, tc = enemy_temple
        distance = abs(r - tr) + abs(c - tc)
        score += max(0, 4 - distance)

    return score

def minimax_alpha_beta(
    state: GameState,
    depth: int,
    alpha: int,
    beta: int,
    perspective: Player,
) -> SearchResult:

    w = winner(state)
    if w is not None or depth == 0:
        return SearchResult(score=evaluate(state, perspective), best_move=None)

    legal_moves = generate_legal_moves(state)
    if not legal_moves:
        return SearchResult(score=evaluate(state, perspective), best_move=None)

    maximizing = state.to_move is perspective

    best_move = None
    if maximizing:
        best_score = -10 ** 9
        for mv in legal_moves:
            child = apply_move(state, mv)
            result = minimax_alpha_beta(child, depth - 1, alpha, beta, perspective)
            if result.score > best_score:
                best_score = result.score
                best_move = mv
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # prune
        return SearchResult(score=best_score, best_move=best_move)

    best_score = 10 ** 9
    for mv in legal_moves:
        child = apply_move(state, mv)
        result = minimax_alpha_beta(child, depth - 1, alpha, beta, perspective)
        if result.score < best_score:
            best_score = result.score
            best_move = mv
        beta = min(beta, best_score)
        if beta <= alpha:
            break  # prune
    return SearchResult(score=best_score, best_move=best_move)



from __future__ import annotations

from onitama.domain.models import Card, GameState, Move, Player, Square, PieceKind

BOARD_SIZE = 5

def in_bounds(sq: Square) -> bool:
    # Returns true if the desired square is in bounds
    r, c = sq
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def oriented_offsets(card: Card, player: Player):
    # If the player is red, return the offsets in the direction of the card, otherwise rotate the card 180 degrees
    for dr, dc in card.offsets:
        if player is Player.RED:
            yield dr, dc
        else:
            yield -dr, -dc


def generate_legal_moves(state: GameState)-> list[Move]:
    moves: list[Move] = []
    cards = state.hand[state.to_move]

    for (r, c), piece in state.board.items():
        # If the piece is not owned by the current player, skip it
        if piece.owner is not state.to_move:
            continue

        for card in cards:
            for dr, dc in oriented_offsets(card, state.to_move):
                to_sq = (r + dr, c + dc)

                # If the move is out of bounds, skip it
                if not in_bounds(to_sq):
                    continue

                target = state.board.get(to_sq)
                # If the target square is owned by the current player, skip it
                if target is not None and target.owner is state.to_move:
                    continue

                moves.append(Move(from_sq=(r, c), to_sq=to_sq, card_name=card.name))

    return moves

def apply_move(state: GameState, move: Move) -> GameState:
    legal = generate_legal_moves(state)
    if move not in legal:
        raise ValueError("Illegal move")

    moving_piece = state.board[move.from_sq]

    # Move and capture
    new_board = dict(state.board)
    new_board.pop(move.from_sq)
    new_board[move.to_sq] = moving_piece

    # Swap cards
    c1, c2 = state.hand[state.to_move]
    if c1.name == move.card_name:
        used_card, other_card = c1, c2
    else:
        used_card, other_card = c2, c1

    new_hand = dict(state.hand)
    new_hand[state.to_move] = (state.neutral, other_card)

    return GameState(
        board=new_board,
        to_move=state.to_move.other(),
        hand=new_hand,
        neutral=used_card,
    )

def winner(state: GameState) -> Player | None:

    red_temple = (4,2)
    blue_temple = (0,2)

    red_master_sq: Square | None = None
    blue_master_sq: Square | None = None

    for sq, piece in state.board.items():
        if getattr(piece, "kind", None) is None:
            continue

        if piece.kind is PieceKind.MASTER:
            if piece.owner is Player.RED:
                red_master_sq = sq
            else: blue_master_sq = sq

    # Capture victory
    if red_master_sq is None:
        return Player.BLUE
    if blue_master_sq is None:
        return Player.RED

    # Temple victory
    if red_master_sq == blue_temple:
        return Player.RED
    if blue_master_sq == red_temple:
        return Player.BLUE

    return None


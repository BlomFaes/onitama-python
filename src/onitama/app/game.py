from __future__ import annotations

from onitama.app.players.protocol import PlayerController
from onitama.domain.models import Card, GameState, Piece, PieceKind, Player
from onitama.domain.rules import apply_move, winner

def initial_state(cards_for_game: list[Card]) -> GameState:
    if len(cards_for_game) != 5:
        raise ValueError("Need exactly 5 cards (2 red, 2 blue, 1 neutral).")

    red_cards = (cards_for_game[0], cards_for_game[1])
    blue_cards = (cards_for_game[2], cards_for_game[3])
    neutral = cards_for_game[4]

    board: dict[tuple[int, int], Piece] = {
        # RED (row 4)
        (4, 0): Piece(Player.RED, PieceKind.STUDENT),
        (4, 1): Piece(Player.RED, PieceKind.STUDENT),
        (4, 2): Piece(Player.RED, PieceKind.MASTER),
        (4, 3): Piece(Player.RED, PieceKind.STUDENT),
        (4, 4): Piece(Player.RED, PieceKind.STUDENT),
        # BLUE (row 0)
        (0, 0): Piece(Player.BLUE, PieceKind.STUDENT),
        (0, 1): Piece(Player.BLUE, PieceKind.STUDENT),
        (0, 2): Piece(Player.BLUE, PieceKind.MASTER),
        (0, 3): Piece(Player.BLUE, PieceKind.STUDENT),
        (0, 4): Piece(Player.BLUE, PieceKind.STUDENT),
    }

    return GameState(
        board=board,
        to_move=Player.RED,
        hand={Player.RED: red_cards, Player.BLUE: blue_cards},
        neutral=neutral,
    )

def play_game(
    state: GameState,
    red_controller: PlayerController,
    blue_controller: PlayerController,
    max_plies: int = 200,
) -> GameState:

    for _ in range(max_plies):
        w = winner(state)
        if w is not None:
            return state

        controller = red_controller if state.to_move is Player.RED else blue_controller
        move = controller.select_move(state)
        state = apply_move(state, move)

    return state
from __future__ import annotations

from onitama.domain.models import GameState, Move, PieceKind, Player
from onitama.domain.rules import generate_legal_moves

def _piece_char(state: GameState, r: int, c: int) -> str:
    p = state.board.get((r, c))
    if p is None:
        return "."
    if p.owner is Player.RED:
        return "R" if p.kind is PieceKind.MASTER else "r"
    return "B" if p.kind is PieceKind.MASTER else "b"

def render(state: GameState) -> str:
    blue_cards = " | ".join(c.name for c in state.hand[Player.BLUE])
    red_cards = " | ".join(c.name for c in state.hand[Player.RED])

    board_lines: list[str] = []
    for r in range(5):
        row_text = " ".join(_piece_char(state, r, c) for c in range(5))
        board_lines.append(f"{r}  {row_text}")

    left_header = "   0 1 2 3 4"

    # We'll place the neutral card text on the right side of the board,
    # roughly centered vertically.
    right_column = [""] * 5
    right_column[2] = f"NEUTRAL: {state.neutral.name}"

    lines = [
        f"To move: {state.to_move.value}",
        f"BLUE hand: {blue_cards}",
        "",
    ]

    for i in range(5):
        lines.append(f"{board_lines[i]}    {right_column[i]}")

    lines.append(left_header)
    lines.append("")
    lines.append(f"RED hand:  {red_cards}")

    return "\n".join(lines)

def choose_human_move(state: GameState) -> Move:
    legal = generate_legal_moves(state)

    print(render(state))
    print("")
    print("Choose a move by number:")

    for i, mv in enumerate(legal, start=1):
        moving_piece = state.board[mv.from_sq]
        piece_label = "MASTER" if moving_piece.kind is PieceKind.MASTER else "STUDENT"

        fr, fc = mv.from_sq
        tr, tc = mv.to_sq
        print(f"{i:2d}. {piece_label:7s} ({fr},{fc}) -> ({tr},{tc}) using {mv.card_name}")

    while True:
        raw = input("> ").strip()
        if not raw.isdigit():
            print("Please enter a number.")
            continue

        idx = int(raw)
        if 1 <= idx <= len(legal):
            return legal[idx - 1]

        print(f"Please enter a number between 1 and {len(legal)}.")

    raise AssertionError("Unreachable: loop should return a Move once input is valid.")
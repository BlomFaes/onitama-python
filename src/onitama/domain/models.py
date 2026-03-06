from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Tuple

Square = Tuple[int, int]

Offset = Tuple[int, int]

class Player(Enum):
    RED = "RED"
    BLUE = "BLUE"

    def other(self) -> "Player":
        return Player.BLUE if self == Player.RED else Player.RED

class PieceKind(Enum):
    STUDENT = "STUDENT"
    MASTER = "MASTER"

@dataclass(frozen=True)
class Piece:
    owner: Player
    kind: PieceKind

@dataclass(frozen=True)
class Card:
    name: str
    # Should be relative to the current player
    offsets: FrozenSet[Offset]

@dataclass(frozen=True)
class Move:
    from_sq: Square
    to_sq: Square
    card_name: str

@dataclass(frozen=True)
class GameState:
    # Only store the occupied squares, if they aren't in the dict, it's empty
    board: dict[Square, Piece]

    # The player whose turn it is
    to_move: Player

    # The cards in the hand of each player
    hand: dict[Player, Tuple[Card, Card]]

    # The 'fifth' card
    neutral: Card

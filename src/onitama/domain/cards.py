from __future__ import annotations

import random
from typing import Sequence

from onitama.domain.models import Card


def all_cards() -> list[Card]:

    return [
        Card("Tiger", frozenset({(-2, 0), (1, 0)})),
        Card("Dragon", frozenset({(-1, -2), (-1, 2), (1, -1), (1, 1)})),
        Card("Frog", frozenset({(0, -2), (-1, -1), (1, 1)})),
        Card("Rabbit", frozenset({(0, 2), (-1, 1), (1, -1)})),
        Card("Crab", frozenset({(0, -2), (0, 2), (-1, 0)})),
        Card("Elephant", frozenset({(0, -1), (0, 1), (-1, -1), (-1, 1)})),
        Card("Goose", frozenset({(0, -1), (0, 1), (-1, -1), (1, 1)})),
        Card("Rooster", frozenset({(0, -1), (0, 1), (-1, 1), (1, -1)})),
        Card("Monkey", frozenset({(-1, -1), (-1, 1), (1, -1), (1, 1)})),
        Card("Mantis", frozenset({(-1, -1), (-1, 1), (1, 0)})),
        Card("Horse", frozenset({(0, -1), (-1, 0), (1, 0)})),
        Card("Ox", frozenset({(0, 1), (-1, 0), (1, 0)})),
        Card("Crane", frozenset({(-1, 0), (1, -1), (1, 1)})),
        Card("Boar", frozenset({(0, -1), (0, 1), (-1, 0)})),
        Card("Eel", frozenset({(-1, -1), (1, -1), (0, 1)})),
        Card("Cobra", frozenset({(-1, 1), (1, 1), (0, -1)})),
    ]


def deal_five(seed: int | None = None, cards: Sequence[Card] | None = None) -> list[Card]:

    pool = list(cards) if cards is not None else all_cards()
    if len(pool) < 5:
        raise ValueError("Need at least 5 cards to deal a game.")

    rng = random.Random(seed)
    return rng.sample(pool, 5)


def setup_cards(*, red: tuple[str, str], blue: tuple[str, str], neutral: str) -> list[Card]:

    names = [red[0], red[1], blue[0], blue[1], neutral]
    return get_cards_by_names(names)


def get_cards_by_names(names: Sequence[str]) -> list[Card]:

    name_to_card = {c.name.lower(): c for c in all_cards()}

    chosen: list[Card] = []
    for name in names:
        key = name.strip().lower()
        if key not in name_to_card:
            valid = ", ".join(sorted(c.name for c in all_cards()))
            raise ValueError(f"Unknown card name '{name}'. Valid names: {valid}")
        chosen.append(name_to_card[key])

    if len(chosen) != 5:
        raise ValueError("You must provide exactly 5 card names.")

    # Ensure they are distinct (Onitama uses 5 different cards)
    if len({c.name for c in chosen}) != 5:
        raise ValueError("Card names must be distinct (no duplicates).")

    return chosen
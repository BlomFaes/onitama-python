from onitama.app.game import initial_state, play_game
from onitama.app.players import HumanPlayer, MinimaxPlayer
from onitama.domain.cards import deal_five, setup_cards
from onitama.domain.models import Player
from onitama.domain.rules import winner
from onitama.ui.cli import choose_human_move, render


def main() -> None:
    # Manual deal
    # cards_for_game = setup_cards(
    #     red=("Ox", "Goose"),
    #     blue=("Elephant", "Eel"),
    #     neutral="Horse",
    # )

    # Random deal
    cards_for_game = deal_five(seed=None)

    state = initial_state(cards_for_game)

    red = HumanPlayer(choose_human_move)
    blue = MinimaxPlayer(player=Player.BLUE, depth=1)

    final_state = play_game(state, red, blue, verbose=False)
    print(render(final_state))

    w = winner(final_state)
    print("Winner:", w.value if w else "None (max moves reached)")


if __name__ == "__main__":
    main()
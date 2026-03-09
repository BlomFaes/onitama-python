from onitama.app.game import initial_state, play_game
from onitama.app.players.human_player import HumanPlayer
from onitama.app.players.minimax_player import MinimaxPlayer
from onitama.app.players.random_player import RandomPlayer

from onitama.domain import cards
from onitama.domain.models import Player
from onitama.domain.rules import winner

from onitama.ui.protocol import UIHandler
from onitama.ui.cli import CliUI

def run_game() -> None:

    # UI selection:
    ui: UIHandler = CliUI()

    # Manual deal:
    # cards_for_game = cards.setup_cards(
    #     red=("Frog", "Eel"),
    #     blue=("Horse", "Rooster"),
    #     neutral="Tiger",
    # )

    # Random deal:
    cards_for_game = cards.deal_five(seed=None)

    #Starting state
    state = initial_state(cards_for_game)

    # Player selection:

    # Possibilities:
    # - Human:
        # red/blue = HumanPlayer(ui.choose_move)
    # - Minimax:
        # red/blue = MinimaxPlayer(player=Player.RED, depth=5)
    # - Random:
        # red/blue = RandomPlayer(seed=None)

    red = HumanPlayer(ui.choose_move)
    blue = MinimaxPlayer(player=Player.BLUE, depth=5)

    # Run the game
    final_state = play_game(state, red, blue)
    ui.show_state(final_state)

    # Check the winner
    w = winner(final_state)
    print("Winner:", w.value if w else "None (max moves reached)")
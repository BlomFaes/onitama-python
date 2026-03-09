# Onitama Python

A Python implementation of the board game Onitama.

## Overview

This project is a Python-based implementation of [Onitama](https://en.wikipedia.org/wiki/Onitama), a two-player abstract strategy board game. The game features a 5x5 board and unique card-based movement mechanics.

## Project Structure

```
onitama-python/
├── src/
│   ├── main.py                      # Entry point for the application
│   └── onitama/                     # Main game package
│       ├── app/
│       │   ├── game.py              # Game initialization and main loop
│       │   ├── minimax.py           # Minimax AI algorithm with alpha-beta pruning
│       │   ├── run_game.py          # Game execution and setup
│       │   └── players/
│       │       ├── protocol.py      # Player interface protocol
│       │       ├── human_player.py  # Human player implementation
│       │       ├── random_player.py # Random move player
│       │       └── minimax_player.py# Minimax-based AI player
│       ├── domain/
│       │   ├── models.py            # Core data models (GameState, Piece, Card, Move)
│       │   ├── rules.py             # Game rules and move generation
│       │   └── cards.py             # Card definitions and dealing
│       └── ui/
│           ├── protocol.py          # UI handler interface
│           └── cli.py               # Command-line interface
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/BlomFaes/onitama-python.git
cd onitama-python
```

2. Run the game:
```bash
python src/main.py
```

## Running the Game

Start a game where you (human player) control the Red pieces and face off against an AI opponent:

```bash
python src/main.py
```

The CLI will display:
- The 5x5 game board with all pieces
- Your available cards and the opponent's cards
- The neutral card in play
- Legal moves available for your current turn

### Board Notation

- `R` = Red Master
- `r` = Red Student
- `B` = Blue Master
- `b` = Blue Student
- `.` = Empty square

### How to Play

1. The game prompts you to choose a move by number
2. Each move shows the piece, its current position, target position, and the card used
3. After your move, the AI makes its move
4. Game ends when someone wins (see Win Conditions below)

## Game Features

### Core Game Mechanics

- **Card-Based Movement**: Players use martial arts cards to move their pieces on the board
- **Hand Management**: Each player holds 2 cards; after using a card, it goes to the neutral pile
- **Card Rotation**: The neutral card becomes available to the opponent next turn, creating dynamic strategy
- **Board State**: 5x5 grid with each player starting with 5 pieces (1 Master, 4 Students)

### Win Conditions

1. **Capture Victory**: Eliminate your opponent's Master piece
2. **Temple Victory**: Move your Master to the opponent's temple:
   - Red Master reaches square (0, 2) - Blue's temple
   - Blue Master reaches square (4, 2) - Red's temple

### AI Implementation

The AI uses **Minimax with Alpha-Beta Pruning** for efficient game tree search:

- **Evaluation Function**: Scores positions based on:
  - Material advantage (Master = 100 points, Student = 1 point)
  - Master safety (penalties for being capturable)
  - Capture opportunities
  - Temple proximity
  - Student protection

- **Search Depth**: Configurable (default: 5 plies)
- **Optimizations**: Alpha-beta pruning to reduce search space

## Customization

### Manual Card Selection

To play with specific cards, edit `src/onitama/app/run_game.py`:

```python
# Uncomment and modify:
cards_for_game = cards.setup_cards(
    red=("Frog", "Eel"),
    blue=("Horse", "Rooster"),
    neutral="Tiger",
)
```

### AI Difficulty

Adjust the AI search depth in `src/onitama/app/run_game.py`:

```python
blue = MinimaxPlayer(player=Player.BLUE, depth=5)  # Change depth value
```

- Lower depth = faster but weaker AI
- Higher depth = stronger but slower AI

## Architecture

### Domain Layer (`onitama/domain/`)

- **models.py**: Immutable data classes representing game state
- **rules.py**: Pure functions implementing game rules
- **cards.py**: Card definitions and game setup

### Application Layer (`onitama/app/`)

- **game.py**: Main game loop and initialization
- **minimax.py**: AI decision-making algorithm
- **players/**: Different player implementations (Human, AI, Random)

### UI Layer (`onitama/ui/`)

- **cli.py**: Command-line interface and board rendering
- **protocol.py**: Interface definition for UI handlers

### Design Principles

- **Separation of Concerns**: Domain logic independent from UI and AI
- **Immutability**: GameState is immutable, moves create new states
- **Protocol-Based Design**: Flexible player and UI implementations
- **Pure Functions**: Deterministic, testable rule implementations

## Development

### Contributing

Contributions are welcome! Feel free to:
- Submit pull requests for improvements
- Report issues or suggest features
- Enhance the AI evaluation function
- Add new UI implementations
- Improve documentation

## About Onitama

Onitama is an elegant two-player abstract strategy game published by Arcane Wonders. Players command warriors using martial arts cards, balancing hand management with spatial tactics. The game is known for its depth despite simple rules and quick playtime.

## Author

Created by BlomFaes

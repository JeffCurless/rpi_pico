# Tic-Tac-Toe

Tic-Tac-Toe game collection for Pico Display, with two AI difficulty levels and a battery monitor utility.

## Files

### tictactoe.py

Basic game with a random-move AI.

- **`Cell`** — a single board cell
- **`Board`** — renders the grid and detects the winner
- **`MoveAI`** — chooses a random empty cell

**Button mapping:**

| Button | Action |
|---|---|
| X | Cycle selection left |
| Y | Cycle selection right |
| A | Confirm selection |
| B | Continue / restart |

### tictactoe_ai.py

Same game with an unbeatable pattern-based AI.

- **`MoveAI`** has 23 base board patterns (expanded with rotations and mirrors) covering all strategic positions
- **Priority:** win > block opponent > pattern match > random fallback
- **RGB LED feedback:** blue = pattern matched, red = random move taken

## Parent

See [classroom/](../README.md) for other classroom projects.

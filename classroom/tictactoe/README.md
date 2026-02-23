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

### battery.py

Standalone battery voltage monitor for Pico Display 2.0.

- Reads ADC on Pin 29 to measure battery voltage
- Maps voltage to charge percentage: 2.8 V = 0%, 4.2 V = 100%
- Displays "Charging!" if Pin 24 reads high (USB power detected)

## Parent

See [classroom/](../README.md) for other classroom projects.

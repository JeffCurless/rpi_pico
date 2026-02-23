# Pac-Man

A Pac-Man clone for Pico Display. Written by Todd P and Andrew W.

## Files

### pacman.py

Full game implementation using `picographics` on `DISPLAY_PICO_DISPLAY`.

**Board:** 15×25 tile grid encoded as a 2D array:

| Tile value | Meaning |
|---|---|
| 0 | Open lane |
| 1 | Wall |
| 2 | Ghost-only passage |
| 3 | Forced turn |
| 4 | Choice turn |
| 5/6 | Forced turn (up) / ghost house exit |

**Tile size:** 9 px per tile, 4 px sprite radius.

**Classes:**

| Class | Description |
|---|---|
| `Pacman_brains` | Player position, speed, movement, wall collision, and drawing |
| `Ghost_brains` | Base ghost class — position, color, target cord tracking, movement |

**Ghost AI (5 characters total):**

| Index | Name | Color | Strategy |
|---|---|---|---|
| 0 | Pac-Man | Yellow | Player-controlled |
| 1 | Inky | Red | Chases Pac-Man directly |
| 2 | Blinky | Blue | Targets 2 tiles ahead of Pac-Man |
| 3 | Pinky | Pink | Pattern-based |
| 4 | Clyde | Orange | Pattern-based |

**Button mapping:**

| Button | Direction |
|---|---|
| A | Up |
| B | Down |
| X | Right |
| Y | Left |

**Features:** pellets, power pellets, high score tracking, home screen.

## Hardware

Requires Pico Display Pack (`picographics`, `DISPLAY_PICO_DISPLAY`, `pimoroni.Button`).

## Parent

See [classroom/](../README.md) for other classroom projects.

# microKarel

A Karel-the-robot programming environment running on Pico Display. Students write Karel programs in a simple text-based language; the interpreter displays Karel's world and animates each step.

## Files

Three files work together to parse and execute Karel programs:

### parser.py

**`Parser`** class reads a `.txt` Karel program file, strips comments, converts braces/parentheses into tokens, and returns a flat token list ready for `Program`.

### command.py

- **`CMD_*`** string constants — one for each Karel command and keyword
- **`Instruction`** class — a single AST node; supports iteration to walk nested blocks
- **`Program`** class — reads the token list from `Parser` and builds the instruction tree using a stack

### ukarel.py

- **`Karel`** — robot state (position, direction, ball count)
- **`Ball`** — ball placement on the grid
- **`World`** — PicoGraphics display engine and execution engine
  - `World.executeProgram()` walks the instruction tree and dispatches each command
  - `World.executeCommand()` handles movement, turning, ball operations, and control flow

### newCmd.txt

The Karel program that runs at startup. Edit this file to change what Karel does.

## Karel Language

```
function myFunc() {
    move()
    turnLeft()
}

for var in range(4) {
    move()
    dropBall()
}

while frontIsClear() {
    move()
}

if rightIsClear() {
    turnRight()
} else {
    turnLeft()
}
```

**Commands:** `move()`, `turnRight()`, `turnLeft()`, `dropBall()`, `takeBall()`

**Conditions:** `frontIsClear()`, `rightIsClear()`, `leftIsClear()`, `ballsPresent()`

## Debug Flags

Set `debugKarel = True` or `debugDraw = True` at the top of `ukarel.py` to enable print tracing.

## Parent

See [classroom/](../README.md) for other classroom projects.

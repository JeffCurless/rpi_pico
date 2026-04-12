# How to Design a Program: Building Tic-Tac-Toe

## The Assignment

> Write a Tic-Tac-Toe program.  The computer always goes first and plays as `X`.
> The computer must never lose — it may tie, but it will not lose.
> The player plays as `O` and enters a number 1–9 to choose a square,
> where 1 is the top-left and 9 is the bottom-right.

That is the whole assignment.  One sentence.  But it contains a lot of work inside
it — a board, two players, turn taking, move validation, win detection, and an AI.
The rest of this document walks through the process of turning that one sentence
into a working program.

---

## The Mantra

Before writing a single line of code, memorize this:

> **Make it work. Make it work right. Make it work fast.**

This is the order that matters.  It means:

1. **Make it work** — get *something* running, even if it is ugly or incomplete.
   A program that runs wrong is easier to fix than a program that does not run at all.

2. **Make it work right** — now that it runs, clean it up.  Handle the edge cases.
   Restructure the code so it is correct and easy to read.

3. **Make it work fast** — only after it is correct, think about performance.
   Sometimes the "right" version is already fast enough.  That is fine.
   Do not optimise code that does not exist yet.

The biggest mistake beginners make is trying to do all three at once.  You end up
with code that is neither working, right, nor fast.  Do them in order.

---

## Step 1: Understand the Problem Before You Write Any Code

Read the assignment again and ask yourself: **what are the things in this problem?**

A Tic-Tac-Toe game has:

- A **board** made up of **squares** (or cells)
- Each square can hold a **token** — `X`, `O`, or empty
- A **player** who picks a square each turn
- A **computer** that picks a square each turn
- A way to detect a **winner** (or a tie)
- A **game loop** that keeps going until the game ends

This gives us a natural structure.  Each "thing" in the problem usually becomes a
**class** in the code.  Each "action" usually becomes a **method**.

---

## Step 2: Start with What You Know — Build the Board

The board is the foundation of everything else.  Without a board, neither the
player nor the computer can do anything.  But what is a board?  In the case of tic-tac-toe, it is simply a collection of 9 separate squares.  Each square can contain the same thing, the only difference with each square is where that square is on the board.

### The Cell

A board is made of squares.  A square (called a `Cell`) needs to know:

- What number it is (so we can refer to it)
- Whether it has a token, and if so, which one

```python
class Cell:
    def __init__( self, cellNum: int ) -> None:
        self.cellNum = cellNum
        self.token   = emptyToken   # starts empty

    def setToken( self, token: str ) -> None:
        self.token = token

    def getToken( self ) -> str:
        return self.token

    def isEmpty( self ) -> bool:
        return self.token == emptyToken

    def getIndex( self ) -> int:
        return self.cellNum
```

Notice that `Cell` does not know anything about the board, the game rules, or the
AI.  It only knows about itself.  This is the **single responsibility** principle:
each class does one job.

### The Board

Now that we have a `Cell`, a `Board` is simply a collection of nine of them,
plus the knowledge of which combinations are winning lines.

```python
class Board:
    def __init__( self ) -> None:
        self.cells    = []
        self.winToken = emptyToken
        self.winMove  = []
        for i in range(9):
            self.cells.append( Cell(i) )
        self.winningMoves = [[0,1,2],[3,4,5],[6,7,8],   # rows
                             [0,3,6],[1,4,7],[2,5,8],   # columns
                             [0,4,8],[2,4,6]]           # diagonals
```

The board numbers its cells 0–8 internally.  The player sees positions 1–9, so
the conversion is simply `cellIndex = playerInput - 1`.

The winning move list encodes every possible way the game can be won.  Write it
down once here, and every other part of the program — win detection, AI — can
use it without having to repeat the logic.

---

## Step 3: Stub Out What You Cannot Write Yet

At this point we know what the program *needs* to do, but we may not know *how*
to do all of it.  That is fine.  **Stub it out.**

A stub is a placeholder function that has the right name and signature, but does
nothing yet (or returns a safe dummy value).  It lets you keep building the rest
of the program without getting stuck.

For example, before we know how the AI will work, we can stub out `computerMove`:

```python
def computerMove( self ) -> None:
    pass   # TODO: make the computer pick a square
```

And before we know how to detect a winner, stub out `checkForWinner`:

```python
def checkForWinner( self, token: str ) -> bool:
    return False   # TODO: check all winning lines
```

Now `main()` can call both of these, the program will run, and we can see the
game loop working — even though the computer does nothing and nobody ever wins.
That is the **Make it work** step.  It is running.  Now we can fill in the stubs
one at a time.

---

## Step 4: Fill In the Stubs — Make It Work Right

### Printing the Board

The first stub to fill in is `paint()`.  If we cannot see the board, we cannot
test anything else.  The board looks like this:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

Empty cells show their position number so the player always knows what to type.
Once a token is placed, the number is replaced by `X` or `O`.

```python
def paint( self ) -> None:
    b = self.getBoardAsList()
    display = []
    for i in range(9):
        if b[i] == emptyToken:
            display.append( str(i + 1) )
        else:
            display.append( b[i] )
    for i in (0, 3, 6):
        print( ' {} | {} | {}'.format(display[i], display[i+1], display[i+2]) )
        if i != 6:
            print('---+---+---')
    print()
```

Run the program now.  Does the board display?  Do the position numbers show up?
Fix any problems before moving on.

### Detecting a Winner

With the winning move list already stored on the board, checking for a winner is
straightforward: loop through every possible winning combination and see if all
three cells hold the same token.

```python
def checkForWinner( self, token: str ) -> bool:
    winner = False
    for move in self.winningMoves:
        if ((self.getCellToken( move[0] ) == token) and
            (self.getCellToken( move[1] ) == token)  and
            (self.getCellToken( move[2] ) == token)):
            self.winMove  = move
            self.winToken = token
            winner = True
    return winner
```

Notice we write one function and call it for *both* the player and the computer,
just passing in a different token.  This is the **Do not Repeat Yourself** (DRY)
principle.

### The Game Loop

With the board printing and win detection working, we can write the game loop in
`main()`.  At this stage the computer can still be a stub — it just picks a random
square.  That is fine.  The loop itself is the important thing to get right first.

```python
def main() -> None:
    while True:
        board.reset()
        move.computerMove()     # computer goes first
        board.paint()

        haveWinner = False
        while not haveWinner:
            # get player input
            pos = int( input( "Enter position (1-9): " ) )
            cellIndex = pos - 1
            board.setCellToken( cellIndex, playerToken )
            board.paint()

            if board.checkForWinner( playerToken ):
                board.displayWinner()
                haveWinner = True
            else:
                move.computerMove()
                board.paint()
                if board.checkForWinner( computerToken ):
                    board.displayWinner()
                    haveWinner = True
                elif not board.movesExist():
                    board.displayWinner()
                    haveWinner = True

        again = input( "Play again? (y/n): " ).strip().lower()
        if again != 'y':
            break
```

Run it now.  Play a full game.  Does the board update?  Does the game end when
someone wins?  Does the tie case work?

**Important:** We are not validating the player's input yet.  If the player enters
a taken square, the game breaks.  That is okay — we will fix it next, because the
core loop works.

### Input Validation

Now make it work *right*.  Wrap the input in a loop and check two things:

1. The number must be between 1 and 9.
2. The chosen cell must be empty.

```python
playerMoved = False
while not playerMoved:
    try:
        pos = int( input( "Enter position (1-9): " ) )
        if pos < 1 or pos > 9:
            print( "Please enter a number between 1 and 9." )
            continue
        cellIndex = pos - 1
        if not board.getCell( cellIndex ).isEmpty():
            print( "That position is already taken. Try again." )
            continue
        board.setCellToken( cellIndex, playerToken )
        board.paint()
        playerMoved = True
    except ValueError:
        print( "Invalid input. Please enter a number between 1 and 9." )
```

Run it again.  Try to enter invalid positions.  Try to enter a taken square.
Does it reject them gracefully?

---

## Step 5: The Hard Part — Building the AI

The requirement is that the computer must **never lose**.  A random move is not
good enough.  We need a strategy.

### The Priority Order

Think about how a human expert plays:

1. **If I can win right now, take that square.**
2. **If my opponent can win on their next move, block that square.**
3. **Otherwise, play a strategically strong square.**
4. **If nothing else applies, pick any empty square.**

This order is critical.  Winning always beats blocking.  Blocking always beats
strategy.  This becomes the structure of `computerMove()`:

```python
def computerMove( self ) -> None:
    cell = self.mustWinMove()
    if cell != -1:
        self.board.setCellToken( cell, computerToken )
    else:
        cell = self.mustBlockMove()
        if cell != -1:
            self.board.setCellToken( cell, computerToken )
        else:
            matchingPatterns = self.findMatchingPatterns()
            if len( matchingPatterns ):
                self.moveAccordingToPattern( matchingPatterns )
            else:
                self.randomMove( computerToken )
```

### Checking for an Immediate Win or Block

Both `mustWinMove()` and `mustBlockMove()` use the same trick: temporarily place
a token, check if it would be a win, then put the original token back.

```python
def couldWin( self, cellNum: int, token: str ) -> bool:
    old = self.getCellToken( cellNum )
    self.setCellToken( cellNum, token )
    winner = False
    for move in self.winningMoves:
        if ((self.getCellToken( move[0] ) == token) and
            (self.getCellToken( move[1] ) == token)  and
            (self.getCellToken( move[2] ) == token)):
            winner = True
    self.setCellToken( cellNum, old )   # always restore
    return winner
```

`mustWinMove()` calls this for the computer's own token.  `mustBlockMove()` calls
it for the player's token.  Same function, two different uses — DRY again.

### Strategic Patterns

For everything that is not an immediate win or block, the AI uses a pattern
matching system.  A pattern is a 9-element list describing what the board should
look like, using these symbols:

| Symbol | Meaning |
|--------|---------|
| `X`    | Our token must be here |
| `O`    | Opponent's token must be here |
| `b`    | Must be blank |
| `*`    | Must be blank — **and this is where we move** |
| `?`    | Anything (wildcard) |

For example, this pattern says: if the opponent is in the centre and we are in
the bottom-right, play in the bottom-centre to set up a future fork:

```
['?','?','?','?','O','X','?','?','*']
```

You do not need many base patterns because each one is automatically rotated 90°,
180°, 270°, and mirrored, producing up to 8 variants from a single entry.  This
keeps the list small and manageable.

```python
def makeAllPatterns( self ) -> None:
    for pattern in self.basePatterns:
        for i in range(4):
            if self.isUniquePattern( pattern ):
                self.patterns.append( pattern )
            m = self.mirrorPattern( pattern )
            if self.isUniquePattern( m ):
                self.patterns.append( m )
            pattern = self.rotatePattern( pattern )
```

---

## Step 6: Test Everything Together

At this point the program is complete.  Before calling it done, play it
deliberately trying to break it:

- Try every possible opening move.  Does the computer always respond sensibly?
- Try to win.  The computer should always block you.
- Let the computer win.  Do you see "You Lose!" and not a crash?
- Fill the board to a tie.  Does it say "It's a Tie!" and not a crash?
- Enter letters, symbols, numbers out of range.  Does input validation hold?

If any of these fail, go back and fix them.  A test you cannot run is not a test.

---

## Step 7: Make It Work Fast (If Needed)

The pattern matching loop scans all patterns against the board on every computer
turn.  For a 3×3 board this is fast enough that you will never notice.  The
**Make it work fast** step simply does not apply here — which is the most common
outcome.

If this were a 10×10 board with thousands of patterns, we might think about
caching or early exit.  But optimising code that is already fast enough is wasted
effort.  Move on.

---

## The Complete Structure at a Glance

```
ttt.py
│
├── Cell                         the smallest unit — one square
│   ├── __init__                 stores cellNum and token
│   ├── setToken / getToken      read and write the token
│   ├── isEmpty                  is this square available?
│   └── getIndex                 what number is this cell?
│
├── Board                        the 3×3 grid and game state
│   ├── __init__                 creates 9 Cells and the winning move list
│   ├── reset                    clears the board for a new game
│   ├── getCell / getCellToken   read access
│   ├── setCellToken             write access
│   ├── checkForWinner           did this token win?
│   ├── couldWin                 would placing here be a win? (used by AI)
│   ├── getEmptyCells            list of available positions
│   ├── movesExist               is the game still going?
│   ├── getBoardAsList           snapshot of all tokens
│   ├── paint                    print the board to the console
│   └── displayWinner            print the result message
│
├── MoveAI                       computer player
│   ├── __init__                 loads base patterns, expands them
│   ├── rotatePattern            90° clockwise rotation
│   ├── mirrorPattern            horizontal mirror
│   ├── makeAllPatterns          expands base patterns to all rotations/mirrors
│   ├── cellMatch                does one cell satisfy a pattern symbol?
│   ├── doesBoardMatchPattern    does the whole board match a pattern?
│   ├── findMatchingPatterns     which patterns match the current board?
│   ├── findMoveInPattern        find the '*' cell in a matched pattern
│   ├── mustWinMove              is there an immediate winning cell?
│   ├── mustBlockMove            is there a cell to block the player's win?
│   ├── randomMove               fallback: pick any empty cell
│   └── computerMove             orchestrates the priority order
│
└── main                         game loop: reset → computer → player → repeat
```

---

## Key Lessons

**Start with the data, not the logic.**
We built `Cell` before `Board`, and `Board` before `MoveAI`.  Each layer depended
only on the layer below it.  This made each piece easy to test on its own.

**Stub first, implement later.**
Writing a stub lets you keep moving forward without getting blocked.  A function
that returns `False` or does nothing is better than a function you cannot write
yet, because the rest of the program can still run.

**Follow the mantra.**
Make it work (game loop runs).  Make it work right (validation, AI).  Make it
work fast (in this case: already fast enough).  Doing them in order keeps you
from over-engineering things you have not built yet.

**Do not repeat yourself.**
`checkForWinner` and `couldWin` both check for a win using the same winning move
list.  `mustWinMove` and `mustBlockMove` both call `couldWin` — just with
different tokens.  One piece of logic, used in multiple places.

**Each class does one job.**
`Cell` knows about tokens.  `Board` knows about the grid and the rules.
`MoveAI` knows about strategy.  `main` knows about the game loop.  None of them
try to do each other's job.

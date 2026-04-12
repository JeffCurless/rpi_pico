
# How to Design a Program: Building Tic-Tac-Toe

## The Assignment

> Write a Tic-Tac-Toe program. The computer always goes first and plays as `X`.
> The computer must never lose — it may tie, but it will not lose.
> The player plays as `O` and enters a number 1–9 to choose a square,
> where 1 is the top-left and 9 is the bottom-right.

That is the whole assignment. One sentence. But it contains a lot of work inside it: a board, two players, turn taking, move validation, win detection, and an AI. The rest of this document walks through the process of turning that one sentence into a working program.

## The Mantra

Before writing a single line of code, memorize this:

> **Make it work. Make it work right. Make it work fast.**

This is the order that matters.

1. **Make it work** — get *something* running, even if it is ugly or incomplete. A program that runs wrong is easier to fix than a program that does not run at all.

2. **Make it work right** — now that it runs, clean it up. Handle the edge cases. Restructure the code so it is correct and easy to read.

3. **Make it work fast** — only after it is correct, think about performance. Sometimes the “right” version is already fast enough. That is fine. Do not optimize code that does not exist yet.

The biggest mistake beginners make is trying to do all three at once. You end up with code that is neither working, right, nor fast. Do them in order. 

## Step 1: Understand the Problem Before You Write Any Code

Before you start typing Python, stop and study the assignment carefully. This is where good programmers separate themselves from frustrated programmers.

A common beginner mistake is to read the assignment once, get excited, and immediately start coding. That usually leads to confusion, broken logic, and a program that has to be rewritten later. Instead, slow down and figure out exactly what problem you are being asked to solve.

Read the assignment again:

> Write a Tic-Tac-Toe program. The computer always goes first and plays as `X`.
> The computer must never lose — it may tie, but it will not lose.
> The player plays as `O` and enters a number 1–9 to choose a square,
> where 1 is the top-left and 9 is the bottom-right.

That short description contains several separate requirements. If you unpack them, the problem becomes much clearer.

### What does the program need to do?

Your program must:

* Create and display a Tic-Tac-Toe board
* Let the computer place `X`
* Let the human player place `O`
* Accept user input from `1` to `9`
* Translate that input into a board location
* Prevent illegal moves
* Detect wins
* Detect ties
* Keep taking turns until the game ends
* Make computer moves that are strong enough that the computer never loses

That is a lot more than “just make Tic-Tac-Toe.” When you break the assignment into a list like this, the work becomes manageable.

### What are the “things” in this problem?

When designing a program, look for the nouns in the assignment. Nouns usually point to objects or classes.

In this problem, the important things are:

* A board
* Squares or cells
* A token in each square
* A player
* A computer
* A move
* A winner
* A game

Now ask: which of these need to be represented in code?

A Tic-Tac-Toe game has:

* A **board** made up of **squares**
* Each square can hold either `X`, `O`, or nothing
* A **player** who chooses a move
* A **computer** who chooses a move
* A way to check whether someone has won
* A way to know whether moves are still available
* A **game loop** that keeps the program running until the round is over

This gives you the first rough design of the program.

### What are the “actions” in this problem?

Now look for the verbs in the assignment. Verbs often become methods or functions.

This program needs actions such as:

* display the board
* place a token
* check whether a square is empty
* check for a winner
* ask the player for input
* choose a move for the computer
* reset the board for a new game

This leads to an important design idea:

* **Things** become classes
* **Actions** become methods

### What information must the program remember?

Every program needs data. Before writing code, ask yourself: what must this program know at all times?

For Tic-Tac-Toe, the program must know:

* What is currently in each of the 9 squares
* Which token belongs to the computer
* Which token belongs to the player
* Which board positions form winning lines
* Whether the game is over
* Who won, if anyone

This is why the board is such an important starting point. Almost every part of the game depends on the current state of the board.

### What should the player see, and what should the program store internally?

The player is told to enter a number from **1 to 9**. That is the user-facing view of the board.

But inside the program, it is often easier to number positions **0 to 8**, because Python lists use zero-based indexing.

So right away, you have a design choice:

* The **player** sees positions `1–9`
* The **program** stores positions `0–8`

That means you will need a simple conversion:

```python
cellIndex = playerInput - 1
```

This may seem small, but catching it early prevents confusion later.

### What rules must always be true?

Good programmers also identify the rules that should never be violated.

In Tic-Tac-Toe:

* A move can only be made in an empty square
* A square can contain only one token
* The computer always moves first
* The computer is always `X`
* The player is always `O`
* The game stops when someone wins or the board is full

These rules tell you what your code must enforce.

### What are the hardest parts of this assignment?

Not every part of the problem is equally difficult.

Some parts are simple:

* Displaying the board
* Letting the player enter a number
* Storing `X` and `O`

Some parts are more complex:

* Detecting wins correctly
* Handling bad input
* Making sure the computer never loses

That last one is the hardest part of the assignment. It means the computer cannot just make random moves. It needs strategy.

### A natural class structure begins to appear

Once you have identified the parts of the problem, a class design usually starts to reveal itself.

#### `Cell`

Represents one square on the board. A `Cell` needs to know:

* its position number
* whether it is empty
* which token it holds

#### `Board`

Represents the full 3×3 playing area. A `Board` needs to know:

* all 9 cells
* which combinations count as wins
* how to print itself
* how to tell whether someone has won
* whether there are empty moves left

#### `MoveAI`

Represents the logic for the computer’s move selection. It needs to know:

* how to find a winning move
* how to block the player
* how to choose a strong move when no immediate win or block exists

#### `main()`

Controls the overall flow of the game. It should handle:

* starting a round
* alternating turns
* ending the game
* asking whether the user wants to play again

### Why this matters before coding

At this point, you have not written any real code yet, but you have already solved several important design problems:

* You know what data exists
* You know what actions are needed
* You know what classes probably make sense
* You know what the user sees
* You know what the program stores internally
* You know what rules must be enforced
* You know which part is the hardest

That means when you do start coding, you are no longer guessing. You are building a plan.

### A good habit: describe the program in plain English first

Before writing code, try explaining the program in plain language:

> “The game has a board made of 9 cells. Each cell can hold `X`, `O`, or be empty. The board knows all possible winning lines. The player chooses a square by entering 1–9. The computer chooses a square using strategy. After every move, the board checks for a winner or a tie. The game continues until it ends.”

If you can explain the program clearly in English, you are much more likely to write it clearly in Python.

### The big takeaway from Step 1

Do not begin with syntax. Begin with structure.

Ask:

* What are the parts of the problem?
* What information must be stored?
* What actions must happen?
* What rules must always stay true?
* Which class should be responsible for each job?

Once you can answer those questions, the code becomes much easier to write.

## Step 2: Start with What You Know — Build the Board

Once you understand the problem, the next step is to decide where to begin coding.

A lot of students make the mistake of starting with the “interesting” part, like the AI or the game loop. That usually creates problems because those pieces depend on something more basic: the board.

The board is the foundation of Tic-Tac-Toe.

Without a board:

* there is nowhere to place a move
* there is nothing to print
* there is nothing to check for wins
* the player has nothing to choose from
* the computer has nothing to analyze

So do not start with the hardest part. Start with the most fundamental part. That part is the board. 

### What is a board, really?

A Tic-Tac-Toe board is just:

* 9 separate squares
* arranged in a 3×3 layout
* where each square can hold one value

Each square can be:

* empty
* `X`
* `O`

That is the most basic truth of the whole game.

### Break the board into smaller objects

Instead of trying to make one giant `Board` class do everything immediately, it is cleaner to begin by asking:

**What is the smallest meaningful piece of a Tic-Tac-Toe board?**

The answer is a single square.

You may call it:

* `Square`
* `Cell`
* `Tile`

In this document, it is called a `Cell`.

So before building a `Board`, build a `Cell`.

### What does one cell need to know?

A `Cell` does not need to know everything about the game.

It does **not** need to know:

* whose turn it is
* how to detect a winner
* how the AI works
* what the entire board looks like

A `Cell` only needs to know about itself:

* which position it represents
* what token is currently inside it

That is all.

### A good first class: `Cell`

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

This is a very small class, but it is already useful.

A `Cell` can answer questions like:

* “What token do you hold?”
* “Are you empty?”
* “What position are you?”

### Why not just use a list of strings?

You *could* represent the board like this:

```python
board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
```

And for a quick solution, that may work.

But this document is teaching program design, not just how to throw together a fast script. Using a `Cell` class gives you a better structure because:

* each square becomes a real object
* each square can manage its own state
* the code becomes easier to read
* the design scales better if you later add features

### Now build the board from cells

Once `Cell` exists, the `Board` becomes much easier to design.

A `Board` is simply:

* a collection of 9 `Cell` objects
* plus some board-level information and behavior

A basic constructor for `Board` might look like this:

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

### Part 1: Create the list of cells

```python
self.cells = []
for i in range(9):
    self.cells.append( Cell(i) )
```

This creates 9 `Cell` objects numbered 0 through 8.

### Part 2: Store the winning combinations

```python
self.winningMoves = [[0,1,2],[3,4,5],[6,7,8],
                     [0,3,6],[1,4,7],[2,5,8],
                     [0,4,8],[2,4,6]]
```

This is one of the smartest design decisions in the whole program.

These eight combinations represent:

* 3 horizontal rows
* 3 vertical columns
* 2 diagonals

That is every possible way to win in Tic-Tac-Toe.

By storing them in one list, you make later code much simpler.

### Internal numbering vs player numbering

The board uses positions `0` through `8` internally because Python lists are zero-based.

But the player sees positions `1` through `9`.

#### Program view

```python
0 1 2
3 4 5
6 7 8
```

#### Player view

```python
1 2 3
4 5 6
7 8 9
```

So the conversion is:

```python
cellIndex = playerInput - 1
```

### What methods should the board eventually have?

A useful `Board` class will probably need methods like:

* `reset()`
* `getCell(index)`
* `getCellToken(index)`
* `setCellToken(index, token)`
* `movesExist()`
* `getEmptyCells()`
* `checkForWinner(token)`
* `paint()`

### Keep responsibilities separated

The board should focus on:

* storing the game state
* reporting the game state
* enforcing board-related rules

It should not also decide:

* what the player should type
* how the AI chooses moves
* whether the user wants to play again

### The big takeaway from Step 2

Do not start by writing the whole game. Start by building the structure the game depends on.

In Tic-Tac-Toe, that means:

* first define a `Cell`
* then build a `Board` out of 9 cells
* then store the winning combinations
* then add board behaviors like reading, writing, checking, and printing

## Step 3: Stub Out What You Cannot Write Yet

At this point, you understand the problem and you have started building the board. Now you reach a very normal moment in programming:

You know what the program needs to do, but you do not yet know how to write every part of it.

That is not a problem. That is expected.

When you know a function must exist, but you are not ready to fully implement it yet, you should **stub it out**. 

### What is a stub?

A stub is a placeholder.

It is a function or method that:

* has the correct name
* has the correct parameters
* returns a safe value, or does nothing yet

A stub is basically your way of saying:

> “I know this piece belongs here. I am not finished with it yet, but I want the rest of the program to keep moving.”

### Why stubs are useful

Suppose you are building Tic-Tac-Toe and you know the game loop will eventually need to do things like:

* ask the computer to move
* check whether someone has won
* display the winner

But maybe you are not ready to write the AI yet. And maybe your winner-checking logic is not done.

Should the entire rest of the program stop just because those parts are unfinished?

No.

You can still:

* build the game loop
* print the board
* accept player input
* test turn-taking
* verify that the program runs

### This is part of “Make it work”

Stubs are part of **Make it work**.

They let you create a program that runs, even if some pieces are incomplete.

### What kinds of things should be stubbed out?

Early candidates for stubs include:

* `computerMove()`
* `checkForWinner()`
* `displayWinner()`
* `movesExist()`
* `paint()`

### Example: stubbing out the computer’s move

```python
def computerMove( self ) -> None:
    pass   # TODO: make the computer pick a square
```

### Example: stubbing out winner detection

```python
def checkForWinner( self, token: str ) -> bool:
    return False   # TODO: check all winning lines
```

### Why a safe dummy return value matters

A good stub should not cause chaos.

If a method must return a value, return something safe and predictable.

For example:

* a function returning `bool` might return `False`
* a function returning a number might return `-1`
* a function that performs an action might simply use `pass`

### Think of stubs as building scaffolding

A good way to picture stubs is as scaffolding around a building. They are not the final structure, but they help you construct the real structure safely.

### The game loop can be built early because of stubs

Even with unfinished methods, you can begin sketching the shape of `main()`:

1. Reset the board
2. Let the computer go first
3. Print the board
4. Let the player move
5. Check for a winner
6. Let the computer move again
7. Repeat until the game ends

If the necessary methods already exist as stubs, you can start writing that flow immediately.

### A stub is not laziness

Stubbing is not avoiding work. It is organizing work.

### The important thing: use the correct interface

A stub should look like the final method as much as possible.

That means:

* use the real method name
* use the correct parameters
* use the correct return type
* place it in the correct class

### The big takeaway from Step 3

Do not let one unfinished problem stop the whole project.

When you know a method belongs in the design, but you are not ready to fully write it yet, stub it out.

## Step 4: Fill In the Stubs — Make It Work Right

By this point, the program has structure.

You understand the problem.
You have started building the board.
You have stubbed out methods that are not ready yet.

Now it is time to start replacing those stubs with real logic.

This is where the project begins to feel like a real program instead of just a design. 

### Why fill in the stubs in a careful order?

Not all stubs are equally important.

Some are foundational:

* printing the board
* checking for wins
* detecting whether moves remain

Others are more advanced:

* choosing intelligent computer moves
* handling pattern-based strategy

The smart order is:

1. Fill in the parts that help you **see** and **test** the program
2. Fill in the rules that make the game **correct**
3. Fill in the edge cases that make the game **safe**
4. Save the more advanced strategy work for after the basics are stable

## First, make the board visible

One of the earliest stubs you should replace is the function that displays the board.

If you cannot see the board, you cannot properly test anything else.

### What should the board look like?

At the start of the game, before any moves are made, the board should help the player understand the position numbers:

```text
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

After a token is placed, the number is replaced with `X` or `O`.

### A working `paint()` method

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

### Why this method is a good example of clean design

A good `paint()` method should be responsible for display, not for modifying game state.

## Next, make winner detection real

Without winner detection:

* the game might continue after a winning move
* the result might never be announced
* the AI cannot properly analyze threats
* ties cannot be identified correctly

### A working `checkForWinner()` method

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

This works for either player because the logic is identical; only the token changes.

## Now write the real game loop

Once the board can print and winner detection works, the program is ready for a real game loop.

### A working `main()` structure

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

## Now fix a major weakness: input validation

Without input validation, the program may crash or behave incorrectly if the player enters:

* a letter
* a symbol
* a number outside 1–9
* a square that is already taken

### A better player input loop

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

### The big takeaway from Step 4

Replace your stubs in a smart order:

* first make the program visible
* then make the rules correct
* then make the loop function properly
* then make the input safe

That is how you **Make it work right**.

## Step 5: The Hard Part — Building the AI

Up to this point, you have built the structure of the game.

Now you reach the most difficult requirement in the entire assignment:

> **The computer must never lose.**

That one sentence changes everything. A random move is not enough. The AI must play intelligently enough to prevent defeat. 

### Why this is the hardest part

The AI has to look at the current board and answer questions like:

* Can I win right now?
* Is the player about to win?
* Which move is safest?
* Which move sets up a future advantage?
* Which moves should I avoid because they give the player an opening?

This part requires strategy.

### A random move is not enough

A random move might:

* miss a winning opportunity
* fail to block the player
* waste a turn on a weak square
* allow a fork or trap
* lose the game even when a safe move existed

### Start with the most important design rule: priorities

A good computer player does not treat every move equally. Some are urgent. Some are merely good. Some are fallback options.

A strong priority order is:

1. **If I can win right now, take that square.**
2. **If my opponent can win on their next move, block that square.**
3. **Otherwise, play a strategically strong square.**
4. **If nothing else applies, pick any empty square.**

### Let the AI make decisions in stages

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

This is strong because it breaks a large problem into manageable subproblems.

## First priority: can the computer win immediately?

The easiest smart move to identify is an immediate winning move.

### A `couldWin()` helper method

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

This method lets the AI simulate a possible move, check the result, and then undo it.

### Use the same logic for both winning and blocking

If you call `couldWin()` with the computer’s token, it tells you whether the computer could win by moving there.

If you call it with the player’s token, it tells you whether the player could win by moving there.

That means the same logic supports both:

* `mustWinMove()`
* `mustBlockMove()`

## Third priority: use strategic patterns

When there is no immediate win and no immediate threat, the AI needs a way to make strong positional moves.

The document solves this with a pattern-matching system.

### What is a pattern?

A pattern is a 9-element list describing what the board should look like, using symbols such as:

| Symbol | Meaning                                   |
| ------ | ----------------------------------------- |
| `X`    | Our token must be here                    |
| `O`    | Opponent's token must be here             |
| `b`    | Must be blank                             |
| `*`    | Must be blank — and this is where we move |
| `?`    | Anything                                  |

For example:

```python
['?','?','?','?','O','X','?','?','*']
```

This represents a recognizable board situation and a recommended move.

### Expand patterns through symmetry

Tic-Tac-Toe is highly symmetrical.

A good pattern in one orientation often remains a good pattern when:

* rotated 90°
* rotated 180°
* rotated 270°
* mirrored

So one base pattern can generate several equivalent versions.

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

### The big takeaway from Step 5

Build the AI around a clear priority system:

1. win if possible
2. block if necessary
3. follow strong patterns
4. fall back to any legal move

This makes the hardest part of the project manageable.

## Step 6: Test Everything Together

At this point, the program is no longer just a set of classes and methods. You now have:

* a board
* player input
* win detection
* a game loop
* a computer opponent
* logic that is supposed to prevent the computer from losing

This is the stage where many students are tempted to say, “It seems fine.”

That is not testing. A program is not finished because it looks correct. It is finished only after you have tried to prove it wrong and failed. 

### Why system testing matters

Earlier steps focused on individual pieces:

* does the board store tokens correctly?
* does the winner check work?
* does the input loop reject bad values?
* does the AI block immediate wins?

Those are all important.

But a real program can still fail even when its individual parts seem correct, because bugs often appear in the way parts interact.

### Testing is not “trying it once”

A lot of beginners test like this:

* run the game once
* make a few moves
* nothing crashes
* declare victory

That is not enough.

Real testing means you deliberately try to break the program.

### Start by playing complete games

Play full games from start to finish.

Do not stop after two or three moves. Play until:

* the computer wins
* the player tries to win
* the game ends in a tie
* the replay prompt appears

### Test every opening move

Try every possible opening move the player can make and watch how the computer responds.

### Try to beat the computer on purpose

The assignment says the computer must never lose. So your job as tester is to try to make the computer lose.

Try to:

* create two in a row
* trick the computer into missing a block
* set up forks
* force it into a weak response

If you can beat the computer, the assignment is not complete.

### Test immediate win and block situations directly

Construct specific board states and ask:

* Does the computer take an immediate winning move?
* Does it block an immediate threat?

### Test tie situations carefully

A tie should happen only when:

* the board is full
* and neither player has won

Test true ties and full boards that also contain a winner.

### Test invalid input on purpose

Try:

* letters
* words
* symbols
* out-of-range numbers
* negative numbers
* a square that is already taken

Ask:

* Does the program crash?
* Does it explain the problem clearly?
* Does it ask again properly?
* Does the board stay unchanged after invalid input?

### Test repeated games

After one round finishes, test:

* choosing to play again
* playing several rounds in a row
* winning in one round and tying in another
* entering `n` to exit

### A failed test is useful

If testing reveals a bug, that is not bad news. That is exactly what testing is for.

### The big takeaway from Step 6

A program is not complete when you finish writing it. A program is complete when you finish testing it.

Test:

* full games
* bad input
* wins, losses, and ties
* repeated games
* the AI under pressure
* interaction bugs between parts of the system

## Step 7: Make It Work Fast (If Needed)

By the time you reach Step 7, something important should already be true:

The program works.

It should now:

* run correctly
* handle input properly
* detect wins and ties
* allow repeated play
* make computer moves that do not lose

Only now do you ask the next question:

> **Does it need to be made faster?**

That word **need** matters. 

### Why speed comes last

If the program is not even correct yet, performance work is wasted.

A fast wrong answer is still wrong.
A fast crashing program is still broken.
A fast unfinished program is still unfinished.

### Most programs do not need optimization immediately

Many programs are already fast enough.

Unnecessary optimization can:

* make code harder to read
* make bugs harder to find
* increase complexity
* waste time solving a problem that may not even matter

### Why Tic-Tac-Toe is usually already fast enough

A Tic-Tac-Toe board has:

* only 9 cells
* only 8 winning lines
* only a small number of possible moves on each turn

Even pattern matching is tiny work for a modern computer.

### Example: pattern matching sounds expensive, but it is not here

The AI checks patterns against the board on each computer turn, but:

* the board has only 9 positions
* each pattern is only 9 entries long
* the number of turns is small

So even if the code is not mathematically optimal, it is still more than fast enough in practice.

### What optimization would even look like here?

Possible ideas could include:

* stopping pattern checks as soon as a match is found
* caching results instead of recalculating them
* reducing repeated board lookups
* simplifying some AI search logic

But in this project, those are probably unnecessary.

### Premature optimization is a real problem

Optimizing too early often causes more harm than good.

For a small classroom program, a clean, readable, correct Tic-Tac-Toe program is much better than a “highly optimized” one that is confusing or fragile.

### The best optimization may be no optimization

Sometimes the correct performance decision is:

> Leave it alone.

If the code is:

* correct
* readable
* maintainable
* fast enough

then changing it may provide little benefit and real risk.

### In this project, “fast enough” is the correct answer

For this Tic-Tac-Toe program, the likely conclusion is simple:

* the board is tiny
* the checks are small
* the AI runs quickly
* the user will not notice any delay

So the correct performance decision is usually:

> The program is already fast enough. Move on.

### The big takeaway from Step 7

Do not optimize just because optimization sounds impressive.

Optimize only when:

* the program is already correct
* there is an actual performance problem
* the improvement is worth the added complexity

For this Tic-Tac-Toe project, the answer will usually be that the current solution is already fast enough.

## The Complete Structure at a Glance

```text
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

This overall structure from the original document is strong because it separates responsibilities cleanly: `Cell` handles one square, `Board` handles the game state and rules, `MoveAI` handles strategy, and `main()` handles overall flow. 

## Key Issues Summary

### 1. Start with the data, not the logic

Build `Cell` before `Board`, and `Board` before `MoveAI`. Each layer should depend only on the layer below it.

### 2. Stub first, implement later

When you do not yet know how to write something fully, create the method anyway with a safe placeholder so the rest of the program can continue to take shape.

### 3. Follow the mantra in order

Make it work.
Make it work right.
Make it work fast.
Trying to do all three at once usually leads to confusion and weak code.

### 4. Do not repeat yourself

Store shared rules, such as the winning combinations, in one place and reuse them. Reuse `couldWin()` for both winning and blocking logic.

### 5. Each class should do one job

`Cell` manages a square.
`Board` manages the grid and rules.
`MoveAI` manages strategy.
`main()` manages the flow of the game.

### 6. Test deliberately, not casually

Do not just “run it once.” Try to break it. Test wins, blocks, ties, bad input, replay behavior, and AI responses under pressure.

### 7. Only optimize when it matters

For a 3×3 Tic-Tac-Toe game, the correct answer is usually that the code is already fast enough. Readability and correctness matter more than micro-optimizations.

### Final Summary

This project is not just about building Tic-Tac-Toe. It is about learning how to think like a programmer:

* understand the problem before coding
* build the foundation first
* use placeholders when needed
* replace them in a smart order
* separate responsibilities clearly
* test the full system
* optimize only if there is a real reason

That is what turns one sentence of assignment text into a working program. 


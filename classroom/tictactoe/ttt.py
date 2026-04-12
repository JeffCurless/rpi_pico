import random

computerToken   = 'X'
playerToken     = 'O'
emptyToken      = ' '

debugRules      = False
debugMatching   = False
debugTest       = False
debugPlay       = True

#
# Cell class.  A cell is a single component of the TicTacToe board.  The class contains
# the cell number and the token currently placed on it.
#
class Cell:

    """
    Cell class definition.  A tictactoe board consists of cells, each cell can contain a token
    representing the player that owns the location.
    """
    def __init__( self, cellNum: int ) -> None:
        """
            Initialize a tictactoe cell.

            Parameters:
                cellNum - The number of this cell (0-8).  Makes it easier to look up cells
                          that have tokens in it.

            Members:
                token   - The owning player's token
        """
        self.cellNum = cellNum
        self.token   = emptyToken

    def setToken( self, token: str ) -> None:
        """
            Set our current token to the token being passed in.  No validation.
        """
        self.token = token

    def getToken( self ) -> str:
        """
            Get the token of the player that owns this cell.
        """
        return self.token

    def isEmpty( self ) -> bool:
        """
            Determine if this cell is empty, or has a token.
        """
        return self.token == emptyToken

    def getIndex( self ) -> int:
        """
            Return the cell number of this cell.  This allows us to generically
            access which cell number we have *if* all we have is the cell (i.e. no
            reference to the board that contains this cell)
        """
        return self.cellNum

#
# Board class - This class contains all of the definitions and functions needed to play the
# game of tic tac toe
#
class Board:
    def __init__( self ) -> None:
        """
            Initialize the Board Class.  Creates the 9 cells and defines all
            possible winning move combinations.

            Members:
                cells        - A list of 9 Cell objects, one per board square
                winToken     - The winning token, i.e. who won the game
                winMove      - The winning move (the three cell indices that form the winning line)
                winningMoves - A list of all possible winning moves, used to detect if there is
                               a winner yet.  Could also be used to help the computer plan moves...
        """
        self.cells    = []
        self.winToken = emptyToken
        self.winMove  = []
        for i in range(9):
            self.cells.append( Cell(i) )
        self.winningMoves = [[0,1,2],[3,4,5],[6,7,8],
                             [0,3,6],[1,4,7],[2,5,8],
                             [0,4,8],[2,4,6]]

    def reset( self ) -> None:
        """
            Reset the board back to the beginning
        """
        for cell in self.cells:
            cell.setToken( emptyToken )
        self.winToken = emptyToken
        self.winMove  = []

    def getCell( self, cellNum: int ) -> Cell:
        """
            Return the cell located at the cell number provided
        """
        return self.cells[cellNum]

    def getCellToken( self, cellNum: int ) -> str:
        """
            Return the token for the cell number provided
        """
        return self.cells[cellNum].getToken()

    def setCellToken( self, cellNum: int, value: str ) -> None:
        """
            Set the token on the cell number provided
        """
        self.cells[cellNum].setToken( value )

    def checkForWinner( self, token: str ) -> bool:
        """
            Check to see if the current token is a winner, this way we can utilize the same code for both
            the computer and the player
        """
        winner = False
        for _move in self.winningMoves:
            if ((self.getCellToken( _move[0] ) == token) and
                (self.getCellToken( _move[1] ) == token)  and
                (self.getCellToken( _move[2] ) == token)):
                self.winMove  = _move
                self.winToken = token
                winner = True
        return winner

    def couldWin( self, cellNum: int, token: str ) -> bool:
        """
            Hypothetically place the token in cellNum and check if that would be a
            winning move.  The cell is restored to its previous state afterwards.
            Used by mustWinMove() to find an immediate winning cell for the computer,
            and by mustBlockMove() to find a cell the player would win with if left empty.
        """
        winner = False
        old = self.getCellToken( cellNum )
        self.setCellToken( cellNum, token )
        for _move in self.winningMoves:
            if ((self.getCellToken( _move[0] ) == token) and
                (self.getCellToken( _move[1] ) == token)  and
                (self.getCellToken( _move[2] ) == token)):
                winner = True
        self.setCellToken( cellNum, old )
        return winner

    def getEmptyCells( self ) -> list:
        """
            Return a list of cell indices for all cells that are currently empty
        """
        moves = []
        for i in range(9):
            item = self.getCell(i)
            if item.getToken() == emptyToken:
                moves.append( item.cellNum )
        return moves

    def movesExist( self ) -> bool:
        """
            Determine if there are any moves left on the board, if there are the game can
            continue
        """
        return len( self.getEmptyCells() ) > 0

    def getBoardAsList( self ) -> list:
        """
            Create a list of the current board tokens, used for printing and pattern matching.
        """
        _board = []
        for cell in self.cells:
            _board.append( cell.getToken() )
        return _board

    def paint( self ) -> None:
        """
            Print the current board state to the console.  Empty cells show their position
            number (1-9) so the player knows which number to enter for each square.
        """
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

    def displayWinner( self ) -> None:
        """
            Print the end-of-game result to the console.
        """
        if self.winToken == emptyToken:
            print( "It's a Tie!" )
        elif self.winToken == computerToken:
            print( "You Lose!" )
        else:
            print( "You win!" )

#
# MoveAI - The Movement class for the computer.  This will contain all of the required code to handle
# selecting a move (or series of moves) that will keep the computer from losing.  Note a tie is not
# considered a loss.
#
class MoveAI:
    def __init__( self, board: Board ) -> None:
        """
            Initialize the movement AI, this code will predict movement of the player, and
            move to actively block them.  The end result is the computer will never lose a
            game, it may tie, but not lose.

            Pattern descriptions:
                b - Blank
                * - Blank, but where we should move
                O - Opponent Token
                X - Our Token
                ? - Anything

        """
        self.board        = board
        self.patterns     = []
        self.basePatterns = [
                            # Strategic patterns: fork prevention and positional setup.
                            # Win (XX*) and block (OO*) patterns have been removed because
                            # computerMove() now handles those via mustWinMove/mustBlockMove,
                            # which scan all empty cells directly and never miss a win or block.
                            ['?','?','?','?','O','X','?','?','*'],
                            ['?','?','O','?','*','b','?','?','?'],
                            ['?','O','b','?','*','?','?','?','?'],
                            ['*','O','b','O','X','X','?','?','?'],
                            ['X','b','*','?','?','?','?','?','?'],
                            ['X','*','b','?','?','?','?','?','?'],
                            ['?','?','?','X','*','b','?','?','?'],
                            ['?','?','?','X','b','*','?','?','?'],
                            ['?','O','*','?','X','X','?','?','?'],
                            ['b','X','O','b','X','*','?','?','?'],
                            ]
        self.testPats = [
                         ['0','1','2','3','4','5','6','7','8'],
                        ]
        self.makeAllPatterns()

    def rotatePattern( self, pattern: list ) -> list:
        """
            Given a pattern we are looking at, rotate the pattern 90 degrees clockwise and
            return that pattern back to the caller.  This routine is used to determine if
            the board might match a rotated version of our given pattern so that we do not
            have to store all possible patterns.
        """
        newPattern = []
        for i in [6,3,0,7,4,1,8,5,2]:
            newPattern.append(pattern[i])
        return newPattern

    def mirrorPattern( self, pattern: list ) -> list:
        """
            Given a pattern we are looking at, generate its mirror image.  This routine is
            utilized to allow us to not have to store every possible pattern.
        """
        newPattern = []
        for i in [2,1,0,5,4,3,8,7,6]:
            newPattern.append(pattern[i])
        return newPattern

    def rotateMirrorTest( self ) -> None:
        """
            Verify that the rotate and mirror functions are working properly.
        """
        for pattern in self.testPats:
            n = pattern
            for i in range(4):
                n = self.rotatePattern( n )
                print( "rotate " + str(i) + " : " + str(n) )
            if n != pattern:
                print( "Rotation Test failed!")

        for pattern in self.testPats:
            n = pattern
            for i in range(2):
                n = self.mirrorPattern(n)
                print( "mirror " + str(i) + " : " + str(n) )
            if n != pattern:
                print( "Mirror test failed!" )

    def isUniquePattern( self, newPattern: list ) -> bool:
        """
            Check the given pattern against all of the patterns stored in self.patterns.
            Returns True if the newPattern does not already exist (i.e. it is unique).
        """
        for pattern in self.patterns:
            if pattern == newPattern:
                return False
        return True

    def makeAllPatterns( self ) -> None:
        """
            Given the list of base patterns (i.e. rules) create all of the patterns
            we can based off of rotating and mirroring the patterns given.  When we
            create the list we only want the unique ones presented...
        """
        for pattern in self.basePatterns:
            for i in range(4):
                if self.isUniquePattern( pattern ):
                    self.patterns.append( pattern )
                elif debugRules:
                    print( "Found Duplicate rotating " + str( pattern ))
                m = self.mirrorPattern( pattern )
                if self.isUniquePattern( m ):
                    self.patterns.append( m )
                elif debugRules:
                    print( "Found Duplicate mirroring " + str( pattern ))
                pattern = self.rotatePattern( pattern )

        if debugRules:
            print( "Base patterns expanded from " + str(len(self.basePatterns)) + " to " + str(len(self.patterns)) + " patterns." )
            self.printListOfPatterns( self.patterns )

    def cellMatch( self, boardToken: str, patternToken: str ) -> bool:
        """
            Return True if the boardToken satisfies the patternToken rule:
                b or * - matches an empty cell  (* also marks where to move)
                O      - matches the player token
                X      - matches the computer token
                ?      - matches anything
        """
        if patternToken == 'b' and boardToken == emptyToken:
            return True
        elif patternToken == '*' and boardToken == emptyToken:
            return True
        elif patternToken == 'O' and boardToken == playerToken:
            return True
        elif patternToken == 'X' and boardToken == computerToken:
            return True
        elif patternToken == '?':
            return True
        return False

    def doesBoardMatchPattern( self, pattern: list ) -> bool:
        """
            This routine takes the given pattern, and determines if the board in its
            current state matches the pattern.
        """
        for i in range(9):
            boardToken = self.board.getCellToken(i)
            if not self.cellMatch( boardToken, pattern[i]):
                return False
        return True

    def findMatchingPatterns( self ) -> list:
        """
            Scan all patterns in self.patterns and return a list of those that
            match the current board state.  Returns an empty list if none match.
        """
        matchList = []
        for pattern in self.patterns:
            if self.doesBoardMatchPattern( pattern ):
                matchList.append( pattern )
        return matchList

    def findMoveInPattern( self, pattern: list ) -> int:
        """
            Return the cell index marked '*' in the given pattern.  This is the cell
            the computer should move to.  Raises an exception if no '*' is found.
        """
        for i in range(9):
            if pattern[i] == '*':
                return i
        raise Exception( "Found no '*' in pattern " + str( pattern ))

    def printListOfPatterns( self, patterns: list, board: list = None ) -> None:
        """
            Debug utility: print each pattern in the list.  If board is provided,
            it is printed as a header showing the current board state alongside
            the matching patterns.
        """
        if board is None:
            print( "Possible moves: " )
        else:
            print( "Possible moves for: " + str( board ))
        for pattern in patterns:
            print( "    " + str(pattern) )

    def moveAccordingToPattern( self, listOfPatterns: list ) -> None:
        """
            Place the computer token on the cell marked '*' in the first pattern
            of the provided list.  The first matching pattern takes priority.
        """
        if debugMatching:
            self.printListOfPatterns( listOfPatterns, self.board.getBoardAsList() )
        cellNumber = self.findMoveInPattern( listOfPatterns[0] )
        self.board.setCellToken( cellNumber, computerToken )

    def mustWinMove( self ) -> int:
        """
            Scan all empty cells and return the first one that would give the computer
            a win.  Returns -1 if no immediate winning move exists.
        """
        for cell in self.board.getEmptyCells():
            if self.board.couldWin( cell, computerToken ):
                return cell
        return -1

    def mustBlockMove( self ) -> int:
        """
            Scan all empty cells and return the first one that would let the player win
            if left empty.  Returns -1 if no immediate block is needed.
        """
        for cell in self.board.getEmptyCells():
            if self.board.couldWin( cell, playerToken ):
                return cell
        return -1

    def randomMove( self, token: str ) -> None:
        """
            Generate a random move when we have no good choice to make.  Do this by
            generating a list of the empty cell locations, and then select one at
            random.
        """
        cells = self.board.getEmptyCells()
        if len(cells) > 0:
            location = random.randrange(len(cells))
            self.board.setCellToken( cells[location], token )

    def computerMove( self ) -> None:
        """
            Allow the computer to move using an explicit priority order:
              1. Win  - take any cell that wins the game immediately
              2. Block - take any cell that would let the player win
              3. Strategic patterns - fork prevention / positional setup
              4. Random - fallback when no pattern matches
        """
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
                    if debugMatching:
                        print( "Random move for board " + str(self.board.getBoardAsList()) )
                    self.randomMove( computerToken )

#
# Create the board and the AI
#
board = Board()
move  = MoveAI(board)

if debugTest:
    move.rotateMirrorTest()

#
# Main loop.  The computer (X) always goes first.  The player enters a position
# number 1-9 to place their token, where 1 is top-left and 9 is bottom-right.
#
def main() -> None:
    print( "Tic Tac Toe" )
    print( "Positions: 1=top-left  9=bottom-right" )
    print( " 1 | 2 | 3 " )
    print( "---+---+---" )
    print( " 4 | 5 | 6 " )
    print( "---+---+---" )
    print( " 7 | 8 | 9 " )
    print()

    while True:
        board.reset()
        if debugPlay:
            print( "New Game - Computer goes first (X)" )
        move.computerMove()
        board.paint()

        haveWinner = False
        while not haveWinner:
            #
            # Get a valid move from the player
            #
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

            if board.checkForWinner( playerToken ):
                board.displayWinner()
                haveWinner = True
            elif not board.movesExist():
                board.displayWinner()
                haveWinner = True
            else:
                print( "Computer's turn..." )
                move.computerMove()
                board.paint()
                if board.checkForWinner( computerToken ):
                    board.displayWinner()
                    haveWinner = True
                elif not board.movesExist():
                    board.displayWinner()
                    haveWinner = True

        #
        # Ask the player if they want to play again
        #
        again = input( "Play again? (y/n): " ).strip().lower()
        if again != 'y':
            break

#
# The main application
#
main()

import time
import random

from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from machine import Pin

debugSetup      = False
debugRules      = False
debugMatching   = False
debugTest       = False
debugPlay       = True

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(0.8)

led = RGBLED(6, 7, 8)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WIDTH, HEIGHT = display.get_bounds()
penGrid         = display.create_pen( 255,255,255 )
penBackground   = display.create_pen( 0, 0, 0 )
penSelector     = display.create_pen( 255, 0, 0 )
penToken        = display.create_pen( 0, 255, 0 )
offset          = 4
scaleFactor     = 2
computerToken   = 'X'
playerToken     = 'O'
emptyToken      = ' '
debugSetup      = False
debugRules      = False
debugMatching   = False
debugTest       = False
debugPlay       = True

#
# Cell class.  A cell is a single component of the TicTacToe board.  The class contains the
# coordinates of the upper left corner of the cell, as well as the current player that owns it,
# and the cell number as is exists in the board.
#
class Cell:
    
    global debugSetup


    """
    Cell class definition.  A tictactoe board consists of cells, each cell can contain a token
    representing the player that owns the location.
    """
    def __init__( self, x, y, width, cellNum ):
        """
            Initialize a tictactoe cell.
        
            Parameters:
                x       - The upper left corner of the cell
                y       - The upper left corner of the cell
                width   - How wide is cell (and since it is a square, how tall is it)
                cellNum - The number of this cell.  Makes it easier to look up cells
                          that have tokens in it.
                          
            Members:
                token   - The owning players token
        """

        self.x       = x
        self.y       = y
        self.width   = width
        self.cellNum = cellNum
        self.token   = emptyToken
        if debugSetup:
            print( "Creating cell " + str(cellNum) + " at (" + str(x) + ", " + str(y) + ")")
        
    def getX( self ):
        """
            Return the X location of the cell
        """
        return self.x
    
    def getY( self ):
        """
            Return the Y location of the cell
        """
    def setToken( self, token ):
        """
            Set our current token to the token being passed in.  No validation.
        """
        self.token = token
        
    def getToken( self ):
        """
            Get the token of the player that owns this cell.
        """
        return self.token
    
    def isEmpty( self ):
        """
            Determine if this cell is empty, or has a token.
        """
        return self.token == emptyToken
    
    def getIndex( self ):
        """
            Return the cell number of this cell.  This allows us to generically
            access which cell number we have *if* all we have is the cell (i.e. no
            reference to the board that contains this cell)
        """
        return self.cellNum
            
    def getCenter( self ):
        """
            Since we know the dimensions of the cell, return the coordinates of the
            center.  Let the cell itself do the math
        """
        cx = self.x + self.width//2
        cy = self.y + self.width//2
        return cx, cy
    
#
# Board class - This class contains all of the definitions and functions needed to play the
# game of tic tac toe
#
class Board:
    def __init__( self, width ):
        """
            Initialize the Board Class.  This takes the width of the board are on the
            screen.  This area is then broken down into the cells for each square a
            player can move in.  Also stored are the winning move and winning token.
            
            Parameters:
                width        - The total width of the board.
                
            Members:
                width        - How wide the board is
                cells        - An array of class Cell, each entry representing a square on the board
                selector     - The location of the current cell the user can select for a turn
                cwidth       - Width of a cell (yes it is just 1/3 of width, but this makes is easier
                winToken     - The winning token, i.e. who one the game
                winMove      - The winning move (the row info)
                winningMoves - A list of all possible winning moves, used to detect if there is
                               a winner yet.  Could also be used to help the computer plan moves...
        """
        self.width    = width
        self.cells    = []
        self.selector = 0
        self.cwidth   = width // 3
        self.winToken = emptyToken
        self.winMove  = []
        x = 0
        y = 0
        for i in range(9):
            self.cells.append( Cell(x, y, self.cwidth, i) )
            x += self.cwidth
            if ((i+1) % 3) == 0:
                x = 0
                y += self.cwidth
        self.winningMoves = [[0,1,2],[3,4,5],[6,7,8],
                             [0,3,6],[1,4,7],[2,5,8],
                             [0,4,8],[2,4,6]]
    
    def reset( self ):
        """
            Reset the board back to the beginning
        """
        for cell in self.cells:
            cell.setToken( emptyToken )
        self.winToken = emptyToken
        self.winMove  = []
        self.selector = 0
        
        
    def getCell( self, cellNum ):
        """
            Return the cell located at the cell number povided
        """
        return self.cells[cellNum]
    
    def getCellToken( self, cellNum ):
        """
            Return the token for the cell number provided
        """
        return self.cells[cellNum].getToken()
    
    def setCellToken( self, cellNum, value ):
        """
            Set the token on the cell number provided
        """
        self.cells[cellNum].setToken( value )
        
    def getSelectedCell( self ):
        """
            get the cell that is currently selected
        """
        return self.cells[self.selector]
    
    def incSelector( self ):
        """
            Increment the selector, and handle the wrap
        """
        self.selector += 1
        if self.selector >= 9:
            self.selector = 0
    
    def decSelector( self ):
        """
            Decrement the selector, and handle any wrap that might occur
        """
        self.selector -= 1
        if self.selector < 0:
            self.selector = 8

    def showSelector(self):
        """
            Show the selector.  The selector is a square that outlines which cell
            the user currently has selected.
        """
        width  = self.cwidth - (offset * 2)
        display.set_pen(penSelector)
        cell = self.cells[self.selector]
        startx = cell.x + offset
        starty = cell.y + offset
        stopx  = startx + width
        stopy  = starty + width
        display.line(startx, starty, stopx, starty,offset)
        display.line(stopx,  starty, stopx, stopy, offset)
        display.line(startx, starty, startx,stopy, offset)
        display.line(startx, stopy,  stopx, stopy, offset)
    
    def displayWinningMove( self ):
        """
            Display the winning move!  This is done by taking the winning move as stored
            on the board, and dring from the center of the first cell, to the center of
            the last cell.
        """
        if self.winMove != []:
            cell1 = board.getCell( self.winMove[0] )
            cell2 = board.getCell( self.winMove[2] )
            display.set_pen( penSelector )
            startx, starty = cell1.getCenter()
            stopx, stopy = cell2.getCenter()
            display.line( startx, starty, stopx, stopy, 10 )
            
    def checkForWinner(self, token):
        """
            Check to see if the current token is a winner, this was we can utilize the same code for both
            the computer and the player
        """
        winner = False
        for move in self.winningMoves:
            if ((self.getCellToken( move[0] ) == token) and
                (self.getCellToken( move[1] ) == token)  and
                (self.getCellToken( move[2] ) == token)):
                self.winMove  = move
                self.winToken = token
                winner = True
        return winner
    
    def couldWin( self, cellNum, token ):
        """
            Determine if the token were placed in the cellnumber, if the
            player (determined by the token) would win.  This is used to help
            determine if we should play a specific rule or not.  We want to
            win, but we need to move *if* the player would win if we don't
        """
        winner = False
        old = self.getCellToken( cellNum )
        self.setCellToken( cellNum, token )
        for move in self.winningMoves:
            if ((self.getCellToken( move[0] ) == token) and
                (self.getCellToken( move[1] ) == token)  and
                (self.getCellToken( move[2] ) == token)):
                winner = True
        self.setCellToken( cellNum, old )
        return winner
    
    def drawToken( self, cell ):
        """
            Draw the token for this cell.  There are two tokens, an 'X' and an 'O'.  
        """
        display.set_pen( penToken )
        if cell.getToken() == computerToken:
            width  = self.cwidth - offset
            startx = cell.x + offset
            starty = cell.y + offset
            stopx  = cell.x + width
            stopy  = cell.y + width
            display.line( startx, starty, stopx, stopy,  offset )
            display.line( startx, stopy,  stopx, starty, offset )
        elif cell.getToken() == playerToken:
            r = (cell.width//2) - offset
            x, y = cell.getCenter()
            display.circle( x, y, r )
            display.set_pen( penBackground )
            display.circle( x, y, r-offset )
    
    def getEmptyCells( self ):
        """
            Return a list containing all of the cells that are empty
        """
        moves = []
        for i in range(9):
            item = self.getCell(i)
            if item.getToken() == emptyToken:
               moves.append( item.cellNum )
        return moves
    
    def movesExist( self ):
        """
            Determine if there are any moves left on the board, if there are the game can
            continue
        """
        movesAvailable = False
        if len(self.getEmptyCells()) > 0:
            movesAvailable = True
        return movesAvailable
    
    def displayWinner(self):
        """
            Display who won!
        """
        textx = 0
        texty = WIDTH+(8*scaleFactor)

        display.set_pen( penGrid )
        display.set_font( "bitmap8" )
        if self.winToken == emptyToken:
            message = "It's a Tie!"
        elif board.winToken == computerToken:
            message = "You Lose!"
        else:
            message = "You win!"

        width = display.measure_text( message, scaleFactor )
        textx = (WIDTH - width)//2
        display.text( message, textx, texty, WIDTH, scale=scaleFactor )
        display.update()
        
    def getBoardAsList(self):
        """
            Create a list of the current board, we can use this list to display the board
            to the user as a text image if we wish
        """
        board = []
        for cell in self.cells:
            board.append( cell.getToken() )
                
        return board
        
    def printTextBoard( self, board ):
        """
            Given a board setup as a list, draw it out on text screen,  This is primarily used
            as a debug tool.
        """
        for i in (0,3,6):
            print( ' {} | {} | {}'.format(board[i],board[i+1],board[i+2]))
            if i != 6:
                print('---+---+---')
        print( emptyToken )
    
    def paint( self ):
        """
            Paint the board on the screen, we paint the hash grid, then the board cells, then
            we paint the winner (if there is one) or show the selector so we know where the player
            can add their move
        """
        first  = self.cwidth
        second = first * 2
        display.set_pen( penBackground )
        display.clear()
        display.set_pen( penGrid )
        display.line( first, 0, first, self.width, 2 )
        display.line( second, 0, second, self.width, 2)
        display.line( 0, first, self.width, first, 2 )
        display.line( 0, second, self.width, second, 2 )
        
        for i in range(9):
            cell = board.cells[i]
            if not cell.isEmpty():
                self.drawToken( cell )
    
        if self.winMove != []:
            self.displayWinningMove()
        else:
            self.showSelector()
        display.update()

#
# MoveAI - The Movement class for the computer.  This will contain all of the required code to handle
# selecting a move (or series of moves) that will keep the computer from losing.  Note a tie is not
# considered a loss.
#
class MoveAI:
    def __init__(self,board):
        """
            Initialize the movement AI, this code will predict movement of the player, and
            move to activly block them.  The end result is the computer will never lose a
            game, it may tie, but not lose.
            
            Pattern descriptions:
                b - Blank
                * - Blank, but where we should move
                O - Opponent Token
                X - Our Token
                ? - Anything
                
        """
        self.board    = board
        self.patterns     = []
        self.basePatterns = [
                            #['b','*','b','b','b','b','b','b','b'],
                            ['X','X','*','?','?','?','?','?','?'],
                            ['X','*','X','?','?','?','?','?','?'],
                            ['?','?','?','X','X','*','?','?','?'],
                            ['?','?','?','X','*','X','?','?','?'],
                            ['X','?','?','?','X','?','?','?','*'],
                            ['X','?','?','?','*','?','?','?','X'],
                            ['?','?','?','?','O','X','?','?','*'],
                            ['?','?','O','?','*','b','?','?','?'],
                            ['?','O','b','?','*','?','?','?','?'],
                            ['O','O','*','?','?','?','?','?','?'],
                            ['O','*','O','?','?','?','?','?','?'],
                            ['?','?','?','O','O','*','?','?','?'],
                            ['?','?','?','O','*','O','?','?','?'],
                            ['O','?','?','?','O','?','?','?','*'],
                            ['O','?','?','?','*','?','?','?','O'],
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
    
    def rotatePattern( self, pattern ):
        """
            Given a pattern we are looking at, rotate the pattern to the right and
            return that battern back to the caller.  This routine is used to determine if
            the board might match a rotated version of our given pattern so that we do not
            have to store all possible patterns.
        """
        newPattern = []
        for i in [6,3,0,7,4,1,8,5,2]:
            newPattern.append(pattern[i])
        return newPattern
                
    def mirrorPattern( self, pattern ):
        """
            Given a pattern we are looking at, generate its mirror image.  This routine is
            utilized to allow us to not have to store every possible pattern.
        """
        newPattern = []
        for i in [2,1,0,5,4,3,8,7,6]:
            newPattern.append(pattern[i])
        #for i in [6,7,8,3,4,5,0,1,2]:
        #    newPattern.append(pattern[i])
        return newPattern
    
    def rotateMirrorTest( self ):
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
    
    def isUniquePattern( self, newPattern ):
        """
            Check the given pattern against all of the patters stored in self.patterns.
            and if the newPattern does not exist, return TRUE, in that it is a unique pattern.
        """
        for pattern in self.patterns:
            if pattern == newPattern:
                return False
        return True
    
    def makeAllPatterns( self ):
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
                
    def cellMatch( self, boardToken, patternToken ):
        #print( "Checking to see if " + str(boardToken) + " matches " + str(patternToken) )
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
    
    def doesBoardMatchPattern( self, pattern ):
        """
            This routine takes the given pattern, and determines if the board in its
            current state matches the pattern.
        """
        #print( "Checking pattern : " + str( pattern ) )
        for i in range(9):
            boardToken = self.board.getCellToken(i)
            if not self.cellMatch( boardToken, pattern[i]):
                return False
        return True

    def findMatchingPatterns( self ):
        matchList = []
        for pattern in self.patterns:
            if self.doesBoardMatchPattern( pattern ):
                #print( "Matched : " + str(pattern))
                matchList.append( pattern )

        return matchList
    
    def findMoveInPattern( self, pattern ):
        for i in range(9):
            if pattern[i] == '*':
                return i
            
        raise Exception( "Found no '*' in pattern " + str( pattern ))
        return -1
    
    def printListOfPatterns( self, patterns, board = []):
        if board == []:
            print( "Possible moves: " )
        else:
            print( "Possible moves for: " + str( board ))

        for pattern in patterns:
            print( "    " + str(pattern) )
    
    def moveAccordingToPattern( self, listOfPatterns ):
        if debugMatching:
            self.printListOfPatterns( listOfPatterns, self.board.getBoardAsList() )
        
        if len( listOfPatterns  ) == 1:
            cellNumber = self.findMoveInPattern( listOfPatterns[0] )
        else:
            first = -1
            for pattern in listOfPatterns:
                cellNumber = self.findMoveInPattern( pattern )
                if first == -1:
                    first = cellNumber
                if self.board.couldWin( cellNumber, computerToken ):
                    self.board.setCellToken( cellNumber, computerToken )
                    if debugMatching:
                        print( "Using move:" + str(pattern))
                    return
                else:
                    if self.board.couldWin( cellNumber, playerToken ):
                        self.board.setCellToken( cellNumber, computerToken )
                        if debugMatching:
                            print( "Blocking move: " + str( pattern ))
                        return        
            cellNumber = first
            
        self.board.setCellToken( cellNumber, computerToken )
        
    def randomMove( self, token ):
        """
            Generate a random move when we have no good choice to make.  Do this by
            generating a list of the empty cell locations, and then select one at
            random.
        """
        cells = self.board.getEmptyCells()
        if len(cells) > 0:
            location = random.randrange(len(cells))
            self.board.setCellToken( cells[location], token )

    def computerMove(self):
        """
            Allow the computer to move.  This routine should be where we add in the AI logic
            to automatically select the best move based on what we currently see on the board.
        
            The intent here is that we can utilize the winningMoves list looking for a weighted
            solution that provides the best move based on all possible moves.
        
            Most Important:
        
            We simply select a random location from the currently empty locations...
        """
        matchingPatterns = self.findMatchingPatterns()
        if len( matchingPatterns ):
            led.set_rgb( 0, 0, 255 )
            self.moveAccordingToPattern( matchingPatterns )
        else:
            led.set_rgb( 255,0,0 )
            if debugMatching:
                print( "Random move for board " + str(self.board.getBoardAsList()) )
            self.randomMove( computerToken )
        
        board.printTextBoard( board.getBoardAsList() )
        self.board.paint()

#
# Display a message on screen, at the y offset, centered
#
def printMessage( yOffset, message ):
    """
        Display a message, centered along X
    """
    width = display.measure_text( message, scaleFactor )
    textx = (WIDTH - width)//2
    texty = WIDTH + yOffset
    display.text( message, textx, texty, WIDTH, scale=scaleFactor )
    display.update()
#
# Create the board to fit the display
#
board = Board(WIDTH)
move  = MoveAI(board)

if debugTest:
    move.rotateMirrorTest()

#
# Main loop... Depending on the button pressed, perform the action.  First things first, let the
# computer (X) make the first move
#
def main():
    print("New Game:")
    while True:
        board.reset()
        move.computerMove()

        playerMoved = False
        haveWinner  = False
        while not haveWinner:
            if button_a.read():
                cell = board.getSelectedCell()
                if cell.isEmpty():
                    board.setCellToken( cell.getIndex(), playerToken )
                    board.paint()
                    playerMoved = True
            elif button_x.read():
                board.incSelector()
                board.paint()
            elif button_y.read():
                board.decSelector()
                board.paint()
    
            if playerMoved:
                board.printTextBoard( board.getBoardAsList() )
                if board.checkForWinner( playerToken ):
                    board.paint()
                    haveWinner = True
                else:
                    move.computerMove()
                    if board.checkForWinner( computerToken ):
                        board.paint()
                        haveWinner = True
                    elif not board.movesExist():
                        haveWinner = True
                    playerMoved = False
        
            time.sleep(0.1)
        #
        # Display who won!
        #
        board.displayWinner()
        
        #
        # Display a message for the user to continue
        #
        printMessage( 48, "Press B to" )
        printMessage( 62, "continue..." )
        
        waitForContinue = False
        while( waitForContinue == False ):
            if button_b.read():
                waitForContinue = True
            time.sleep(0.1)
            
        if debugPlay:
            print( "New Game:")

#
# The main application
#
main()
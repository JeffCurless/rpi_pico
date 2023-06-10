import time
import random
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(0.8)

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
computerToken   = 'X'
playerToken     = 'O'
emptyToken      = ''
scaleFactor     = 2
#
# List of all winning moves as strings... so we can search quickly
#
winningMoves = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]

#
# Cell class.  A cell is a single component of the TicTacToe board.  The class contains the
# coordinates of the upper left corner of the cell, as well as the current player that owns it,
# and the cell number as is exists in the board.
#
class Cell:
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
        """
        self.width = width
        self.cells = []
        self.selector = 0
        self.cwidth = width // 3
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
    
    def displayWinner( self ):
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
        for move in winningMoves:
            if ((self.getCellToken( move[0] ) == token) and
                (self.getCellToken( move[1] ) == token)  and
                (self.getCellToken( move[2] ) == token)):
                self.winMove  = move
                self.winToken = token
                winner = True
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
            if item.getToken() == '':
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
            self.displayWinner()
        else:
            self.showSelector()
        display.update()

def randomMove( token ):
    """
        Generate a random move when we have no good choice to make.  Do this by
        generating a list of the empty cell locations, and then select one at
        random.
    """
    cells = board.getEmptyCells()
    if len(cells) > 0:
        location = random.randrange(len(cells))
        board.setCellToken( cells[location], token )

def computerMove():
    """
        Allow the computer to move.  This routine should be where we add in the AI logic
        to automatically select the best move based on what we currently see on the board.
        
        The intent here is that we can utilize the winningMoves list looking for a weighted
        solution that provides the best move based on all possible moves.
        
        Most Important:
        
        We simply select a random location from the currently empty locations...
    """
    randomMove( computerToken )
    board.paint()

#
# Create the board to fit the display
#
board = Board(WIDTH)

#
# Main loop... Depending on the button pressed, perform the action.  First things first, let the
# computer (X) make the first move
#
computerMove()

playerMoved = False
haveWinner  = False
while not haveWinner:
    if button_a.read():
        cell = board.getSelectedCell()
        if cell.isEmpty():
            board.setCellToken( cell.getIndex(), playerToken )
            board.paint()
            playerMoved = True
    elif button_b.read():
        print( "Button B pressed" )
    elif button_x.read():
        board.incSelector()
        board.paint()
    elif button_y.read():
        board.decSelector()
        board.paint()
    
    if playerMoved:
        if board.checkForWinner( playerToken ):
            board.paint()
            haveWinner = True
        else:
            computerMove()
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
textx = 0
texty = WIDTH+(8*scaleFactor)

display.set_pen( penGrid )
display.set_font( "bitmap8" )
if board.winToken == emptyToken:
    message = "It's a Tie!"
elif board.winToken == computerToken:
    message = "You Lose!"
else:
    message = "You win!"

width = display.measure_text( message, scaleFactor )
textx = (WIDTH - width)//2
display.text( message, textx, texty, WIDTH, scale=scaleFactor )
display.update()
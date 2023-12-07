#
# microKarel - A miniature version of the Karel Programming Environment.
#
# This code is not perfect, there are going to be issues with the syntax
# checking of the "language" being used, as not much time has been spent
# dealing with that aspect.
#
# This code is meant to be a mechanism to show how something like a Karel
# programming world could be created, and created on a tiny little display
# running on a Raspberry Pi PICO.
#
# Author: Jeff Curless
# Written for STEM night
#
import time
import random
import gc

from command import *
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from machine import Pin

#
# Debug settings... when there is an issue, turn them on to see the
# problem can be found..
#
debugDraw  = False
debugKarel = False
debugBall  = False
debugWhile = False
debugMem   = False
debugCode  = False

#
# Some constants that we will need
# 
scaleFactor = 2          # Text Scaling factor
NORTH       = 0      
EAST        = 1
SOUTH       = 2
WEST        = 3
BETWEEN     = 15         # Space between dots: 15(9x9 grid), 21(6x6 grid) are good
START       = BETWEEN//2 # Offset for starting the dots (gives us a border)
BALLSIZE    = 6          # Size of a ball
TIMEDELAY   = 0.25       # How long do we wait between instructions

#
# Setup the tricolor LED, and initialize it to black (No color) 
#
led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)

#
# Setup buttons, not that we are actually using them...
# 
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

#
# HandleException - Display an exception on the screen of the PICO Display
#
def handleException( e ):
    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
    display.set_backlight(1.0)
    width, height = display.get_bounds()
    display.set_pen( display.create_pen( 0, 0, 0 ) )
    display.clear()
    textx = 0
    texty = 0
    display.set_pen( display.create_pen( 0, 255, 0 ) )
    display.text( str(e), textx, texty, width-20, scale=scaleFactor )
    display.update()
    led.set_rgb( 255,0,0)

#
# Karel Class...
#
# Karel is a dog that wanders around the room, based on how he is programmed.
#
# Karel *always* is initialized to the top left corner of his world.
#
class Karel:
    def __init__(self,direct):
        self.x            = START
        self.y            = START
        self.direction    = direct
        self.world_width  = 0
        self.world_height = 0
    
    #
    # setup - Initialze karel with world information, happens after karel has
    #         been created, and the world has been created... just as we insert
    #         karel into the world
    #
    def setup( self, width, height ):
        self.world_width = width
        self.world_height = height
        
    #
    # canMove - Check to see if karel can move to the new location,
    #           if the move cannot be done, and exception is thrown
    #
    def canMove(self,x,y):
        if (x >= START) and (x < self.world_width):
            if (y >= START) and (y < self.world_height):
                self.x = x
                self.y = y
                return
        raise Exception( "Karel hit a wall!" )
    
    #
    # move - Move karel one space in the direction he is facing.
    #
    def move(self):
        if self.direction == NORTH:
            self.canMove( self.x, self.y-BETWEEN)
        elif self.direction == EAST:
            self.canMove( self.x+BETWEEN, self.y )
        elif self.direction == SOUTH:
            self.canMove( self.x, self.y+BETWEEN)
        elif self.direction == WEST:
            self.canMove( self.x-BETWEEN, self.y )
        if debugKarel:
            print( "K: %d (%3d,%3d)" % (self.direction,self.x, self.y) )
    
    #
    # turnRight - Turn Karel to the right
    #
    def turnRight(self):
        self.direction = self.direction + 1
        if self.direction > WEST:
            self.direction = NORTH 
        if debugKarel:
            print( "K: %d (%3d,%3d)" % (self.direction,self.x, self.y))

    #
    # turnLeft - Turn Karel to the left
    #
    def turnLeft(self):
        self.direction = self.direction - 1
        if self.direction < NORTH:
            self.direction = WEST
        if debugKarel:
            print( "K: %d (%3d,%3d)" % (self.direction,self.x, self.y))

#
# Ball - Sometimes Karel likes to play with a ball!
#
# For the moment, simply keep track of where the ball is.  
#
class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#
# World - The world that Karel lives in
#
# This class contains all of the code to display the Karel world,
# and allow him to move about the place.
#
class World:
    def __init__( self, karel ):
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
        self.display.set_backlight(0.8)
        self.width, self.height = self.display.get_bounds()
        self.background = self.display.create_pen( 0, 0, 0 )
        self.error      = self.display.create_pen( 0, 255, 0 )
        self.foreground = self.display.create_pen( 192,192,192 )
        self.karelPen   = self.display.create_pen( 255,0,0 )
        self.ballPen    = self.display.create_pen( 255,255, 0 )
        self.karel      = karel
        self.balls      = []
        self.program    = []
        
        #
        # Make Karel's world a square...  If you want the maximum space
        # Karel can roam about in, simply remove the assignment below.
        #
        self.height = self.width
        
        #
        # Set Karel up in the world... and draw it!
        #
        self.karel.setup( self.width, self.height )
        self.display.set_pen( self.background )
        self.display.clear()
        self.drawBoard()
 
    #
    # drawKarel - Draw Karel.  Given the really low resolution, make Karel
    #             a triangle.
    #
    def drawKarel( self ):
        global debugKarel
        self.display.set_pen( self.karelPen )        
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        x3 = 0
        y3 = 0
        if self.karel.direction == NORTH:
            x1 = self.karel.x-START
            y1 = self.karel.y+START
            x2 = self.karel.x
            y2 = self.karel.y-START
            x3 = self.karel.x+START
            y3 = self.karel.y+START
        elif self.karel.direction == EAST:
            x1 = self.karel.x-START
            y1 = self.karel.y-START
            x2 = self.karel.x+START
            y2 = self.karel.y
            x3 = self.karel.x-START
            y3 = self.karel.y+START
        elif self.karel.direction == SOUTH:
            x1 = self.karel.x-START
            y1 = self.karel.y-START
            x2 = self.karel.x
            y2 = self.karel.y+START
            x3 = self.karel.x+START
            y3 = self.karel.y-START
        elif self.karel.direction == WEST:
            x1 = self.karel.x+START
            y1 = self.karel.y-START
            x2 = self.karel.x-START
            y2 = self.karel.y
            x3 = self.karel.x+START
            y3 = self.karel.y+START
        
        if debugDraw:
            print( "K: %d ( %3d, %3d ), (%3d, %3d), (%3d, %3d)" % (self.karel.direction,x1,y1,x2,y2,x3,y3))
        self.display.triangle( x1, y1, x2, y2, x3, y3 )

    #
    # drawBalls - Karel likes to play with balls... this routine draws them
    #             all on the display.
    #
    def drawBalls( self ):
        for ball in self.balls:
            self.display.set_pen( self.ballPen )
            self.display.circle( ball.x, ball.y, BALLSIZE )

    #
    # drawBackground - Draw the background board.  Make sure that we draw
    #                  within the ranges allowed.
    #
    def drawBackground( self ):
        self.display.set_pen( self.background )
        self.display.clear()
        self.display.set_pen( self.foreground )
        for h in range( START, self.height, BETWEEN ):
            for w in range( START, self.width, BETWEEN ):
                self.display.circle( w, h, 1 )

    #
    # drawBoard - Draw the entire board... this includes all the items
    #             that are in the world, making sure that we draw Karel
    #             last.
    #
    def drawBoard(self):
        self.drawBackground()
        self.drawBalls()
        self.drawKarel()
        self.display.update()
           
    #
    # executeCommand - Given a command, process it!
    #
    # All commands should be listed here, but no conditionals.
    # Conditionals are executed by commands that accept/require
    # a conditional
    #
    def executeCommand( self, cmd ):
        gc.collect()
        if debugMem: print( "Free Memory: %d"%(gc.mem_free()))
        if cmd.cmd == CMD_MOVE:
            self.move()
        elif cmd.cmd == CMD_TURNRIGHT:
            self.turnRight()
        elif cmd.cmd == CMD_TURNLEFT:
            self.turnLeft()
        elif cmd.cmd == CMD_DROPBALL:
            self.dropBall()
        elif cmd.cmd == CMD_TAKEBALL:
            self.takeBall()
        elif cmd.cmd == CMD_WHILE:
            self.whileCmd(cmd)
        elif cmd.cmd == CMD_FOR:
            self.forCmd(cmd)
        elif cmd.cmd == CMD_IF:
            self.ifCmd(cmd)
        elif cmd.cmd == CMD_ELSE:
            self.elseCmd(cmd)
        elif cmd.cmd == CMD_FUNCTION:
            self.functionCmd(cmd)
        else:
            print( f"Command {cmd} not implemented!" )
        time.sleep(0.1)
    
    #
    # executeCondition - Given a conditional command, execute it.
    #
    # Note that for sanity we utilize the "range" as a "conditional" 
    #
    def executeCondition( self, cmd ):
        if cmd.cmd == CMD_FRONTCLEAR:
            return self.frontIsClear()
        elif cmd.cmd == CMD_FRONTBLOCKED:
            return self.frontIsBlocked()
        elif cmd.cmd == CMD_BALLSPRESENT:
            return self.ballsPresent()
        elif cmd.cmd == CMD_NOBALLS:
            return self.noBallsPresent()
        elif cmd.cmd == CMD_RIGHTCLEAR:
            return self.rightIsClear()
        elif cmd.cmd == CMD_RIGHTBLOCKED:
            return self.rightIsBlocked()
        elif cmd.cmd == CMD_LEFTCLEAR:
            return self.leftIsClear()
        elif cmd.cmd == CMD_LEFTBLOCKED:
            return self.leftIsBLocked()
        elif cmd.cmd == CMD_FACINGNORTH:
            return self.facingNorth()
        elif cmd.cmd == CMD_FACINGEAST:
            return self.facingEast()
        elif cmd.cmd == CMD_FACINGSOUTH:
            return self.facingSouth()
        elif cmd.cmd == CMD_FACINGWEST:
            return self.facingWest()
        elif cmd.cmd == CMD_RANGE:
            return self.rangeCmd(cmd)
        else:
            print( f"Command {cmd} has not been implemented yet!" )
    
    #
    # executeProgram - Given a "program" from the user, execute it
    #
    def executeProgram(self):
        if self.program is None:
            raise Exception( "No program defined!" )
        else:
            for cmd in self.program:
                self.executeCommand( cmd )

    #
    # setupProgram - This function simply assigns read in program
    #                 the the Karel world
    #
    def setupProgram( self, program ):
        self.program = program

    #
    # handleCrash - If there is a crash, make sure we tell the user what happened!
    #
    def handleCrash(self, e):
        self.display.set_pen( self.background )
        self.display.clear()
        width = self.display.measure_text( str(e), scaleFactor )
        textx = 0 #(self.width - width)//2
        texty = 0
        self.display.set_pen( self.error )
        self.display.text( str(e), textx, texty, self.width, scale=scaleFactor )
        self.display.update()
        led.set_rgb( 255,0,255)
        print( e )
        
    #
    # All Karel functions are listed below.  Note that some will call
    # and update the karel object, others will add or remove from the
    # balls object.  Anything that involves changing how the world looks
    # should result in a delay...
    #
    
    #
    # move - Called when we want to move Karel.  This function actually tells karel to move, and
    #        then we draw karel in the world.
    # 
    def move(self):
        self.karel.move()
        self.drawBoard()
        
    #
    # turnRight - Called when we want to turn Karel.  This function actually tells karel to turn, and
    #             then we draw karel in the world.
    # 
    def turnRight(self):
        self.karel.turnRight()
        self.drawBoard()
    
    #
    # turnLeft - Called when we want to turn Karel.  This function simply tells karel to turn, and
    #            then we draw karel in the world.
    #            
    #
    def turnLeft(self):
        self.karel.turnLeft()
        self.drawBoard()
        
    #
    # dropBall -  Drop a ball for Karel.
    #
    # We drop the ball directly where Karel is, and he can later pick it up.
    # Note that we are doing nothing to make storing the balls efficiently
    # as we assume that no will will create a huge number of balls... if they
    # do it will be slow to collect them all.
    #
    def dropBall(self):
        ball = Ball( self.karel.x, self.karel.y )
        if debugBall:
            print( "Drop (%3d,%3d)" % (ball.x,ball.y))
        self.balls.append( ball )
        self.drawBoard()
        
    #
    # takeBall - Allow Karel to take a ball if he is standing on it
    #
    # If there is no ball preset, he will generate a exception and the
    # program ends
    #
    def takeBall(self):
        found = False
        for ball in self.balls:
            if (ball.x == self.karel.x) and (ball.y == self.karel.y):
                self.balls.remove(ball)
                if debugBall:
                    print( "Take (%3d,%3d)" % (ball.x,ball.y))
                found = True
                break
        if not found:
            raise Exception( "No ball to take!" )
        self.drawBoard()
        
    #
    # frontIsClear = Determine if there is anyting blocking Karels way forward in the world.
    #    
    def frontIsClear(self):
        clear = False
        x = self.karel.x
        y = self.karel.y
        direct = self.karel.direction
        if (direct == NORTH) and (y-BETWEEN >= START):
            clear = True
        elif (direct == EAST) and (x+BETWEEN < self.width): 
            clear = True
        elif (direct == SOUTH) and (y+BETWEEN < self.height):
            clear = True
        elif (direct == WEST) and (x-BETWEEN >= START):
            clear = True
        return clear
    
    #
    # leftIsClear - Is the left side if Karl clear?
    #
    # Determine if the left side of Karel is clear, based on
    # his current diretion
    #
    def leftIsClear(self):
        clear = False
        x = self.karel.x
        y = self.karel.y
        direct = self.karel.direction
        if (direct == NORTH) and (x-BETWEEN >= START):
            clear = True
        elif (direct == EAST) and (y-BETWEEN < self.width): 
            clear = True
        elif (direct == SOUTH) and (x+BETWEEN < self.height):
            clear = True
        elif (direct == WEST) and (y+BETWEEN >= START):
            clear = True
        return clear
    
    #
    # rightIsClear - Is the right side if Karl clear?
    #
    # Determine if the right side of Karel is clear, based on
    # his current diretion
    #
    def rightIsClear(self):
        clear = False
        x = self.karel.x
        y = self.karel.y
        direct = self.karel.direction
        if (direct == NORTH) and (x+BETWEEN >= START):
            clear = True
        elif (direct == EAST) and (y+BETWEEN < self.width): 
            clear = True
        elif (direct == SOUTH) and (x-BETWEEN < self.height):
            clear = True
        elif (direct == WEST) and (y-BETWEEN >= START):
            clear = True
        return clear
    
    #
    # range - Takes a cmd and executes the "range" function on it.  Bascially, we
    #         initialize a counter when we read in the program, and when that counter
    #         ends at zero we quit.
    #
    def rangeCmd( self,cmd ):
        cmd.rangeIter -= 1
        if cmd.rangeIter >= 0:
            return True
        else:
            return False

    #
    # frontIsBlocked - detemine if the way forward for Karel is blocked
    #
    def frontIsBlocked(self):
        return not self.frontIsClear()
    
    #
    # leftIsBlocked - Determine if the way to the left is blocked
    #
    def leftIsBlocked(self):
        return not self.leftIsClear()
    
    #
    # rightIsBlocked - Determine if the way to the right is blocked
    #
    def rightIsBlocked(self):
        return not self.rightIsClear()
    
    #
    # ballsPresent - Determine if Karel is standing on one or more balls!
    #
    def ballsPresent(self):
        for ball in self.balls:
            if (ball.x == self.karel.x) and (ball.y == self.karel.y):
                return True
        return False
    
    #
    # noBallsPresent - Determine if Karel is NOT standing on one or more balls
    # 
    def noBallsPresent(self):
        return not self.ballsPresent()
    
    #
    # facingNorth - is Karel facing North?
    #
    def facingNorth(self):
        return self.karel.direction == NORTH
    
        #
    # facingNorth - is Karel facing North?
    #
    def facingEast(self):
        return self.karel.direction == EAST
    
        #
    # facingNorth - is Karel facing North?
    #
    def facingSouth(self):
        return self.karel.direction == SOUTH
    
        #
    # facingNorth - is Karel facing North?
    #
    def facingWest(self):
        return self.karel.direction == WEST
    
    #
    # whileCmd - A while loop.
    #
    # While the condition we hit is true, continue until it is false
    #
    def whileCmd(self,whileLoop):
        for cmd in whileLoop:
            if debugWhile:
                print( cmd )
            if cmd.loopCondition:
                result = self.executeCondition( cmd )
                if result == False:
                    break
            else:
                self.executeCommand( cmd )

    #
    # forCmd - A for loop.
    #
    # Like a normal loop, continue running until the condition fails.
    # In this case the one and only condition supported is "range"
    #
    def forCmd( self, forloop ):
        firstTime = True
        for cmd in forloop:
            if firstTime and (cmd.cmd == CMD_RANGE):
                cmd.resetRange()
                firstTime = False
            if cmd.loopCondition:
                result = self.executeCondition( cmd )
                if result == False:
                    break
            else:
                self.executeCommand( cmd )

    #
    # ifCmd - The if statement.
    #
    # An if statement is different in that we have the if and a condition,
    # if that condition is true, we excute the "true" portion of the if,
    # otherwise we execute the "false" portion.
    # 
    def ifCmd( self, ifbody ):
        cmd = ifbody.getFirst()
        if cmd.condition:
            result = self.executeCondition( cmd )
            if result == False:
                ifbody.switchToElse()
                
        for cmd in ifbody:
            self.executeCommand( cmd )

    #
    # elseCmd - This is a do nothing command
    #
    # This is a place holder, as we should never see an else as
    # the IF command stores both the "true" and "false" body
    #
    def elseCmd( self, elseBody ):
        pass
    
    #
    # functionCmd - Execute the function command...
    #
    def functionCmd( self, funcBody):
        if funcBody.isDefinition:
            funcBody.isDefinition = False
        else:
            for cmd in funcBody:
                self.executeCommand( cmd )

#
# setupWorld - Setup everything we need to run Karel in his world
#
def setupWorld():
    try:
        print( "Setting up..." )
        karel = Karel(NORTH)
        board = World(karel)
        program = Program( "newCmd.txt" )
        if debugCode: program.printProgram( program.instructions)
        board.setupProgram( program )
        return board
        
    except Exception as e:
        import sys
        handleException( e )
        sys.print_exception( e )

#
# executeProgram - Execute the program
#
# Execute the code, if there is an error, make sure we report that
# problem.
#
def executeProgram(board):
    try:
        print( "Starting program..." )
        board.executeProgram()
        
    except Exception as e:
        board.handleCrash( e )

#
# main - The main program
#
def main():
    board = setupWorld()
    if not board is None:
        executeProgram(board)

main()
time.sleep(10)
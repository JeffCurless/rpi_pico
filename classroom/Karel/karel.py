import time
import random

from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from machine import Pin

scaleFactor = 2
NORTH = 0
EAST  = 1
SOUTH = 2
WEST  = 3

debugDraw  = False
debugKarel = True
debugBall  = True

BETWEEN  = 15  # 21,22 are good
START    = BETWEEN//2
BALLSIZE = 6

led = RGBLED(6, 7, 8)
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led.set_rgb(0,0,0)
#
# Karel Class... Karel is a dog that wanders around the room, based on how he is programmed.
#
class Karel:
    def __init__(self,direct):
        self.x = START
        self.y = START
        self.direction = direct
        self.world_width = 0
        self.world_height = 0
    
    def setup( self, width, height ):
        self.world_width = width
        self.world_height = height
        
    def canMove(self,x,y):
        if (x >= START) and (x < self.world_width):
            if (y >= START) and (y < self.world_height):
                self.x = x
                self.y = y
                return
        raise Exception( "Karel hit a wall!" )
    
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
            print( "D: %d (%3d,%3d)" % (self.direction,self.x, self.y) )
            
    def turnRight(self):
        self.direction = self.direction + 1
        if self.direction > WEST:
            self.direction = 0
        if debugKarel:
            print( "D: %d (%3d,%3d)" % (self.direction,self.x, self.y))

#
# Ball - Sometimes Karel likes to play with a ball!
# 
class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#
# The world that Karel lives in
#
class World:
    def __init__( self, karel ):
        self.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
        self.display.set_backlight(0.8)
        self.width, self.height = self.display.get_bounds()
        self.background = self.display.create_pen( 0, 0, 0 )
        self.error      = self.display.create_pen( 0, 255, 0 )
        self.white      = self.display.create_pen( 255,255,255 )
        self.red        = self.display.create_pen( 255,0,0 )
        self.ballpen    = self.display.create_pen( 255,255, 0 )
        self.karel      = karel
        self.balls      = []
        
        self.karel.setup( self.width, self.height )
        self.display.set_pen( self.background )
        self.display.clear()
        self.drawBoard()
 
    def drawKarel( self ):
        global debugKarel
        self.display.set_pen( self.red )        
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
            print( "D: %d ( %3d, %3d ), (%3d, %3d), (%3d, %3d)" % (self.karel.direction,x1,y1,x2,y2,x3,y3))
        self.display.triangle( x1, y1, x2, y2, x3, y3 )
        
    def drawBalls( self ):
        for ball in self.balls:
            self.display.set_pen( self.ballpen )
            self.display.circle( ball.x, ball.x, BALLSIZE )
            
    def drawBackground( self ):
        self.display.set_pen( self.background )
        self.display.clear()
        self.display.set_pen( self.white )
        for h in range( START, self.height, BETWEEN ):
            for w in range( START, self.width, BETWEEN ):
                self.display.circle( w, h, 1 )
        
    def drawBoard(self):
        self.drawBackground()
        self.drawBalls()
        self.drawKarel()
        self.display.update()
        
    def testKarel(self):
        for j in range(4):
            board.turnRight()
            while( board.frontIsClear() ):
                board.move()
        board.turnRight()
        board.dropBall()
        board.move()
        board.turnRight()
        board.turnRight()
        board.move()
        if board.ballsPresent():
            board.takeBall()

    def handleCrash(self, e):
        self.display.set_pen( self.background )
        self.display.clear()
        width = self.display.measure_text( str(e), scaleFactor )
        textx = 0 #(self.width - width)//2
        texty = 0
        self.display.set_pen( self.error )
        self.display.text( str(e), textx, texty, self.width, scale=scaleFactor )
        self.display.update()
        print( e )
        
    #
    # All Karel functions are listed below.  Note that some will call and update the karel object,
    # others will add or remove from the balls object.  Anything that involves changing how the
    # world looks should result in a one second pause...
    #
    
    #
    # move - Called when we want to move Karel.  This function actually tells karel to move, and
    #        then we draw karel in the world, and sleep for a little..
    # 
    def move(self):
        self.karel.move()
        self.drawBoard()
        time.sleep(1)
        
    #
    # turnRight - Called when we want to turn Karel.  This function actually tells karel to turn, and
    #             then we draw karel in the world, and sleep for a little..
    # 
    def turnRight(self):
        self.karel.turnRight()
        self.drawBoard()
        time.sleep(1)
        
    #
    # dropBall -  Drop a ball for Karel.  We drop the ball directly where Karel is, and he can later
    #             pick it up.  Note that we are doing nothing to make storing the balls efficiently
    #             as we assume that no will will create a huge number of balls... if they do it will
    #             be slow to collect them all.
    #
    def dropBall(self):
        ball = Ball( self.karel.x, self.karel.y )
        if debugBall:
            print( "Drop (%3d,%3d)" % (ball.x,ball.y))
        self.balls.append( ball )
        self.drawBoard()
        time.sleep(1)
        
    #
    # takeBall - Allow Karel to take a ball if he is standing on it...  If there is no ball preset,
    #            he will generate a exception and the program ends
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
        time.sleep(1)
        
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
    # frontIsBlocked - detemine if the way forward for Karel is blocked
    #
    def frontIsBlocked(self):
        return not self.frontIsClear()
    
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
        
try:
    karel = Karel(NORTH)
    board = World(karel)
    board.testKarel()
    
except Exception as e:
    board.handleCrash( e )
    

        
        
        
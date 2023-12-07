import os
import gc
import time
import sys
import machine
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
from machine import Pin

APPDIR  = "/apps"
X_DELTA = 5
Y_DELTA = 6
XSTART  = 15
YSTART  = 0
YOFFSET = 15

BUTTON_A = 12
BUTTON_B = 13
BUTTON_X = 14
BUTTON_Y = 15

button_a = Button(BUTTON_A,invert=True)
button_b = Button(BUTTON_B,invert=True)
button_x = Button(BUTTON_X,invert=True)
button_y = Button(BUTTON_Y,invert=True)

BUTTONS = [button_a,button_b,button_x,button_y]

#
# Display - A class that creates a small dialog box for selecting and item from
# a list
#
class DialogBox:
    def __init__(self):
        self.display  = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0, pen_type=PEN_P8)
        self.display.set_backlight(1.0)
        self.width, self.height = self.display.get_bounds()
        self.TEXT     = self.display.create_pen( 0, 255, 0 )
        self.BG       = self.display.create_pen( 0, 0, 0 )

        self.messages = []
        self.index    = 0
        self.clear()
        self.update()
        
    def clear(self):
        self.display.set_pen( self.BG )
        self.display.clear()
        
    def update(self):
        self.display.update()
        
    def addItem(self, text ):
        self.messages.append(text)

    def displayMenu( self ):
        self.clear()
        x = XSTART
        y = YSTART
        self.display.set_pen( self.TEXT )
        for index in range(len(self.messages)):
            item = self.messages[index]
            if( index == self.index ):
                self.display.circle( X_DELTA, y+Y_DELTA, 4 )
            self.display.text( item, x, y, self.width )
            y += YOFFSET
        self.display.update()
        
    def displayMessage( self, text ):
        self.clear()
        x = XSTART
        y = YSTART
        self.display.set_pen(self.TEXT)
        self.display.text( text, x, y, self.width )
        self.display.update()
        
    def selector(self):
        noFileSelected = True
        self.displayMenu()
        while noFileSelected:
            if button_a.read():
                self.index -= 1
                if self.index < 0:
                    self.index = 0
                self.displayMenu()
            elif button_b.read():
                self.index += 1
                if self.index >= len(self.messages):
                    self.index = len(self.messages)-1
                self.displayMenu()
            elif button_x.read():
                print( "X" )
            elif button_y.read():
                noFileSelected = False
            time.sleep( 0.1 )
        return self.messages[self.index]
    
    def pressedAny(self):
        for button in BUTTONS:
            print( f"button.pin.value() = {button.pin} : {button.pin.value()}" )
            if button.raw():
                return True
        return False
    
    def waitForButtonRelease(self):
        while self.pressedAny():
            time.sleep(0.01)

def launch( app ):
    gc.collect()

    def quit_to_launcher(pin):
        a_pressed = False
        b_pressed = False
        if button_a.raw():
            a_pressed = True
        if button_b.raw():
            b_pressed = True
        if a_pressed or b_pressed:
            print( f"A = {a_pressed} B = {b_pressed}" )
        if a_pressed and b_pressed:
            machine.reset()

    button_a.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=quit_to_launcher)
    button_x.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=quit_to_launcher)

    try:
        print( f"Attemping to load {app}" )
        __import__(app)
    except Exception as e:
        print( e )
    
    machine.reset()
    
def getAppList():
    files = [name[:-3] for name in os.listdir(APPDIR)
             if name.endswith('.py') and name != 'main.py']
    return files  
    
def main():
    dialog = DialogBox()
    files = getAppList()
    for file in files:
        dialog.addItem( file )
        
    item = dialog.selector()
    dialog.displayMessage( f"Loading {item}..." )
    app = f"{APPDIR}/{item}"
    
    dialog.waitForButtonRelease()
    gc.collect()
    launch( app )
    
main()

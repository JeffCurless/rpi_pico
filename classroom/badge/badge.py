# This example shows you a simple, non-interrupt way of reading Pico Inky Pack's buttons with a loop that checks to see if buttons are pressed.

import time
import gc
import os
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec

PANEL_DISPLAY_TIME = 10
BUTTON_CHECK_TIME  = 0.1
SWITCH_PANEL_COUNT = PANEL_DISPLAY_TIME // BUTTON_CHECK_TIME

panel = 0
currentUser = "/user/user.jpg"

#
# Setup the display, need a specific one for the eINK display we use
#
display = PicoGraphics(display=DISPLAY_INKY_PACK)

# you can change the update speed here!
# it goes from 0 (slowest) to 3 (fastest)
display.set_update_speed(1)
display.set_font("serif")
display.set_pen(0)

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

#
# Does a file exist?
#
def fileExists( filename ):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False

# set up
width,height = display.get_bounds()

#
# Given a filename, display it on screen
#
def displayFile( file ):
    print( "Showing file " + file )
    display.set_pen(0)
    jpeg = jpegdec.JPEG(display)
    try:
        jpeg.open_file( file )
        jpeg.decode(0,0,jpegdec.JPEG_SCALE_FULL)
    except Exception as inst:
        print( type(inst))
        print( inst.args )
        print( inst )
    display.update()
    gc.collect()
    #print( "Free: " + str(gc.mem_free()) )
    time.sleep(BUTTON_CHECK_TIME)
    
#
# Display the current panel.  When called anything that needs to be initialized is
# setup, then we return a function that is to be called to change the panel number
# and display it.  This is a closuer.
#
def setupPanel():
    panel = 0
    def innerFunction():
        nonlocal panel
        global currentUser
        found = False
        
        while not found:
            if panel == 0:
                displayFile( currentUser )
                panel += 1
                found = True
            else:
                file = "/panels/panel" + str(panel) + ".jpg"
                if fileExists( file ):
                    displayFile( file )
                    found = True
                    panel += 1
                else:
                    panel = 0
                    
    return innerFunction

#
# Setup the display
#
showPanel = setupPanel()
showPanel()
count = 0
user = 0
autoSwitch = True
while True:
    if button_a.read():              # Switch between users
        user += 1
        currentUser = "/user/user" + str(user) + ".jpg"
        if not fileExists( currentUser ):
            user = 0
            currentUser = "/user/user.jpg"
        displayFile( currentUser )
        count = 0
        autoSwitch = False
    elif button_b.read():            # Restart panel switching
        count = 0
        autoSwitch = True
    elif button_c.read():            # Move on to the next panel
        showPanel()
        autoSwitch = True
        count = 0
    elif autoSwitch:
        count += 1
        if count >= SWITCH_PANEL_COUNT:
            showPanel()
            count = 0
    time.sleep(BUTTON_CHECK_TIME)  # this number is how frequently the Pico checks for button presses

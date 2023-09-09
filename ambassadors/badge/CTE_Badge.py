#
# This code was designed to run on the Pimoroni Badger2040W
# 
import gc
import os
import time
import math
import badger2040
import json
import jpegdec

state = { 
          "panel": 0,                        # Which panel do we display
          "user": 0,                         # Which user do we display
          "showUser": True,                  # Are we supposed to show the User or a Panel?
          "autoSwitch": True }               # Are we in autoswitch mode?

#
# Save our current state
#
def saveState( app, data ):
    print( "saveState( " + app + ", " + str(data) + ")" )
    try:
        with open("/state/{}.json".format(app),"w") as f:
            f.write(json.dumps(data))
            f.flush()
    except OSError:
        import os
        try:
            os.stat("/state")
        except OSError:
            os.mkdir( "/state" )
            saveState( app, data )
        
#
# This function obtains our current state
#
def loadState( app, defaults ):
    try:
        data = json.loads(open("/state/{}.json".format(app), "r").read())
        if type(data) is dict:
            defaults.update(data)
            print( "loadState( " + app + ", " + str(defaults) + ")" )
            return True
    except (OSError,ValueError):
        pass
    
    print( "state does not exist, creating the defaults..." )
    saveState( app, defaults )
    return False

#
# Did we restart based on being woken up by a button?  If so, and that button was the up button
# reset back to the original settings
#
if badger2040.pressed_to_wake(badger2040.BUTTON_UP):
    woken_by_button = badger2040.woken_by_button()  # Must be done before we clear_pressed_to_wake
    badger2040.reset_pressed_to_wake()
    saveState( "CTEBadge", state )
else:
    loadState( "CTEBadge", state )

display = badger2040.Badger2040()

#
# Set the I'm Currently on power LED brighness (0->255)
#
display.led(64)

jpeg = jpegdec.JPEG(display.display)
# set up
width,height = display.get_bounds()

#
# Does a file exist?
#
def fileExists( filename ):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False
    
#
# Given a filename, display it on screen
#
def displayFile( file ):
    print( "Showing file " + file )
    display.set_pen(0)
    try:
        jpeg.open_file( file )
        jpeg.decode(0,0,jpegdec.JPEG_SCALE_FULL)
    except Exception as inst:
        print( type(inst))
        print( inst.args )
        print( inst )
    display.update()
    gc.collect()
    print( "Free: " + str(gc.mem_free()) )

#
# Display the current panel.  This is done by checking to see what our current state is
# and displaying the proper panel, or if its time, the user panel again.
#
def showPanel():
    global state
    found  = False
    while not found:
        if state["showUser"]:
            file = "/user/user" + str(state["user"]) + ".jpg"
            displayFile( file )
            state["showUser"] = False
            found  = True
        else:
            file = "/panels/panel" + str(state["panel"]) + ".jpg"
            if fileExists( file ):
                displayFile( file )
                found = True
                state["panel"] += 1
                state["showUser"] = True
            else:
                state["panel"] = 0
    saveState( "CTEBadge", state )

#
# Wait until someone releases the button they pressed
#
def wait_for_user_to_release_buttons():
    while display.pressed_any():
        time.sleep(0.01)

#
# Select the user that we wish to display when we get there...
#
def selectUser():
    global state
    
    state["user"] += 1
    file = "/user/user" + str(state["user"]) + ".jpg"
    if not fileExists( file ):
        state["user"] = 0
        file = "/user/user0.jpg"

    #
    # Update the display
    #
    displayFile( file )
    
    #
    # Update the state file
    #
    state["autoSwitch"]  = False
    saveState( "CTEBadge", state )
    
#
# Restart the automatic screen updates
#
def restartAutoSwitch():
    global state
    state["autoSwitch"] = True
    saveState( "CTEBadge", state )
    
#
# Manually move on to the next panel
#
def manualMove():
    global state
    
    state["autoSwitch"] = True
    showPanel()
    
#
# Given a specific button press, decode and handle the function call
#
def button(pin):
    if pin == badger2040.BUTTON_A:  # Switch between users
        selectUser()
    elif pin == badger2040.BUTTON_B:  # Resart Panel Switching
        restartAutoSwitch()
    elif pin == badger2040.BUTTON_C:  # Move on to next panel
        manualMove()
    elif pin == badger2040.BUTTON_UP:
        print( "Button Up" )
    elif pin == badger2040.BUTTON_DOWN:
        print( "Button Down" )
    wait_for_user_to_release_buttons()

# Start executing code now...

display.set_update_speed(badger2040.UPDATE_MEDIUM)


while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()
    
    if display.pressed(badger2040.BUTTON_A):
        button(badger2040.BUTTON_A)
    elif display.pressed(badger2040.BUTTON_B):
        button(badger2040.BUTTON_B)
    elif display.pressed(badger2040.BUTTON_C):
        button(badger2040.BUTTON_C)
    elif display.pressed(badger2040.BUTTON_UP):
        button(badger2040.BUTTON_UP)
    elif display.pressed(badger2040.BUTTON_DOWN):
        button(badger2040.BUTTON_DOWN)
    elif state["autoSwitch"]:
        showPanel()

    badger2040.sleep_for( 1 )  # Sleep for 1 minute
    
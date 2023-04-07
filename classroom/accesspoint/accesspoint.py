import network
import socket
import time
import gc
import secret

from machine import Pin
import uasyncio as asyncio

onboard = Pin( 'LED', Pin.OUT, value=0 )

ssid     = secret.SSID
password = secret.PASSWORD
channel  = secret.CHANNEL
uname    = ""

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title></head>
    <body><h1=Pico W></h1>
        <p>%s</p>
        <p>Username: %s</p>
    </body>
</html>
"""

ap = network.WLAN( network.AP_IF )

#
# Create a soft access point for connecting PICO's in an environment where we have no
# network, or cannot be put on the network for security reasons.  Note that this code
# creates an access point, but it does NOT generate a connetion to the internet.  
#
def create_ap():
    ap.active(False)
    ap.config(essid=ssid, password=password, channel=channel,pm=0xa11140)
    ap.active(True)
    while ap.active() == False:
        pass

    print('Connection is successful, Server IP: ' + str(ap.ifconfig()[0]) )
    print('Operating on channel : ' + str(ap.config('channel')) )
    print('Transmission Power :' + str(ap.config('txpower')))

#
# Asynchronous function that is called whenever a client attempts to connect to our
# server.  Our job is to process the request as quickly as possible, and return a
# message to the caller via a write.
#
async def serve_client( reader, writer ):
    global uname
    print( "Client Connected" )
    
    request_line = await reader.readline()
    print( "Request: ", request_line )
    
    # Not interested in HTTP headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line)
    led_on = request.find( '/light/on' )
    led_off = request.find( '/light/off' )
    username = request.find( '/badge?username=' )
    #print( 'led_on = ' + str( led_on ))
    #print( 'led_off = ' + str( led_off ))
    #print( 'username = ' + str( username ))
    
    stateis = ""
    if led_on == 6:
        print( "led on" )
        onboard.value(1)
        stateis = "LED is ON"
        
    if led_off == 6:
        print( "led off" )
        onboard.value(0)
        stateis = "LED is OFF"
        
    if username == 6:
        start = request.index('"')
        end   = request.index('"',start+1)
        uname = request[start+1:end]
        print( "Username is " + uname )
        
    response = html % (stateis, uname)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print( "Client disconnected" )
    
#
# Our main execution loop.  If there was anything we wanted to do, i.e. monitor something,
# or display something this is where we could add additional code to help handle the
# day to day work.
#
async def main():
    print( "Setting up Access point..." )
    create_ap()
    
    print( "Setting up connection handler..." )
    asyncio.create_task( asyncio.start_server(serve_client, "0.0.0.0", 80 ))
    
    while True:
        await asyncio.sleep( 1 )

#
# And start things off.  We want to make sure that when we terminate we close down things
# properly and handle the asyncio close out.
#
try:
    asyncio.run( main() )
finally:
    asyncio.new_event_loop()
    

import network
import urequests as request
import time
import secret

# Fill in your router's ssid and password here.
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect( secret.SSID, secret.PASSWORD )

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break;
    max_wait -= 1
    print( "Waiting for connection..." )
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed with error:' + str( wlan.status() ) )
else:
    print( "Connected.")
    status = wlan.ifconfig()
    print( "ifconfig = " + str(status) )
    
r=request.get( 'http://192.168.4.1:80/badge?username="curless"')
print( "request status = " + str( r.status_code ) )
print( "request test = " + str( r.text ) )
r.close()
        
try:
    while True:
        r = request.get( "http://192.168.4.1:80/light/on" )
        print( "request status = " + str(r.status_code) )
        print( "request text  = " + str(r.text) )
        r.close()
        time.sleep( 1 )
        r = request.get( "http://192.168.4.1:80/light/off" )
        print( "request status = " + str(r.status_code) )
        print( "request text  = " + str(r.text) )
        r.close()
        time.sleep( 1 )

finally:
    wlan.disconnect()
    print( "Executed finally" )
    

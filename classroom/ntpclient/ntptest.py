import network
import socket
import time
import struct
import WIFI

from ntptime import NTPTime


host = "pool.ntp.org"
ssid = WIFI.SSID
password = WIFI.PASSWORD

#
# Print out a formated time
#
def print_time( tt, msg = ""):
    tt = time.gmtime()
    print( f'{msg}{tt[1]:0>2d}/{tt[2]:0>2d}/{tt[0]} {tt[3]:0>2d}:{tt[4]:0>2d}:{tt[5]:0>2d}' )

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

#
# Set current hour to some bogus value to force initialization on first pass
# 
currentHour = 24

ntp = NTPTime( host )


try:
    
    while True:
        tt = time.localtime()
        if( tt[3] != currentHour ):
            print_time(tt, msg="Old Time: ")
            ntp.setTime()
            tt = time.localtime()
            currentHour = tt[3]
        print_time(tt)
        time.sleep(1)
        
finally:
    print( "Executed finally" )
    wlan.close()
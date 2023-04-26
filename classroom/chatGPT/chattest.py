import network
import time
from chatgpt import chatGPT
import WIFI
import apikey

#
# Setup to test chatGPT
#
ssid = WIFI.SSID
password = WIFI.PASSWORD

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


chat = chatGPT( apikey.KEY, 2048 )
answer = chat.askQuestion( "In the style of a sherlock holmes story, write a chapter about a new case" )

print( answer )
wlan.disconnect()

    




import machine
import network
import socket
import time
import struct

#
# Class used to obtain time from an NTP server
#
class NTPTime:
    def __init__( self, host ):
        self.ntpHost = host
        self.NTP_DELTA = 2208988800
        
    def getTime(self):
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo( self.ntpHost, 123 )[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(3)
            result = s.sendto(NTP_QUERY, addr)
            message = s.recv(48)
        finally:
            s.close()
        #
        # Unpack network (big-endian) into an unsigned integer
        #
        value = struct.unpack("!I", message[40:44])[0]
        t = value - self.NTP_DELTA
        tm = time.gmtime(t)
        return tm
    
    def setTime(self):
        tm = self.getTime()
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6]+1, tm[3], tm[4], tm[5], 0 ))
        

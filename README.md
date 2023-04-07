# rpi_pico
Collection of programs for the Raspberry Pi Pico/PicoW

# Classroom
## Access Point

**accesspoint.py**
>Contains a simple project that generates an access point, and webserver.  The access point will act as a DHCP server so it can give out network addresses in an environment where there is no other network access, or network access to the internet is restricted.

**get.py**

>A simple test program that generates a connection to the access point and verifies data transfers

## ntpclient

**ntpclient.py**

>A Class that obtains the time from a network time server, if there is an already established network connection.

**ntptest.py**

>A simgple test program to test ntpclient code.

# rpi_pico
Collection of programs for the Raspberry Pi Pico/PicoW

# Classroom
## Access Point

**accesspoint.py**

Contains a simple project that generates an access point, and webserver.  The access point will act as a DHCP server so it can give out network addresses in an environment where there is no other network access, or network access to the internet is restricted.

**get.py**

A simple test program that generates a connection to the access point and verifies data transfers

## ntpclient

**ntpclient.py**

A Class that obtains the time from a network time server, if there is an already established network connection.

**ntptest.py**

A simgple test program to test ntpclient code.

## chatGPT

**chatgpt.py**

A class that communicates with chatGPT.  This assumes there is an already established network.  

**chattest.py**

A small tests program that helps test the chatGPT object.

## Badge

++badge.py++

Is a small app that updates an inky eInk display from Pimoroni.  The code simply displays image /user/user.jpg, and then starts showing panels from /panels/ starting with panel1.jpg, and continues on until there are no more panel##.jpg files.  When this occurs it goes back to the original user.  This code is being used for a badge for my CTE ambassadors at school.  Each student ambassador has a badge, and it rotates betweehn their name and some information about the school etc.

## prange

++prange.py++

A simple iterator class.  In the file is also a function isprime, that uses the prange iterator to determine if the number is prime or not.  While this iterator is not the best mechansim, as it has very large memory reuirements for very large numbers it does show how an iterator can work, and was used in a class discussing for loops and how we calculate prime numbers.


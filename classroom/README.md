# Access Point

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

**badge.py**

## prange

**prange.py**

A simple iterator class.  In the file is also a function isprime, that uses the prange iterator to determine if the number is prime or not.  While this iterator is not the best mechansim, as it has very large memory reuirements for very large numbers it does show how an iterator can work, and was used in a class discussing for loops and how we calculate prime numbers.

## tictactoe
**tictactoe.py**

A simple tictactoe program for the pico with a pico_display.  Could be ported over to any python environment.  One suggestion for porting would be to convert the graphics over to text displays, and instead of button moves, simply have the player select a number for a blank spot on the board.


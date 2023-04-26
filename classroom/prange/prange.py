import math

class prange:
    """
    prange is a class that provides a range of prime numbers between 2 and the
    number provided.  These prime numbers can be used to special cases determining if
    a number is prime or not with minimum division (i.e. only checking with primes).
    
    Note this is done with a static set of primes, and we need to generate them all, this
    could be done by determining the next prime in __next__
    """
    def __init__(self,x):
        x = int(math.sqrt(x))+1
        thing = [True] * x
        self.primes = []
        self.index = 0
        for i in range(2,x):
            if thing[i]:
                self.primes.append(i)
                for j in range(i*2,x,i):
                    thing[j] = False
        self.show()
    def __iter__(self):
        return self
    def __next__(self):
        if self.index < len(self.primes):
            item = self.primes[self.index]
            self.index += 1
            return item
        raise StopIteration
    def show(self):
        print( self.primes )

def isprime( x ):
    if x == 0 or x == 1:
        return False
    for i in prange( x ):
        if (x%i) == 0:
            print( str(x) + " is not prime, divisible by " + str(i) )
            return False
    print( str(x) + " is a prime" )
    return True

isprime( 10597)

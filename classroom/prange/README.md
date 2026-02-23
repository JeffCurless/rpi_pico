# prange — Prime Iterator

A teaching example for Python iterators and prime number detection using the Sieve of Eratosthenes.

## Files

### prange.py

**`prange(x)`** class — implements the iterator protocol to generate all prime numbers up to √x.

**`isprime(x)`** function — uses `prange` to test whether `x` is prime.

## How It Works

`prange` applies the Sieve of Eratosthenes to find all primes up to √x, then tests divisibility. While not memory-efficient for very large numbers (it stores the full sieve), it demonstrates clearly how iterators work and how prime detection can be implemented using one.

## Running

Pure Python — no hardware or Pimoroni libraries required:

```python
from prange import prange, isprime

for p in prange(100):
    print(p)          # prints all primes up to √100 = 10

print(isprime(17))    # True
print(isprime(18))    # False
```

## Parent

See [classroom/](../README.md) for other classroom projects.

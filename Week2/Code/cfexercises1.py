#!/usr/bin/env python3

"""Some numerical functions"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##

def foo_1(x):
    """Divide the input by 2"""
    return x ** 0.5

def foo_2(x, y):
    """Return the larger of the two inputs
    (or the latter if they are equal)."""
    if x > y:
        return x
    return y

def foo_3(x, y, z):
    if x > y:
        # Swap their values
        tmp = y
        y = x
        x = tmp
    if y > z:
        # Swap their values
        tmp = z
        z = y
        y = tmp
    return [x, y, z]

def foo_4(x):
    """Calculate the factorial of the input."""
    result = 1
    for i in range(1, x + 1):
        result = result * i
    return result

def foo_5(x):
    """A recursive function that calculates the factorial of x"""
    if x == 1:
        return 1
    return x * foo_5(x - 1)

def foo_6(x):
    """Calculate the factorial of x in a different way"""
    facto = 1
    while x >= 1:
        facto = facto * x
        x = x - 1
    return facto

def main(argv):
    """Run functions"""
    print(foo_1(4))
    print(foo_2(3, 4))
    print(foo_3(1, 2, 3))
    print(foo_4(3))
    print(foo_5(4))
    print(foo_6(3))
    return 0

if __name__ == '__main__':
    """Run as script"""
    status = main(sys.argv)
    sys.exit(status)

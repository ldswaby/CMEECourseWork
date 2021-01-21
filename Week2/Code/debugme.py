#!/urs/bin/env python3

"""Experimenting with debugging"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

def buggyfunc(x):
    """Recursively divide x by all natural numbers < x
    """
    y = x
    for i in range(x):
        y -= 1
        if y == 0:
            break
        z = x/y
    return z

buggyfunc(20)

#!/urs/bin/env python3

"""Experimenting with debugging"""

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
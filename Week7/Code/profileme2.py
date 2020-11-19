#!/usr/bin/env python3

"""More profiling code in python"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import numpy as np
import timeit

## Functions ##
def my_squares(iters):
    """Returns list of squares range of integers using list comprehension.
    """
    #out = [i ** 2 for i in range(iters)]  # using list comprehension
    out = np.arange(iters)**2
    return out

def my_join(iters, string):
    """Joins string by ', ' iters times using explicit string concatenation
    """
    out = ''
    for i in range(iters):
        out += ", " + string
    return out

def run_my_funcs(x,y):
    """Runs preceding functions with given args.
    """
    print(x,y)
    my_squares(x)
    my_join(x,y)
    return 0

run_my_funcs(10000000, "My string")
#!/usr/bin/env python3

"""Profiling code in python"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##
def my_squares(iters):
    """Returns list of squares of range of integers.
    """
    out = []
    for i in range(iters):
        out.append(i ** 2)
    return out

def my_join(iters, string):
    """Joins string by ', ' iters times using .join()
    """
    out = ''
    for i in range(iters):
        out += string.join(", ")
    return out

def run_my_funcs(x,y):
    """Runs preceding functions with given args.
    """
    print(x,y)
    my_squares(x)
    my_join(x,y)
    return 0

def main():
    """Run functions
    """
    run_my_funcs(10000000,"My string")
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
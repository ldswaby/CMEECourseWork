#!/usr/bin/env python3

"""Quick profiling using the timeit and time modules"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys
import time
import timeit
from profileme import my_squares as my_squares_loops
from profileme2 import my_squares as my_squares_lc
from profileme import my_join as my_join_join
from profileme2 import my_join as my_join

## Functions ##
def main():
    """Compare run times of different string/list methods using time module
    """
    # loops vs. list comprehensions: which is faster?
    iters = 1000000
    start = time.time()
    my_squares_loops(iters)
    print("my_squares_loops takes %f s to run." % (time.time() - start))

    start = time.time()
    my_squares_lc(iters)
    print("my_squares_lc takes %f s to run." % (time.time() - start))

    # loops vs. the join method for strings: which is faster?
    mystring = "my string"
    start = time.time()
    my_join_join(iters, mystring)
    print("my_squares_loops takes %f s to run." % (time.time() - start))

    start = time.time()
    my_join(iters, mystring)
    print("my_squares_lc takes %f s to run." % (time.time() - start))

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)

#!/usr/bin/env python3

"""Groupwork: to do vectorize1 using Python"""

## Variables ##

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
__version__ = '0.0.1'

## Imports ##

import sys
import time
import numpy as np

## Functions ##


def SumALLElements(M):
    """Sum all elements of a matrix
    """
    Tot = 0
    Dimensions = np.shape(M)
    for i in range(0, Dimensions[0]):
        for j in range(0, Dimensions[1]):
            Tot += M[i, j]
    return Tot


def main():
    """Print the execution time of loop-based SumALLElements() and vectorized
    np.sum() functions.
    """
    M = np.random.rand(1000, 1000)

    start1 = time.time()
    SumALLElements(M)
    print("SumALLElements takes %f s to run" % (time.time() - start1))

    start2 = time.time()
    # print(np.sum(M))
    np.sum(M)
    print("np.sum takes %f s to run" % (time.time() - start2))

    return 0

## Main ##

if __name__ == '__main__':
    status = main()
    sys.exit(status)

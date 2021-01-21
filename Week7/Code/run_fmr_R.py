#!/usr/bin/env python3

"""Running R subprocess.os"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys
import subprocess

## Functions ##

def main():
    """Run main functions
    """
    # Run fmr.R
    p = subprocess.Popen(['Rscript', 'fmr.R'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # Print outputs and check for errors
    print(stdout.decode())

    if stderr.decode():
        print(f"{stderr.decode()}\nRUN FAILED")
    else:
        print("RUN SUCCESS")

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)

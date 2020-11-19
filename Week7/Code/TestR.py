#!/usr/bin/env python3

"""Test running R in Python with subprocess"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys
import subprocess

## Functions ##
def main():
    """Run main function
    """
    subprocess.Popen("Rscript --verbose TestR.R > ../Results/TestR.Rout 2> "
                     "../Results/TestR_errFile.Rout", shell=True).wait()

    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
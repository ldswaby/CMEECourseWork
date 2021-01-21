#!/usr/bin/env python3

"""Print profiles on Lotka-Volterra model scripts, taking a single numerical
argument specifying the number of lines of each profile output the user wants
printed to the command line"""

## Variables ##

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
__version__ = '0.0.1'

## Imports ##

import sys
import io
import pstats
import cProfile
import LV1, LV2, LV3, LV4

## Functions ##

def main(h=0):
    """Print profiles on Lotka-Volterra model scripts

    Arguments:
     - h: numerical argument specifying the number of lines of each profile
          output the user wants printed to the command line.

    Output:
     - Printed profiles to the command line.
    """
    ## Print profile for each file ##
    for file in [LV1, LV2, LV3, LV4]:
        pr = cProfile.Profile()  # allows profile formatting with no file out
        pr.enable()  # open profile
        file.main()  # run script
        pr.disable()  # close profile

        s = io.StringIO()  # create text stream

        # read profile results from file
        stats = pstats.Stats(pr, stream=s).sort_stats('cumulative')

        # remove extraneous paths from all the module names and only print head
        stats.strip_dirs().print_stats(h)

        print(f"Profiling '{file.__name__}':")
        print(s.getvalue())

    return 0

if __name__ == '__main__':
    # Check if optional profile output number of rows argument is provided
    if len(sys.argv) == 2:
        head = int(sys.argv[1])
        status = main(head)
    elif len(sys.argv) < 2:
        print('WARNING: no arguments parsed. Default used = 0.\n')
        status = main()
    else:
        print('WARNING: too many arguments parsed. Default used = 0.\n')
        status = main()

    sys.exit(status)

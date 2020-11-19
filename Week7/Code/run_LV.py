#!/usr/bin/env python3

"""Print profiles on Lotka-Volterra model scripts"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import cProfile, pstats, io
import LV1, LV2

## Print profile for each file ##
for file in [LV1, LV2]:
    pr = cProfile.Profile()  # allows profile formatting with no file out
    pr.enable()  # open profile
    file.main()  # run script
    pr.disable()  # close profile

    s = io.StringIO()  # create text stream

    # read profile results from file
    stats = pstats.Stats(pr, stream=s).sort_stats('cumulative')

    # remove extraneous paths from all the module names and only print head
    stats.strip_dirs().print_stats(0)

    print(f"Profiling '{file.__name__}':")
    print(s.getvalue())
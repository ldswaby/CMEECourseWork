#!/usr/bin/env python3

"""Calculate tree heights using Python and writes to csv. Accepts Two optional
arguments: file name, and output directory path."""

## Variables ##

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
__version__ = '0.0.1'

## Imports ##

import sys
import pandas as pd
import numpy as np

## Functions ##

def TreesHeight(degrees, dist):
    """This function calculates heights of trees given distance of each tree
    from its base and angle to its top, using  the trigonometric formula
    height = distance * tan(radians)

    Arguments:
     - degrees:   The angle of elevation of tree
     - dist:  The distance from base of tree (e.g., meters)

    Output:
     - The heights of the tree, same units as "distance"
    """
    radians = degrees * np.pi / 180
    height = dist * np.tan(radians)
    print(height)

    return height

def main(argv):
    """Writes tree height results to CSV file including the input file name in
    the output file name.
    """

    if len(argv) < 2:
        print("WARNING: no arguments parsed. Default filename used: "
              "'trees.csv'.\n")
        filename = "trees.csv"
        outdir = "../Data/"
    elif len(argv) == 2:
        filename = argv[1]
        outdir = "../Data/"
    elif len(argv) == 3:
        filename = argv[1]
        outdir = argv[2]  # Accept output directory path as second arg
    else:
        print("WARNING: too many arguments parsed.Default filename used: "
              "'trees.csv'.\n")
        filename = "trees.csv"
        outdir = "../Data/"

    filename_noExt = filename.split('/')[-1].split('.')[0]  # Assumes no full
                                                           # stops in filename

    save_name = "../Results/%s_treeheights_python.csv" % filename_noExt
    filepath = outdir + filename
    trees_data = pd.DataFrame(pd.read_csv(filepath))
    trees_data["Height"] = TreesHeight(trees_data["Angle.degrees"],
                                       trees_data["Distance.m"])
    
    # Save to csv
    trees_data.to_csv(save_name, sep=",", index=False)

    return 0

## Main ##

if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)

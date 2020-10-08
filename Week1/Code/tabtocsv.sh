#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: tabtocsv.sh
# Desc: substitute tabs in a file with commas
# Saves the output to a .csv file
# Arguments: 1 -> tab delimited file
# Date: Oct 2020

echo "Creating comma-delimited version of '${1##*/}'..."
cat $1 | tr -s "\t" "," >> ${1%%.*}.csv
# Change '>>' to '>' if you wish to have each run overwrite any 
# identically named files on output instead of appending to them.
echo "Done."
exit
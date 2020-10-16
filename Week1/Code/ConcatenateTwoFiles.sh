#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: ConcatenateTwoFiles.sh
# Desc: Concatenates two files
# Arguments: 3 -> 2 files, and new concatenated file path/name
# Date: Oct 2020

if (( $# != 3 )); then
	echo "ERROR: This script requires 3 arguments (2 filepaths and a name for \
the new file). You have provided $#." # How to wrap multi-line strings w. indent?
	exit
fi

cat $1 > $3
cat $2 >> $3
echo "Merged file is:"
cat $3
#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: ConcatenateTwoFiles.sh
# Desc: Concatenates two files
# Arguments: 1
# Date: Oct 2020

cat $1 > $3
cat $2 >> $3
echo "Merged file is:"
cat $3
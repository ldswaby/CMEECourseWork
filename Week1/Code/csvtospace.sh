#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: csvtospace.sh
# Desc: Takes a comma separated values and converts it to a space separated values file.
# Arguments: 2
# Date: Oct 2020

echo "Creating space-separated version of '${1##*/}'..."
cat $1 | tr -s "," " " >> $2
echo "Done!"
exit

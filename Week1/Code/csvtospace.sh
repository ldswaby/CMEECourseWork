#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: csvtospace.sh
# Desc: Takes a CSV file and creates a space-separated version
# Arguments: 2 -> A CSV file and the file path/name of new version
# Date: Oct 2020

if (( $# != 2 )) 
then
	echo "This script requires 2 arguments (a CSV file and a file \
path/name for new space-separated version). You have provided $#." 
	# How to wrap multi-line strings w. indent?
	exit
fi

echo "Creating space-separated version of '${1##*/}'..."
cat $1 | tr -s "," " " >> $2
echo "Done!"
exit

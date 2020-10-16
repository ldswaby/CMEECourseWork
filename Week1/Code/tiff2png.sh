#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: tiff2png.sh
# Desc: Converts .tif to .png files in the working directory
# Arguments: inf -> If 0 args are provided the script will convert all .tif 
# files in the cwd, otherwise it will convert any provided, skipping any 
# without a .tif extension.
# Date: Oct 2020

if (( $# == 0 )); then
	# Convert all .tif files in cwd
	for f in *.tif
    do
      	echo "\nConverting $f";
      	convert "$f" "$(basename "$f" .tif).png";
    done
else
	# Convert all specified files
	for f in "$@"
	do 
		# if filename doesn't end in '.tif' skip with an error message
		if [ ${f: -4} != ".tif" ]; then
			echo "\nERROR: File '$f' is not a .tif file."
			continue
		fi
		echo "\nConverting $f";
      	convert "$f" "$(basename "$f" .tif).png";
    done
fi

echo "\nDone!"
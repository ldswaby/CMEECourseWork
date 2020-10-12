#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: tiff2png.sh
# Desc: Converts .tif to .png files in the working directory
# Arguments: 1
# Date: Oct 2020

for f in *.tif;
    do
      echo "Converting $f";
      convert "$f" "$(basename "$f" .tif).jpg";
    done

echo "Done."
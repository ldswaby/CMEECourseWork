#!/bin/bash
# Author: Luke Swaby (lds20@ic.ac.uk), Jingkai Sun (ks3020@ic.ac.uk)
#         Acacia Tang (t.tang20@imperial.ac.uk), Dengku Tang (dengkui.tang20@imperial.ac.uk)
# Script: run_get_TreeHeight.sh
# Desc: run both R version and Python version of get_Treeheight script
# Arguments: none
# Date: Jan 2021

echo "Run get_TreeHeight.R and get_TreeHeight.py with an argument 'Trees.csv'"
Rscript get_TreeHeight.R Trees.csv
python3 get_TreeHeight.py Trees.csv
echo "Finished!"
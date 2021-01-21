#!/bin/bash
# Author: Luke Swaby (lds20@ic.ac.uk), Jingkai Sun (ks3020@ic.ac.uk)
#         Acacia Tang (t.tang20@imperial.ac.uk), Dengku Tang (dengkui.tang20@imperial.ac.uk)
# Script: run_vectorization.sh
# Desc: run both R version and Python version of 'Vectorize' script
# Arguments: none
# Date: Jan 2021

echo "The runtime for four vectorization scripts:"
echo "-----------------------The Vectorize1.R-----------------------"
Rscript Vectorize1.R
echo "-----------------------The Vectorize1.py-----------------------"
python3 Vectorize1.py
echo "-----------------------The Vectorize2.R-----------------------"
Rscript Vectorize2.R
echo "-----------------------The Vectorize2.py-----------------------"
python3 Vectorize2.py
echo "Done!"

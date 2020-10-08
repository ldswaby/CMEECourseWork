#!/bin/bash
# Author: Luke Swaby lds20@ic.ac.uk
# Script: CompileLaTex.sh
# Desc: Compiles LaTeX with bibtex
# Arguments: 1
# Date: Oct 2020

pdflatex $1
pdflatex $1
bibtex ${1%.*}
pdflatex $1
pdflatex $1
evince ${1%.*}.pdf

#Cleanup
rm *~
rm *.aux
rm *.dvi
rm *.log
rm *.nav
rm *.out
rm *.snm
rm *.toc
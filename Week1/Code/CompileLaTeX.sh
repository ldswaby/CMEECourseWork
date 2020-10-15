#!/bin/bash
# Author: Luke Swaby (lds20@ic.ac.uk)
# Script: CompileLaTex.sh
# Desc: Compiles LaTeX with bibtex. Can be operated from any dir so long as
# your .bib file is in your cwd. Note that pdf output will also be generated
# in your cwd.
# Arguments: 2 -> .tex filepath and .bib filepath
# Date: Oct 2020

#In case user is operating from separate directory
FILE=${1##*/}
BIB=${2##*/}

#Copy .bib file into cwd if not present
if ! [ -e "./$BIB" ];
then
	cp $2 ./
	copy=1
fi

#Functions
pdflatex $1
pdflatex $1
bibtex ${FILE%.*}
pdflatex $1
pdflatex $1
open ${FILE%.*}.pdf
#evince ${FILE%.*}.pdf

#Cleanup
rm *~
rm *.aux
rm *.dvi
rm *.log
rm *.nav
rm *.out
rm *.snm
rm *.toc
rm *.bbl
rm *.blg
if [ -n "$copy" ];
then
	rm $BIB
fi	


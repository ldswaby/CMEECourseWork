#!/bin/bash
# Author: Luke Swaby (lds20@ic.ac.uk)
# Script: CompileLaTex.sh
# Desc: Compiles LaTeX with bibtex. Note that pdf output will be generated
# in your cwd.
# Arguments: 3 -> .tex filepath (required), .bib filepath, and .pdf output 
# filepath.
# Date: Oct 2020

#Check inputs
if ! [[ $# == 1 || $# == 2 || $# == 3 ]]; then
  echo "ERROR: This script requires at least 1 argument (a .tex filepath) and \
at most 3 (.tex filepath, .pdf output filepath, and a .bib filepath, in that \
order). You have provided $#. \n\nNOTE:\n * If the third argument is omitted, \
the script will assume that your .bib file is in the cwd (your output will \
lack a bibliography if not).\n * If the second and third arguments are \
omitted, the script will assume that your .bib file is in the cwd and \
generate your output in the cwd."
  exit
fi
	
#Strip filename in case user is operating from separate directory
TEX=${1##*/}

#Check for .bib file and copy into cwd if not present
if [ -n "$3" ]; then
	BIB=${3##*/}
	if ! [ -e "./$BIB" ]; then
		cp $3 ./
		copy=1
	fi
fi

#Compile into pdf
pdflatex $1 > /dev/null 2>&1
echo "\n\nCOMPILING BIBLIOGRAPHY WITH BIBTEX...\n\n"
bibtex ${TEX%.*}
echo "\n\nCOMPILING PDF WITH CITATIONS...\n\n"
pdflatex $1 > /dev/null 2>&1
pdflatex $1

#Open pdf (renaming if requested)
if [ -n "$2" ]; then
	echo "\n\nRENAMING/OPENING FILE...\n\n"
	mv ${TEX%.*}.pdf $2
	open $2 #Mac
	#evince $3 #Linux
else
	echo "\n\nOPENING FILE...\n\n"
	open ${TEX%.*}.pdf #Mac
	#evince ${TEX%.*}.pdf #Linux
fi

#Cleanup
echo "CLEANING UP...\n\n"

rm *~ > /dev/null 2>&1
rm *.aux > /dev/null 2>&1
rm *.dvi > /dev/null 2>&1
rm *.log > /dev/null 2>&1
rm *.nav > /dev/null 2>&1
rm *.out > /dev/null 2>&1
rm *.snm > /dev/null 2>&1
rm *.toc > /dev/null 2>&1
rm *.bbl > /dev/null 2>&1
rm *.blg > /dev/null 2>&1
if [ -n "$copy" ];
then
	rm $BIB
fi		

echo "DONE!"
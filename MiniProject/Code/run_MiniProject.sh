# Author: Luke Swaby (lds20@ic.ac.uk)
# Script: CompileLaTex.sh
# Desc: Compiles LaTeX with bibtex. Note that pdf output will be generated
# in your cwd.
# Arguments: 3 -> .tex filepath (required), .bib filepath, and .pdf output 
# filepath.
# Date: Dec 2020

echo '\nCOMPILING PROJECT...\n'

Rscript DataPrep.R

python3 ModelFitting.py

Rscript PlotAnalyse.R

#pdflatex Report.tex > /dev/null 2>&1
#bibtex Report > /dev/null 2>&1
#pdflatex Report.tex > /dev/null 2>&1
#pdflatex Report.tex > /dev/null 2>&1

echo "\rCLEANING UP..."

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

echo '\rSUCCESS!'
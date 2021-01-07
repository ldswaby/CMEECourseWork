# Author: Luke Swaby (lds20@ic.ac.uk)
# Script: run_MiniProject.sh
# Desc: Compiles Computing Mini-Project
# Arguments: 0
# Date: Dec 2020

echo '\n%%%%%%%%%%%%%%%%%%%%%% COMPUTING MINI-PROJECT %%%%%%%%%%%%%%%%%%%%%%\n'

Rscript DataPrep.R

python3 ModelFitting.py

Rscript PlotAnalyse.R

# Compile project report
pdflatex Report.tex > /dev/null 2>&1
bibtex Report > /dev/null 2>&1
pdflatex Report.tex > /dev/null 2>&1
pdflatex Report.tex > /dev/null 2>&1

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

echo "\rOPENING REPORT..."
mv Report.pdf ../Writeup/
if [ "$(uname)" == "Darwin" ]
then
    open ../Writeup/Report.pdf # Mac
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]
then
    evince ../Writeup/Report.pdf # Linux
fi

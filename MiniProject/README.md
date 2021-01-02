# Computing Miniproject

This directory contains materials for the computing miniproject in the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

## Prerequisites

This project was developed on a Unix OS.

The following packages (with versions) are used in the project:
* R (4.0.3)
* Python (3.7.7)
* Jupyter-Notebook (6.1.4)

## Dependencies

### R
* `tidyverse` 
* `plyr` 
* `gridExtra`
* `grid`
* `scales`

### Python
* `numpy`
* `pandas`  
* `matplotlib`
* `lmfit`
* `smt`
* `statsmodels`

### LaTeX
* `agsm.bst` (bibliography style to be stored in Code directory - see [here](http://ftp.math.utah.edu/pub/tex/bibtex/agsm.bst))

### Jupyter Notebook
* IPython kernel
* R kernel (see [here](https://github.com/IRkernel/IRkernel))

## Structure and Usage

This directory contains the following folders:
* **Data**: contains CSV file containing the functional response data set — 
*CRat.csv*. (Modified versions of this file will also be placed here.)
* **Code**: contains all code scripts for the project (see below for details).
* **Results**: empty directory for plots and results files to be pushed into.
* **Writeup**: directory for the written report pdf and front page graphics.

## Scripts
1. [DataPrep.R](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/DataPrep.R)
2. [ModelFitting.py](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/ModelFitting.py)
3. [PlotAnalyse.R](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/PlotAnalyse.R)
4. [Report.tex](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/Report.tex)
5. [Frontpage.tex](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/Frontpage.tex)
6. [Biblio.bib](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/Biblio.bib)
7. [run_MiniProject.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/MiniProject/Code/run_MiniProject.sh)

### 1. DataPrep.R

A script for preparing the *CRat.csv* data for model fitting, filtering out unnecessary columns and problematic rows.

### 2. ModelFitting.py

Fits a cubic polynomial and C. S. Holling's type I, II, and III models to the functional response data set by least squares regression,
and prints fit statistics and parameter estimates to a separate CSV file.

### 3. PlotAnalyse.R

Imports results from the previous step and performs analysis of the Model fitting for the final report.

### 4. Report.tex

This .sh script assigns values to variables and shows how these values can be replaced during the running of the script. There are two separate scripts, one with strings and one with integers.

### 5. Frontpage.tex

The written report, written in LATEX.

### 6. Biblio.bib

Bibliography file for the written report.

### 7. run_MiniProject.sh

Runs/compiles the whole project. 

## Contact

Email: <lds20@ic.ac.uk>.
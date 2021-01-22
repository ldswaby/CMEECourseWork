# My CMEE Coursework Repository

This repository contains computing coursework for the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) at Imperial College London.

This repository is divided into weeks, with the directory for each week containing a combination of the following subdirectories:
* Data - contains data files used during the week.
* Code - contains all code scripts for the week.
* Results - empty directory for any results files to be pushed into if they exist.

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if any) being pushed into the *Results/* directory.

E.g.

```
$ sh Week1/Code/CountLines.sh Week1/Data/E.coli.fasta 
```
Each week's directory contains it's own README.md file detailing it's dependencies and a brief description of of each script.

## Table of Contents
1. [Week 1: Computing Bootcamp](https://github.com/ldswaby/CMEECourseWork/tree/master/Week1)
2. [Week 2: Python I](https://github.com/ldswaby/CMEECourseWork/tree/master/Week2)
3. [Week 3: R](https://github.com/ldswaby/CMEECourseWork/tree/master/Week3)
4. [Week 7: Python II](#7.Week-7-Python-II)
5. [Computing Mini-Project](https://github.com/ldswaby/CMEECourseWork/tree/master/MiniProject)

### Week 1: Computing Bootcamp

Orientation with basic hardware/software concepts in computing such as the UNIX environment and terminal,
typesetting documents, and version control.

Topics covered:
* [UNIX/Linux](https://mhasoba.github.io/TheMulQuaBio/notebooks/01-Unix.html)
* [Shell Scripting](https://mhasoba.github.io/TheMulQuaBio/notebooks/02-ShellScripting.html)
* [Git](https://mhasoba.github.io/TheMulQuaBio/notebooks/03-Git.html)
* [LaTeX](https://mhasoba.github.io/TheMulQuaBio/notebooks/04-LaTeX.html)

### Week 2: Python I

Introduction to the Python programming language.

Topics covered:
* Basics of Python as a programming language.
* Basic Python data types and structures.
* How to write clean and well-annotated Python scripts for automating computing tasks. 
* How to write Python functions and programs.

Notes: [Biological Computing in Python I](https://mhasoba.github.io/TheMulQuaBio/notebooks/05-Python_I.html#)

### Week 3: R

Introduction to the R programming language.

Topics covered:
* How to use R for data exploration
* How to use R for data visualization and producing elegant, intuitive, and publication quality graphics.
* R data types & structures and control flows.
* How to write and debug efficient R scripts and functions.
* How to use R packages and applications in certain areas (e.g., Genomics, Population biology).

Notes: 
* [Biological Computing in R](https://mhasoba.github.io/TheMulQuaBio/notebooks/07-R.html)
* [Data Management and Visualization](https://mhasoba.github.io/TheMulQuaBio/notebooks/08-Data_R.html)

### Week 7: Python II

More advanced Python topics.

Topics covered:
* Python program testing, debugging and documentation.
* How to use Python for retrieving, managing, and analyzing data from local and remote databases. 
* How to automate file handling, string manipulation, and run shell scripts.
* How to use Python for efficient numerical analyses.
* How to run analyses by patching together R or R + Python scripts and functions.

Notes: 
* [Biological Computing in Python II](https://mhasoba.github.io/TheMulQuaBio/notebooks/06-Python_II.html)
* [Introduction to Jupyter](https://mhasoba.github.io/TheMulQuaBio/notebooks/Appendix-JupyIntro.html)

## Prerequisites

This project was developed on a Mac OS, but was developed to be platform-independent (across Unix OS).

The following packages (with versions) are used in the project:
* LaTeX 
* Python (3.7.7)
* R (4.0.3)
* Jupyter-Notebook (6.1.4)

## Dependencies

### Python 3.7
* `pickle` 
* `numpy` 
* `scipy` 
* `pandas` 
* `matplotlib`
* `lmfit`
* `smt`
* `statsmodels`
 
### R 4.0.3
* `tidyverse`
* `reshape2` 
* `dplyr` 
* `tidyr` 
* `ggplot2` 
* `maps`
* `plyr` 
* `gridExtra`
* `grid`
* `scales`

### LaTeX
* `agsm.bst` (bibliography style to be stored in MiniProject/Code/ directory - see [here](http://ftp.math.utah.edu/pub/tex/bibtex/agsm.bst))

### Jupyter Notebook
* IPython kernel
* R kernel (see [here](https://github.com/IRkernel/IRkernel))

### Command Line
* `texcount` - see [here](https://app.uio.no/ifi/texcount/intro.html)

## Contact

Email: <lds20@ic.ac.uk>.

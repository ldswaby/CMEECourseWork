# Week 1

This directory contains coursework for week 1 of the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

Topics covered are:
* [UNIX/Linux](https://mhasoba.github.io/TheMulQuaBio/notebooks/01-Unix.html)
* [Shell Scripting](https://mhasoba.github.io/TheMulQuaBio/notebooks/02-ShellScripting.html)
* [Git](https://mhasoba.github.io/TheMulQuaBio/notebooks/03-Git.html)
* [LaTeX](https://mhasoba.github.io/TheMulQuaBio/notebooks/04-LaTeX.html)

## Prerequisites

This week's work was completed on a Mac OS, but was written to run on any Unix system.

The following packages were used:
* MacTeX (or LaTeX)
* imagemagick


## Week 1 Structure and Usage

This directory containins the following folders:
* Data - contains data files used during the week.
* Code - contains all code scripts for the week.
* Results - empty directory for any results files to be pushed into if they exist.

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if there are any) being pushed into the *Results/* directory. However, most (if not all) scripts can be run with no arguments.

E.g.

```$ sh Code/CountLines.sh Data/E.coli.fasta ```

Or:

```$ sh Code/CountLines.sh```

## Scripts
1. [UnixPrac1.txt](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/UnixPrac1.txt)
2. [boilerplate.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/boilerplate.sh)
3. [tabtocsv.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/tabtocsv.sh)
4. [variables.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/variables.sh)
5. [MyExampleScript.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/MyExampleScript.sh)
6. [Countlines.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/CountLines.sh)
7. [ConcatenateTwoFiles.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/ConcatenateTwoFiles.sh)
8. [tiff2png.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/tiff2png.sh)
9. [csvtospace.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/csvtospace.sh)
10. [FirstExample.tex](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/FirstExample.tex)
11. [FirstBiblio.bib](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/FirstBiblio.bib)
12. [CompileLaTeX.sh](https://github.com/ldswaby/CMEECourseWork/blob/master/Week1/Code/CompileLaTeX.sh)


### 1. UnixPrac1.txt

A .txt file containing a collection of single line commands to perform different counts on a set of .fasta files containing genetic code.

### 2. boilerplate.sh

This is my first .sh script, printing "This is a shell script!".

### 3. tabtocsv.sh

This .sh script converts the tabs to commas in a given text file (without changing the original file) and saves output as a txt file in the **Results** directory.

### 4. variables.sh

This .sh script assigns values to variables and shows how these values can be replaced during the running of the script. There are two separate scripts, one with strings and one with integers.

### 5. MyExampleScript.sh

This .sh script shows two ways of assigning variables, printing both to screen.

### 6. CountLines.sh

This .sh script counts lines in a file (provided as a command line argument).

### 7. ConcatenateTwoFiles.sh

This .sh script combines two files into a third. It requires three arguments: 1) first file (and realtive path) to be merged, 2) second file (and relative path) to be merged and 3) name and relative path of file to be created from merged files

### 8. tiff2png.sh

This .sh script converts a given .tiff (provided as a command line argument) to a .png, saving the png in the **Results** directory.

### 9. csvtospace.sh

This .sh script converts a given .csv file (provided as a command line argument) to a space delimited .txt file (without changing the original file) and saves the result in the **Results** folder.

### 10. FirstExample.tex

This .tex file contains my first LaTeX code for a simple document with title, abstract, 2 sections, equations and one bibliography reference using BibTeX.

### 11. FirstBiblio.bib

This .bib file contains a BibTeX reference taken from Google Scholar for use in FirstExample.tex.

### 12. CompileLaTeX.sh

This .sh script compiles a LaTeX .tex file (provided as a command line argument) with BibTeX and creates a pdf. It also removes all the unnecessary files that are created at the same time. If a path, such as ../Results/, is provided as a second command line argument, the resulting pdf will be moved to that directory. Note that this second argument is optional.

## Contact

If you want to contact me you can reach me at <lds20@ic.ac.uk>.

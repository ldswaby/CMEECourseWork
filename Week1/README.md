# Week 1

This directory contains coursework for week 1 of the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

Topics covered are:
* [UNIX/Linux](https://mhasoba.github.io/TheMulQuaBio/notebooks/01-Unix.html)
* [Shell Scripting](https://mhasoba.github.io/TheMulQuaBio/notebooks/02-ShellScripting.html)
* [Git](https://mhasoba.github.io/TheMulQuaBio/notebooks/03-Git.html)
* [LaTeX](https://mhasoba.github.io/TheMulQuaBio/notebooks/04-LaTeX.html)

## Prerequisites

This week's work was completed on a Unix OS.

The following packages were used:
* LaTeX 

Installed with the following command

Linux:
```
sudo apt-get install texlive-full texlive-fonts-recommended texlive-pictures texlive-latex-extra imagemagick
```

macOS:

```brew install mactex ``` 
OR 
```brew install basictex ```

## Week 1 Structure and Usage

This directory containins the following folders:
* Data - contains data files used during the week.
* Code - contains all code scripts for the week.
* Results - contains any results generated during the week's exercises.

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if there are any) being pushed into the *Results/* directory. However, most (if not all) scripts can be run with no arguments.

E.g.

```
$ sh Code/CountLines.sh Data/E.coli.fasta 
```
Or:
```
$ sh Code/CountLines.sh
```

## Contact

If you want to contact me you can reach me at <lds20@ic.ac.uk>.

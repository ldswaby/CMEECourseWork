# My CMEE Coursework Repository

This repository contains coursework for the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) at Imperial College London.

## Prerequisites

This project was developed on a Unix OS.

The following packages (with versions) are used in the project:
* LaTeX 
* Python (3.7.7)
* R (3.6.3)

## Dependencies

TBA

## CMEECoursework Structure and Usage

This repository is divided into weeks, with the directory for each week containing a combination of the following subdirectories:
* Data - contains data files used during the week.
* Code - contains all code scripts for the week.
* Results - contains any results generated during the week's exercises.
* Sandbox - contains any 'dummy' files/scripts used to experiment.

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if there are any) being pushed into the *Results/* directory.

E.g.

```
>> sh Week1/Code/CountLines.sh Week1/Data/E.coli.fasta 
```

## Contact

Email: <lds20@ic.ac.uk>.
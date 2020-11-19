# My CMEE Coursework Repository

This directory contains coursework for week 7 of the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

Topics covered are:
* [Biological Computing in Python II](https://mhasoba.github.io/TheMulQuaBio/notebooks/06-Python_II.html)

## Prerequisites

This project was developed on a Unix OS.

The following packages (with versions) are used in the project:
* Python (3.7.7)

## Dependencies

* `numpy` 
* `scipy` 
* `matplotlib`
* `pandas` 

## Week 2 Structure and Usage

This directory contains the following folders:
* Data - contains data files used during the week.
* Code - contains all code scripts for the week.
* Results - empty directory for any results files to be pushed into if they exist.

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if there are any) being pushed into the *Results/* directory. However, most (if not all) scripts can be run with no arguments.

E.g.

```
$ python3 Code/align_seqs.py Data/seqs.txt 
```
Or:
```
$ python3 Code/align_seqs.py
```

## Contact

Email: <lds20@ic.ac.uk>.
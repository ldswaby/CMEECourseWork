# Week 7

This directory contains coursework for week 7 of the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

Topics covered are:
* [Biological Computing in Python II](https://mhasoba.github.io/TheMulQuaBio/notebooks/06-Python_II.html)
* [Introduction to Jupyter](https://mhasoba.github.io/TheMulQuaBio/notebooks/Appendix-JupyIntro.html)

## Prerequisites

This project was developed on a Unix OS.

The following packages (with versions) are used in the project:
* Python (3.7.7)
* Jupyter-Notebook (6.1.4)

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

Many scripts in the *Code/* directory accept arguments (e.g. files in the *Data/* directory), with results (if there are any) being pushed into the *Results/* directory. However, most (if not all) scripts can be run with no arguments.

E.g.

```
$ python3 Code/LV2.py 1 0.1 1.5 0.75 50 35
```
Or:
```
$ python3 Code/LV2.py
```

## Contact

Email: <lds20@ic.ac.uk>.
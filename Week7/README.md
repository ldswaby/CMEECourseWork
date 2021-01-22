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

## Scripts
1. [LV1](#1.-LV1)
2. [LV2](#2.-LV2)
3. [Profileme](#3.-Profileme)
4. [profileme2](#4.-Profileme2)
5. [timeitme](#5.-timeitme)
6. [LV3](#6.-LV3)
7. [LV4](#7.-LV4)
8. [run_LV](#8.-run_LV)
9. [re4](#11.-regexs)
10. [blackbirds](#12.-blackbirds)
11. [TestR(R)](#14.-TestR(R))
12. [TestR(python)](#15.TestR(python))
13. [using_os](#16.-using_os)
14. [fmr(R)](#17.-fmr)
15. [run_fmr_R](#18.-run_fmr_R)
16. [MyFirstJupyterNb](#19.-MyFirstJupyterNb)

### 1. LV1

A .py script that uses numerical integration to solve the Lotka-Volterra model. It contains one function that calculates the growth rate of resource and consumer populations at a given time step one main function that contains the rest of the script. Initial parameters are then set and the scipy integrate subpackage is used to solve the Lotka-Volterra system. The results are plotted in two different graphs, showing the change of the two population densities over time and also the change in the two population densities with respect to each other.

### 2. LV2

A .py script that uses numerical integration to solve the Lotka-Volterra model, including carrying capacity K, and allows user inputs for certain parameters. It contains one function that calculates the growth rate of resource and consumer populations at a given time step and one main function that contains the rest of the script. Within the main programme, this function is redefined as a partial to allow the fixed parameters to be passed to the function. Initial parameters are inputted by user, otherwise defaults are used, and the scipy integrate subpackage is used to solve the Lotka-Volterra system. The results are plotted in two different graphs, showing the change of the two population densities over time and also the change in the 
two population densities with respect to each other.

### 3. profileme

A .py script that contains three functions for practising profiling. One function, my_squares, squares the input, one, my_join, joins string together and the third, run_my_funcs, runs the other two functions. A sample of run_my_funcs is called at the end to allow profiling.

### 4. profileme2

A .py script that contains improved versions of the three functions from Profileme for practising profiling. One function, my_squares, squares the input using a list comprehension (there is also a commented out version that uses preallocation, which is slower than the list comprehension), one, my_join, joins string together using an explicit string concatenation and the third, run_my_funcs, runs the other two functions as before. A sample of run_my_funcs is called at the end to allow profiling.

### 5. timeitme

A .ipy script that compares the speed of for loops and list comprehensions and the join method for strings by importing the functions from Profileme.py and Profileme2.py and using the ipython timeit function. It also compares this to a simpler approach using time.time().

### 6. LV3

A .py script that uses a discrete time for loop to solve the Lotka-Volterra model including carrying capacity K, and allows user inputs for certain parameters. It contains one function that calculates population densities of resource and consumer populations at a given time step by running a for loop over the time steps and calculating the populations densities at each step, and one main function that contains the rest of the script. Initial parameters are inputted by user (otherwise defaults are used) and passed to the function, which solves the Lotka-Volterra system at discrete time intervals. The results are plotted in two different graphs, showing the change of the two population densities over time and also the change in the two population densities with respect to each other.

### 7. LV4

A .py script that uses a discrete time for loop to solve the Lotka-Volterra model including carrying capacity K and Gaussian Fluctuation E, and allows user inputs for certain parameters. Contains one function that calculates population densities of resource and consumer populations at a given time step by running a for loop over the time steps and calculating the populations densities at each step, and one main function that contains the rest of the script. Initial parameters are inputted by user (otherwise defaults are used) and passed to the function, which solves the Lotka-Volterra system at discrete time intervals. The results are plotted in two different graphs, showing the change of the two population densities over time and also the change in the two population densities with respect to each other.

### 8. run_LV

A .py script that profiles four scripts that solve the Lotka-Volterra model, comparing the time taken for the ten longest calls in each.

### 9. re4

A .py script containing various examples using regex to search for matches in strings, text files and also a webpage.


### 10. blackbirds

A .py script that uses regex to capture Kingdom, Phylum and Species name from a text file of blackbird taxonomic information. It prepares the data by reading the file, replacing tabs and newlines with spaces and removing any non_ASCII symbols. Regex is then used to print Kingdom, Phylum and Species name in a list of tuples.

### 11. TestR(R)

A simple .R script that prints a string.

### 12. TestR(python)

A .py script that runs the test R script of the same name.

### 13. using_os

A .py script that produces a list of files and directories from your home directory using the subprocess.os module. It creates three separate lists: files and directories starting with an upper case "C"; files and directories starting with an upper case "C" or a lower case "c"; and finally only directories starting with an upper case "C" or a lower case "c".

### 14. fmr

A .R script that plots log(field metabolic rate) against log(body mass) for the Nagy et al 1999 dataset to a file fmr.pdf. This script was not written by me and is only used for practicing running R scripts from python in the python script run_fmr_R.py.

### 15. run_fmr_R

A .py script that uses the subprocess module to run an R-script that produces a pdf. Prints the R output to screen and includes try and except to kill the process if it takes longer than 30 seconds and also includes an if statement to print whether the R-script ran successfully.

### 16. MyFirstJupyterNb

A Jupyter Notebook (.ipynb) practising various Jupyter capabilities, including symbolic variables and differentiation.

## Contact

Email: <lds20@ic.ac.uk>.
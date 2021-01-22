# Week 2

This directory contains coursework for week 2 of the [MSc Computational Methods in Ecology and Evolution](https://www.imperial.ac.uk/study/pg/life-sciences/computational-methods-ecology-evolution/) course at Imperial College London.

Topics covered are:
* [Biological Computing in Python I](https://mhasoba.github.io/TheMulQuaBio/notebooks/05-Python_I.html#)

## Prerequisites

This project was developed on a Unix OS.

The following packages (with versions) are used in the project:
* Python (3.7.7)

## Dependencies

* `pickle`

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

## Scripts
1. [align_seqs.py](#20.-align_seqs)
2. [align_seqs_better.py](#22.-align_seqs_better)
3. [align_seqs_fasta](#21.-align_seqs_fasta)
4. [basic_csv](#4.-basic_csv)
5. [basic_io1](#1.-basic.io1)
6. [basic_io2](#2.-basic_io2)
7. [basic_io3](#3.-basic_io3)
8. [boilerplate](#10.-boilerplate)
9. [cfexercises1](#5.-cfexercises1)
10. [cfexercises2](#7.-cfexercises2)
11. [control_flow](#13.-control_flow)
12. [debugme](#19.-debugme)
13. [dictionary](#16.-dictionary)
14. [lc1](#14.-lc1)
15. [lc2](#15.-lc2)
16. [loops](#6.-loops)
17. [oaks](#8.-oaks)
18. [oaks_debugme](#23.-oaks_debugme)
19. [Scope](#9.-Scope)
20. [sysargv](#12.-sysargv)
21. [test_control_flow](#18.-test_control_flow)
22. [tuple](#17.-tuple)
23. [using_name](#11.-using_name)

### 1. basic_io1.py

A .py script that uses a for loop to read from a .txt file, printing the content first with and then without blank lines. Requires testweek2.txt from the directory **Data**.

### 2. basic_io2.py

A .py script that uses a for loop to write the numbers 0-99 into a .txt file with a new line between each number. This .txt file is saved in **Results**.

### 3. basic_io3.py

A .py script to store a dictionary for later use using the pickle package.

### 4. basic_csv.py

A .py script that reads and writes .csv files. The script reads a csv (using the csv package) and then prints it as a list, explicitly stating the species name after each row (on a new line). The script then writes a subset of each row from the first csv into a different csv. Requires testcsv.csv from the directory **Data** and saves the new .csv file (bodymass.csv) into the **Results** directory.

### 5. cfexercises1.py

A .py script that contains six mathematical functions showing different conditionals, including doctests for each function. Main function calls all six mathematical functions on sample parameters.

### 6. loops.py

A .py script to practice various for and while loops.

### 7. cfexercises2.py

A .py script combining loops and conditionals, printing the string 'hello' each time a condition is met.

### 8. oaks.py

A .py script that contains one function, is_an_oak, which finds the taxa of oak trees from a list of species by returning `True` if `name` parameter starts with 'quercus '. Oaks are saved to two sets (as written and all in capitals) using both for loops and list comprehensions with the is_an_oak function. In all, four sets are printed.

### 9. scope.py

A .py containing five separate scripts exemplifying variable scope. Global variables are printed at various stages, inside and outside of functions.

### 10. boilerplate.py

A .py boilerplate for a basic programme, containing docstrings, imports, arguments, functions and an if statement to ensure that the function is called from the command line.

### 11. using_name.py

A .py script illustrating the difference between importing a module and running it as the main programme.

### 12. sysargv.py

A short .py script illustating how sys.argv works when run with different variables.

### 13. control_flow.py

A .py programme with some functions emplifying the use of control statements, including some examples as part of the main programme.

### 14. lc1.py

A .py script containing some list comprehensions and for loops to print different attributes of birds from a tuple of tuples.

### 15. lc2.py

A .py script that uses list comprehensions and loops to identify months with high and low rainfall from a given tuple of tuples.

### 16. dictionary.py

A .py scipt that populates a dictionary from a given list of tuples.

### 17. tuple.py

A .py script that prints data from a tuple of tuples in a more readable format.

### 18. test_control_flow.py

A .py programme based on [control_flow](#13.-control_flow) but containing only the even_or_odd function and with added doctests.

### 19. debugme.py

A .py programme containing a practice example for using the debugger. The function has a written-in error for the debugger to detect.

### 20. align_seqs.py

A .py programme that calculates the best alignment of two DNA sequences. It contains one function (calculate_scores), which computes a score by returning the number of matches starting from an arbitrary startpoint (chosen by user). The first alignment found with the best score overall is saved to a csv file.

### 21. align_seqs_fasta.py

A .py that calculates the best alignment of any two DNA sequences, with defaults if no user input is given. It contains the same function as above along with a short script to identify whether or not user inputs have been given. The first alignment found with the best score overall is saved to a csv file.

### 22. align_seqs_better.py

A .py that calculates the best alignment of any two DNA sequences, with defaults if no user input is given. It contains one function (calculate_scores), which computes a score by returning the number of matches starting from an arbitrary startpoint (chosen by user), as well as along with a short script to identify whether or not user inputs have been given. It also saves all combinations with the best alignment scores into a csv file.

### 23. oaks_debugme.py

A .py programme that locates oaks by genus from given data in a csv file. It contains two functions: one (is_an_oak) that returns `True` if the genus is exactly 'quercus' and another (main) that prints all taxa and searches for oaks, printing 'FOUND AN OAK!' when one is located and printing them into a new .csv file (with the species, genus headers) called JustOaksData.csv, saved in the Results directory. It requires the TestOaksData.csv located in the Data directory of Week2.

## Contact

Email: <lds20@ic.ac.uk>.
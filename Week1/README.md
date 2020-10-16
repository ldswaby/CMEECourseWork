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
<sudo apt-get install texlive-full texlive-fonts-recommended texlive-pictures texlive-latex-extra imagemagick>
```

macOS:
```<brew install mactex> ``` 
OR 
```<brew install basictex> ```

## CMEECoursework Structure and Usage

Scripts in the *Code/* directory are typically run on files in the *Data/* directory, with results (if there are any) being pushed into the *Results/* directory.

E.g.

```
>> sh Code/CountLines.sh Data/E.coli.fasta 
```

## Contact

If you want to contact me you can reach me at <lds20@ic.ac.uk>.

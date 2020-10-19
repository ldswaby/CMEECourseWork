#!/usr/bin/env python3

"""Playing around with CSVs"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import csv

# Read a file containing:
# 'Species','Infraorder','Family','Distribution','Body mass male (Kg)'
f = open('../data/testcsv.csv', 'r')

csvread = csv.reader(f)
next(csvread)
temp = []
for row in csvread:
    temp.append(tuple(row))
    print(row)
    print("The species is", row[0])

f.close()

# write a file containing only species name and Body mass
f = open('../data/testcsv.csv', 'r')
g = open('../data/bodymass.csv', 'w')

csvread = csv.reader(f)
next(csvread)
csvwrite = csv.writer(g)
for row in csvread:
    print(row)
    csvwrite.writerow([row[0], row[4]])

f.close()
g.close()
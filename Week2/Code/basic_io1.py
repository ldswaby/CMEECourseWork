#!/usr/bin/env python3

"""File I/O exercises 1"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

#############################
# FILE INPUT
#############################
# Open a file for reading
f = open('../Data/test.txt', 'r')

for line in f:
    print(line)

# close the file
f.close()

# Same example, skip blank lines
f = open('../Data/test.txt', 'r')
for line in f:
    if len(line.strip()) > 0:
        print(line)

f.close()

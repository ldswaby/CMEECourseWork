#!/usr/bin/env python3

"""File I/O exercises 2"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

#############################
# FILE OUTPUT
#############################
# Save the elements of a list to a file
list_to_save = range(100)

f = open('../Data/testout.txt', 'w')
for i in list_to_save:
    f.write(str(i) + '\n')  # Add a new line at the end

f.close()
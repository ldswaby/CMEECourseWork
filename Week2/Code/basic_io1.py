#!/usr/bin/env python3

"""File I/O exercises 1"""
#TODO: How are these meant to run if we ignore Sandbox?

#############################
# FILE INPUT
#############################
# Open a file for reading
f = open('../Sandbox/test.txt', 'r')

for line in f:
    print(line)

# close the file
f.close()

# Same example, skip blank lines
f = open('../Sandbox/test.txt', 'r')
for line in f:
    if len(line.strip()) > 0:
        print(line)

f.close()
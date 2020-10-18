#!/usr/bin/env python3

#TODO: No functions, but no script-level docstring either. 2 pts deducted

# Filename: using_name.py

if __name__ == '__main__':
    print('This program is being run by itself')
else:
    print('I am being imported from another module')

print("This module's name is: " + __name__)
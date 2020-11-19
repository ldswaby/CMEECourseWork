#!/usr/bin/env python3

"""Playing with subprocess.os"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import os

## Practicals ##

# Use the subprocess.os module to get a list of files and directories 
# in your ubuntu home directory

# Hint: look in subprocess.os and/or subprocess.os.path and/or 
# subprocess.os.walk for helpful functions

#################################
#~Get a list of files and 
#~directories in your home/ that start with an uppercase 'C'

# Type your code here:

# Get the user's home directory.
home = os.path.expanduser("~")

# Create a list to store the results.
FilesDirsStartingWithC = []

# Use a for loop to walk through the home directory.
for (dir, subdir, files) in os.walk(home):
    for item in subdir + files:
        if item.startswith('C'):
            FilesDirsStartingWithC.append(item)

# Print result
print(f"{len(FilesDirsStartingWithC)} files/subdirectories beginning with 'C' "
      f"found in your home directory.")

#################################
# Get files and directories in your home/ that start with either an 
# upper or lower case 'C'

FilesDirsStartingWithCc = []

for (dir, subdir, files) in os.walk(home):
    for item in subdir + files:
        if item.lower().startswith('c'):
            FilesDirsStartingWithCc.append(item)

print(f"{len(FilesDirsStartingWithCc)} files/subdirectories beginning with an "
      f"upper or lower case 'C' found in your home directory.")

#################################
# Get only directories in your home/ that start with either an upper or 
#~lower case 'C'

# Type your code here:
DirsStartingWithCc = []

for (dir, subdir, files) in os.walk(home):
    for s in subdir:
        if s.lower().startswith('c'):
            DirsStartingWithCc.append(s)

print(f"{len(DirsStartingWithCc)} subdirectories beginning with an "
      f"upper or lower case 'C' found in your home directory.")
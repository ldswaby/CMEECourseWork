#!/usr/bin/env python3

"""File I/O exercises 3"""

#TODO: No such file or directory: '../Sandbox/testp.p' (AS SANDBOX IS GITIGNORED)

#############################
# STORING OBJECTS
#############################
# To save an object (even complex) for later use
my_dictionary = {"a key": 10, "another key": 11}

import pickle

f = open('../Sandbox/testp.p', 'wb')  # note the b: accept binary files
pickle.dump(my_dictionary, f)
f.close()

# Load the data again
f = open('../Sandbox/testp.p', 'rb')
another_dictionary = pickle.load(f)
f.close()

print(another_dictionary)
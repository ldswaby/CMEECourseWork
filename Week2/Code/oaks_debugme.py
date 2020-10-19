#!/urs/bin/env python3

"""Playing with doc tests and debugging"""

# Fix the bug (e.g., you could insert a debugging breakpoint using import ipdb; ipdb.set_trace())
# TODO: why do we need to do this if the error message alerts us to the bug instantly?

import csv
import sys

#Define function
def is_an_oak(name):
    """ Returns True if lowercase name is starts with 'quercus '

    >>> is_an_oak('Fagus sylvatica')
    False

    >>> is_an_oak('Fraxinus excelsior')
    False

    >>> is_an_oak('Quercus ajoensis')
    True

    >>> is_an_oak('Quercuss ajoensis')
    False
    """
    return name.split()[0].lower() == 'quercus'

def main(argv):
    """Run functions
    """
    f = open('../data/TestOaksData.csv','r')
    g = open('../data/JustOaksData.csv','w')
    taxa = csv.reader(f)
    next(taxa)
    csvwrite = csv.writer(g)
    oaks = set()
    for row in taxa:
        print(row)
        print ("The genus is: ") 
        print(row[0] + '\n')
        if is_an_oak(row[0]):
            print('FOUND AN OAK!\n')
            csvwrite.writerow([row[0], row[1]])    

    return 0
    
if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
#!/urs/bin/env python3

#TODO: 2 practicals on this, one group one single, so do we keep a copy in each?
#TODO: README dependencies

"""Playing with doc tests and debugging"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import csv
import sys

#Define function
def is_an_oak(name):
    """ Returns True if lowercase name contains 'quercus'

    >>> is_an_oak('Fagus sylvatica')
    False

    >>> is_an_oak('Fraxinus excelsior')
    False

    >>> is_an_oak('Quercus ajoensis')
    True

    >>> is_an_oak('Quercuss ajoensis')
    True

    >>> is_an_oak('aQuercus')
    True

    >>> is_an_oak('Fagus quercusi')
    False
    """
    return 'quercus' in name.split()[0].lower()

def main(argv):
    """Run functions
    """
    f = open('../data/TestOaksData.csv','r')
    g = open('../data/JustOaksData.csv','w')
    taxa = csv.reader(f)
    header = next(taxa, None)
    csvwrite = csv.writer(g)
    csvwrite.writerow(header)
    #oaks = set()
    for row in taxa:
        print(row)
        print("The genus is: ")
        print(row[0] + '\n')
        if is_an_oak(row[0]):
            print('FOUND AN OAK!\n')
            csvwrite.writerow([row[0], row[1]])    

    return 0
    
if __name__ == "__main__":
    status = main(sys.argv)
    sys.exit(status)
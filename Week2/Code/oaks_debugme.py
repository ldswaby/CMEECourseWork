#!/urs/bin/env python3

"""Playing with doc tests and debugging"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
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

def main():
    """Run functions
    """
    f = open('../Data/TestOaksData.csv', 'r')
    g = open('../Data/JustOaksData.csv', 'w')
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
    status = main()
    sys.exit(status)

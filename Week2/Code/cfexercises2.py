#!/urs/bin/env python3

"""Playing with loops and conditionals"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

for j in range(12):
    if j % 3 == 0:
        print('hello')

for j in range(15):
    if j % 5 == 3:
        print('hello')
    elif j % 4 == 3:
        print('hello')

z = 0
while z != 15:
    print('hello')
    z = z + 3

z = 12
while z < 100:
    if z == 31:
        for k in range(7):
            print('hello')
    elif z == 18:
        print('hello')
    z += 1

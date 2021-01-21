#!/urs/bin/env python3

"""Tuples and string formatting practical."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

birds = (('Passerculus sandwichensis', 'Savannah sparrow', 18.7),
         ('Delichon urbica', 'House martin', 19),
         ('Junco phaeonotus', 'Yellow-eyed junco', 19.5),
         ('Junco hyemalis', 'Dark-eyed junco', 19.6),
         ('Tachycineata bicolor', 'Tree swallow', 20.2),
         )

# Birds is a tuple of tuples of length three: latin name, common name, mass.
# write a (short) script to print these on a separate line or output block by species 
# Hints: use the "print" command! You can use list comprehensions!

for (latin, common, mass) in birds:
    print(f"The {common} (latin name '{latin}') weighs {mass}g")
    # Or:
    # print("The {} (latin name '{}') weighs {}g".format(common, latin, mass))
    # print("The %s (latin name '%s') weighs %dg" % (common, latin, mass))

#!/urs/bin/env python3

"""Dictionaries practical"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

taxa = [('Myotis lucifugus', 'Chiroptera'),
        ('Gerbillus henleyi', 'Rodentia',),
        ('Peromyscus crinitus', 'Rodentia'),
        ('Mus domesticus', 'Rodentia'),
        ('Cleithrionomys rutilus', 'Rodentia'),
        ('Microgale dobsoni', 'Afrosoricida'),
        ('Microgale talazaci', 'Afrosoricida'),
        ('Lyacon pictus', 'Carnivora'),
        ('Arctocephalus gazella', 'Carnivora'),
        ('Canis lupus', 'Carnivora'),
        ]

# Write a short python script to populate a dictionary called taxa_dic 
# derived from  taxa so that it maps order names to sets of taxa. 
# E.g. 'Chiroptera' : set(['Myotis lucifugus']) etc.

taxa_dic = {}

for order in {x[1] for x in taxa}:
    # Populate dict with order names mapped to corresponding sets of taxa
    taxa_dic[order] = {x[0] for x in taxa if x[1] == order}

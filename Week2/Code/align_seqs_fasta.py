#!/usr/bin/env python3

"""Aligns sequences"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##
def calculate_score(s1, s2, l1, l2, startpoint):
    """Calculate best alignment score (no. of matched bases) if 2
    sequences
    """
    matched = "" # to hold string displaying alignements
    score = 0
    for i in range(l2):
        if (i + startpoint) < l1:
            if s1[i + startpoint] == s2[i]: # if the bases match
                matched += "*"
                score += 1
            else:
                matched += "-"

    return score

def main(argv):
    """Run functions"""

    # Parse inputs
    if len(argv) == 1:
        seqfile1 = '../Data/407228326.fasta'
        seqfile2 = '../Data/407228412.fasta'
    elif len(argv) == 2:
        sys.exit(
            'ERROR: this script takes 2 input seq files. You have provided 1.')
    elif len(argv) == 3:
        seqfile1 = argv[1]
        seqfile2 = argv[2]
    else:
        sys.exit('ERROR: too many arguments were provided.')

    ## TEXT IN
    #TODO: account for csv inputs

    with open(seqfile1, 'r') as f1:
        head1 = f1.readline().strip()
        seq1 = ''.join(line.strip() for line in f1)

    with open(seqfile2, 'r') as f2:
        head2 = f2.readline().strip()
        seq2 = ''.join(line.strip() for line in f2)

    # Assign the longer sequence s1, and the shorter to s2
    # l1 is length of the longest, l2 that of the shortest

    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1 = seq1
        h1 = head1
        s2 = seq2
        h2 = head2
    else:
        s1 = seq2
        h1 = head2
        s2 = seq1
        h2 = head1
        l1, l2 = l2, l1  # swap the two lengths

    # Find the best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(l1):  # Note that you just take the last alignment with the highest score
        z = calculate_score(s1, s2, l1, l2, i)
        if z > my_best_score:
            my_best_align = "-" * i + s2  # think about what this is doing!
            my_best_score = z

    with open('../Results/group_fasta_algmt.fa', 'w') as algmt:
        algmt.write(f'{h2}\n')
        algmt.write(f'{my_best_align}\n')
        algmt.write(f'{h1}\n')
        algmt.write(s1)
        algmt.write('\n\n' + f"Best score: {my_best_score}")

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)
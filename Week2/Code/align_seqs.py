#!/usr/bin/env python3

#TODO: Write README.md

"""Aligns 2 sequences in an input text file."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##
def calculate_score(s1, s2, l1, l2, startpoint):
    """Calculate best alignment score (no. of matched bases) of 2
    sequences
    """
    matched = "" # to hold string displaying alignements
    score = 0
    for i in range(l2):
        if (i + startpoint) < l1:
            if s1[i + startpoint] == s2[i]:
                # if the bases match, fill with '*' and add 1 to score
                matched += "*"
                score += 1
            else:
                # otherwise fill with '-'
                matched += "-"
    # import ipdb; ipdb.set_trace()

    # some formatted output
    matches = "." * startpoint + matched
    print(matches)
    print("." * startpoint + s2)
    print(s1)
    print(score)
    print(" ")

    return score, matches

def main(argv):
    """Run functions
    """
    # Parse inputs
    if len(argv) == 1:
        seqfile = '../Data/seqs.txt'
    elif len(argv) == 2:
        seqfile = argv[1]
    else:
        sys.exit('ERROR: too many arguments were provided.')

    ## TEXT IN
    with open(seqfile, 'r') as f:
        recs = f.read().splitlines()  # To strip newlines
        seq1 = recs[0]
        seq2 = recs[1]

    """
    ## FASTA IN
    from Bio import SeqIO
    try:
        seqfile = argv[1]
    except:
        seqfile = '../Data/seqs.fa'

    recs = list(SeqIO.parse(seqfile, 'fasta'))
    seq1 = str(recs[0].seq)
    seq2 = str(recs[1].seq)
    """

    # Assign the longer sequence s1, and the shorter to s2
    # l1 is length of the longest, l2 that of the shortest

    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1 = seq1
        s2 = seq2
    else:
        s1 = seq2
        s2 = seq1
        l1, l2 = l2, l1  # swap the two lengths

    # now try to find the best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(
            l1):  # Note that you just take the last alignment with the highest score
        z, match = calculate_score(s1, s2, l1, l2, i)
        if z > my_best_score:
            my_best_align = ("-" * i) + s2  # start sequence at startpoint
            my_best_score = z
            my_best_match = match
    print(my_best_match.replace('-', '.'))
    print(my_best_align)
    print(s1)
    print("Best score:", my_best_score)

    """
    ## FASTA OUT
    from Bio import SeqIO
    from Bio.SeqRecord import SeqRecord
    from Bio.Seq import Seq
    
    outrec1 = SeqRecord(
        Seq(my_best_align),
        id="Seq1",
        description=f'Best Score: {my_best_score}'
    )
    outrec2 = SeqRecord(
        Seq(s1),
        id="Seq2",
        description=''
    )
    outrecs = [outrec1, outrec2]
    SeqIO.write(outrecs, '../Results/algmt.fa', 'fasta')
    """

    ## TEXT OUT
    with open(f'../Results/algmt.txt', 'w') as algmt:
        algmt.write(f"{my_best_match.replace('-', '.')}\n")
        algmt.write(f'{my_best_align}\n')
        algmt.write(str(s1))
        algmt.write('\n\n' + f"Best score: {my_best_score}")

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)
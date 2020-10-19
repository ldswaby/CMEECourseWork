#!/usr/bin/env python3

"""Aligns sequences"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

## Functions ##
def calculate_score(s1, s2, l1, l2, startpoint):
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

    ## FASTA IN
    try:
        seqfile1 = argv[1]
        seqfile2 = argv[2]
    except:
        seqfile1 = '../Data/407228326.fasta'
        seqfile2 = '../Data/407228412.fasta'

    # Parse inputs
    SeqRec1 = list(SeqIO.parse(seqfile1, 'fasta'))[0]
    seq1 = str(SeqRec1.seq)
    SeqRec2 = list(SeqIO.parse(seqfile2, 'fasta'))[0]
    seq2 = str(SeqRec2.seq)

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

    # Find the best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(l1):  # Note that you just take the last alignment with the highest score
        z = calculate_score(s1, s2, l1, l2, i)
        if z > my_best_score:
            my_best_align = "-" * i + s2  # think about what this is doing!
            my_best_score = z

    # Create SeqRecords for output fasta
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

    # Write to fasta
    SeqIO.write(outrecs, '../Results/group_fasta_algmt.fa', 'fasta')

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)
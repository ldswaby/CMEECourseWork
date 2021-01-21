#!/usr/bin/env python3

"""Aligns sequences"""

__author__ = 'Luke Swaby (lds20@ic.ac.uk), ' \
             'Jinkai Sun (jingkai.sun20@imperial.ac.uk), ' \
             'Acacia Tang (t.tang20@imperial.ac.uk), ' \
             'Dengku Tang (dengkui.tang20@imperial.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##
def calculate_score(s1, s2, startpoint):
    """Calculate best alignment score (no. of matched bases) of 2 padded
     sequences
    """
    score = 0
    for i in range(len(s1)):
        if (i + startpoint) < len(s1):
            if s1[i + startpoint] == s2[i] and s2[i] != '-':
                score += 1
            else:
                continue

    return score

def extract_seq(filename):
    """Extract seq from file (and header if present)
    """
    with open(filename) as f:
        line1 = f.readline().strip()
        header = line1.startswith('>')
        if header:
            # If there a header...
            head = line1
            seq = ''.join(line.strip() for line in f)
        else:
            # If there is no header (just seq)...
            f.seek(0)  # Return to first line
            head = None
            seq = ''.join(line.strip() for line in f)  # Join all lines into seq var

    return seq, head

def main(argv):
    """Run functions
    """    
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
    seq1, head1 = extract_seq(seqfile1)
    seq2, head2 = extract_seq(seqfile2)

    # Assign the longer sequence s1, and the shorter to s2
    # l1 is length of the longest, l2 that of the shortest

    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1 = (l2 - 1) * '-' + seq1 + (l2 - 1) * '-'
        s2 = seq2 + (l1 + l2 - 2) * '-'
        h1 = head1
        h2 = head2
        padlen = len(s2)
    else:
        l1, l2 = l2, l1  # swap the two lengths
        s1 = (l2 - 1) * '-' + seq2 + (l2 - 1) * '-'
        s2 = seq1 + (l1 + l2 - 2) * '-'
        h1 = head2
        h2 = head1
        padlen = len(s2)

    # Find the best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(padlen - l2 + 1):  # Note that you just take the last alignment with the highest score
        z = calculate_score(s1, s2, i)
        if z > my_best_score:
            my_best_align = "-" * i + s2[:-i]  # start sequence at startpoint
            my_best_score = z

    # Clip trailing hyphens
    s1start = s1.find(next(filter(str.isalpha, s1)))
    s2start = s2.find(next(filter(str.isalpha, s2)))
    start = max(s1start, s2start)

    s1end = s1[start:].find('-')
    s2end = my_best_align[start:].find('-')
    stop = len(s1[start:]) - max(s1end, s2end)

    my_best_align = my_best_align[start:-stop]
    s1 = s1[start:-stop]

    # Write fasta out
    with open('../Results/align_seqs_fasta.fa', 'w') as algmt:
        if h2:
            algmt.write(f'{h2}\n')
        algmt.write(f'{my_best_align}\n')
        if h1:
            algmt.write(f'{h1}\n')
        algmt.write(s1)

    print(f'Best Score: {my_best_score}')

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)

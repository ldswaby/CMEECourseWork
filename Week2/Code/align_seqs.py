#!/usr/bin/env python3

"""Aligns 2 sequences in an input text file."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys

## Functions ##
def calculate_score(s1, s2, startpoint):
    """Calculate best alignment score (no. of matched bases) of 2 padded
     sequences
    """
    matched = ""  # to hold string displaying alignements
    score = 0
    for i in range(len(s1)):
        if (i + startpoint) < len(s1):
            if s1[i + startpoint] == s2[i] and s2[i] != '-':
                # If match, add '*' to matched str and increment score
                matched += "*"
                score += 1
            else:
                # otherwise add '-' to matched str
                matched += "-"

    # Formatted output
    matches = "-" * startpoint + matched
    print(matches)
    print("-" * startpoint + s2[:len(s2)-startpoint])
    # Note: cannot use 'print("-" * startpoint + s2[:-startpoint])' here^ as
    # negative indexing won't work for i=0
    print(s1)
    print(f'Score: {score}')
    print(' ')

    return score, matches

def main(argv):
    """Run functions
    """
    # Parse inputs
    if len(argv) == 1:
        seqfile = '../Data/seqs.fa'
    elif len(argv) == 2:
        seqfile = argv[1]
    else:
        sys.exit('ERROR: too many arguments were provided.')

    # Text file in
    with open(seqfile, 'r') as f:
        # Assumes input fasta is not wrapped...
        seqs = [s for s in f.read().splitlines() if not s.startswith('>')]
        seq1 = seqs[0]
        seq2 = seqs[1]

    # Assign the longer sequence s1, and the shorter to s2
    # l1 is length of the longest, l2 that of the shortest
    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1 = (l2 - 1) * '-' + seq1 + (l2 - 1) * '-'
        s2 = seq2 + (l1 + l2 - 2) * '-'
        padlen = len(s2)
    else:
        l1, l2 = l2, l1  # swap the two lengths
        s1 = (l2 - 1) * '-' + seq2 + (l2 - 1) * '-'
        s2 = seq1 + (l1 + l2 - 2) * '-'
        padlen = len(s2)

    # Find best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(padlen-l2+1):
        # Note that only last alignment with the highest score is recorded
        print(f'Start index: {i}')
        z, match = calculate_score(s1, s2, i)
        if z > my_best_score:
            my_best_align = "-" * i + s2[:-i]  # start sequence at startpoint
            my_best_score = z
            my_best_match = match

    # Clip trailing hyphens
    s1start = s1.find(next(filter(str.isalpha, s1)))
    s2start = s2.find(next(filter(str.isalpha, s2)))
    start = max(s1start, s2start)

    s1end = s1[start:].find('-')
    s2end = my_best_align[start:].find('-')
    stop = len(s1[start:]) - max(s1end, s2end)

    my_best_match = my_best_match[start:-stop]
    my_best_align = my_best_align[start:-stop]
    s1 = s1[start:-stop]

    # Print result
    print(my_best_match)
    print(my_best_align)
    print(s1)
    print("Best score:", my_best_score)

    # Text file out
    with open(f'../Results/algmt.txt', 'w') as algmt:
        algmt.write(f"{my_best_match}\n")
        algmt.write(f'{my_best_align}\n')
        algmt.write(str(s1))
        algmt.write('\n\n' + f"Best score: {my_best_score}")

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)
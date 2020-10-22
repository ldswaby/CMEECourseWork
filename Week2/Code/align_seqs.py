#!/usr/bin/env python3

# TODO: Write README.md

"""Aligns 2 sequences in an input text file."""

__author__ = 'Luke Swaby (lds20@ic.ac.uk)'
__version__ = '0.0.1'

## Imports ##
import sys, re

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

    # some formatted output
    matches = "-" * startpoint + matched
    print(matches)
    print("-" * startpoint + s2[:len(s2)-startpoint])
    # Note: cannot use 'print("-" * startpoint + s2[:-startpoint])' here^ as
    # negative indexing won't work for i=0
    print(s1)
    print(f'Score: {score}')
    print('\n')

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

    # Text file in
    with open(seqfile, 'r') as f:
        recs = f.read().splitlines()  # To strip newlines
        seq1 = recs[0]
        seq2 = recs[1]

    # Assign the longer sequence s1, and the shorter to s2
    # l1 is length of the longest, l2 that of the shortest
    l1 = len(seq1)
    l2 = len(seq2)
    if l1 >= l2:
        s1algn = (l2-1)*'-' + seq1 + (l2-1)*'-'
        s2algn = seq2 + (l1+l2-2)*'-'
        padlen = len(s2algn)
    else:
        l1, l2 = l2, l1  # swap the two lengths
        s1algn = (l2-1)*'-' + seq2 + (l2-1)*'-'
        s2algn = seq1 + (l1+l2-2)*'-'
        padlen = len(s2algn)

    # Find best match (highest score) for the two sequences
    my_best_align = None
    my_best_score = -1

    for i in range(padlen-l2+1):
        # Note that only last alignment with the highest score is recorded
        print(f'Startpoint: {i}')
        z, match = calculate_score(s1algn, s2algn, i)
        if z > my_best_score:
            my_best_align = "-"*i + s2algn[:-i]  # start sequence at startpoint
            my_best_score = z
            my_best_match = match

    # Clip trailing hyphens
    s1start = re.search(r'[^-]', s1algn).start()
    s2start = re.search(r'[^-]', my_best_align).start()
    start = max(s1start, s2start)

    s1end = re.search(r'[^A-Z]', s1algn[start:]).start()
    s2end = re.search(r'[^A-Z]', my_best_align[start:]).start()
    stop = len(s1algn[start:]) - max(s1end, s2end)

    my_best_match = my_best_match[start:-stop]
    my_best_align = my_best_align[start:-stop]
    s1algn = s1algn[start:-stop]

    # Print result
    print(my_best_match)
    print(my_best_align)
    print(s1algn)
    print("Best score:", my_best_score)

    # Text file out
    with open(f'../Results/algmt.txt', 'w') as algmt:
        algmt.write(f"{my_best_match}\n")
        algmt.write(f'{my_best_align}\n')
        algmt.write(str(s1algn))
        algmt.write('\n\n' + f"Best score: {my_best_score}")

    return 0

if __name__ == '__main__':
    status = main(sys.argv)
    sys.exit(status)
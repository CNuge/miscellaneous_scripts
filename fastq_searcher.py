

"""
DNA Restriction Enzyme:  EcoT22I (AvaIII)

A	 	TGCA	|	T
T	|	ACGT	 	A

So search for ATGCAT

INPUT:

python3 fastq_searcher.py -r ATGCAT
"""

import re
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import argparse
import itertools
import os


parser = argparse.ArgumentParser()
parser.add_argument("input", help="input FASTQ file")
parser.add_argument("-r", "--restriction_enzyme", type=str, help="The restriction enzyme sequence you're searching for")
args = parser.parse_args()


print("counting records....")
with open(args.input) as input:
    num_lines = sum([1 for line in input])

total_records = int(num_lines / 4)



restriction_count_number = 0

with open(args.input) as f:
    seq_lines = itertools.islice(f, 1, None, 4)
    print('searching for: ' + args.restriction_enzyme)
    for line in seq_lines:
    	if args.restriction_enzyme in line:
    		restriction_count_number += 1

outstring1="Total number reads = %s" % total_records
print()
outstring2 = "The restriction enzyme sequence %s was found in %s number of reads" % ( args.restriction_enzyme, restriction_count_number)
print(outstring2)
print('Note some lines may contain the restriction sequence two or more times')
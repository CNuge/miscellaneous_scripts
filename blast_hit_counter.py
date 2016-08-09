#!/usr/bin/env python3

# This program is designed to take BLASTn output data in outfmt7 and output only the top hits

# into command line type the following:
#
# python3 Blastfilter_outfmt7.py Blast_output_file  -q Blast_query_file
#
#below is the argument parser that will take the command line options and pass them into the code
import argparse 

import numpy as np

import pandas as pd

from pandas import Series, DataFrame

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
parser.add_argument("-q", "--query_list", type=int, help="A fasta file with all of the sequences that you queried to produce the given blast output file")
args = parser.parse_args()


query_sequences = args.query_list
Blast_filename = args.input
making_XL = len(Blast_filename) - 4
output = 'Hit_count_' + Blast_filename[:making_XL] +'.xlsx'

##########################################################################################


Blast_hits = []
with open(Blast_filename) as file:
	for line in file:
		line_d = line.rstrip()
		dat = line_d.split()
		if line[0] == '#':
			continue
		else:
			Blast_hits.append(dat[0])
			
query_list = []


with open(query_sequences) as file:
	for line in file:
		if line[0] == '>':
			name = line[1:]
			query_list.append(name)
		else:
			continue
			
"""			
test run

Blast_hits = ['TP1','TP1','TP3','TP3','TP4','TP3']

query_list = ['TP1','TP2','TP3','TP4','TP5']


"""
		
blank_list = [0 for x in query_list]
query_count= DataFrame(blank_list, columns=['hit_count'], index=query_list)

for hit in Blast_hits:
	if hit in query_count.index:
		current = query_count.ix[hit]
		query_count.ix[hit] = current + 1
	else:
		continue
		

query_count.to_excel(output, 'Hit_count_data')




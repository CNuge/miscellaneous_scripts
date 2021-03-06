#!/usr/bin/env python3

"""

inputs:
fastq file
barcode/individual file

input format:

py3 fastq_barcode_splitter.py input_datafile.fastq -d Barcode_datafile.txt

then:
- a second program that runs fastq_searcher.py for each of the files in the output folder
	- writes a file with the total reads in each and the # of times that the given sequence arises.
	- need it to count not just the lines but the # of times its in the sequence
		import grep and run it in the 
import re
import sys
file = open(file.fastq, "r")
for line in file:
	   if re.search("query", line):
	   	count += 1

Barcode file in the following format:
-sex column is optional depending on your purpose. Its only used by the follow up program

Lane	Barcode	Sample	Sex
4	TTGA	GBS_F	F
4	CTAGAA	GBS_F	F
4	CGTAGGA	GBS_F	F
4	TGGTCAG	GBS_M	M
4	TTAACGA	GBS_M	M


"""

import re
import sys
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import argparse
import itertools
import os
import shutil 

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input FASTQ filename")
parser.add_argument("-d","--datafile", help="input a tab delimited .txt file with the following columns:\n Lane\tBarcode\tSample\tSex")
parser.add_argument("-r", "--restriction_enzyme", type=str, help="The restriction enzyme sequence you're searching for")
args = parser.parse_args()

num_lines = 0
print("counting reads....")
with open(args.input) as input:
	for line in input:
		num_lines += 1

print('loading datafile...')
datafile = pd.read_table(args.datafile,sep='\t')
Individuals_List = list(set(datafile['Sample'].tolist()))


outfiles = ['No_Barcode']
for x in Individuals_List:
	outfiles.append(x)

for name in outfiles:
	filename = name + '.fastq'
	open(filename, 'w')
	


barcode_dict= {}
index = datafile.index
for x in index:
	name = datafile['Sample'][x]
	barcode = datafile['Barcode'][x]
	if name in barcode_dict:
		barcode_dict[barcode].append(name) 
	else:
		barcode_dict[barcode] = name
	


print('sorting reads...')
record_number = 0
with open(args.input) as input:
		for line1 in input:
			line2 = next(input)
			line3 = next(input)
			line4 = next(input)
			for seq in datafile['Barcode']:
				if line2[:len(seq)] == seq:
					line2alt = line2[len(seq):]
					to_file_x = barcode_dict[seq]
					file_append = to_file_x + '.fastq'
					with open(file_append, "a") as outfile:
						outfile.write(line1)
						outfile.write(line2alt)
						outfile.write(line3)
						outfile.write(line4)
						break
			else: 
				to_file_x =  'No_Barcode.fastq'
				with open(to_file_x , "a") as outfile:
					outfile.write(line1)
					outfile.write(line2)
					outfile.write(line3)
					outfile.write(line4)	
			record_number += 1
			if record_number % 100000 == 0:
				print(str(((record_number * 4) / num_lines) * 100)  + " % done")

print('making output folder...')

dir_name= 'Sorted_reads'

here_we_are = os.getcwd()

new_dir = here_we_are + '/' + dir_name

if not os.path.exists(new_dir):
	os.makedirs(new_dir)

for name in outfiles:
	filename= here_we_are + '/' + name + '.fastq'
	newfilename = new_dir + '/' + name + '.fastq'	
	shutil.move(filename, newfilename )
#need to then make a program that will read through each of the files and
# add a new column to the current _data_ file with a number of restriction sites count
# and the 









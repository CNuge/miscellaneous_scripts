#!/usr/bin/env python3

"""
This file takes a folder filled with .fastq files and will search all of them for a given
sequence.
You must be outside the folder, in a directory containing this file and the desired folder

It will search all files in the folder and count the number of times the given sequence is seen in each.
The results will be printed to 'Summary_file.txt' in the directory
Summary file will have a tab delimited array containing the following:
Filename 	Number of reads	Number of times restriction sequence was seen	Number of reads with restriction enzyme sequence
file1.txt	400000			2000											1738																	

input the following:

python3 fastq_batch_searcher.py  folder_name -r ATGCAT

where ATGCAT is the sequence you're searching for and folder_name is the folder contianing the fastq files
"""

import argparse
import itertools
parser = argparse.ArgumentParser()
parser.add_argument("input", help="input folder containing Fastq files ")
parser.add_argument("-r", "--restriction_enzyme", type=str, help="The restriction enzyme sequence you're searching for")
args = parser.parse_args()

#open the directory
dir_name= input
here_we_are = os.getcwd()
new_dir = here_we_are + '/' + dir_name
os.chdir(new_dir)


header = 'File\tNumber of reads\tNumber of times restriction sequence was seen\tNumber of reads with restriction enzyme sequence'
filex = open('Summary_file.txt','w')
filex.write(header)
filex.close()


for file in new_dir:
	update = 	"counting records from file" + file
	print(update)
	with open(file) as input:
    	num_lines = sum([1 for line in input])

	total_records = int(num_lines / 4)

	restriction_count_number = 0
	num_of_lines = 0

	with open(file) as f:
    	seq_lines = itertools.islice(f, 1, None, 4)
    	print('searching for: ' + args.restriction_enzyme +'in ' + file)
    	for line in seq_lines:
    		if args.restriction_enzyme in line:
    			num_of_times = line.count(args.restriction_enzyme)
    			restriction_count_number += num_of_times
				num_of_lines = +=1

	outstring1="\s\t\d\t\d\t\d\n" % (file, total_records, restriction_count_number, num_of_lines)
	with open('Summary_file.txt', "a") as outfile:
    	outfile.write(outstring1)
	outstring2 = "The restriction enzyme sequence %s was found in %s" % ( args.restriction_enzyme, file)
	print(outstring2)



os.chdir('..')
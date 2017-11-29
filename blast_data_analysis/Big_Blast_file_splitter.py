#!/usr/local/bin/python

import argparse 
from tailhead import tail

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
parser.add_argument("-s", "--size", type=int, help="The number of lines for each output file", default=1000000)

args = parser.parse_args()

output_shell = '_split_' + args.input

Blast_hits = []
counter = 0
file_num = 1

with open(args.input) as file:
	for line in file:
		if line[0] == '#':
			continue
		else:
			if counter < args.size:
				current_file = str(file_num)+output_shell
				file=open(current_file,'a+')
				file.write(line)
				file.close()
				counter += 1
			else:	
				
				current_file =  str(file_num)+output_shell
				#getting the lines for comparison
				#line in for loop
				line_d = line.rstrip()
				overflow_line = line_d.split()
				#line from end of last file
				file_end = tail(open(current_file , 'rb'), 1)
				last_line = file_end[0]
				last_line_prev = last_line.split()
				compare_line = last_line_prev[0].decode('utf-8')
				#compare the lines
				if overflow_line[0] == compare_line:
					#if same query put it in the old file
					file=open(current_file,'a+')
					file.write(line)
					file.close()
					counter += 1
				else:	
					#if different query
					#file name changes
					#add it to the new file
					file_num += 1
					current_file =  str(file_num)+output_shell
					file=open(current_file,'a+')
					file.write(line)
					file.close()
					counter = 0
				

#!/usr/bin/env python3

"""
Use this to merge a bunch of large split files into a single output with all
superfluous information removed
you should: 
1. make the ouput file (touch)
2. run a shell script that runs the following program on each of the files you want to merge,
	all directed towards the same -d output file
3. Reason for doing this is that it lets you get all the information in one spot, without
	having a giant ass file to deal with it. 
	Its smaller in size and then you can run Blastfilter and Blastcounter on 
	only the important information.
	
"""
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
parser.add_argument("-d", "--destination", type=str, help="Input the name of the file you want the data to be written to")
args = parser.parse_args()

Blast_filename = args.input

Blast_hits = []
with open(Blast_filename) as file:
	for line in file:
		line_d = line.rstrip()
		dat = line_d.split()
		if line[0] == '#':
			continue
		else:
			Blast_hits.append(dat)

Outstring = ''
for x in Blast_hits:
	y = '\t'.join(x)	
	z = y + '\n'
	Outstring += z


with open(args.destination, "a") as outfile:
    outfile.write(Outstring)
    file.close()
  

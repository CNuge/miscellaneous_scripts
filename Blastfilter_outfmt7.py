#!/usr/bin/env python3

# This program is designed to take BLASTn output data in outfmt7 and output only the top hits

# into command line type the following:
#
# python3 Blastfilter_outfmt7.py input_file_name -f number
#
# where number corresponds to which of the following you wish to filter based on:
#	1			2			3			4					5			6			7			8		9			10		11		12
#	query id 	subject id 	% identity	alignment length	mismatches 	gap opens	q. start	q. end	s. start	s. end	evalue	bit score
#	TP13970		Ssa06		95.31		64					2			1			1			64		3119453		3119515	9e-021	98.7

# i.e. '11' would be e-value, as it is the 11th column in outfmt7
# input file is a *.out from BLASTn outfmt7

# Two output files:
# Tophit_No_ties.out
# Tophit_ties.out
#
#Tophits are: 
# greater than for the following (highest number):
# 3 %identity , 4 alignmnet length , 5 mismatches, 6 gap opens, 12 bit score 
# less than for the following (lowest number):
# 11 e-value


#below is the argument parser that will take the command line options and pass them into the code
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
parser.add_argument("-f", "--filter_parameter", type=int, help="Input the column number you wish to filter your Blast outputs by\nquick reference: 3 % identity , 4 alignmnet length , 5 mismatches, 6 gap opens, 11 e value, 12 bit score ")
args = parser.parse_args()



Blast_filename = args.input
output = 'FILTERED_' + Blast_filename
filter_parameter = args.filter_parameter
if filter_parameter == 11:
	G_OR_L = '<' 
else:
	G_OR_L = '>'


##########################################################################################
Tophit_output = 'TopHits' + output
Ties_output = 'Ties_TopHits' + output

Blast_hits = []
with open(Blast_filename) as file:
	for line in file:
		line_d = line.rstrip()
		dat = line_d.split()
		if line[0] == '#':
			continue
		else:
			Blast_hits.append(dat)

# TP13970	Ssa06_gi|830107324|gb|CM003284.1|	95.31	64	2	1	1	64	3119453	3119515	9e-021	98.7

Hit_Dict = {}


def hit_compare(new_hit, prev_hits, parameter, greater_or_less, new_dict):
	if greater_or_less == '>':
		variable = parameter - 1
		new_no = float(new_hit[variable])
		old_no = float(prev_hits[0][variable])
		if new_no > old_no:
			new_value = [new_hit]
			name = new_hit[0]
			new_dict[name] = new_value
		elif new_no == old_no:
			new_value = []
			for x in prev_hits:
				new_value.append(x)
			new_value.append(new_hit)
			new_dict[new_hit[0]] = new_value
		else:
			pass	
		
	
	elif greater_or_less == '<':
		variable = parameter - 1
		new_no = float(new_hit[variable])
		old_no = float(prev_hits[0][variable])
		if new_no < old_no:
			new_value = [new_hit]
			name = new_hit[0]
			new_dict[name] = new_value
		elif new_no == old_no:
			new_value = []
			for x in prev_hits:
				new_value.append(x)
			new_value.append(new_hit)
			new_dict[new_hit[0]] = new_value
		else:
			pass	
			
		


def hit_filter(List, parameter, greater_or_less, new_dict):
	for hit in List:
		name = hit[0]
		new_hit = [hit]
		check_dict = list(new_dict.keys())
		if name in check_dict:
			previous = new_dict[name]	
			hit_compare(hit, previous, parameter, greater_or_less, new_dict)					
		else:
			new_dict[name] = [hit]

hit_filter(Blast_hits, filter_parameter, G_OR_L, Hit_Dict)


# The above produces a filled, Hit_Dict, some with multiple associate values (ties)
# and some with only a single value (tophits, noties)
# Below sorts by key name, split the two values types into separate lists
Ties_list = []
Top_hits = []
Marker_list = list(Hit_Dict.keys())
Marker_list.sort()

#'TP13972'
#Hit_Dict['TP13971']
for marker in Marker_list:
	data = Hit_Dict[marker]
	if len(Hit_Dict[marker]) == 1:
		Top_hits.append(data)
	elif len(Hit_Dict[marker]) > 1:
		Ties_list.append(data)
	else:
		print('Problem in marker dictonary')
		

# this convert the lists to \n strings, where each individual hit is tab delimited

Top_hit_outstring = ''

for x in Top_hits:
	for imbed in x:
		y = '\t'.join(imbed)
		z = y + '\n'
		Top_hit_outstring += z
	

Ties_outstring = ''

for x in Ties_list:
	for imbed in x:
		y = '\t'.join(imbed)
		z = y + '\n'
		Ties_outstring += z

# this print to two files, ties and noties 

header = 'query id \tsubject id\t% identity\talignment length\tmismatches\tgap opens\tq. start\tq. end\ts. start\ts. end\tevalue\tbit score\n'

file=open(Tophit_output,'w')
file.write('Top BLASTn Hits, for subject sequences, consult tie file to see markers with equal top hits to two or more locations\n')
file.write(header)
file.write(Top_hit_outstring)
file.close()


file=open(Ties_output,'w')
file.write('Subject sequences that displayed equal top hits to two or more locations based on filter criteria\nAll equal top hits for each marker are listed below\n')
file.write(header)
file.write(Ties_outstring)
file.close()








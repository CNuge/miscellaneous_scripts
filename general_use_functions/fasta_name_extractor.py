
""" take a fasta file, and extract just the names of the sequences"""

fasta_file = 'input.fasta'

output = 'fasta_names.txt'

names=[]
with open(fasta_file) as file:
	for line in file:
		if line[0] == '>':
			name = line[1:]
			names.append(name)
		
name_string = '\n'.join(names)
outfile=open(output,'w')
outfile.write(name_string)
outfile.close()

# Take a .txt input that is \t delimited
# Column 1 is SNP name, Column 2 is Blast hit location
# Make a dictionary with the SNP names as the keys and the Hits as the
# Print to a comma delimited file with all hit locations combined to a single cell 
#i.e.:
# TP1234	Ssa01/Ssa07/Ssa12 
# TP8783	Ssa29/Ssa19/Ssa01


Blast_filename = 'Omy_PolyA_ties.txt'
output = 'Omy_PolyA_ties_consolidated.txt'

with open(Blast_filename) as f:
    Location_List = [line.rstrip() for line in f]


SNP_Hit_List = []
for SNP in Location_List:
	new = SNP.split()
	x = []
	x = [new[0] ,new[1]]
	SNP_Hit_List.append(x)

# Take the SNPs, if the SNP is already in dict it adds the location to the values
# else it makes a new key and value

SNP_dict = {}	
for SNP in SNP_Hit_List:
	SNPkey = SNP[0]
	value = SNP[1]
	if SNPkey in SNP_dict.keys():
		SNP_dict[SNPkey].append(value)
	else:	
		SNP_dict[SNPkey] = [value]
		


Print_list = []
for key in SNP_dict:
	values = SNP_dict[key]
	values.sort()
	values_out = '/'.join(values)
	out = [key,values_out]
	Print_list.append(out)

outstring=''

for x in Print_list:
	data = '\t'.join(x)
	tempstring= data +'\n'
	outstring += tempstring


header = 'marker\tSsa_Hit_Locations\n'

file=open(output,'w')
file.write(header)
file.write(outstring)
file.close()
	
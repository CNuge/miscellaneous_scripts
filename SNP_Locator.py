#!/usr/bin/env python3

#This code takes a .FASTA that lists both the query and hits outputs from 
#Tassel 3.0, locates the bp where the SNP is located and returns
#this information and the # of bp either side of the SNP

with open('HapMap.fas.txt') as f:
    SNPList = [line.rstrip() for line in f]

#This separates the input into the sequence data and the fasta names
#relies on the fact that they come one after the other in the input file

Names = SNPList[0:len(SNPList):2]

Sequence = SNPList[1:len(SNPList):2]


#Merge the two lists into a single dictionary, thereby pairing sequence data with its ID

FASTApair = dict(zip(Names, Sequence))


#Empty dict to start
query = {}
hit = {}

for key in list(FASTApair.keys()):
	if key[-9:-2] == '_query_':
		name = key[:-9]
		seq = FASTApair[key]
		query[name] = seq
	
	elif key[-7:-2] == '_hit_':
		name = key[:-7]
		seq = FASTApair[key]
		hit[name] = seq
	else:
		print('bad SNP name up in this joint:', key)

# Now have two dictionaries, one with hits and one with queries
# can compare the values in the two to see where the SNP difference is		

SNP_locations = []

for key in list(query.keys()):
	SNP = key
	query_seq = query[key]
	hit_seq = hit[key]
	pos = 1
	while query_seq != '':
		if query_seq[0] != hit_seq[0]:
			SNP_locations.append([SNP,pos,query_seq[0],hit_seq[0]])
			break	
		elif query_seq[0] == hit_seq[0]:
			query_seq = query_seq[1:]
			hit_seq = hit_seq[1:]
			pos += 1
			continue
	
#cleanup, turn into a series of strings, and adding \n

SNP_locations.sort()
Final_List = []

for x in SNP_locations:
	name = x[0]
	position = str(x[1])
	allele1 = x[2]
	allele2 = x[3]
	z = '%s,%s,%s,%s' % (name, position, allele1, allele2)
	Final_List.append(z)
	
header ='SNP,bp_location,query_allele,hit_allele\n'
output = '\n'.join([str(x) for x in Final_List])

#Print the output with a header
file = open('List_SNP_locations.txt','w')
file.write(header)
file.write(output)
file.close()




		

		
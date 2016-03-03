

#Take a GBS HapMap output with only genotypes and SNP names
# Take this information and produce a OneMap genotype file

#End goal is:
# *MarkerName D2.15	a,ab,a,-,ab,etc.
filename = 'GBS_Add_Data.txt'
filenameOut= 'OneMap-' + filename 
HetOut= 'Het-Het_Markers_' + filename

with open(filename) as f:
    SNPList = [line.rstrip() for line in f]

Fish_Ids = SNPList[0]

geno_list = []

for SNP in SNPList:
	new = SNP.split()
	geno_list.append(new)
# the following function will replace the GBS genotype coding with equivalent onemap coding
# will return a second variable that allows the SNP to be piped to either the mapping
# list or the Het-Het list

def M_het_code_changer(old_list, new_list, fgeno, mgeno):
	for x in old_list:
		if x == fgeno:
			new_list.append('a')
		elif x == mgeno:
			new_list.append('ab')
		elif x != mgeno and x != fgeno:
			new_list.append('-')
		
def F_het_code_changer(old_list, new_list, fgeno, mgeno):
	for x in old_list:
		if x == mgeno:
			new_list.append('a')
		elif x == fgeno:
			new_list.append('ab')
		elif x != mgeno and x != fgeno:
			new_list.append('-')

# This function takes the het-het inputs and codes it as OneMap based on the given het-het genotype alleles

def het_het_code_changer(old_list, new_list, fgeno, mgeno):
	if (fgeno == 'M' or fgeno == 'R' or fgeno == 'W' or fgeno == 'S' or fgeno == 'Y' or fgeno == 'K') and (mgeno == fgeno):
		hetero = fgeno
		if hetero == 'M':
			for x in old_list:
				if x == 'A':
					new_list.append('a')
				if x == 'C':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'A' and x != 'C' and x != hetero:
					new_list.append('-')
		elif hetero == 'R':
			for x in old_list:
				if x == 'A':
					new_list.append('a')
				if x == 'G':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'A' and x != 'G' and x != hetero:
					new_list.append('-')
		elif hetero == 'W':
			for x in old_list:
				if x == 'A':
					new_list.append('a')
				if x == 'T':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'A' and x != 'T' and x != hetero:
					new_list.append('-')								
		elif hetero == 'S':
			for x in old_list:
				if x == 'C':
					new_list.append('a')
				if x == 'G':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'G' and x != 'C' and x != hetero:
					new_list.append('-')
		elif hetero == 'Y':
			for x in old_list:
				if x == 'C':
					new_list.append('a')
				if x == 'T':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'T' and x != 'C' and x != hetero:
					new_list.append('-')
		elif hetero == 'K':
			for x in old_list:
				if x == 'T':
					new_list.append('a')
				if x == 'G':
					new_list.append('b')	
				elif x == hetero:
					new_list.append('ab')
				elif x != 'G' and x != 'T' and x != hetero:
					new_list.append('-')					
					
										
	else:
		print('SNP exists that is neither a single-het or a het-het, check parent genotypes!')
		print(fgeno, mgeno, old_list)
		


OneMapList = []
HetHetList=[]

#The following function takes the list of SNPs in the dataset and pipes them to the necessary cross conversion based
# on the parental genotypes.
#Markers are evaluated by one of 3 functions above, based on which parent(s) is heterozygous
# genolist[1] is female, genolist[2] is male
def geno_convert(genolist):
	if (genolist[1] == 'A' or genolist[1] == 'C' or genolist[1] == 'G' or genolist[1] == 'T')  and (genolist[2] == 'M' or genolist[2] == 'R' or genolist[2] == 'W' or genolist[2] == 'S' or genolist[2] == 'Y' or genolist[2] == 'K'):
		name = genolist[0]
		genos = []
		M_het_code_changer(genolist[3:], genos, genolist[1], genolist[2])
		OneMapList.append([name,'D2.15' ,genos])
		
	elif (genolist[1] == 'M' or genolist[1] == 'R' or genolist[1] == 'W' or genolist[1] == 'S' or genolist[1] == 'Y' or genolist[1] == 'K') and (genolist[2] == 'A' or genolist[2] == 'C' or genolist[2] == 'G' or genolist[2] == 'T'):
		name = genolist[0]
		genos = []
		F_het_code_changer(genolist[3:], genos, genolist[1], genolist[2])
		OneMapList.append([name,'D1.10' ,genos])
	
	elif (genolist[1] == 'M' or genolist[1] == 'R' or genolist[1] == 'W' or genolist[1] == 'S' or genolist[1] == 'Y' or genolist[1] == 'K') and (genolist[2] == 'M' or genolist[2] == 'R' or genolist[2] == 'W' or genolist[2] == 'S' or genolist[2] == 'Y' or genolist[2] == 'K'):
		name = genolist[0]
		genos = []
		het_het_code_changer(genolist[3:], genos, genolist[1], genolist[2])
		HetHetList.append([name, 'B3.7', genos])
	
	else:
		pass
		
		
for SNP in geno_list:
	geno_convert(SNP)
	
# Next Section writes OneMapList and HetHetList lists to separate files.


#Writing output OneMap file
OneMap_Out = []
for SNP in OneMapList:
	outstring = ''
	data_list = SNP[2]
	data_string = ','.join(data_list)
	outstring = '*%s %s\t%s' % (SNP[0], SNP[1], data_string)
	OneMap_Out.append(outstring)

#These next lines extract the number of markers and number of progeny for
# first line in OneMap

Marker_No = len(OneMap_Out)
Progeny_No = len(OneMapList[0][2])		
header = str(Progeny_No) + ' ' + str(Marker_No) + '\n'		
output = '\n'.join([str(x) for x in OneMap_Out])

file = open(filenameOut,'w')
file.write(header)
file.write(output)
file.close()


#Below creates the file with the het-het SNPs in a separate file
HetHet_Out =[]
Het_Marker_No = len(HetHetList)
header = str(Progeny_No) + ' ' + str(Het_Marker_No) + '\n'

HetHetList

for SNP in HetHetList:
	outstring = ''
	data_list = SNP[2]
	data_string = ','.join(data_list)
	outstring = '*%s %s\t%s' % (SNP[0], SNP[1], data_string)
	HetHet_Out.append(outstring)

HetOutput = '\n'.join([str(x) for x in HetHet_Out])

file = open(HetOut,'w')
file.write(header)
file.write(HetOutput)
file.close()









	
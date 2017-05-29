

#Take a GBS HapMap output with only genotypes and SNP names
# Take this information and produce a OneMap genotype file

#End goal is:
# 

Map_filename = 'Male_map_markers.txt'

Add_filename = 'Male_add_markers.txt'

with open(Map_filename) as f:
    Map_List = [line.rstrip() for line in f]

Map_List = Map_List[1:]
Map_Data = []
Starred_removed = []
#The star bit here removes the het-hets and leaves just the core file

for SNP in Map_List:
	new = SNP.split()
	if new[0][-1] == '*':
		Starred_removed.append(new)
	else:
		Map_Data.append(new)

with open(Add_filename) as f:
    Add_List = [line.rstrip() for line in f]

Add_List = Add_List[1:]
Add_Data = []
for SNP in Add_List:
	new = SNP.split()
	Add_Data.append(new)

Starred_Out = ''
for SNP in Starred_removed:
	z = ','.join(SNP)
	Starred_Out += z + '\n'

#This next code bit only works if the LG names are the same in the add and the map lists so 
# make sure to double check that!!!

LG_dict = {}

for SNP in Map_Data:
	SNPkey = SNP[1]
	value = SNP
	if SNPkey in LG_dict.keys():
		LG_dict[SNPkey].append(value)
	else:	
		
		LG_dict[SNPkey] = [value]
	

for SNP in Add_Data:
	SNPkey = SNP[1]
	value = SNP
	if SNPkey in LG_dict.keys():
		LG_dict[SNPkey].append(value)
	else:	
		LG_dict[SNPkey] = [value]


#Two lists now merged into one dictionary that is split by Keys = Linkage groups



OneMap_Codes = ''
for k in LG_dict:
	name = k
	values = LG_dict[k]
	OneString = ''
	for x in values:
		z = str(x[3])
		if x == values[len(values) -1]:
			tempstring = z
			OneString += tempstring
		else:
			tempstring = z+','
			OneString += tempstring
	add_to_output= '%s\nc=(%s)\n\n' % (k, OneString)
	OneMap_Codes +=add_to_output
		
	#something here along the lines of for list of values for K
	#make a list of just the OneMap codes
	#make a string with the name and the codes and add to OneMap_Order_List
	#i.e. 'AC12 = c(24,56,3232,45453,2331,343)'
	

#then print Three files:
	# one with the OneMap order strings
	# one with the Markers and all info in the LG_dict
	# one with just the het-hets removed from the MapList to add in later.

# making string for Markers in LG_dict
Markers_in_OneMap_Work = ''
for k in LG_dict:
	name = k
	values = LG_dict[k]
	LGstring = ''
	for x in values:
		z = ','.join(x)
		tempstring = k+','+ z +'\n'
		LGstring += tempstring
	Markers_in_OneMap_Work += LGstring




file=open('Markers_in_OneMap.txt','w')
file.write(Markers_in_OneMap_Work)
file.close()

file = open('Map_starred_markers_removed.txt','w')
file.write(Starred_Out)
file.close()

file = open('OneMap_marker_order_lists.txt','w')
file.write('\n\n')
file.write(OneMap_Codes)
file.close()









	
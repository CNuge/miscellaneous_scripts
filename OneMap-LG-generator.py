
#This program takes 3 inputs:
# a list of markers and their Position in the following format:
#Change the file names on lines 35, 46 and 54, output name at end
	#1	TP20164	AC-1 D1.10
	#2	TP30004	AC-1 D2.15
	#3	TP39583	AC-1 D2.15
	#4	TP26151	AC-1 D1.10
	#5	TP23571	AC-1 B3.7
	#6	TP7399	AC-1 B3.7 

# Need the MapManipulation.py M and F outputs as well to split based on maps
# Here is what those outputs look like:
#Replace \n\n with \n prior to running file
#* on end of marker names are acceptable
	#AC-1f,TP7399,11.7
	#AC-1f,TP13505,43.5
	#AC-1f,TP31245,38.8
	#AC-1f,TP13573,45.8
	#AC-1f,TP41143,25.8
	
###########################################################	
#See Line 88 to change how non-map SNPs are designated!!!
#Depends on the codes you've got in column 3 of the marker list file
###########################################################	
	
# It will split the markers based on their LG (and/or other category)
# Will return a list of all markers for each LG in the OneMap number designations corresponding to
# the markers positions in the input file in the male and female maps





with open('Markers_OneMap_File_Positions.txt') as f:
    MarkerFile = [line.rstrip() for line in f]

FilePositions = []
for x in MarkerFile:
	z = x.split()  
	FilePositions.append(z)


#Input these two lists, only need the SNP names in the list, comparing for
#existence, LG info is in Filepositions
with open('OutAC-FemaleMerged.map.txt') as LadyIn:
     Finfo= [line.rstrip() for line in LadyIn]

InputFemaleMap = []    
for x in Finfo: 
	z = x.split(',')  
	InputFemaleMap.append(z)  
		  
with open('OutAC-MaleMerged.map.txt') as DudeIn:
    Minfo = [line.rstrip() for line in DudeIn]
	
InputMaleMap = []
for x in Minfo: 
	y = x.split(',')  
	InputMaleMap.append(y)
	
	
Female_list = []
for L in InputFemaleMap:
	SNPname = L[1]
	if SNPname[-1] == '*':
		SNPname = SNPname[:-1]
	Female_list.append(SNPname)
	
Male_list = []
for line in InputMaleMap:
	SNPname = line[1]
	if SNPname[-1] == '*':
		SNPname = SNPname[:-1]
	Male_list.append(SNPname)


MaleMap = []
FemaleMap = []
Additions = []

#def __eq__(self, other):

for SNP in FilePositions:
	z = SNP[1]
	for x in Male_list:
		if z == x:
			MaleMap.append(SNP)
	for x in Female_list:
		if z == x:
			FemaleMap.append(SNP)

###Hey its the Old man from line 12!!!!	
for SNP in FilePositions:
	x = SNP[2]
	if x == 'SegDistortionHH' or x == 'MsatDrop' or x =='SegDistortionSH':
		Additions.append(SNP)
	
#Have five lists:
	#placed Male markers, 
	#placed female markers 
	#m unplaced markers
	#f unplaced markers.
	#het_het unplaced markers

###########################################
###########################################
#From Male and Female Markers, must further split by LGs


#make a set of lists from all the LG names

MaleLG_dict = dict()

for line in MaleMap:
    if line[2] in MaleLG_dict:
        # append the new number to the existing array at this slot
        MaleLG_dict[line[2]].append(line[0])
    else:
        # create a new array in this slot
        MaleLG_dict[line[2]] = [line[0]]

FemaleLG_dict = dict()

for line in FemaleMap:
    if line[2] in FemaleLG_dict:
        # append the new number to the existing array at this slot
        FemaleLG_dict[line[2]].append(line[0])
    else:
        # create a new array in this slot
        FemaleLG_dict[line[2]] = [line[0]]

LGoutstring =''

Malekeylist = MaleLG_dict.keys()
Malekeylist = sorted(Malekeylist)
for key in Malekeylist:
	LGoutstring += key
	LGoutstring += ' Male'
	LGoutstring += '\n'
	markerlist= MaleLG_dict[key]
	s = ','.join(markerlist)
	LGoutstring += s
	LGoutstring += '\n'
	LGoutstring += '\n'

Femalekeylist = FemaleLG_dict.keys()
Femalekeylist = sorted(Femalekeylist)
for key in Femalekeylist:
	LGoutstring += key
	LGoutstring += ' Female'
	LGoutstring += '\n'
	markerlist= FemaleLG_dict[key]
	s = ','.join(markerlist)
	LGoutstring += s
	LGoutstring += '\n'
	LGoutstring += '\n'


###########################################
###########################################


# making the unplaced marker lists
# splits the additions into different lists
# female and male (microsat inc) informative and the h-hs!

female_additions =[]
male_additions = []
het_het_additions = []
for x in Additions:
	gt_code = x[3]
	if gt_code == 'D1.10' or gt_code == 'D1.9' or gt_code == 'D1.11'or gt_code == 'D1.12' or gt_code == 'D1.13': #female Informative
		female_additions.append(x)
	elif gt_code == 'D2.14' or gt_code == 'D2.15' or gt_code == 'D2.16' or gt_code == 'D2.17' or gt_code == 'D2.18': #male informative
		male_additions.append(x)
	elif gt_code[0] == 'A': #both parent informative (microsats)
		male_additions.append(x)
		female_additions.append(x)
	elif gt_code == 'B3.7': #het-hets and some microsats
		if x[2] == 'MsatDrop':
			male_additions.append(x)
			female_additions.append(x)
		else:
			het_het_additions.append(x)




###################
# Making the output strings
#############
MaleMapNums = []
for x in MaleMap:
	designation = x[0]	
	MaleMapNums.append(designation)

MaleMapNums = sorted(MaleMapNums)	
MaleMapoutput = ','.join([str(x) for x in MaleMapNums])

FemaleMapNums = []
for x in FemaleMap:
	designation = x[0]	
	FemaleMapNums.append(designation)

FemaleMapNums = sorted(FemaleMapNums)	
FemaleMapoutput = ','.join([str(x) for x in FemaleMapNums])

male_add_out = []
for x in male_additions:
	marker = x[0]
	male_add_out.append(marker)

male_add_out = sorted(male_add_out)
MaleAddoutput = ','.join([str(x) for x in male_add_out])

female_add_out = []
for x in female_additions:
	marker = x[0]
	female_add_out.append(marker)

female_add_out=sorted(female_add_out)
FemaleAddoutput = ','.join([str(x) for x in female_add_out])

hethet_add_out = []
for x in het_het_additions:
	marker = x[0]
	hethet_add_out.append(marker)

female_add_out = sorted(female_add_out)
HetHetAddoutput = ','.join([str(x) for x in hethet_add_out])

###################
#Print the output with a header
file = open('Marker_Lists_for_OneMap.txt','w')

file.write('Male Map Markers:\n')
file.write(MaleMapoutput +'\n')
file.write('\n')
file.write('c('+ MaleMapoutput +')\n\n')

file.write('Female Map Markers:\n')
file.write(FemaleMapoutput +'\n')
file.write('\n')
file.write('c('+FemaleMapoutput+')\n\n')


file.write('Male Add Markers:\n')
file.write(MaleAddoutput+'\n')
file.write('\n')
file.write('c('+MaleAddoutput+')\n\n')


file.write('Female Add Markers:\n')
file.write(FemaleAddoutput+'\n')
file.write('\n')
file.write('c('+FemaleAddoutput+')\n\n')

file.write('HetHet Add Markers:\n')
file.write(HetHetAddoutput+'\n')
file.write('\n')
file.write('c('+HetHetAddoutput+')\n\n')


file.write('\n\n\n\n')
file.write('Below are the markers split by LGs:\n')

file.write(LGoutstring)

#Add by LG here if necessary

file.close()


    

#This program takes a mapdis-v input file and outputs a .csv
# Also adds a first column that designates the LG for each marker directly

#Change input filename here
filename ='AC-MaleMerged.map'
filenameOut = 'Out'+filename+'.txt'

data2f = ''

#This may need to be simplified if existence as unicode was exception
#If just \n used chrom at start of next LG to produce
# a \n\n thereby making splits between LGs unique
import codecs
f = codecs.open(filename, encoding='utf-8')
for line in f:
    x = line
    data2f = data2f + x

fLGs2 = []
#Below line will need to be changed based on what is separating the 
#LGs in the mapdis-v file
fLGs2 = data2f.split('\r\n\r')

if fLGs2[0] == ' ':
	fLGs2 = fLGs2[1:]
	 
#fLGs2= fLGs2[1:]
if fLGs2[len(fLGs2)-1] == '\n':
	fLGs2.pop()


LG_List = []

for LG in fLGs2:
	x = (LG.split())
	Name = x[1]
	markers = x[2:len(x):2]
	distance = x[3:len(x):2]
	list = [Name, dict(zip(markers,distance))]
	LG_List.append(list)
	
Final_List = []
for LG in LG_List:
	outstring = ''
	D = LG[1]
	for key in LG[1]:
		x = '%s%s%s%s%s%s' % (LG[0],',',key,',',D[key],'\n')
		outstring += x
	Final_List.append(outstring)
		

		
output = '\n'.join([str(x) for x in Final_List])

file = open(filenameOut,'w')
file.write(output)
file.close()




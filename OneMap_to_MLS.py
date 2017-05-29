#This program will take the output marker orders from OneMap, with .rec.txt extensions
#and convert them to .mls format for LINKMFEX double check of marker ordering
#Place this program in the same directory as the desired files and it will do the rest


from os import listdir
from os.path import isfile, join
DirFiles = [f for f in listdir('./') if isfile(join('./', f))]

OneMap_Files = []

for x in DirFiles:
	if str(x[-8:]) == '.rec.txt':
		OneMap_Files.append(x)
	else:
		pass
		
def mls_maker(File):
	OrderFile = str(File)
	with open(OrderFile) as f:
		OneMap_Data = [line.rstrip() for line in f]
	mls_data=[OrderFile[:-8]]
	OneMap_Data.pop(0)
	for z in OneMap_Data:
		dat = z.split()
		marker = dat[1]
		mls_data.append(marker)
	outstring = '\n'.join(mls_data)
	newfile = OrderFile[:-8] + '.mls'
	file = open(newfile,'w')
	file.write(outstring)
	file.close()
    
for file in OneMap_Files:
	mls_maker(file)
    
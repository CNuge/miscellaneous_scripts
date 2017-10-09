
#these are the imports, anywhere you see pd is using pandas and os is using the os library
import pandas as pd
import os #import ability to interact with operating system


#use this to read in the files
x = pd.read_excel('example_file.xlsx',skiprows=3)


#use this to set up the for loop for all the file
#iterate through the files in the directory, getting all the csvs
xl_list = []
for file in os.listdir():
	if file[-4:] == 'xlsx':
		xl_list.append(file)


for file in xl_list:
	x = pd.read_excel(file,skiprows=3)
	x['d'] = x['d'].fillna('_')
	x['d'] = x['d'].apply(lambda y: y.strip().replace(' ', '_'))
	new_name = 'changed_' + file[:-5] + '.csv'
	x.to_csv(new_name,index=False)

#save the files as .csvs

# Then you can do a command replace on the files in any way you want,
# you don't need to overcomplicate it if you don't want to.

#how I would do it.




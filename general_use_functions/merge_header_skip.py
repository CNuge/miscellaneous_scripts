import os

merge_files = [x for x in os.listdir() if x[-4:] == '.lig']

if 'all_data.csv' in merge_files:
	merge_files.remove('all_data.lig')

output_name = 'all_data.csv'
data = open(output_name,'w')
#data.write('#put the header info here\n')
data.close()

for name in merge_files:
	new_col = name[:-4]
	with open(name) as file:
		data = open(output_name, 'a')
		for i, next_line in enumerate(file):
			if i != 0:
				line = next_line.rstrip()
				output = f'{new_col},{new_col},{line}\n'
				data.write(output)
		data.close()




import pandas as pd
from pandas import Series, DataFrame
from collections import defaultdict



male_groups = pd.read_table('male_strays.txt',sep='\t')


male_LG_names = list(male_groups['LG_name_col'].unique())


male_data_list = []

for row in male_groups.iterrows():
	dat = row[1]
	LG = dat['LG_name_col']
	marker_num  = dat['Marker_number']
	dat_tuple = (LG, marker_num)
	male_data_list.append(dat_tuple)
	
dict_of_LGs = defaultdict(list)

for LG, marker in male_data_list:
	dict_of_LGs[LG].append(marker)
	
	
male_outstring = ''

for group in dict_of_LGs.keys():
	list_of_markers = dict_of_LGs[group]
	string_of_markers = ','.join(str(x) for x in list_of_markers)
	outdat = '%s=make.seq(AFS_CZRI_hethet_twopt_hq,c(%s))\n%s\n\n' % (group , string_of_markers, group)
	male_outstring += outdat
	


female_groups = pd.read_table('female_strays.txt',sep='\t')


female_LG_names = list(female_groups['LG_name_col'].unique())


female_data_list = []

for row in female_groups.iterrows():
	dat = row[1]
	LG = dat['LG_name_col']
	marker_num  = dat['Marker_number']
	dat_tuple = (LG, marker_num)
	female_data_list.append(dat_tuple)
	
dict_of_LGs = defaultdict(list)

for LG, marker in female_data_list:
	dict_of_LGs[LG].append(marker)
	
	
female_outstring = ''

for group in dict_of_LGs.keys():
	list_of_markers = dict_of_LGs[group]
	string_of_markers = ','.join(str(x) for x in list_of_markers)
	outdat = '%s=make.seq(AFS_CZRI_hethet_twopt_hq,c(%s))\n%s\n\n' % (group , string_of_markers, group)
	female_outstring += outdat
	


file=open('LG_sequence_dat.txt', 'w')
file.write(male_outstring)
file.write('\n\n\n\n')
file.write(female_outstring)
file.close()
	 
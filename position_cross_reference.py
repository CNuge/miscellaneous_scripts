import pandas as pd
from pandas import Series, DataFrame

""" here I am using trimmed .vcf files to speed things gup. just the contig and pos
	columns. these can be isolated from a .vcf using the code:
	cat input.vcf | grep -v '##' | cut -f 1,2 > output_positions.txt """ 


def read_pos_dat(position_file):
	""" take the positions file and read in lines, adding info to a df """
	list_of_dat =[]
	with open(position_file) as file:
		for line in file:
			line_dat = line.rstrip().split('\t')
			designation = '%s_%s' % (line_dat[0], line_dat[1])
			list_of_dat.append([designation , line_dat[0], line_dat[1], 1])
	return list_of_dat

def pos_dat_to_df(list_of_pos_dat, individual_name):
	"""return the df of informaiton for that individual with columns:
		designation	contig	pos	individual_name	"""
	position_df = DataFrame(list_of_pos_dat, columns = ['designation', 'Contig', 'position', individual_name])
	return position_df


def merge_dict_of_df(dict_of_dfs, col_to_merge_by):
	""" take a dictonary of dataframes, merge them all to a single df based on
		the query column """
	first = list(dict_of_dfs.keys())[0]
	left = dict_of_dfs[first]
	for i in list(dict_of_dfs.keys())[1:]:
		right = dict_of_dfs[i]
		result = pd.merge(left, right, on=col_to_merge_by)
		left = result
	return left

if __name__ == '__main__':


	list_of_files = ['HI.3442.001.Index_2.Salp_J03B_positions.txt',
					'HI.3442.002.Index_13.Salp_J10A_positions.txt',
					'HI.3442.003.Index_6.Salp_J10B_positions.txt',
					'HI.3442.004.Index_15.Salp_J13B_positions.txt',
					'HI.3442.005.Index_7.Salp_J16B_positions.txt',
					'HI.3442.006.Index_18.Salp_J18A_positions.txt',
					'HI.3442.007.Index_14.Salp_J20A_positions.txt',
					'HI.3442.008.Index_16.Salp_J20B_positions.txt']

	df_dict = {}
	
	for text in list_of_files:
		""" construct the df for each snp, add results to dictonary """
		name = 'Koop_AC_' + text.split('.')[2]

		input_dat = read_pos_dat(text)

		df_dict[name] = pos_dat_to_df(input_dat, name)

	df_dict.keys()
	output_df = merge_dict_of_df(df_dict,'designation')
	output_df.head()
	output_df.to_csv('koop_merged_dataframe_snp_locations.tsv', sep='\t')









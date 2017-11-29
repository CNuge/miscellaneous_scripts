import pandas as pd
from pandas import Series, DataFrame
import numpy as np

def cluster_representitives(data):
	""" take a datframe with 'LG', 'map_distance', 'marker'"""
	""" pull the cluster representitives from large df"""

	data['full_designation'] = data['cluster'] + data['LG']

	representitives = DataFrame(columns = data.columns)
	positions_used = []

	for row in data.iterrows():
		position = row[1]['full_designation']
		if position in positions_used:
			#skip the 2nd -> nth marker in a cluster
			continue
		elif (row[1]['map_distance'] == '-' ):
			#remove the unordered markers
			continue
		else:
			representitives = representitives.append(row[1])
			positions_used.append(position)
	return representitives

def grid_qtl_writer(marker_dataframe, outfile):
	""" take a datframe with 'LG', 'map_distance', 'marker'"""
	""" use this data to write the gridQTL map file """
	outstring = ''
	#group markers by the linkage group column
	lg_groups = marker_dataframe.groupby(['LG'])
	#add the first header line
	outstring += str(len(lg_groups))+'\n1\n'
	for lg in lg_groups:
		#number of markers for line 1
		marker_number = len(lg[1]['marker'])
		order_string = lg[0] + ' ' + str(len(lg[1]['marker'])) + ' 1\n'
		prev_cM = 0
		#build the string, adding the seed marker
		#then adding the cM difference 
		#followed by the next marker (space delimited)
		for marker in lg[1].iterrows():
			if order_string[-1] == '\n':
				order_string += marker[1]['marker']
				order_string += ' '
			else:
				print(marker[1]['map_distance'])
				current_prev_difference = (float(marker[1]['map_distance']) - float(prev_cM))
				add_num = '%.1f' % current_prev_difference
				order_string += add_num 
				order_string += ' '
				order_string += marker[1]['marker']
				order_string += ' '
				prev_cM = marker[1]['map_distance']
				continue
		#replace final space with a newline, add to the outstring		
		outstring += order_string[:-1] +'\n'
	file=open(outfile,'w')
	file.write(outstring)
	file.close
	#return the string as well, in case we wish to store it or call it
	return outstring



if __name__ == '__main__':

	male_data = pd.read_table('male_map.tsv', sep = '\t')
	male_data = male_data.fillna('-')

	female_data = pd.read_table('female_map.tsv', sep = '\t')
	female_data = female_data.fillna('-')

	male_representitives = cluster_representitives(male_data)

	female_representitives = cluster_representitives(female_data)

	male_grid_map = grid_qtl_writer(male_representitives, 'male_gridQTL_map.txt')

	female_grid_map = grid_qtl_writer(female_representitives, 'female_gridQTL_map.txt')





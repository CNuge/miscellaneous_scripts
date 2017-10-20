import os
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt


"""
this set of programs will let you work with chromosome gene comparison files to identify
regions with abnormally high and low levels of synteny. You can also compare the index order 
of the gene pairs on the two chromosomes to see if there is homeologous gene order fielity
across the two chromosomes

"""



def read_homeology_file(filename ):
	""" specify the filename, along with the names of the chromosomes"""
	""" returns a dataframe with the names of the chromosomes involved """
	header = ['id1', 'pos1','description1','id2', 'pos2', 'description2']

	data = pd.read_csv(filename, skiprows= 1, names = header)

	return data



def homeologs_by_mb(df):
	""" take a homeology dataframe, count the number of homeologs per megabase """
	#break each chr's length up into 1mbp bins
	#note this only goes to the homeolog hit pos, not the absloute end of the chr 
	bin1 = [ x*1000000 for x in range(int(df['pos1'].max()/1000000)+1)]

	bin2 = [ x*1000000 for x in range(int(df['pos2'].max()/1000000)+1)]

	bin_counts1 = df.groupby(pd.cut(df['pos1'], bins=bin1)).size()

	bin_counts2 = df.groupby(pd.cut(df['pos2'], bins=bin2)).size()

	return bin_counts1, bin_counts2



def homeolog_order_blocks(df):
	""" sorts and indexes based off of the first chr's bp positions, 
		then sorts based on the second chr and returns the order of the
		first chr's homeologs on the second """
	#sort by the positions on the first chr
	data = df.sort_values(by=['pos1'])
	#reindex base on the sorted df
	data.reindex()
	#sort by the positions on the second chromosomes
	data.sort_values(by=['pos2'], inplace = True)

	return list(data.index)



def synteny_blocks(chr_pos):
	""" pass in a list of the numeric positions of genes on chromosome one,
		in their order on chromosome two. Assess the lengths of synteny blocks
		and return a df with starting index, and the len of the synteny """
	list_of_synteny_blocks = []
	current_block = []
	for pos in chr_pos:
		if current_block == []:
			current_block.append(pos)

		elif ((current_block[-1] - 1) == pos) or ((current_block[-1] + 1) == pos):
			current_block.append(pos)
		else:
			#end of previous synteny block, append its length and its starting position to 
			#the list of synteny blocks and begin a new current block
			end_of_s = (np.min(current_block), len(current_block))
			list_of_synteny_blocks.append(end_of_s)
			current_block = [pos]
	#add on the last members
	end_of_s = (np.min(current_block), len(current_block))
	list_of_synteny_blocks.append(end_of_s)
	df = DataFrame(list_of_synteny_blocks, columns = ['block_start', 'block_len'] )
	return df




def hist_synteny_blocks(list_of_lengths, filename):
	plt.hist(list_of_lengths, color='blue')
	plt.title('Length of syntenic gene order block lengths on chromosome pairing')
	plt.xlabel('Length of Synteny Blocks')
	plt.ylabel('Frequency')
	plt.savefig(filename)


if __name__ == '__main__':

	files = [x for x in os.listdir() if '.csv' in x]

	for i in files:

		#replace this with a loop for a the .csv in the dir
		split_name = i.split('+')
		
		chr1 = split_name[0].split()[-1] #split on whitespace, keep last bit
		chr2 = split_name[1].split('.')[0][1:] #split on the .csv, drop leading whitespace

		filename = i
		
		#read in the data
		data = read_homeology_file(filename)
		# get data on the number of homeologs per bin
		homeolog_bins = homeologs_by_mb(data)

		homeolog_output_1 = chr1 + '_matches_to' + chr2 + 'distribution.csv'

		homeolog_bins[0].to_csv(homeolog_output_1)

		homeolog_output_2 = chr2 + '_matches_to' + chr1 + 'distribution.csv'
		homeolog_bins[1].to_csv(homeolog_output_2)

		#
		gene_order_chr2 = homeolog_order_blocks(data)

		chr1_v_chr2_order = synteny_blocks(gene_order_chr2)

		synteny_output = chr1 +'_'+ chr2 + '_syntenic_order_regions.csv'

		chr1_v_chr2_order.to_csv(synteny_output, index=False)

		length_lists = list(chr1_v_chr2_order['block_len'])		

		graph_filename = chr1 +'_'+ chr2 +'_histogram.pdf'
		hist_synteny_blocks(length_lists, graph_filename)











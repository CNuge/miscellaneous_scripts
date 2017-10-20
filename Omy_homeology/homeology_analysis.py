
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
	bin1 = [ x*100000 for x in range(int(df['pos1'].max()/1000000)+1)]

	bin2 = [ x*100000 for x in range(int(df['pos2'].max()/1000000)+1)]

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

syn_dat = synteny_blocks(x)



def hist_synteny_blocks(list_of_lengths):
	plt.hist(list_of_lengths)
	plt.xlabel('Length of Synteny Blocks')
	plt.ylabel('Frequency')
	plt.show()


if __name__ == '__main__':

	#replace this with a loop for a the .csv in the dir

	filename = '1and2_homelogy.csv'
	
	#read in the data
	data = read_homeology_file(filename)
	# get data on the number of homeologs per bin
	homeolog_bins = homeologs_by_mb(data)

	#
	gene_order_chr2 = homeolog_order_blocks(data)

	chr1_v_chr2_order = synteny_blocks(gene_order_chr2)

	length_lists = list(chr1_v_chr2_order['block_len'])
	

	hist_synteny_blocks(length_lists)











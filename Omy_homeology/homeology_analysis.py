
import pandas as pd
from pandas import Series, DataFrame
import numpy as np



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

	data.sort_values(by=['pos1'], inplace = True)
	
	data.reindex()

	data.sort_values(by=['pos2'], inplace = True)

	return list(data.index)


# use homeolog_order_blocks to develop an 'index match score'
# this should take the index of the second chr relative to the first and
# give a score based on the number of adjacent #s that match, along
# with the overall median continious number string length (average combo match length)



if __name__ == '__main__':

	#replace this with a loop for a the .csv in the dir

	filename = '1and2_homelogy.csv'
	
	data = read_homeology_file(filename)

	homeolog_bins = homeologs_by_mb(data)

	homeolog_order_blocks(data)













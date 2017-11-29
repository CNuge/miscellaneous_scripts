#!/usr/local/bin/python3

import pandas as pd
from pandas import Series, DataFrame

class linkage_group: #this is a class holding the data from a linkage group
	def __init__ (self, groupby_obj):
		self.LG = groupby_obj 
		self.name = groupby_obj[0]
		#****NOTE****#
		#currently this is built from a .groupby() df, grouped by LG
		#could pass in a tuple if modelling one LG where:
		#groupby_obj = ('name', dataframe)
	def marker_grab(self, marker_column): #take in the markers for the LG, build a list
		self.markers = list(self.LG[1][marker_column])
	def genotypes_grab(self, geno_df): #grab the onemap input file, pull the relevant lines
		self.genotypes = []
		geno_sample = geno_df.ix[0][1].split(',') 
		#note this relies on the marker name being the df index
		#change slicing or load df differently otherwise
		self.geno_num = len(geno_sample)
		for marker in geno_df.iterrows():
			name = marker[0][1:]
			if name in self.markers:
				self.genotypes.append(marker)
			else:
				continue
	def print_genotypes(self): #this will take the marker list and make an LG specific input file
		filename = str(self.name + '_markers.txt')
		outstring = '%s %s\n' % (self.geno_num , len(self.markers))
		for i in self.genotypes: #take self.genotypes, iterate through and build a string
			marker_dat = '%s %s\t%s\n' % (i[0] , i[1][0], i[1][1])
			outstring += marker_dat
		file = open(filename, 'w') #print the outstring to the passed in filename
		file.write(outstring)
		file.close()


if __name__ == '__main__':
	#read in the files
	#the list of marker assignments
	linkage_group_assignments = pd.read_table('linkage_group_assignments.txt',  sep = '\t')
	
	#all the markers
	all_markers = pd.read_table('CZRI_ALL_SNPs.txt', delim_whitespace = True)
	
	#group the list of marker assignments table by the linkage group column.
	grouped_LGs = linkage_group_assignments.groupby('LG_name_col')
	
	#initiate a class instance for each linkage group in the marker assignments groupby frame
	LG_instancelist = [linkage_group(i) for i in grouped_LGs]
	
	#iterate through the list of LG_class objects, producing the output for each
	for group in LG_instancelist:
		group.marker_grab('Marker_name')	#grab the markers to a list, pass in the column name
		group.genotypes_grab(all_markers)	#get the genotypes for all the markers in the LG
		group.print_genotypes()


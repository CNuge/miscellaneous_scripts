import pandas as pd
from pandas import Series, DataFrame

def pwd_reader(pwd_file):
	"""this takes a pwd file and turns it in to a pandas dataframe"""
	headers=['1st_locus', '2nd_locus','rec','LOD','N']
	table_in = pd.read_table(pwd_file, skiprows=3, names = headers, delim_whitespace=True)
	table_in['1st_locus'] = table_in['1st_locus'].map(lambda x: str(x)[:-1])
	table_in['2nd_locus'] = table_in['2nd_locus'].map(lambda x: str(x)[:-1])
	return table_in
	

def flank_marker_reader(flank_csv_file):
	"""This will read in a flank markers, ignoring the bottom of the file """
	file_lines = []
	with open(flank_csv_file) as file:
		for n, line in enumerate(file):
			if (n == 0) or (n == 1):
				continue
			else:
				while True:
					x = file.__next__().strip()
					if x == '':
						return file_lines
					else:
						file_lines.append(x)
						
def flank_markers_to_table(flank_marker_reader_output):	
	"""queries with two flanking positions to dataframe"""
	list_of_good_lines = []
	for line in flank_marker_reader_output:
		list_line = line.split(',')
		if len(list_line) > 4:
			continue
		else:
			list_line= list_line[:3]
			list_of_good_lines.append(list_line)
	flank_df = DataFrame(data = list_of_good_lines, columns = ['query','flank_1','flank_2'])
	return flank_df
						

def order_reader(consensus_order_file):
	file=open(consensus_order_file, 'r')
	dat = file.read()
	dat.rstrip()
	marker_list = dat.split('\t')
	return marker_list
	


def zrc_file_reader(zrc_file):
	"""read in data, separating the problem_markers from the ZRC marker clusters"""
	problem_markers = []
	ZRC_dict = {}
	with open(zrc_file) as file:
		junk = 'The following marker appears to incorrectly join two or more ZRC or singletons at the N threshold specified:'
		for line in file:
			if line[:len(junk)] == junk:
				marker = line[len(junk):].strip()
				if marker not in problem_markers:
					problem_markers.append(marker)
			elif line[:3] == 'ZRC':
				suffix = line[6:].strip()
				name = 'ZRC_' + suffix
				markers = []
				while True:
					x = file.__next__().strip()
					if x == '':
						break
					else:
						markers.append(x)
				ZRC_dict[name] = markers
			else:
				continue			
	return (problem_markers, ZRC_dict)
	
def onemap_fam_file_reader(fam_file):
	"""read in the onemap family file"""
	markers_dat = pd.read_table(fam_file, sep=' ', names = ['name','dat'], skiprows=1)
	markers_dat['name'] = markers_dat['name'].map(lambda x: str(x)[1:])
	return markers_dat









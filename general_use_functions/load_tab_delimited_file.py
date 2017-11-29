def load_lines(cluster_file):
	""" load a tab delimited file into memory as a list of lines"""
	list_of_lines = []
	with open(cluster_file) as file:
		for line in file:
			strip_line = line.rstrip()
			split_line = strip_line.split('\t')
			list_of_lines.append(split_line)
	return list_of_lines
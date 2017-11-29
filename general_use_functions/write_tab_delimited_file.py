def write_lines(output_list, filename):
	""" write a list of lines to a tab delimited file"""
	for line in output_list:
		outstring = '\t'.join(map(str, line)) 
		output = open(filename, 'a')
		output.write(outstring)
		output.write('\n')
		output.close()

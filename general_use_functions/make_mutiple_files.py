

def make_files(list_of_names, extension='', headerline=''):
	"""make multiple files from a list of names"""
	"""optional header line and file extension passed in"""
	for name in list_of_names:
		filename = name + extension
		file = open(filename, 'a')
		file.write(headerline)
		file.close()
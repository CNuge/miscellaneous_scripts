

"""check if the major and minor alleles match the query's 
	base at the given position, if not then make the necessary
	adjuestment to the alleles column"""
def write_to_file(outline,outfile):
	file=open(outfile, 'a')
	file.write(outline)
	file.close()


outfile = 'output_snp_file.txt'


with open('input_snp_file.txt') as file:
	for line in file:
		data = line.rstrip().split('\t')
		alleles = data[2].split('/')
		if (data[3][int(data[1])- 1]) == (alleles[0]):
			alleles_out = '/'.join(alleles)
			outline = '%s\t%s\t%s\t%s\n' % (data[0], data[1], alleles_out , data[3])
			write_to_file(outline,outfile)
		elif data[3][(int(data[1])-1)] == alleles[1]:
			alleles_split = [alleles[1],alleles[0]]
			alleles_out = '/'.join(alleles_split)
			outline = '%s\t%s\t%s\t%s\n' % (data[0], data[1], alleles_out , data[3])
			write_to_file(outline,outfile)

		else:
			""" put the alleles into the alt common and start with the query """
			alleles_split = list(data[3][int(data[1])-1])
			for i in alleles:
				alleles_split.append(i)
			alleles_out = '/'.join(alleles_split)
			outline = '%s\t%s\t%s\t%s\n' % (data[0], data[1], alleles_out , data[3])
			write_to_file(outline,outfile)

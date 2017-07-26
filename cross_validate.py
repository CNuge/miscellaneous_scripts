

def read_pos_dat(vcf_file):
	""" take the vcf file and read in lines, adding info to a list """
	list_of_dat =[]
	with open(vcf_file) as file:
		for line in file:
			line_dat = line.rstrip().split('\t')
			designation = '%s_%s' % (line_dat[0], line_dat[1])
			list_of_dat.append(designation)
	return list_of_dat

if __name__ == '__main__':

	""" read in the koop positions """

	koop_positions = read_pos_dat('all_unique_koop_positions.tsv')

	""" read in the positions from the other dataset """
	
	query_positions = read_pos_dat('stacks_two_locations.vcf')


	output_file = 'DanzfergTwoLocations_KoopGenome_CV.txt'

	for snp in query_positions:
		if snp in koop_positions:
			file=open(output_file, 'a')
			file.write(snp)
			file.write('\n')
			file.close()




def read_pos_dat(vcf_file):
	""" take the vcf file and read in lines, adding info to a list """
	dict_of_dat ={}
	with open(vcf_file) as file:
		for line in file:
			line_dat = line.rstrip().split('\t')
			designation = '%s_%s' % (line_dat[0], line_dat[1])
			if line_dat[0] in dict_of_dat.keys():
				dict_of_dat[line_dat[0]].append(designation)
			else:
				dict_of_dat[line_dat[0]] = [designation]
	return dict_of_dat

if __name__ == '__main__':

	""" read in the koop positions """

	koop_positions = read_pos_dat('all_unique_koop_positions.tsv')

	
	""" read in the positions from the other dataset """
	
	query_positions = read_pos_dat('stacks_two_locations.vcf')


	output_file = 'Dict_StacksTwoLocations_KoopGenome_CV.txt'

	for contig in query_positions.keys():
		try:
			subject = koop_positions[contig]
		except:
			continue
		for snp in set(query_positions[contig]):
			if snp in subject:
				file=open(output_file, 'a')
				file.write(snp)
				file.write('\n')
				file.close()


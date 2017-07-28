

def read_pos_dat(vcf_file):
	""" take the vcf file and read in lines, adding info to a list 
		stored with contig as key, and values are a list of tuples,
		first part of tuple is the pos, second is the entire line in a string"""
	dict_of_dat ={}
	with open(vcf_file) as file:
		for line in file:
			line_string = line.rstrip()
			line_dat = line_string.split('\t')
			
			if line_dat[0] in dict_of_dat.keys():
				try:
					dict_of_dat[line_dat[0]].append((line_dat[1], line_string))
				except:
					print(line)
					continue
			else:
				try:
					dict_of_dat[line_dat[0]] = [(line_dat[1], line_string)]
				except:
					print(line)
					continue
	return dict_of_dat


if __name__ == '__main__':


	""" read in the koop positions and alleles"""

	koop_positions = read_pos_dat('trimmed_koop_alleles.tsv')

	
	""" read in the vcf from the other dataset """
	
	query_positions = read_pos_dat('all_snps_aligning_to_genome.vcf')

	""" """
	output_file = 'stacks_allele_compare.tsv'

	for contig in query_positions.keys():
		try:
			subject = set(koop_positions[contig])
		except:
			continue
		""" build a dict from the subject data, then compare to it """
		subject_positions_dict =  {key: value for (key, value) in subject}

		for query_snp in query_positions[contig]:
			try:
				compare_alleles = subject_positions_dict[query_snp[0]]
				output = query_snp[1] + '\t' + compare_alleles
				file=open(output_file, 'a')
				file.write(output)
				file.write('\n')
				file.close()
			except:
				pass

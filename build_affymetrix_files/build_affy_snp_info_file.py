import pandas as pd
from pandas import Series, DataFrame


def allele_sort(allele_list):
	""" sort a list of two alleles, and return the string in fmt: [A/T]"""
	if len(allele_list) > 2:
		print('no triallele snps allowed')
		return -1
	allele_string = '[%s/%s]' % (sorted(allele_list)[0], sorted(allele_list)[1])
	return allele_string

def get_71mer(contig, pos, alleles):
	""" take the contig sequence, stored as a variable and get the
		35 bases either side of the snp, insert the alleles in the middle of 
		the sequence, in alphabetical order """
	try:
		contig[pos-36] #check if snp is to close to the end of the contigs
		contig[pos+35]
	except:
		return '-' #if it is, return a blank 71mer so we know to exclude
	""" below slicing relies on the zero indexing of the contig string """
	front_of_71mer = contig[pos-36:pos-1]
	middle_of_71mer = allele_sort(alleles)
	back_of_71mer = contig[pos:pos+35]
	""" merge the 71mer to a single string """
	out_dat = ''.join([front_of_71mer,middle_of_71mer,back_of_71mer])
	return out_dat

def load_contigs(contig_fasta_file):
	"""load the contigs into memory, in order ot get surrounding bp """
	contig_dict = {}
	with open(contig_fasta_file) as file:
		for line in file:
			name = line[1:].rstrip()
			contig_dict[name] = file.next()
	return contig_dict

def read_vcf(filename):
	""" skip the header info lines and make a .vcf dataframe """
	in_data = []
	with open(filename) as file:
		for line in file:
			if line[:2] == "##":
				continue
			elif line[0] = "#"
				header = line[1:].rstrip().split('\t')
			else:
				line_dat = line.rstrip().split('\t')
				in_data.append(line_dat)
	vcf_df = DataFrame(data = in_data, columns = header)
	return vcf_df


if __name__ == '__main__':

""" read in the genome fasta  """
contig_dict = load_contigs('salp_contig_file.fasta')

""" read the .vcf in as a dataframe, then project get_71mer through a lambda """
""" remove all the top lines with # except for the header, just easier this way """
snp_data = read_vcf('fraser_strain_snps_one_location.vcf')

""" apply the 71mer build to the dataframe to make a new column 
	note it calls the contig in the dictonary to get the sequence """
snp_data['seventyone_mer'] = snp_data.apply(
		lambda x: get_71mer(contig_dict[x['#CHROM']], x['Pos'], [x['REF'],x['ALT']]))

""" add an argparse for the 1. snp_priority level 2. strain of origin
	add this information to the dataframe """

"""next reorder and rename the columns to the affymetrix specs, then output the data"""














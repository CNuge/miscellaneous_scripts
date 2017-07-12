import argparse 
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
		contig[pos-36] #check if snp is too close to the end of the contigs
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
	"""load the contigs into memory, in order to get surrounding bp """
	contig_dict = {}
	with open(contig_fasta_file, 'r+') as file:
		for line in file:
			name = line[1:].rstrip()
			contig_dict[name] = next(file)
	return contig_dict

def read_vcf(filename):
	""" skip the header info lines and make a .vcf dataframe """
	in_data = []
	with open(filename) as file:
		for line in file:
			if line[:2] == "##":
				continue
			elif line[0] == "#":
				header = line[1:].rstrip().split('\t')
			else:
				line_dat = line.rstrip().split('\t')
				in_data.append(line_dat)
	vcf_df = DataFrame(data = in_data, columns = header)
	return vcf_df

def name_split(name):
	""" return only first segment of a name with underscores in it """
	new = name.split('_')[0]
	return new

if __name__ == '__main__':


parser = argparse.ArgumentParser()
parser.add_argument("input_vcf", help="input the .vcf file")
parser.add_argument("-c", "--contigs", type=str, help="input the genome in .fasta fmt")
parser.add_argument("-p", "--priority_level", type=str, help="state the priority level of this snp batch")
parser.add_argument("-s", "--strain", type=str, help="state the strain of origin of this snp batch")
parser.add_argument("-o", "--organism", type=str, help="state the name of the species")
args = parser.parse_args()



""" read in the genome fasta  """
contig_dict = load_contigs(args.contigs) 
#'/Users/Cam/Documents/University/microarray_development/Arctic_charr_snp_information/genome_and_raw_vcfs/salp.genome.assembly_03.scaffolds.fa'

""" read the .vcf in as a dataframe, then project get_71mer through a lambda """
snp_data = read_vcf(args.input_vcf) 
#'fraser_strain_snps_one_location.vcf'

""" change the name of the snps, store in affy column name"""
snp_data['snpid'] = snp_data.apply(
		lambda x: name_split(x['ID']), axis=1)

""" add this information to the dataframe:
	1. snp_priority level 
	2. strain of origin 
	3. organism name
	4. make Pos an integer for use in 71mer """

snp_data['SNP_PRIORITY'] = args.priority_level

snp_data['REF_STR'] = args.strain

snp_data['Organism'] = args.organism

snp_data['Pos'] = snp_data['POS'].astype(int)

""" apply the 71mer build to the dataframe to make a new column 
	note it calls the contig in the dictonary to get the sequence """
snp_data['seventyonemer'] = snp_data.apply(
		lambda x: get_71mer(contig_dict[x['CHROM']], x['Pos'], [x['REF'],x['ALT']]), axis=1)


"""next reorder and rename the columns to the affymetrix specs, then output the data"""

snp_data['CHR'] = snp_data['CHROM']

snp_data['SNP_VAL'] = '0'
snp_data['CHR_TYPE'] = 'autosomal'


""" list the columns needed in the affymetrix output file """
final_cols = ['Organism','snpid','REF_STR','seventyonemer','CHR','Pos','SNP_PRIORITY','SNP_VAL','CHR_TYPE']

""" make a subset df, output to a tab delimited file """
output_data = snp_data[final_cols]

output_name =  args.vcf.split('.')[0] + ".tsv"

output_data.to_csv(output_name, sep='\t', index=False)







import pandas as pd
from pandas import Series, DataFrame
from random import randint

def get_37mer(contig, pos):
	""" take the contig sequence in string form and gets the
		30 bases left, the [base] and the size trailing bases """

	front_of_37mer = contig[pos-31:pos-1]
	middle_of_37mer = "[%s]" % (contig[pos-1])
	back_of_37mer = contig[pos:pos+6]
	""" merge the 37mer to a single string """
	out_dat = ''.join([front_of_37mer,middle_of_37mer,back_of_37mer])
	return out_dat

def load_contigs(contig_fasta_file):
	"""load the contigs into memory, in order to get surrounding bp """
	contig_dict = {}
	with open(contig_fasta_file, 'r+') as file:
		for line in file:
			name = line[1:].rstrip()
			contig_dict[name] = next(file)
	return contig_dict

def read_gap_file(gap_file):
    """ take the vcf file and read in lines, adding info to a list """
    return pd.read_table(gap_file, sep='\t')



if __name__ == '__main__':


	""" read in the genome fasta  """
	contig_dict = load_contigs('../genome_and_raw_vcfs/salp.genome.assembly_03.scaffolds.fa') 


	""" read in the locations of the gaps """
	gap_data = read_gap_file('locations_of_gaps_in_coverage.tsv')

	
	# this is gap_data format, gaps of 500+ bp with no snp
	"""
	Contig	Size	Size_rank	leading_position	trailing_position
	Contig985	8893364	1	14175	280284
	Contig985	8893364	1	297378	412775
	"""   

	""" make the output file and write the header"""
	output_file = 'non-polymorphic_probes.tsv'

	file = open(output_file, 'a')
	file.write('probeID\tprobeseq\tchr\tpos\n')
	file.close()
	
	# output format:
	"""
	probeID		probeseq	chr		pos
	Contig8_12	ATC[A]TC	Contig8	pos_of_31st
	"""

	""" iterate through the gap data file, picking a random in in each gap """

	for row in gap_data.iterrows():
		""" limit probe to away from the edges """
		front_wall = row[1]['leading_position']+40
		back_wall = row[1]['trailing_position']-40
		""" pick a random position """
		pos = randint(front_wall, back_wall)
		contig = row[1]['Contig']	
		""" build the 37mer string """
		seq = get_37mer(contig_dict[contig], pos)
		probe_id = contig + str(pos)
		
		""" build the output line """
		row = '%s\t%s\t%s\t%s\n' % (probe_id, seq, contig, pos)
		
		""" write to file """
		file = open(output_file, 'a')
		file.write(row)
		file.close()


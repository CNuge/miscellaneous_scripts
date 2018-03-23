
input_file = 'ALL_SNPs_allele_info_one_file.txt'


output = ''
with open(input_file) as file:
	for line in file:
		data = line.split()
		output_string = f'>{data[0]}_{data[1]}_{data[2]}\n{data[3]}\n'
		output += output_string


outfile = 'all_snps.fasta'

file = open(outfile, 'w')
file.write(output)
file.close()
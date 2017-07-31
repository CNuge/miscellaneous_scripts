def allele_sort(allele_list):
	""" sort a list of two alleles, and return the string in fmt: [A/T]"""
	if len(allele_list) > 2:
		print('no triallele snps allowed')
		return -1
	allele_string = '%s/%s' % (sorted(allele_list)[0], sorted(allele_list)[1])
	return allele_string



with open('allele_in.txt') as file:
	for line in file:
		dat = line.rstrip().split('\t')
		print(allele_sort(dat))
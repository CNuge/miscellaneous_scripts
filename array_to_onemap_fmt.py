import argparse

import numpy as np

import pandas as pd

from pandas import Series, DataFrame


print('loading arguments')


parser = argparse.ArgumentParser(
	description="Input your stacks.genotypes.tsv file here, the program will convert it to a OneMap genotypes file",
	epilog=" ")
parser.add_argument('-i','--input', action='store', required=True, help = 'Put the input .genotypes.tsv file here')

args = parser.parse_args()


###
AFS_125_gts = pd.read_table('AFS_125_high_quality_good_cross.txt', sep='\t')
#for working bit only
geno_dat = AFS_125_gts
###

geno_dat = pd.read_table(args.input, sep='\t')

output = 'OneMap' + args.input

progeny = geno_dat.columns.tolist()
name_list = progeny[0]
num_snps = len(geno_dat[name_list])

no_progeny = len(progeny[2:])

outstring = '%d\t%d\n' % (no_progeny, num_snps)
for row in geno_dat.iterrows():
	name = row[1][0]
	cross = row[1][1]
	gts_list = list(row[1][2:])
	gts_string = ','.join(gts_list)
	dat_string = '*%s %s\t%s\n' % (name , cross, gts_string)
	outstring += dat_string


file = open(output,'w')
file.write(outstring)
file.close()






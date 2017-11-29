
keep_SNPs = []
with open ('SNPs_to_keep.txt') as SNP_dat:
	for line in SNP_dat:
		name = line.rstrip()
		keep_SNPs.append(name)




Blast_hits = []
with open('merged_filtered_data.out') as file:
	for line in file:
		line_d = line.rstrip()
		dat = line_d.split()
		if line[0] == '#':
			continue
		elif dat[0] in keep_SNPs:
			Blast_hits.append(dat)
		else:
			continue
			


# this convert the lists to \n strings, where each individual hit is tab delimited

Top_hit_outstring = ''

for x in Blast_hits:
	for imbed in x:
		y = '\t'.join(imbed)
		z = y + '\n'
		Top_hit_outstring += z
	

# this print to two files, ties and noties 


file=open(Tophit_output,'w')
file.write(Top_hit_outstring)
file.close()


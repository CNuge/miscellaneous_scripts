#!/usr/bin/env python3


"""
Change the input file name in line 20!, keep it wrapped in ' '

This file takes an input in the following format:
TP9010	53	TGCATATCATATGTTCTGGGCCCGAGAAGCAGGCAGTGTAATTTGGGCATGCAAAAAAAAAAAA
TP9085	54	TGCATATCCAATAAGACAGAGCAATATTTGGACAGGTGTTCCTTTTTATATGCAAAAAAAAAAA
TP9161	55	TGCATATCCTAGATAATGACTCTGTTGTCTACCAGACCGTTAGTTCTAACATGCAAAAAAAAAA
TP9184	53	TGCATATCCTAGCTTCTGGGCCTGAGTAGCAGGCAGTTTACTTTGGGCATGCAAAAAAAAAAAA
TP9193	56	TGCATATCCTATAACCACAAACAGGAAGCTGTTCTTCACTCATTTAACTCCATGCAAAAAAAAA
TP9354	46	TGCATATCTAATCAATATACTATCTCTAGTTCTGAGTATAGATGCAAAAAAAAAAAAAAAAAAA

It will take the number in the second column and trim the bp sequence down to that size,
thereby removing the poly-A tail

Output will be in the same format, but the sequences will have the poly A removed
"""
with open('query_input_trim.txt') as f:
    Input_List = [line.rstrip() for line in f]

SNP_list = []

for SNP in Input_List:
	new = SNP.split()
	SNP_list.append(new)

trimmed_seq = []
	
for SNP in SNP_list:
	bp = int(SNP[1])
	name = SNP[0]
	seq = SNP[2]
	nu_seq = seq[0:bp]
	out = [name, str(bp) , nu_seq]
	trimmed_seq.append(out)
	
Output_list = []
for SNP in trimmed_seq:
	data_string = '\t'.join(SNP)
	Output_list.append(data_string)
	

Outstring = '\n'.join([str(x) for x in Output_list])
		
Header ='Marker\tbp_length\tsequence\n'


#Print the output with a header
file = open('Trimmed_query_output.txt','w')
file.write(Header)
file.write(Outstring)
file.close()




		

		

#This script will take a OneMap genotype file and identify
#markers in zero recombination clusters
with open('OneMapexampleGeno.txt') as f:
    GenoList = [line.rstrip() for line in f]

# Extract info from header line, get # of SNPs and # of Genotypes
header = GenoList[0].split(' ')
data = GenoList[1:]
individuals = header[0]
Number_of_SNPs = header[1] 

#use the csv delimiters to split the big genotype string into a list
#for each SNP

geno_sep = []
for SNP in data:
	new = SNP.split(',')
	geno_sep.append(new)

#Alter positon one of the string to remove all but the marker name
#other information is unnecessary for this current task, so just dropped
#if needed it can be grabbed from the global variable geno_sep later on.

snp_dict = {}
for SNP in geno_sep:
	info = SNP[0][:-1]
	info = info[1:]
	info_sep = info.split(' ')
	marker = info_sep[0]
	SNP[0] = SNP[0][-1:]
	
	snp_dict = {marker : SNP}


matching_dict = {}

for key1, value1 in snp_dict.items():
    
    match_found = False
    temp_genotypes = value1
    
    for key2, value2 in snp_dict.items():
        
        print("Comparing %s against %s." % (temp_genotypes, value2))
        
        if value2 == temp_genotypes:
            if str(key1) != str(key2):
                match_found = True
                matching_dict[key1] = key2
                print("Match found between %s and %s.\n" % (key1, key2))
            else:
                pass
            
        else:
            match_found = False
            print("No match found.\n")

print(matching_dict)



# Send data to two output files, one with only the 'figurehead' SNPs
# other with a dictionary with the 'figurehead' as key and all the other 
# SNPs listed as a value, possibly build into a string similar to the 
# original fam file

keep_lines = []

with open('non-polymorphic_probes.tsv', 'r+') as file:
		for line in file:
			probe_string =  line.rstrip().split('\t')[1]
			if 'N' in probe_string:
				continue
			else:
				keep_lines.append(line)


for line in keep_lines:
	file = open('trimmed_non-polymorphic_probes.tsv','a')
	file.write(line)
	file.close()
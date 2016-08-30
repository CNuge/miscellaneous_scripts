
#figure out how to get these programs to run with just the name, i.e. Hit_retainer.py instead of python3 Hit_re.....
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
parser.add_argument("-f", "--filter_parameter_1", type=int, help="Input the column number you wish to filter your Blast outputs by\nquick reference: 3 % identity , 4 alignmnet length , 5 mismatches, 6 gap opens, 11 e value, 12 bit score ")
parser.add_argument("-c", "--cutoff_1", type=str, help="The cutoff value you wish to use, all retained hits will be greater than or equal to this value (or less than in the case of e value")
parser.add_argument("-f2", "--filter_parameter_2", type=int, default= 0)
parser.add_argument("-c2", "--cutoff_2", type=str, help="The cutoff value you wish to use, all retained hits will be greater than or equal to this value (or less than in the case of e value", default= 0)

args = parser.parse_args()

Retained_hits_output = 'Retained_hits_' + args.input

filter_parameter = args.filter_parameter_1
if filter_parameter == 11:
	G_OR_L = '<' 
else:
	G_OR_L = '>'

def hit_retain(hit, parameter, cutoff, greater_or_less):
	column = int(parameter) - 1
	try:
		value = float(hit[column])
	except:
		print('The following line was kicked out because it has letters in the columns where numbers are required. Math impossible!')
		print(line)
	float_cutoff = float(cutoff)
	if greater_or_less == '>':	
		if value >= float_cutoff:
			return['keep']
		else:
			return['omit']
	elif greater_or_less == '<':
		if value <= float_cutoff:
			return['keep']
		else:
			return['omit']

Blast_hits = []
with open(args.input) as file:
	for line in file:
		line_d = line.rstrip()
		dat = line_d.split()
		if line[0] == '#':
			continue
		else:
			ruling = hit_retain(dat, args.filter_parameter_1, args.cutoff_1, G_OR_L)
			if ruling == ['keep']:
				Blast_hits.append(dat)
			else:
				pass
#below repeat the filtering if a second paramater is given at input
Blast_filtered_twice = []
if args.filter_parameter_2 == 0:
	pass
else:
	if args.filter_parameter_2 == 11:
		G_OR_L_2 = '<' 
	else:
		G_OR_L_2 = '>'
	for line in Blast_hits:
		ruling = hit_retain(line, args.filter_parameter_2, args.cutoff_2, G_OR_L_2)
		if ruling == ['keep']:
			Blast_filtered_twice.append(line)
		else:
			pass


if args.filter_parameter_2 == 0:
	Retained_hits = Blast_hits
else:
	Retained_hits = Blast_filtered_twice


Retained_hits_outstring = ''
for x in Retained_hits:
	y = '\t'.join(x)
	z = y + '\n'
	Retained_hits_outstring += z
	

header = 'query id\tsubject id\t% identity\talignment length\tmismatches\tgap opens\tq. start\tq. end\ts. start\ts. end\tevalue\tbit score\n'

file=open(Retained_hits_output,'w')
file.write(header)
file.write(Retained_hits_outstring)
file.close()

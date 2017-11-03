#!/usr/bin/env python
import argparse 

""" this program takes a tsv list of fish sample IDs and their current concentrations and
	returns the amount of volume needed to dilute the samples to a set concentration 
	currently two concentrations given and two dilutions calculated, modify accordingly
	for single calculation"""



def calc_v1_set_h2o(c1,c2,v2_water):
	""" calculate the amount of sample to add to a set water volume
		to arrive at desired volume """
	v1 = v2_water / ((c1/c2)-1)
	return v1


def calc_v1(c1,c2,v2):
	""" calculate the amount of initial sample needed 
		to dilute to a given concentration"""
	v1 = (c2*v2)/c1
	return (format(c1, '.2f'), format(v1, '.2f'), format(c2, '.2f'), format(v2, '.2f'))


def calc_v2(c1,v1,c2):
	""" calculate the final volume of a dilution"""
	v2 = (c1*v1)/c2
	return (format(c1, '.2f'), format(v1, '.2f'), format(c2, '.2f'), format(v2, '.2f'))


def load_lines(cluster_file):
	""" load a tab delimited file into memory as a list of lines"""
	list_of_lines = []
	with open(cluster_file) as file:
		for line in file:
			strip_line = line.rstrip()
			split_line = strip_line.split('\t')
			list_of_lines.append(split_line)
	return list_of_lines

def write_lines(output_list, filename):
	""" write a list of lines to a tab delimited file"""
	for line in output_list:
		outstring = '\t'.join(map(str, line)) 
		output = open(filename, 'a')
		output.write(outstring)
		output.write('\n')
		output.close()


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="input the tsv with ids and concentrations")
	args = parser.parse_args()


	#values we are trying to get to
	final_conc = 10. #ng/ul
	set_water_volume = 100

	input_data = load_lines(args.input)

	output_list = []

	for line in input_data:
		""" get fish information """
		
		sample_id = line[0]
		
		if line[1] == '-':
			outlist_stock = ['stock', 
				sample_id, 
				'-', 
				'-', 
				'-', 
				'-', 
				'-']
			output_list.append(outlist_stock)
			continue

		c1_stock = float(line[1])

		v1 = calc_v1_set_h2o(c1_stock, final_conc, set_water_volume)
		v2 = set_water_volume + v1
		
		outlist_stock = ['stock', 
						sample_id, 
						format(c1_stock, '.2f'), 
						format(v1, '.2f'),  
						format(final_conc, '.2f'), 
						format(v2, '.2f'), 
						set_water_volume]

		output_list.append(outlist_stock)


	


	""" write the output to file """
	output_file = 'calculated_' + args.input

	output_dat = open(output_file, 'a')
	output_dat.write('source\tFish_ID\tstock_conc\tstock_vol_req\tc2\tv2\twater_needed\n')
	output_dat.close()

	write_lines(output_list,output_file)






import argparse 

""" this program takes a tsv list of fish sample IDs and their current concentrations and
	returns the amount of volume needed to dilute the samples to a set concentration 

	currently two concentrations given and two dilutions calculated, modify accordingly
	for single calculation"""


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
	std_sample_vol = 65. #ul

	"""set the files """
	input_data = load_lines(args.input)


	output_list = []

	for line in input_data:
		""" get fish information """
		sample_id = line[0]
		output = [sample_id]
		c1 = float(line[2])
		c1_stock = float(line[1])

		if (c1 >= 10) and (c1 <= 75):
			""" do standard dilution procedure if value in needed range """
			dilution_nums = calc_v2(c1, std_sample_vol , final_conc)
			""" calculate the water to add to the sample to make v2 """ 
			final_water = float(dilution_nums[3]) - std_sample_vol
			final_water = format(final_water, '.2f')
			outlist_plate = ['plate', sample_id, '-','-','-','-', format(c1, '.2f'), 65, final_conc, dilution_nums[3], final_water]		
			output_list.append(outlist_plate)
		
		elif c1 < 10 :
			""" if below the value needed, go off the original stock solution for dilution """
			final_vol = 75
			dilution_nums = calc_v1(c1_stock, final_conc, final_vol)

			final_water = float(dilution_nums[3]) - float(dilution_nums[1])
			final_water = format(final_water, '.2f')

			outlist_stock = ['stock', sample_id, format(c1_stock, '.2f'), dilution_nums[1],final_conc, dilution_nums[3],'-','-','-','-', final_water]
			output_list.append(outlist_stock)

		elif c1 > 75:
			""" make custom dilution off of the plate to keep volume below the plate maximum """
			final_vol = 75
			dilution_nums = calc_v1(c1, final_conc, final_vol)

			final_water = final_vol - float(dilution_nums[1])
			final_water = format(final_water, '.2f')

			outlist_plate = ['custom_plate', sample_id, '-','-','-','-', format(c1, '.2f'), dilution_nums[1], final_conc, final_vol, final_water]
			output_list.append(outlist_plate)

		


	""" write the output to file """
	output_file = 'calculated_' + args.input

	output_dat = open(output_file, 'a')
	output_dat.write('source\tFish_ID\tstock_conc\tstock_vol_req\tc2\tv2\tplate_conc\tplate_vol_req\tc2\tv2\twater_needed\n')
	output_dat.close()

	write_lines(output_list,output_file)






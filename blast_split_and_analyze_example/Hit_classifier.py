#########################################################################################
#########################################################################################
#########################################################################################
#note:
#Split this beast into subfiles when you're done!
# use import on the functions to bring their
# jobs over to the main program
#see if yo can make the dataframe appending bits into a general function
#^would let you cut out a few dozen lines
#########################################################################################
#########################################################################################
#########################################################################################


#see your written work for the architecture of this program
import argparse 
import numpy as np
import pandas as pd
from pandas import Series, DataFrame



parser = argparse.ArgumentParser()
parser.add_argument("input", help="input the Blast outfmt 7 file")
args = parser.parse_args()

#recall blast_outfmt_7
Blast_outfmt7_cols = ['query_id','subject_id','%_identity','alignment_length','mismatches','gap_opens','q_start','q_end','s_start','s_end','e_value','bit_score']

#designate the desired output files here
print('Making output dataframes') 
classification_cols = ['Query_seq','Classification','hits_to_chr','potential_seg_dups']
Query_Classificiation = DataFrame(np.nan,index=[0], columns = classification_cols)

#make an array with the query seq listed on left, have the array give
# Query_seq	Classification	hits_to_chr			potential_seg_dups	
# TP1738	S_1				Ssa02		
# TP1588	S_1a			Ssa04		
# TP1478	S_1PDL			Ssa04				Ssa04
# TP1677	PuDu_2			Ssa05*/Ssa09		Ssa05
# TP1899	PuDu_2			Ssa12/Ssa25
# TP1992	PuUbiq			Ssa17/Ssa29/Ssa04/Ssa12/Ssa19/Ssa20/Ssa21/Ssa22
# TP2211	PuDu_3			Ssa06/Ssa03*/Ssa12*	Ssa03/Ssa12
Location_cols = ['Hit','Type','Location','start(range)','end(range)','Number_of_hits']
Location_by_hit = DataFrame(np.nan,index=[0], columns = Location_cols)

#Also output a location for each no PuUbiq hit to a different file
#I.e.
#Hit		Type			Location	start(range)	end(range) hits_in_cluster
# TP1738	S_1				Ssa02		
# TP1588	S_1a			Ssa04		
# TP1478	S_1PDL			Ssa04_a		2332323			2323421		2
# TP1478	S_1PDL			Ssa04_b		5342342			5342411		9
# TP1677	PuDu_2			Ssa05_a
# TP1677	PuDu_2			Ssa05_b
#

#have the outputs of the below functions append lines to the end of the above lists!


#functions are below
#########################################################################################
def blast_extractor(filename):
	with open(filename) as file:
		Blast_hits = []
		for line in file:
			line_d = line.rstrip()
			dat = line_d.split()
			if line[0] == '#':
				continue
			elif line_d[0] == 'query_id' or line_d[0] == 'query' :
				continue
			else:
				Blast_hits.append(dat)
		return Blast_hits
		

def hit_parse(Blast_hits_list):
	Out_Dict = {}
	print('Making dictonary of Blast queries and all of their respective hits')
	for line in Blast_hits_list:
		try: 
			Out_Dict[line[0]]
		except:
			query_list = [line]
			Out_Dict[line[0]] = query_list
		query_list = Out_Dict[line[0]]
		query_list.append(line)
	return Out_Dict

def chromosome_split(query_frame, unique_hit_locations, chr_dict):
	for name in unique_hit_locations:
		hit_list = []
		for line in query_frame.index.tolist():
			if query_frame.ix[line,1] == name:
				hit_list.append(query_frame.ix[line].tolist())
			else:
				continue
		chr_dict[name] = hit_list



#below will parse the date into segmental duplicate, and/or unique values
#returns a classification and a list of lists
#list of list contains:
#Location	start(range)	end(range)
#this can be combined with the Name, chromosome of hit and the classification from hit_classifier to make
#the objects to add to the output arrays
def seg_split(Hit_dataframe):
	seg_dict = {}
	all_group_lists =[]
	for unique_number in Hit_dataframe.index.tolist():
		for compare_number in Hit_dataframe.index.tolist():
			place_x = [int(Hit_dataframe.ix[unique_number, 's_start']), int(Hit_dataframe.ix[unique_number, 's_end'])]
			place_y = [int(Hit_dataframe.ix[compare_number, 's_start']), int(Hit_dataframe.ix[compare_number, 's_end'])]
			place_x.sort()
			place_y.sort()
			place_xs = list(range(place_x[0], place_x[1]))
			if place_y[0] in place_xs or place_y[1] in place_xs:
				try:
					seg_dict[compare_number]
					
				except:
					seg_dict[unique_number] = 'G_' + str(unique_number)
					seg_dict[compare_number] = 'G_' + str(unique_number)
				seg_dict[unique_number] = seg_dict[compare_number]
	for group in set(list(seg_dict.values())):
		group_count = 0 
		start_hit = 0
		end_hit = 0
		for u_hit in list(seg_dict.keys()):
			if seg_dict[u_hit] == group:
				group_count += 1
				if int(Hit_dataframe.ix[u_hit, 8]) < start_hit or start_hit == 0 :
					start_hit = int(Hit_dataframe.ix[u_hit, 8])
				else:
					pass
				if int(Hit_dataframe.ix[u_hit, 9]) > end_hit or end_hit == 0:
					end_hit = int(Hit_dataframe.ix[u_hit, 9])
				else:
					pass
			else:
				continue
		Location = Hit_dataframe.ix[0, 1]
		group_output = [Location , group_count, start_hit, end_hit]
		all_group_lists.append(group_output)
	return all_group_lists
	#list of list that contains:
	#Location	no_of_hits start(range)	end(range)
	# ['chr','no_of_hits','s_end','s_stop'],
	
		
#########################################################################################

#hit Parser here
print('Loading input files')
Blast_filename = args.input
Blast_hits = blast_extractor(Blast_filename)

print('Splitting hits by query')
Out_Dict = hit_parse(Blast_hits)


print('Classifying alignments, be patient may take a while')
tracker_count = 0
total = len(Out_Dict.keys())
for query in Out_Dict.keys():
	tracker_count += 1
	#this if clause gets the single hit locations dealt with
	if len(Out_Dict[query]) == 1:
		single_hit = Out_Dict[query]
		Query_class_list = [[query, 'S_1', single_hit[1], 'NaN']]
		Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
		Query_Classificiation = pd.concat( [Query_Classificiation, Query_temp_frame])
		location_dat = [[query, 'S_1', single_hit[1],single_hit[8],single_hit[9], 'NaN']]
		Location_frame = DataFrame(location_dat, columns = Location_cols)
		Location_by_hit= pd.concat([Location_by_hit, Location_frame])
	
	else:
		query_frame = DataFrame(Out_Dict[query], columns = Blast_outfmt7_cols)
		#below value can be sent to output array!!!
		#column 3! of Query_class_list
		unique_hit_locations = list(query_frame['subject_id'].unique())
		#chr_dict is a dictionsary with the chr as keys and a list of all hits to that chromosome as values
		chr_dict = {}
		chromosome_split(query_frame, unique_hit_locations, chr_dict)
		#below takes the unique_hit_locations, sorts them and turns them into an outputable string if necessary
		if len(unique_hit_locations) > 1:
			unique_hit_locations.sort()
			unique_hit_locations = ' '.join(unique_hit_locations)
		else:
			pass
			
		if len(list(chr_dict.keys())) == 1:
			name = list(chr_dict.keys())
			chr_w_hit = chr_dict[name[0]][0][1]
			hit_frame = DataFrame(chr_dict[name[0]], columns = Blast_outfmt7_cols)
			segment_data = seg_split(hit_frame)
			if len(segment_data) == 1:
				looker = list(chr_dict.keys())[0]
				single_hit = chr_dict[looker]
				Query_class_list = [[query, 'S_1', chr_w_hit, 'NaN']]
				Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
				Query_Classificiation = pd.concat([Query_Classificiation, Query_temp_frame])
				location_dat = [[query, 'S_1a', single_hit[0][1],segment_data[0][2],segment_data[0][3], segment_data[0][1]]]
				Location_frame = DataFrame(location_dat, columns = Location_cols)
				Location_by_hit= pd.concat([Location_by_hit, Location_frame])
			else:
				looker = list(chr_dict.keys())[0]
				single_hit = chr_dict[looker]
				Query_class_list = [[query, 'S_1PDL', chr_w_hit, chr_w_hit]]
				Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
				Query_Classificiation = pd.concat([Query_Classificiation, Query_temp_frame])
				for segment in segment_data:
					location_dat = [[query, 'S_1PDL', chr, segment[2],segment[3],segment[1]]]
					Location_frame = DataFrame(location_dat, columns = Location_cols)
					Location_by_hit= pd.concat([Location_by_hit, Location_frame])
		elif len(list(chr_dict.keys())) == 2:		
			seg_dup_list =[]
			for chr in list(chr_dict.keys()):	
				hit_frame = DataFrame(np.array(chr_dict[chr]), columns = Blast_outfmt7_cols)
				segment_data = seg_split(hit_frame)
				if len(segment_data) == 1:
					location_dat = [[query, 'PuDu_2', chr, segment_data[0][2],segment_data[0][3], segment_data[0][1]]]
					Location_frame = DataFrame(location_dat, columns = Location_cols)
					Location_by_hit= pd.concat([Location_by_hit, Location_frame])
				else:
					seg_dup_list.append(chr)
					for segment in segment_data:
						location_dat = [[query, 'PuDu_2', chr, segment[2],segment[3],segment[1]]]
						Location_frame = DataFrame(location_dat, columns = Location_cols)
						Location_by_hit= pd.concat([Location_by_hit, Location_frame])
			
			type = 'PuDu_2'
			if len(seg_dup_list) > 1:
				seg_dup_list.sort()
				seg_dup_list = ' '.join(seg_dup_list)
			elif len(seg_dup_list) == 0:
				seg_dup_list = 'NaN'
			hit_data_1 = list(chr_dict.values())[0][0]
			Query_class_list =[[query, type ,unique_hit_locations, seg_dup_list]]
			Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
			Query_Classificiation = pd.concat( [Query_Classificiation, Query_temp_frame])
				
		elif len(list(chr_dict.keys())) == 3:		
			seg_dup_list =[]
			for chr in list(chr_dict.keys()):
				hit_frame = DataFrame(np.array(chr_dict[chr]), columns = Blast_outfmt7_cols)
				segment_data = seg_split(hit_frame)
				if len(segment_data) == 1:
					location_dat = [[query, 'PuDu_3', chr, segment_data[0][2],segment_data[0][3], segment_data[0][1]]]
					Location_frame = DataFrame(location_dat, columns = Location_cols)
					Location_by_hit= pd.concat([Location_by_hit, Location_frame])
				else:
					seg_dup_list.append(chr)
					for segment in segment_data:
						location_dat = [[query, 'PuDu_3', chr, segment[2],segment[3],segment[1]]]
						Location_frame = DataFrame(location_dat, columns = Location_cols)
						Location_by_hit= pd.concat([Location_by_hit, Location_frame])
			
			type = 'PuDu_3'
			if len(seg_dup_list) > 1:
				seg_dup_list.sort()
				seg_dup_list = ' '.join(seg_dup_list)
			elif len(seg_dup_list) == 0:
				seg_dup_list = 'NaN'
			hit_data_1 = list(chr_dict.values())[0][0]
			Query_class_list =[[query, type ,unique_hit_locations, seg_dup_list]]
			Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
			Query_Classificiation = pd.concat( [Query_Classificiation, Query_temp_frame])
					
		elif len(list(chr_dict.keys())) == 4:		
			seg_dup_list =[]
			for chr in list(chr_dict.keys()):
				hit_frame = DataFrame(np.array(chr_dict[chr]), columns = Blast_outfmt7_cols)
				segment_data = seg_split(hit_frame)
				if len(segment_data) == 1:
					location_dat = [[query, 'PuDu_4', chr, segment_data[0][2],segment_data[0][3], segment_data[0][1]]]
					Location_frame = DataFrame(location_dat, columns = Location_cols)
					Location_by_hit= pd.concat([Location_by_hit, Location_frame])
				else:
					seg_dup_list.append(chr)
					for segment in segment_data:
						location_dat = [[query, 'PuDu_4', chr, segment[2],segment[3],segment[1]]]
						Location_frame = DataFrame(location_dat, columns = Location_cols)
						Location_by_hit= pd.concat([Location_by_hit, Location_frame])
			type = 'PuDu_4'
			if len(seg_dup_list) > 1:
				seg_dup_list.sort()
				seg_dup_list = ' '.join(seg_dup_list)
			elif len(seg_dup_list) == 0:
				seg_dup_list = 'NaN'
			hit_data_1 = list(chr_dict.values())[0][0]
			Query_class_list =[[hit_data_1[0], type ,unique_hit_locations, seg_dup_list]]
			Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
			Query_Classificiation = pd.concat( [Query_Classificiation, Query_temp_frame])
			
		else:
			type = 'PuUbiq'
			hit_data_1 = list(chr_dict.values())[0][0]
			Query_class_list =[[query, type ,unique_hit_locations, 'Not assessed']]
			Query_temp_frame = DataFrame(Query_class_list,  columns = classification_cols)
			Query_Classificiation = pd.concat( [Query_Classificiation, Query_temp_frame])
		current_pct = ((tracker_count/total)*100)
		update='%dpct done, on record %d of %d.' % (current_pct, tracker_count, total)
		print(update)	


print('Writing output files')

Location_by_hit.to_string()
Query_Classificiation.to_string()

Hit_location_out = 'Hit_Locations_' + args.input
Location_by_hit.to_csv(Hit_location_out, sep='\t', index=False)

Query_Classificiation_out = 'Hit_Classifications_' + args.input
Query_Classificiation.to_csv(Query_Classificiation_out, sep='\t',index=False)

print('Done!')













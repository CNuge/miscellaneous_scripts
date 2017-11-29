This script will let you take a dataframe and turn it into a gridQTL 
map input file.

This is needed because gridQTL maps list markers in a unique format,
with the markers for each linkage group listed horizontally,
and the cM distance between them in between (as opposed to the cM from 0)

This script needs a df with the following headers (other cols allowed),
tab delimited:
marker	cluster	LG	map_distance
m1	0	LG_1	0

map distance is the conventional, distance from 0, and the program does
the math for you, and builds the horizontal, space delimited list.
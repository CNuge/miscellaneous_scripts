#!/bin/sh


#we take the list of files with a unique quality
#in this case and AC beginning and .txt ending
#and we read this in, slice off the _markers.txt finish
#then make a new folder for each file, and move the file to its respective folder
for i in AC*.txt
do
	name=$(echo $i | cut -d '_'  -f 1)
	mkdir $name
	mv $i $name
done
Working with the output files of linkmfex, I have found the need to move them
in to python/pandas dataframes in order to allow for efficient manipulation
and parsing of data.

These can get a little messy, as certain files have messy header lines,
multiple dataframes output to a single file, etc etc.
This repository contains a few functions to quickly read in specific messy
linkmfex output files and move them into pandas dataframes.
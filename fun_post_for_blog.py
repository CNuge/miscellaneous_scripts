""" just because you can doesn't mean you should: 
	a python function written in normal and idiomatic python

	then contrast it with cryptic python, compare the best practices
	to the frankenstein method 


	I will do it on a function that takes two sorted lists and returns a single sorted
	list with no duplicates 
"""

#simplest starting answer

def merge_sorted(list_a, list_b):
	""" take two lists of integers sorted smallest to largest, 
		merge them to a single output list with
		no duplicate values """
	
	output_list = []

	while (len(list_a) > 0) and (len(list_b) >0):
		if list_a[0] == list_b[0]:
			output_list.append(list_a.pop())
			list_b.pop()
		elif list_a[0] < list_b[0]:
			output_list.append(list_a.pop())
		
		elif list_a[0] > list_b[0]:	
			output_list.append(list_b.pop())

	if len(list_a) > 0:
		output_list.extend(list_a)
	elif len(list_b) > 0:
		output_list.extend(list_b)
	
	return output_list


# do weird shit
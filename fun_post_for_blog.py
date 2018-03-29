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

	while (len(list_a) > 0) and (len(list_b) > 0):
		if list_a[0] == list_b[0]:
			output_list.append(list_a.pop(0))
			list_b.pop(0)
		
		elif list_a[0] < list_b[0]:
			output_list.append(list_a.pop(0))
		
		elif list_a[0] > list_b[0]:	
			output_list.append(list_b.pop(0))

	if len(list_a) > 0:
		output_list.extend(list_a)
	elif len(list_b) > 0:
		output_list.extend(list_b)
	
	return output_list


#weird stuff to stay in the constraints
globals().__setitem__('x', 10)
#instead of 
x = 10

len(list_a) is not 0
#instead of 
len(list_a) > 0

list_a[0] is list_b[0]
#instead of 
list_a[0] == list_b[0]
# that isn't that much worse, but generally is should not be used as a direct
# equivalent to == it works here but that is by no means true in all context.
# just remember:
a = [1,2,3]
b = [1,2,3]
a == b
a is b

abs(list_b[0] - list_a[0]) is (list_b[0] - list_a[0])
#instead of 
list_a[0] < list_b[0]
#this one is messier than the is substitute for ==
# we don't just need to know if they differ, but we also need to know which
# of the two is the smaller number (so that we can append that to the output)

# I use the abs() to make this work. The logic isn't the most linear thing,
# but here is why this works.
# take the first member of list_a, subtract the first member of list_b
# this will give us a positive (list_a's number is bigger) or 
# negative (list_b's number is bigger). The case where they are equal is already
# dealt with by the preceeding if statement.

# abs() will turn a negative integer to a positive one (absloute value)
# while a positive number will remain a positive integer

# so if abs() changes the sign of the int,
abs(list_a[0] - list_b[0]) is (list_a[0] - list_b[0])
# will evaluate to false, and we know that the list_a value is smaller than the list_b value

#building this in to the function we can use both an is and is not
#elif function to control the logic and evaluate to true in opposite instances

#when this is true the list_a value is smaller
abs(list_a[0] - list_b[0]) is not (list_a[0] - list_b[0])

#when this is tru the list_b value is smaller
abs(list_a[0] - list_b[0]) is (list_a[0] - list_b[0])

#clear as mud right? do you miss the > and < signs yet?




def constrained_merge_sorted(list_a, list_b):
	globals().__setitem__('out_list' ,  list_a * 0)

	while (len(list_a) is not 0) and (len(list_b) is not 0):
		if list_a[0] is list_b[0]:
			globals().__setitem__('out_list', out_list + [list_a.pop(0)])
			list_b.pop(0)

		elif abs(list_a[0] - list_b[0]) is not (list_a[0] - list_b[0]):
			globals().__setitem__('out_list', out_list + [list_a.pop(0)])

		elif abs(list_a[0] - list_b[0]) is (list_a[0] - list_b[0]):
			globals().__setitem__('out_list', out_list + [list_b.pop(0)])

	if len(list_a) is not 0:
		return output_list + list_a
	elif len(list_a) is not 0:
		return out_list + list_b
	else:
		return output_list

		

def constrained_merge_sorted(list_a, list_b):
	# multiplying another list by zero is a valid way to get an empty a list
	# this wasn't a constraint, but I do it because its silly
	globals().__setitem__('out_list' ,  list_a * 0)

	#while statement here
	while (len(list_a) is not 0) and (len(list_b) is not 0):

		#equivalent to: list_a[0] == list_b[0]
		if list_a[0] is list_b[0]:
			# output_list.append(list_a.pop(0))
			globals().__setitem__('out_list', out_list + [list_a.pop(0)])
			#hey this is the same :)
			list_b.pop(0)

		#equivalent to: list_a[0] < list_b[0]
		elif abs(list_a[0] - list_b[0]) is not (list_a[0] - list_b[0]):
 			# output_list.append(list_a.pop(0))
			globals().__setitem__('out_list', out_list + [list_a.pop(0)])

		#equivalent to: list_a[0] > list_b[0]
		elif abs(list_a[0] - list_b[0]) is (list_a[0] - list_b[0]):
			# output_list.append(list_b.pop(0))
			globals().__setitem__('out_list', out_list + [list_b.pop(0)])

	# to avoid more hideous globals().__setitem__() calls, I here return
	# straight out of the if and elif as oppsed to appending to output_list
	if len(list_a) is not 0:
		return output_list + list_a
	elif len(list_a) is not 0:
		return out_list + list_b
	else:
		return output_list

		



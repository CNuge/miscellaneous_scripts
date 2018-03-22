""" just because you can doesn't mean you should 
	a python function written in normal and idiomatic python

	then contrast it with cryptic python, compare the best practices
	to the frankenstein method 


	I will do it on a function that takes two sorted lists and returns a single sorted
	list with no duplicates 



Assume we are implementing a new search app, and our app sends a query to two 
different data sources (e.g. "news" and "images") to get back "Result"s. 
Each result has a relevance score in [0, 1] (with 1=most relevant, 0=least relevant) 
nd a url that uniquely identifies it (as well as other information to display 
to the user). Suppose that both sources return the results to the app in order 
of decreasing relevance. Further suppose that we want to show the user a single 
unified list of results that is also in decreasing relevance order and without 
duplicates. How would you go about implementing such a thing?


Example:

// Input1: News
0.9 yahoo.com
0.8 cnn.com
0.7 google.com

// Input2: Images
0.8 cnn.com
0.6 aol.com

// Output: Result
0.9 yahoo.com
0.8 cnn.com
0.7 google.com
0.6 aol.com

"""


#take in two sorted lists, news and images, return ordered with no duplicates
# need to make sure they aren't seen twice, catch is when there are different relevancy
# scores, need a seen/not seen dict to catch and pop these.


def return_sorted_list( news, images):
	output_list = []
	while (len(news) > 0) and (len(images) > 0):	
	if news[0][1] == images[0][1]:
		if news[0][0] >= images[0][0]:
		output_list.append(news.pop(0))
			images.pop(0)
		else:
			output_list.append(images.pop(0))
			news.pop(0)
	elif news[0][0] > images[0][0]:
			output_list.append(news.pop(0))
		elif news[0][0] < images[0][0]:
	output_list.append(images.pop(0))
		
		if len(news) > 0:
			output_list.extend(news)
				
		elif len(images) > 0:


	for value in output_list:
		if obsevered_urls[value[1]] == 0 :
			output_cleaned.append(value)
	obsevered_urls[value[1]] = 1
		else:
			continue

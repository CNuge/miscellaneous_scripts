
class example_class:
	def __init__(self, *, kw1 = None, kw2 = None):
		if kw1 is not None or kw2 is not None:
			#do stuff with the args
			self.kw1 = kw1
			self.kw2 = kw2

	def read(self, *, kw1 = None, kw2 = None):	
		if kw1 is not None or kw2 is not None:
			#do stuff with the args
			self.kw1 = kw1
			self.kw2 = kw2
			

x = example_class('test')
# will throw the error 
# TypeError: __init__() takes 1 positional argument but 2 were given

#decorator factory
def validate_kwargs(func):
	""" This decorator passes a more descriptive error message when the user
		fails to pass the data in using a keyword arguments """	
	# created decorator
	def validated(*args, **kwargs):
		#we try to replace the decorated function with the function itself
		#it we recieve a TypeError, we know keywords werent passed and we can throw
		#the informative error message
		try:
			result = func(*args, **kwargs)
			return result
		except TypeError:
			raise TypeError("You must specify inputs using the following syntax to explicitly identify arguments:\n"+ \
				"example_class(kw1 = 'keyword1_type_data', kw2 = 'keyword2_type_data')")
	return validated

class example_class:
	@validate_kwargs 
	def __init__(self, *, kw1 = None, kw2 = None):
		if kw1 is not None or kw2 is not None:
			#do stuff with the args
			self.kw1 = kw1
			self.kw2 = kw2

	@validate_kwargs #now decorated
	def read(self, *,kw1 = None, kw2 = None):
		if kw1 is not None or kw2 is not None:
			#do stuff with the args
			self.kw1 = kw1
			self.kw2 = kw2

x = example_class('test')
# will now throw the error
# TypeError: You must specify inputs using the following syntax to explicitly identify arguments: 
#            example_class(kw1 = 'keyword1_type_data', kw2 = 'keyword2_type_data')


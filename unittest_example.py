import unittest

""" important note:
	the tests will only be run if the name of the function in the 
	unittest.TestCase subclass begins with the work test

	all tests must be labelled as such in their names 
	docs:
	https://docs.python.org/3/library/unittest.html

	run:
	python unittest_example.py -v
	to get a verbose output
	"""	

def fun(x):
	return x + 1

class MyTest(unittest.TestCase):
	
	def test_adder(self):
		self.assertEqual(fun(3), 4)

	def test_square(self):
		self.assertEqual(2**2, 4)
		self.assertEqual(4**2, 16)
	

class TestStringMethods(unittest.TestCase):

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')

	def test_isupper(self):
		self.assertTrue('FOO'.isupper())
		self.assertFalse('Foo'.isupper())

	def test_split(self):
		s = 'hello world'
		self.assertEqual(s.split(), ['hello', 'world'])
		# check that s.split fails when the separator is not a string
		with self.assertRaises(TypeError):
			s.split(2)

if __name__ == '__main__':
	q
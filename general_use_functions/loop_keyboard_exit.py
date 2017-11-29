


""" use this motif to run a loop continiously until
	the user interrupts the process. """


import sys
print('type stop to close the program\n')

try:
	    
	x = 1
	while x != -1:	
		print(x)
		x += 1

except KeyboardInterrupt:

	print('ending early\n')
	print('last x was %d' % (x))
	sys.exit()
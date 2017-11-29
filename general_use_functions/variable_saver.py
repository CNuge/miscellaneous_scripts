import shelve

""" use this if you've got a big ipython session going with variables in memoory
	that you want to store so you don't have to take the time to remake them 
	this was from a stack overflow answer I found and am using in my work"""


#store data to a shelf in the current dir
filename='temp_shelve.out'
make_shelf = shelve.open(filename,'n') # 'n' for new


for key in dir():
    try:
        make_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR for obj: %s' % (format(key)))

my_shelf.close()

#RESTORE when you load back up
make_shelf = shelve.open(filename)
for key in make_shelf:
    globals()[key]=make_shelf[key]
make_shelf.close()

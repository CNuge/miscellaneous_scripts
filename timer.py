#!/usr/bin/env python
import time

def clock(func):
    def clocked(*args): #any number of positional arguments
        t0 = time.perf_counter() #performance counter returns a float time in seconds
        result = func(*args)
        t1 = time.perf_counter()
        name = func.__name__
        arg_str =' ,'.join(repr(arg) for arg in args)
        print('function %s ran in: %0.8fs' % (name, t1 - t0))
        return result
    return clocked #return the iner function to replace the decorated func

__author__ = 'rcj1492'
__created__ = '2016.05'
__license__ = 'MIT'

from time import perf_counter as timer

from labpack.randomization import randomlab
from copy import deepcopy

def repeat(function, kwargs, title, count, verbose=True):

    t0 = timer()
    id_list = []
    while len(id_list) < count:
        func = deepcopy(function)
        kw = deepcopy(kwargs)
        id_list.append(func(**kw))
    t1 = timer()
    if verbose:
        print('%s inits of %s in %s secs' % (count, title, (t1 - t0)))
    rand_int = randomlab.random_integer(0, (count - 1))
    rand_item = id_list[rand_int]
    try:
        rand_str = str(rand_item)
        if verbose:
            print('Value of item[%s] of %s performance test is: %s' % (rand_int, title, rand_str))
    except:
        if verbose:
            print('Value returned by %s cannot be coerced into a string.' % title)
    return rand_item

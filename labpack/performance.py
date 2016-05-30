__author__ = 'rcj1492'
__created__ = '2016.05'
__license__ = 'MIT'

from time import perf_counter as timer
from labpack.randomization import labRandom

def labPerform(function, title, count, quiet=False):

    t0 = timer()
    id_list = []
    while len(id_list) < count:
        id_list.append(function)
    t1 = timer()
    if not quiet:
        print('%s inits of %s in %s secs' % (count, title, (t1 - t0)))
    rand_int = labRandom.integer(0, (count - 1))
    rand_item = id_list[rand_int]
    try:
        rand_str = str(rand_item)
        if not quiet:
            print('Value of item[%s] of %s performance test is: %s' % (rand_int, title, rand_str))
    except:
        if not quiet:
            print('Value returned by %s cannot be coerced into a string.' % title)
    return rand_item

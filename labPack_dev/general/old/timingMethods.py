__author__ = 'rcj1492'
__created__ = '2015.07'


import time
print(time.perf_counter())
counter = 0
while counter < 100:
    s = ''
    for i in range(0, 1000):
        s += str(i) + ', '
    # test = symCrypt.encrypt(s, 'hi')
    # test = symCrypt.decrypt(test, 'hi')
    if counter == 0:
        print(time.perf_counter())
    elif counter % 20 == 0:
        print(time.perf_counter())
    counter += 1


from timeit import default_timer as timer
t1 = timer()

t2 = timer()
print(str(t2 - t1) + ' seconds')
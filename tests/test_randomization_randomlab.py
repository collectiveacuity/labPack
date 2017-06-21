__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from labpack.performance import performlab
from labpack.randomization import randomlab

class testlabRandom(object):

    def __init__(self):
        pass

    def unitTests(self):

    # assertion tests
        assert randomlab.random_object()
        assert randomlab.random_number(35)
        assert randomlab.random_bytes(2)
        assert randomlab.random_binary(32)
        assert randomlab.random_fraction()
        assert randomlab.random_integer(-55, 55)
        assert randomlab.random_double(-5.5, 5.5)
        test1 = [1, 2, 3, 4, 5, 6]
        test2 = ['a', 'b', 'c', 'd', 'e', 'f']
        test3 = [{'a'}, {'b'}, {'c'}, {'d'}, {'e'}, {'f'}]
        assert randomlab.random_shuffle(test1)
        assert randomlab.random_shuffle(test2)
        assert randomlab.random_shuffle(test3)

        return self

    def performanceTests(self):

        performlab.repeat(randomlab.random_double(1, 2), 'labRandom.random_double(1, 2)', 10000)
        test1 = [1, 2, 3, 4, 5, 6]
        performlab.repeat(randomlab.random_shuffle(test1), 'labRandom.random_shuffle([1,2,3,4,5,6])', 10000)
        test4 = [i for i in range(1000)]
        performlab.repeat(randomlab.random_shuffle(test4), 'labRandom.random_shuffle([1,2,..., 1000])', 10000)

        return self

if __name__ == '__main__':
    testlabRandom().unitTests()
    testlabRandom().performanceTests()
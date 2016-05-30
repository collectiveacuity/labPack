__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from labpack.randomization import labRandom
from labpack.performance import labPerform

class testlabRandom(object):

    def __init__(self):
        pass

    def unitTests(self):

    # assertion tests
        assert labRandom.object()
        assert labRandom.number(35)
        assert labRandom.bytes(2)
        assert labRandom.binary(32)
        assert labRandom.fraction()
        assert labRandom.integer(-55, 55)
        assert labRandom.double(-5.5, 5.5)
        test1 = [1, 2, 3, 4, 5, 6]
        test2 = ['a', 'b', 'c', 'd', 'e', 'f']
        test3 = [{'a'}, {'b'}, {'c'}, {'d'}, {'e'}, {'f'}]
        assert labRandom.shuffle(test1)
        assert labRandom.shuffle(test2)
        assert labRandom.shuffle(test3)

        return self

    def performanceTests(self):

        labPerform(labRandom.double(1, 2), 'labRandom.double(1, 2)', 10000)
        test1 = [1, 2, 3, 4, 5, 6]
        labPerform(labRandom.shuffle(test1), 'labRandom.shuffle([1,2,3,4,5,6])', 10000)
        test4 = [i for i in range(10000)]
        labPerform(labRandom.shuffle(test4), 'labRandom.shuffle([1,2,..., 10,000])', 10000)

        return self

if __name__ == '__main__':
    testlabRandom().unitTests()
    testlabRandom().performanceTests()
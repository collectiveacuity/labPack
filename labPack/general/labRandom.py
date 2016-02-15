__author__ = 'rcj1492'
__created__ = '2015.07'

# https://docs.python.org/2/library/random.html

from processor.methods.general.labValidation import labValid
import os
import binascii
import random

class labRandom(object):

    '''
        a class of methods for generating random data

        dependencies:
            from processor.methods.general.labValidation import labValid
            import os
            import binascii
            import random

    '''

    __name__ = 'labRandom'

    @classmethod
    def object(self):
        rand_data = os.urandom(32)
        rand_string = binascii.hexlify(rand_data).decode()
        return random.SystemRandom(rand_string)

    @classmethod
    def number(self, length):
        labValid.integer(length, 'Length input for %s.number' % self.__name__)
        low = pow(10, length - 1)
        high = pow(10, length) - 1
        return self.object().randint(low, high)

    @classmethod
    def bytes(self, length):
        labValid.integer(length, 'Length input for %s.bytes' % self.__name__)
        return os.urandom(length)

    @classmethod
    def binary(self, length):
        labValid.integer(length, 'Length input for %s.binary' % self.__name__)
        low = pow(2, length)
        high = pow(2, length + 1) - 1
        integer = self.object().randint(low, high)
        string = '{0:b}'.format(integer)
        return string[1:]

    @classmethod
    def fraction(self):
        return self.object().random()

    @classmethod        
    def integer(self, low, high):
        labValid.integer(low, 'Low input for %s.integer' % self.__name__)
        labValid.integer(high, 'High input for %s.integer' % self.__name__)
        return self.object().randint(low, high)

    @classmethod
    def double(self, low, high):
        labValid.float(low, 'Low input for %s.double' % self.__name__)
        labValid.float(high, 'High input for %s.double' % self.__name__)
        return self.object().uniform(low, high)
    
    @classmethod
    def shuffle(self, item_list):
        if not isinstance(item_list, list):
            raise TypeError('\nItem list input for %s.shuffle must be a list.' % self.__name__)
        random.shuffle(item_list, self.object().random)
        return item_list

    @classmethod
    def unitTests(self):
        assert self.object()
        assert self.number(35)
        assert self.bytes(2)
        assert self.binary(32)
        assert self.fraction
        assert self.integer(-55, 55)
        assert self.double(-5.5, 5.5)
        test1 = [1,2,3,4,5,6]
        test2 = ['a','b','c','d','e','f']
        test3 = [{'a'},{'b'},{'c'},{'d'},{'e'},{'f'}]
        assert self.shuffle(test1)
        assert self.shuffle(test2)
        assert self.shuffle(test3)
        return self

# labRandom.unitTests()

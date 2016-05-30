__author__ = 'rcj1492'
__created__ = '2015.07'
__license__ = 'MIT'

# https://docs.python.org/2/library/random.html
from os import urandom
from binascii import hexlify
from random import SystemRandom, shuffle

class labRandom(object):

    '''
        a class of methods to generate random data
    '''

    @classmethod
    def object(cls):
        rand_data = urandom(32)
        rand_string = hexlify(rand_data).decode()
        return SystemRandom(rand_string)

    @classmethod
    def number(cls, length):
        low = pow(10, length - 1)
        high = pow(10, length) - 1
        return cls.object().randint(low, high)

    @classmethod
    def bytes(cls, length):
        return urandom(length)

    @classmethod
    def binary(cls, length):
        low = pow(2, length)
        high = pow(2, length + 1) - 1
        integer = cls.object().randint(low, high)
        string = '{0:b}'.format(integer)
        return string[1:]

    @classmethod
    def fraction(cls):
        return cls.object().random()

    @classmethod
    def integer(cls, low, high):
        return cls.object().randint(low, high)

    @classmethod
    def double(cls, low, high):
        return cls.object().uniform(low, high)

    @classmethod
    def shuffle(cls, item_list):
        shuffle(item_list, cls.object().random)
        return item_list

if __name__ == '__main__':
    print(labRandom.fraction())

__author__ = 'rcj1492'
__created__ = '2015.07'
__license__ = 'MIT'

# https://docs.python.org/2/library/random.html
from os import urandom
from binascii import hexlify
from random import SystemRandom, shuffle

def random_object():
    rand_data = urandom(32)
    rand_string = hexlify(rand_data).decode()
    return SystemRandom(rand_string)

def random_number(length):
    low = pow(10, length - 1)
    high = pow(10, length) - 1
    return random_object().randint(low, high)

def random_bytes(length):
    return urandom(length)

def random_binary(length):
    low = pow(2, length)
    high = pow(2, length + 1) - 1
    integer = random_object().randint(low, high)
    string = '{0:b}'.format(integer)
    return string[1:]

def random_fraction():
    return random_object().random()

def random_integer(low, high):
    return random_object().randint(low, high)

def random_double(low, high):
    return random_object().uniform(low, high)

def random_shuffle(item_list):
    shuffle(item_list, random_object().random)
    return item_list

def random_characters(character_set, length):
    return ''.join(random_object().choice(character_set) for i in range(length))

if __name__ == '__main__':
    from string import ascii_lowercase
    print(random_fraction())
    print(random_characters(ascii_lowercase, 32))
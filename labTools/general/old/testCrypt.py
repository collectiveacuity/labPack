__author__ = 'rcj1492'
__created__ = '2015'

# pip install simplecrypt

import hashlib
import sha3
import base64
import codecs
import os
import random
import re
import binascii
import simplecrypt

def encrypt(string, password):
# create cipher method
    def simpleCipher(base_list, hex_string):
        i = int(hex_string, 16)
        count_list = base_list.copy()
        count_len = len(count_list)
        cipher_list = []
        while i and count_len > 0:
            i, rem = divmod(i, count_len)
            cipher_list.append(count_list[rem])
            del count_list[rem]
            count_len = len(count_list)
        return dict(zip(base_list, cipher_list))
# create shuffle dictionary
    base_list = []
    for i in range(0, 96):
        base_list.append(i)
    utf_bytes = password.encode('utf-8')
    hash_object = hashlib.sha3_512(utf_bytes)
    hex_string = hash_object.hexdigest()
    shuffle_dict = simpleCipher(base_list, hex_string)
# create substitution dictionary
    base_list = list('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
    hex_bytes = hash_object.hexdigest().encode()
    hash_object = hashlib.sha3_512(hex_bytes)
    hex_string = hash_object.hexdigest()
    sub_dict = simpleCipher(base_list, hex_string)
# convert text string to binary string
    utf_bytes = string.encode('utf-8')
    hex_string = binascii.hexlify(utf_bytes).decode()
    integer = int(hex_string, 16)
    binary_string = '{0:b}'.format(integer)
# return results
    temp_list = []
    temp_list.append(binary_string)
    temp_list.append(shuffle_dict)
    temp_list.append(sub_dict)
    return temp_list

test = encrypt('food and drink', 'bar')
print(test)

def encryptSimple(string, password):
    if not string:
        raise Exception('input does not contain all required parameters')
    elif not isinstance(string, str):
        raise Exception('input is not the correct datatype')
    else:
        t0 = time.perf_counter()
        cipher_text = simplecrypt.encrypt(password, string)
        print(time.perf_counter())
        return binascii.hexlify(cipher_text).decode()

def decryptSimple(string, password):
    if not string:
        raise Exception('input does not contain all required parameters')
    elif not isinstance(string, str):
        raise Exception('input is not the correct datatype')
    else:
        t0 = time.perf_counter()
        cipher_text = binascii.unhexlify(string.encode())
        plain_text = simplecrypt.decrypt(password, cipher_text)
        print(time.perf_counter())
        return plain_text.decode()

# print(len(test))
# test = encryptSimple(s, 'hi')
# print(test)
# test = decryptSimple(test, 'hi')
# print(test)

class testCrypt:
    '''
        dependencies:
        import hashlib
        import sha3 # pip install pysha3
        import base64
        import codecs
        import os
        import random
        import re
    '''
    def encrypt64(string="", password=""):
        if not string or not password:
            raise Exception('input does not have all required parameters')
        elif not isinstance(string, str) or not isinstance(password, str):
            raise Exception('parameters are the wrong data types')
        else:
        # define base 64 encoding system
            base_list = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_~')
            base_len = len(base_list)
        # create a randomly shuffled version of the base 64 list
            random_string = ''.join(base_list)
            random_list = list(random_string[0:len(random_string)-1])
            def randomMethod():
                randNum = random.SystemRandom(codecs.encode(os.urandom(1), 'hex').decode())
                return randNum.random()
            random.shuffle(random_list, randomMethod)
        # encode string to base 64 replacing '=' with url safe "~"
            utf_bytes = string.encode('utf-8')
            base64_string = base64.urlsafe_b64encode(utf_bytes).decode()
            base64_string = base64_string.replace('=','~')
        # add padding to the string with random base 64 characters
            rem = len(base64_string) % base_len
            extra = base_len - rem
            for i in range(0, 3):
                base64_string += '~'
            for i in range(0, extra):
                base64_string += random.choice(random_list)
        # create a 65-digit cipher dictionary from hash of password
            utf_bytes = password.encode('utf-8')
            hash_object = hashlib.sha3_512(utf_bytes)
            hex_string = hash_object.hexdigest()
            i = int(hex_string, 16)
            b_list = ''.join(base_list)
            b_list = list(b_list)
            b_len = len(b_list)
            cipher_list = []
            while i and b_len > 0:
                i, rem = divmod(i, b_len)
                cipher_list.append(b_list[rem])
                del b_list[rem]
                b_len = len(b_list)
            cipher_dict = dict(zip(base_list, cipher_list))
        # create a shuffle index based upon the order of a hash of the password hash
            s_hash_object = hashlib.sha3_512(utf_bytes)
            s_hex_string = s_hash_object.hexdigest()
            i = int(s_hex_string, 16)
            b_list = ''.join(base_list)
            b_list = list(b_list)
            b_len = len(b_list)
            shuffle_list = []
            while i and b_len > 0:
                i, rem = divmod(i, b_len)
                shuffle_list.append(b_list[rem])
                del b_list[rem]
                b_len = len(b_list)
            shuffle_index = []
            for i in range(0, len(base_list)):
                shuffle_index.append(shuffle_list.index(base_list[i]))
        # shuffle characters in the padded string according to order of the shuffle index
            shuffled_string = ''
            padded_string = ''.join(list(base64_string))
            padded_len = len(padded_string)
            while padded_len > base_len:
                for i in range(0, base_len):
                    shuffled_string += padded_string[shuffle_index[i]]
                padded_string = padded_string[base_len:padded_len]
                padded_len = len(padded_string)
            shuffled_string = shuffled_string + padded_string
        # substitute each character in the shuffled string with value in cipher dictionary
            encrypted_string = ''
            for i in range(0, len(shuffled_string)):
                cipher_key = shuffled_string[i]
                encrypted_string += cipher_dict[cipher_key]
            return encrypted_string

    def decrypt64(string="", password=""):
        if not string or not password:
            raise Exception('input does not have all required parameters')
        elif not isinstance(string, str) or not isinstance(password, str):
            raise Exception('parameters are the wrong data types')
        else:
        # define base 64 encoding system
            base_list = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_~')
            base_len = len(base_list)
        # create a 65-digit decipher dictionary from hash of password
            utf_bytes = password.encode('utf-8')
            hash_object = hashlib.sha3_512(utf_bytes)
            hex_string = hash_object.hexdigest()
            i = int(hex_string, 16)
            b_list = ''.join(base_list)
            b_list = list(b_list)
            b_len = len(b_list)
            cipher_list = []
            while i and b_len > 0:
                i, rem = divmod(i, b_len)
                cipher_list.append(b_list[rem])
                del b_list[rem]
                b_len = len(b_list)
            decipher_dict = dict(zip(cipher_list, base_list))
        # create an unshuffle index based upon the order of a hash of the password hash
            s_hash_object = hashlib.sha3_512(utf_bytes)
            s_hex_string = s_hash_object.hexdigest()
            i = int(s_hex_string, 16)
            b_list = ''.join(base_list)
            b_list = list(b_list)
            b_len = len(b_list)
            shuffle_list = []
            while i and b_len > 0:
                i, rem = divmod(i, b_len)
                shuffle_list.append(b_list[rem])
                del b_list[rem]
                b_len = len(b_list)
            unshuffle_index = []
            for i in range(0, len(shuffle_list)):
                unshuffle_index.append(base_list.index(shuffle_list[i]))
        # substitute each character in the encrypted string with value in decipher dict
            deciphered_string = ''
            for i in range(0, len(string)):
                decipher_key = string[i]
                deciphered_string += decipher_dict[decipher_key]
        # unshuffle characters in the deciphered string based upon unshuffle index
            unshuffled_string = ''
            padded_string = ''.join(list(deciphered_string))
            padded_len = len(padded_string)
            while padded_len > base_len:
                for i in range(0, base_len):
                    unshuffled_string += padded_string[unshuffle_index[i]]
                padded_string = padded_string[base_len:padded_len]
                padded_len = len(padded_string)
            unshuffled_string = unshuffled_string + padded_string
        # eliminate padding from unshuffled string
            pattern = re.compile('~{3}[^~]+')
            unpadded_string = pattern.sub('',unshuffled_string)
        # decode string from base 64
            unpadded_string = unpadded_string.replace('~','=')
            base64_bytes = base64.urlsafe_b64decode(unpadded_string)
            try:
                decrypted_string = base64_bytes.decode('utf-8')
                return decrypted_string
            except:
                raise Exception('password entered is not correct')
test = testCrypt.encrypt64('he has a cable in the stable!','hit')
assert testCrypt.decrypt64(test, 'hit') == 'he has a cable in the stable!'

url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')

def convertToURLFriendly(hex_bytes):
    hex_string = binascii.hexlify(hex_bytes).decode()
    integer = int(hex_string, 16)
    url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
    base_len = len(url_set)
    string = ''
    while integer:
        integer, remainder = divmod(integer, base_len)
        string = url_set[remainder] + string
    return string

def convertFromURLFriendly(string):
    url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
    base_dict = dict((c, v) for v, c in enumerate(url_set))
    base_len = len(url_set)
    number = 0
    for character in string:
        number = number * base_len + base_dict[character]
    hex_string = hex(number)
    hex_bytes = binascii.unhexlify(hex_string[2:].encode())
    return hex_bytes



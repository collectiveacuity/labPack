__author__ = 'rcj1492'
__created__ = '2015.06'

# HEXS = '0123456789abcdef'
# INTS = '0123456789'
# ISODT = 'YYYY-MM-DDTHH:MM:SS.mmmZ'

# RFC3986 URL unreserved character string
# CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ-._~' = 66 characters
# CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ-_' = 64 characters
# CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ' = 62 characters

# https://docs.python.org/2/library/base64.html
# https://www.npmjs.com/package/urlsafe-base64 / javascript

import binascii

class labHex(object):
    def __init__(self, data):
        if isinstance(data, str):
            self.asBytes = binascii.unhexlify(data.encode())
            self.asString = data
        elif isinstance(data, labHex):
            self.asBytes = data.asBytes
            self.asString = data.asString
        elif isinstance(data, bytes):
            self.asString = binascii.hexlify(data).decode()
            self.asBytes = data
        else:
            raise TypeError('labHex cannot handle ' + str(data.__class__) )
assert labHex('ab').asString == 'ab'
assert labHex(labHex('ab').asBytes).asString == 'ab'
data = labHex('abcd')
data1 = labHex(data)
print(data1.asBytes)


class labData:
    '''
        methods for converting data from one type to another
    '''
    def intToHex(integer):
        if not integer:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(integer, int):
            raise Exception('input is not the correct datatype')
        else:
            return format(integer, 'x')

    def intToBinary(integer):
        if not integer:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(integer, int):
            raise Exception('input is not the correct datatype')
        else:
            return '{0:b}'.format(integer)

    def intToURLFriendly(integer):
        if not integer:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(integer, int):
            raise Exception('input is not the correct datatype')
        else:
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            base_len = len(url_set)
            if not integer:
                return url_set[0]
            else:
                string = ''
                while integer:
                    integer, remainder = divmod(integer, base_len)
                    string = url_set[remainder] + string
                return string

    def intToBaseX(integer, base_set=False):
        if not integer:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(integer, int):
            raise Exception('integer input is not the correct datatype')
        else:
            alphanumeric_set = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if base_set:
                if not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                        and not isinstance(base_set, list):
                    raise Exception('base_set input must be a list, string or tuple')
                else:
                    alphanumeric_set = base_set
            base_set = tuple(''.join(alphanumeric_set))
            base_len = len(base_set)
            if not integer:
                return base_set[0]
            else:
                string = ''
                while integer:
                    integer, remainder = divmod(integer, base_len)
                    string = base_set[remainder] + string
                return string

    def hexToInt(hex_string):
        if not hex_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(hex_string, str):
            raise Exception('input is not the correct datatype')
        else:
            hex_string = labHex(hex_string).asString
            return int(hex_string, 16)

    def hexToBinary(hex_string):
        if not hex_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(hex_string, str):
            raise Exception('input is not the correct datatype')
        else:
            hex_string = labHex(hex_string).asString
            integer = int(hex_string, 16)
            return '{0:b}'.format(integer)

    def hexToURLFriendly(hex_string):
        if not hex_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(hex_string, str):
            raise Exception('input is not the correct datatype')
        else:
            hex_string = labHex(hex_string).asString
            integer = int(hex_string, 16)
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            base_len = len(url_set)
            if not integer:
                return url_set[0]
            else:
                string = ''
                while integer:
                    integer, remainder = divmod(integer, base_len)
                    string = url_set[remainder] + string
                return string

    def hexToBaseX(hex_string, base_set=False):
        if not hex_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(hex_string, str):
            raise Exception('input is not the correct datatype')
        else:
            hex_string = labHex(hex_string).asString
            integer = int(hex_string, 16)
            alphanumeric_set = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            if base_set:
                if not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                        and not isinstance(base_set, list):
                    raise Exception('base_set input must be a list, string or tuple')
                else:
                    alphanumeric_set = base_set
            base_set = tuple(''.join(alphanumeric_set))
            base_len = len(base_set)
            if not integer:
                return base_set[0]
            else:
                string = ''
                while integer:
                    integer, remainder = divmod(integer, base_len)
                    string = base_set[remainder] + string
                return string

    def binaryToInt(binary_string):
        if not binary_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(binary_string, str):
            raise Exception('input is not the correct datatype')
        else:
            binary_tuple = tuple(binary_string)
            binary_set = tuple('01')
            binary_test = []
            for i in range(0, len(binary_tuple)):
                 if binary_tuple[i] in binary_set:
                     binary_test.append(binary_tuple[i])
            if not len(binary_test) == len(binary_tuple):
                raise Exception('input is not a valid binary string')
            else:
                return int(binary_string, 2)

    def binaryToHex(binary_string):
        if not binary_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(binary_string, str):
            raise Exception('input is not the correct datatype')
        else:
            binary_tuple = tuple(binary_string)
            binary_set = tuple('01')
            binary_test = []
            for i in range(0, len(binary_tuple)):
                 if binary_tuple[i] in binary_set:
                     binary_test.append(binary_tuple[i])
            if not len(binary_test) == len(binary_tuple):
                raise Exception('input is not a valid binary string')
            else:
                integer = int(binary_string, 2)
                return format(integer, 'x')

    def binaryToURLFriendly(binary_string):
        if not binary_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(binary_string, str):
            raise Exception('input is not the correct datatype')
        else:
            binary_tuple = tuple(binary_string)
            binary_set = tuple('01')
            binary_test = []
            for i in range(0, len(binary_tuple)):
                 if binary_tuple[i] in binary_set:
                     binary_test.append(binary_tuple[i])
            if not len(binary_test) == len(binary_tuple):
                raise Exception('input is not a valid binary string')
            else:
                integer = int(binary_string, 2)
                url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
                base_len = len(url_set)
                if not integer:
                    return url_set[0]
                else:
                    string = ''
                    while integer:
                        integer, remainder = divmod(integer, base_len)
                        string = url_set[remainder] + string
                    return string

    def binaryToBaseX(binary_string, base_set=False):
        if not binary_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(binary_string, str):
            raise Exception('input is not the correct datatype')
        else:
            binary_tuple = tuple(binary_string)
            binary_set = tuple('01')
            binary_test = []
            for i in range(0, len(binary_tuple)):
                 if binary_tuple[i] in binary_set:
                     binary_test.append(binary_tuple[i])
            if not len(binary_test) == len(binary_tuple):
                raise Exception('input is not a valid binary string')
            else:
                integer = int(binary_string, 2)
                alphanumeric_set = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if base_set:
                    if not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
                        raise Exception('base_set input must be a list, string or tuple')
                    else:
                        alphanumeric_set = base_set
                base_set = tuple(''.join(alphanumeric_set))
                base_len = len(base_set)
                if not integer:
                    return base_set[0]
                else:
                    string = ''
                    while integer:
                        integer, remainder = divmod(integer, base_len)
                        string = base_set[remainder] + string
                    return string

    def urlFriendlyToBinary(url_friendly_string):
        if not url_friendly_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(url_friendly_string, str):
            raise Exception('input is not the correct datatype')
        else:
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            string = url_friendly_string
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in url_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('input is not a valid urlShorten string')
            else:
                base_dict = dict((c, v) for v, c in enumerate(url_set))
                base_len = len(url_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return '{0:b}'.format(integer)

    def urlFriendlyToInt(url_friendly_string):
        if not url_friendly_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(url_friendly_string, str):
            raise Exception('input is not the correct datatype')
        else:
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            string = url_friendly_string
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in url_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('input is not a valid urlShorten string')
            else:
                base_dict = dict((c, v) for v, c in enumerate(url_set))
                base_len = len(url_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return integer

    def urlFriendlyToHex(url_friendly_string):
        if not url_friendly_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(url_friendly_string, str):
            raise Exception('input is not the correct datatype')
        else:
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            string = url_friendly_string
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in url_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('input is not a valid urlShorten string')
            else:
                base_dict = dict((c, v) for v, c in enumerate(url_set))
                base_len = len(url_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return format(integer, 'x')

    def urlFriendlyToBaseX(url_friendly_string, base_set=False):
        if not url_friendly_string:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(url_friendly_string, str):
            raise Exception('input is not the correct datatype')
        else:
            url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            string = url_friendly_string
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in url_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('input is not a valid urlShorten string')
            else:
                base_dict = dict((c, v) for v, c in enumerate(url_set))
                base_len = len(url_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                alphanumeric_set = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if base_set:
                    if not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
                        raise Exception('base_set input must be a list, string or tuple')
                    else:
                        alphanumeric_set = base_set
                base_set = tuple(''.join(alphanumeric_set))
                base_len = len(base_set)
                if not integer:
                    return base_set[0]
                else:
                    string = ''
                    while integer:
                        integer, remainder = divmod(integer, base_len)
                        string = base_set[remainder] + string
                    return string

    def baseXToInt(string, base_set):
        if not string or not base_set:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str):
            raise Exception('input is not the correct datatype')
        elif not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
            raise Exception('base_set input must be a list, string or tuple')
        else:
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in base_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('string contains characters not in the base_set')
            else:
                base_dict = dict((c, v) for v, c in enumerate(base_set))
                base_len = len(base_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return integer

    def baseXToBinary(string, base_set):
        if not string or not base_set:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str):
            raise Exception('input is not the correct datatype')
        elif not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
            raise Exception('base_set input must be a list, string or tuple')
        else:
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in base_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('string contains characters not in the base_set')
            else:
                base_dict = dict((c, v) for v, c in enumerate(base_set))
                base_len = len(base_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return '{0:b}'.format(integer)

    def baseXToHex(string, base_set):
        if not string or not base_set:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str):
            raise Exception('input is not the correct datatype')
        elif not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
            raise Exception('base_set input must be a list, string or tuple')
        else:
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in base_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('string contains characters not in the base_set')
            else:
                base_dict = dict((c, v) for v, c in enumerate(base_set))
                base_len = len(base_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                return format(integer, 'x')

    def baseXToURLFriendly(string, base_set):
        if not string or not base_set:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str):
            raise Exception('input is not the correct datatype')
        elif not isinstance(base_set, str) and not isinstance(base_set, tuple) \
                            and not isinstance(base_set, list):
            raise Exception('base_set input must be a list, string or tuple')
        else:
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in base_set:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('string contains characters not in the base_set')
            else:
                base_dict = dict((c, v) for v, c in enumerate(base_set))
                base_len = len(base_set)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                url_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
                base_len = len(url_set)
                if not integer:
                    return url_set[0]
                else:
                    string = ''
                    while integer:
                        integer, remainder = divmod(integer, base_len)
                        string = url_set[remainder] + string
                    return string

    def baseXToBaseY(string, base_set_x, base_set_y=False):
        if not string or not base_set_x:
            raise Exception('input does not contain all required parameters')
        elif not isinstance(string, str):
            raise Exception('input is not the correct datatype')
        elif not isinstance(base_set_x, str) and not isinstance(base_set_x, tuple) \
                            and not isinstance(base_set_x, list):
            raise Exception('base_set_x input must be a list, string or tuple')
        else:
            input_test = []
            for i in range(0, len(tuple(string))):
                 if string[i] in base_set_x:
                     input_test.append(string[i])
            if not len(input_test) == len(string):
                raise Exception('string contains characters not in the base_set_x')
            else:
                base_dict = dict((c, v) for v, c in enumerate(base_set_x))
                base_len = len(base_set_x)
                integer = 0
                for character in string:
                    integer = integer * base_len + base_dict[character]
                alphanumeric_set = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if base_set_y:
                    if not isinstance(base_set_y, str) and not isinstance(base_set_y, tuple) \
                            and not isinstance(base_set_y, list):
                        raise Exception('base_set_y input must be a list, string or tuple')
                    else:
                        alphanumeric_set = base_set_y
                base_set_y = tuple(''.join(alphanumeric_set))
                base_len_y = len(base_set_y)
                if not integer:
                    return base_set_y[0]
                else:
                    string = ''
                    while integer:
                        integer, remainder = divmod(integer, base_len_y)
                        string = base_set_y[remainder] + string
                    return string
base_62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
base_56 = '23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
assert labData.intToHex(553379258) == '20fbe5ba'
assert labData.intToBinary(553379258) == '100000111110111110010110111010'
assert labData.intToURLFriendly(553379258) == '32h6eu'
assert labData.intToBaseX(553379258, base_62) == 'BrVdU'
assert labData.hexToInt('20fbe5ba') == 553379258
assert labData.hexToBinary('20fbe5ba') == '100000111110111110010110111010'
assert labData.hexToURLFriendly('20fbe5ba') == '32h6eu'
assert labData.hexToBaseX('20fbe5ba', base_62) == 'BrVdU'
assert labData.binaryToInt('100000111110111110010110111010') == 553379258
assert labData.binaryToHex('100000111110111110010110111010') == '20fbe5ba'
assert labData.binaryToURLFriendly('100000111110111110010110111010') == '32h6eu'
assert labData.binaryToBaseX('100000111110111110010110111010', base_62) == 'BrVdU'
assert labData.urlFriendlyToInt('32h6eu') == 553379258
assert labData.urlFriendlyToBinary('32h6eu') == '100000111110111110010110111010'
assert labData.urlFriendlyToHex('32h6eu') == '20fbe5ba'
assert labData.urlFriendlyToBaseX('32h6eu', base_62) == 'BrVdU'
assert labData.baseXToInt('BrVdU', base_62) == 553379258
assert labData.baseXToBinary('BrVdU', base_62) == '100000111110111110010110111010'
assert labData.baseXToHex('BrVdU', base_62) == '20fbe5ba'
assert labData.baseXToURLFriendly('BrVdU', base_62) == '32h6eu'
assert labData.baseXToBaseY('BrVdU', base_62, base_56) == '32h6eu'


# class labCodecs:
    # def ascii
    # def utf-8
    # def utf-16
    # def unicode


### Old Methods for reference

def oldConvertNumToBaseX(number, base_set=None):
    '''
        encode an integer into a string with any base
        https://stackoverflow.com/questions/1119722/base-62-conversion-in-python
    :param number: integer
    :param base_set: list (defaults to alphanumerics)
    :return: string
    '''
    if not isinstance(number, int):
        raise Exception('input is not an integer')
    else:
        if base_set:
            if list(base_set):
                base_alpha = tuple(base_set)
            else:
                raise Exception('base_set is not iterable')
        else:
            base_alpha = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        base_len = len(base_alpha)
        if number == 0:
            return base_alpha[0]
        new_array = []
        while number:
            remainder = number % base_len
            number = number // base_len
            new_array.append(base_alpha[remainder])
        new_array.reverse()
        return ''.join(new_array)

def oldConvertBaseXToNum(string, base_set=None):
    '''
        encode a string with any character set into an integer
    :param string: string
    :param base_set: list (defaults to alphanumerics)
    :return: integer
    '''
    if not isinstance(string, str):
        raise Exception('input is not a string')
    else:
        if base_set:
            if list(base_set):
                base_alpha = tuple(base_set)
            else:
                raise Exception('base_set is not iterable')
        else:
            base_alpha = tuple('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        base_len = len(base_alpha)
        strlen = len(string)
        number = 0
        idx = 0
        for character in string:
            power = (strlen - (idx + 1))
            number += base_alpha.index(character) * (base_len ** power)
            idx += 1
        return number
assert oldConvertBaseXToNum(oldConvertNumToBaseX(12345)) == 12345


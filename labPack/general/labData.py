__author__ = 'rcj1492'
__created__ = '2015.08'

import pytest
import binascii
import base64
from decimal import Decimal
from copy import deepcopy

class labDecimal(object):

    '''
        a class of methods to convert numerical data to and from decimal.Decimal data
        from decimal import Decimal
        import pytest
    '''

    __name__ = 'labDecimal'

    def __init__(self, input, title=''):

    # parse input types and setup base output methods
        if isinstance(input, bool):
            raise TypeError('%s input must be a number or decimal.' % title)
        elif isinstance(input, int) or isinstance(input, float):
            self.asDecimal = Decimal(str(input))
            self.asNumber = input
        elif isinstance(input, str):
            try:
                integer = int(input)
                self.asDecimal = Decimal(input)
                self.asNumber = integer
            except:
                try:
                    double = float(input)
                    self.asDecimal = Decimal(input)
                    self.asNumber = double
                except:
                    raise TypeError('%s input cannot be converted to a number.' % title)
        elif isinstance(input, Decimal):
            self.asDecimal = input
            if not float(input).is_integer():
                self.asNumber = float(input)
            else:
                self.asNumber = int(input)
        elif isinstance(input, labDecimal):
            self.asDecimal = input.asDecimal
            self.asNumber = input.asNumber
        else:
            raise TypeError('%s input must be a number or decimal.' % title)

    # define other details of decimal data
        self.exponent = self.asDecimal.as_tuple()[2]
        self.matissa = list(self.asDecimal.as_tuple()[1])

    def unitTests(self):
        test1 = labDecimal('3.141592653589793')
        test2 = labDecimal(3.141592653589793)
        test3 = labDecimal(3141592653589793)
        test4 = labDecimal(Decimal('3.141592653589793'))
        test5 = labDecimal(test1)
        assert test1.asNumber == test2.asNumber
        assert test1.asNumber == test4.asNumber
        assert test2.asDecimal == test4.asDecimal
        assert test2.asDecimal == test5.asDecimal
        assert isinstance(test3.matissa[1], int)
        assert test4.exponent == -15
        with pytest.raises(TypeError):
            labDecimal(True)
        return self

class labBytes(object):

    '''
        a class of methods to convert byte data to and from its different representations
        import binascii
        import base64
        import pytest
    '''

    __name__ = 'labBytes'

    def __init__(self, data, title=''):

    # parse input types and setup base output methods
        if isinstance(data, str):
            if len(data) % 2:
                raise ValueError('%s input cannot be an odd number of digits' % title)
            try:
                self.asBytes = binascii.unhexlify(data.encode())
                self.asString = data
            except:
                raise TypeError('%s input must be a valid hexidecimal string.' % title)
        elif isinstance(data, labBytes):
            self.asBytes = data.asBytes
            self.asString = data.asString
        elif isinstance(data, bytes):
            self.asString = binascii.hexlify(data).decode()
            self.asBytes = data
        else:
            raise TypeError('%s input must be hexadecimal data.' % title)

    # convert byte data to integer
        if self.asString == '':
            self.asInteger = 0
        else:
            self.asInteger = int(self.asString, 16)

    # convert byte data to binary string
        self.asBinary = '{0:b}'.format(self.asInteger)

    # convert byte data to a url safe base 64 string
        self.asBase64 = base64.urlsafe_b64encode(self.asBytes).decode()

    # convert byte data to a human friendly base 56 string
        base_set = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
        base_len = len(base_set)
        integer = deepcopy(self.asInteger)
        if not integer:
            self.asBase56 = base_set[0]
        else:
            string = ''
            while integer:
                integer, remainder = divmod(integer, base_len)
                string = base_set[remainder] + string
            self.asBase56 = string

    def asBaseX(self, char_set):

    # validate input
        try:
            base_set = tuple(char_set)
        except:
            raise TypeError('Character set must be an ordered list, tuple or string of characters.')
        if isinstance(char_set, set):
            raise TypeError('Character set must be an ordered list, tuple or string of characters.')
        elif len(set(char_set)) != len(base_set):
            raise TypeError('Character set cannot have duplicate characters.')
        for digit in base_set:
            if not isinstance(digit, str):
                raise TypeError('Character set must contain utf-8 characters.')

    # convert byte to new base with divmod of integer value
        base_len = len(base_set)
        integer = deepcopy(self.asInteger)
        if not integer:
            return base_set[0]
        else:
            string = ''
            while integer:
                integer, remainder = divmod(integer, base_len)
                string = base_set[remainder] + string
            return string

    def unitTests(self):
        assert labBytes('ab').asString == 'ab'
        assert labBytes(labBytes('ab').asBytes).asString == 'ab'
        data1 = labBytes('abcdef')
        data2 = labBytes(data1)
        assert isinstance(data1.asString, str)
        assert isinstance(data1.asInteger, int)
        assert isinstance(data1.asBinary, str)
        assert isinstance(data2.asBytes, bytes)
        assert isinstance(data2, labBytes)
        assert data1.asInteger == data2.asInteger
        assert data1.asBinary == '101010111100110111101111'
        assert data2.asBase64 == 'q83v'
        assert data2.asBase56 == '3a8nh'
        assert data1.asBaseX('01') == data2.asBinary
        assert data1.asBaseX(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        assert data1.asBaseX(tuple(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']))
        with pytest.raises(ValueError):
            labBytes('a')
        with pytest.raises(TypeError):
            labBytes('jk')
        with pytest.raises(TypeError):
            labBytes(2)
        with pytest.raises(TypeError):
            labBytes('abcdef').asBase64([1,2])
        with pytest.raises(TypeError):
            labBytes('abcdef').asBase64({'1','2'})
        with pytest.raises(TypeError):
            labBytes('abcdef').asBase64(['1','2','1'])
        return self

class modData(object):

    '''
        a class of recursive methods for modifying values inside object data
        type of modification depends upon code in self.action method
        sample action turns all primitives into strings
        import pytest
    '''

    __name__ = 'modData'

    def __init__(self, input):
        datatypes = [ 'string', '', True, False, 2, 0, 1.1, 0.0, None, [], {}, [ 'string' ], { 'key': 'pair' }, { 'string' } ]
        for data in datatypes:
            try:
                attempt = self.action(data)
            except:
                raise TypeError('\nModifying action must validate %s datatype inputs.' % data.__class__)
        if isinstance(input, dict):
            self.output = self.dict(input)
        elif isinstance(input, list):
            self.output = self.list(input)
        elif isinstance(input, set):
            self.output = self.set(input)
        else:
            self.output = self.action(input)

    def dict(self, dict_object):

        '''
            a method for recursively modifying the values of a dictionary
        :param dict_object: dictionary with key-value pairs
        :return: dictionary with modified values
        '''

        for key, value in dict_object.items():
            if not value:
                dict_object[key] = self.action(value)
            else:
                if isinstance(value, dict):
                    self.dict(value)
                elif isinstance(value, list):
                    self.list(value)
                elif isinstance(value, set):
                    dict_object[key] = self.set(value)
                else:
                    dict_object[key] = self.action(value)

        return dict_object

    def list(self, list_object):

        '''
            a method for recursively modifying the values of a list
        :param list_object: list with items
        :return: list with modified values
        '''

        for i in range(0, len(list_object)):
            if not list_object[i]:
                list_object[i] = self.action(list_object[i])
            else:
                if isinstance(list_object[i], list):
                    self.list(list_object[i])
                elif isinstance(list_object[i], dict):
                    self.dict(list_object[i])
                elif isinstance(list_object[i], set):
                    list_object[i] = self.set(list_object[i])
                else:
                    list_object[i] = self.action(list_object[i])

        return list_object

    def set(self, set_object):

        '''
            a method for recursively modifying the items of a set
        :param set_object: set with items
        :return: set with modified values
        '''

        new_set = set()
        for item in set_object:
            new_set.add(self.action(item))
        return new_set

    def action(self, value):
        if isinstance(value, bool):
            return str(value)
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        else:
            return value

    def unitTests(self):
        record = {
            'active': True,
            'id': '3nwaA3sLGWEeeRUmzuJLTcLDECrUx7D9Jbaw',
            'dT': 1440184621.607344,
            'score': 2,
            'dict': { 'key1': 'string',
                      'key2': 2,
                      'key3': 2.2,
                      'key4': True,
                      'set1': { 1, 2, 3 },
                      'set2': { True },
                      'set3': { 1.1, 2.2, 3.3 },
                      'set4': { "one", "two", "three" },
                      'list1': [ 1, 2, 3 ],
                      'list2': [ 1.1, 2.2, 3.3 ],
                      'list3': [ 'one', 'two', 'three' ],
                      'list4': [ True ],
                      'list5': [ { 1, 2, 3 } ],
                      'list6': [ { 'key': 'value' } ],
                      'list7': [ [ 1, 2, 3 ], [ 4.4, 5.5, 6.6 ] ]
                      }
                }
        assert self.dict(record)['dict']['list7'][0][0] == '1'
        return self

class deltaData(object):

    '''
        a class of recursive methods for identifying changes between two objects
        from copy import deepcopy
    '''

    __name__ = 'deltaData'

    def __init__(self, new_details, old_details):

        '''

        :param new_details: set, list or dictionary with new details of an item
        :param old_details: set, list or dictionary with old details of an item
        :return: list with dictionary of changes
        '''

        if new_details.__class__ != old_details.__class__:
            raise TypeError('\nDatatype of new and old data must match.')
        new_map = deepcopy(new_details)
        old_map = deepcopy(old_details)
        if isinstance(new_map, dict):
            self.output = self.dict(new_map, old_map, [], [])
        elif isinstance(new_map, list):
            self.output = self.list(new_map, old_map, [], [])
        elif isinstance(new_map, set):
            self.output = self.set(new_map, old_map, [], [])
        else:
            raise TypeError('\nData inputs must be sets, lists or dictionaries.')

    def dict(self, new_dict, old_dict, change_list=None, root=None):
        '''
            a method for recursively listing changes made to a dictionary
        :param new_dict: dictionary with new key-value pairs
        :param old_dict: dictionary with old key-value pairs
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''
        new_keys = set(new_dict.keys())
        old_keys = set(old_dict.keys())
        missing_keys = old_keys - new_keys
        extra_keys = new_keys - old_keys
        same_keys = new_keys.intersection(old_keys)
        for key in missing_keys:
            new_path = deepcopy(root)
            new_path.append(key)
            change_list.append({'action': 'DELETE', 'value': None, 'path': new_path})
        for key in extra_keys:
            for k, v in new_dict.items():
                if key == k:
                    new_path = deepcopy(root)
                    new_path.append(key)
                    change_list.append({'action': 'ADD', 'value': v, 'path': new_path})
        for key in same_keys:
            new_path = deepcopy(root)
            new_path.append(key)
            if new_dict[key].__class__ != old_dict[key].__class__:
                change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
            elif isinstance(new_dict[key], dict):
                self.dict(new_dict[key], old_dict[key], change_list, new_path)
            elif isinstance(new_dict[key], list):
                self.list(new_dict[key], old_dict[key], change_list, new_path)
            elif isinstance(new_dict[key], set):
                self.set(new_dict[key], old_dict[key], change_list, new_path)
            elif new_dict[key] != old_dict[key]:
                change_list.append({'action': 'UPDATE', 'value': new_dict[key], 'path': new_path})
        return change_list

    def list(self, new_list, old_list, change_list=None, root=None):
        '''
            a method for recursively listing changes made to a list
        :param new_list: list with new value
        :param old_list: list with old values
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''
        if len(old_list) > len(new_list):
            same_len = len(new_list)
            for i in reversed(range(len(new_list), len(old_list))):
                new_path = deepcopy(root)
                new_path.append(i)
                change_list.append({'action': 'REMOVE', 'value': None, 'path': new_path})
        elif len(new_list) > len(old_list):
            same_len = len(old_list)
            append_list = []
            path = deepcopy(root)
            for i in range(len(old_list), len(new_list)):
                append_list.append(new_list[i])
            change_list.append({'action': 'APPEND', 'value': append_list, 'path': path})
        else:
            same_len = len(new_list)
        for i in range(0, same_len):
            new_path = deepcopy(root)
            new_path.append(i)
            if new_list[i].__class__ != old_list[i].__class__:
                change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
            elif isinstance(new_list[i], dict):
                self.dict(new_list[i], old_list[i], change_list, new_path)
            elif isinstance(new_list[i], list):
                self.list(new_list[i], old_list[i], change_list, new_path)
            elif isinstance(new_list[i], set):
                self.set(new_list[i], old_list[i], change_list, new_path)
            elif new_list[i] != old_list[i]:
                change_list.append({'action': 'UPDATE', 'value': new_list[i], 'path': new_path})
        return change_list

    def set(self, new_set, old_set, change_list, root):
        '''
            a method for list changes made to a set
        :param new_set: set with new values
        :param old_set: set with old values
        :param change_list: list of differences between old and new
        :patam root: string with record of path to the root of the main object
        :return: list of differences between old and new
        '''
        path = deepcopy(root)
        missing_items = old_set - new_set
        extra_items = new_set - old_set
        for item in missing_items:
            change_list.append({'action': 'REMOVE', 'key': None, 'value': item, 'path': path})
        for item in extra_items:
            change_list.append({'action': 'ADD', 'key': None, 'value': item, 'path': path})
        return change_list

    def unitTests(self):
        newRecord = {
            'active': True,
            'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
            'dT': 1440184621.607344,
            'score': 400,
            'dict1': { 'key': 'value' },
            'list1': [ 'item' ],
            'dict2': {
                'key1': 'string',
                'key2': 2.2,
                'key3': 2,
                'key4': True,
                'dict': {
                    'key': 'value',
                    'list1': [ 'item' ],
                    'list2': [ 'item', 2, 2.2, True, { 'key': 'newValue' } ]
                } },
            'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
        }
        oldRecord = {
            'active': True,
            'id': 'd53iedBwKNcFCJXLEAWHCfCT3zGLCu93rxTG',
            'dT': 1440184621.607344,
            'score': 400,
            'dict1': { 'key': 'value' },
            'list1': [ 'item' ],
            'dict2': {
                'key1': 'string',
                'key2': 2.2,
                'key3': 2,
                'key4': True,
                'dict': {
                    'key': 'value',
                    'list1': [ 'item' ],
                    'list2': [ 'item', 2, 2.2, True, { 'key': 'oldValue' } ]
                } },
            'list2': [ 'item', 2, 2.2, True, { 'key': 'value', 'list': [ 2, 2.2, True, 'item' ] } ]
        }
        assert self.dict(newRecord, oldRecord, [], [])[0]['path'][4] == 'key'
        return self

dummy = ''
# labDecimal(0).unitTests()
# labBytes('').unitTests()
# modData({}).unitTests()
# deltaData({},{}).unitTests()
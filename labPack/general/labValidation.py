__author__ = 'rcj1492'
__created__ = '2015.09'

import re
import os
from ipaddress import ip_address
from decimal import Decimal
from copy import deepcopy
from base64 import b64decode

class labValid(object):

    '''
        a class of methods for validating inputs of python objects

        dependencies:
            import re
            from decimal import Decimal
    '''

    @classmethod
    def datatype(self, input, datatype_list, title=''):
        data_match = False
        data_list = []
        for data in datatype_list:
            data_list.append(data.__class__)
            if isinstance(input, bool) and isinstance(data, int):
                if isinstance(data, bool):
                    data_match = True
                pass
            elif isinstance(input, data.__class__):
                data_match = True
            elif isinstance(input, int) and isinstance(data, float):
                data_match = True
        if not data_match:
            raise TypeError('\n%s must be one of %s datatypes.' % (title, data_list))
        return input

    @classmethod
    def string(self, input, prohibited_char='', min_length=0, max_length=0, title=''):
        if not title:
            title = 'String input'
        try:
            assert input == str(input)
        except:
            raise TypeError('\n%s must be an utf-8 encoded string.' % title)
        if min_length and len(input) < min_length:
            raise ValueError('\n%s must be at least %s characters.' % (title, min_length))
        if max_length and len(input) > max_length:
            raise ValueError('\n%s cannot be more than %s characters.' % (title, max_length))
        if prohibited_char:
            bad_char = re.compile(prohibited_char)
            bad_char_list = bad_char.findall(input)
            if bad_char_list:
                raise ValueError('\n%s cannot contain %s characters.' % (title, bad_char_list))
        return input

    @classmethod
    def integer(self, input, min_value=0, max_value=0, title=''):
        if not isinstance(input, int):
            raise TypeError('\n%s input must be an integer.' % title)
        elif min_value and input < min_value:
            raise ValueError('\n%s input cannot be less than %s.' % (title, min_value))
        elif max_value and input > max_value:
            raise ValueError('\n%s input cannot be greater than %s.' % (title, max_value))
        return input

    @classmethod
    def number(self, input, min_value=None, max_value=None, precision=0, min_exp=0, title=''):
        if isinstance(input, bool):
            raise TypeError('\n%s input is not numerical.' % title)
        elif isinstance(input, float) or isinstance(input, int):
            input_dec = Decimal(str(input))
        else:
            try:
                input_dec = Decimal(input)
            except:
                raise TypeError('\n%s input is not numerical.' % title)
        input_tuple = input_dec.as_tuple()
        digit_list = list(input_tuple.digits)
        input_digits = ''
        for i in digit_list:
            input_digits += str(i)
        if precision and len(input_digits) > precision:
            raise ValueError('\n%s input cannot be stored accurately beyond %s digit precision' % (title, precision))
        if min_exp and int(input_tuple.exponent) < min_exp:
            raise ValueError('\n%s input exceeds the minimum exponent size of %s' % (title, min_exp))
        if min_value and input_dec < min_value:
            raise ValueError('\n%s input cannot be less than %s' % (title, min_value))
        if max_value and input_dec > max_value:
            raise ValueError('\n%s input cannot be greater than %s' % (title, max_value))
        return input

    @classmethod
    def path(self, input, title=''):
        if not isinstance(input, str):
            raise TypeError('\n%s input must be a string.' % title)
        try:
            os.listdir(path=input)
        except:
            raise ValueError('\n%s does not exist in local environment.' % title)
        return input

    @classmethod
    def reqData(self, test_data, req_data, null_values=False, title=''):
        '''
            a method for recursively testing a data collection against requirements
        :param test_data: list or dictionary with values being tested
        :param req_data: list or dictionary with required value types
        :param null_values: [optional] boolean to allow null values
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        if test_data.__class__ != req_data.__class__:
            raise TypeError('\nTest data and Required data must be the same datatype.')
        elif isinstance(test_data, dict):
            return self.reqDict(test_data, req_data, path_to_root='', null_values=null_values, title=title)
        elif isinstance(test_data, list):
            return self.reqList(test_data, req_data, path_to_root='', null_values=null_values, title=title)
        else:
            raise TypeError('\nTest data must be a list or dictionary.')

    @classmethod
    def reqDict(self, test_dict, req_dict, path_to_root='', null_values=False, title=''):
        '''
            a method for recursively testing a dictionary against requirements
        :param test_dict: dictionary with keys-value pairs being tested
        :param req_dict: dictionary with required key-value pairs
        :param path_to_root: string with recursive record of location
        :param null_values: [optional] boolean to allow null values in key-value pairs
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        null_test = null_values
        current_path = path_to_root
        for req_key, req_value in req_dict.items():
            index_error = "\nRequired key not found at %s%s['%s']" % (title, current_path, req_key)
            type_error = "\nValue for %s%s['%s'] must be a %s datatype." % (title, current_path, req_key, req_value.__class__)
            value_error = "\nValue for %s%s['%s'] cannot be empty." % (title, current_path, req_key)
            if not isinstance(req_value, dict):
                if not req_key in test_dict:
                    raise IndexError(index_error)
                elif isinstance(req_value, set):
                    data_match = False
                    data_type_list = []
                    for item in req_value:
                        if item.__class__ not in data_type_list:
                            data_type_list.append(item.__class__)
                        if test_dict[req_key].__class__ == item.__class__:
                            data_match = True
                    if not data_match:
                        raise TypeError("\nValue for %s%s['%s'] must be a %s datatype." % (title, current_path, req_key, data_type_list))
                elif test_dict[req_key].__class__ != req_value.__class__:
                    raise TypeError(type_error)
                elif req_value:
                    if not null_test and not test_dict[req_key]:
                        raise ValueError(value_error)
                    elif isinstance(req_value, list):
                        new_path = current_path + "['" + req_key + "']"
                        self.reqList(test_dict[req_key], req_value, path_to_root=new_path, null_values=null_test, title=title)
            else:
                if not req_key in test_dict:
                    raise IndexError(index_error)
                elif not isinstance(test_dict[req_key], dict):
                    raise TypeError(type_error)
                elif req_value:
                    if not null_test and not test_dict[req_key]:
                        raise ValueError(value_error)
                    else:
                        new_path = current_path + "['" + req_key + "']"
                        self.reqDict(test_dict[req_key], req_value, path_to_root=new_path, null_values=null_test, title=title)
        return True

    @classmethod
    def reqList(self, test_list, req_list, path_to_root='', null_values=False, title=''):
        '''
            a method for recursively testing a dictionary against requirements
        :param test_list: list with items being tested
        :param req_list: list with required items
        :param path_to_root: string with recursive record of location
        :param null_values: [optional] boolean to allow null lists or null item values
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        null_test = null_values
        current_path = path_to_root
        for i in range(0, len(req_list)):
            type_error = '\nValue for item at %s%s[%s] must be a %s datatype.' % (title, current_path, i, req_list[i].__class__)
            value_error = '\nValue for item at %s%s[%s] cannot be empty.' % (title, current_path, i)
            index_error = '\nItem at %s%s[%s] is missing.' % (title, current_path, i)
            if not isinstance(req_list[i], list):
                if len(test_list) - 1 < i:
                    raise IndexError(index_error)
                elif isinstance(req_list[i], set):
                    data_match = False
                    data_type_list = []
                    for item in req_list[i]:
                        if item.__class__ not in data_type_list:
                            data_type_list.append(item.__class__)
                        if test_list[i].__class__ == item.__class__:
                            data_match = True
                    if not data_match:
                        raise TypeError("\nValue for item at %s%s[%s] must be a %s datatype." % (title, current_path, i, data_type_list))
                elif test_list[i].__class__ != req_list[i].__class__:
                    raise TypeError(type_error)
                elif req_list[i]:
                    if not null_test and not test_list[i]:
                        raise ValueError(value_error)
                    elif isinstance(req_list[i], dict):
                        new_path = current_path + '[' + str(i) + ']'
                        self.reqDict(test_list[i], req_list[i], path_to_root=new_path, null_values=null_test, title=title)
            else:
                if len(test_list) - 1 < i:
                    raise IndexError(index_error)
                elif not isinstance(test_list[i], list):
                    raise TypeError(type_error)
                elif req_list[i]:
                    if not null_test and not test_list[i]:
                        raise ValueError(value_error)
                    else:
                        new_path = current_path + '[' + str(i) + ']'
                        self.reqList(test_list[i], req_list[i], path_to_root=new_path, null_values=null_test, title=title)
        return True

    @classmethod
    def maxData(self, test_data, max_data, null_values=True, title=''):
        '''
            a method for recursively testing a data collection against maximum bounds
        :param test_data: list or dictionary with values being tested
        :param max_data: list or dictionary with definitions of maximum bounds
        :param null_values: [optional] boolean to allow null values
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        if test_data.__class__ != max_data.__class__:
            raise TypeError('\nTest data and max data must be the same datatype.')
        elif isinstance(test_data, dict):
            return self.maxDict(test_data, max_data, path_to_root='', null_values=null_values, title=title)
        elif isinstance(test_data, list):
            return self.maxList(test_data, max_data, path_to_root='', null_values=null_values, title=title)
        else:
            raise TypeError('\nTest data must be a list or dictionary.')

    @classmethod
    def maxDict(self, test_dict, max_dict, path_to_root='', null_values=True, title=''):
        '''
            a method for recursively testing a dictionary against a maximum scope
        :param test_dict: dictionary with keys-value pairs being tested
        :param max_dict: dictionary with largest scope of key-value pairs
        :param path_to_root: string with recursive record of location
        :param null_values: [optional] boolean to allow null values in key-value pairs
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        null_test = null_values
        current_path = path_to_root
        for test_key, test_value in test_dict.items():
            index_error = "\nKey %s%s['%s'] not found in max dictionary." % (title, current_path, test_key)
            if not isinstance(test_value, dict):
                if not test_key in max_dict:
                    raise IndexError(index_error)
                elif isinstance(max_dict[test_key], set):
                    data_match = False
                    data_type_list = []
                    for item in max_dict[test_key]:
                        if item.__class__ not in data_type_list:
                            data_type_list.append(item.__class__)
                        if test_dict[test_key].__class__ == item.__class__:
                            data_match = True
                    if not data_match:
                        raise TypeError("\nValue for %s%s['%s'] must be a %s datatype." % (title, current_path, test_key, data_type_list))
                elif max_dict[test_key].__class__ != test_value.__class__:
                    raise TypeError("\nValue for %s%s['%s'] must be a %s datatype." % (title, current_path, test_key, max_dict[test_key].__class__))
                elif max_dict[test_key]:
                    if not null_test and not test_dict[test_key]:
                        raise ValueError("\nValue for %s%s['%s'] cannot be empty." % (title, current_path, test_key))
                    elif isinstance(test_value, list):
                        new_path = current_path + "['" + test_key + "']"
                        self.maxList(test_value, max_dict[test_key], path_to_root=new_path, null_values=null_test, title=title)
            else:
                if not test_key in max_dict:
                    raise IndexError(index_error)
                elif not isinstance(max_dict[test_key], dict):
                    raise TypeError("\nValue for %s%s['%s'] must be a %s datatype." % (title, current_path, test_key, max_dict[test_key].__class__))
                elif max_dict[test_key]:
                    if not null_test and not test_dict[test_key]:
                        raise ValueError("\nValue for %s%s['%s'] cannot be empty." % (title, current_path, test_key))
                    else:
                        new_path = current_path + "['" + test_key + "']"
                        self.maxDict(test_value, max_dict[test_key], path_to_root=new_path, null_values=null_test, title=title)
        return True

    @classmethod
    def maxList(self, test_list, max_list, path_to_root='', null_values=True, title=''):
        '''
            a method for recursively testing a dictionary against requirements
        :param test_list: list with items being tested
        :param max_list: list with maximum scope of items
        :param path_to_root: string with recursive record of location
        :param null_values: [optional] boolean to allow null lists or null item values
        :param title: [optional] string with name of data being tested
        :return: True (or Raises Exceptions)
        '''
        null_test = null_values
        current_path = path_to_root
        for i in range(0, len(test_list)):
            value_error = '\nValue for item at %s%s[%s] cannot be empty.' % (title, current_path, i)
            if not isinstance(test_list[i], list):
                if len(max_list) - 1 < i:
                    raise IndexError('\nLength of list at %s%s is greater than the maximum index of %s.' % (title, current_path, len(max_list)))
                elif isinstance(max_list[i], set):
                    data_match = False
                    data_type_list = []
                    for item in max_list[i]:
                        if item.__class__ not in data_type_list:
                            data_type_list.append(item.__class__)
                        if test_list[i].__class__ == item.__class__:
                            data_match = True
                    if not data_match:
                        raise TypeError("\nValue for item at %s%s[%s] must be a %s datatype." % (title, current_path, i, data_type_list))
                elif max_list[i].__class__ != test_list[i].__class__:
                    raise TypeError('\nValue for item at %s%s[%s] must be a %s datatype.' % (title, current_path, i, max_list[i].__class__))
                elif max_list[i]:
                    if not null_test and not test_list[i]:
                        raise ValueError(value_error)
                    elif isinstance(test_list[i], dict):
                        new_path = current_path + '[' + str(i) + ']'
                        self.maxDict(test_list[i], max_list[i], path_to_root=new_path, null_values=null_test, title=title)
            else:
                if len(max_list) - 1 < i:
                    raise IndexError('\nLength of list at %s%s is greater than the maximum scope of %s.' % (title, current_path, len(max_list)))
                elif not isinstance(max_list[i], list):
                    raise TypeError('\nValue for %s%s[%s] must be a %s datatype.' % (title, current_path, i, max_list[i].__class__))
                elif max_list[i]:
                    if not null_test and not test_list[i]:
                        raise ValueError(value_error)
                    else:
                        new_path = current_path + '[' + str(i) + ']'
                        self.maxList(test_list[i], max_list[i], path_to_root=new_path, null_values=null_test, title=title)
        return True

    @classmethod
    def validateAlphaNumeric(self, string):
        '''
            verifies that a given string is an alphanumeric
            https://docs.python.org/2/howto/regex.html
            import re
        :param string: string
        :return: boolean
        '''
        if not isinstance(string, str):
            return False
        else:
            pattern = re.compile('\W+')
            if not pattern.findall(string):
                return True
            else:
                return False

    @classmethod
    def validateURL(self, string):
        '''
            verifies that a given string has valid URL syntax
            https://docs.python.org/2/howto/regex.html
            https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
            import re
        :param string: string
        :return: boolean
        '''
        if not string:
            raise Exception('input does not have all required parameters')
        elif not isinstance(string, str):
            return False
        else:
            pattern1 = re.compile('https?://')
            pattern2 = re.compile('[\w\-]+\.[a-z][a-z]+/')
            pattern3 = re.compile('[\w\-]+\.xn\-\-[a-z0-9]+/')
            pattern4 = re.compile('[^0-9a-zA-Z/:=_,&~@#\.\-\?\+\$]+')
            if (pattern1.match(string) or pattern2.search(string) or pattern3.search(string)) and \
                   not pattern4.findall(string):
                return True
            else:
                return False

    @classmethod
    def validateEmail(self, string):
        '''
            verifies that a given string has valid email syntax
            https://docs.python.org/2/howto/regex.html
            import re
        :param string:
        :return: boolean
        '''
        if not string:
            raise Exception('input does not have all required parameters')
        elif not isinstance(string, str):
            return False
        else:
            pattern1 = re.compile('[\w\.\-]+@[\w\-\.]+\.[a-z][a-z]+$')
            pattern2 = re.compile('[\w\.\-]+@[\w\-\.]+\.xn\-\-[a-z0-9]+$')
            pattern3 = re.compile('[^\w@\.\-]+')
            if (pattern1.match(string) or pattern2.match(string)) and not pattern3.match(string):
                return True
            else:
                return False

    @classmethod
    def unitTests(self):
        assert labValid.datatype(3, [1])
        assert labValid.integer(67, min_value=66, max_value=67)
        assert labValid.string('hello@gym.time', prohibited_char='<>$')
        assert labValid.number(1443734240.058347, min_value=.000001, max_value=5000000000.1, precision=17, min_exp=-15)
        assert labValid.path('../../')
        assert labValid.validateAlphaNumeric('http:\/\/www.meetup.com\/insidestartupsclub\/') == False
        assert labValid.validateAlphaNumeric('insidestartupsclub') == True
        assert labValid.validateAlphaNumeric(123) == False
        assert labValid.validateURL('http:\/\/www.meetup.com\/insidestartupsclub\/events\/221\/') == False
        assert labValid.validateURL('http://www.meetup.com/<script>') == False
        assert labValid.validateURL('http://www.meetup.com/insidestartups/events/2/?p=7&k=U_-,&~@#+$') == True
        assert labValid.validateURL('u.me/') == True
        assert labValid.validateURL(123) == False
        assert labValid.validateEmail('r@m.me') == True
        assert labValid.validateEmail('!@m.me') == False
        assert labValid.validateEmail('really_long-emailname.foruser@really.longemailaddress.com') == True
        assert labValid.validateEmail('number@the.topd0main') == False
        assert labValid.validateEmail('strange@character$.com') == False
        assert labValid.validateEmail('r@me.xn--internationaltopdomain') == True
        return self

class labString(str):

    '''
        a class of methods for parsing, formatting and validating a string
        
        dependencies:
            import re
            from copy import deepcopy
            import b
        
        built-in methods:
            all standard string methods

    '''

    def __init__(self, input):

        name = '%s.__init__()' % self.__class__.__name__

        self.title = 'String input'

        try:
            assert input == str(input)
        except:
            raise TypeError('\n%s for %s must be an utf-8 encoded string.' % (self.title, name))

        str.__init__(input)

    def argument(self, argument, name):

        try:
            assert argument == str(argument)
        except:
            raise TypeError('\n%s must be a string.' % name)

        return True

    def rename(self, title):

        name = 'title argument for %s.rename()' % self.__class__.__name__

        self.argument(title, name)
        self.title = title

        return self

    def validate(self, byte_data=False, min_length=None, max_length=None, must_contain=None, must_not_contain=None, contains_either=None, discrete_values=None):
        
        '''
            a method to validate the string against a number of criteria
        
        :param byte_data: boolean
        :param min_length: integer
        :param max_length: integer
        :param must_contain: list
        :param must_not_contain: list
        :param contains_either: list
        :param discrete_values: list
        :return: labString
        '''

        if byte_data:
            error_msg = '\n%s must be a 64 byte encodable string.' % self.title
            try:
                decoded_bytes = b64decode(self)
            except:
                raise TypeError(error_msg)
            if not isinstance(decoded_bytes, bytes):
                raise TypeError(error_msg)

        if min_length or min_length == 0:
            error_msg = '\n%s cannot be less than %s.' % (self.title, min_length)
            if not isinstance(min_length, int):
                raise Exception('min_length argument for %s.validate() must be an integer.' % self.__class__.__name__)
            elif min_length < 0:
                raise ValueError('min_length argument for %s.validate() may not be negative.' % self.__class__.__name__)
            elif len(self) < min_length:
                raise ValueError(error_msg)

        if max_length or max_length == 0:
            error_msg = '\n%s cannot be greater than %s.' % (self.title, max_length)
            if not min_length:
                min_length = 0
            if not isinstance(max_length, int):
                raise Exception('max_length argument for %s.validate() must be an integer.' % self.__class__.__name__)
            elif max_length < 0:
                raise ValueError('max_length argument for %s.validate() may not be negative.', self.__class__.__name__)
            elif max_length < min_length:
                raise ValueError('max_length argument for %s.validate() may not be less than min_length.', self.__class__.__name__)
            elif len(self) > max_length:
                raise ValueError(error_msg)

        if must_contain:
            if not isinstance(must_contain, list):
                raise TypeError('must_contain argument for %s.validate() must be a list.' % self.__class__.__name__)
            for i in range(len(must_contain)):
                if not isinstance(must_contain[i], str):
                    raise TypeError('item [%s] of must_contain argument for %s.validate() is not a string.' % (i, self.__class__.__name__))
                regex = must_contain[i]
                error_msg = "\n%s must contain pattern '%s'" % (self.title, regex)
                regex_pattern = re.compile(regex)
                if not regex_pattern.findall(self):
                    raise ValueError(error_msg)

        if must_not_contain:
            if not isinstance(must_not_contain, list):
                raise TypeError('must_not_contain argument for %s.validate() must be a list.' % self.__class__.__name__)
            for i in range(len(must_not_contain)):
                if not isinstance(must_not_contain[i], str):
                    raise TypeError('item [%s] of must_not_contain argument for %s.validate() is not a string.' % (i, self.__class__.__name__))
                regex = must_not_contain[i]
                regex_pattern = re.compile(regex)
                regex_match = regex_pattern.findall(self)
                if regex_match:
                    error_msg = "\n%s must not contain %s which match pattern '%s'" % (self.title, regex_match, regex)
                    raise ValueError(error_msg)

        if contains_either:
            if not isinstance(contains_either, list):
                raise TypeError('contains_either argument for %s.validate() must be a list.' % self.__class__.__name__)
            regex_match = []
            for i in range(len(contains_either)):
                if not isinstance(contains_either[i], str):
                    raise TypeError('item [%s] of contains_either argument for %s.validate() is not a string.' % (i, self.__class__.__name__))
                regex = contains_either[i]
                regex_pattern = re.compile(regex)
                for match in regex_pattern.findall(self):
                    regex_match.append(match)
            if not regex_match:
                error_msg = "\n%s must contain either of %s patterns." % (self.title, contains_either)
                raise ValueError(error_msg)

        if discrete_values:
            if not isinstance(discrete_values, list):
                raise TypeError('discrete_values argument for %s.validate() must be a list.' % self.__class__.__name__)
            error_msg = "\n%s must be one of %s discrete values." % (self.title, discrete_values)
            if self not in set(discrete_values):
                raise ValueError(error_msg)
        
        return self

    def validDNS(self):
        kw_args = {
            'must_not_contain': ['[^0-9a-zA-Z/:=_,&~%@#\.\-\?\+\$]+'],
            'contains_either': [
                'https?://',
                '[\w\-]+\.[a-z]{2}'
            ]
        }
        self.validate(**kw_args)
        return True

    def validIP(self):
        # kw_args = {
        #     'contains_either': [
        #         '\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', # ipv4
        #         '[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$' #ipv6
        #     ]
        # }
        # self.validate(**kw_args)
        ip = ip_address(self)
        return True

    def validURL(self):
        try:
            self.validIP()
        except:
            self.validDNS()
        return True

    def stripHTML(self):

        '''
            a method for removing html elements from the string

            (re.S creates DOTALL flag to make . = ANY character at all)
        :return: string
        '''

        html_pattern1 = re.compile('<!--.+?-->', re.S) # html comments
        html_pattern2 = re.compile('<[^>]+?>') # html selectors
        html_pattern3 = re.compile('&.+?;') # non-ascii characters
        stripA = html_pattern1.sub('', self)
        stripB = html_pattern2.sub('', stripA)
        stripC = html_pattern3.sub('', stripB)

        return labString(stripC)

    def stripScripts(self):

        '''
            a method for removing script and style elements from the string

            (re.S creates DOTALL flag to make . = ANY character at all)
        :return: string
        '''

        script_pattern1 = re.compile('<script.+?</script>', re.S) # html scripts
        script_pattern2 = re.compile('<style>.+?</style>', re.S) # html styles
        stripA = script_pattern1.sub('', self)
        stripB = script_pattern2.sub('', stripA)

        return labString(stripB)

    def stripEscapes(self):

        '''
            a method for removing escape elements from the string

            (re.S creates DOTALL flag to make . = ANY character at all)
        :return: string
        '''

        escape_pattern1 = re.compile(r'\\n') # new line
        escape_pattern2 = re.compile(r'\\t') # tab
        escape_pattern3 = re.compile(r'\\') # escape character
        stripA = escape_pattern1.sub('', self)
        stripB = escape_pattern2.sub('', stripA)
        stripC = escape_pattern3.sub('', stripB)

        return labString(stripC)

    def extractByFind(self, prefix, suffix):

        '''
            method for finding a single segment using a distinct prefix & suffix
        :param prefix: substring of string input before desired segment
        :param suffix: substring of string input after desired segment
        :return: string segment (or '' if none exists)
        '''

    # validate inputs
        self.argument(prefix, 'prefix argument for %s.extractByFind()' % self.__class__.__name__)
        self.argument(suffix, 'suffix argument for %s.extractByFind()' % self.__class__.__name__)

    # find segment
        start = self.find(prefix) + len(prefix)
        stop = self.rfind(suffix)
        if start and stop:
            return self[start:stop]
        else:
            return ''

    def extractByRegex(self, pattern, prefix=None, suffix=None):

        '''
            method for finding one or more segments using a regex pattern
        :param pattern: string with Regex syntax
        :param prefix: string with Regex syntax
        :param suffix: string with Regex syntax
        :return: list with string segments matching pattern
        '''

    # validate inputs
        self.argument(pattern, 'pattern argument for %s.extractByRegex()' % self.__class__.__name__)

    # construct segment
        prefix_test = False
        suffix_test = False
        segment = deepcopy(pattern)
        if prefix:
            self.argument(pattern, 'prefix argument for %s.extractByRegex()' % self.__class__.__name__)
            segment = prefix + segment
            prefix_test = True
            if '\\' in prefix:
                prefix = prefix.replace('\\\\','\\')
        if suffix:
            self.argument(pattern, 'suffix argument for %s.extractByRegex()' % self.__class__.__name__)
            segment = segment + suffix
            suffix_test = True
            if '\\' in suffix:
                suffix = suffix.replace('\\\\','\\')

    # compile regex and search string
        segment_pattern = re.compile(segment)
        results = segment_pattern.findall(self)
        segment_list = []
        if results:
            for i in range(0, len(results)):
                if prefix_test:
                    start = results[i].find(prefix) + len(prefix)
                else:
                    start = 0
                if suffix_test:
                    stop = results[i].rfind(suffix)
                else:
                    stop = len(results[i])
                segment_list.append(results[i][start:stop])
        return segment_list

    def unitTests(self):
        test1 = labString('http:\/\/www.meetup.com\/insidestartupsclub\/events\/221604732\/')
        test2 = labString('<p>Drinks with <b><a href=\"http:\/\/uncubed.com\/\">Uncubed<\/a><\/b>.<\/p>')
        noEscapes = '<p>Drinks with <b><a href="http://uncubed.com/">Uncubed</a></b>.</p>'
        assert test1.extractByFind('events\/', '\/') == '221604732'
        assert test1.extractByRegex('\d+', 'events\\\\/', '\\\\/')[0] == '221604732'
        assert test1.extractByRegex('\d+', 'events\\\\/')[0] == '221604732'
        assert test1.extractByRegex('\d+', suffix='\\\\/')[0] == '221604732'
        assert test1.extractByRegex('\d+')[0] == '221604732'
        assert test1.extractByRegex('[A-Z]+') == []
        assert test1.extractByRegex('\d+', 'A') == []
        assert test1.extractByRegex('[a-zA-Z0-9.:]+')[4] == '221604732'
        assert test2.stripHTML() == 'Drinks with Uncubed.'
        assert test2.stripEscapes() == noEscapes
        assert test1.stripEscapes().validDNS()
        assert labString('me.ca').validDNS()
        assert labString('192.168.99.100').validIP()
        test_list = [ 'validIP' ]
        test3 = labString('192.168.99.100')
        assert test3.__getattribute__(test_list[0])()
        return self

labValid.unitTests()
test = labString('hi').rename('mom')
test.unitTests()
print(test.title)
text = b64decode('ZGF0LnRvL2hleQ==')
print(text)
testModel = { 'schema': { 'hi': 'mom' } }
testInput = { 'hi': 'dad' }
from jsonmodel.validators import jsonModel
jsonModel(testModel).validate(testInput)
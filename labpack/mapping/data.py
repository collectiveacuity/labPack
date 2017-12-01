__author__ = 'rcj1492'
__created__ = '2017.12'
__license__ = 'MIT'

def walk_data(input_data):

    ''' a generator function for retrieving data in a nested dictionary

    :param input_data: dictionary or list with nested data
    :return: string with dot_path, object with value of endpoint
    '''

    def _walk_dict(input_dict, path_to_root):
        if not path_to_root:
            yield '.', input_dict
        for key, value in input_dict.items():
            key_path = '%s.%s' % (path_to_root, key)
            type_name = value.__class__.__name__
            yield key_path, value
            if type_name == 'dict':
                for dot_path, value in _walk_dict(value, key_path):
                    yield dot_path, value
            elif type_name == 'list':
                for dot_path, value in _walk_list(value, key_path):
                    yield dot_path, value

    def _walk_list(input_list, path_to_root):
        for i in range(len(input_list)):
            item_path = '%s[%s]' % (path_to_root, i)
            type_name = input_list[i].__class__.__name__
            yield item_path, input_list[i]
            if type_name == 'dict':
                for dot_path, value in _walk_dict(input_list[i], item_path):
                    yield dot_path, value
            elif type_name == 'list':
                for dot_path, value in _walk_list(input_list[i], item_path):
                    yield dot_path, value

    if isinstance(input_data, dict):
        for dot_path, value in _walk_dict(input_data, ''):
            yield dot_path, value
    elif isinstance(input_data, list):
        for dot_path, value in _walk_list(input_data, ''):
            yield dot_path, value
    else:
        raise ValueError('walk_data() input_data argument must be a list or dictionary.')

def segment_path(dot_path):

    '''  a function to separate the path segments in a dot_path key

    :param dot_path: string with dot path syntax
    :return: list of string segments of path
    '''

    import re
    digit_pat = re.compile('\[(\d+)\]')
    key_list = dot_path.split('.')
    segment_list = []
    for key in key_list:
        if key:
            item_list = digit_pat.split(key)
            for item in item_list:
                if item:
                    segment_list.append(item)

    return segment_list

def transform_data(function, input_data):

    ''' a function to apply a function to each value in a nested dictionary

    :param function: callable function with a single input of any datatype
    :param input_data: dictionary or list with nested data to transform
    :return: dictionary or list with data transformed by function
    '''

# construct copy
    try:
        from copy import deepcopy
        output_data = deepcopy(input_data)
    except:
        raise ValueError('transform_data() input_data argument cannot contain module datatypes.')

# walk over data and apply function
    for dot_path, value in walk_data(input_data):
        current_endpoint = output_data
        segment_list = segment_path(dot_path)
        segment = None
        if segment_list:
            for i in range(len(segment_list)):
                try:
                    segment = int(segment_list[i])
                except:
                    segment = segment_list[i]
                if i + 1 == len(segment_list):
                    pass
                else:
                    current_endpoint = current_endpoint[segment]
            current_endpoint[segment] = function(value)

    return output_data

def clean_data(input_value):

    ''' a function to transform a value into a json or yaml valid datatype

    :param input_value: object of any datatype
    :return: object with json valid datatype
    '''

# pass normal json/yaml datatypes
    if input_value.__class__.__name__ in ['bool', 'str', 'float', 'list', 'dict', 'int', 'NoneType']:
        pass

# transform byte data to base64 encoded string
    elif isinstance(input_value, bytes):
        from base64 import b64encode
        input_value = b64encode(input_value).decode()

# convert tuples and sets into lists
    elif isinstance(input_value, tuple) or isinstance(input_value, set):
        new_list = []
        new_list.extend(input_value)
        input_value = transform_data(clean_data, new_list)
    else:
        input_value = str(input_value)

    return input_value

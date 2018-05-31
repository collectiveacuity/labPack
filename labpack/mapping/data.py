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
    if input_value.__class__.__name__ in ['bool', 'str', 'float', 'int', 'NoneType']:
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

# recurse through dictionaries and lists
    elif isinstance(input_value, dict) or isinstance(input_value, list):
        input_value = transform_data(clean_data, input_value)

# convert to string all python objects and callables
    else:
        input_value = str(input_value)

    return input_value

def reconstruct_dict(dot_paths, values):
    
    ''' a method for reconstructing a dictionary from the values along dot paths '''
    
    output_dict = {}
    
    for i in range(len(dot_paths)):
        if i + 1 <= len(values):
            path_segments = segment_path(dot_paths[i])
            current_nest = output_dict
            for j in range(len(path_segments)):
                key_name = path_segments[j]
                try:
                    key_name = int(key_name)
                except:
                    pass
                if j + 1 == len(path_segments):
                    if isinstance(key_name, int):
                        current_nest.append(values[i])
                    else:
                        current_nest[key_name] = values[i]
                else:
                    next_key = path_segments[j+1]
                    try:
                        next_key = int(next_key)
                    except:
                        pass
                    if isinstance(next_key, int):
                        if not key_name in current_nest.keys():
                            current_nest[key_name] = []
                        current_nest = current_nest[key_name]
                    else:
                        if isinstance(key_name, int):
                            current_nest.append({})
                            current_nest = current_nest[len(current_nest) - 1]
                        else:
                            if not key_name in current_nest.keys():
                                current_nest[key_name] = {}
                            current_nest = current_nest[key_name]
    
    return output_dict

if __name__ == '__main__':

# test walk_data
    from collections import OrderedDict
    recursive_paths = []
    recursive_values = []
    test_dict = {
        'you': {
            'me': {
                'us': 'them'
            }
        },
        'him': [ { 'her': { 'their': 'our' } } ],
        'here': [ { 'there': [ 'everywhere' ] } ]
    }
    ordered_dict = OrderedDict(test_dict)
    for dot_path, value in walk_data(ordered_dict):
        recursive_paths.append(dot_path)
        recursive_values.append(value)

# test segment_paths and reconstruct_dict
    dot_paths = []
    values = []
    for number in (3,7,11):
        dot_paths.append(recursive_paths[number])
        values.append(recursive_values[number])

    rebuilt_dict = reconstruct_dict(dot_paths, values)
    assert rebuilt_dict == test_dict
''' a package of functions to convert data architecture formats '''
__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

def _to_camelcase(input_string):
    ''' a helper method to convert python to camelcase'''
    camel_string = ''
    for i in range(len(input_string)):
        if input_string[i] == '_':
            pass
        elif not camel_string:
            camel_string += input_string[i].upper()
        elif input_string[i-1] == '_':
            camel_string += input_string[i].upper()
        else:
            camel_string += input_string[i]
    return camel_string

def _to_python(input_string):
    ''' a helper method to convert camelcase to python'''
    python_string = ''
    for i in range(len(input_string)):
        if not python_string:
            python_string += input_string[i].lower()
        elif input_string[i].isupper():
            python_string += '_%s' % input_string[i].lower()
        else:
            python_string += input_string[i]
    return python_string
        
def _ingest_list(input_list, dict_func, output_list=None):
    
    if not output_list:
        output_list = []
        output_model = None
    else:
        from copy import deepcopy
        output_model = deepcopy(output_list[0])
        output_list = []
    for i in range(len(input_list)):
        if isinstance(input_list[i], dict):
            if not isinstance(output_model, dict):
                output_model = {}
            output_list.append(dict_func(input_list[i], output_model))
        elif isinstance(input_list[i], list):
            if not isinstance(output_model, list):
                output_model = []
            output_list.append(_ingest_list(input_list[i], dict_func, output_model))
        else:
            output_list.append(input_list[i])
            
    return output_list

def _to_python_dict(camelcase_dict, python_dict=None):
    
    if not python_dict:
        python_dict = {}
    for key, value in python_dict.items():
        camel_key = _to_camelcase(key)
        if camel_key in camelcase_dict.keys():
            if value.__class__ == camelcase_dict[camel_key].__class__:
                if isinstance(python_dict[key], dict):
                    python_dict[key] = _to_python_dict(camelcase_dict[camel_key], python_dict[key])
                elif isinstance(python_dict[key], list):
                    python_dict[key] = _ingest_list(camelcase_dict[camel_key], _to_python_dict, python_dict[key])
                else:
                    python_dict[key] = camelcase_dict[camel_key]
    for key, value in camelcase_dict.items():
        python_key = _to_python(key)
        if isinstance(camelcase_dict[key], dict):
            python_dict[python_key] = _to_python_dict(camelcase_dict[key])
        elif isinstance(camelcase_dict[key], list):
            python_dict[python_key] = _ingest_list(camelcase_dict[key], _to_python_dict)
        else:
            python_dict[python_key] = camelcase_dict[key]
    
    return python_dict

def _to_camelcase_dict(python_dict, camelcase_dict=None):
    
    if not camelcase_dict:
        camelcase_dict = {}
    for key, value in camelcase_dict.items():
        python_key = _to_python(key)
        if python_key in python_dict.keys():
            if value.__class__ == python_dict[python_key].__class__:
                if isinstance(camelcase_dict[key], dict):
                    camelcase_dict[key] = _to_camelcase_dict(python_dict[python_key], camelcase_dict[key])
                elif isinstance(camelcase_dict[key], list):
                    camelcase_dict[key] = _ingest_list(python_dict[python_key], _to_camelcase_dict, camelcase_dict[key])
                else:
                    camelcase_dict[key] = python_dict[python_key]
    for key, value in python_dict.items():
        camel_key = _to_camelcase(key)
        if isinstance(python_dict[key], dict):
            camelcase_dict[camel_key] = _to_camelcase_dict(python_dict[key])
        elif isinstance(python_dict[key], list):
            camelcase_dict[camel_key] = _ingest_list(python_dict[key], _to_camelcase_dict)
        else:
            camelcase_dict[camel_key] = python_dict[key]
    
    return camelcase_dict

def camelcase_to_lowercase(camelcase_input, python_input=None):
    
    '''
        a function to recursively convert data with camelcase key names into lowercase keys 
        
    :param camelcase_input: list or dictionary with camelcase keys 
    :param python_input: [optional] list or dictionary with default lowercase keys in output
    :return: dictionary with lowercase key names
    '''
    
    if python_input:
        if camelcase_input.__class__ != python_input.__class__:
            raise ValueError('python_input type %s does not match camelcase_input type %s' % (python_input.__class__, camelcase_input.__class__))
    if isinstance(camelcase_input, dict):
        return _to_python_dict(camelcase_input, python_input)
    elif isinstance(camelcase_input, list):
        return _ingest_list(camelcase_input, _to_python_dict, python_input)
    else:
        return camelcase_input

def lowercase_to_camelcase(python_input, camelcase_input=None):
    
    '''
        a function to recursively convert data with lowercase key names into camelcase keys 
        
    :param camelcase_input: list or dictionary with lowercase keys 
    :param python_input: [optional] list or dictionary with default camelcase keys in output
    :return: dictionary with camelcase key names
    '''
    
    if camelcase_input:
        if python_input.__class__ != camelcase_input.__class__:
            raise ValueError('camelcase_input type %s does not match python_input type %s' % (camelcase_input.__class__, python_input.__class__))
    if isinstance(python_input, dict):
        return _to_camelcase_dict(python_input, camelcase_input)
    elif isinstance(python_input, list):
        return _ingest_list(python_input, _to_camelcase_dict, camelcase_input)
    else:
        return python_input

if __name__ == '__main__':
    
    test_dict = { 'MyAddress': { 'StreetLines': [ { 'StreetNumber': 0, 'StreetName': 'Circle Drive' }], 'ZipCode': '10001', 'Country': { 'CountryName': 'Inversionland', 'CountryCode': 906 }}}
    from pprint import pprint
    test_output1 = camelcase_to_lowercase(test_dict)
    test_primer1 = { 'my_address': { 'zip_code': '' } }
    test_output2 = camelcase_to_lowercase(test_dict, test_primer1)
    assert test_output1 == test_output2
    test_output3 = lowercase_to_camelcase(test_output2)
    test_primer2 = lowercase_to_camelcase(test_primer1)
    test_output4 = lowercase_to_camelcase(test_output2, test_primer2)
    assert test_output3 == test_output4
    assert test_output4 == test_dict
    
    
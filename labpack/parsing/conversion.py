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
        
def _ingest_list(camelcase_list, python_list=None):
    
    if not python_list:
        python_list = []
        python_model = None
    else:
        from copy import deepcopy
        python_model = deepcopy(python_list[0])
        python_list = []
    for i in range(len(camelcase_list)):
        if isinstance(camelcase_list[i], dict):
            if not isinstance(python_model, dict):
                python_model = {}
            python_list.append(_ingest_dict(camelcase_list[i], python_model))
        elif isinstance(camelcase_list[i], list):
            if not isinstance(python_model, list):
                python_model = []
            python_list.append(_ingest_list(camelcase_list[i], python_model))
        else:
            python_list.append(camelcase_list[i])
            
    return python_list

def _ingest_dict(camelcase_dict, python_dict=None):
    
    if not python_dict:
        python_dict = {}
    for key, value in python_dict.items():
        camel_key = _to_camelcase(key)
        if camel_key in camelcase_dict.keys():
            if value.__class__ == camelcase_dict[camel_key].__class__:
                if isinstance(python_dict[key], dict):
                    python_dict[key] = _ingest_dict(camelcase_dict[camel_key], python_dict[key])
                elif isinstance(python_dict[key], list):
                    python_dict[key] = _ingest_list(camelcase_dict[camel_key], python_dict[key])
                else:
                    python_dict[key] = camelcase_dict[camel_key]
    for key, value in camelcase_dict.items():
        python_key = _to_python(key)
        if isinstance(camelcase_dict[key], dict):
            python_dict[python_key] = _ingest_dict(camelcase_dict[key])
        elif isinstance(camelcase_dict[key], list):
            python_dict[python_key] = _ingest_list(camelcase_dict[key])
        else:
            python_dict[python_key] = camelcase_dict[key]
    
    return python_dict

def camelcase_to_lowercase(camelcase_input, python_input=None):
    
    if python_input:
        if camelcase_input.__class__ != python_input.__class__:
            raise ValueError('python_input type %s does not match camelcase_input type %s' % (python_input.__class__, camelcase_input.__class__))
    if isinstance(camelcase_input, dict):
        return _ingest_dict(camelcase_input, python_input)
    elif isinstance(camelcase_input, list):
        return _ingest_list(camelcase_input, python_input)
    else:
        return camelcase_input

if __name__ == '__main__':
    
    test_dict = { 'MyAddress': { 'StreetLines': [ { 'StreetNumber': 0, 'StreetName': 'Circle Drive' }], 'ZipCode': '10001', 'Country': { 'CountryName': 'Inversionland', 'CountryCode': 906 }}}
    from pprint import pprint
    pprint(camelcase_to_lowercase(test_dict))
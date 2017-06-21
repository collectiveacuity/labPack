__author__ = 'rcj1492'
__created__ = '2016.09'
__license__ = 'MIT'

class _method_constructor(object):
    ''' a class constructor for sub-method attributes '''
    def __init__(self, method_dict):
        for k, v in method_dict.items():
            setattr(self, k, v)

class _walk_constructor(object):
    ''' a walking class constructor for sub-method attributes '''
    def __init__(self, input_dict):
        for key, value in input_dict.items():
            if isinstance(value, dict):
                setattr(self, key, _walk_constructor(value))
            else:
                setattr(self, key, value)

def retrieve_function(function_string, global_scope=None, root_path='./'):

# determine if function is pickled
    import pickle
    from base64 import b64decode
    try:
        byte_data = b64decode(function_string)
        isinstance(byte_data, bytes) == True
        function_object = pickle.loads(byte_data)
        return function_object
    except:
        pass

# parse function string
    import re
    python_pattern = re.compile('\\.pyc?$')
    function_path = function_string.split(':')
    if len(function_path) > 1:
        function_file = function_path[0]
        if not python_pattern.findall(function_path[0]):
            function_file = '%s.py' % function_path[0]
        function_tokens = function_path[1].split('.')
    else:
        function_file = ''
        function_tokens = function_string.split('.')

# define attribute walk function
    import pkgutil
    from importlib import import_module
    def _walk_attributes(func_obj, func_tokens):
        attr_name = func_tokens.pop(0)
        new_obj = None
        try:
            new_obj = getattr(func_obj, attr_name)
        except AttributeError as err:
            try:
                for loader, name, is_package in pkgutil.walk_packages(func_obj.__path__):
                    if name == attr_name:
                        full_name = func_obj.__name__ + '.' + name
                        new_obj = import_module(full_name)
                        break
            except:
                pass
            if not new_obj:
                raise err
        if func_tokens:
            return _walk_attributes(new_obj, func_tokens)
        return new_obj

# import module from path
    if function_file:
        from os import path
        from importlib.util import spec_from_file_location, module_from_spec
        file_path = path.join(root_path, function_file)
        if not path.exists(file_path):
            raise ValueError('%s is not a valid file path.' % file_path)
        spec_file = spec_from_file_location("file_module", file_path)
        function_object = module_from_spec(spec_file)
        spec_file.loader.exec_module(function_object)

# import module from scope or library
    else:
        from importlib import import_module
        if not global_scope:
            global_scope = {}
        module_name = function_tokens.pop(0)
        if module_name in global_scope.keys():
            function_object = global_scope[module_name]
        else:
            function_object = import_module(module_name)

# walk down attributes to endpoint
    if function_tokens:
        function_object = _walk_attributes(function_object, function_tokens)

    return function_object



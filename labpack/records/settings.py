__author__ = 'rcj1492'
__created__ = '2016.10'
__license__ = 'MIT'

def load_settings(file_path, module_name='', secret_key=''):

    ''' a method to load data from json valid files

    :param file_path: string with path to settings file
    :param module_name: [optional] string with name of module containing file path
    :param secret_key: [optional] string with key to decrypt drep file
    :return: dictionary with settings data
    '''

# validate inputs
    title = 'load_settings'
    try:
        _path_arg = '%s(file_path=%s)' % (title, str(file_path))
    except:
        raise ValueError('%s(file_path=...) must be a string.' % title)

# find relative path from module
    from os import path
    if module_name:
        try:
            _path_arg = _path_arg.replace(')', ', module_name=%s)' % str(module_name))
        except:
            raise ValueError('%s(module_name=...) must be a string.' % title)
        from importlib.util import find_spec
        module_path = find_spec(module_name).submodule_search_locations[0]
        file_path = path.join(module_path, file_path)

# validate existence of file
    if not path.exists(file_path):
        raise ValueError('%s is not a valid file path.' % _path_arg)

# parse extension type
    ext_map = {}
    file_extensions = {
        "json": ".+\\.json$",
        "json.gz": ".+\\.json\\.gz$",
        "yaml": ".+\\.ya?ml$",
        "yaml.gz": ".+\\.ya?ml\\.gz$",
        "drep": ".+\\.drep$"
    }
    import re
    for key, value in file_extensions.items():
        file_pattern = re.compile(value)
        if file_pattern.findall(file_path):
            ext_map[key] = True
        else:
            ext_map[key] = False

# retrieve file details
    if ext_map['json']:
        import json
        try:
            file_data = open(file_path, 'rt')
            file_details = json.loads(file_data.read())
        except:
            raise ValueError('%s is not valid json data.' % _path_arg)
    elif ext_map['yaml']:
        import yaml
        try:
            file_data = open(file_path, 'rt')
            file_details = yaml.load(file_data.read())
        except:
            raise ValueError('%s is not valid yaml data.' % _path_arg)
    elif ext_map['json.gz']:
        import gzip
        import json
        try:
            file_data = gzip.open(file_path, 'rb')
        except:
            raise ValueError('%s is not valid gzip compressed data.' % _path_arg)
        try:
            file_details = json.loads(file_data.read().decode())
        except:
            raise ValueError('%s is not valid json data.' % _path_arg)
    elif ext_map['yaml.gz']:
        import gzip
        import yaml
        try:
            file_data = gzip.open(file_path, 'rb')
        except:
            raise ValueError('%s is not valid gzip compressed data.' % _path_arg)
        try:
            file_details = yaml.load(file_data.read().decode())
        except:
            raise ValueError('%s is not valid yaml data.' % _path_arg)
    elif ext_map['drep']:
        from labpack.compilers import drep
        try:
            file_data = open(file_path, 'rb').read()
            file_details = drep.load(encrypted_data=file_data, secret_key=secret_key)
        except:
            raise ValueError('%s is not valid drep data.' % _path_arg)
    else:
        raise ValueError('%s must be one of %s file types.' % (_path_arg, list(ext_map.keys())))

    return file_details

def save_settings(file_path, record_details, overwrite=False, secret_key=''):

    ''' a method to save dictionary typed data to a local file

    :param file_path: string with path to settings file
    :param record_details: dictionary with record details
    :param overwrite: [optional] boolean to overwrite existing file data
    :param secret_key: [optional] string with key to decrypt drep file
    :return: string with file path
    '''

# validate inputs
    title = 'save_settings'
    try:
        _path_arg = '%s(file_path=%s)' % (title, str(file_path))
    except:
        raise ValueError('%s(file_path=...) must be a string.' % title)
    _details_arg = '%s(record_details={...})' % title
    if not isinstance(record_details, dict):
        raise ValueError('%s must be a dictionary.' % _details_arg)
    if secret_key:
        try:
            _secret_arg = '%s(secret_key=%s)' % (title, str(secret_key))
        except:
            raise ValueError('%s(secret_key=...) must be a string.' % title)

# parse extension type
    ext_map = {}
    file_extensions = {
        "json": ".+\\.json$",
        "json.gz": ".+\\.json\\.gz$",
        "yaml": ".+\\.ya?ml$",
        "yaml.gz": ".+\\.ya?ml\\.gz$",
        "drep": ".+\\.drep$"
    }
    import re
    for key, value in file_extensions.items():
        file_pattern = re.compile(value)
        if file_pattern.findall(file_path):
            ext_map[key] = True
        else:
            ext_map[key] = False

# construct file data
    file_time = 0
    file_data = ''.encode('utf-8')
    if ext_map['json']:
        import json
        file_data = json.dumps(record_details, indent=2).encode('utf-8')
    elif ext_map['yaml']:
        import yaml
        file_data = yaml.dump(record_details).encode('utf-8')
    elif ext_map['json.gz']:
        import json
        import gzip
        file_bytes = json.dumps(record_details).encode('utf-8')
        file_data = gzip.compress(file_bytes)
    elif ext_map['yaml.gz']:
        import yaml
        import gzip
        file_bytes = yaml.dump(record_details).encode('utf-8')
        file_data = gzip.compress(file_bytes)
    elif ext_map['drep']:
        from labpack.compilers import drep
        file_data = drep.dump(record_details, secret_key)
        file_time = 1
    else:
        raise ValueError('%s must be one of %s file types.' % (_path_arg, list(ext_map.keys())))

# check overwrite exception
    import os
    if not overwrite:
        if os.path.exists(file_path):
            raise Exception('%s already exists. To overwrite %s, set overwrite=True' % (_path_arg, _path_arg))

# create directories in path to file
    dir_path = os.path.split(file_path)
    if dir_path[0]:
        if not os.path.exists(dir_path[0]):
            os.makedirs(dir_path[0])

# write data to file
    with open(file_path, 'wb') as f:
        f.write(file_data)
        f.close()

# eliminate update and access time metadata (for drep files)
    if file_time:
        os.utime(file_path, times=(file_time, file_time))

# TODO add windows creation time wiping
# http://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file-from-python

    return file_path

def _remove_settings(_file_path, _retry_count=10, _remove_dir=False):

    '''
        a helper method for removing settings file
        
    :param _file_path: string with path to file to remove 
    :param _retry_count: integer with number of attempts before error is raised
    :param _remove_dir: [optional] boolean to remove empty parent directories
    :return: None
    '''

    import os
    from time import sleep

    count = 0
    while True:
        try:
            os.remove(_file_path)
            if _remove_dir:
                path_segments = os.path.split(_file_path)
                if len(path_segments) > 1:
                    file_folders = path_segments[0]
                    try:
                        os.removedirs(file_folders)
                    except:
                        pass
            break
        except PermissionError:
            sleep(.05)
            count += 1
            if count > _retry_count:
                raise

    os._exit(0)

def remove_settings(file_path, retry_count=10, remove_dir=False):

    '''
        a method to remove a file using a child process

        http://www.petercollingridge.co.uk/blog/running-multiple-processes-python
        https://docs.python.org/3.5/library/multiprocessing.html

    :param file_path: string with path to file to remove
    :param retry_count: integer with number of attempts to remove before error is thrown
    :param remove_dir: [optional] boolean to remove empty parent directories
    :return: None
    '''

# validate inputs
    title = 'remove_settings'
    try:
        _path_arg = '%s(file_path=%s)' % (title, str(file_path))
    except:
        raise ValueError('%s(file_path=...) must be a string.' % title)
    if not isinstance(retry_count, int):
        raise ValueError('%s(retry_count=...) must be an integer.' % title)
    elif retry_count < 1:
        raise ValueError('%s(retry_count=%s) must be greater than 0.' % (title, retry_count))

# create a child process to remove file
    from multiprocessing import Process
    child_process = Process(target=_remove_settings, args=(file_path, retry_count, remove_dir))
    child_process.start()

def ingest_environ(model_path=''):

    ''' a method to convert environment variables to a python dictionary

    :param model_path: [optional] string with path to jsonmodel of data to ingest
    :return: dictionary with environmental variables

    NOTE:   if a model is provided, then only those fields in the model will be
            added to the output and the value of any environment variable which
            matches the uppercase name of each field in the model will be added
            to the dictionary if its value is valid according to the model. if
            a value is not valid, the method will throw a InputValidationError
    '''

# convert environment variables into json typed data
    from os import environ, path
    typed_dict = {}
    environ_variables = dict(environ)
    for key, value in environ_variables.items():
        if value.lower() == 'true':
            typed_dict[key] = True
        elif value.lower() == 'false':
            typed_dict[key] = False
        elif value.lower() == 'null':
            typed_dict[key] = None
        elif value.lower() == 'none':
            typed_dict[key] = None
        else:
            try:
                try:
                    typed_dict[key] = int(value)
                except:
                    typed_dict[key] = float(value)
            except:
                typed_dict[key] = value

# feed environment variables through model
    if model_path:
        if not path.exists(model_path):
            raise ValueError('%s is not a valid file path.' % model_path)
        model_dict = load_settings(model_path)
        from jsonmodel.validators import jsonModel
        model_object = jsonModel(model_dict)
        default_dict = model_object.ingest(**{})
        for key in default_dict.keys():
            if key.upper() in typed_dict:
                valid_kwargs = {
                    'input_data': typed_dict[key.upper()],
                    'object_title': 'Environment variable %s' % key.upper(),
                    'path_to_root': '.%s' % key
                }
                default_dict[key] = model_object.validate(**valid_kwargs)
        return default_dict

    return typed_dict

def compile_settings(model_path, file_path, ignore_errors=False):

    ''' a method to compile configuration values from different sources

        NOTE:   method searches the environment variables, a local
                configuration path and the default values for a jsonmodel
                object for valid configuration values. if an environmental
                variable or key inside a local config file matches the key
                for a configuration setting declared in the jsonmodel schema,
                its value will be added to the configuration file as long
                as the value is model valid. SEE jsonmodel module.

        NOTE:   the order of assignment:
                    first:  environment variable
                    second: configuration file
                    third:  default value
                    fourth: empty value

        NOTE:   method is guaranteed to produce a full set of top-level keys

    :param model_path: string with path to jsonmodel valid model data
    :param file_path: string with path to local configuration file
    :param ignore_errors: [optional] boolean to ignore any invalid values
    :return: dictionary with settings
    '''

# construct configuration model and default details
    from jsonmodel.validators import jsonModel
    config_model = jsonModel(load_settings(model_path))
    default_details = config_model.ingest(**{})

# retrieve environmental variables and file details
    environ_details = ingest_environ()

    try:
        file_details = load_settings(file_path)
    except:
        file_details = {}

# construct config details from (first) envvar, (second) file, (third) default
    config_details = {}
    for key in default_details.keys():
        test_file = True
        test_default = True
        if key.upper() in environ_details.keys():
            test_file = False
            test_default = False
            try:
                config_details[key] = config_model.validate(environ_details[key.upper()], '.%s' % key)
            except:
                if ignore_errors:
                    test_file = True
                    test_default = True
                else:
                    raise
        if key in file_details.keys() and test_file:
            test_default = False
            try:
                config_details[key] = config_model.validate(file_details[key], '.%s' % key)
            except:
                if ignore_errors:
                    test_default = True
                else:
                    raise
        if test_default:
            config_details[key] = default_details[key]

    return config_details

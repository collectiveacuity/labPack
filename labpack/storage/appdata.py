__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
from labpack.platforms.localhost import localhostClient

class appdataClient(object):

    ''' a class of methods for managing file storage in local app data

        NOTE:   class is designed to store json valid data nested in a dictionary
                structure. acceptable data types include:
                    boolean
                    integer or float (number)
                    string
                    dictionary
                    list
                    none
                to store other types of data, try first creating an url safe base64
                string using something like:
                    base64.urlsafe_b64encode(byte_data).decode()
    '''

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'collection_name': 'User Data',
            'key_string': 'obs/terminal/2016-03-17T17-24-51-687845Z.ogg',
            'key_string_dict': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'key_string_path': '/home/user/.config/collective-acuity-labpack/user-data/obs/terminal',
            'key_string_comp': 'obs',
            'previous_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'body_dict': { 'dT': 1458235492.311154 },
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'max_results': 1,
            'path_filters': [ { } ],
            'path_filter': {
                'byte_data': False,
                'discrete_values': [ '' ],
                'excluded_values': [ '' ],
                'greater_than': '',
                'less_than': '',
                'max_length': 0,
                'max_value': '',
                'min_length': 0,
                'min_value': '',
                'must_contain': [ '' ],
                'must_not_contain': [ '' ],
                'contains_either': [ '' ]
            }
        },
        'components': {
            '.org_name': {
                'max_length': 255,
                'must_not_contain': ['/', '^\\.']
            },
            '.prod_name': {
                'max_length': 255,
                'must_not_contain': ['/', '^\\.']
            },
            '.collection_name': {
                'max_length': 255,
                'must_not_contain': ['/', '^\\.']
            },
            '.key_string': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            },
            '.key_string_dict': {
                'contains_either': [ '\\.json$', '\\.ya?ml$', '\\.json\\.gz$', '\\.ya?ml\\.gz$', '\\.drep$' ]
            },
            '.key_string_path': {
                'max_length': 32767
            },
            '.key_string_comp': {
                'max_length': 255
            },
            '.body_dict': {
                'extra_fields': True
            },
            '.body_dict.dT': {
                'required_field': False
            },
            '.secret_key': {
                'must_not_contain': [ '[\\s\\t\\n\\r]' ]
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            },
            '.path_filter.discrete_values': {
                'required_field': False
            },
            '.path_filter.excluded_values': {
                'required_field': False
            },
            '.path_filter.must_contain': {
                'required_field': False
            },
            '.path_filter.must_not_contain': {
                'required_field': False
            },
            '.path_filter.contains_either': {
                'required_field': False
            }
        }
    }

    def __init__(self, collection_name='', prod_name='', org_name=''):

        ''' initialization method of appdata client class

        :param collection_name: [optional] string with name of collection to store records
        :param prod_name: [optional] string with name of application product
        :param org_name: [optional] string with name of organization behind product
        '''

    # add localhost property to class
        self.localhost = localhostClient()

    # construct input validation model
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        if not collection_name:
            collection_name = 'User Data'
        else:
            collection_name = self.fields.validate(collection_name, '.collection_name')
        if not org_name:
            org_name = __team__
        else:
            org_name = self.localhost.fields.validate(org_name, '.org_name')
        if not prod_name:
            prod_name = __module__
        else:
            prod_name = self.localhost.fields.validate(prod_name, '.prod_name')

    # validate existence of file data folder in app data (or create)
        self.app_folder = self.localhost.app_data(org_name=org_name, prod_name=prod_name)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            collection_name = collection_name.replace(' ', '-').lower()
        self.collection_folder = os.path.join(self.app_folder, collection_name)
        self.fields.validate(self.collection_folder, '.key_string_path')
        if not os.path.exists(self.collection_folder):
            os.makedirs(self.collection_folder)

    def _delete(self, _file_path, _key_arg, _key_string):

        '''
            a helper method for non-blocking deletion of files
            
        :param _file_path: string with path to file to remove  
        :return: None
        '''

        import os
        from time import sleep

        current_dir = os.path.split(_file_path)[0]
        count = 0
        retry_count = 10
        while True:
            try:
                os.remove(_file_path)
                while current_dir != self.collection_folder:
                    if not os.listdir(current_dir):
                        os.rmdir(current_dir)
                        current_dir = os.path.split(current_dir)[0]
                    else:
                        break
                break
            except PermissionError:
                sleep(.05)
                count += 1
                if count > retry_count:
                    raise Exception('%s failed to delete %s' % (_key_arg, _key_string))

        os._exit(0)

    def create(self, key_string, body_dict=None, byte_data=None, overwrite=True, secret_key=''):

        ''' a method to create a file in the collection folder

        :param key_string: string with name to assign file (see NOTE below)
        :param body_dict: dictionary with file body details
        :param byte_data: byte data to save under key string
        :param overwrite: boolean to overwrite files with same name
        :param secret_key: [optional] string with key to encrypt body data
        :return: self

            NOTE:   key_string may only contain alphanumeric, /, _, . or -
                    characters and may not begin with the . or / character.
            
            NOTE:   body_dict and byte_data arguments cannot both be empty
                    if creating a record with dictionary data, then the
                    key_string must end with one of the following acceptable 
                    file extensions:
                        .json
                        .yaml
                        .yml
                        .json.gz
                        .yaml.gz
                        .yml.gz
                        .drep
                    if creating a record with byte data, then neither the
                    key_string file extension nor the byte data will be
                    validated. it is up to the saving method to ensure that
                    mimetype of the data is correct.

            NOTE:   using one or more / characters splits the key into
                    separate segments. these segments will appear as a
                    sub directories inside the record collection and each
                    segment is used as a separate index for that record
                    when using the list method
                    eg. lab/unittests/1473719695.2165067.json is indexed:
                    [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
        '''

        _title = '%s.create' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (_title, key_string)
        _body_arg = '%s(body_dict={...}' % {_title}
        _secret_arg = '%s(secret_key="%s")' % (_title, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string', _key_arg)
        if body_dict:
            key_string = self.fields.validate(key_string, '.key_string_dict', _key_arg)
            body_dict = self.fields.validate(body_dict, '.body_dict', _body_arg)
        elif byte_data:
            pass
        else:
            raise IndexError('%s must contain either a body_dict or byte_data argument' % _title)

    # construct and validate file path
        file_path = os.path.join(self.collection_folder, key_string)
        file_path = self.fields.validate(file_path, '.key_string_path')
        current_path = os.path.split(file_path)
        self.fields.validate(current_path[1], '.key_string_comp')
        while current_path[0] != self.collection_folder:
            current_path = os.path.split(current_path[0])
            self.fields.validate(current_path[1], '.key_string_comp')

    # save dictionary data
        if body_dict:
            from labpack.records.settings import save_settings
            save_kwargs = {
                'file_path': file_path,
                'record_details': body_dict,
                'overwrite': overwrite,
                'secret_key': secret_key
            }
            save_settings(**save_kwargs)

    # save byte data
        elif byte_data:
            if not overwrite:
                if os.path.exists(file_path):
                    raise Exception('%s already exists. To overwrite %s, set overwrite=True' % (key_string, key_string))
            dir_path = os.path.split(file_path)
            if dir_path[0]:
                if not os.path.exists(dir_path[0]):
                    os.makedirs(dir_path[0])
            if secret_key:
                from labpack.encryption import cryptolab
                byte_data, secret_key = cryptolab.encrypt(byte_data, secret_key)
            with open(file_path, 'wb') as f:
                f.write(byte_data)
                f.close()

        return key_string

    def read(self, key_string, secret_key=''):

        ''' a method to retrieve body details from a file

        :param key_string: string with name of file
        :param secret_key: [optional] string used to decrypt data
        :return: dictionary with file content details or byte data
        '''

        _title = '%s.read' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (_title, key_string)
        _secret_arg = '%s(secret_key="%s")' % (_title, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string', _key_arg)

    # construct path to file
        file_path = os.path.join(self.collection_folder, key_string)

    # validate existence of file
        if not os.path.exists(file_path):
            raise Exception('%s does not exist.' % _key_arg)

    # parse extension
        record_data = False
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
                record_data = True
                break
        
    # retrieve file details from record data
        if record_data:
            from labpack.records.settings import load_settings
            load_kwargs = {
                'file_path': file_path,
                'secret_key': secret_key
            }
            file_details = load_settings(**load_kwargs)
    
            return file_details
    
    # retrieve byte data from other files
        else:
            byte_data = open(file_path, 'rb').read()
            if secret_key:
                from labpack.encryption import cryptolab
                byte_data = cryptolab.decrypt(byte_data, secret_key)
            
            return byte_data
            
    def conditional_filter(self, path_filters):

        ''' a method to construct a conditional filter function for class list method

        :param path_filters: list with query criteria dictionaries
        :return: filter_function object

            NOTE:   query criteria architecture

                    each item in the path filters argument must be a dictionary
                    which is composed of integer-value key names that represent the
                    index value of the file path segment to test and key values
                    with the dictionary of conditional operators used to test the
                    string value in the indexed field of the record.

                    eg. path_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]

                    this example filter looks at the first segment of each key string
                    in the collection for a string value which starts with the
                    characters 'lab'. as a result, it will match both the following:
                        lab/unittests/1473719695.2165067.json
                        'laboratory20160912.json'

            NOTE:   the filter method uses a query filters list structure to represent
                    the disjunctive normal form of a logical expression. a record is
                    added to the results list if any query criteria dictionary in the
                    list evaluates to true. within each query criteria dictionary, all
                    declared conditional operators must evaluate to true.

                    in this way, the path_filters represents a boolean OR operator and
                    each criteria dictionary inside the list represents a boolean AND
                    operator between all keys in the dictionary.

                    each query criteria uses the architecture of query declaration in
                    the jsonModel.query method

            path_filters:
            [ { 0: { conditional operators }, 1: { conditional_operators }, ... } ]

            conditional operators:
                "byte_data": false,
                "discrete_values": [ "" ],
                "excluded_values": [ "" ],
                "greater_than": "",
                "less_than": "",
                "max_length": 0,
                "max_value": "",
                "min_length": 0,
                "min_value": "",
                "must_contain": [ "" ],
                "must_not_contain": [ "" ],
                "contains_either": [ "" ]
        '''

        _title = '%s.filter' % self.__class__.__name__
        _filter_arg = '%s(path_filters=[...])' % _title

    # validate input
        if not isinstance(path_filters, list):
            raise TypeError('%s key value must be a list.' % _filter_arg)
        for i in range(len(path_filters)):
            if not isinstance(path_filters[i], dict):
                raise TypeError('%s item %s must be a dictionary.' % (_filter_arg, i))
            for key, value in path_filters[i].items():
                _key_name = '%s : {...}' % key
                if not isinstance(key, int):
                    raise TypeError('%s key name must be an int.' % _filter_arg.replace('...', _key_name))
                elif not isinstance(value, dict):
                    raise TypeError('%s key value must be a dictionary' % _filter_arg.replace('...', _key_name))
                self.fields.validate(value, '.path_filter')

    # construct segment value model
        segment_schema = { 'schema': { 'segment_value': 'string' } }
        segment_model = jsonModel(segment_schema)

    # construct filter function
        def filter_function(*args):
            max_index = len(args) - 1
            for filter in path_filters:
                criteria_match = True
                for key, value in filter.items():
                    if key > max_index:
                        criteria_match = False
                        break
                    segment_criteria = { '.segment_value': value }
                    segment_data = { 'segment_value': args[key] }
                    if not segment_model.query(segment_criteria, segment_data):
                        criteria_match = False
                        break
                if criteria_match:
                    return True
            return False

        return filter_function

    def list(self, filter_function=None, max_results=1, reverse_search=True, previous_key=''):

        ''' a method to list keys in the collection

        :param filter_function: (positional arguments) function used to filter results
        :param max_results: integer with maximum number of results to return
        :param reverse_search: boolean to search keys in reverse alphanumeric order
        :param previous_key: string with key in collection to begin search after
        :return: list of key strings

            NOTE:   each key string can be divided into one or more segments
                    based upon the / characters which occur in the key string as
                    well as its file extension type. if the key string represents
                    a file path, then each directory in the path, the file name
                    and the file extension are all separate indexed values.

                    eg. lab/unittests/1473719695.2165067.json is indexed:
                    [ 'lab', 'unittests', '1473719695.2165067', '.json' ]

                    it is possible to filter the records in the collection according
                    to one or more of these path segments using a filter_function.

            NOTE:   the filter_function must be able to accept an array of positional
                    arguments and return a value that can evaluate to true or false.
                    while searching the records, list produces an array of strings
                    which represent the directory structure in relative path of each
                    key string. if a filter_function is provided, this list of strings
                    is fed to the filter function. if the function evaluates this input
                    and returns a true value the file will be included in the list
                    results.
        '''

        _title = '%s.list(...)' % self.__class__.__name__

    # validate input
        input_kwargs = [max_results, previous_key]
        input_names = ['.max_results', '.key_string']
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # validate filter function
        if filter_function:
            try:
                path_segments = [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
                filter_function(*path_segments)
            except:
                err_msg = _title.replace('...', 'filter_function=%s' % filter_function.__class__.__name__)
                raise TypeError('%s must accept positional arguments.' % err_msg)

    # construct empty results list
        results_list = []
        root_segments = self.collection_folder.split(os.sep)
        if previous_key:
            previous_key = os.path.join(self.collection_folder, previous_key)

    # walk collection folder to find files
        for file_path in self.localhost.walk(self.collection_folder, reverse_search, previous_key):
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            key_string = os.path.join(*path_segments)
            key_string = key_string.replace('\\','/')

    # apply filtering criteria
            if filter_function:
                if filter_function(*path_segments):
                    results_list.append(key_string)
            else:
                results_list.append(key_string)

    # return results list
            if len(results_list) == max_results:
                return results_list

        return results_list

    def delete(self, key_string):

        ''' a method to delete a file

        :param key_string: string with name of file
        :return: string reporting outcome
        '''

        _title = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (_title, key_string)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string')

    # construct path to file
        file_path = os.path.join(self.collection_folder, key_string)

    # validate existence of file
        if not os.path.exists(file_path):
            return '%s does not exist.' % key_string
        current_dir = os.path.split(file_path)[0]

    # remove file
        try:
            os.remove(file_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, key_string))

    # # remove empty directories in path to file
    #     if not os.listdir(current_dir):
    #         os.removedirs(current_dir)

    # remove empty directories in path to file
        while current_dir != self.collection_folder:
            if not os.listdir(current_dir):
                os.rmdir(current_dir)
                current_dir = os.path.split(current_dir)[0]
            else:
                break

        return '%s has been deleted.' % key_string

    def remove(self):

        ''' a method to remove collection and all records in the collection

        :return: string with confirmation of deletion
        '''

        _title = '%s.remove' % self.__class__.__name__

    # TODO  error handling is turned off to avoid system blocking
    #       fix potential to create artifacts in the system

    # remove collection tree
        try:
            import shutil
            shutil.rmtree(self.collection_folder, ignore_errors=True)
        except:
            raise Exception('%s failed to remove %s collection from app data.' % (_title, self.collection_folder))

        return '%s collection has been removed from app data.' % self.collection_folder

if __name__ == '__main__':
    appdataClient()
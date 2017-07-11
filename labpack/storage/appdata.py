__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
from labpack.platforms.localhost import localhostClient

class appdataClient(object):

    ''' a class of methods for managing file storage on local device in app data 

        NOTE:   class is designed to store json valid data. acceptable data types 
                inside the record body include:
                    boolean
                    integer or float (number)
                    string
                    dictionary
                    list
                    none
                to store other types of data, try first creating an url safe base64
                string using something like:
                    base64.urlsafe_b64encode(byte_data).decode()
                otherwise, you can store the entire body as a byte blob and handle the
                data type architecture manually
    '''

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'collection_name': 'User Data',
            'record_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.ogg',
            'record_key_dict': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'record_key_path': '/home/user/.config/collective-acuity-labpack/user-data/obs/terminal',
            'record_key_comp': 'obs',
            'previous_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'record_body': { 'dT': 1458235492.311154 },
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
            '.record_key': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            },
            '.record_key_dict': {
                'contains_either': [ '\\.json$', '\\.ya?ml$', '\\.json\\.gz$', '\\.ya?ml\\.gz$', '\\.drep$' ]
            },
            '.record_key_path': {
                'max_length': 32767
            },
            '.record_key_comp': {
                'max_length': 255
            },
            '.record_body': {
                'extra_fields': True
            },
            '.record_body.dT': {
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
        self.fields.validate(self.collection_folder, '.record_key_path')
        if not os.path.exists(self.collection_folder):
            os.makedirs(self.collection_folder)

    def _delete(self, _file_path, _key_arg, _record_key):

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
                    raise Exception('%s failed to delete %s' % (_key_arg, _record_key))

        os._exit(0)

    def _import(self, _record_key, _byte_data, _overwrite=True):
        
        '''
            a helper method for other storage clients to import into appdata
        :param _record_key: string with key for record
        :param _byte_data: byte data for body of record
        :param _overwrite: [optional] boolean to overwrite existing records
        :return: True
        '''
        
    # construct and validate file path
        file_path = os.path.join(self.collection_folder, _record_key)

    # check overwrite exception
        from os import path, makedirs
        if not _overwrite:
            if path.exists(file_path):
                return False

    # create directories in path to file
        file_root, file_name = path.split(file_path)
        if file_root:
            if not path.exists(file_root):
                makedirs(file_root)
                
    # save file
        with open(file_path, 'wb') as f:
            f.write(_byte_data)
            f.close()
    
    # erase file date from drep files
        import re
        if re.search('\\.drep$', file_name):
            from os import utime
            file_time = 1
            utime(file_path, times=(file_time, file_time))
        
        return True
        
    def create(self, record_key, record_body=None, overwrite=True, secret_key=''):

        ''' a method to create a file in the collection folder

        :param record_key: string with name to assign file (see NOTE below)
        :param record_body: object with file body details (see NOTE below)
        :param overwrite: [optional] boolean to overwrite files with same name
        :param secret_key: [optional] string with key to encrypt body data
        :return: self

        NOTE:   record_key may only contain alphanumeric, /, _, . or -
                characters and may not begin with the . or / character.
        
        NOTE:   record_body datatype is inferred from the record_key extension
                name. if the record_key ends with one of the following file 
                extensions then the record_body can be any json valid object:
                    .json
                    .yaml
                    .yml
                    .json.gz
                    .yaml.gz
                    .yml.gz
                    .drep
                the body of record_key values with .txt or .md extension are
                interpreted as string data types. any other file extension is
                treated as a byte data type. it is up to the saving method to 
                ensure that the mimetype of byte data is correct.

        NOTE:   using one or more / characters splits the key into
                separate segments. these segments will appear as a
                sub directories inside the record collection and each
                segment is used as a separate index for that record
                when using the list method
                eg. lab/unittests/1473719695.2165067.json is indexed:
                [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
        '''

        _title = '%s.create' % self.__class__.__name__
        _key_arg = '%s(record_key="%s")' % (_title, record_key)
        _body_arg = '%s(record_body={...}' % {_title}
        _secret_arg = '%s(secret_key="%s")' % (_title, secret_key)

    # validate inputs
        record_key = self.fields.validate(record_key, '.record_key', _key_arg)

    # construct and validate file path
        file_path = os.path.join(self.collection_folder, record_key)
        file_path = self.fields.validate(file_path, '.record_key_path')
        file_root, file_name = os.path.split(file_path)
        self.fields.validate(file_name, '.record_key_comp')
        while file_root != self.collection_folder:
            file_root, path_node = os.path.split(file_root)
            self.fields.validate(path_node, '.record_key_comp')

    # # check overwrite exception
        from os import path, makedirs
        if not overwrite:
            if path.exists(file_path):
                raise Exception('%s already exists. To overwrite %s, set overwrite=True' % (_key_arg, _key_arg))

    # create directories in path to file
        file_root, file_node = path.split(file_path)
        if file_root:
            if not path.exists(file_root):
                makedirs(file_root)
            
    # encode data
        from labpack.compilers.encoding import encode_data
        byte_data = encode_data(file_name, record_body, secret_key=secret_key)
    
    # save file
        with open(file_path, 'wb') as f:
            f.write(byte_data)
            f.close()
    
    # erase file date from drep files
        import re
        if re.search('\\.drep$', file_name):
            from os import utime
            file_time = 1
            utime(file_path, times=(file_time, file_time))

        return record_key

    def read(self, record_key, secret_key=''):

        ''' a method to retrieve body details from a file

        :param record_key: string with name of file
        :param secret_key: [optional] string used to decrypt data
        :return: object with file body details (see NOTE below)
        
        NOTE:   the datatype returned is inferred from the record_key extension
                name. if the record_key ends with one of the following file 
                extensions then the returned datatype can be any json valid object:
                    .json
                    .yaml
                    .yml
                    .json.gz
                    .yaml.gz
                    .yml.gz
                    .drep
                the body of record_key values with .txt or .md extension are
                interpreted as string data types. any other file extension is
                returns a byte data type object. it is up to the saving method
                to ensure that the mimetype of byte data is correct.
        '''

        _title = '%s.read' % self.__class__.__name__
        _key_arg = '%s(record_key="%s")' % (_title, record_key)
        _secret_arg = '%s(secret_key="%s")' % (_title, secret_key)

    # validate inputs
        record_key = self.fields.validate(record_key, '.record_key', _key_arg)

    # construct path to file
        from os import path
        file_path = path.join(self.collection_folder, record_key)

    # validate existence of file
        if not path.exists(file_path):
            raise Exception('%s does not exist.' % _key_arg)

    # determine file name
        file_root, file_name = path.split(file_path)
        
    # open file and decode data
        from labpack.compilers.encoding import decode_data
        byte_data = open(file_path, 'rb')
        record_body = decode_data(file_name, byte_data, secret_key=secret_key)
    
        return record_body
            
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
        input_names = ['.max_results', '.record_key']
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
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')

    # apply filtering criteria
            if filter_function:
                if filter_function(*path_segments):
                    results_list.append(record_key)
            else:
                results_list.append(record_key)

    # return results list
            if len(results_list) == max_results:
                return results_list

        return results_list

    def delete(self, record_key):

        ''' a method to delete a file

        :param record_key: string with name of file
        :return: string reporting outcome
        '''

        _title = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(record_key="%s")' % (_title, record_key)

    # validate inputs
        record_key = self.fields.validate(record_key, '.record_key')

    # construct path to file
        file_path = os.path.join(self.collection_folder, record_key)

    # validate existence of file
        if not os.path.exists(file_path):
            return '%s does not exist.' % record_key
        current_dir = os.path.split(file_path)[0]

    # remove file
        try:
            os.remove(file_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, record_key))

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

        return '%s has been deleted.' % record_key

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
    
    def export(self, storage_client, overwrite=True):
        
        '''
            a method to export all the records in collection to another platform
            
        :param storage_client: class object with storage client methods
        :return: string with exit message
        '''
        
        title = '%s.export' % self.__class__.__name__
        
    # validate storage client
        method_list = [ 'create', 'read', 'list', 'export', 'delete', 'remove', '_import' ]
        for method in method_list:
            if not getattr(storage_client, method, None):
                from labpack.parsing.grammar import join_words
                raise ValueError('%s(storage_client=...) must be a client object with %s methods.' % (title, join_words(method_list)))
            
    # walk collection folder to find files
        import os
        root_segments = self.collection_folder.split(os.sep)
        count = 0
        skipped = 0
        for file_path in self.localhost.walk(self.collection_folder):
            count += 1
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')
            
    # read file and save files
            byte_data = open(file_path, 'rb').read()
            outcome = storage_client._import(record_key, byte_data, overwrite)
            if not outcome:
                count -= 1
                skipped += 1
            
    # report outcome
        plural = ''
        skip_insert = ''
        new_root, new_folder = os.path.split(storage_client.collection_folder)
        if count != 1:
            plural = 's'
        if skipped > 0:
            skip_plural = ''
            if skipped > 1:
                skip_plural = 's'
            skip_insert = ' %s record%s skipped to avoid overwrite.' % (str(skipped), skip_plural)
        exit_msg = '%s record%s exported to %s.%s' % (str(count), plural, new_folder, skip_insert)
        return exit_msg

if __name__ == '__main__':
    
    from time import time
    old_client = appdataClient(collection_name='Test Export')
    new_client = appdataClient(collection_name='Test Import')
    
    try:
        secret_key = 'password'
        record_key = 'test/migrate/%s.drep' % str(time())
        record_body = { 'test': 'value' }
        old_client.create(record_key, record_body, secret_key=secret_key)
        exit_msg = old_client.export(new_client)
        exit_msg = old_client.export(new_client, overwrite=False)
        record_details = new_client.read(record_key, secret_key)
        assert record_details == record_body
        print(exit_msg)
    except Exception as err:
        print(err)
    old_client.remove()
    new_client.remove()
    
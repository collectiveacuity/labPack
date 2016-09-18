__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
import yaml
import gzip
import json
from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
from labpack.parsing.regex import labRegex
from labpack.platforms.localhost import localhostClient

class appdataConnectionError(Exception):
    def __init__(self, message='', request_name='', error_dict=None):
        generic_msg = 'Failure connecting to app data'
        self.error = {
            'message': message,
            'request_name': request_name
        }
        if error_dict:
            if isinstance(error_dict, dict):
                for key, value in error_dict.items():
                    self.error[key] = value
        if self.error['message']:
            text = self.error['message']
        elif self.error['request_name']:
            text = '%s with %s request.' % (generic_msg, self.error['request_name'])
        else:
            text = '%s.' % generic_msg
        super(appdataConnectionError, self).__init__(text)

class appdataModel(object):
    
    def __init__(self, record_schema=None, collection_settings=None, appdata_model=None, access_key=''):

        '''
            a method to initialize the appdata file storage class

        :param record_schema: dictionary with record schema in jsonModel format
        :param collection_settings: dictionary with collection settings
        :param appdata_model: [optional] appdataModel object with pre-existing settings
        :param access_key: [optional] string to access drep index

        general database model init args:
            record_schema
            collection_settings
            access_credentials
        '''

        class_name = self.__class__.__name__
        
        if appdata_model:
            if isinstance(appdata_model, appdataModel):
                self.metadata = {}
                self.data = {}
                self.model = appdata_model.model
                self.settings = appdata_model.settings
                self.methods = appdata_model.methods
                self.index = appdata_model.index
                self.access = appdata_model.access
            else:
                raise TypeError('\nModel input must be an %s object.' % class_name)
        
        elif record_schema and collection_settings:
            collection_schema = {
                'schema': {
                    'collection_name': '',
                    'prod_name': '',
                    'org_name': '',
                    'versioning': False,
                    'index_fields': [ '.dt' ],
                    'file_extension': ''
                },
                'components': {
                    '.file_extension': {
                        'discrete_values': [ 'json', 'json.gz', 'yaml', 'yaml.gz', 'drep' ]
                    }
                }
            } 
            collection_model = jsonModel(collection_schema)
            self.metadata = {}
            self.data = {}
            self.model = jsonModel(record_schema)
            self.settings = collection_model.ingest(**collection_settings)
            self.index = []
            for item in self.settings['index_fields']:
                if item not in self.model.keyMap.keys():
                    raise ValueError('\nCollection settings index item %s is not found in record schema.' % item)
                else:
                    self.index.append(item)
            client_kwargs = {
                'collection_name': self.settings['collection_name'],
                'org_name': self.settings['org_name'],
                'prod_name': self.settings['prod_name']
            }
            self.methods = appdataClient(**client_kwargs)
            self.access = ''
            if access_key:
                if isinstance(access_key, str):
                    self.access = access_key
        
        else:
            raise IndexError('\n%s init requires either an existing %s or record schema and collection settings.' % (class_name, class_name))
            
    def new(self, **kwargs):
        return self
    
    def save(self, overwrite=True):

        '''

        :param overwrite: boolean to overwrite existing file if update without versioning
        :return: primary key

        general database model args:
            overwrite
            access_ids
        '''

        primary_key = ''

        return primary_key
    
    def load(self, primary_key):
        return self
    
    def delete(self):
        return self

    def migrate(self, storage_model):
        return self
    
    def find(self, query_filters=None, max_results=1, sort_order=None, reverse_search=True, starting_key='', all_versions=False, scan_records=False):

        '''

        :param query_filters: list with query criteria dictionaries to filter records
        :param max_results: integer with maximum number of results to return (up to 100)
        :param sort_order: list with index key direction value pairs to sort result order by
        :param reverse_search: boolean to begin search with last item first
        :param starting_key: string with key to begin next search with (for pagination)
        :param all_versions: boolean to retrieve all versions of record
        :param scan_record: boolean to search body of records with criteria in query filters
        :param secret_key: string with secret key used to
        :return: list of primary_keys, next_key

        sort_order - list of keys to sort by along with ascending or descending order value
            sort_order = [ { '.userid': 'ascending' }, { '.datetime': 'descending' } ]

        general database model args:
            query_index (not relevant for file store)
            signature_key (not relevant for non drep files)
            query_filters
            max_results
            sort_order
            reverse_search
            starting_key
            all_versions
            scan_record
        '''

        result_list = []
        return result_list

    def compact(self, total_number=0, cutoff_date=''):

        return True

class appdataClient(object):

    '''
        a class of methods for managing file storage in the local app data
    '''

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'collection_name': 'User Data',
            'key_string': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'key_string_path': '/home/user/.config/collective-acuity-labpack/user-data/obs/terminal',
            'key_string_comp': 'obs',
            'previous_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'body_dict': { 'dT': 1458235492.311154 },
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'max_results': 1,
            'path_filters': [ {} ],
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
            },
            'sort_order': {}
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
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ],
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

    def __init__(self, collection_name='', org_name='', prod_name=''):

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

    # validate existence of file data folder in app data (or create)
        self.appFolder = self.localhost.appData(org_name=org_name, prod_name=prod_name)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            collection_name = collection_name.replace(' ', '-').lower()
        self.collectionFolder = os.path.join(self.appFolder, collection_name)
        if not os.path.exists(self.collectionFolder):
            os.makedirs(self.collectionFolder)

    # construct supported file type regex patterns
        file_extensions = {
            "json": ".+\\.json$",
            "json.gz": ".+\\.json\\.gz$",
            "yaml": ".+\\.ya?ml$",
            "yaml.gz": ".+\\.ya?ml\\.gz$",
            "drep": ".+\\.drep$"
        }
        self.ext = labRegex(file_extensions)
        
    def create(self, key_string, body_dict, overwrite=True, secret_key=''):

        '''
            a method to create a file in the collection folder

        :param key_string: string with name to assign file (see NOTE below)
        :param body_dict: dictionary with file body details
        :param overwrite: boolean to overwrite files with same name
        :param secret_key: [optional] string with key to encrypt body data
        :return: self

            NOTE:   key_string may only contain alphanumeric, /, _, . or -
                    characters and may not begin with the . or / character.
                    key_string must end with one of the acceptable file
                    extensions:
                        .json
                        .yaml
                        .yml
                        .json.gz
                        .yaml.gz
                        .yml.gz
                        .drep

            NOTE:   using one or more / characters splits the key into
                    separate segments. these segments will appear as a
                    sub directories inside the record collection and each
                    segment is used as a separate index for that record
                    when using the list method
                    eg. lab/unittests/1473719695.2165067.json is indexed:
                    [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
        '''

        method_name = '%s.create' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (method_name, key_string)
        _body_arg = '%s(body_dict={...}' % {method_name}
        _secret_arg = '%s(secret_key="%s")' % (method_name, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string')
        body_dict = self.fields.validate(body_dict, '.body_dict')

    # construct file path
        file_path = os.path.join(self.collectionFolder, key_string)
        file_path = self.fields.validate(file_path, '.key_string_path')
        current_path = os.path.split(file_path)
        self.fields.validate(current_path[1], '.key_string_comp')
        while current_path[0] != self.collectionFolder:
            current_path = os.path.split(current_path[0])
            self.fields.validate(current_path[1], '.key_string_comp')

    # construct file data
        file_time = 0
        file_data = ''.encode('utf-8')
        key_map = self.ext.map(key_string)[0]
        if key_map['json']:
            file_data = json.dumps(body_dict).encode('utf-8')
        elif key_map['yaml']:
            file_data = yaml.dump(body_dict).encode('utf-8')
        elif key_map['json.gz']:
            file_bytes = json.dumps(body_dict).encode('utf-8')
            file_data = gzip.compress(file_bytes)
        elif key_map['yaml.gz']:
            file_bytes = yaml.dump(body_dict).encode('utf-8')
            file_data = gzip.compress(file_bytes)
        elif key_map['drep']:
            from labpack.compilers import drep
            secret_key = self.fields.validate(secret_key, '.secret_key')
            file_data = drep.dump(body_dict, secret_key)
            file_time = 1

    # check overwrite exception
        if not overwrite:
            if os.path.exists(file_path):
                raise Exception('%s already exists. To overwrite %s, set overwrite=True' % (_key_arg, key_string))

    # create directories in path to file
        dir_path = os.path.split(file_path)
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

        return self

    def read(self, key_string, secret_key=''):

        '''
            a method to retrieve body details from a file

        :param key_string: string with name of file
        :param secret_key: [optional] string used to decrypt data
        :return: dictionary with file content details
        '''

        method_name = '%s.create' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (method_name, key_string)
        _secret_arg = '%s(secret_key="%s")' % (method_name, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string')

    # construct path to file
        file_path = os.path.join(self.collectionFolder, key_string)

    # validate existence of file
        if not os.path.exists(file_path):
            raise Exception('%s does not exist.' % _key_arg)

    # retrieve file details
        file_details = {}
        key_map = self.ext.map(key_string)[0]
        if key_map['json']:
            try:
                file_data = open(file_path, 'rt')
                file_details = json.loads(file_data.read())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif key_map['yaml']:
            try:
                file_data = open(file_path, 'rt')
                file_details = yaml.load(file_data.read())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif key_map['json.gz']:
            try:
                file_data = gzip.open(file_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                file_details = json.loads(file_data.read().decode())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif key_map['yaml.gz']:
            try:
                file_data = gzip.open(file_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                file_details = yaml.load(file_data.read().decode())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif key_map['drep']:
            from labpack.compilers import drep
            secret_key = self.fields.validate(secret_key, '.secret_key')
            try:
                file_data = open(file_path, 'rb').read()
                file_details = drep.load(encrypted_data=file_data, secret_key=secret_key)
            except:
                raise Exception('%s is not valid drep data.' % _key_arg)

        return file_details

    def list(self, max_results=1, reverse_order=True, previous_key=''):

        '''
            a method to list keys in collection

        :param max_results: integer with maximum number of results to return
        :param reverse_order: boolean to search keys in reverse alphanumeric order
        :param previous_key: string with key in collection to begin search after
        :return: list of key strings
        '''

        __name__ = '%s.list(...)' % self.__class__.__name__

    # validate input
        input_kwargs = [max_results, previous_key]
        input_names = ['.max_results', '.key_string']
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # construct empty results list
        results_list = []
        root_segments = self.collectionFolder.split(os.sep)
        if previous_key:
            previous_key = os.path.join(self.collectionFolder, previous_key)

    # walk collection folder to find files
        for file_path in self.localhost.walk(self.collectionFolder, reverse_order, previous_key):
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            key_string = os.path.join(*path_segments)
            key_string = key_string.replace('\\','/')
            results_list.append(key_string)

    # return results list
            if len(results_list) == max_results:
                return results_list

        return results_list

    def find(self, path_filters=None, max_results=1, reverse_order=True, previous_key=''):

        '''
            a method to discover key strings from a query criteria on path segments

        :param path_filters: list of dictionaries with path segment query criteria
        :param max_results: integer with maximum number of results to return
        :param reverse_order: boolean to search keys in reverse alphanumeric order
        :param previous_key: string with key in collection to begin search after
        :return: list of key strings
        
            **NOTE: each key string can be divided into one or more segments
                    based upon the / characters which occur in the key string as
                    well as its file extension type. if the key string represents
                    a file path, then each directory in the path, the file name
                    and the file extension are all separate indexed values.
                    
                    eg. lab/unittests/1473719695.2165067.json is indexed:
                    [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
                    
                    it is possible to filter the records in the collection according
                    to one or more of these path segments using the query filters.

                    each item in the query filters argument must be a dictionary
                    which is composed of integer-value key names that represent the
                    index value of the file path segment to test and key values
                    with the dictionary of conditional operators used to test the 
                    string value in the indexed field of the record.
                    
                    eg. path_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]
                    
                    this example filter looks at the first segment of each key string
                    in the collection for a string value which starts with the 
                    characters 'lab'. as a result, it will match both the example
                    record above as well as another key string called
                    'laboratory20160912.json'

            **NOTE: the query method uses a query filters list structure to represent
                    the disjunctive normal form of a logical expression. a record is
                    added to the results list if any query criteria dictionary in the
                    list evaluates to true. within each query_criteria dictionary, all
                    declared conditional operators must evaluate to true.

            **NOTE: in this way, the path_filters represents a boolean OR operator and
                    the query_criteria represents a boolean AND operator between all
                    keys in the dictionary. any number of path segments may be added to
                    each query criteria dictionary, but the method will only return
                    key_strings which match all indexed criteria.
                    
            NOTE:   all values in each indexed segment are a string datatype

        path_filters:
            [ { 0: { conditional operators }, 1: { conditional_operators }, ... } ]

        conditional operators for an index criteria:
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

    # TODO: Look into declarative query language architecture instead

        __name__ = '%s.list' % self.__class__.__name__
        _filter_arg = '%s(path_filters={...})' % __name__
        _results_arg = '%s(max_results=1)' % __name__
        _starting_arg = '%s(starting_key="...")' % __name__

    # validate inputs
        input_args = [ path_filters, max_results, previous_key ]
        input_names = [ '.path_filters', '.max_results', '.key_string' ]
        for i in range(len(input_args)):
            if input_args[i]:
                self.fields.validate(input_args[i], input_names[i])
        if path_filters:
            for filter in path_filters:
                if not isinstance(filter, dict):
                    raise TypeError('%s must be a dictionary datatype.' % _filter_arg)
                for key, value in filter.items():
                    _key_name = '%s : {...}' % key
                    if not isinstance(key, str):
                        raise TypeError('%s key name must be an string.' % _filter_arg.replace('...', _key_name))
                    elif not isinstance(value, dict):
                        raise TypeError('%s key value must be a dictionary' % _filter_arg.replace('...', _key_name))
                    self.fields.validate(value, '.path_filter')

    # construct index model
        index_schema = {'schema': {'index_segment': 'string'}}
        index_model = jsonModel(index_schema)
    
    # construct empty results list
        results_list = []
        root_segments = self.collectionFolder.split(os.sep)
        if previous_key:
            previous_key = os.path.join(self.collectionFolder, previous_key)

    # construct query test function
        def _yield_results(index_criteria, path_segments):
            file_match = True
            for key, value in index_criteria.items():
                query_criteria = {'.index_segment': value}
                try:
                    valid_record = {'index_segment': path_segments[int(key)]}
                    if not index_model.query(query_criteria, valid_record):
                        file_match = False
                        break
                except:
                    file_match = False
                    break
            return file_match

    # decompose file path values into path segments and test against filters
        for file_path in self.localhost.walk(self.collectionFolder, reverse_order, previous_key):
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            key_string = os.path.join(*path_segments)
            key_string = key_string.replace('\\','/')
            for key, value in self.ext.map(path_segments[-1])[0].items():
                if value and isinstance(value, bool):
                    crop_length = int((len(key) + 1) * -1)
                    path_segments[-1] = path_segments[-1][0:crop_length]
                    path_segments.append('.%s' % key)
                    for filter in path_filters:
                        if _yield_results(filter, path_segments):
                            results_list.append(key_string)
                            break

    # end search if results match desired result number
            if len(results_list) == max_results:
                return results_list

        return results_list

    def delete(self, key_string):

        '''
            a method to delete a file

        :param key_string: string with name of file
        :return: string reporting outcome
        '''

        __name__ = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string')

    # construct path to file
        file_path = os.path.join(self.collectionFolder, key_string)

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
        while current_dir != self.collectionFolder:
            if not os.listdir(current_dir):
                os.rmdir(current_dir)
                current_dir = os.path.split(current_dir)[0]
            else:
                break

        return '%s has been deleted.' % key_string

    def remove(self):

        '''
            a method to remove all records in the collection

        :return: string with confirmation of deletion
        '''

        __name__ = '%s.remove' % self.__class__.__name__

    # remove collection tree
        try:
            import shutil
            shutil.rmtree(self.collectionFolder)
        except:
            raise Exception('%s failed to remove %s collection from app data.' % (__name__, self.collectionFolder))

        return '%s collection has been removed from app data.' % self.collectionFolder

if __name__ == '__main__':
    appdataModel()
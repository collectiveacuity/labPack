__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from os import path, listdir, remove
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

        :param record_schema:
        :param collection_settings:
        :param appdata_model:

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
            else:
                raise TypeError('\nModel input must be an %s object.' % class_name)
        
        elif record_schema and collection_settings:
            collection_schema = {
                'schema': {
                    'folder_name': '',
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
                'folder_name': self.settings['folder_name'],
                'org_name': self.settings['org_name'],
                'prod_name': self.settings['prod_name']
            }
            self.methods = appdataClient(**client_kwargs)
        
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
            'folder_name': 'User Data',
            'key_string': 'obs-terminal-2016-03-17T17-24-51-687845Z.yaml',
            'body_dict': { 'dT': 1458235492.311154 },
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'max_results': 1,
            'key_filters': {
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
              'must_not_contain': ['/']
            },
            '.prod_name': {
                'must_not_contain': ['/']
            },
            '.folder_name': {
                'must_not_contain': ['/']
            },
            '.key_string': {
                'must_not_contain': [ '[^\\w\\-\\.]' ],
                'contains_either': [ '\\.json$', '\\.ya?ml$', '\\.json\\.gz$', '\\.ya?ml\\.gz$', '\\.drep$' ]
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
            '.key_filters.discrete_values': {
                'required_field': False
            },
            '.key_filters.excluded_values': {
                'required_field': False
            },
            '.key_filters.must_contain': {
                'required_field': False
            },
            '.key_filters.must_not_contain': {
                'required_field': False
            },
            '.key_filters.contains_either': {
                'required_field': False
            }
        }
    }

    def __init__(self, folder_name='', org_name='', prod_name=''):

    # add localhost property to class
        self.localhost = localhostClient()

    # construct input validation model
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        if not folder_name:
            folder_name = 'User Data'
        else:
            folder_name = self.fields.validate(folder_name, '.folder_name')
        if not org_name:
            org_name = __team__
        else:
            org_name = self.localhost.fields.validate(org_name, '.org_name')
        if not prod_name:
            prod_name = __module__

    # validate existence of file data folder in app data (or create)
        self.appFolder = self.localhost.appData(org_name=org_name, prod_name=prod_name)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            folder_name = folder_name.replace(' ', '-').lower()
        self.collectionFolder = path.join(self.appFolder, folder_name)
        if not path.exists(self.collectionFolder):
            from os import makedirs
            makedirs(self.collectionFolder)

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
            a method to create a file in store folder

        :param key_string: string with name to assign file
        :param body_dict: dictionary with file body details
        :param overwrite: boolean to overwrite files with same name
        :param secret_key: [optional] string with key to encrypt body data
        :return: self
        '''

        method_name = '%s.create' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (method_name, key_string)
        _body_arg = '%s(body_dict={...}' % {method_name}
        _secret_arg = '%s(secret_key="%s")' % (method_name, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string')
        body_dict = self.fields.validate(body_dict, '.body_dict')

    # construct data file path
        file_path = ''
        file_data = ''.encode('utf-8')
        key_map = self.ext.map(key_string)[0]
        if key_map['json']:
            file_path = path.join(self.collectionFolder, key_string)
            file_data = json.dumps(body_dict).encode('utf-8')
        elif key_map['yaml']:
            file_path = path.join(self.collectionFolder, key_string)
            file_data = yaml.dump(body_dict).encode('utf-8')
        elif key_map['json.gz']:
            file_path = path.join(self.collectionFolder, key_string)
            file_bytes = json.dumps(body_dict).encode('utf-8')
            file_data = gzip.compress(file_bytes)
        elif key_map['yaml.gz']:
            file_path = path.join(self.collectionFolder, key_string)
            file_bytes = yaml.dump(body_dict).encode('utf-8')
            file_data = gzip.compress(file_bytes)
        elif key_map['drep']:
            from labpack.compilers import drep
            secret_key = self.fields.validate(secret_key, '.secret_key')
            file_path = path.join(self.collectionFolder, key_string)
            file_data = drep.dump(body_dict, secret_key)

    # save file data to folder
        if not overwrite:
            if path.exists(file_path):
                raise Exception('%s already exists. To overwrite %s, set overwrite=True' % (_key_arg, key_string))
        with open(file_path, 'wb') as f:
            f.write(file_data)
            f.close()

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
        file_path = path.join(self.collectionFolder, key_string)

    # validate existence of file
        if not path.exists(file_path):
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

    def list(self, key_filters=None, max_results=1, reverse_search=True, starting_key=''):

        '''
            a method to find key strings from query filters

            NOTE: query filters only apply to key_string, not contents of records

        :param key_filters: dictionary with conditional operators for key string filter
        :param max_results: integer with maximum number of results to return
        :param reverse_search: boolean to start search from last file in folder first
        :param starting_key: string with file name of record to begin search on
        :return: list of file names

        conditional operators for key_string
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
        _key_arg = '%s(key_filters={...})' % __name__
        _results_arg = '%s(max_results=1)' % __name__
        _starting_arg = '%s(starting_key="...")' % __name__

    # validate inputs
        input_args = [ key_filters, max_results, starting_key ]
        input_names = [ '.key_filters', '.max_results', '.key_string' ]
        for i in range(len(input_args)):
            if input_args[i]:
                self.fields.validate(input_args[i], input_names[i])

    # construct result function
        def _yield_results(query_filters, record_details):
            for query_criteria in query_filters:
                if self.localhost.fileModel.query(query_criteria, record_details):
                    return True
            return False

    # retrieve list of files from collection and order them
        collection_files = listdir(self.collectionFolder)
        collection_length = len(collection_files)
        if reverse_search:
            reversed(collection_files)

    # validate starting key and determine starting index
        starting_index = 0
        if starting_key:
            if starting_key not in collection_files:
                _starting_arg = _starting_arg.replace('...', starting_key)
                raise ValueError('%s is not a file in the collection %s.' % (_starting_arg, path.basename(self.collectionFolder)))
            else:
                starting_index = collection_files.index(starting_key)

    # construct empty results list
        results_list = []

    # search file names in collection for query match
        for i in range(starting_index, collection_length):
            file_name = collection_files[i]
            file_record = { 'file_name': file_name }
            query_criteria = [ { '.file_name': key_filters } ]
            filter_match = False
            if _yield_results(query_criteria, file_record):
                filter_match = True

    # make sure that file name is an eligible extension
            if filter_match:
                key_map = self.ext.map(file_name)[0]
                for key in key_map.keys():
                    if key_map[key]:
                        results_list.append(file_name)

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
        file_path = path.join(self.collectionFolder, key_string)

    # validate existence of file
        if not path.exists(file_path):
            return '%s does not exist.' % key_string

        try:
            remove(file_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, key_string))

        return '%s has been deleted.' % key_string

if __name__ == '__main__':
    appdataModel()
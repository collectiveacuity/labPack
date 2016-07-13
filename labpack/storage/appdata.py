__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from os import path, listdir, remove

from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
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
    
    def __init__(self, record_schema=None, collection_settings=None, appdata_model=None):

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
                    'index_fields': [ '.dt' ]
                }
            } 
            collection_model = jsonModel(collection_schema)
            self.metadata = {}
            self.data = {}
            self.model = jsonModel(record_schema)
            self.settings = collection_model.ingest(**collection_settings)
            if not self.settings['index_fields']:
                self.index = False
            else:
                self.index = True
                for item in self.settings['index_fields']:
                    if item not in self.model.keyMap.keys():
                        raise ValueError('\nCollection settings index item %s is not found in record schema.' % item)
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
    
    def find(self, query_filters=None, max_results=1, sort_order=None, reverse_search=True, starting_key='', all_versions=False, scan_record=False):

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
            'max_results': 1,
            'query_filters': {},
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
                'must_not_contain': [ '[^\\w\\-_\\.]' ],
                'contains_either': [ '\\.json$', '\\.ya?ml$', '\\.json\\.gz$', '\\.ya?ml\\.gz$' ]
            },
            '.body_dict': {
                'extra_fields': True
            },
            '.body_dict.dT': {
                'required_field': False
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            }
        }
    }

    def __init__(self, folder_name='', org_name='', prod_name=''):

    # add localhost property to class
        self.localhost = localhostClient()

    # construct input validation model
        self.validInput = jsonModel(self._class_fields)

    # validate inputs
        if not folder_name:
            folder_name = 'User Data'
        else:
            folder_name = self.validInput.validate(folder_name, '.folder_name')
        if not org_name:
            org_name = __team__
        else:
            org_name = self.localhost.validInput.validate(org_name, '.org_name')
        if not prod_name:
            prod_name = __module__

    # validate existence of file data folder in app data (or create)
        self.appFolder = self.localhost.appData(org_name=org_name, prod_name=prod_name)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            folder_name = folder_name.replace(' ', '-').lower()
        self.storeFolder = path.join(self.appFolder, folder_name)
        if not path.exists(self.storeFolder):
            from os import makedirs
            makedirs(self.storeFolder)

    # construct supported file type regex patterns
        class _regex_ext(object):
            def __init__(self):
                from re import compile
                self.json = compile('\.json$')
                self.yaml = compile('\.ya?ml$')
                self.jsongz = compile('\.json\.gz$')
                self.yamlgz = compile('\.ya?ml\.gz$')
                self.drep = compile('\.drep$')
                self.types = ['.json','.json.gz','.yaml','.yml','.yaml.gz','.yml.gz','.drep']
                self.names = ['json', 'yaml', 'jsongz', 'yamlgz', 'drep']
        self.ext = _regex_ext()

    def put(self, key_string, body_dict, override=True):

        '''
            a method to create a file in store folder

        :param key_string: string with name to assign file
        :param body_dict: dictionary with file body details
        :param override: boolean to overwrite files with same name
        :return: self
        '''

        __name__ = '%s.put' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)
        _body_arg = '%s(body_dict={...}' % {__name__}

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')
        body_dict = self.validInput.validate(body_dict, '.body_dict')

    # construct data file path
        file_path = ''
        file_data = ''.encode('utf-8')
        if self.ext.json.findall(key_string):
            import json
            file_path = path.join(self.storeFolder, key_string)
            file_data = json.dumps(body_dict).encode('utf-8')
        elif self.ext.yaml.findall(key_string):
            import yaml
            file_path = path.join(self.storeFolder, key_string)
            file_data = yaml.dump(body_dict).encode('utf-8')
        elif self.ext.jsongz.findall(key_string):
            import json
            from gzip import compress
            file_path = path.join(self.storeFolder, key_string)
            file_bytes = json.dumps(body_dict).encode('utf-8')
            file_data = compress(file_bytes)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            from gzip import compress
            file_path = path.join(self.storeFolder, key_string)
            file_bytes = yaml.dump(body_dict).encode('utf-8')
            file_data = compress(file_bytes)
        elif self.ext.drep.findall(key_string):
            from dev.compilers import drep
            file_path = path.join(self.storeFolder, key_string)
            private_key, file_data, drep_index = drep.dump(body_dict)

    # save file data to folder
        if not override:
            if path.exists(file_path):
                raise Exception('%s already exists. To overwrite %s, set override=True' % (_key_arg, key_string))
        with open(file_path, 'wb') as f:
            f.write(file_data)
            f.close()

        return self

    def get(self, key_string):

        '''
            a method to retrieve body details from a file

        :param key_string: string with name of file
        :return: dictionary with body details
        '''

        __name__ = '%s.get' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')

    # construct path to file
        file_path = path.join(self.storeFolder, key_string)

    # validate existence of file
        if not path.exists(file_path):
            raise Exception('%s does not exist.' % _key_arg)

    # retrieve file details
        file_details = {}
        if self.ext.json.findall(key_string):
            import json
            try:
                file_data = open(file_path, 'rt')
                file_details = json.loads(file_data.read())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yaml.findall(key_string):
            import yaml
            try:
                file_data = open(file_path, 'rt')
                file_details = yaml.load(file_data.read())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.jsongz.findall(key_string):
            import json
            import gzip
            try:
                file_data = gzip.open(file_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                file_details = json.loads(file_data.read().decode())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            import gzip
            try:
                file_data = gzip.open(file_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                file_details = yaml.load(file_data.read().decode())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.drep.findall(key_string):
            from dev.compilers import drep
            try:
                file_data = open(file_path)
                file_details = drep.load(private_key='', encrypted_data=file_data)
            except:
                raise Exception('%s is not valid drep data.' % _key_arg)

        return file_details

    def query(self, key_filters=None, body_filters=None, max_results=1, reverse_search=True):

        '''
            a method to find files from query parameters

        :param key_filters: dictionary with query criteria for record key
        :param body_filters: dictionary with names & query criteria for fields in record body
        :param max_results: integer with maximum number of results to return
        :param reverse_search: boolean to start search from last file in folder first
        :return: list of file names
        '''

    # TODO: Look into declarative query language architecture instead

        __name__ = '%s.query' % self.__class__.__name__
        _key_arg = '%s(key_filters={...})' % __name__
        _body_arg = '%s(body_filters={...})' % __name__
        _results_arg = '%s(max_results=1)' % __name__

    # validate inputs
        input_args = [ key_filters, body_filters, max_results ]
        input_names = [ '.key_filters', '.body_filters', '.max_results' ]
        for i in range(len(input_args)):
            if input_args[i]:
                self.validInput.validate(input_args[i], input_names[i])

    # validate query criteria structure
        key_criteria = {}
        if key_filters:
            key_criteria = {
                '.key_string': key_filters
            }
            self.validInput.query(key_criteria)

    # construct search resource variables
        result_list = []
        file_list = listdir(self.storeFolder)
        if reverse_search:
            file_list = reversed(file_list)

    # conduct search over list of files in folder and return results
        for file in file_list:
            add_file = True

    # add files whose name match each regex expression in key query
            if key_criteria:
                file_name = { 'key_string': file }
                if not self.validInput.query(key_criteria, file_name):
                    add_file = False

    # add files whose top level values match each regex expression in body query
            if add_file and body_filters:
                valid_file = False
                for extension in self.ext.names:
                    regex_pattern = getattr(self.ext, extension)
                    if regex_pattern.findall(file):
                        valid_file = True
                if not valid_file:
                    add_file = False
                else:
                    file_details = self.get(file)
                    file_schema = {'schema': file_details}
                    file_model = jsonModel(file_schema)
                    if not file_model.query(body_filters, file_details):
                        add_file = False

    # add file that passes all query tests
            if add_file:
                for extension in self.ext.names:
                    regex_pattern = getattr(self.ext, extension)
                    if regex_pattern.findall(file):
                        result_list.append(file)

    # end search if results match desired result number
            if len(result_list) == max_results:
                return result_list

        return result_list

    def delete(self, key_string):

        '''
            a method to delete a file

        :param key_string: string with name of file
        :return: string reporting outcome
        '''

        __name__ = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')

    # construct path to file
        file_path = path.join(self.storeFolder, key_string)

    # validate existence of file
        if not path.exists(file_path):
            return '%s does not exist.' % key_string

        try:
            remove(file_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, key_string))

        return '%s has been deleted.' % key_string

    def compact(self, total_number=0, cutoff_date=''):

        return True

if __name__ == '__main__':
    appdataModel()
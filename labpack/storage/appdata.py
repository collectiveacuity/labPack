__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
import hashlib
from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
from labpack.platforms.localhost import localhostClient

class appdataModel(object):

    ''' a schema-enforceable class for managing record collections in local app data

        NOTE: class is still WIP

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

    _metadata_fields = {
        'schema': {
            'file_path': '',
            'update_date': '',
            'primary_key': '',
            'path_segments': ''
        }
    }

    _index_fields = {
        'schema': {
            'index_string': '9MY67Ke9thkefQUJU-1PYeUj',
        },
        'components': {
            '.index_string': {
                'must_not_contain': ['[^\\w\\-\\.]'],
                'max_length': 255
            }
        }
    }
    
    def __init__(self, record_schema=None, collection_settings=None, appdata_model=None):

        ''' initialization method for the appdata file storage class

        :param record_schema: dictionary with record schema in jsonModel format
        :param collection_settings: dictionary with collection settings
        :param appdata_model: [optional] appdataModel object with pre-existing settings

        record schema : {
            'schema': {
                'example_string': 'string',
                'example_dict': { },
                'example_number': 123.45
            }
        }

        collection settings : {
            'collection_name': 'User Data',
            'prod_name': 'labpack',
            'org_name': 'Collective Acuity',
            'versioning': False,
            'enforce_schema': False,
            'index_fields': [ '.deviceID', '.dt' ],
            'file_extension': 'json'
        }

        NOTE:   To maximize record flexibility, record schema should only include
                those fields which are used in the record index as well as fields
                which are vital to validate for other business logic processes.

                If enforce_schema is TRUE, then

        NOTE:   Index fields should contain enough fields to create a unique
                file path. Otherwise, records will overwrite other records. The
                order of the fields will effect the efficiency of the find method.
                Because the method walks the collection directory structure from
                bottom up, a wide range of values for indexed fields which appear
                prior to index field of interest may have to search through many
                file paths.

        NOTE:   If the value of an indexed field is not a string or number, it will
                be converted into its MD5Hash and can only be queried using the
                'discrete_values', 'excluded_values' and 'field_exists' criteria.
                The value of an indexed field in a record must contain only
                alphanumeric, _, - or . characters and be no longer than 255
                characters. Otherwise, the value will also be converted to an
                MD5Hash.

        general database model init args:
            record_schema
            collection_settings
            class_model
            access_credentials: [n/a] dictionary with properties required to access database
        '''

        class_name = self.__class__.__name__

        if appdata_model:
            if isinstance(appdata_model, appdataModel):
                self.metadata = {}
                self.data = {}
                self.model = appdata_model.model
                self.metadataFields = appdata_model.metadataFields
                self.indexFields = appdata_model.indexFields
                self.settings = appdata_model.settings
                self.methods = appdata_model.methods
                self.index = appdata_model.index
            else:
                raise TypeError('\nModel input must be an %s object.' % class_name)
        
        elif record_schema and collection_settings:
            client_fields = appdataClient._class_fields
            collection_schema = {
                'schema': {
                    'collection_name': 'User Data',
                    'prod_name': 'labpack',
                    'org_name': 'Collective Acuity',
                    'versioning': False,
                    'enforce_schema': True,
                    'index_fields': [ '.dt' ],
                    'file_extension': 'json'
                },
                'components': {
                    '.collection_name': client_fields['components']['.collection_name'],
                    '.prod_name': client_fields['components']['.prod_name'],
                    '.org_name': client_fields['components']['.org_name'],
                    '.file_extension': {
                        'discrete_values': [ 'json', 'json.gz', 'yaml', 'yaml.gz' ],
                        'default_value': 'json'
                    },
                    '.enforce_schema': { 'default_value': True }
                }
            } 
            collection_model = jsonModel(collection_schema)
            self.metadata = {}
            self.data = {}
            self.model = jsonModel(record_schema)
            self.metadataFields = jsonModel(self._metadata_fields)
            self.indexFields = jsonModel(self._index_fields)
            self.settings = collection_model.ingest(**collection_settings)
            self.index = []
            for item in self.settings['index_fields']:
                if item not in self.model.keyMap.keys():
                    raise ValueError('\nCollection settings index item %s is not found in record schema.' % item)
                else:
                    self.index.append(item)
            if not self.index:
                raise ValueError('\nCollection settings index must contain at least one field.')
            client_kwargs = {
                'collection_name': self.settings['collection_name'],
                'org_name': self.settings['org_name'],
                'prod_name': self.settings['prod_name']
            }
            self.methods = appdataClient(**client_kwargs)
        
        else:
            raise IndexError('\n%s init requires either an existing %s or record schema and collection settings.' % (class_name, class_name))
            
    def new(self, **kwargs):

        ''' a method to create a new record in the object model using keyword arguments

        :param kwargs: keyword arguments with fields to add to record
        :return: appdataModel

            NOTE:   To persist the record to disk, you must use self.save()

            NOTE:   Schema enforcement is turned ON by default but can be adjusted
                    in the collection settings.

                    While enforce_schema = True, any attempt to add a record which
                    does not validate according to the schema will raise an
                    InputValidationError exception. InputValidationErrors.error
                    contains a dictionary which can be used for error handling.

                    If enforce_schema = False, only those fields in the record which
                    validate against the schema will be included in the record and
                    any index fields with empty or invalid values will be indexed
                    with a 'null' value. Fields not specified in the schema are
                    included in the record as well.
        '''

        _title = '%s.new' % self.__class__.__name__

        record = appdataModel(appdata_model=self)
        record_data = {}
        for key, value in kwargs.items():
            record_data[key] = value
        if self.settings['enforce_schema']:
            record.data = self.model.validate(record_data)
        else:
            for key, value in record_data.items():
                dot_path = '.' + key
                if dot_path in self.model.keyMap.keys():
                    try:
                        record.data[key] = self.model.validate(value, dot_path)
                    except:
                        pass
                else:
                    record.data[key] = value

        return record
    
    def save(self, overwrite=True):

        ''' a method to save the values of a record to a file in local app data

        :param overwrite: [optional] boolean to force a consistency check
        :return: primary key (or float with latest updated time if overwrite = False)

            NOTE:   if the record does not exist, record is created. if record
                    already exists, default automatically overwrites existing data.

            versioning = True
            if previous data is important, set versioning to true in collection
            settings. versioning automatically appends a time stamp to all records.

            overwrite = False
            if data being changed by a separate process during custody is an issue,
            setting overwrite to false will force a check of lastModified value
            before save. if lastModified value in metadata does not match current
            record, save is aborted. to be meaningful, this toggle needs to be
            connected to a handler that is designed to respond to intervening
            changes to the data state.

        general database model args:
            overwrite
            access_ids
        '''

        _title = '%s.new' % self.__class__.__name__

    # check to see if data changed between last load
        if not overwrite:
            if self.metadata:
                file_path = self.metadata['file_path']
                try:
                    file_metadata = self.methods.localhost.metadata(file_path)
                    if self.metadata['update_date'] != file_metadata['update_date']:
                        return file_metadata['update_date']
                except:
                    return False

    # construct segments of primary key from index values
        path_segments = []
        for dot_path in self.index:
            path_segments.append(self._extract_value(dot_path))
        if self.settings['versioning']:
            from time import time
            micro_sec = str(time())
            path_segments.append(micro_sec[0:17])
        path_segments[-1] = path_segments[-1] + '.' + self.settings['file_extension']

    # join segments together into primary key
        primary_key = os.path.join(*path_segments)
        primary_key = primary_key.replace('\\', '/')

    # create save request
        save_kwargs = {
            'key_string': primary_key,
            'body_dict': self.data
        }
        try:
            return self.methods.create(**save_kwargs)
        except:
            return False

    def _extract_value(self, dot_path):

        ''' a helper method to extract the value for an indexed field from a record

        :param dot_path: string with dot path to indexed field
        :return: string that is URL safe and less than 256 characters
        '''

        if not self.model.query({dot_path: {'value_exists': True}}, self.data):
            return 'null'
        else:
            data_value = self.model._walk(dot_path, self.data)[0]
            data_type = self.model.keyMap[dot_path]['value_datatype']
            if data_type in ('boolean', 'string', 'number'):
                try:
                    return self.indexFields.validate(str(data_value), '.index_string')
                except:
                    return hashlib.md5(str(data_value).encode('utf-8')).hexdigest()
            else:
                return hashlib.md5(str(data_value).encode('utf-8')).hexdigest()

    def load(self, key_string):
        return self
    
    def delete(self):
        return self

    def migrate(self, storage_model):
        return self
    
    def find(self, index_filters=None, max_results=1, reverse_search=True, previous_key=''):

        '''
            a method to find records based upon their indexed values

        :param index_filters: list with index query criteria dictionaries to filter records
        :param max_results: integer with maximum number of results to return
        :param reverse_search: boolean to begin search with last item in collection first
        :param previous_key: string with key to begin next search with (for pagination)
        :return: list of primary keys

        sort_order - list of keys to sort by along with ascending or descending order value
            sort_order = [ { '.userid': 'ascending' }, { '.datetime': 'descending' } ]

        general database model args:
            query_index (not relevant for file store)
            signature_key (not relevant for non drep files)
            query_filters
            max_results
            reverse_search
            starting_key / previous_key (for paginated results)
            sort_order: list with index key direction value pairs to sort result order by
            all_version: boolean to retrieve all versions of record
            scan_record: boolean to search body of records with criteria in query filters
        '''

        result_list = []
        return result_list

    def compact(self, total_number=0, cutoff_date=''):

        return True

class appdataClient(object):

    ''' a low-level class of methods for managing file storage in local app data

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
                    key_string file_extension nor the byte data will be
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
            with open(file_path, 'wb') as f:
                f.write(byte_data)
                f.close()

        return key_string

    def read(self, key_string, secret_key=''):

        ''' a method to retrieve body details from a file

        :param key_string: string with name of file
        :param secret_key: [optional] string used to decrypt data
        :return: dictionary with file content details
        '''

        _title = '%s.read' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (_title, key_string)
        _secret_arg = '%s(secret_key="%s")' % (_title, secret_key)

    # validate inputs
        key_string = self.fields.validate(key_string, '.key_string', _key_arg)
        key_string = self.fields.validate(key_string, '.key_string_dict', _key_arg)

    # construct path to file
        file_path = os.path.join(self.collection_folder, key_string)

    # validate existence of file
        if not os.path.exists(file_path):
            raise Exception('%s does not exist.' % _key_arg)

    # retrieve file details
        from labpack.records.settings import load_settings
        load_kwargs = {
            'file_path': file_path,
            'secret_key': secret_key
        }
        file_details = load_settings(**load_kwargs)

        return file_details

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
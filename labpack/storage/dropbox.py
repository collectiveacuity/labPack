__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

'''
PLEASE NOTE:    dropbox package requires the dropbox module.

(all platforms) pip3 install dropbox
'''

try:
    from sys import path as sys_path
    sys_path.append(sys_path.pop(0))
    from dropbox import Dropbox
    sys_path.insert(0, sys_path.pop())
except:
    import sys
    print('dropbox package requires the dropbox module. try: pip3 install dropbox')
    sys.exit(1)
    
# TODO: incorporate rate limiting logic
# TODO: add method to retrieve metadata from record
# TODO: add method to use Dropbox search functionality

import os
from jsonmodel.validators import jsonModel

class DropboxConnectionError(Exception):
    
    def __init__(self, request='', message='', errors=None, captured_error=None):

    # report request attempt
        self.errors = errors
        text = 'Failure connecting to Dropbox API with %s request.' % request
    # test connectivity
        try:
            import requests
            requests.get('https://www.google.com')
        except:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            request_object = Request(method='GET', url='https://www.google.com')
            request_details = handle_requests(request_object)
            text += '\n%s' % request_details['error']
    # include original error message
        else:
            try:
                if captured_error:
                    raise captured_error
                else:
                    raise
            except Exception as err:
                text += '\n%s' % err
            if message:
                text += '\n%s' % message
    
        super(DropboxConnectionError, self).__init__(text)
        
class dropboxHandler(object):

    ''' handles responses from dropbox api and usage data'''

    _class_fields = {
        'schema': {
            'rate_limits': []
        }
    }

    def __init__(self, usage_client=None):

        ''' initialization method for dropbox handler class

        :param usage_client: callable that records usage data
        '''

    # construct class field model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct initial methods
        self.rate_limits = self.fields.schema['rate_limits']
        self.usage_client = usage_client

    def handle(self, response):

    # construct default response details
        details = {
            'method': response.request.method,
            'code': response.status_code,
            'url': response.url,
            'error': '',
            'json': None,
            'headers': response.headers
        }

        # rate limit headers:
        # https://www.meetup.com/meetup_api/docs/#limits
        # X-RateLimit-Limit
        # X-RateLimit-Remaining
        # X-RateLimit-Reset

    # handle different codes
        if details['code'] in (200, 201, 202):
            details['json'] = response.json()
        else:
            details['error'] = response.content.decode()

        return details

class dropboxRegister(object):
    ''' currently must be done manually '''
    # https://www.dropbox.com/developers/apps
    def __init__(self, app_settings):
        pass

    def setup(self):
        return self

    def update(self):
        return self

class dropboxClient(object):

    ''' a class of methods to manage file storage on Dropbox API '''

    # https://www.dropbox.com/developers/documentation/http/documentation

    _class_fields = {
        'schema': {
            'access_token': '',
            'collection_name': 'labPack',
            'record_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.ogg',
            'record_key_path': '/home/user/.config/collective-acuity-labpack/user-data/obs/terminal',
            'record_key_comp': 'obs',
            'previous_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'prefix': 'obs/terminal',
            'delimiter': '2016-03-17T17-24-51-687845Z.yaml',
            'max_results': 1
        },
        'components': {
            '.collection_name': {
                'max_length': 255,
                'must_not_contain': ['/', '^\\.']
            },
            '.record_key': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            },
            '.record_key_path': {
                'max_length': 32767
            },
            '.record_key_comp': {
                'max_length': 255
            },
            '.secret_key': {
                'must_not_contain': [ '[\\t\\n\\r]' ]
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            },
            '.previous_key': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            },
            '.prefix': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            }
        },
        'metadata': {
            'record_optimal_bytes': 10000 * 1024,
            'record_max_bytes': 150000 * 1024
        }
    }
    
    def __init__(self, access_token, collection_name=''):
        
        '''
            a method to initialize the dropboxClient class
            
        :param access_token: string with oauth2 access token for users account
        '''    

        title = '%s.__init__' % self.__class__.__name__
    
    # construct input validation model
        self.fields = jsonModel(self._class_fields)
        
    # validate inputs
        input_fields = {
            'access_token': access_token,
            'collection_name': collection_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # workaround for module namespace conflict
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from dropbox import Dropbox
        from dropbox.files import FileMetadata, WriteMode, DeleteArg
        from dropbox.exceptions import ApiError
        sys_path.insert(0, sys_path.pop())
    
    # construct dropbox client
        from labpack.compilers.objects import _method_constructor
        self.dropbox = Dropbox(oauth2_access_token=access_token)
    
    # construct dropbox objects
        self.objects = _method_constructor({
            'FileMetadata': FileMetadata,
            'ApiError': ApiError,
            'WriteMode': WriteMode,
            'DeleteArg': DeleteArg
        })
    
    # construct collection name
        self.collection_name = collection_name
    
    def _import(self, record_key, record_data, overwrite=True, last_modified=0.0, **kwargs):
        
        '''
            a helper method for other storage clients to import into appdata
            
        :param record_key: string with key for record
        :param record_data: byte data for body of record
        :param overwrite: [optional] boolean to overwrite existing records
        :param last_modified: [optional] float to record last modified date
        :param kwargs: [optional] keyword arguments from other import methods 
        :return: boolean indicating whether record was imported
        '''
        
        title = '%s._import' % self.__class__.__name__
    
    # check overwrite
        if not overwrite:
            if self.exists(record_key):
                return False
    
    # check max size
        import sys
        record_max = self.fields.metadata['record_max_bytes']
        record_size = sys.getsizeof(record_data)
        error_prefix = '%s(record_key="%s", record_data=b"...")' % (title, record_key)
        if record_size > record_max:
            raise ValueError('%s exceeds maximum record data size of %s bytes.' % (error_prefix, record_max))
    
    # TODO: apply session upload for files greater than record_max
            
    # construct upload kwargs
        upload_kwargs = {
            'f': record_data,
            'path': '/%s' % record_key,
            'mute': True,
            'mode': self.objects.WriteMode.overwrite
        }
    
    # modify file time
        import re
        if re.search('\\.drep$', record_key):
            from labpack.records.time import labDT
            drep_time = labDT.fromEpoch(1)
            upload_kwargs['client_modified'] = drep_time
        elif last_modified:
            from labpack.records.time import labDT
            mod_time = labDT.fromEpoch(last_modified)
            upload_kwargs['client_modified'] = mod_time
    
    # send upload request
        try:
            self.dropbox.files_upload(**upload_kwargs)
        except:
            raise DropboxConnectionError(title)
        
        return True
    
    def _walk(self, root_path=''):
        ''' an iterator method which walks the file structure of the dropbox collection '''
        title = '%s._walk' % self.__class__.__name__
        if root_path:
            root_path = '/%s' % root_path
        try:
            response = self.dropbox.files_list_folder(path=root_path, recursive=True)
            for record in response.entries:
                if not isinstance(record, self.objects.FileMetadata):
                    continue
                yield record.path_display[1:]
            if response.has_more:
                while response.has_more:
                    response = self.dropbox.files_list_folder_continue(response.cursor)
                    for record in response.entries:
                        if not isinstance(record, self.objects.FileMetadata):
                            continue
                        yield record.path_display[1:]
        except:
            raise DropboxConnectionError(title)
    
    def exists(self, record_key):
        
        ''' 
            a method to determine if a record exists in collection

        :param record_key: string with key of record
        :return: boolean reporting status
        '''
        
        title = '%s.exists' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # send get metadata request
        file_path = '/%s' % record_key
        try:
            self.dropbox.files_get_metadata(file_path)
        except Exception as err:
            if str(err).find("LookupError('not_found'") > -1:
                return False
            else:
                raise DropboxConnectionError(title)

        return True
        
    def save(self, record_key, record_data, overwrite=True, secret_key=''):

        ''' 
            a method to create a record in the collection folder

        :param record_key: string with name to assign to record (see NOTES below)
        :param record_data: byte data for record body
        :param overwrite: [optional] boolean to overwrite records with same name
        :param secret_key: [optional] string with key to encrypt data
        :return: string with name of record

        NOTE:   record_key may only contain alphanumeric, /, _, . or -
                characters and may not begin with the . or / character.

        NOTE:   using one or more / characters splits the key into
                separate segments. these segments will appear as a
                sub directories inside the record collection and each
                segment is used as a separate index for that record
                when using the list method
                eg. lab/unittests/1473719695.2165067.json is indexed:
                [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
        '''

        title = '%s.save' % self.__class__.__name__
            
    # validate inputs
        input_fields = {
            'record_key': record_key,
            'secret_key': secret_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
    
    # validate byte data
        if not isinstance(record_data, bytes):
            raise ValueError('%s(record_data=b"...") must be byte data.' % title)
        
    # construct and validate file path
        file_root, file_name = os.path.split(record_key)
        self.fields.validate(file_name, '.record_key_comp')
        while file_root:
            file_root, path_node = os.path.split(file_root)
            self.fields.validate(path_node, '.record_key_comp')

    # check overwrite exception
        if not overwrite:
            if self.exists(record_key):
                raise Exception('%s(record_key="%s") already exists. To overwrite, set overwrite=True' % (title, record_key))
    
    # check size of file
        import sys
        record_optimal = self.fields.metadata['record_optimal_bytes']
        record_max = self.fields.metadata['record_max_bytes']
        record_size = sys.getsizeof(record_data)
        error_prefix = '%s(record_key="%s", record_data=b"...")' % (title, record_key)
        if record_size > record_max:
            raise ValueError('%s exceeds maximum record data size of %s bytes.' % (error_prefix, record_max))
        elif record_size > record_optimal:
            print('[WARNING] %s exceeds optimal record data size of %s bytes.' % (error_prefix, record_optimal))
    
    # TODO add upload session for support of files over 150MB
    # http://dropbox-sdk-python.readthedocs.io/en/latest/moduledoc.html#dropbox.dropbox.Dropbox.files_upload_session_start
            
    # encrypt data
        if secret_key:
            from labpack.encryption import cryptolab
            record_data, secret_key = cryptolab.encrypt(record_data, secret_key)
    
    # construct upload kwargs
        upload_kwargs = {
            'f': record_data,
            'path': '/%s' % record_key,
            'mute': True,
            'mode': self.objects.WriteMode.overwrite
        }
    
    # modify file time
        import re
        if re.search('\\.drep$', file_name):
            from labpack.records.time import labDT
            drep_time = labDT.fromEpoch(1)
            upload_kwargs['client_modified'] = drep_time
    
    # send upload request
        try:
            self.dropbox.files_upload(**upload_kwargs)
        except:
            raise DropboxConnectionError(title)
        
        return record_key
    
    def load(self, record_key, secret_key=''):

        ''' 
            a method to retrieve byte data of appdata record

        :param record_key: string with name of record
        :param secret_key: [optional] string used to decrypt data
        :return: byte data for record body
        '''

        title = '%s.load' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key,
            'secret_key': secret_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct file path
        file_path = '/%s' % record_key
    
    # request file data
        try:
            metadata, response = self.dropbox.files_download(file_path)
        except Exception as err:
            if str(err).find("LookupError('not_found'") > -1:
                raise Exception('%s(record_key=%s) does not exist.' % (title, record_key))
            else:
                raise DropboxConnectionError(title)
        record_data = response.content
    
    # decrypt (if necessary)
        if secret_key:
            from labpack.encryption import cryptolab
            record_data = cryptolab.decrypt(record_data, secret_key)
    
        return record_data
    
    def conditional_filter(self, path_filters):

        ''' a method to construct a conditional filter function for list method

        :param path_filters: dictionary or list of dictionaries with query criteria
        :return: filter_function object

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

        title = '%s.conditional_filter' % self.__class__.__name__
        
        from labpack.compilers.filters import positional_filter
        filter_function = positional_filter(path_filters, title)
        
        return filter_function

    def list(self, prefix='', delimiter='', filter_function=None, max_results=1, previous_key=''):
        
        ''' 
            a method to list keys in the dropbox collection

        :param prefix: string with prefix value to filter results
        :param delimiter: string with value which results must not contain (after prefix)
        :param filter_function: (positional arguments) function used to filter results
        :param max_results: integer with maximum number of results to return
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
        
        title = '%s.list' % self.__class__.__name__
        
    # validate input
        input_fields = {
            'prefix': prefix,
            'delimiter': delimiter,
            'max_results': max_results,
            'previous_key': previous_key
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate filter function
        if filter_function:
            try:
                path_segments = [ 'lab', 'unittests', '1473719695.2165067', '.json' ]
                filter_function(*path_segments)
            except:
                err_msg = '%s(filter_function=%s)' % (title, filter_function.__class__.__name__)
                raise TypeError('%s must accept positional arguments.' % err_msg)

    # construct empty results list
        results_list = []
        check_key = True
        if previous_key: 
            check_key = False
    
    # determine root path
        root_path = ''
        if prefix:
            from os import path
            root_path, file_name = path.split(prefix)

    # iterate over dropbox files
        for file_path in self._walk(root_path):
            path_segments = file_path.split(os.sep)
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')
            if record_key == previous_key:
                check_key = True
    
    # find starting point
            if not check_key:
                continue
                
    # apply prefix filter
            partial_key = record_key
            if prefix:
                if record_key.find(prefix) == 0:
                    partial_key = record_key[len(prefix):]
                else:
                    continue
    
    # apply delimiter filter
            if delimiter:
                if partial_key.find(delimiter) > -1:
                    continue
    
    # apply filter function
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

        title = '%s.delete' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'record_key': record_key
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # validate existence of file
        if not self.exists(record_key):
            exit_msg = '%s does not exist.' % record_key
            return exit_msg
            
    # remove file
        current_dir = os.path.split(record_key)[0]
        try:
            file_path = '/%s' % record_key
            self.dropbox.files_delete(file_path)
        except:
            raise DropboxConnectionError(title)

    # remove empty directories in path to file
        try:
            while current_dir:
                folder_path = '/%s' % current_dir
                response = self.dropbox.files_list_folder(folder_path)
                if not response.entries:
                    self.dropbox.files_delete(folder_path)
                    current_dir = os.path.split(current_dir)[0]
                else:
                    break
        except:
            raise DropboxConnectionError(title)

        exit_msg = '%s has been deleted.' % record_key
        return exit_msg
    
    def remove(self):
        
        ''' 
            a method to remove all records in the collection

        NOTE:   this method removes all the files in the collection, but the
                collection folder itself created by oauth2 cannot be removed.
                only the user can remove the app folder
                
        :return: string with confirmation of deletion
        '''

        title = '%s.remove' % self.__class__.__name__
    
    # get contents in root
        try:
            response = self.dropbox.files_list_folder(path='')
        except:
            raise DropboxConnectionError(title)

    # populate delete list
        delete_list = []
        for file in response.entries:
            delete_list.append(self.objects.DeleteArg(path=file.path_display))

    # continue retrieval if folder is large
        if response.has_more:
            try:
                while response.has_more:
                    response = self.dropbox.files_list_folder_continue(response.cursor)
                    for file in response.entries:
                        delete_list.append(self.objects.DeleteArg(path=file.path_display))
            except:
                raise DropboxConnectionError(title)

    # send batch delete request
        try:
            self.dropbox.files_delete_batch(delete_list)
        except:
            raise DropboxConnectionError(title)
    
    # return outcome
        insert = 'collection'
        if self.collection_name:
            insert = self.collection_name
        exit_msg = 'Contents of %s will been removed from Dropbox.' % insert
        return exit_msg

    def export(self, storage_client, overwrite=True):
        
        '''
            a method to export all the records in collection to another platform
            
        :param storage_client: class object with storage client methods
        :return: string with exit message
        '''
        
        title = '%s.export' % self.__class__.__name__
        
    # validate storage client
        method_list = [ 'save', 'load', 'list', 'export', 'delete', 'remove', '_import', 'collection_name' ]
        for method in method_list:
            if not getattr(storage_client, method, None):
                from labpack.parsing.grammar import join_words
                raise ValueError('%s(storage_client=...) must be a client object with %s methods.' % (title, join_words(method_list)))
            
    # walk collection folder to find files
        import os
        count = 0
        skipped = 0
        for file_path in self._walk():
            path_segments = file_path.split(os.sep)
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')
            file_path = '/%s' % file_path
            
    # retrieve data and metadata
            try:
                metadata, response = self.dropbox.files_download(file_path)
            except:
                raise DropboxConnectionError(title)
            record_data = response.content
            client_modified = metadata.client_modified
            
    # import record into storage client
            last_modified = 0.0
            if client_modified:
                from dateutil.tz import tzutc
                from labpack.records.time import labDT
                last_modified = labDT.fromPython(client_modified.replace(tzinfo=tzutc())).epoch()
            outcome = storage_client._import(record_key, record_data, overwrite=overwrite, last_modified=last_modified)
            if outcome:
                count += 1
            else:
                skipped += 1
            
    # report outcome
        plural = ''
        skip_insert = ''
        new_folder = storage_client.collection_name
        if count != 1:
            plural = 's'
        if skipped > 0:
            skip_plural = ''
            if skipped > 1:
                skip_plural = 's'
            skip_insert = ' %s record%s skipped to avoid overwrite.' % (str(skipped), skip_plural)
        exit_msg = '%s record%s exported to %s.%s' % (str(count), plural, new_folder, skip_insert)
        return exit_msg
    
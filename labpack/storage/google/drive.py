__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

'''
PLEASE NOTE:    drive package requires the google-api-python-client module.

(all platforms) pip3 install google-api-python-client

PLEASE NOTE:    google drive is not designed to store files in the POSIX file hierarchy
                as a result, numerous requests are required to create the parentage
                and ensure that records exist in the correct nodes. if preserving the
                parentage does not matter, you can use the methods specified here:
                https://developers.google.com/drive/v3/web/manage-uploads

PLEASE NOTE:    oauth2 tokens granted by google drive expire quickly - usually after
                3600 seconds. to handle a large number of records, it may be necessary to
                refresh the token. to obtain an access token that can interact with a 
                google drive account, you must specify one of the following scopes in your
                access request: https://developers.google.com/drive/v3/web/about-auth
            
PLEASE NOTE:    however, to write to a google drive account using a non-approved app,
                the oauth2 grantee account must also join this google group
                https://groups.google.com/forum/#!forum/risky-access-by-unreviewed-apps
'''

try:
    from googleapiclient import discovery
except:
    import sys
    print('drive package requires the google-api-python-client module. try: pip3 install google-api-python-client')
    sys.exit(1)

# TODO: handle intermittent connectivity in export/import process
# TODO: handle variable permissions in export/import process
# TODO: add google document export method to load/save process
# TODO: store current folder path ids in import method to reduce redundant requests
# TODO: figure out a way to reduce redundant requests in list method with previous key

import os
from jsonmodel.validators import jsonModel

class DriveConnectionError(Exception):
    
    def __init__(self, request='', message='', errors=None, captured_error=None):

    # report request attempt
        self.errors = errors
        text = 'Failure connecting to Google Drive API with %s request.' % request
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
    
        super(DriveConnectionError, self).__init__(text)
    
class driveClient(object):
    
    ''' a class of methods to manage file storage on Google Drive API '''

    # https://developers.google.com/drive/v3/web/about-sdk
    # https://developers.google.com/api-client-library/python/apis/drive/v3
    # https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
    # https://groups.google.com/forum/#!forum/risky-access-by-unreviewed-apps

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
            'max_results': 1,
            'folder_path': 'obs/terminal/'
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
            },
            '.folder_path': {
                'must_not_contain': [ '[^\\w\\-\\./]', '^\\.', '\\.$', '^/', '//' ]
            }
        },
        'metadata': {
            'record_optimal_bytes': 10000 * 1024,
            'file_object': {}
        }
    }
    
    def __init__(self, access_token, collection_name=''):
        
        '''
            a method to initialize the driveClient class
            
        :param access_token: string with oauth2 access token for users account
        :param collection_name: [optional] string with name of collection for import
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
    
    # construct access token
        self.access_token = access_token
        
    # construct drive client
        import httplib2
        from googleapiclient import discovery
        from oauth2client.client import AccessTokenCredentials
        google_credentials = AccessTokenCredentials(self.access_token, 'my-user-agent/1.0')
        google_http = httplib2.Http()
        google_http = google_credentials.authorize(google_http)
        google_drive = discovery.build('drive', 'v3', http=google_http)
        self.drive = google_drive.files()
    
    # construct collection properties
        self.permissions_write = True
        self.permissions_content = True
        self.drive_space = 'drive'
        self.space_id = ''
        if collection_name:
            self.collection_name = collection_name
        else:
            self.collection_name = 'My Drive'
    
    # construct file object
        from labpack import __module__
        from jsonmodel.loader import jsonLoader
        drive_rules = jsonLoader(__module__, 'storage/google/drive-rules.json')
        self.object_file = drive_rules['file_object']
        
    # validate access token
        self._validate_token()
        
    def _validate_token(self):
        
        ''' a method to validate active access token '''
        
        title = '%s._validate_token' % self.__class__.__name__
    
    # construct access token url
        import requests
        url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % self.access_token
    
    # retrieve access token details
        try:
            token_details = requests.get(url).json()
        except:
            raise DriveConnectionError(title)
        if 'error' in token_details.keys():
            raise ValueError('access_token for google drive account is %s' % token_details['error_description'])
    
    # determine collection space
    # https://developers.google.com/drive/v3/web/about-organization
        if 'scope' in token_details.keys():
            service_scope = token_details['scope']
            if service_scope.find('drive.appfolder') > -1:
                self.drive_space = 'appDataFolder'
                if not self.collection_name:
                    self.collection_name = 'App Data Folder'
            elif service_scope.find('drive.photos.readonly') > -1:
                self.drive_space = 'photos'
                if not self.collection_name:
                    self.collection_name = 'Photos'
    
    # determine permissions
    # https://developers.google.com/drive/v3/web/about-auth
            if service_scope.find('readonly') > -1:
                self.permissions_write = False
            if service_scope.find('readonly.metadata') > -1:
                self.permissions_content = False
          
    # TODO refresh token
        if 'expires_in' in token_details.keys():
            from time import time
            expiration_date = time() + token_details['expires_in']
        if 'issued_to' in token_details.keys():
            client_id = token_details['issued_to']
    
        return token_details
    
    def _get_id(self, file_path):
        
        ''' a helper method for retrieving id of file or folder '''
        
        title = '%s._get_id' % self.__class__.__name__
        
    # construct request kwargs
        list_kwargs = {
            'spaces': self.drive_space,
            'fields': 'files(id, parents)'
        }
    
    # determine path segments
        path_segments = file_path.split(os.sep)
        
    # walk down parents to file name
        parent_id = ''
        empty_string = ''
        while path_segments:
            walk_query = "name = '%s'" % path_segments.pop(0)
            if parent_id:
                walk_query += "and '%s' in parents" % parent_id
            list_kwargs['q'] = walk_query
            try:
                response = self.drive.list(**list_kwargs).execute()
            except:
                raise DriveConnectionError(title)
            file_list = response.get('files', [])
            if file_list:
                if path_segments:
                    parent_id = file_list[0].get('id')
                else:
                    file_id = file_list[0].get('id')
                    return file_id, parent_id
            else:
                return empty_string, empty_string
    
    def _get_space(self):
        
        ''' a helper method to retrieve id of drive space '''
        
        title = '%s._space_id' % self.__class__.__name__
        list_kwargs = {
            'q': "'%s' in parents" % self.drive_space,
            'spaces': self.drive_space,
            'fields': 'files(name, parents)',
            'pageSize': 1
        }
        try:
            response = self.drive.list(**list_kwargs).execute()
        except:
            raise DriveConnectionError(title)
        for file in response.get('files',[]):
            self.space_id = file.get('parents')[0]
            break
        return self.space_id
  
    def _get_data(self, file_id):
    
        ''' a helper method for retrieving the byte data of a file '''
        
        title = '%s._get_data' % self.__class__.__name__
        
    # request file data
        try:
            record_data = self.drive.get_media(fileId=file_id).execute()
        except:
            raise DriveConnectionError(title)
        
        return record_data
        
    def _get_metadata(self, file_id, metadata_fields=''):
        
        ''' a helper method for retrieving the metadata of a file '''
        
        title = '%s._get_metadata' % self.__class__.__name__
        
    # construct fields arg
        if not metadata_fields:
            metadata_fields = ','.join(self.object_file.keys())
        else:
            field_list = metadata_fields.split(',')
            for field in field_list:
                if not field in self.object_file.keys():
                    raise ValueError('%s(metadata_fields="%s") is not a valid drive file field' % (title, field))
    
    # send request
        try:
            metadata_details = self.drive.get(fileId=file_id, fields=metadata_fields).execute()
        except:
            raise DriveConnectionError(title)
        
        return metadata_details
        
    def _list_directory(self, folder_id=''):
    
        ''' a generator method for listing the contents of a directory '''
        
        title = '%s._list_directory' % self.__class__.__name__
        
    # construct default response
        file_list = []
    
    # construct request kwargs
        list_kwargs = {
            'spaces': self.drive_space,
            'fields': 'nextPageToken, files(id, name, parents, mimeType)'
        }
    
    # add query field for parent
        if folder_id:
            list_kwargs['q'] = "'%s' in parents" % folder_id
    
    # retrieve space id
        if not self.space_id:
            self._get_space()
        
    # send request
        page_token = 1
        while page_token:
            try:
                response = self.drive.list(**list_kwargs).execute()
            except:
                raise DriveConnectionError(title)
        
        # populate list from response
            results = response.get('files', [])
            for file in results:
                if not folder_id and file.get('parents', [])[0] != self.space_id:
                    pass
                else:
                    yield file.get('id', ''), file.get('name', ''), file.get('mimeType', '')
    
        # get page token
            page_token = response.get('nextPageToken', None)
            if page_token:
                list_kwargs['pageToken'] = page_token
        
        return file_list
      
    def _walk(self, root_path='', root_id=''):
        
        ''' a generator method which walks the file structure of the dropbox collection '''
        
        title = '%s._walk' % self.__class__.__name__
        
        if root_id:
            pass
        elif root_path:
            root_id, root_parent = self._get_id(root_path)
        for file_id, name, mimetype in self._list_directory(root_id):
            file_path = os.path.join(root_path, name)
            if mimetype == 'application/vnd.google-apps.folder':
                for path, id in self._walk(root_path=file_path, root_id=file_id):
                    yield path, id
            else:
                yield file_path, file_id
    
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
    
    # verify permissions
        if not self.permissions_write:
            raise Exception('%s requires an access_token with write permissions.' % title)
    
    # retrieve file id
        file_id, parent_id = self._get_id(record_key)
        
    # check overwrite condition
        if file_id:
            if overwrite:
                try:
                    self.drive.delete(fileId=file_id).execute()
                except:
                    raise DriveConnectionError(title)
            else:
                return False
    
    # # check size of file
    #     import sys
    #     record_optimal = self.fields.metadata['record_optimal_bytes']
    #     record_size = sys.getsizeof(record_data)
    #     error_prefix = '%s(record_key="%s", record_data=b"...")' % (title, record_key)
    #     if record_size > record_optimal:
    #         print('[WARNING] %s exceeds optimal record data size of %s bytes.' % (error_prefix, record_optimal))
            
    # prepare file body
        from googleapiclient.http import MediaInMemoryUpload
        media_body = MediaInMemoryUpload(body=record_data, resumable=True)
        
    # determine path segments
        path_segments = record_key.split(os.sep)
        
    # construct upload kwargs
        create_kwargs = {
            'body': {
                'name': path_segments.pop()
            },
            'media_body': media_body,
            'fields': 'id'
        }
    
    # walk through parent directories
        parent_id = ''
        if path_segments:
        
        # construct query and creation arguments
            walk_folders = True
            folder_kwargs = {
                'body': {
                    'name': '',
                    'mimeType' : 'application/vnd.google-apps.folder'
                },
                'fields': 'id'
            }
            query_kwargs = {
                'spaces': self.drive_space,
                'fields': 'files(id, parents)'
            }
            while path_segments:
                folder_name = path_segments.pop(0)
                folder_kwargs['body']['name'] = folder_name
        
        # search for folder id in existing hierarchy
                if walk_folders:
                    walk_query = "name = '%s'" % folder_name
                    if parent_id:
                        walk_query += "and '%s' in parents" % parent_id
                    query_kwargs['q'] = walk_query
                    try:
                        response = self.drive.list(**query_kwargs).execute()
                    except:
                        raise DriveConnectionError(title)
                    file_list = response.get('files', [])
                else:
                    file_list = []
                if file_list:
                    parent_id = file_list[0].get('id')
        
        # or create folder
        # https://developers.google.com/drive/v3/web/folder
                else:
                    try:
                        if not parent_id:
                            if self.drive_space == 'appDataFolder':
                                folder_kwargs['body']['parents'] = [ self.drive_space ]
                            else:
                                del folder_kwargs['body']['parents']
                        else:
                            folder_kwargs['body']['parents'] = [parent_id]
                        response = self.drive.create(**folder_kwargs).execute()
                        parent_id = response.get('id')
                        walk_folders = False
                    except:
                        raise DriveConnectionError(title)
    
    # add parent id to file creation kwargs
        if parent_id:
            create_kwargs['body']['parents'] = [parent_id]
        elif self.drive_space == 'appDataFolder':
            create_kwargs['body']['parents'] = [self.drive_space] 
    
    # modify file time
        import re
        if re.search('\\.drep$', create_kwargs['body']['name']):
            from labpack.records.time import labDT
            drep_time = labDT.fromEpoch(1).isoformat()
            create_kwargs['body']['modifiedTime'] = drep_time
        elif last_modified:
            from labpack.records.time import labDT
            mod_time = labDT.fromEpoch(last_modified).isoformat()
            create_kwargs['body']['modifiedTime'] = mod_time
            
    # send create request
        try:
            self.drive.create(**create_kwargs).execute()
        except:
            raise DriveConnectionError(title)
        
        return True
        
    def exists(self, record_key):
        
        ''' 
            a method to determine if a record exists in collection

        :param record_key: string with key of record
        :return: boolean indicating file existence
        '''
        
        title = '%s.exists' % self.__class__.__name__
    
    # validate inputs
        input_fields = {
            'record_key': record_key
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct request kwargs
        list_kwargs = {
            'spaces': self.drive_space,
            'fields': 'files(id)'
        }
    
    # retrieve file id
        file_id, parent_id = self._get_id(record_key)
        if file_id:
            return True
        return False
            
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

    # verify permissions
        if not self.permissions_write:
            raise Exception('%s requires an access_token with write permissions.' % title)
    
    # retrieve file id
        file_id, parent_id = self._get_id(record_key)
        
    # check overwrite condition
        if file_id:
            if overwrite:
                try:
                    self.drive.delete(fileId=file_id).execute()
                except:
                    raise DriveConnectionError(title)
            else:
                raise Exception('%s(record_key="%s") already exists. To overwrite, set overwrite=True' % (title, record_key))
    
    # check size of file
        import sys
        record_optimal = self.fields.metadata['record_optimal_bytes']
        record_size = sys.getsizeof(record_data)
        error_prefix = '%s(record_key="%s", record_data=b"...")' % (title, record_key)
        if record_size > record_optimal:
            print('[WARNING] %s exceeds optimal record data size of %s bytes.' % (error_prefix, record_optimal))
            
    # encrypt data
        if secret_key:
            from labpack.encryption import cryptolab
            record_data, secret_key = cryptolab.encrypt(record_data, secret_key)

    # prepare file body
        from googleapiclient.http import MediaInMemoryUpload
        media_body = MediaInMemoryUpload(body=record_data, resumable=True)
        
    # determine path segments
        path_segments = record_key.split(os.sep)
        
    # construct upload kwargs
        create_kwargs = {
            'body': {
                'name': path_segments.pop()
            },
            'media_body': media_body,
            'fields': 'id'
        }
    
    # walk through parent directories
        parent_id = ''
        if path_segments:
        
        # construct query and creation arguments
            walk_folders = True
            folder_kwargs = {
                'body': {
                    'name': '',
                    'mimeType' : 'application/vnd.google-apps.folder'
                },
                'fields': 'id'
            }
            query_kwargs = {
                'spaces': self.drive_space,
                'fields': 'files(id, parents)'
            }
            while path_segments:
                folder_name = path_segments.pop(0)
                folder_kwargs['body']['name'] = folder_name
        
        # search for folder id in existing hierarchy
                if walk_folders:
                    walk_query = "name = '%s'" % folder_name
                    if parent_id:
                        walk_query += "and '%s' in parents" % parent_id
                    query_kwargs['q'] = walk_query
                    try:
                        response = self.drive.list(**query_kwargs).execute()
                    except:
                        raise DriveConnectionError(title)
                    file_list = response.get('files', [])
                else:
                    file_list = []
                if file_list:
                    parent_id = file_list[0].get('id')
        
        # or create folder
        # https://developers.google.com/drive/v3/web/folder
                else:
                    try:
                        if not parent_id:
                            if self.drive_space == 'appDataFolder':
                                folder_kwargs['body']['parents'] = [ self.drive_space ]
                            else:
                                del folder_kwargs['body']['parents']
                        else:
                            folder_kwargs['body']['parents'] = [parent_id]
                        response = self.drive.create(**folder_kwargs).execute()
                        parent_id = response.get('id')
                        walk_folders = False
                    except:
                        raise DriveConnectionError(title)
    
    # add parent id to file creation kwargs
        if parent_id:
            create_kwargs['body']['parents'] = [parent_id]
        elif self.drive_space == 'appDataFolder':
            create_kwargs['body']['parents'] = [self.drive_space] 
    
    # modify file time
        import re
        if re.search('\\.drep$', file_name):
            from labpack.records.time import labDT
            drep_time = labDT.fromEpoch(1).isoformat()
            create_kwargs['body']['modifiedTime'] = drep_time
            
    # send create request
        try:
            self.drive.create(**create_kwargs).execute()
        except:
            raise DriveConnectionError(title)
        
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

    # verify permissions
        if not self.permissions_content:
            raise Exception('%s requires an access_token with file content permissions.' % title)
            
    # retrieve file id
        file_id, parent_id = self._get_id(record_key)
        if not file_id:
            raise Exception('%s(record_key=%s) does not exist.' % (title, record_key))
    
    # request file data
        try:
            record_data = self.drive.get_media(fileId=file_id).execute()
        except:
            raise DriveConnectionError(title)
    
    # retrieve data from response
    #     import io
    #     from googleapiclient.http import MediaIoBaseDownload
    #     file_header = io.BytesIO
    #     record_data = MediaIoBaseDownload(file_header, response)
    #     done = False
    #     while not done:
    #         status, done = record_data.next_chunk()
    
    # TODO export google document to other format
            
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
            "equal_to": "",
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
            a method to list keys in the google drive collection

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
        for file_path, file_id in self._walk(root_path):
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
        file_id, parent_id = self._get_id(record_key)
        if not file_id:
            exit_msg = '%s does not exist.' % record_key
            return exit_msg
            
    # remove file
        try:
            self.drive.delete(fileId=file_id).execute()
        except:
            raise DriveConnectionError(title)

    # determine file directory
        current_dir = os.path.split(record_key)[0]
        
    # remove empty parent folders
        try:
            while current_dir:
                folder_id, parent_id = self._get_id(current_dir)
                count = 0
                for id, name, mimetype in self._list_directory(folder_id):
                    count += 1
                    break
                if count:
                    self.drive.delete(fileId=folder_id).execute()
                    current_dir = os.path.split(current_dir)[0]
                else:
                    break
        except:
            raise DriveConnectionError(title)

    # return exit message
        exit_msg = '%s has been deleted.' % record_key
        return exit_msg
    
    def remove(self):
        
        ''' 
            a method to remove all records in the collection

        NOTE:   this method removes all the files in the collection, but the
                collection folder itself created by oauth2 cannot be removed.
                only the user can remove access to the app folder
                
        :return: string with confirmation of deletion
        '''

        title = '%s.remove' % self.__class__.__name__
    
    # get contents of root
        for id, name, mimetype in self._list_directory():
            try:
                self.drive.delete(fileId=id).execute()
            except Exception as err:
                if str(err).find('File not found') > -1:
                    pass
                else:
                    raise DriveConnectionError(title)
    
    # return outcome
        insert = 'collection'
        if self.collection_name:
            insert = self.collection_name
        exit_msg = 'Contents of %s will be removed from Google Drive.' % insert
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
        for file_path, file_id in self._walk():
            path_segments = file_path.split(os.sep)
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')
            
    # retrieve data and metadata
            try:
                record_data = self.drive.get_media(fileId=file_id).execute()
            except:
                raise DriveConnectionError(title)
            try:
                file = self.drive.get(fileId=file_id, fields='modifiedTime').execute()
                client_modified = file.get('modifiedTime', '')
            except:
                raise DriveConnectionError(title)
            
    # import record into storage client
            last_modified = 0.0
            if client_modified:
                from labpack.records.time import labDT
                last_modified = labDT.fromISO(client_modified).epoch()
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

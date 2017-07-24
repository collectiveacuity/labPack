__author__ = 'rcj1492'
__created__ = '2017.07'
__license__ = 'MIT'

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

    # https://developers.google.com/api-client-library/python/apis/drive/v3
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
            'record_optimal_bytes': 10000 * 1024
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
        self.drive_space = 'drive'
        if collection_name:
            self.collection_name = collection_name
        else:
            self.collection_name = 'My Drive'
    
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
            raise ValueError('access_token for driveClient is %s' % token_details['error_description'])
    
    # determine collection space
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
    
    # determine write permissions
            if service_scope.find('readonly') > -1:
                self.permissions_write = False
                
    # refresh token
        if 'expires_in' in token_details.keys():
            from time import time
            expiration_date = time() + token_details['expires_in']
        if 'issued_to' in token_details.keys():
            client_id = token_details['issued_to']
        
        return token_details
    
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
    
    # construct request kwargs
        list_kwargs = {
            'spaces': self.drive_space,
            'fields': 'files(id, name)'
        }
    
    # determine path segments
        path_segments = record_key.split(os.sep)
        
    # add query field
        query_string = "name = '%s'" % path_segments.pop()
        for segment in path_segments:
            query_string += "and '%s' in parents" % segment
        list_kwargs['q'] = query_string
        
    # send request
        try:
            response = self.drive.list(**list_kwargs).execute()
        except:
            raise DriveConnectionError(title)
    
    # interpret response
        empty_string = ''
        file_list = response.get('files', [])
        if file_list:
            file_id = file_list[0].get('id')
            return file_id
        else:
            return empty_string
    
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
            
    # check overwrite exception
        if not overwrite:
            if self.exists(record_key):
                raise Exception('%s(record_key="%s") already exists. To overwrite, set overwrite=True' % (title, record_key))
    
    # check size of file
        import sys
        record_optimal = self.fields.metadata['record_optimal_size']
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
                'name': path_segments.pop(),
                'parents': []
            },
            'media_body': media_body,
            'fields': 'id'
        }
    
    # add parents
        if self.drive_space == 'appDataFolder':
            create_kwargs['body']['parents'].append(self.drive_space)
        for segment in path_segments:
            create_kwargs['body']['parents'].append(segment)
        if not create_kwargs['body']['parents']:
            del create_kwargs['body']['parents']
        
    # modify file time
        import re
        if re.search('\\.drep$', file_name):
            from labpack.records.time import labDT
            drep_time = labDT.fromEpoch(1).isoformat()
            create_kwargs['body']['modifiedTime'] = drep_time
    
    # send create request
        try:
            response = self.drive.create(**create_kwargs).execute()
        except:
            raise DriveConnectionError(title)
        
        return record_key
    
    def test(self):
        
        test_id = '1dIYUS4HI20mkNr-Fut2EILXJSHdIOXVltJahMSV-xuto'
        
        list_kwargs = {
            'spaces': self.drive_space,
            'fields': 'nextPageToken, files(id, name)'
        }
    
    # add query field
        
    
    # send request
        response = self.drive.list(**list_kwargs).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        # items = results.get('items', [])
        # if not items:
        #     print('No files found.')
        # else:
        #     print('Files:')
        #     for item in items:
        #         print('{0} ({1})'.format(item['title'], item['id']))
                
            
if __name__ == '__main__':
    
# initialize client
    import pytest
    from pprint import pprint
    from labpack.records.settings import load_settings
    google_tokens = load_settings('../../../../cred/tokens/google-drive.yaml')
    access_token = google_tokens['google_drive_access_token']
    drive_client = driveClient(access_token, 'Unit Test')

# construct test records
    import json
    from hashlib import md5
    from labpack.compilers import drep
    secret_key = 'upside'
    test_record = {
        'dt': 1474509314.419702,
        'deviceID': '2Pp8d9lpsappm8QPv_Ps6cL0'
    }
    test_data = open('../../../data/test_voice.ogg', 'rb').read()
    data_key = 'lab/voice/unittest.ogg'
    data_key = 'unittest.ogg'
    record_data = json.dumps(test_record).encode('utf-8')
    record_key = 'lab/device/unittest.json'
    drep_data = drep.dump(test_record, secret_key)
    drep_key = 'lab/device/unittest.drep'

# test save method
    old_hash = md5(test_data).digest()
    # file_id = drive_client.save(data_key, test_data, secret_key=secret_key)
#     drive_client.save(record_key, record_data)
#     drive_client.save(drep_key, drep_data)
    # assert drive_client.exists(drep_key)
    # assert not drive_client.exists('notakey')

    test_output = drive_client.exists(data_key)
    print(test_output)   
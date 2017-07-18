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
            'optimal_file_size': 150000000
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
    
    # construct dropbox client
        import httplib2
        from apiclient import discovery
        from oauth2client.client import AccessTokenCredentials
        google_credentials = AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        google_http = httplib2.Http()
        google_http = google_credentials.authorize(google_http)
        self.drive = discovery.build('drive', 'v3', http=google_http)
    
    # construct collection name
        if collection_name:
            self.collection_name = collection_name

    def test(self):
        
        results = self.drive.files().list(spaces='appDataFolder').execute()
        items = results.get('items', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['title'], item['id']))
            
if __name__ == '__main__':
    
# initialize client
    import pytest
    from pprint import pprint
    from labpack.records.settings import load_settings
    google_tokens = load_settings('../../../../cred/tokens/google-drive.yaml')
    access_token = google_tokens['google_drive_access_token']
    # import requests
    # url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    # print(requests.get(url).json())
    drive_client = driveClient(access_token, 'Unit Test')
    drive_client.test()
    
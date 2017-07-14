__author__ = 'rcj1492'
__created__ = '2016.12'
__license__ = 'MIT'

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
            'record_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.ogg',
            'record_key_dict': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'record_key_path': '/home/user/.config/collective-acuity-labpack/user-data/obs/terminal',
            'record_key_comp': 'obs',
            'previous_key': 'obs/terminal/2016-03-17T17-24-51-687845Z.yaml',
            'record_body': { 'dT': 1458235492.311154 },
            'secret_key': '6tZ0rUexOiBcOse2-dgDkbeY',
            'prefix': 'obs/terminal',
            'delimiter': '2016-03-17T17-24-51-687845Z.yaml',
            'max_results': 1
        },
        'components': {
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
                'must_not_contain': [ '[\\t\\n\\r]' ]
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            }
        }
    }
    
    def __init__(self, access_token):
        
        '''
            a method to initialize the dropboxClient class
            
        :param access_token: string with oauth2 access token for users account
        '''    

        title = '%s.__init__' % self.__class__.__name__
    
    # construct input validation model
        self.fields = jsonModel(self._class_fields)
        
    # validate inputs
        input_fields = {
            'access_token': access_token
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # workaround for module namespace conflict
        from sys import path as sys_path
        sys_path.append(sys_path.pop(0))
        from dropbox import Dropbox
        sys_path.insert(0, sys_path.pop())
    
    # construct dropbox client
        self.dropbox = Dropbox(oauth2_access_token=access_token)
    
    def _walk(self):
        ''' an iterator method which walks the file structure of the dropbox collection '''
        title = '%s._walk' % self.__class__.__name__
        
        try:
            response = self.dropbox.files_list_folder(path='', recursive=True)
            for record in response.entries:
                yield record
            if response.has_more:
                while response.has_more:
                    response = self.dropbox.files_list_folder_continue(response.cursor)
                    for record in response.entries:
                        yield record
        except:
            raise DropboxConnectionError(title)
                
    
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
            'record_key': previous_key
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
    
    # iterate over dropbox files
        for file_path in self._walk():
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
        
        
        

if __name__ == '__main__':
    
# initialize client
    from pprint import pprint
    from labpack.records.settings import load_settings
    dropbox_tokens = load_settings('../../../cred/tokens/dropbox.yaml')
    access_token = dropbox_tokens['dropbox_access_token']
    dropbox_client = dropboxClient(access_token)

# test list
    record_list = dropbox_client.list()
    print(record_list)


    


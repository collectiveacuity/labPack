__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
from jsonmodel.validators import jsonModel
from labpack import __team__, __module__
from labpack.platforms.localhost import localhostClient

class appdataClient(object):

    ''' a class of methods for managing file storage on local device in app data 

        NOTE:   appdataClient is designed to store byte data, so encoding (or 
                decoding) different types of file types must be handled by the
                application prior (or after) data is saved (or loaded)
    ''' 

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'collection_name': 'User Data',
            'root_path': '../data',
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
                'must_not_contain': [ '[\\t\\n\\r]' ]
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            }
        }
    }

    def __init__(self, collection_name='', prod_name='', org_name='', root_path=''):

        ''' initialization method of appdata client class

        :param collection_name: [optional] string with name of collection to store records
        :param prod_name: [optional] string with name of application product
        :param org_name: [optional] string with name of organization behind product
        :param root_path: [optional] string with path to root of collections (defaults to user home)
        '''

        title = '%s.__init__' % self.__class__.__name__
        
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
    
    # construct collection name
        from copy import deepcopy
        self.collection_name = deepcopy(collection_name)

    # construct app folder
        if not root_path:
            self.app_folder = self.localhost.app_data(org_name=org_name, prod_name=prod_name)
        else:
            root_path = self.fields.validate(root_path, '.root_path')
            if os.path.exists(root_path):
                if not os.path.isdir(root_path):
                    raise ValueError('%s(root_path="%s") is an existing file.' % (title, root_path))
            self.app_folder = os.path.abspath(root_path)

    # validate existence of file data folder in app data (or create)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            collection_name = collection_name.replace(' ', '-').lower()
        self.collection_folder = os.path.join(self.app_folder, collection_name)
        self.fields.validate(self.collection_folder, '.record_key_path')
        if not os.path.exists(self.collection_folder):
            os.makedirs(self.collection_folder)

    def _delete(self, _file_path, _method_title, _record_key):

        '''
            a helper method for non-blocking deletion of files
            
        :param _file_path: string with path to file to remove 
        :param _method_title: string with name of method calling _delete
        :param _record_key: string with name of record key to delete
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
                    raise Exception('%s failed to delete %s' % (_method_title, _record_key))

        os._exit(0)
    
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
        
    # construct and validate file path
        file_path = os.path.join(self.collection_folder, record_key)

    # check overwrite exception
        from os import path, makedirs
        if not overwrite:
            if path.exists(file_path):
                return False

    # create directories in path to file
        file_root, file_name = path.split(file_path)
        if file_root:
            if not path.exists(file_root):
                makedirs(file_root)
                
    # save file
        with open(file_path, 'wb') as f:
            f.write(record_data)
            f.close()
    
    # erase file date from drep files
        import re
        if re.search('\\.drep$', file_name):
            from os import utime
            file_time = 1
            utime(file_path, times=(file_time, file_time))
        elif last_modified:
            from os import utime
            utime(file_path, times=(last_modified, last_modified))
        
        return True
    
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
    
    # construct path to file
        from os import path
        file_path = path.join(self.collection_folder, record_key)

    # validate existence of file
        if not path.exists(file_path):
            return False
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
        file_path = os.path.join(self.collection_folder, record_key)
        file_path = self.fields.validate(file_path, '.record_key_path')
        file_root, file_name = os.path.split(file_path)
        self.fields.validate(file_name, '.record_key_comp')
        while file_root != self.collection_folder:
            file_root, path_node = os.path.split(file_root)
            self.fields.validate(path_node, '.record_key_comp')

    # check overwrite exception
        from os import path, makedirs
        if not overwrite:
            if path.exists(file_path):
                raise Exception('%s(record_key="%s") already exists. To overwrite, set overwrite=True' % (title, record_key))

    # create directories in path to file
        file_root, file_node = path.split(file_path)
        if file_root:
            if not path.exists(file_root):
                makedirs(file_root)
            
    # encrypt data
        if secret_key:
            from labpack.encryption import cryptolab
            record_data, secret_key = cryptolab.encrypt(record_data, secret_key)
    
    # save file
        with open(file_path, 'wb') as f:
            f.write(record_data)
            f.close()
    
    # erase file date from drep files
        import re
        if re.search('\\.drep$', file_name):
            from os import utime
            file_time = 1
            utime(file_path, times=(file_time, file_time))

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

    # construct path to file
        from os import path
        file_path = path.join(self.collection_folder, record_key)

    # validate existence of file
        if not path.exists(file_path):
            raise Exception('%s(record_key=%s) does not exist.' % (title, record_key))

    # open file and read data
        record_data = open(file_path, 'rb').read()
    
    # decrypt (if necessary)
        if secret_key:
            from labpack.encryption import cryptolab
            record_data = cryptolab.decrypt(record_data, secret_key)
    
        return record_data
            
    def conditional_filter(self, path_filters):

        ''' a method to construct a conditional filter function for class list method

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

    def list(self, prefix='', delimiter='', filter_function=None, max_results=1, reverse_search=True, previous_key=''):

        ''' 
            a method to list keys in the collection

        :param prefix: string with prefix value to filter results
        :param delimiter: string with value which results must not contain (after prefix)
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
        root_segments = self.collection_folder.split(os.sep)
        if previous_key:
            previous_key = os.path.join(self.collection_folder, previous_key)

    # determine root path
        root_path = self.collection_folder
        if prefix:
            from os import path
            file_root, file_name = path.split(prefix)
            root_path = path.join(root_path, file_root)
            
    # walk collection folder to find files
        for file_path in self.localhost.walk(root_path, reverse_search, previous_key):
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')

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
        key_arg = '%s(record_key="%s")' % (title, record_key)

    # validate inputs
        record_key = self.fields.validate(record_key, '.record_key')

    # construct path to file
        file_path = os.path.join(self.collection_folder, record_key)

    # validate existence of file
        if not os.path.exists(file_path):
            exit_msg = '%s does not exist.' % record_key
            return exit_msg
    
    # delete file asynchronously
    #     if non_blocking:
    #         self._delete(file_path, title, record_key)
    #         exit_msg = '%s will be deleted.' % record_key
    #         return exit_msg
        
    # remove file
        current_dir = os.path.split(file_path)[0]
        try:
            os.remove(file_path)
        except:
            raise Exception('%s failed to delete %s' % (key_arg, record_key))

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

        exit_msg = '%s has been deleted.' % record_key
        return exit_msg
    
    def remove(self):

        ''' 
            a method to remove collection and all records in the collection

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

        exit_msg = '%s collection has been removed from app data.' % self.collection_folder
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
        root_segments = self.collection_folder.split(os.sep)
        count = 0
        skipped = 0
        for file_path in self.localhost.walk(self.collection_folder):
            path_segments = file_path.split(os.sep)
            for i in range(len(root_segments)):
                del path_segments[0]
            record_key = os.path.join(*path_segments)
            record_key = record_key.replace('\\','/')
            
    # read and save files
            record_data = open(file_path, 'rb').read()
            last_modified = os.path.getmtime(file_path)
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
    
__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

import os
from jsonmodel.validators import jsonModel
from socket import gethostname, gethostbyname

class osClient(object):

    ''' a class of methods for retrieving local os properties '''

    def __init__(self):

        ''' initialization method for osClient class '''

    # construct empty methods
        self.sysname = ''
        self.nodename = ''
        self.release = ''
        self.version = ''
        self.machine = ''
        self.processor = ''

    # reconstruct class methods from system call
        from platform import uname
        local_os = uname()
        if local_os.system:
            self.sysname = local_os.system
        if local_os.node:
            self.nodename = local_os.node
        if local_os.release:
            self.release = local_os.release
        if local_os.version:
            self.version = local_os.version
        if local_os.machine:
            self.machine = local_os.machine
        if local_os.version:
            self.processor = local_os.processor

        # from os import uname
        # local_os = uname()
        # if local_os.sysname:
        #     self.sysname = local_os.sysname
        # if local_os.nodename:
        #     self.nodename = local_os.nodename
        # if local_os.release:
        #     self.release = local_os.release
        # if local_os.version:
        #     self.release = local_os.version
        # if local_os.machine:
        #     self.machine = local_os.machine
        
class localhostClient(object):

    ''' a class of methods to interact with the localhost '''

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'walk_root': '../',
            'list_root': '../',
            'max_results': 1,
            'previous_file': '/home/user/.config/collective-acuity-labpack/user-data/test.json',
            'file_path': '/home/user/.config/collective-acuity-labpack/user-data/test.json',
            'query_root': '../',
            'metadata_filters': [ {
                '.file_name': {},
                '.file_path': {},
                '.file_size': {},
                '.create_date': {},
                '.update_date': {},
                '.access_date': {}
            } ]
        },
        'components': {
            '.org_name': {
                'must_not_contain': ['/']
            },
            '.prod_name': {
                'must_not_contain': ['/']
            },
            '.max_results': {
                'min_value': 1,
                'integer_data': True
            }
        }
    }

    def __init__(self):

        ''' a method to initialize a client class to interact with the localhost '''

    # construct class field input validation property
        self.fields = jsonModel(self._class_fields)

    # retrieve operating system from localhost
        self.os = osClient()

    # TODO: determine file system and parameters
    # TODO: request latest info from
    # https://en.wikipedia.org/wiki/Comparison_of_file_systems#Limits

    # retrieve IP from system
        self.os.nodename = gethostname()
        self.ip = gethostbyname(self.os.nodename)

    # retrieve environment variables from system
        self.environ = dict(os.environ.items())

    # retrieve path to user home
        self.home = ''
        if self.os.sysname == 'Windows':
            env_username = os.environ.get('USERNAME')
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            app_data = ''
            if os.environ.get('APPDATA'):
                app_data = os.environ.get('APPDATA')
            if xp_pattern.findall(app_data):
                self.home = 'C:\\Documents and Settings\\%s' % env_username
            else:
                self.home = 'C:\\Users\\%s' % env_username
        elif self.os.sysname in ('Linux', 'FreeBSD', 'Solaris', 'Darwin'):
            self.home = os.path.expanduser('~')

    # retrieve path to shell configs
        self.bash_config = ''
        self.sh_config = ''
        if self.os.sysname == 'Windows':
            bash_config = '.bash_profile'
            sh_config = ''
        else:
            bash_config = '.bashrc'
            sh_config = '.cshrc'
        if bash_config:
            self.bash_config = os.path.join(self.home, bash_config)
        if sh_config:
            self.sh_config = os.path.join(self.home, sh_config)
    # TODO check different terminal protocols

    # construct file record model property
        file_model = {
            'schema': {
                'file_name': 'test.json',
                'file_path': '/home/user/.config/collective-acuity-labpack/user-data/test.json',
                'file_size': 678,
                'create_date': 1474509314.419702,
                'update_date': 1474509314.419702,
                'access_date': 1474509314.419702
            },
            'components': {
                '.file_size': {
                    'integer_data': True
                }
            }
        }
        self.file_model = jsonModel(file_model)

    def app_data(self, org_name, prod_name):

        ''' a method to retrieve the os appropriate path to user app data

        # https://www.chromium.org/user-experience/user-data-directory

        :param org_name: string with name of product/service creator
        :param prod_name: string with name of product/service
        :return: string with path to app data
        '''

        __name__ = '%s.app_data' % self.__class__.__name__

    # validate inputs
        org_name = self.fields.validate(org_name, '.org_name')
        prod_name = self.fields.validate(prod_name, '.prod_name')

    # construct empty fields
        data_path = ''

    # construct path from os
        if self.os.sysname == 'Windows':
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            app_data = ''
            if os.environ.get('APPDATA'):
                app_data = os.environ.get('APPDATA')
            if xp_pattern.findall(app_data):
                data_path = '%s\\Local Settings\\Application Data\\%s\\%s' % (self.home, org_name, prod_name)
            else:
                data_path = '%s\\AppData\\Local\\%s\\%s' % (self.home, org_name, prod_name)

        elif self.os.sysname == 'Darwin':
            data_path = '%s/Library/Application Support/%s/%s/' % (self.home, org_name, prod_name)

        elif self.os.sysname in ('Linux', 'FreeBSD', 'Solaris'):
            org_format = org_name.replace(' ','-').lower()
            prod_format = prod_name.replace(' ', '-').lower()
            data_path = '%s/.config/%s-%s/' % (self.home, org_format, prod_format)

        return data_path

    def walk(self, walk_root='', reverse_order=False, previous_file=''):

        ''' a generator method of file paths on localhost from walk of directories

        :param walk_root: string with path from which to root walk of localhost directories
        :param reverse_order: boolean to determine alphabetical direction of walk
        :param previous_file: string with path of file after which to start walk
        :return: string with absolute path to file
        '''

        __name__ = '%s.walk(...)' % self.__class__.__name__

    # validate input
        input_kwargs = [walk_root, previous_file]
        input_names = ['.walk_root', '.previous_file']
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # validate that previous file exists
        file_exists = False
        previous_found = False
        if previous_file:
            if os.path.exists(previous_file):
                if os.path.isfile(previous_file):
                    file_exists = True
                    previous_file = os.path.abspath(previous_file)
            if not file_exists:
                err_msg = __name__.replace('...', 'previous_file="%s"' % previous_file)
                raise ValueError('%s must be a valid file.' % err_msg)

    # construct empty result
        file_path = ''

    # determine root for walk
        if walk_root:
            if not os.path.isdir(walk_root):
                err_msg = __name__.replace('...', 'walk_root="%s"' % walk_root)
                raise ValueError('%s msut be a valid directory.' % err_msg)
        else:
            walk_root = './'

    # walk directory structure to find files
        for current_dir, sub_dirs, dir_files in os.walk(walk_root):
            dir_files.sort()
            sub_dirs.sort()
            if reverse_order:
                sub_dirs.reverse()
                dir_files.reverse()
            if previous_file and not previous_found:
                key_path = previous_file.split(os.sep)
                current_path = os.path.abspath(current_dir)
                for i in range(len(current_path.split(os.sep))):
                    del key_path[0]
                if key_path:
                    if key_path[0] in sub_dirs:
                        path_index = sub_dirs.index(key_path[0])
                        sub_dirs[0:path_index] = []
                        dir_files = []
                    elif key_path[0] in dir_files:
                        file_index = dir_files.index(key_path[0]) + 1
                        dir_files[0:file_index] = []
                        previous_found = True

    # yield file path
            for file in dir_files:
                file_path = os.path.join(os.path.abspath(current_dir), file)
                yield file_path

    def metadata(self, file_path):

        ''' a method to retrieve the metadata of a file on the localhost

        :param file_path: string with path to file
        :return: dictionary with file properties
        '''

        __name__ = '%s.metadata(...)' % self.__class__.__name__

    # validate input
        self.fields.validate(file_path, '.file_path')
        file_exists = False
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                file_exists = True
        if not file_exists:
            err_msg = __name__.replace('...', 'file_path=%s' % file_path)
            raise ValueError('%s must be a valid file.' % err_msg)

    # construct metadata dictionary
        abs_path = os.path.abspath(file_path)
        file_stats = os.stat(file_path)
        file_metadata = {
            'path_segments': abs_path.split(os.sep),
            'file_name': os.path.split(abs_path)[1],
            'file_path': abs_path,
            'file_size': file_stats.st_size,
            'create_date': file_stats.st_ctime,
            'update_date': file_stats.st_mtime,
            'access_date': file_stats.st_atime
        }

        return file_metadata

    def conditional_filter(self, metadata_filters):

        ''' a method to construct a conditional filter function for the list method

        :param metadata_filters: list with query criteria dictionaries
        :return: filter_function object

            NOTE:   query criteria architecture

                    each item in the metadata filters list must be a dictionary
                    which is composed of one or more key names which represent the
                    dotpath to a metadata element of the record to be queried with a
                    key value that is a dictionary of conditional operators used to
                    test the value in the corresponding metadata field of the record.

                    eg. path_filters = [ { '.file_name': { 'must_contain': [ '^lab' ] } } ]

                    this example filter looks in the file tree that is walked for a
                    file which starts with the characters 'lab'. as a result, it will
                    match both the following:
                        log/unittests/test/20160912/lab.json
                        laboratory20160912.json

            NOTE:   the filter method uses a query filters list structure to represent
                    the disjunctive normal form of a logical expression. a record is
                    added to the results list if any query criteria dictionary in the
                    list evaluates to true. within each query criteria dictionary, all
                    declared conditional operators must evaluate to true.

                    in this way, the metadata_filters represents a boolean OR operator and
                    each criteria dictionary inside the list represents a boolean AND
                    operator between all keys in the dictionary.

            NOTE:   each query_criteria uses the architecture of query declaration in
                    the jsonModel.query method

            query_criteria = {
                '.file_name': {},
                '.file_path': {},
                '.file_size': {},
                '.create_date': {},
                '.update_date': {},
                '.access_date': {}
            }

            conditional operators for '.file_name' and '.file_path' fields:
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

            conditional operators for '.file_size', '.create_date', '.update_date', '.access_date':
                "discrete_values": [ 0.0 ],
                "excluded_values": [ 0.0 ],
                "greater_than": 0.0,
                "integer_data": false,
                "less_than": 0.0,
                "max_value": 0.0,
                "min_value": 0.0
        '''

    # validate input
        self.fields.validate(metadata_filters, '.metadata_filters')

    # construct function called by list function
        def query_function(**kwargs):
            file_metadata = {}
            for key, value in kwargs.items():
                if key in self.file_model.schema.keys():
                    file_metadata[key] = value
            for query_criteria in metadata_filters:
                if self.file_model.query(query_criteria, file_metadata):
                    return True
            return False

        return query_function

    def list(self, filter_function=None, list_root='', max_results=1, reverse_order=False, previous_file=''):

        ''' a method to list files on localhost from walk of directories

        :param filter_function: (keyword arguments) function used to filter results
        :param list_root: string with localhost path from which to root list of files
        :param max_results: integer with maximum number of results to return
        :param reverse_order: boolean to determine alphabetical direction of walk
        :param previous_file: string with absolute path of file to begin search after
        :return: list of file absolute path strings

            NOTE:   the filter_function must be able to accept keyword arguments and
                    return a value that can evaluate to true or false. while walking
                    the local file structure, the metadata for each file will be
                    fed to the filter function. if the function evaluates this input
                    and returns a true value the file will be included in the list
                    results.

                    fields produced by the metadata function are listed in the
                    self.file_model.schema
        '''

        __name__ = '%s.list(...)' % self.__class__.__name__

    # validate input
        input_kwargs = [list_root, max_results, previous_file]
        input_names = ['.list_root', '.max_results', '.previous_file']
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # validate filter function
        if filter_function:
            try:
                filter_function(**self.file_model.schema)
            except:
                err_msg = __name__.replace('...', 'filter_function=%s' % filter_function.__class__.__name__)
                raise TypeError('%s must accept key word arguments.' % err_msg)

    # validate that previous file exists
        file_exists = False
        if previous_file:
            if os.path.exists(previous_file):
                if os.path.isfile(previous_file):
                    file_exists = True
            if not file_exists:
                err_msg = __name__.replace('...', 'previous_file="%s"' % previous_file)
                raise ValueError('%s must be a valid file.' % err_msg)

    # construct empty results object
        results_list = []

    # determine root for walk
        if list_root:
            if not os.path.isdir(list_root):
                return results_list
        else:
            list_root = './'

    # walk directory structure to find files
        for file_path in self.walk(list_root, reverse_order, previous_file):
            if filter_function:
                file_metadata = self.metadata(file_path)
                if filter_function(**file_metadata):
                    results_list.append(file_path)
            else:
                results_list.append(file_path)

    # return results list
            if len(results_list) == max_results:
                return results_list

        return results_list

if __name__ == '__main__':
    os_client = osClient()
    localhost_client = localhostClient()
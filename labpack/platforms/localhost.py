__author__ = 'rcj1492'
__created__ = '2016.03'

from os import environ, path, walk, stat
from jsonmodel.validators import jsonModel
from subprocess import check_output

class localhostClient(object):

    '''
        a class of methods to interact with the localhost
    '''

    _class_fields = {
        'schema': {
            'org_name': 'Collective Acuity',
            'prod_name': 'labPack',
            'max_results': 1,
            'query_root': '../',
            'query_filters': [ {
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

    # construct class field input validation property
        self.fields = jsonModel(self._class_fields)

    # retrieve OS variable from system
        env_os = environ.get('OS')
        if not env_os:
            sys_command = 'uname -a'
            env_os = check_output(sys_command).decode('utf-8').replace('\n','')

    # determine OS from environment variable
        local_os = ''
        if 'Linux' in env_os:
            local_os = 'Linux'
        elif 'FreeBSD' in env_os:
            local_os = 'FreeBSD'
        elif 'Windows' in env_os:
            local_os = 'Windows'
        elif 'Darwin' in env_os:
            local_os = 'Mac'
        elif 'SunOS' in env_os:
            local_os = 'Solaris'
        self.os = local_os

    # retrieve USERNAME variable from system
        self.username = ''
        env_username = environ.get('USERNAME')
        if env_username:
            self.username = env_username

    # retrieve IP from system
        self.ip = 'localhost'
        if self.os in ('Linux', 'FreeBSD', 'Solaris'):
            try:
                sys_command = 'hostname -i'
                self.ip = check_output(sys_command).decode('utf-8').replace('\n', '')
            except:
                pass

    # retrieve path to user home
        self.home = ''
        if self.os == 'Windows':
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            app_data = ''
            if environ.get('APPDATA'):
                app_data = environ.get('APPDATA')
            if xp_pattern.findall(app_data):
                self.home = 'C:\\Documents and Settings\\%s' % self.username
            else:
                self.home = 'C:\\Users\\%s' % self.username
        elif self.os in ('Linux', 'FreeBSD', 'Solaris', 'Mac'):
            self.home = '~/'

    # construct file record model property
        file_model = {
            'schema': {
                'file_name': '',
                'file_path': '',
                'file_size': 0,
                'create_date': 0,
                'update_date': 0,
                'access_date': 0
            }
        }
        self.fileModel = jsonModel(file_model)

    def appData(self, org_name, prod_name):

        '''
            a method to retrieve the os appropriate path to user app data
            https://www.chromium.org/user-experience/user-data-directory

        :param org_name: string with name of product/service creator
        :param prod_name: string with name of product/service
        :return: string with path to app data
        '''

        __name__ = '%s.appData' % self.__class__.__name__

    # validate inputs
        org_name = self.fields.validate(org_name, '.org_name')
        prod_name = self.fields.validate(prod_name, '.prod_name')

    # construct empty fields
        data_path = ''

    # construct path from os
        if self.os == 'Windows':
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            app_data = ''
            if environ.get('APPDATA'):
                app_data = environ.get('APPDATA')
            if xp_pattern.findall(app_data):
                data_path = '%s\\Local Settings\\Application Data\\%s\\%s' % (self.home, org_name, prod_name)
            else:
                data_path = '%s\\AppData\\Local\\%s\\%s' % (self.home, org_name, prod_name)

        elif self.os == 'Mac':
            data_path = '%sLibrary/Application Support/%s/%s/' % (self.home, org_name, prod_name)

        elif self.os in ('Linux', 'FreeBSD', 'Solaris'):
            org_format = org_name.replace(' ','-').lower()
            prod_format = prod_name.replace(' ', '-').lower()
            data_path = '%s.config/%s-%s/' % (self.home, org_format, prod_format)

        return data_path

    def find(self, query_filters=None, query_root='', max_results=1, top_down=True):

        '''
            a method to find files on localhost based upon a variety of query criteria

        :param query_filters: list with query_criteria dictionaries
        :param query_root: string with path from which to root walk of localhost directories
        :param max_results: integer with maximum number of results to return
        :param top_down: boolean to determine direction of walk from top of root down branches
        :return: list of file path strings

            **NOTE: the query method uses a query filters list structure to represent
                    the disjunctive normal form of a logical expression. a record is
                    added to the results list if any query_criteria dictionary in the
                    list evaluates to true. within each query_criteria dictionary, all
                    declared conditional operators must evaluate to true.

            **NOTE: in this way, the query_filters represents a boolean OR operator and
                    the query_criteria represents a boolean AND operator between all
                    keys in the dictionary.

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


    # TODO: Look into declarative query language architecture instead

        __name__ = '%s.query' % self.__class__.__name__

    # validate input
        input_kwargs = [ query_filters, query_root, max_results ]
        input_names = [ '.query_filters', '.query_root', '.max_results' ]
        for i in range(len(input_kwargs)):
            if input_kwargs[i]:
                self.fields.validate(input_kwargs[i], input_names[i])

    # construct empty fields
        result_list = []
        if not query_filters:
            query_filters = [ {} ]

    # determine root for walk
        if query_root:
            if not path.isdir(query_root):
                return result_list
        else:
            query_root = './'

    # construct result function
        def _yield_results(query_filters, record_details):
            for query_criteria in query_filters:
                if self.fileModel.query(query_criteria, record_details):
                    return True
            return False

    # walk the local file index
        for current_dir, sub_dirs, dir_files in walk(query_root, topdown=top_down):
            for file in dir_files:
                file_source = path.join(path.abspath(current_dir), file)
                file_stats = stat(file_source)
                record_details = {
                    'file_path': path.abspath(current_dir),
                    'file_name': file,
                    'file_size': file_stats.st_size,
                    'create_date': file_stats.st_ctime,
                    'update_date': file_stats.st_mtime,
                    'access_date': file_stats.st_atime
                }

    # add qualifying file to results list
                if _yield_results(query_filters, record_details):
                    result_list.append(file_source)

    # return results list
                if len(result_list) == max_results:
                    return result_list

        return result_list

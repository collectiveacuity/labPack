__author__ = 'rcj1492'
__created__ = '2016.03'

from os import environ, path, walk
from jsonmodel.validators import jsonModel
from subprocess import check_output
from labpack import __team__, __module__

class localhostClient(object):

    def __init__(self):

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

    # construct class fields validator model
        class_fields = {
            'schema': {
                'org_name': 'Collective Acuity',
                'prod_name': 'labPack',
                'repo_name': 'User Data',
                'key_query': ['terminal'],
                'body_query': {'key': ['regex']},
                'results': 1,
                'query_root': '../'
            },
            'components': {
                '.org_name': {
                    'must_not_contain': ['/']
                },
                '.prod_name': {
                    'must_not_contain': ['/']
                },
                '.repo_name': {
                    'must_not_contain': ['/']
                },
                '.key_query': {
                    'min_size': 1
                },
                '.results': {
                    'min_value': 0,
                    'integer_only': True
                },
                '.body_query': {
                    'extra_fields': True,
                },
                '.body_query.key': {
                    'required_field': False,
                    'min_size': 1
                }
            }
        }
        self.validKwargs = jsonModel(class_fields)

    def appData(self, org_name, prod_name):

        '''
            a method to retrieve the os appropriate path to user app data

        :param org_name: string with name of product/service creator
        :param prod_name: string with name of product/service
        :return: string with path to app data
        '''

        __name__ = '%s.appData' % self.__class__.__name__

    # validate inputs
        org_name = self.validKwargs.validate(org_name, '.org_name')
        prod_name = self.validKwargs.validate(prod_name, '.prod_name')

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
    
    def repoData(self, repo_name, org_name='', prod_name=''):

        '''
            a method to retrieve the os appropriate path to an user app file repo

        :param repo_name: string with name of file repository folder
        :param org_name: string with name of product/service creator
        :param prod_name: string with name of product/service
        :return: string with path to app data
        '''

        __name__ = '%s.repoData' % self.__class__.__name__

    # validate inputs
        repo_name = self.validKwargs.validate(repo_name, '.repo_name')
        if org_name:
            org_name = self.validKwargs.validate(org_name, '.org_name')
        if prod_name:
            prod_name = self.validKwargs.validate(prod_name, '.prod_name')

    # construct path from os
        if not org_name:
            org_name = __team__
        if not prod_name:
            prod_name = __module__
        app_path = self.appData(org_name, prod_name)
        if self.os in ('Linux', 'FreeBSD', 'Solaris'):
            repo_name = repo_name.replace(' ', '-').lower()
        data_path = path.join(app_path, repo_name)
        
        return data_path

    def query(self, key_query=None, body_query=None, results=0, top_down=True, query_root=''):

        '''
            a method to find files from query parameters

        :param key_query: list of regex expressions
        :param body_query: dictionary of keys and values which are lists of regex
        :param results: integer of results to return
        :param top_down: boolean to direct search from root to the branches
        :param query_root: string with path of root folder
        :return: list of file paths
        '''

    # TODO: Look into declarative query language architecture instead

        __name__ = '%s.query' % self.__class__.__name__
        _key_arg = '%s(key_query=[...])' % __name__
        _body_arg = '%s(body_query={...})' % __name__

    # validate inputs
        if key_query:
            key_query = self.validKwargs.validate(key_query, '.key_query')
        if body_query:
            body_query = self.validKwargs.validate(body_query, '.body_query')
            for key, value in body_query.items():
                self.validKwargs.validate(value, '.body_query.key')
        if query_root:
            query_root = self.validKwargs.validate(query_root, '.query_root')
        results = self.validKwargs.validate(results, '.results')

    # construct empty fields
        result_list = []

    # determine results size
        if not results:
            results = 1000

    # compile regex patterns
        _key_query = []
        if key_query:
            import re
            for regex in key_query:
                _key_query.append(re.compile(regex))

    # determine root for walk
        if query_root:
            if not path.isdir(query_root):
                query_root = './'
        else:
            query_root = './'

    # walk the local file index
        for current_dir, sub_dirs, dir_files in walk(query_root, topdown=top_down):
            for file in dir_files:
                add_file = True

    # add files whose name match each regex expression in key query
                if _key_query:
                    for regex_pattern in _key_query:
                        if not regex_pattern.findall(file):
                            add_file = False

    # add qualifying file to results list
                if add_file:
                    result_list.append(path.join(path.abspath(current_dir), file))
                if len(result_list) == results:
                    return result_list

        return result_list

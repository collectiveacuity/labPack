__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from os import path, listdir
from re import compile
from labpack import __team__, __module__
from jsonmodel.validators import jsonModel
from labpack.platforms.localhost_client import localhostClient

class appdataClient(object):

    def __init__(self, folder_name='', org_name='', prod_name=''):

    # add localhost property
        self.localhost = localhostClient()

    # validate existence of user data folder in app data (or create)
        if not folder_name:
            folder_name = 'User Data'
        if not org_name:
            org_name = __team__
        if not prod_name:
            prod_name = __module__
        self.appFolder = self.localhost.appData(org_name=org_name, prod_name=prod_name)
        if self.localhost.os in ('Linux', 'FreeBSD', 'Solaris'):
            folder_name = folder_name.replace(' ', '-').lower()
        self.repoFolder = path.join(self.appFolder, folder_name)
        if not path.exists(self.repoFolder):
            from os import makedirs
            makedirs(self.repoFolder)

    # construct supported file type regex patterns
        class _regex_ext(object):
            def __init__(self):
                from re import compile
                self.json = compile('\.json$')
                self.yaml = compile('\.ya?ml$')
                self.jsongz = compile('\.json\.gz$')
                self.yamlgz = compile('\.ya?ml\.gz$')
                self.drep = compile('\.drep$')
                self.types = ['.json','.json.gz','.yaml','.yml','.yaml.gz','.yml.gz','.drep']
                self.names = ['json', 'yaml', 'jsongz', 'yamlgz', 'drep']
        self.ext = _regex_ext()

    # construct class fields validator model
        class_fields = {
            'schema': {
                'key_string': 'obs-terminal-2016-03-17T17-24-51-687845Z.yaml',
                'body_dict': { 'dT': 1458235492.311154 },
                'key_query': [ 'terminal' ],
                'body_query': { 'key': [ 'regex' ] },
                'results': 1
            },
            'components': {
                '.key_string': {
                    'must_not_contain': [ '[^\\w/\\-_\\.]' ],
                    'contains_either': [ '\\.json$', '\\.ya?ml$', '\\.json\\.gz$', '\\.ya?ml\\.gz$', '\\.drep$' ]
                },
                '.body_dict': {
                    'extra_fields': True
                },
                '.body_dict.dT': {
                    'required_field': False
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
        self.validInput = jsonModel(class_fields)

    def put(self, key_string, body_dict, override=True):

        '''
            a method to create a file in log folder

        :param key_string: string with name to assign file
        :param body_dict: dictionary with log data body
        :param override: boolean to overwrite files with same name
        :return: self
        '''

        __name__ = '%s.put' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)
        _body_arg = '%s(body_dict={...}' % {__name__}

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')
        body_dict = self.validInput.validate(body_dict, '.body_dict')

    # construct log file path
        log_path = ''
        log_data = ''.encode('utf-8')
        if self.ext.json.findall(key_string):
            import json
            log_path = path.join(self.repoFolder, key_string)
            log_data = json.dumps(body_dict).encode('utf-8')
        elif self.ext.yaml.findall(key_string):
            import yaml
            log_path = path.join(self.repoFolder, key_string)
            log_data = yaml.dump(body_dict).encode('utf-8')
        elif self.ext.jsongz.findall(key_string):
            import json
            from gzip import compress
            log_path = path.join(self.repoFolder, key_string)
            log_bytes = json.dumps(body_dict).encode('utf-8')
            log_data = compress(log_bytes)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            from gzip import compress
            log_path = path.join(self.repoFolder, key_string)
            log_bytes = yaml.dump(body_dict).encode('utf-8')
            log_data = compress(log_bytes)
        elif self.ext.drep.findall(key_string):
            from popuplab.compilers import drep
            log_path = path.join(self.repoFolder, key_string)
            private_key, log_data, drep_index = drep.dump(body_dict)

    # save details to log file
        if not override:
            if path.exists(log_path):
                raise Exception('%s already exists. To overwrite %s, set override=True' % (_key_arg, key_string))
        with open(log_path, 'wb') as f:
            f.write(log_data)
            f.close()

        return self

    def query(self, key_query=None, body_query=None, results=0, reverse=True):

        '''
            a method to find files from query parameters

        :param key_query: list of regex expressions
        :param body_query: dictionary of keys and values which are lists of regex
        :param results: integer of results to return
        :param reverse: boolean to search from last file in log folder first
        :return: list of file names
        '''

    # TODO: Look into declarative query language architecture instead

        __name__ = '%s.query' % self.__class__.__name__
        _key_arg = '%s(key_query=[...])' % __name__
        _body_arg = '%s(body_query={...})' % __name__

    # construct regex list for key_query
        if key_query:
            key_query = self.validInput.validate(key_query, '.key_query')
        if body_query:
            body_query = self.validInput.validate(body_query, '.body_query')
            for key, value in body_query.items():
                self.validInput.validate(value, '.body_query.key')
        results = self.validInput.validate(results, '.results')

    # construct search resource variables
        result_list = []
        log_list = listdir(self.repoFolder)
        if not results:
            results = len(log_list)
        if reverse:
            log_list = reversed(log_list)

    # conduct search over log list and return results
        for file in log_list:
            add_file = True

    # add files whose name match each regex expression in key query
            if key_query:
                for regex in key_query:
                    regex_pattern = compile(regex)
                    if not regex_pattern.findall(file):
                        add_file = False

    # add files whose top level values match each regex expression in body query
            if add_file and body_query:
                valid_file = False
                for extension in self.ext.names:
                    regex_pattern = getattr(self.ext, extension)
                    if regex_pattern.findall(file):
                        valid_file = True
                if not valid_file:
                    add_file = False
                else:
                    file_details = self.get(file)
                    for key, value in body_query.items():
                        if not key in file_details.keys():
                            add_file = False
                        else:
                            if not isinstance(file_details[key], str) and \
                                    not isinstance(file_details[key], int) and \
                                    not isinstance(file_details[key], float) and \
                                    not isinstance(file_details[key], bool):
                                add_file = False
                            else:
                                try:
                                    v = str(file_details[key])
                                    for regex in value:
                                        regex_pattern = compile(regex)
                                        if not regex_pattern.findall(v):
                                            add_file = False
                                except:
                                    add_file = False

    # add file that passes all query tests
            if add_file:
                for extension in self.ext.names:
                    regex_pattern = getattr(self.ext, extension)
                    if regex_pattern.findall(file):
                        result_list.append(file)

    # end search if results match desired result number
            if len(result_list) == results:
                return result_list

        return result_list

    def get(self, key_string):

        '''
            a method to retrieve body data from a log file

        :param key_string: string with name of file
        :return: dictionary with body data
        '''

        __name__ = '%s.get' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')

    # construct path to file
        log_path = path.join(self.repoFolder, key_string)

    # validate existence of file
        if not path.exists(log_path):
            raise Exception('%s does not exist.' % _key_arg)

    # retrieve file details
        log_details = {}
        if self.ext.json.findall(key_string):
            import json
            try:
                file_data = open(log_path, 'rt')
                log_details = json.loads(file_data.read())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yaml.findall(key_string):
            import yaml
            try:
                file_data = open(log_path, 'rt')
                log_details = yaml.load(file_data.read())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.jsongz.findall(key_string):
            import json
            import gzip
            try:
                file_data = gzip.open(log_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                log_details = json.loads(file_data.read().decode())
            except:
                raise Exception('%s is not valid json data.' % _key_arg)
        elif self.ext.yamlgz.findall(key_string):
            import yaml
            import gzip
            try:
                file_data = gzip.open(log_path, 'rb')
            except:
                raise Exception('%s is not valid gzip compressed data.' % _key_arg)
            try:
                log_details = yaml.load(file_data.read().decode())
            except:
                raise Exception('%s is not valid yaml data.' % _key_arg)
        elif self.ext.drep.findall(key_string):
            from popuplab.compilers import drep
            try:
                file_data = open(log_path)
                log_details = drep.load(private_key='', encrypted_data=file_data)
            except:
                raise Exception('%s is not valid drep data.' % _key_arg)

        return log_details

    def delete(self, key_string):

        '''
            a method to delete a log file

        :param key_string: string with name of file
        :return: string reporting outcome
        '''

        __name__ = '%s.delete' % self.__class__.__name__
        _key_arg = '%s(key_string="%s")' % (__name__, key_string)

    # validate inputs
        key_string = self.validInput.validate(key_string, '.key_string')

    # construct path to file
        log_path = path.join(self.repoFolder, key_string)

    # validate existence of file
        if not path.exists(log_path):
            return '%s does not exist.' % key_string

        try:
            from os import remove
            remove(log_path)
        except:
            raise Exception('%s failed to delete %s' % (_key_arg, key_string))

        return '%s has been deleted.' % key_string

    def compact(self, total_number=0, cutoff_date=''):

        return True

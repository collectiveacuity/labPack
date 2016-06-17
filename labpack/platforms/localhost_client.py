__author__ = 'rcj1492'
__created__ = '2016.03'


from os import environ, path
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

    # construct empty file list
        self.files = []

    def appData(self, org_name, prod_name):

        data_path = ''

        if self.os == 'Windows':
            from re import compile
            xp_pattern = compile('^C:\\Documents and Settings')
            app_data = ''
            if environ.get('APPDATA'):
                app_data = environ.get('APPDATA')
            if xp_pattern.findall(app_data):
                data_path = 'C:\\Documents and Settings\\%sLocal Settings\\Application Data\\%s\\%s' % (self.username, org_name, prod_name)
            else:
                data_path = 'C:\\Users\\%s\\AppData\\Local\\%s\\%s' % (self.username, org_name, prod_name)

        elif self.os == 'Mac':
            data_path = '~/Library/Application Support/%s/%s/' % (org_name, prod_name)

        elif self.os in ('Linux', 'FreeBSD', 'Solaris'):
            org_format = org_name.replace(' ','-').lower()
            prod_format = prod_name.replace(' ', '-').lower()
            data_path = '~/.config/%s-%s/' % (org_format, prod_format)

        return data_path
    
    def clientData(self, client_name, org_name='', prod_name=''):

        if not org_name:
            org_name = __team__
        if not prod_name:
            prod_name = __module__
        app_path = self.appData(org_name, prod_name)
        if self.os in ('Linux', 'FreeBSD', 'Solaris'):
            client_name = client_name.replace(' ', '-').lower()
        data_path = path.join(app_path, client_name)
        
        return data_path

    def index(self, index_root=''):

    # import dependencies
        from os import walk

    # clear existing index
        self.files = []

    # determine inputs
        if index_root:
            if not path.isdir(index_root):
                index_root = './'
        else:
            index_root = './'

    # walk the local file index
        for current_dir, sub_dirs, dir_files in walk(index_root):
            for file in dir_files:
                self.files.append(path.join(path.abspath(current_dir), file))

        return self
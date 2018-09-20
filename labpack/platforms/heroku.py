__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

from labpack.handlers.requests import requestsHandler

class herokuClient(requestsHandler):
    
    _class_fields = {
        'schema': {
            'account_email': 'noreply@collectiveacuity.com',
            'account_password': 'abcDEF123GHI!!!',
            'auth_token': 'abcdef01-2345-6789-abcd-ef0123456789',
            'app_subdomain': 'mycoolappsubdomain',
            'virtualbox_name': 'default',
            'site_folder': 'site/',
            'runtime_type': 'html',
            'dockerfile_path': '/home/user/lab/project/Dockerfile'
        },
        'components': {
            '.runtime_type': {
                'discrete_values': [ 'html', 'php', 'node', 'python', 'java', 'ruby', 'jingo' ]
            }
        }
    }
    
    def __init__(self, account_email, auth_token, verbose=True):
        
        ''' a method to initialize the herokuClient class '''

        title = '%s.__init__' % self.__class__.__name__
    
    # initialize super
        super(herokuClient, self).__init__(verbose=verbose)
        
    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # validate inputs
        input_fields = {
            'account_email': account_email,
            'auth_token': auth_token
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # construct properties
        self.email = account_email
        self.token = auth_token
        self.subdomain = ''
        self.apps = []
        
    # construct localhost
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()
    
    # validate installation
        self._validate_install()
    
    # validate access
        self._validate_login()
        
    def _validate_install(self):

        ''' a method to validate heroku is installed '''

        self.printer('Checking heroku installation ... ', flush=True)
    
    # import dependencies
        from os import devnull
        from subprocess import call, check_output
        
    # validate cli installation
        sys_command = 'heroku --version'
        try:
            call(sys_command, shell=True, stdout=open(devnull, 'wb'))
        except Exception as err:
            self.printer('ERROR')
            raise Exception('"heroku cli" not installed. GoTo: https://devcenter.heroku.com/articles/heroku-cli')
    
    # print response and return
        self.printer('done.')
        
        return True

    def _update_netrc(self, netrc_path, auth_token, account_email):
        
        ''' a method to replace heroku login details in netrc file '''
    
    # define patterns
        import re
        record_end = '(\n\n|\n\w|$)'
        heroku_regex = re.compile('(machine\sapi\.heroku\.com.*?\nmachine\sgit\.heroku\.com.*?)%s' % record_end, re.S)
        
    # retrieve netrc text
        netrc_text = open(netrc_path).read().strip()
        
    # replace text with new password and login
        new_heroku = 'machine api.heroku.com\n  password %s\n  login %s\n' % (auth_token, account_email)
        new_heroku += 'machine git.heroku.com\n  password %s\n  login %s\n\n' % (auth_token, account_email)
        heroku_search = heroku_regex.findall(netrc_text)
        if heroku_search:
            if re.match('\n\w', heroku_search[0][1]):
                new_heroku = new_heroku[:-1]
                new_heroku += heroku_search[0][1]
            netrc_text = heroku_regex.sub(new_heroku, netrc_text)
        else:
            netrc_text += '\n\n' + new_heroku
        
    # save netrc
        with open(netrc_path, 'wt') as f:
            f.write(netrc_text)
            f.close()

        return netrc_text
    
    def _validate_login(self):
        
        ''' a method to validate user can access heroku account '''
        
        title = '%s.validate_login' % self.__class__.__name__
            
    # verbosity
        windows_insert = ' On windows, run in cmd.exe'
        self.printer('Checking heroku credentials ... ', flush=True)

    # validate netrc exists
        from os import path
        netrc_path = path.join(self.localhost.home, '.netrc')
    # TODO verify path exists on Windows
        if not path.exists(netrc_path):
            error_msg = '.netrc file is missing. Try: heroku login, then heroku auth:token'
            if self.localhost.os.sysname in ('Windows'):
                error_msg += windows_insert
            self.printer('ERROR.')
            raise Exception(error_msg)

    # replace value in netrc
        netrc_text = self._update_netrc(netrc_path, self.token, self.email)

    # verify remote access
        def handle_invalid(stdout, proc):

        # define process closing helper
            def _close_process(_proc):
            # close process
                import psutil
                process = psutil.Process(_proc.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            # restore values to netrc
                with open(netrc_path, 'wt') as f:
                    f.write(netrc_text)
                    f.close()

        # invalid credentials
            if stdout.find('Invalid credentials') > -1:
                _close_process(proc)
                self.printer('ERROR.')
                raise Exception('Permission denied. Heroku auth token is not valid.\nTry: "heroku login", then "heroku auth:token"')

        sys_command = 'heroku apps --json'
        response = self._handle_command(sys_command, interactive=handle_invalid, handle_error=True)

        if response.find('Warning: heroku update') > -1:
            self.printer('WARNING: heroku update available.')
            self.printer('Try: npm install -g -U heroku\nor see https://devcenter.heroku.com/articles/heroku-cli#staying-up-to-date')
            self.printer('Checking heroku credentials ... ')
            response_lines = response.splitlines()
            response = '\n'.join(response_lines[1:])

    # add list to object
        import json
        try:
            self.apps = json.loads(response)
        except:
            self.printer('ERROR.')
            raise Exception(response)

        self.printer('done.')

        return self
    
    def access(self, app_subdomain):

        ''' a method to validate user can access app '''

        title = '%s.access' % self.__class__.__name__
    
    # validate input
        input_fields = {
            'app_subdomain': app_subdomain
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
        
    # verbosity
        self.printer('Checking access to "%s" subdomain ... ' % app_subdomain, flush=True)

    # confirm existence of subdomain
        for app in self.apps:
            if app['name'] == app_subdomain:
                self.subdomain = app_subdomain
                break
    
    # refresh app list and search again
        if not self.subdomain:
            import json
            response = self._handle_command('heroku apps --json', handle_error=True)
            self.apps = json.loads(response)

            for app in self.apps:
                if app['name'] == app_subdomain:
                    self.subdomain = app_subdomain
                    break
    
    # check reason for failure
        if not self.subdomain:
            sys_command = 'heroku ps -a %s' % app_subdomain
            heroku_response = self._handle_command(sys_command, handle_error=True)
            if heroku_response.find('find that app') > -1:
                self.printer('ERROR')
                raise Exception('%s does not exist. Try: heroku create -a %s' % (app_subdomain, app_subdomain))
            elif heroku_response.find('have access to the app') > -1:
                self.printer('ERROR')
                raise Exception('%s belongs to another account.' % app_subdomain)
            else:
                self.printer('ERROR')
                raise Exception('Some unknown issue prevents you from accessing %s' % app_subdomain)

        self.printer('done.')
        
        return self
        
    def deploy_docker(self, dockerfile_path, virtualbox_name='default'):

        ''' a method to deploy app to heroku using docker '''

        title = '%s.deploy_docker' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'dockerfile_path': dockerfile_path,
            'virtualbox_name': virtualbox_name
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # check app subdomain
        if not self.subdomain:
            raise Exception('You must access a subdomain before you can deploy to heroku. Try: %s.access()' % self.__class__.__name__)
            
    # import dependencies
        from os import path

    # validate docker client
        from labpack.platforms.docker import dockerClient
        dockerClient(virtualbox_name, self.verbose)

    # validate dockerfile
        if not path.exists(dockerfile_path):
            raise Exception('%s is not a valid path on local host.' % dockerfile_path)
        dockerfile_root, dockerfile_node = path.split(dockerfile_path)
        if dockerfile_node != 'Dockerfile':
            raise Exception('heroku requires a file called Dockerfile to deploy using Docker.')

    # validate container plugin
        from os import devnull
        from subprocess import check_output
        self.printer('Checking heroku plugin requirements ... ', flush=True)
        sys_command = 'heroku plugins --core'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-container-registry') == -1 and heroku_plugins.find('container-registry') == -1:
            sys_command = 'heroku plugins'
            heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
            if heroku_plugins.find('heroku-container-registry') == -1 and heroku_plugins.find('container-registry') == -1:
                self.printer('ERROR')
                raise Exception(
                    'heroku container registry required. Upgrade heroku-cli.')
        self.printer('done.')

    # verify container login
        self.printer('Checking heroku container login ... ', flush=True)
        sys_command = 'heroku container:login'
        self._handle_command(sys_command)
        self.printer('done.')
    
    # Old Login Process (pre 2018.02.03)
        # import pexpect
        # try:
        #     child = pexpect.spawn('heroku container:login', timeout=5)
        #     child.expect('Email:\s?')
        #     child.sendline(self.email)
        #     i = child.expect([pexpect.EOF, pexpect.TIMEOUT])
        #     if i == 0:
        #         child.terminate()
        #     elif i == 1:
        #         child.terminate()
        #         raise Exception('Some unknown issue prevents Heroku from accepting credentials.\nTry first: heroku login')
        # except Exception as err:
        #     self._check_connectivity(err)
        # self.printer('done.')
        
    # verbosity
        self.printer('Building docker image ...')
    
    # build docker image
        sys_command = 'cd %s; heroku container:push web --app %s' % (dockerfile_root, self.subdomain)
        self._handle_command(sys_command, print_pipe=True)
        sys_command = 'cd %s; heroku container:release web --app %s' % (dockerfile_root, self.subdomain)
        self._handle_command(sys_command, print_pipe=True)
        self.printer('Deployment complete.')

        return True

    def deploy_app(self, site_folder, runtime_type=''):

        ''' a method to deploy a static html page to heroku using php '''

        title = '%s.deploy_php' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'site_folder': site_folder,
            'runtime_type': runtime_type
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify app subdomain
        if not self.subdomain:
            raise Exception('You must access a subdomain before you can deploy to heroku. Try: %s.access()' % self.__class__.__name__)
                    
    # validate existence of site folder
        from os import path
        if not path.exists(site_folder):
            raise ValueError('%s is not a valid path on localhost.' % site_folder)
    
    # validate existence of proper runtime file
        runtime_file = 'index.html'
        static_build = False
        if runtime_type == 'php':
            runtime_file = 'index.php'
        elif runtime_type in ('ruby', 'java', 'python', 'jingo'):
            runtime_file = 'Procfile'
        elif runtime_type == 'node':
            runtime_file = 'package.json'
        else:
            runtime_type = 'html'
            static_build = True
        build_file = path.join(site_folder, runtime_file)
        if not path.exists(build_file):
            raise Exception('%s must contain an %s file to build a %s app.' % (site_folder, runtime_file, runtime_type))
        if runtime_type == 'python':
            req_file = path.join(site_folder, 'requirements.txt')
            if not path.exists(req_file):
                raise Exception('%s must contain a requirements.txt file to build a python app.' % site_folder)
        if runtime_type == 'jingo':
            req_file = path.join(site_folder, 'package.json')
            if not path.exists(req_file):
                raise Exception('%s must contain a package.json file to build a jingo app.' % site_folder)

    # validate container plugin
        from os import devnull
        from subprocess import check_output
        self.printer('Checking heroku plugin requirements ... ', flush=True)
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-builds') == -1:
            self.printer('ERROR')
            raise Exception(
                'heroku builds plugin required. Try: heroku plugins:install heroku-builds')
        self.printer('done.')
    
    # construct temporary folder
        self.printer('Creating temporary files ... ', flush=True)
        from shutil import copytree, move, ignore_patterns
        from os import makedirs
        from time import time
        from labpack import __module__
        from labpack.storage.appdata import appdataClient
        client_kwargs = {
            'collection_name': 'TempFiles',
            'prod_name': __module__
        }
        tempfiles_client = appdataClient(**client_kwargs)
        temp_folder = path.join(tempfiles_client.collection_folder, 'heroku%s' % time())
    
    # define cleanup function
        def _cleanup_temp():
            self.printer('Cleaning up temporary files ... ', flush=True)
            from shutil import rmtree
            rmtree(temp_folder, ignore_errors=True)
            self.printer('done.')

    # copy site to temporary folder
        try:
            makedirs(temp_folder)
            site_root, site_name = path.split(path.abspath(site_folder))
            build_path = path.join(temp_folder, site_name)
            copytree(site_folder, build_path, ignore=ignore_patterns('*node_modules/*','*.lab/*'))
            if static_build:
                index_path = path.join(build_path, 'index.html')
                home_path = path.join(build_path, 'home.html')
                compose_path = path.join(build_path, 'compose.json')
                php_path = path.join(build_path, 'index.php')
                with open(compose_path, 'wt') as f:
                    f.write('{}')
                    f.close()
                with open(php_path, 'wt') as f:
                    f.write('<?php include_once("home.html"); ?>')
                    f.close()
                move(index_path, home_path)
        except:
            self.printer('ERROR')
            _cleanup_temp()
            raise
        self.printer('done.')

    # deploy site to heroku
        self.printer('Deploying %s to heroku ... ' % site_folder, flush=True)
        try:
            sys_command = 'cd %s; heroku builds:create -a %s' % (temp_folder, self.subdomain)
            self._handle_command(sys_command, print_pipe=True)
        except:
            self.printer('ERROR')
            raise
        finally:
            _cleanup_temp()

        self.printer('Deployment complete.')
        
        return True
    
if __name__ == '__main__':
    
    from labpack.records.settings import load_settings
    heroku_config = load_settings('../../../cred/heroku.yaml')
    heroku_kwargs = {
        'account_email': heroku_config['heroku_account_email'],
        'auth_token': heroku_config['heroku_auth_token'],
        'verbose': True
    }
    heroku_client = herokuClient(**heroku_kwargs)
    heroku_client.access(heroku_config['heroku_app_subdomain'])
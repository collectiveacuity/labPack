__author__ = 'rcj1492'
__created__ = '2017.06'
__license__ = 'MIT'

class herokuClient(object):
    
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
                'discrete_values': [ 'html', 'php', 'node', 'python', 'java', 'ruby' ]
            }
        }
    }
    
    def __init__(self, account_email, auth_token, verbose=True):
        
        ''' a method to initialize the herokuClient class '''

        title = '%s.__init__' % self.__class__.__name__
        
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
        self.email = account_email
        self.token = auth_token
        self.subdomain = ''
        self.apps = []

    # construct class properties
        self.verbose = verbose
        self.printer_on = True
        def _printer(msg, flush=False):
            if self.verbose:
                if self.printer_on:
                    if flush:
                        print(msg, end='', flush=True)
                    else:
                        print(msg)
        self.printer = _printer
        
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
        
    def _handle_command(self, sys_command, pipe=False, handle_error=False):

        ''' a method to handle system commands which require connectivity '''

        import sys
        from subprocess import Popen, PIPE, check_output, STDOUT, CalledProcessError

        try:
            if pipe:
                response = Popen(sys_command, shell=True, stdout=PIPE, stderr=STDOUT)
                for line in response.stdout:
                    self.printer(line.decode('utf-8').rstrip('\n'))
                    sys.stdout.flush()
                response.wait()
                return response
            else:
                response = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                return response
        except CalledProcessError as err:
            try:
                import requests
                requests.get('https://www.google.com')
                if handle_error:
                    return err.output.decode('ascii', 'ignore')
            except:
                from requests import Request
                from labpack.handlers.requests import handle_requests
                request_object = Request(method='GET', url='https://www.google.com')
                request_details = handle_requests(request_object)
                self.printer('ERROR')
                raise ConnectionError(request_details['error'])
            self.printer('ERROR')
            raise
        except:
            self.printer('ERROR')
            raise
        
    def _check_connectivity(self, err):

        ''' a method to check connectivity as source of error '''
        
        try:
            import requests
            requests.get('https://www.google.com')
        except:
            from requests import Request
            from labpack.handlers.requests import handle_requests
            request_object = Request(method='GET', url='https://www.google.com')
            request_details = handle_requests(request_object)
            self.printer('ERROR')
            raise ConnectionError(request_details['error'])
        self.printer('ERROR')
        raise err

    def _update_netrc(self, netrc_path, auth_token, account_email):
        
        ''' a method to replace heroku login details in netrc file '''
    
    # define patterns
        import re
        api_regex = re.compile('machine\sapi\.heroku\.com.*?\s\slogin\s.*?\n', re.S)
        git_regex = re.compile('machine\sgit\.heroku\.com.*?\s\slogin\s.*?\n', re.S)
        
    # retrieve netrc text
        netrc_text = open(netrc_path).read()
    
    # replace text with new password and login
        new_api = 'machine api.heroku.com\n  password %s\n  login %s\n' % (auth_token, account_email)
        new_git = 'machine git.heroku.com\n  password %s\n  login %s\n' % (auth_token, account_email)
        netrc_text = api_regex.sub(new_api, netrc_text)
        netrc_text = git_regex.sub(new_git, netrc_text)
        
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
            error_msg = '.netrc file is missing. Try: heroku login, then update auth token.'
            if self.localhost.os.sysname in ('Windows'):
                error_msg += windows_insert
            self.printer('ERROR.')
            raise Exception(error_msg)
    
    # replace value in netrc
        self._update_netrc(netrc_path, self.token, self.email)
    
    # verify remote access
        sys_command = 'heroku apps --json'
        response = self._handle_command(sys_command, handle_error=True)
        if response.find('Invalid credentials') > -1:
            raise Exception('Permission denied. Heroku login credentials are not valid.')
    
    # add list to object
        import json
        self.apps = json.loads(response)
        
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
                raise Exception('%s belongs to another account.')
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
        sys_command = 'heroku plugins'
        heroku_plugins = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8')
        if heroku_plugins.find('heroku-container-registry') == -1:
            self.printer('ERROR')
            raise Exception(
                'heroku container plugin required. Try: heroku plugins:install heroku-container-registry')
        self.printer('done.')
            
    # verify container login
        self.printer('Checking heroku container login ... ', flush=True)
        import pexpect
        try:
            child = pexpect.spawn('heroku container:login', timeout=2)
            child.expect('Email:\s?')
            child.sendline(self.email)
            i = child.expect([pexpect.EOF, pexpect.TIMEOUT])
            if i == 0:
                child.terminate()
            elif i == 1:
                child.terminate()
                raise Exception('Some unknown issue prevents Heroku from accepting credentials.\nTry first: heroku login')
        except Exception as err:
            self._check_connectivity(err)
        self.printer('done.')
        
    # verbosity
        self.printer('Building docker image ...')
    
    # build docker image
        sys_command = 'cd %s; heroku container:push web --app %s' % (dockerfile_root, self.subdomain)
        heroku_response = self._handle_command(sys_command, pipe=True)
        self.printer('Deployment complete.')

        return heroku_response

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
        elif runtime_type in ('ruby', 'java', 'python'):
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
    
    # construct temporary file folder
        self.printer('Creating temporary files ... ', flush=True)
        try:
            from shutil import copytree, move
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
            makedirs(temp_folder)
            site_root, site_name = path.split(path.abspath(site_folder))
            build_path = path.join(temp_folder, site_name)
            copytree(site_folder, build_path)
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
            raise
        self.printer('done.')
    
    # define cleanup function
        def _cleanup_temp():
            self.printer('Cleaning up temporary files ... ', flush=True)
            from shutil import rmtree
            rmtree(temp_folder, ignore_errors=True)
            self.printer('done.')
            
    # deploy site to heroku
        self.printer('Deploying %s to heroku ... ' % site_folder, flush=True)
        try:
            sys_command = 'cd %s; heroku builds:create -a %s' % (temp_folder, self.subdomain)
            self._handle_command(sys_command, pipe=True)
        except:
            self.printer('ERROR')
            _cleanup_temp()
            raise
        self.printer('Deployment complete.')
        
    # remove temporary files
        _cleanup_temp()
        
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
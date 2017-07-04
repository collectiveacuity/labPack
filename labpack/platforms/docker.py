__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

class dockerClient(object):

    def __init__(self, virtualbox_name='', verbose=False):

        '''
            a method to initialize the dockerClient class
            
        :param virtualbox_name: [optional] string with name of virtualbox image
        :return: dockerClient object
        '''
    
    # construct vbox property
        self.vbox = virtualbox_name
        self.verbose = verbose
        
    # construct localhost
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()
        
    # verbosity
        if self.verbose:
            print('Checking docker installation...', end='', flush=True)
            
    # validate docker installation
        self._validate_install()
        if self.verbose:
            print('.', end='', flush=True)
            
    # validate virtualbox installation
        box_running = self._validate_virtualbox()
        if self.verbose:
            print('.', end='', flush=True)
    
    # set virtualbox variables
        if box_running:
            self._set_virtualbox()
            if self.verbose:
                print('.', end='', flush=True)
        
        if self.verbose:
            print(' done.')
        
    def _validate_install(self):

        ''' a method to validate docker is installed '''
    
        from os import devnull
        from subprocess import call
        sys_command = 'docker --help'
        try:
            call(sys_command, stdout=open(devnull, 'wb'))
        except Exception as err:
            raise Exception('"docker" not installed. GoTo: https://www.docker.com')
    
        return True

    def _validate_virtualbox(self):

        '''
            a method to validate that virtualbox is running on Win 7/8 machines

        :return: boolean indicating whether virtualbox is running
        '''

    # validate operating system
        if self.localhost.os.sysname != 'Windows':
            return False
        win_release = float(self.localhost.os.release)
        if win_release >= 10.0:
            return False

    # validate docker-machine installation
        from os import devnull
        from subprocess import call, check_output
        sys_command = 'docker-machine --help'
        try:
            call(sys_command, stdout=open(devnull, 'wb'))
        except Exception as err:
            raise Exception('Docker requires docker-machine to run on Win7/8. GoTo: https://www.docker.com')

    # validate virtualbox is running
        sys_command = 'docker-machine status %s' % self.vbox
        try:
            vbox_status = check_output(sys_command, stderr=open(devnull, 'wb')).decode('utf-8').replace('\n', '')
        except Exception as err:
            if not self.vbox:
                raise Exception('Docker requires VirtualBox to run on Win7/8. GoTo: https://www.virtualbox.org')
            elif self.vbox == "default":
                raise Exception('Virtualbox "default" not found. Container will not start without a valid virtualbox.')
            else:
                raise Exception('Virtualbox "%s" not found. Try using "default" instead.' % self.vbox)
        if 'Stopped' in vbox_status:
            raise Exception('Virtualbox "%s" is stopped. Try first running: docker-machine start %s' % (self.vbox, self.vbox))

        return True
    
    def _set_virtualbox(self):
        
        '''
            a method to set virtualbox environment variables for docker-machine
            
        :return: True
        '''

        from os import environ
        if not environ.get('DOCKER_CERT_PATH'):
            import re
            from subprocess import check_output
            sys_command = 'docker-machine env %s' % self.vbox
            cmd_output = check_output(sys_command).decode('utf-8')
            variable_list = ['DOCKER_TLS_VERIFY', 'DOCKER_HOST', 'DOCKER_CERT_PATH', 'DOCKER_MACHINE_NAME']
            for variable in variable_list:
                env_start = '%s="' % variable
                env_end = '"\\n'
                env_regex = '%s.*?%s' % (env_start, env_end)
                env_pattern = re.compile(env_regex)
                env_statement = env_pattern.findall(cmd_output)
                env_var = env_statement[0].replace(env_start, '').replace('"\n', '')
                environ[variable] = env_var
        
        return True
    
    def images(self):

        '''

        :return: list of docker images available

        [ {
            'CREATED': '7 days ago',
            'TAG': 'latest',
            'IMAGE ID': '2298fbaac143',
            'VIRTUAL SIZE': '302.7 MB',
            'REPOSITORY': 'test1'
        } ]
        '''

        import re
        from subprocess import check_output
        gap_pattern = re.compile('\t|\s{2,}')
        image_list = []
        sys_command = 'docker images'
        output_lines = check_output(sys_command).decode('utf-8').split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            if len(columns) == len(column_headers):
                image_details = {}
                for j in range(len(columns)):
                    image_details[column_headers[j]] = columns[j]
                image_list.append(image_details)

        return image_list

    def ps(self):

        '''

        :return: list of active docker containers

        [{
            'CREATED': '6 minutes ago',
            'NAMES': 'flask',
            'PORTS': '0.0.0.0:5000->5000/tcp',
            'CONTAINER ID': '38eb0bbeb2e5',
            'STATUS': 'Up 6 minutes',
            'COMMAND': '"gunicorn --chdir ser"',
            'IMAGE': 'rc42/flaskserver'
        }]
        '''

        import re
        from subprocess import check_output
        gap_pattern = re.compile('\t|\s{2,}')
        container_list = []
        sys_command = 'docker ps -a'
        output_lines = check_output(sys_command).decode('utf-8').split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            container_details = {}
            if len(columns) > 1:
                for j in range(len(column_headers)):
                    container_details[column_headers[j]] = ''
                    if j <= len(columns) - 1:
                        container_details[column_headers[j]] = columns[j]
        # stupid hack for possible empty port column
                if container_details['PORTS'] and not container_details['NAMES']:
                    from copy import deepcopy
                    container_details['NAMES'] = deepcopy(container_details['PORTS'])
                    container_details['PORTS'] = ''
                container_list.append(container_details)

        return container_list

    def inspect(self, container_alias='', docker_image='', image_tag=''):

        '''

        :param container_alias: string with name of container
        :return: dictionary of settings of container

        { TOO MANY TO LIST }
        '''

        from subprocess import check_output
        sys_arg = container_alias
        if docker_image:
            sys_arg = docker_image
            if image_tag:
                sys_arg += ':%s' % image_tag
        import json
        sys_command = 'docker inspect %s' % sys_arg
        output_dict = json.loads(check_output(sys_command).decode('utf-8'))
        container_settings = output_dict[0]

        return container_settings

    def run(self, run_script):

        from subprocess import check_output
        output_lines = check_output(run_script).decode('utf-8').split('\n')
        container_id = output_lines[0]

        return container_id

    def rm(self, container_alias):

        from subprocess import check_output
        sys_cmd = 'docker rm -f %s' % container_alias
        output_lines = check_output(sys_cmd).decode('utf-8').split('\n')

        return output_lines[0]

    def rmi(self, image_id):

        from subprocess import check_output
        sys_cmd = 'docker rmi %s' % image_id
        output_lines = check_output(sys_cmd).decode('utf-8').split('\n')

        return output_lines

    def ip(self):

        '''

        :return: string with ip address of system
        '''

        if self.vbox:
            from subprocess import check_output
            sys_command = 'docker-machine ip %s' % self.vbox
            system_ip = check_output(sys_command).decode('utf-8').replace('\n','')
        else:
            system_ip = self.localhost.ip

        return system_ip

    def command(self, sys_command):

        '''

        :param sys_command: string with docker command
        :return: raw output from docker
        '''

        from subprocess import check_output
        return check_output(sys_command).decode('utf-8')

    def synopsis(self, container_settings):

        '''

        :param container_settings: dictionary returned from dockerConfig.inspect
        :return: dictionary with values required for module configurations
        '''

        settings = {
            'container_status': container_settings['State']['Status'],
            'container_ip': container_settings['NetworkSettings']['IPAddress'],
            'docker_image': container_settings['Config']['Image'],
            'container_alias': container_settings['Name'].replace('/',''),
            'container_variables': {},
            'mapped_ports': {},
            'mounted_volumes': {}
        }
        import re
        num_pattern = re.compile('\d+')
        if container_settings['NetworkSettings']['Ports']:
            for key, value in container_settings['NetworkSettings']['Ports'].items():
                port = num_pattern.findall(value[0]['HostPort'])[0]
                settings['mapped_ports'][port] = num_pattern.findall(key)[0]
        if container_settings['Config']['Env']:
            for variable in container_settings['Config']['Env']:
                k, v = variable.split('=')
                settings['container_variables'][k] = v
        for volume in container_settings['Mounts']:
            system_path = volume['Source']
            container_path = volume['Destination']
            settings['mounted_volumes'][system_path] = container_path

        return settings

    def enter(self, container_alias):

        from os import system
        sys_cmd = 'docker exec -it %s sh' % container_alias
        if self.localhost.os.sysname in ('Windows'):
            sys_cmd = 'winpty %s' % sys_cmd

        system(sys_cmd)

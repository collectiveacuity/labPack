__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from labpack.handlers.requests import requestsHandler

class dockerClient(requestsHandler):

    _class_fields = {
        'schema': {
            'virtualbox_name': '',
            'container_alias': '',
            'image_name': '',
            'image_tag': '',
            'image_id': '',
            'sys_command': '',
            'environmental_variables': {},
            'envvar_key': '',
            'envvar_value': '',
            'mapped_ports': {},
            'port_key': '1000',
            'port_value': '1000',
            'mounted_volumes': {},
            'mount_field': '',
            'start_command': '',
            'network_name': '',
            'run_flags': ''
        },
        'components': {
            '.envvar_key': {
                'must_contain': [ '^[a-zA-Z_][a-zA-Z0-9_]+$' ],
                'max_length': 255
            },
            '.envvar_value': {
                'max_length': 32767
            },
            '.port_key': {
                'contains_either': [ '\d{2,5}', '\d{2,5}\-\d{2,5}' ]
            },
            '.port_value': {
                'contains_either': [ '\d{2,5}', '\d{2,5}\-\d{2,5}' ]
            }
        }
    }

    def __init__(self, virtualbox_name='', verbose=False):

        '''
            a method to initialize the dockerClient class

        :param virtualbox_name: [optional] string with name of virtualbox image
        :return: dockerClient object
        '''

        title = '%s.__init__' % self.__class__.__name__
    
    # construct super
        super(dockerClient, self).__init__()

    # construct fields model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)
    
    # validate inputs
        input_fields = {
            'virtualbox_name': virtualbox_name
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # construct properties
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
        self.vbox_running = self._validate_virtualbox()
        if self.verbose:
            print('.', end='', flush=True)
    
    # set virtualbox variables
        if self.vbox_running:
            self._set_virtualbox()
            if self.verbose:
                print('.', end='', flush=True)

        if self.verbose:
            print(' done.')

    def _validate_install(self):

        ''' a method to validate docker is installed '''

        from subprocess import check_output, STDOUT
        sys_command = 'docker --help'
        try:
            check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
            # call(sys_command, stdout=open(devnull, 'wb'))
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
        from subprocess import call, check_output, STDOUT
        sys_command = 'docker-machine --help'
        try:
            check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
        except Exception as err:
            raise Exception('Docker requires docker-machine to run on Win7/8. GoTo: https://www.docker.com')

    # validate virtualbox is running
        sys_command = 'docker-machine status %s' % self.vbox
        try:
            vbox_status = check_output(sys_command, shell=True, stderr=open(devnull, 'wb')).decode('utf-8').replace('\n', '')
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
            sys_command = 'docker-machine env %s' % self.vbox
            cmd_output = self.command(sys_command)
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

    def _images(self, sys_output):
    
        ''' a helper method for parsing docker image output '''

        import re
        gap_pattern = re.compile('\t|\s{2,}')
        image_list = []
        output_lines = sys_output.split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            if len(columns) == len(column_headers):
                image_details = {}
                for j in range(len(columns)):
                    image_details[column_headers[j]] = columns[j]
                image_list.append(image_details)

        return image_list

    def _ps(self, sys_output):
        
        ''' a helper method for parsing docker ps output '''
        
        import re
        gap_pattern = re.compile('\t|\s{2,}')
        container_list = []
        output_lines = sys_output.split('\n')
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
    
    def _synopsis(self, container_settings, container_status=''):

        ''' a helper method for summarizing container settings '''
    
    # compose default response
        settings = {
            'container_status': container_settings['State']['Status'],
            'container_exit': container_settings['State']['ExitCode'],
            'container_ip': container_settings['NetworkSettings']['IPAddress'],
            'image_name': container_settings['Config']['Image'],
            'container_alias': container_settings['Name'].replace('/',''),
            'container_variables': {},
            'mapped_ports': {},
            'mounted_volumes': {},
            'container_networks': []
        }
    
    # parse fields nested in container settings
        import re
        num_pattern = re.compile('\d+')
        if container_settings['NetworkSettings']['Ports']:
            for key, value in container_settings['NetworkSettings']['Ports'].items():
                if value:
                    port = num_pattern.findall(value[0]['HostPort'])[0]
                    settings['mapped_ports'][port] = num_pattern.findall(key)[0]
        elif container_settings['HostConfig']['PortBindings']:
            for key, value in container_settings['HostConfig']['PortBindings'].items():
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
        if container_settings['NetworkSettings']:
            if container_settings['NetworkSettings']['Networks']:
                for key in container_settings['NetworkSettings']['Networks'].keys():
                    settings['container_networks'].append(key)

    # determine stopped status
        if settings['container_status'] == 'exited':
            if not container_status:
                try:
                    from subprocess import check_output, STDOUT
                    sys_command = 'docker logs --tail 1 %s' % settings['container_alias']
                    check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                    settings['container_status'] = 'stopped'
                except:
                    pass
            else:
                settings['container_status'] = container_status

        return settings
    
    def images(self):

        '''
            a method to list the local docker images
            
        :return: list of dictionaries with available image fields

        [ {
            'CREATED': '7 days ago',
            'TAG': 'latest',
            'IMAGE ID': '2298fbaac143',
            'VIRTUAL SIZE': '302.7 MB',
            'REPOSITORY': 'test1'
        } ]
        '''

        sys_command = 'docker images'
        sys_output = self.command(sys_command)
        image_list = self._images(sys_output)

        return image_list

    def ps(self):

        '''
            a method to list the local active docker containers 
            
        :return: list of dictionaries with active container fields

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

        sys_command = 'docker ps -a'
        sys_output = self.command(sys_command)
        container_list = self._ps(sys_output)

        return container_list

    def network_ls(self):
        
        '''
            a method to list the available networks
            
        :return: list of dictionaries with docker network fields

        [{
            'NETWORK ID': '3007476acfe5',
            'NAME': 'bridge',
            'DRIVER': 'bridge',
            'SCOPE': 'local'
        }]
        '''

        import re
        gap_pattern = re.compile('\t|\s{2,}')
        network_list = []
        sys_command = 'docker network ls'
        output_lines = self.command(sys_command).split('\n')
        column_headers = gap_pattern.split(output_lines[0])
        for i in range(1,len(output_lines)):
            columns = gap_pattern.split(output_lines[i])
            network_details = {}
            if len(columns) > 1:
                for j in range(len(column_headers)):
                    network_details[column_headers[j]] = ''
                    if j <= len(columns) - 1:
                        network_details[column_headers[j]] = columns[j]
                network_list.append(network_details)

        return network_list

    def inspect_container(self, container_alias):

        '''
            a method to retrieve the settings of a container
            
        :param container_alias: string with name or id of container
        :return: dictionary of settings of container

        { TOO MANY TO LIST }
        '''

        title = '%s.inspect_container' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'container_alias': container_alias
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # send inspect command
        import json
        sys_command = 'docker inspect %s' % container_alias
        output_dict = json.loads(self.command(sys_command))
        container_settings = output_dict[0]

        return container_settings

    def inspect_image(self, image_name, image_tag=''):
        
        '''
            a method to retrieve the settings of an image

        :param image_name: string with name or id of image
        :param image_tag: [optional] string with tag associated with image 
        :return: dictionary of settings of image

        { TOO MANY TO LIST }
        '''

        title = '%s.inspect_image' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_name': image_name,
            'image_tag': image_tag
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # determine system command argument
        sys_arg = image_name
        if image_tag:
            sys_arg += ':%s' % image_tag

    # run inspect command
        import json
        sys_command = 'docker inspect %s' % sys_arg
        output_dict = json.loads(self.command(sys_command))
        image_settings = output_dict[0]

        return image_settings

    def rm(self, container_alias):

        '''
            a method to remove an active container
            
        :param container_alias: string with name or id of container 
        :return: string with container id
        '''

        title = '%s.rm' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'container_alias': container_alias
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # run remove command
        sys_cmd = 'docker rm -f %s' % container_alias
        output_lines = self.command(sys_cmd).split('\n')

        return output_lines[0]

    def rmi(self, image_id):

        '''
            a method to remove an image

        :param image_name: string with id of image
        :return: list of strings with image layers removed
        '''

        title = '%s.rmi' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_id': image_id
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # send remove command 
        sys_cmd = 'docker rmi %s' % image_id
        output_lines = self.command(sys_cmd).split('\n')

        return output_lines

    def ip(self):

        '''
            a method to retrieve the ip of system running docker

        :return: string with ip address of system
        '''

        if self.localhost.os.sysname == 'Windows' and float(self.localhost.os.release) < 10:
            sys_cmd = 'docker-machine ip %s' % self.vbox
            system_ip = self.command(sys_cmd).replace('\n','')
        else:
            system_ip = self.localhost.ip

        return system_ip

    def search(self, image_name):

    # run docker search
        sys_command = 'docker search %s' % image_name
        shell_output = self._handle_command(sys_command)
    
    # parse table
        from labpack.parsing.shell import convert_table
        image_list = convert_table(shell_output)

        return image_list

    def build(self, image_name, image_tag='', dockerfile_path='./Dockerfile'):
    
    # construct sys command arguments
        from os import path
        tag_insert = ''
        if image_tag:
            tag_insert = ':%s' % image_tag
        path_root, path_node = path.split(dockerfile_path)
        sys_command = 'docker build -t %s%s -f %s %s' % (image_name, tag_insert, path_node, path_root)
    
    # determine verbosity
        print_pipe = False
        if self.verbose:
            print_pipe = True
        else:
            sys_command += ' -q'

    # run command
        shell_output = self._handle_command(sys_command, print_pipe=print_pipe)

        return shell_output
    
    def save(self, image_name, file_name, image_tag=''):

        sys_command = 'docker save -o %s %s' % (file_name, image_name)
        if image_tag:
            sys_command += ':%s' % image_tag
        return self.command(sys_command)

    def command(self, sys_command):

        '''
            a method to run a system command in a separate shell

        :param sys_command: string with docker command
        :return: string output from docker
        '''

        title = '%s.command' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'sys_command': sys_command
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

        from subprocess import check_output, STDOUT, CalledProcessError
        try:
            output = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
        except CalledProcessError as err:
            raise Exception(err.output.decode('ascii', 'ignore'))

        return output

    def synopsis(self, container_alias):

        '''
            a method to summarize key configuration settings required for docker compose

        :param container_alias: string with name or id of container
        :return: dictionary with values required for module configurations
        '''

        title = '%s.synopsis' % self.__class__.__name__
        
    # validate inputs
        input_fields = {
            'container_alias': container_alias
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
            
    # retrieve container settings
        container_settings = self.inspect_container(container_alias)
    
    # summarize settings
        settings = self._synopsis(container_settings)
        
        return settings

    def enter(self, container_alias):

        '''
            a method to open up a terminal inside a running container

        :param container_alias: string with name or id of container 
        :return: None
        '''
        
        title = '%s.enter' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'container_alias': container_alias
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)
    
    # compose system command
        from os import system
        sys_cmd = 'docker exec -it %s sh' % container_alias
        if self.localhost.os.sysname in ('Windows'):
            sys_cmd = 'winpty %s' % sys_cmd

    # open up terminal
        system(sys_cmd)

    def run(self, image_name, container_alias, image_tag='', environmental_variables=None, mapped_ports=None, mounted_volumes=None, start_command='', network_name='', run_flags=''):

        '''
             a method to start a local container

        :param image_name: string with name or id of image
        :param container_alias: string with name to assign to container
        :param image_tag: [optional] string with tag assigned to image
        :param environmental_variables: [optional] dictionary of envvar fields to add to container
        :param mapped_ports: [optional] dictionary of port fields to map to container
        :param mounted_volumes: [optional] dictionary of path fields to map to container
        :param start_command: [optional] string of command (and any arguments) to run inside container
        :param network_name: [optional] string with name of docker network to link container to 
        :param run_flags: [optional] string with additional docker options to add to container
        :return: string with container id

        NOTE:   valid characters for environmental variables key names follow the shell
                standard of upper and lower alphanumerics or underscore and cannot start
                with a numerical value.

        NOTE:   ports are mapped such that the key name is the system port and the
                value is the port inside the container. both must be strings of digits.
        
        NOTE:   volumes are mapped such that the key name is the absolute or relative
                system path and the value is the absolute path inside the container. 
                both must be strings.
        
        NOTE:   additional docker options:
                    --entrypoint    overrides existing entrypoint command
                    --rm            removes container once start command exits
                    --log-driver    sets system logging settings for the container
                https://docs.docker.com/engine/reference/run
        '''
    
        title = '%s.run' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'image_name': image_name,
            'container_alias': container_alias,
            'image_tag': image_tag,
            'environmental_variables': environmental_variables,
            'mapped_ports': mapped_ports,
            'mounted_volumes': mounted_volumes,
            'start_command': start_command,
            'network_name': network_name,
            'run_flags': run_flags
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # validate subfields
        if environmental_variables:
            for key, value in environmental_variables.items():
                key_title = '%s(environmental_variables={%s:...})' % (title, key)
                self.fields.validate(key, '.envvar_key', key_title)
                value_title = '%s(environmental_variables={%s:%s})' % (title, key, str(value))
                self.fields.validate(value, '.envvar_value', value_title)
        else:
            environmental_variables = {}
        if mapped_ports:
            for key, value in mapped_ports.items():
                key_title = '%s(mapped_ports={%s:...})' % (title, key)
                self.fields.validate(key, '.port_key', key_title)
                value_title = '%s(mapped_ports={%s:%s})' % (title, key, str(value))
                self.fields.validate(value, '.port_value', value_title)
        else:
            mapped_ports = {}
        if mounted_volumes:
            for key, value in mounted_volumes.items():
                key_title = '%s(mounted_volumes={%s:...})' % (title, key)
                self.fields.validate(key, '.mount_field', key_title)
                value_title = '%s(mounted_volumes={%s:%s})' % (title, key, str(value))
                self.fields.validate(value, '.mount_field', value_title)
        else:
            mounted_volumes = {}
    
    # TODO verify image exists (locally or remotely) ???

    # verify alias does not exist
        for container in self.ps():
            if container['NAMES'] == container_alias:
                raise ValueError('%s(container_alias="%s") already exists. Try first: docker rm -f %s' % (title, container_alias, container_alias))

    # verify network exists
        network_exists = False
        for network in self.network_ls():
            if network['NAME'] == network_name:
                network_exists = True
        if network_name and not network_exists:
            raise ValueError('%s(network_name="%s") does not exist. Try first: docker network create %s' % (title, network_name, network_name))

    # verify system paths and compose absolute path mount map
        absolute_mounts = {}
        from os import path
        for key, value in mounted_volumes.items():
            if not path.exists(key):
                raise ValueError('%s(mounted_volume={%s:...}) is not a valid path on localhost.' % (title, key))
            absolute_path = path.abspath(key)
            if self.localhost.os.sysname == 'Windows':
                absolute_path = '"/%s"' % absolute_path
            else:
                absolute_path = '"%s"' % absolute_path
            absolute_mounts[absolute_path] = '"%s"' % value

    # compose run command
        sys_cmd = 'docker run --name %s' % container_alias
        for key, value in environmental_variables.items():
            sys_cmd += ' -e %s=%s' % (key.upper(), value)
        for key, value in mapped_ports.items():
            sys_cmd += ' -p %s:%s' % (key, value)
        for key, value in absolute_mounts.items():
            sys_cmd += ' -v %s:%s' % (key, value)
        if network_name:
            sys_cmd += ' --network %s' % network_name
        if run_flags:
            sys_cmd += ' %s' % run_flags.strip()
        sys_cmd += ' -d %s' % image_name
        if image_tag:
            sys_cmd += ':%s' % image_tag
        if start_command:
            sys_cmd += ' %s' % start_command.strip()

    # run run command
        output_lines = self.command(sys_cmd).split('\n')

        return output_lines[0]
    
if __name__ == '__main__':

# test docker client init
    from pprint import pprint
    docker_client = dockerClient()

# test docker list methods
    images = docker_client.images()
    print(images)
    containers = docker_client.ps()
    print(containers)
    networks = docker_client.network_ls()
    print(networks)
    remote_images = docker_client.search('alpine')
    print(remote_images)

# # test docker run
#     from labpack.records.settings import load_settings
#     docker_config = load_settings('../../data/test_docker.yaml')
#     container_id = docker_client.run(
#         image_name=docker_config['image_name'],
#         container_alias=docker_config['container_alias'],
#         environmental_variables=docker_config['envvar'],
#         mounted_volumes=docker_config['mounts'],
#         mapped_ports=docker_config['ports'],
#         start_command=docker_config['command']
#     )
#     print(container_id)
# 
# # wait for container to start
#     from time import sleep
#     sleep(1)

# test docker synopsis
    for container in containers:
        settings = docker_client.synopsis(container['CONTAINER ID'])
        pprint(settings)

# test enter and rm from separate script
    print('************\nRUN python test_platforms_docker_enter.py to test enter and rm functionality' )

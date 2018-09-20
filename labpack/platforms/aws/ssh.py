''' a class of methods to run commands on an active AWS instance '''
__author__ = 'rcj1492'
__created__ = '2015.10'
__license__ = 'MIT'

'''
PLEASE NOTE:    ssh package requires the paramiko and C package pycrypto on windows.

(windows)       download Visual Studio C++ Express
                pip3 install pycrypto

PLEASE NOTE:    pycrypto import process is corrupted and requires a correction
                https://github.com/dlitz/pycrypto/issues/110
                ..\site-packages\Crypto\Random\OSRNG\nt.py
                
PLEASE NOTE:    SCP protocol requires SCP installed on Remote Host

(aws-linux)     sudo yum install -y git
'''

from platform import uname
if uname().system in ('Windows'):
    try:
        import paramiko
        import scp
    except:
        import sys
        print('ssh package on Windows requires the paramiko module. try: pip3 install paramiko')
        sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError
from timeit import default_timer as timer
import tarfile

class sshClient(object):

    '''
        a class of methods to run commands on an active AWS instance

        NOTE:   Make sure that VPC rules allow SSH access to your local IP
        NOTE:   SCP protocol requires SCP installed on Remote Host
    '''

    _class_fields = {
        'schema': {
            'commands': [ 'ls -a' ],
            'login_name': 'ec2-user',
            'local_path': 'cred/dev/aws.yaml',
            'remote_path': '~/cred/aws.yaml',
            'port': 80,
            'timeout': 600
        },
        'components': {
            '.port': {
                'integer_data': True,
                'min_value': 1
            },
            '.timeout': {
                'integer_data': True,
                'min_value': 1
            }
        }
    }

    def __init__(self, instance_id, pem_file, access_id, secret_key, region_name, owner_id, user_name, login_name='', verbose=True):

        '''
            a method for initializing the SSH connection parameters to the EC2 instance

        :param instance_id: string with AWS id of instance
        :param pem_file: string with path to keypair pem file
        :param access_id: string with access_key_id from aws IAM user setup
        :param secret_key: string with secret_access_key from aws IAM user setup
        :param region_name: string with name of aws region
        :param owner_id: string with aws account id
        :param user_name: string with name of user access keys are assigned to
        :param login_name: [optional] string with name of login user
        :param verbose: boolean to enable process messages
        '''

        title = '%s.__init__' % self.__class__.__name__

    # initialize model
        from jsonmodel.validators import jsonModel
        self.fields = jsonModel(self._class_fields)

    # construct localhost client
        from labpack.platforms.localhost import localhostClient
        self.localhost = localhostClient()

    # validate credentials and construct ec2 method
        from labpack.platforms.aws.ec2 import ec2Client
        self.ec2 = ec2Client(access_id, secret_key, region_name, owner_id, user_name, verbose)

    # validate inputs
        input_fields = {
            'instance_id': instance_id,
            'pem_file': pem_file
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.ec2.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.instance_id = instance_id

    # verify pem file exists
        from os import path
        if not path.exists(pem_file):
            raise Exception('%s is not a valid path.' % pem_file)
        self.pem_file = path.abspath(pem_file)

    # verify user has privileges
        try:
            self.ec2.iam.printer_on = False
            self.ec2.list_keypairs()
        except AWSConnectionError as err:
            if str(err).find('Could not connect') > -1:
                raise
            raise AWSConnectionError(title, 'You must have privileges to access EC2 to use sshClient')

    # verify instance exists
        instance_list = self.ec2.list_instances()
        if instance_id not in instance_list:
            raise Exception('%s does not exist in this region or permission scope.' % instance_id)

    # verify instance has public ip
        instance_details = self.ec2.read_instance(instance_id)
        if not instance_details['public_ip_address']:
            raise Exception('%s requires a public IP address to access through ssh.' % instance_id)
        self.instance_ip = instance_details['public_ip_address']

    # retrieve login name from tag
        self.login_name = ''
        input_fields = {
            'login_name': login_name
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
                self.login_name = login_name
        if not self.login_name:
            for tag in instance_details['tags']:
                if tag['key'] == 'UserName':
                    self.login_name = tag['value']
        if not self.login_name:
            raise Exception('SSH access to %s requires a login_name argument or UserName tag' % instance_id)

    # verify local and remote pem file names match
        from os import path
        pem_absolute = path.abspath(pem_file)
        pem_root, pem_ext = path.splitext(pem_absolute)
        pem_path, pem_name = path.split(pem_root)
        if not instance_details['key_name'] == pem_name:
            raise Exception('%s does not match name of keypair %s for instance %s.' % (pem_name, instance_details['keypair'], instance_id))

    # verify instance is ready
        self.ec2.check_instance_status(instance_id)

    # verify security group allows ssh
        group_list = []
        for group in instance_details['security_groups']:
            group_list.append(group['group_id'])
        if not group_list:
            raise Exception('SSH access to %s requires a security group attached to instance.' % instance_id)
        port_22_list = []
        for group_id in group_list:
            group_details = self.ec2.read_security_group(group_id)
            for permission in group_details['ip_permissions']:
                if permission['from_port'] == 22:
                    port_22_list.extend(permission['ip_ranges'])
        if not port_22_list:
            raise Exception('SSH access to %s requires a security group with inbound permissions for port 22.' % instance_id)
        from labpack.records.ip import get_ip
        current_ip = get_ip()
        ssh_access = False
        for ip_range in port_22_list:
            if ip_range['cidr_ip'].find('0.0.0.0/0') > -1 or ip_range['cidr_ip'].find(current_ip) > -1:
                ssh_access = True
                break
        if not ssh_access:
            raise Exception('SSH access to %s requires your IP %s to be added to port 22 on its security group.' % (instance_id, current_ip))
        
    # verify pem file has access
        try:
            self.script('ls -a')
        except:
            raise AWSConnectionError(title, '%s does not have access to instance %s.' % (pem_name, instance_id))

    # verify scp
        self.scp = False
        
    # turn printer back on
        self.ec2.iam.printer_on = True

    def terminal(self, confirmation=True):

        '''
            method to open an SSH terminal inside AWS instance

        :param confirmation: [optional] boolean to prompt keypair confirmation
        :return: True
        '''

        title = '%s.terminal' % self.__class__.__name__

    # construct ssh command
        if confirmation:
            override_cmd = ' '
        else:
            override_cmd = ' -o CheckHostIP=no '
        sys_command = 'ssh -i %s%s%s@%s' % (self.pem_file, override_cmd, self.login_name, self.instance_ip)
        self.ec2.iam.printer(sys_command)

    # send shell script command to open up terminal
        if self.localhost.os.sysname in ('Windows'):
            raise Exception('%s is not supported on Windows. try using putty.exe')
        try:
            import os
            os.system(sys_command)
    # TODO: check into making sys_command OS independent
        except:
            raise AWSConnectionError(title)

        return True

    def script(self, commands, synopsis=True):

        '''
            a method to run a list of shell command scripts on AWS instance

        :param commands: list of strings with shell commands to pass through connection
        :param synopsis: [optional] boolean to simplify progress messages to one line
        :return: string with response to last command
        '''

        title = '%s.script' % self.__class__.__name__

    # validate inputs
        if isinstance(commands, str):
            commands = [commands]
        input_fields = {
            'commands': commands
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # run commands through paramiko on Windows
        response = ''
        if self.localhost.os.sysname in ('Windows'):
            ssh_key = paramiko.RSAKey.from_private_key_file(self.pem_file)
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.instance_ip, username=self.ec2.iam.user_name, pkey=ssh_key)
            for i in range(len(commands)):
                self.ec2.iam.printer('[%s@%s]: %s ... ' % (self.login_name, self.instance_ip, commands[i]), flush=True)
                std_in, std_out, std_err = client.exec_command(commands[i], get_pty=True)
                if std_err:
                    self.ec2.iam.printer('ERROR.')
                    raise Exception('Failure running [%s@%s]: %s\n%s' % (self.login_name, self.instance_ip, commands[i], std_err.decode('utf-8').strip()))
                else:
                    response = std_out.decode('utf-8')
                    if synopsis:
                        self.ec2.iam.printer('done.')
                    else:
                        if response:
                            self.ec2.iam.printer('\n%s' % response)
                        else:
                            self.ec2.iam.printer('done.')
            client.close()

    # run command through ssh on other platforms
        else:
            from subprocess import Popen, PIPE, STDOUT
            for i in range(len(commands)):
                self.ec2.iam.printer('[%s@%s]: %s ... ' % (self.login_name, self.instance_ip, commands[i]), flush=True)
                sys_command = 'ssh -i %s %s@%s %s' % (self.pem_file, self.login_name, self.instance_ip, commands[i])
                # DEBUG print(sys_command)
                pipes = Popen(sys_command.split(), stdout=PIPE, stderr=STDOUT)
            # automatically accept keys
                std_out, std_err = pipes.communicate('yes\n'.encode('utf-8'))
                if pipes.returncode != 0:
                    self.ec2.iam.printer('ERROR.')
                    raise Exception('Failure running [%s@%s]: %s\n%s' % (self.login_name, self.instance_ip, commands[i], std_out.decode('utf-8').strip()))

        # report response to individual commands
                else:
                    response = std_out.decode('utf-8')
                    if synopsis:
                        self.ec2.iam.printer('done.')
                    else:
                        if response:
                            self.ec2.iam.printer('\n%s' % response)
                        else:
                            self.ec2.iam.printer('done.')

    # close connection and return last response
        return response

    def put(self, local_path, remote_path='', overwrite=False, synopsis=True):

        '''
            a method to copy a folder or file from local device to AWS instance

        :param local_path: string with path to folder or file on local host
        :param remote_path: [optional] string with path to copy contents on remote host
        :param overwrite: [optional] boolean to enable file overwrite on remote host
        :param synopsis: [optional] boolean to simplify progress messages to one line
        :return: string with response
        '''

        title = '%s.put' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'local_path': local_path,
            'remote_path': remote_path
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)
        
    # verify local path exists
        from os import path
        if not path.exists(local_path):
            raise Exception('%s is not a valid path on local host.' % local_path)
        local_path_root, local_path_node = path.split(local_path)

    # verify remote root exists
        self.ec2.iam.printer_on = False
        if remote_path:
            remote_path_root, remote_path_node = path.split(remote_path)
            if not remote_path_root:
                remote_path_root = '~/'
                remote_path = path.join(remote_path_root, remote_path_node)
            remote_path_root = remote_path_root.replace(' ', '\ ')
            remote_path_node = remote_path_node.replace(' ', '\ ')
            test_root_cmd = 'cd %s' % remote_path_root
            try:
                self.script(test_root_cmd)
            except:
                raise ValueError('%s folder does not exist on remote host. Canceling transfer.' % remote_path_root)
            remote_path = remote_path.replace(' ', '\ ')
        else:
            from copy import deepcopy
            remote_path_node = deepcopy(local_path_node)
            remote_path_root = '~/'
            remote_path = '~/%s' % remote_path_node.replace(' ','\ ')

    # verify remote path does not exist
        if not overwrite:
            try:
                test_path_cmd = 'ls %s' % remote_path
                self.script(test_path_cmd)
            except Exception as err:
                pass
            else:
                raise ValueError('%s already exists on remote host. Canceling transfer.' % remote_path)

    # verify installation of scp on remote host
        if not self.scp:
            try:
                self.script('scp')
                self.scp = True
            except Exception as err:
                if str(err).find('usage: scp') > 1:
                    self.scp = True
                else:
                    raise Exception('SCP needs to be installed on remote host. Canceling transfer.\nOn remote host, try: sudo yum install -y git')

    # determine sudo privileges
        sudo_insert = 'sudo '
        user_abs = self.script('readlink -f ~/')
        remote_abs = self.script('readlink -f %s' % remote_path_root)
        if remote_abs.find(user_abs) > -1:
            sudo_insert = ''
        self.ec2.iam.printer_on = True

    # initiate transfer process
        remote_host = '[%s@%s]' % (self.login_name, self.instance_ip)
        if synopsis:
            self.ec2.iam.printer('Transferring %s to %s:%s ... ' % (local_path, remote_host, remote_path), flush=True)
            self.ec2.iam.printer_on = False
        self.ec2.iam.printer('Initiating transfer of %s to %s:%s.' % (local_path, remote_host, remote_path))

    # construct temporary file folder
        from labpack import __module__
        from labpack.storage.appdata import appdataClient
        client_kwargs = {
            'collection_name': 'TempFiles',
            'prod_name': __module__
        }
        tempfiles_client = appdataClient(**client_kwargs)

    # make local folder into a tar file
        from time import time
        tar_file = 'temp%s.tar.gz' % str(time())
        tar_path = path.join(tempfiles_client.collection_folder, tar_file)
        self.ec2.iam.printer('Creating temporary file %s ... ' % tar_file, flush=True)
        def _make_tar(source_path, output_file, content_name=''):
            kw_args = { 'name': source_path }
            if content_name:
                kw_args['arcname'] = content_name
            with tarfile.open(output_file, 'w:gz') as tar:
                tar.add(**kw_args)
        _make_tar(local_path, tar_path, remote_path_node)
        self.ec2.iam.printer('done.')

    # define cleanup function
        def _cleanup_temp(tar_file):
            self.ec2.iam.printer('Cleaning up temporary file %s ... ' % tar_file, flush=True)
            tempfiles_client.delete(tar_file)
            self.ec2.iam.printer('done.')

    # initiate scp transfer of tar file
        copy_msg = 'Copying %s to %s:~/%s ... ' % (tar_file, remote_host, tar_file)
        error_msg = 'Failure copying file %s to ip %s.' % (tar_file, self.instance_ip)

    # use paramiko on windows systems
        if self.localhost.os.sysname in ('Windows'):
            ssh_key = paramiko.RSAKey.from_private_key_file(self.pem_file)
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.instance_ip, username=self.ec2.iam.user_name, pkey=ssh_key)
            scp_transport = scp.SCPClient(client.get_transport())
            self.ec2.iam.printer(copy_msg, flush=True)
            try:
                response = scp_transport.put(tar_path, tar_file)
            except:
                self.ec2.iam.printer('ERROR.')
                _cleanup_temp(tar_file)
                raise Exception(error_msg)
            client.close()
            self.ec2.iam.printer('done.')

    # use scp on other systems
        else:
            self.ec2.iam.printer(copy_msg, flush=True)
            sys_command = 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o IdentityFile="%s" "%s" %s@%s:~/' % (self.pem_file, tar_path, self.login_name, self.instance_ip)
            from subprocess import check_output, CalledProcessError, STDOUT
            try:
                response = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                self.ec2.iam.printer('done.')
            except CalledProcessError as err:
                self.ec2.iam.printer('ERROR.')
                _cleanup_temp(tar_file)
                print(err)
                raise Exception(error_msg)

    # extract tar file to remote path
        extract_cmd = '%star -C %s -xvf %s' % (sudo_insert, remote_path_root, tar_file)
        ext_kwargs = {
            'commands': extract_cmd,
            'synopsis': True
        }
        try:
            self.script(**ext_kwargs)
        except:
            _cleanup_temp(tar_file)
            raise

    # cleanup temporary files on remote host
        rm_cmd = 'sudo rm -f %s' % tar_file
        rm_kwargs = {
            'commands': rm_cmd,
            'synopsis': True
        }
        try:
            self.script(**rm_kwargs)
        except:
            _cleanup_temp(tar_file)
            raise

    # cleanup local temporary files and return response
        _cleanup_temp(tar_file)
        self.ec2.iam.printer('Transfer of %s to %s:%s complete.' % (local_path, remote_host, remote_path))
        if synopsis:
            self.ec2.iam.printer_on = True
            self.ec2.iam.printer('done.')

        return response

    def get(self, remote_path, local_path='', overwrite=False, synopsis=True):

        '''
            a method to copy a folder or file from AWS instance to local device

        :param remote_path: string with path to copy contents on remote host
        :param local_path: [optional] string with path to folder or file on local host
        :param overwrite: [optional] boolean to enable file overwrite on remote host
        :param synopsis: [optional] boolean to simplify progress messages to one line
        :return: string with response
        '''

        title = '%s.transfer' % self.__class__.__name__

    # validate inputs
        input_fields = {
            'local_path': local_path,
            'remote_path': remote_path
        }
        for key, value in input_fields.items():
            if value:
                object_title = '%s(%s=%s)' % (title, key, str(value))
                self.fields.validate(value, '.%s' % key, object_title)

    # verify remote path exists
        from os import path
        self.ec2.iam.printer_on = False
        try:
            test_path_cmd = 'ls %s' % remote_path.replace(' ','\ ')
            self.script(test_path_cmd)
        except:
            raise ValueError('%s does not exist on remote host. Canceling transfer.' % remote_path)
        self.ec2.iam.printer_on = True
        remote_path_root, remote_path_node = path.split(remote_path)
        if not remote_path_root:
            remote_path_root = '~/'
        remote_path = remote_path.replace(' ', '\ ')
        remote_path_root = remote_path_root.replace(' ','\ ')

    # verify local root exists
        if local_path:
            local_path_root, local_path_node = path.split(local_path)
            if not local_path_root:
                local_path_root = './'
                local_path = path.join(local_path_root, local_path_node)
            if not path.exists(local_path_root):
                raise ValueError('%s folder does not exist on localhost. Canceling transfer.' % local_path_root)
        else:
            from copy import deepcopy
            local_path_node = deepcopy(remote_path_node)
            local_path = path.join('./', local_path_node)
            local_path_root = './'
        remote_path_node = remote_path_node.replace(' ', '\ ')
    
    # verify local path does not exist
        if not overwrite:
            if path.exists(local_path):
                raise ValueError('%s already exists on localhost. Canceling transfer.' % local_path)

    # verify installation of scp on remote host
        self.ec2.iam.printer_on = False
        if not self.scp:
            try:
                self.script('scp')
                self.scp = True
            except Exception as err:
                if str(err).find('usage: scp') > 1:
                    self.scp = True
                else:
                    raise Exception('SCP needs to be installed on remote host. Canceling transfer.\nOn remote host, try: sudo yum install -y git')

    # determine sudo privileges
        sudo_insert = 'sudo '
        user_abs = self.script('readlink -f ~/')
        remote_abs = self.script('readlink -f %s' % remote_path_root)
        if remote_abs.find(user_abs) > -1:
            sudo_insert = ''
        self.ec2.iam.printer_on = True

    # initiate transfer process
        remote_host = '[%s@%s]' % (self.login_name, self.instance_ip)
        if synopsis:
            self.ec2.iam.printer('Transferring %s:%s to %s ... ' % (remote_host, remote_path, local_path), flush=True)
            self.ec2.iam.printer_on = False
        self.ec2.iam.printer('Initiating transfer of %s:%s to %s ... ' % (remote_host, remote_path, local_path))

    # construct temporary file folder on localhost
        from labpack import __module__
        from labpack.storage.appdata import appdataClient
        client_kwargs = {
            'collection_name': 'TempFiles',
            'prod_name': __module__
        }
        tempfiles_client = appdataClient(**client_kwargs)

    # make remote folder into a tar file
        from time import time
        tar_file = 'temp%s.tar.gz' % str(time())
        local_tar_path = path.join(tempfiles_client.collection_folder, tar_file)
        remote_tar_path = path.join('~/', tar_file)
        self.ec2.iam.printer('Creating temporary file %s:%s ... ' % (remote_host, remote_tar_path))
        create_command = '%star -czf %s -C %s %s' % (sudo_insert, remote_tar_path, remote_path_root, remote_path_node)
        self.script(create_command) 

    # define cleanup functions
        def _cleanup_local(tar_file, local_tar_path):
            self.ec2.iam.printer('Cleaning up temporary file %s ... ' % local_tar_path, flush=True)
            tempfiles_client.delete(tar_file)
            self.ec2.iam.printer('done.')
        def _cleanup_remote(remote_host, tar_path):
            self.ec2.iam.printer('Cleaning up temporary file %s:%s ... ' % (remote_host, tar_path))
            self.script('rm %s' % tar_path)
            
    # initiate scp transfer of tar file
        copy_msg = 'Copying %s:%s to %s ... ' % (remote_host, remote_tar_path, local_tar_path)
        error_msg = 'Failure copying file %s:%s to localhost.' % (remote_host, remote_tar_path)

    # use paramiko on windows systems
        if self.localhost.os.sysname in ('Windows'):
            ssh_key = paramiko.RSAKey.from_private_key_file(self.pem_file)
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.instance_ip, username=self.ec2.iam.user_name, pkey=ssh_key)
            scp_transport = scp.SCPClient(client.get_transport())
            self.ec2.iam.printer(copy_msg, flush=True)
            try:
                response = scp_transport.get(remote_tar_path, local_tar_path)
            except:
                self.ec2.iam.printer('ERROR.')
                _cleanup_remote(remote_host, remote_tar_path)
                raise Exception(error_msg)
            client.close()
            self.ec2.iam.printer('done.')

    # use scp on other systems
        else:
            self.ec2.iam.printer(copy_msg, flush=True)
            sys_command = 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o IdentityFile="%s" %s@%s:%s "%s"' % (self.pem_file, self.login_name, self.instance_ip, remote_tar_path, local_tar_path)
            from subprocess import check_output, CalledProcessError, STDOUT
            try:
                response = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                self.ec2.iam.printer('done.')
            except CalledProcessError as err:
                self.ec2.iam.printer('ERROR.')
                _cleanup_remote(remote_host, remote_tar_path)
                print(err)
                raise Exception(error_msg)

    # extract tar file to local path and rename directory
        try:
            import tarfile
            with tarfile.open(local_tar_path, 'r:gz') as tar:
                tar.extractall(local_path_root)
                tar.close()
            if local_path_node.replace(' ','\ ') != remote_path_node:
                from shutil import move
                src = path.join(local_path_root, remote_path_node)
                dst = path.join(local_path_root, local_path_node)
                move(src, dst)
        except Exception as err:
            self.ec2.iam.printer('ERROR.')
            _cleanup_remote(remote_host, remote_tar_path)
            _cleanup_local(tar_file, local_tar_path)
            print(err)
            raise Exception(error_msg)
            
    # cleanup temporary files
        _cleanup_remote(remote_host, remote_tar_path)
        _cleanup_local(tar_file, local_tar_path)

    # return response
        self.ec2.iam.printer('Transfer of %s:%s to %s complete.' % (remote_host, remote_path, local_path))
        if synopsis:
            self.ec2.iam.printer_on = True
            self.ec2.iam.printer('done.')

        return response

    def responsive(self, port=80, timeout=600):

        '''
            a method for waiting until web server on AWS instance has restarted

        :param port: integer with port number to check
        :param timeout: integer with number of seconds to continue to check
        :return: string with response code
        '''

        title = '%s.wait' % self.__class__.__name__

        from time import sleep

    # validate inputs
        input_fields = {
            'port': port,
            'timeout': timeout
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.fields.validate(value, '.%s' % key, object_title)

    # construct parameters for request loop
        import requests
        waiting_msg = 'Waiting for http 200 response from %s' % self.instance_ip
        nonres_msg = 'Instance %s is not responding to requests at %s.' % ( self.instance_id, self.instance_ip)
        server_url = 'http://%s' % self.instance_ip
        if port:
            server_url += ':%s' % str(port)

    # initiate waiting loop
        self.ec2.iam.printer(waiting_msg, flush=True)
        t0 = timer()
        while True:
            t1 = timer()
            self.ec2.iam.printer('.', flush=True)
            try:
                response = requests.get(server_url, timeout=2)
                response_code = response.status_code
                if response_code >= 200 and response_code < 300:
                    self.ec2.iam.printer(' done.')
                    return response_code
            except:
                pass
            t2 = timer()
            if t2 - t0 > timeout:
                timeout_msg = 'Timeout [%ss]: %s' % (timeout, nonres_msg)
                raise TimeoutError(timeout_msg)
            response_time = t2 - t1
            if 3 - response_time > 0:
                delay = 3 - response_time
            else:
                delay = 0
            sleep(delay)

if __name__ == '__main__':

# retrieve credentials
    from labpack.records.settings import load_settings
    from labpack.platforms.aws.ec2 import ec2Client
    pem_folder = '../../../keys'
    cred_path = '../../../../cred/awsLab.yaml'
    aws_cred = load_settings(cred_path)

# determine active test instance properties
    client_kwargs = {
        'access_id': aws_cred['aws_access_key_id'],
        'secret_key': aws_cred['aws_secret_access_key'],
        'region_name': aws_cred['aws_default_region'],
        'owner_id': aws_cred['aws_owner_id'],
        'user_name': aws_cred['aws_user_name'],
        'verbose': False
    }
    ec2_client = ec2Client(**client_kwargs)
    instance_list = ec2_client.list_instances(tag_values=['test'])
    if not instance_list:
        raise Exception('There are no test instances running.')
    instance_id = instance_list[0]
    instance_details = ec2_client.read_instance(instance_id)
    pem_name = instance_details['key_name']
    from os import path
    pem_file = path.join(pem_folder, '%s.pem' % pem_name)
    if not path.exists(pem_file):
        raise Exception('Instance pem key %s.pem does not exist in keys folder.' % pem_name)

# initialize ssh client
    client_kwargs['instance_id'] = instance_id
    client_kwargs['pem_file'] = pem_file
    del client_kwargs['verbose']
    ssh_client = sshClient(**client_kwargs)

# test responsive method
    assert ssh_client.responsive() == 200

# run test scripts
    ssh_client.script('mkdir test20170615; touch test20170615/newfile.txt')
    ssh_client.script('rm -rf test20170615')

# run test transfers
    from os import remove
    from shutil import rmtree
    local_file = '../../../tests/test-model.json'
    local_folder = '../../../tests/testing'
    incoming_folder = '../../../tests/test-incoming/'
    spaces_file = '../../../tests/test space.sh'
    spaces_folder = '../../../tests/test space'
    spaces_subfolder = path.join(spaces_folder, 'test space.sh')
    remote_file = 'test-model2.json'
    remote_folder = 'testing2'
    ssh_client.put(local_file)
    ssh_client.script('rm test-model.json')
    ssh_client.put(local_file, remote_file)
    ssh_client.get(remote_file, path.join(incoming_folder, remote_file))
    ssh_client.script('rm test-model2.json')
    remove(path.join(incoming_folder, remote_file))    
    ssh_client.put(local_folder)
    ssh_client.script('rm -r testing')
    ssh_client.put(local_folder, remote_folder)
    ssh_client.get(remote_folder, path.join(incoming_folder, 'testing'))
    ssh_client.script('rm -r testing2')
    rmtree(path.join(incoming_folder, 'testing'))    

# run test transfer with sudo
    ssh_client.put(local_folder, '/home/testing')
    ssh_client.get('/home/testing', path.join(incoming_folder, 'testing2'))
    ssh_client.script('sudo rm -r /home/testing')
    rmtree(path.join(incoming_folder, 'testing2'))

# run test transfer with space
    ssh_client.put(spaces_file)
    ssh_client.put(spaces_subfolder, overwrite=True)
    ssh_client.put(spaces_folder)
    ssh_client.put(spaces_subfolder, remote_path='~/test space/test space.sh', overwrite=True)
    ssh_client.get('test space.sh', path.join(incoming_folder, 'test space.sh'))
    ssh_client.get('test space', path.join(incoming_folder, 'test space'))
    ssh_client.get('~/test space/test space.sh', path.join(incoming_folder, 'test space/test space.sh'), overwrite=True)
    ssh_client.script('rm -r "test space"')
    ssh_client.script('rm "test space.sh"')
    rmtree(path.join(incoming_folder, 'test space'))
    remove(path.join(incoming_folder, 'test space.sh'))



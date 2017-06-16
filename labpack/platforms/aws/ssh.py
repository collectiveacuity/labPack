''' a class of methods to run commands on an active AWS instance '''
__author__ = 'rcj1492'
__created__ = '2015.10'
__license__ = 'MIT'

'''
PLEASE NOTE:    ssh package requires the paramiko and C package pycrypto.

(linux)         pip3 install paramiko

(windows)       download Visual Studio C++ Express
                pip3 install pycrypto

PLEASE NOTE:    pycrypto import process is corrupted and requires a correction
                https://github.com/dlitz/pycrypto/issues/110
                ..\site-packages\Crypto\Random\OSRNG\nt.py
                
PLEASE NOTE:    SCP protocol requires SCP installed on Remote Host

(aws-linux)     sudo yum install -y git
'''

try:
    import paramiko
    import scp
except:
    import sys
    print('ssh package requires the paramiko module. try: pip3 install paramiko')
    sys.exit(1)

from labpack.authentication.aws.iam import AWSConnectionError
from urllib.request import urlopen, HTTPError
from urllib.error import URLError
import socket
from timeit import default_timer as timer
import time
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
            'login_name': 'ec2-user'
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

    # verify user has privileges
        try:
            self.ec2.iam.printer_on = False
            self.ec2.list_keypairs()
        except:
            raise AWSConnectionError(title, 'You must have privileges to access EC2 to use sshClient')

    # validate inputs
        input_fields = {
            'instance_id': instance_id,
            'pem_file': pem_file
        }
        for key, value in input_fields.items():
            object_title = '%s(%s=%s)' % (title, key, str(value))
            self.ec2.fields.validate(value, '.%s' % key, object_title)

    # construct class properties
        self.pem_file = pem_file
        self.instance_id = instance_id

    # verify pem file exists
        from os import path
        if not path.exists(pem_file):
            raise Exception('%s is not a valid path.' % pem_file)

    # verify instance exists
        instance_list = self.ec2.list_instances()
        if instance_id not in instance_list:
            raise Exception('%s does not exist in this region or permission scope.' % instance_id)

    # verify instance has public ip
        instance_details = self.ec2.read_instance(instance_id)
        if not instance_details['public_ip']:
            raise Exception('%s requires a public IP address to access through ssh.' % instance_id)
        self.instance_ip = instance_details['public_ip']

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
                if tag['Key'] == 'LoginName':
                    self.login_name = tag['Value']
        if not self.login_name:
            raise Exception('SSH access to %s requires a login_name argument or LoginName tag' % instance_id)

    # verify local and remote pem file names match
        from os import path
        pem_absolute = path.abspath(pem_file)
        pem_root, pem_ext = path.splitext(pem_absolute)
        pem_path, pem_name = path.split(pem_root)
        if not instance_details['keypair'] == pem_name:
            raise Exception('%s does not match name of keypair %s for instance %s.' % (pem_name, instance_details['keypair'], instance_id))

    # verify instance is ready
        self.ec2.check_instance_status(instance_id)

    # verify pem file has access
        try:
            self.script(['ls -a'])
        except:
            raise AWSConnectionError(title, '%s does not have access to instance %s.' % (pem_name, instance_id))

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

    def script(self, commands, synopsis=False, raise_errors=True):

        '''
            a method to run a list of shell command scripts on AWS instance

        :param commands: list of strings with shell commands to pass through connection
        :param synopsis: [optional] boolean to simply responses to done.
        :param raise_errors: [optional] boolean to raise errors
        :return: string with response to last command
        '''

        title = '%s.script' % self.__class__.__name__

    # validate inputs
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
                self.ec2.iam.printer('[%s@%s]: %s ...' % (self.login_name, self.instance_ip, commands[i]), flush=True)
                std_in, std_out, std_err = client.exec_command(commands[i], get_pty=True)
                if std_err:
                    self.ec2.iam.printer(' ERROR.')
                    if raise_errors:
                        raise Exception('Failure running [%s@%s]: %s\n%s' % (self.login_name, self.instance_ip, commands[i], std_err.decode('utf-8').strip()))
                    else:
                        response = std_err.decode('utf-8')
                else:
                    response = std_out.decode('utf-8')
                    if synopsis:
                        self.ec2.iam.printer(' done.')
                    else:
                        if response:
                            self.ec2.iam.printer('\n%s' % response)
                        else:
                            self.ec2.iam.printer(' done.')
            client.close()

    # run command through ssh on other platforms
        else:
            from subprocess import Popen, PIPE
            for i in range(len(commands)):
                self.ec2.iam.printer('[%s@%s]: %s ...' % (self.login_name, self.instance_ip, commands[i]), flush=True)
                sys_command = 'ssh -oStrictHostKeyChecking=no -i %s %s@%s %s' % (self.pem_file, self.login_name, self.instance_ip, commands[i])
                pipes = Popen(sys_command.split(), stdout=PIPE, stderr=PIPE)
                std_out, std_err = pipes.communicate()
                if pipes.returncode != 0:
                    self.ec2.iam.printer(' ERROR.')
                    if raise_errors:
                        raise Exception('Failure running [%s@%s]: %s\n%s' % (self.login_name, self.instance_ip, commands[i], std_err.decode('utf-8').strip()))
                    else:
                        response = std_err.decode('utf-8')

        # report response to individual commands
                else:
                    response = std_out.decode('utf-8')
                    if synopsis:
                        self.ec2.iam.printer(' done.')
                    else:
                        if response:
                            self.ec2.iam.printer('\n%s' % response)
                        else:
                            self.ec2.iam.printer(' done.')

    # close connection and return last response
        return response

    def transfer(self, content, local='', remote='', quiet=False):

        '''
            a method to copy a folder or file from local device to AWS instance

        :param content: string with name of file to copy
        :param local: [optional] string with path to folder or file on local device
        :param remote: [optional] string with path to place folder or file on remote device
        :param quiet: [optional] boolean to silence command sequence
        :return: True
        '''

        title = 'transfer'

    # validate inputs
        self.methods.input.string(input=content, bad_char_list=['/'], title=title + ' file')
        local_path = './' + content
        remote_path = './'
        if local:
            local = self.methods.input.path(local, title + ' local')
            local_path = local + content
        if remote:
            remote = self.methods.input.path(remote, title + ' remote')
            remote_path = remote

    # validate existence of file and remote path
        if not os.path.exists(local_path):
            raise ValueError('\nFile %s does not exist in local path %s' % (content, local_path))
        test_path_cmd = 'cd ' + remote_path
        response = self.script([test_path_cmd], quiet=True)
        if response:
            raise ValueError('\nPath %s does not exist on instance. Canceling transfer.' % remote_path)

    # validate installation of scp on remote host
        response = self.script(['scp'], quiet=True)
        valid_response = re.compile('usage')
        if not valid_response.match(response):
            raise Exception('\nSCP needs to be installed on remote host. Canceling transfer.')

    # make local folder into a tar file
        tar_file = 'temp.tar.gz'
        if not quiet:
            print('Creating temporary file %s ...' % tar_file, end='', flush=True)
        def makeTar(source_path, output_file, content_name=''):
            kw_args = { 'name': source_path }
            if content_name:
                kw_args['arcname'] = content_name
            with tarfile.open(output_file, 'w:gz') as tar:
                tar.add(**kw_args)
        makeTar(local_path, tar_file, content)
        if not quiet:
            print(' Done.')

    # construct paramiko scp transport
        ssh_key = paramiko.RSAKey.from_private_key_file(self.pemFile)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.instanceIP, username=self.userName, pkey=ssh_key)
        scpTransport = scp.SCPClient(client.get_transport())

    # initiate scp transfer
        if not quiet:
            print('Transferring %s to %s:~/%s ...' % (tar_file, self.instanceIP, tar_file), end='', flush=True)
        try:
            scpTransport.put(tar_file, tar_file)
        except:
            raise Exception('\nFailure to copy file %s to ip %s.\nCheck to see if scp has been installed on remote host.' % (tar_file, self.instanceIP))
        if not quiet:
            print(' Done.')
        client.close()

    # extract tar file to remote path
        extract_cmd = 'sudo tar -C %s -xvf %s' % (remote_path, tar_file)
        ext_args = {
            'commands': [extract_cmd],
            'quiet': quiet
        }
        if not quiet:
            ext_args['synopsis'] = True
        self.script(**ext_args)

    # cleanup temporary files and return True
        rm_cmd = 'sudo rm -f %s' % tar_file
        rm_args = {
            'commands': [rm_cmd],
            'quiet': quiet
        }
        if not quiet:
            rm_args['synopsis'] = True
        self.script(**rm_args)
        if not quiet:
            print('Cleaning up temporary file %s ...' % tar_file, end='', flush=True)
        os.remove(tar_file)
        if not quiet:
            print(' Done.')
        return True

    def responsive(self, port=0):

        '''
            a method for waiting until web server on AWS instance has restarted

        :return: True
        '''

        title = 'wait'

    # construct parameters of request loop
        response_200 = False
        print('Waiting for http 200 response from %s' % self.instanceIP, end='', flush=True)
        delay = 3
        status_timeout = 0
        url = 'http://' + self.instanceIP
        if port:
            if isinstance(port, int):
                url += ':%s' % port

    # repeat http requests to public ip until 200 response code
        while not response_200:
            print('.', end='', flush=True)
            t3 = timer()
            try:
                response = urlopen(url, timeout=2)
                response_code = response.getcode()
                response.close()
            except HTTPError as err:
                response_code = err.getcode()
            except URLError as err:
                response_code = err.reason
            except socket.timeout as err:
                print(err.strerror)
                response_code = err.strerror
            t4 = timer()
            response_time = t4 - t3
            if 3 - response_time > 0:
                delay = 3 - response_time
            else:
                delay = 0
            if response_code == 200:
                print(' Done.')
                response_200 = True
            else:
                time.sleep(delay)

    # set a timeout condition
            status_timeout += 1
            if status_timeout > 299:
                total_sec = status_timeout * delay
                raise Exception('\nTimeout [%ss]: Instance %s is not responding to requests at %s.' % (total_sec, self.instanceID, self.instanceIP))
        return True

    def unitTests(self):
        # self.terminal(confirmation=False)
        self.script(['sudo yum update -y', 'sudo yum install -y git'], synopsis=True)
        self.script(['mkdir test'])
        self.transfer('new', '../data/', 'test/')
        # self.responsive()
        return self

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
    pem_name = instance_details['keypair']
    from os import path
    pem_file = path.join(pem_folder, '%s.pem' % pem_name)
    if not path.exists(pem_file):
        raise Exception('Instance pem key %s.pem does not exist in keys folder.' % pem_name)

# initialize ssh client
    client_kwargs['instance_id'] = instance_id
    client_kwargs['pem_file'] = pem_file
    del client_kwargs['verbose']
    ssh_client = sshClient(**client_kwargs)

# run test scripts
    ssh_client.script(['mkdir test20170615; touch test20170615/newfile.txt'])
    ssh_client.script(['rm -rf test20170615'])


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

    def __init__(self, instance_id, pem_file, access_id, secret_key, region_name, owner_id, user_name, verbose=True):

        '''
            a method for initializing the SSH connection parameters to the EC2 instance

        :param instance_id: string with AWS id of instance
        :param pem_file: string with path to keypair pem file
        :param access_id: string with access_key_id from aws IAM user setup
        :param secret_key: string with secret_access_key from aws IAM user setup
        :param region_name: string with name of aws region
        :param owner_id: string with aws account id
        :param user_name: string with name of user access keys are assigned to
        :param verbose: boolean to enable process messages
        '''

        title = '%s.__init__' % self.__class__.__name__

    # validate credentials and construct ec2 method
        from labpack.platforms.aws.ec2 import ec2Client
        self.ec2 = ec2Client(access_id, secret_key, region_name, owner_id, user_name, verbose)

    # verify user has privileges
        try:
            self.ec2.iam.printer = self.ec2.iam.printer_off
            # self.ec2.list_keypairs()
            self.ec2.iam.printer = self.ec2.iam.printer_on
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

    # verify pem file exists

    # verify instance exists

    # verify instance has public ip

    # verify local and remote pem file names match

    # verify pem file has access

    # verify instance is ready



    def terminal(self, confirmation=True):

        '''
            method to open an SSH terminal inside AWS instance

        :param confirmation: [optional] boolean to prompt keypair confirmation
        :return: True
        '''

        title = 'terminal'

    # construct ssh command
        login_address = self.userName + '@' + self.instanceIP
        if confirmation:
            override_cmd = ' '
        else:
            override_cmd = ' -o CheckHostIP=no '
        sys_command = 'ssh -i %s%s%s' % (self.pemFile, override_cmd, login_address)
        print(sys_command)

    # send shell script command to open up terminal
        try:
            os.system(sys_command)
    # TODO: check into making sys_command OS independent
        except:
            raise Exception('\nFailure connecting to AWS instance ip %s with %s request.' % (self.instanceIP, title))

        return True

    def script(self, commands, quiet=False, synopsis=False):

        '''
            a method to run a list of shell command scripts on AWS instance

        :param commands: list of strings with shell commands to pass through connection
        :param quiet: [optional] boolean to silence command sequence
        :param synopsis: [optional] boolean to simply responses to Done.
        :return: string with response to last command
        '''

        title = 'script'

    # validate inputs
        self.methods.input.shellCommands(commands, title + ' commands')

    # construct paramiko connection
        ssh_key = paramiko.RSAKey.from_private_key_file(self.pemFile)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.instanceIP, username=self.userName, pkey=ssh_key)

    # run command through connection
        response = ''
        for i in range(len(commands)):
            if not quiet:
                print('[%s]: %s ...' % (self.instanceIP, commands[i]), end='', flush=True)
            try:
                stdin, stdout, stderr = client.exec_command(commands[i], get_pty=True)
            except:
                raise Exception('\nFailure connecting to AWS instance ip %s with %s command [%s] request.' % (self.instanceIP, title, i))

    # report response to individual commands
            response = stdout.read().decode()
            if quiet:
                pass
            else:
                if synopsis:
                    print(' Done.')
                else:
                    if response:
                        response = response.replace('\n', '')
                        print('\n%s' % response)
                    else:
                        print(' Done.')

    # close connection and return last response
        client.close()
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

    from labpack.records.settings import load_settings
    test_cred = load_settings('../../../../cred/awsLab.yaml')
    client_kwargs = {
        'instance_id': 'i-04ab8722c7b2a3ea7',
        'pem_file': '../../../keys/lab-keypair-useast2-test-20170601.pem',
        'access_id': test_cred['aws_access_key_id'],
        'secret_key': test_cred['aws_secret_access_key'],
        'region_name': test_cred['aws_default_region'],
        'owner_id': test_cred['aws_owner_id'],
        'user_name': test_cred['aws_user_name']
    }
    ssh_client = sshClient(**client_kwargs)


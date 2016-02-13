__author__ = 'rcj1492'
__created__ = '2015'

# pip install paramiko
# https://pypi.python.org/pypi/paramiko/1.15.2
# pip install scp
# https://pypi.python.org/pypi/scp/0.7.0

# NOTE: copyToRemote fails if SCP isn't installed on remote host.
# NOTE: installation of git will import scp

from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.request import HTTPError
from urllib.error import URLError
import time
import json
import os
import re
import paramiko
import scp

class sshInputTest(object):
    '''
        a class of methods to validate inputs associated with ssh
        import re
    '''
    @classmethod
    def pemFile(self, pem_file):
        pem_filetype = re.compile('.pem')
        if not isinstance(pem_file, str):
            raise Exception('\npem_file input must be a string')
        elif not pem_filetype.search(pem_file):
            raise Exception('\npem_file is not a valid .pem file type')
        else:
            return pem_file

    @classmethod
    def validURL(self, url):
        pattern1 = re.compile('https?://')
        pattern2 = re.compile('[\w\-]+\.[a-z]{2}')
        pattern4 = re.compile('[^0-9a-zA-Z/:=_,&~@#\.\-\?\+\$]+')
        if not isinstance(url, str):
            raise Exception('\nurl input must be a string')
        elif pattern4.findall(url):
            raise Exception('\nurl input contains invalid characters')
        elif not pattern1.match(url) and not pattern2.search(url):
            raise Exception('\nurl input does not have valid url syntax')
        else:
            return url

    @classmethod
    def ipAddress(self, ip_address):
        ipv4pattern = re.compile('\d+.\d+.\d+.\d+')
        ipv6pattern = re.compile('[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F]+:[0-9a-fA-F:]*:[0-9a-fA-F]+$')
        if not isinstance(ip_address, str):
            raise Exception('\nip_address input is not a string')
        elif not ipv6pattern.match(ip_address) and not ipv4pattern.match(ip_address):
            if not self.validURL(ip_address):
                raise Exception('\nip_address input is not a valid internet address')
            else:
                return ip_address
        else:
            return ip_address

    @classmethod
    def shellCommands(self, command_list):
        if not isinstance(command_list, list):
            raise Exception('\ncommand_list must be a list')
        for command in command_list:
            if not isinstance(command, str):
                raise Exception('\ncommands in command_list must be strings')
        return command_list

    @classmethod
    def fileName(self, file_name):
        if not isinstance(file_name, str):
            raise Exception('\nfile_name must be a string')
        return file_name

    @classmethod
    def unitTests(self):
        testFileRepo = 'https://username:password@bitbucket.org/docker.git'
        assert sshInputTest.pemFile('aws-key-example.pem')
        assert sshInputTest.ipAddress(testFileRepo)
        assert sshInputTest.ipAddress('8.8.8.8')
        assert sshInputTest.ipAddress('2001:db8:85a3:8d3:1319:8a2e:370:7348')
        assert sshInputTest.ipAddress('2001:4860:4860::8888')
        assert sshInputTest.ipAddress('ec2-52-3-164-75.compute-1.amazonaws.com')
        assert sshInputTest.ipAddress('52.3.164.75')
        assert sshInputTest.shellCommands(['ls', 'mkdir test', 'cd test'])
        assert sshInputTest.fileName('README')
        return True

class labHTTP(object):
    '''
        a class of methods for making http requests
        from urllib.request import urlopen
        from urllib.parse import urlencode
        import time
        import json
    '''
    @classmethod
    def getHTML(self, url):
        '''
            a method for getting the html from a url
        '''
    # validate input
        if not url:
            raise Exception('required parameters are missing')
        else:
            url = sshInputTest.ipAddress(url)
            http_pattern = re.compile('https?://')
            if not http_pattern.search(url):
                url = 'http://' + url
    # send request
            try:
                response = urlopen(url, timeout=2)
                response = response.read().decode('utf-8')
            except HTTPError as err:
                response = err.getcode()
            except URLError as err:
                response = err.reason
            return response

    @classmethod
    def getResponseCode(self, url):
        '''
            a method for getting the response code from a url
        '''
    # validate input
        if not url:
            raise Exception('required parameters are missing')
        else:
            url = sshInputTest.ipAddress(url)
            http_pattern = re.compile('https?://')
            if not http_pattern.search(url):
                url = 'http://' + url
    # send request
            try:
                response = urlopen(url, timeout=2)
                response_code = response.getcode()
                response.close()
            except HTTPError as err:
                response_code = err.getcode()
            except URLError as err:
                response_code = err.reason
            return response_code

    @classmethod
    def getJSON(self, url, params, headers=None):
        if not url or not params:
            raise Exception('required parameters are missing')
        elif not isinstance(url, str):
            raise Exception('url must be a string')
        elif not isinstance(params, dict):
            raise Exception('params must be a dictionary')
        else:
            GET_url = url + '?%s'
            GET_params = urlencode(params)
            if headers:
                if isinstance(headers, dict):
                    GET_headers = headers
            print(time.perf_counter())
            response = urlopen(GET_url % GET_params)
            print(time.perf_counter())
            data = json.loads(response.read().decode('utf-8'))
            return data

    @classmethod
    def postJSON(self, url, params, headers=None):
        if not url or not params:
            raise Exception('required parameters are missing')
        elif not isinstance(url, str):
            raise Exception('url must be a string')
        elif not isinstance(params, dict):
            raise Exception('params must be a dictionary')
        else:
            POST_url = url
            POST_params = urlencode(params).encode('utf-8')
            if headers:
                if isinstance(headers, dict):
                    POST_headers = headers
            print(time.perf_counter())
            response = urlopen(POST_url, POST_params)
            print(time.perf_counter())
            data = json.loads(response.read().decode('utf-8'))
            return data

    @classmethod
    def unitTests(self):
        '''
            a method for running unit tests on the labHTTP class
        '''
        assert labHTTP.getResponseCode('www.google.com') == 200
        assert labHTTP.getResponseCode('www.google.com/probablyNotAWebpage-123') == 404
        return True
# TODO: create unitTests method for labHTTP class

class labSSH(object):
    '''
        a class of methods for interacting with a remote host through SSH
        import paramiko
        import os
        import re
        import scp
    '''
    def __init__(self, user_name, ip_address, pem_file, auth_override=False):
        '''
            a method for initializing an SSH connection with public key authentication
        :param user_name: string with user name login
        :param ip_address: string with ip address of host server
        :param pem_file: string with pem file (and path) for login cred
        :param auth_override: [optional] boolean to override host key confirmation
        :return:
        '''
        if ip_address and user_name and pem_file:
            if isinstance(user_name, str):
                pem_file = sshInputTest.pemFile(pem_file)
                ip_address = sshInputTest.ipAddress(ip_address)
                login_address = user_name + '@' + ip_address
                if auth_override:
                    override_cmd = ' -o CheckHostIP=no '
                else:
                    override_cmd = ' '
                try:
                    sys_command = 'ssh -i ' + pem_file + override_cmd + login_address
                    print(sys_command)
                    os.system(sys_command)
    # TODO: check into making sys_command can be OS independent
                except:
                    raise Exception('\nFailure to connect to instance.')

    @classmethod
    def runCommand(self, user_name, ip_address, pem_file, shell_command, read_out=False):
        '''
            a method for running a sequence of script commands through SSH
        :param user_name: string with user name login
        :param ip_address: string with ip address of host server
        :param pem_file: string with pem file (and path) for login cred
        :param shell_command: string with shell command to pass through connection
        :param read_out: boolean to determine whether response is printed
        :return: string with response from remote host
        '''
    # validate input
        if not ip_address or not user_name or not pem_file or not shell_command:
            raise Exception('\ninput lacks all required parameters')
        elif not isinstance(user_name, str):
            raise Exception('\nuser_name must be a string')
        elif not isinstance(shell_command, str):
            raise Exception('\nshell_command must be a string')
        else:
            ip_address = sshInputTest.ipAddress(ip_address)
            pem_file = sshInputTest.pemFile(pem_file)
    # print out shell command
            print('Running: %s ...' % shell_command, end='', flush=True)
    # open up ssh connection to host
            try:
                ssh_key = paramiko.RSAKey.from_private_key_file(pem_file)
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=ip_address, username=user_name, pkey=ssh_key)
    # run command through ssh connection
                stdin, stdout, stderr = client.exec_command(shell_command, get_pty=True)
                response = stdout.read().decode()
                if read_out:
                    if response:
                        print('\n' + response)
                    else:
                        print(' DONE.')
                else:
                    print(' DONE.')
                if stderr.readlines():
                    print('ERROR Reported: ' + stderr.readlines())
                client.close()
                return response
            except:
                raise Exception('\nFailure to connect to instance.')

    @classmethod
    def copyToRemote(self, user_name, ip_address, pem_file, file_name):
        '''
            a method for copying a file from local folder to remote host using scp
        :param user_name: string with user name login
        :param ip_address: string with ip address of host server
        :param pem_file: string with pem file (and path) for login cred
        :param file_name: string with name of file in local root folder
        :return:
        '''
    # validate input
        if not ip_address or not user_name or not pem_file or not file_name:
            raise Exception('\ninput lacks all required parameters')
        elif not isinstance(user_name, str):
            raise Exception('\nuser_name must be a string')
        else:
            ip_address = sshInputTest.ipAddress(ip_address)
            pem_file = sshInputTest.pemFile(pem_file)
            file_name = sshInputTest.fileName(file_name)
    # print out shell text equivalent of scp command
            scp_cmd = 'scp -i ' + pem_file + ' -o CheckHostIP=no ' + file_name + \
                ' ' + user_name + '@' + ip_address + ':~/' + file_name
            print('Running: %s ...' % scp_cmd, end='', flush=True)
    # define scp transport with paramiko
            try:
                ssh_key = paramiko.RSAKey.from_private_key_file(pem_file)
                client = paramiko.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=ip_address, username=user_name, pkey=ssh_key)
                scpTransport = scp.SCPClient(client.get_transport())
    # use scp to copy file to remote host
                scpTransport.put(file_name, file_name)
                print(' DONE.')
                client.close()
            except:
                raise Exception('\nFailure to copy file to remote host.\n \
                                Check to see if scp has been installed on remote host.')

    @classmethod
    def unitTests(self):
        return True
# TODO: create unitTests method for labSSH class

# UNIT TESTS
# sshInputTest.unitTests()
# labHTTP.unitTests()

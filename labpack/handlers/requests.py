__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

def handle_requests(request_object):

    import requests

# construct request details
    request_details = {
        'method': request_object.method,
        'headers': request_object.headers,
        'url': request_object.url,
        'error': '',
        'json': request_object.json,
        'code': 105
    }

# retrieve low level request objects
    try:
        prepared_request = request_object.prepare()
    except requests.exceptions.InvalidURL:
        request_details['error'] = '%s is an invalid url.' % request_details['url']
        return request_details
    request_session = requests.Session()

# add headers from requests preparation
    request_details['headers'].update(prepared_request.headers)
    request_details['headers'].update(request_session.headers)

# troubleshoot requests exceptions
    try:
        raise
    except requests.exceptions.InvalidURL:
        request_details['error'] = '%s is an invalid url' % request_details['url']

# troubleshoot local connectivity problems
    except:
        import socket
        try:
            socket.getaddrinfo('www.google.com', '80', 0, 0, socket.SOCK_STREAM)
            request_details['error'] = '%s is not available.' % request_details['url']
        except socket.gaierror:
            request_details['error'] = 'Cannot connect to the internet. Check connectivity.'
        except:
            raise

    return request_details

class requestsHandler(object):
    
    def __init__(self, uptime_url='https://www.google.com', verbose=False):
    
    # construct object properties
        self.uptime_url = uptime_url
    
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
                request_object = Request(method='GET', url=self.uptime_url)
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
            requests.get(self.uptime_url)
        except:
            from requests import Request
            request_object = Request(method='GET', url=self.uptime_url)
            request_details = handle_requests(request_object)
            self.printer('ERROR')
            raise ConnectionError(request_details['error'])
        self.printer('ERROR')
        raise err
    
    def _get_request(self, url, params=None):
        pass
    
    def _post_request(self, url, params=None, json=None):
        pass
    
    def _put_request(self, url, params=None, json=None):
        pass
    
    def _patch_request(self, url, params=None, json=None):
        pass
    
    def _delete_request(self, url, params=None):
        pass
__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

def handle_requests(request_object, uptime_url='www.google.com'):

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
            socket.getaddrinfo(uptime_url, '80', 0, 0, socket.SOCK_STREAM)
            request_details['error'] = '%s is not available.' % request_details['url']
        except socket.gaierror:
            request_details['error'] = 'Cannot connect to the internet. Check connectivity.'
        except:
            raise

    return request_details

class requestsHandler(object):
    
    def __init__(self, uptime_url='www.google.com', requests_handler=handle_requests, response_handler=None, verbose=False):
    
        '''
            the initialization method for the requestsHandler class object
            
        :param uptime_url: [optional] string with url to test availability of internet 
        :param requests_handler: [optional] callable method which accepts a Request object
        :param response_handler: [optional] callable method which accepts a Response object 
        :param verbose: boolean to enable print out of status
        '''
        
    # construct object properties
        self.uptime_url = uptime_url
        self.uptime_ssl = 'https://%s' % self.uptime_url
    
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
    
    # construct handler methods
        self.handle_requests = requests_handler
        self.handle_response = response_handler
        
    def _handle_command(self, sys_command, pipe=False, interactive=None, print_pipe=False, handle_error=False):

        '''
            a method to handle system commands which require connectivity
            
        :param sys_command: string with shell command to run in subprocess 
        :param pipe: boolean to return a Popen object
        :param interactive: [optional] callable object that accepts (string, Popen object)
        :param print_pipe: [optional] boolean to send all pipe results to print
        :param handle_error: boolean to return error message (default: errors are raised)
        :return: Popen object or string or None
        '''

        import sys
        from subprocess import Popen, PIPE, check_output, STDOUT, CalledProcessError

        try:
            if pipe:
                p = Popen(sys_command, shell=True, stdout=PIPE, stderr=PIPE)
                return p
            elif interactive:
                p = Popen(sys_command, shell=True, stdout=PIPE, stderr=STDOUT)
                exchange = ''
            # read/write to subprocess
            # https://stackoverflow.com/a/17109481/4941585
                p_output = p.stdout.readline()
                while p_output:
                    output_string = p_output.decode('utf-8')
                    exchange += output_string
                    p_input = interactive(output_string.rstrip('\n'), p)
                    if p_input:
                        p.stdin.write(str(p_input + '\n').encode())
                    p_output = p.stdout.readline()
                # for line in p.stdout:
                #     interactive(line.decode('utf-8').rstrip('\n'), p)
                #     exchange += line.decode('utf-8')
                #     sys.stdout.flush()
                # p.wait()
                return exchange
            elif print_pipe:
                p = Popen(sys_command, shell=True, stdout=PIPE, stderr=STDOUT)
                for line in p.stdout:
                    self.printer(line.decode('utf-8').rstrip('\n'))
                    sys.stdout.flush()
                p.wait()
                return None
            else:
                response = check_output(sys_command, shell=True, stderr=STDOUT).decode('utf-8')
                return response
        except CalledProcessError as err:
            try:
                import requests
                requests.get(self.uptime_ssl)
                std_err = err.output.decode('ascii', 'ignore')
                if handle_error:
                    return std_err
            except:
                from requests import Request
                request_object = Request(method='GET', url=self.uptime_ssl)
                request_details = self.handle_requests(request_object)
                self.printer('ERROR.')
                raise ConnectionError(request_details['error'])
            self.printer('ERROR.')
            raise Exception(std_err)
        
    def _check_connectivity(self, err):

        ''' a method to check connectivity as source of error '''
        
        try:
            import requests
            requests.get(self.uptime_ssl)
        except:
            from requests import Request
            request_object = Request(method='GET', url=self.uptime_ssl)
            request_details = self.handle_requests(request_object)
            self.printer('ERROR.')
            raise ConnectionError(request_details['error'])
        self.printer('ERROR.')
        raise err
    
    def _request(self, **kwargs):
        
        ''' a helper method for processing all request types '''
        
        response = None
        error = ''
        code = 0
        
    # send request
        from requests import request
        try:
            response = request(**kwargs)
        # handle response
            if self.handle_response:
                response, error, code = self.handle_response(response)
            else:
                code = response.status_code
    # handle errors
        except Exception as err:
            from requests import Request
            request_object = Request(**kwargs)
            try:
                request_details = self.handle_requests(request_object)
                error = request_details['error']
            except:
                error = str(err)
                
        return response, error, code
    
    def _get_request(self, url, params=None, **kwargs):
        
        ''' a method to catch and report http get request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'GET',
            'url': url,
            'params': params
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _post_request(self, url, data=None, json=None, **kwargs):
        
        ''' a method to catch and report http post request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'POST',
            'url': url,
            'data': data,
            'json': json
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _put_request(self, url, data=None, json=None, **kwargs):
        
        ''' a method to catch and report http put request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'PUT',
            'url': url,
            'data': data,
            'json': json
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _patch_request(self, url, data=None, json=None, **kwargs):
        
        ''' a method to catch and report http patch request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'PATCH',
            'url': url,
            'data': data,
            'json': json
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _head_request(self, url, **kwargs):
        
        ''' a method to catch and report http head request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'HEAD',
            'url': url
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _options_request(self, url, **kwargs):
        
        ''' a method to catch and report http options request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'OPTIONS',
            'url': url
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)
    
    def _delete_request(self, url, **kwargs):
        
        ''' a method to catch and report http delete request connectivity errors '''
        
    # construct request kwargs
        request_kwargs = {
            'method': 'DELETE',
            'url': url
        }
        for key, value in kwargs.items():
            request_kwargs[key] = value

    # send request and handle response
        return self._request(**request_kwargs)

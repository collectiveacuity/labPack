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

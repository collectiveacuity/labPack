__author__ = 'rcj1492'
__created__ = '2016.11'
__license__ = 'MIT'

def handle_requests(request_object):

    import requests

# retrieve low level request objects
    prepared_request = request_object.prepare()
    request_session = requests.Session()

# construct request details
    request_details = {
        'method': request_object.method,
        'headers': request_object.headers,
        'url': prepared_request.url,
        'error': '',
        'json': request_object.json,
        'code': 105
    }

# add headers from requests preparation
    request_details['headers'].update(prepared_request.headers)
    request_details['headers'].update(request_session.headers)

# troubleshoot requests exceptions
    try:
        raise
    except requests.exceptions.InvalidURL:
        request_details['error'] = 'invalid url'

# troubleshoot local connectivity problems
    except:
        import socket
        try:
            socket.getaddrinfo('www.google.com', '80', 0, 0, socket.SOCK_STREAM)
            request_details['error'] = 'Airplane mode off.'
        except socket.gaierror:
            request_details['error'] = 'Airplane mode on.'
        except:
            raise

    return request_details
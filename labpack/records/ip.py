__author__ = 'rcj1492'
__created__ = '2017.06'
__licence__ = 'MIT'

def get_ip(source='aws'):
    
    ''' a method to get current localhost public ip address '''
    
    if source == 'aws':
        source_url = 'http://checkip.amazonaws.com/'
    else:
        raise Exception('get_ip currently only supports queries to aws')
    
    import requests
    try:
        response = requests.get(url=source_url)
    except Exception as err:
        from labpack.handlers.requests import handle_requests
        from requests import Request
        request_object = Request(method='GET', url=source_url)
        request_details = handle_requests(request_object)
        raise Exception(request_details['error'])
    current_ip = response.content.decode()
    current_ip = current_ip.strip()
    
    return current_ip
__author__ = 'rcj1492'
__created__ = '2018.02'
__license__ = '©2018 Collective Acuity'

from labpack.handlers.requests import requestsHandler

if __name__ == '__main__':
    
    requests_handler = requestsHandler()
    response, error = requests_handler._get_request('http://www.google.com')
    print(response.content)
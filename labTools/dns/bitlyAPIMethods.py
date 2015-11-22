__author__ = 'rcj1492'
__created__ = '2015'

# dependencies for bitly requests & performance tests
# http://dev.bitly.com/api.html
# uses normal web GET requests
# also has module: pip install bitly_api

import json
import urllib.request
import urllib.parse
from timeit import default_timer as timer

from cred.credentialsDataProcessor import *


def shortenURLBitly(longURL, bitly_token):
    '''
        returns shortURL from JSON response to GET request to Bitly API
        includes a performance test of API response time
        dependencies:
        import json
        import urllib.request
        import urllib.parse
        from timeit import default_timer as timer
        from credentials import *
    '''
    urlTitle = 'Bitly API'
    bitly_url = 'https://api-ssl.bitly.com/v3/shorten?%s'
    params = {
        'access_token': bitly_token,
        'longUrl': longURL
    }
    t1 = timer()
    response = urllib.request.urlopen(bitly_url % urllib.parse.urlencode(params))
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    responseJSON = json.loads(response.read().decode("utf-8"))
    return responseJSON['data']['url']
assert shortenURLBitly('https://twitter.com/collectiveacuiT', bitlyToken)


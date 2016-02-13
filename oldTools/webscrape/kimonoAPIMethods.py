__author__ = 'rcj1492'
__created__ = '2015'

import json
import urllib.request
import urllib.parse
from timeit import default_timer as timer

from cred.credentialsDataProcessor import *


def kimonoAPIResults(apiURL, kimono_api_key):
    '''
        call kimono for customized API's results
        includes a performance test of API response time
        https://www.kimonolabs.com/apidocs
        dependencies:
            import json
            import urllib.request
            from datetime import datetime
    :param apiKey: the 8 bit alpha numeric URL of API
    :return:
    '''
    urlTitle = 'Kimono API'
    params = {
        'key': kimono_api_key,
        'kimmodify': 1,
        'kimseries': 1
    }
    url = 'https://www.kimonolabs.com/api/' + str(apiURL) + '?%s'
    GET_params = urllib.parse.urlencode(params)
    t1 = timer()
    response = urllib.request.urlopen(url % GET_params)
    t2 = timer()
    print(urlTitle + ': ' + format((t2 - t1), '.5f') + ' seconds')
    return json.loads(response.read().decode("utf-8"))
assert kimonoAPIResults('7q5c63lk', kimonoAPIKey)

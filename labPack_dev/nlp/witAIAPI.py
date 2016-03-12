__author__ = 'rcj1492'
__created__ = '2016.01'

'''
https://wit.ai/docs/http/20141022

requires a trained app:
https://wit.ai/docs/console/quickstart

'''

import json
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen

from cred.credentialsWitAI import witAICredentials

# construct get request
headers = {
    'Authorization': 'Bearer ' + witAICredentials['accessToken']
}
wit_url = 'https://api.wit.ai/message'
wit_version = '20141022'
missive = 'can you turn off the kitchen lights?'
if len(missive) > 256:
    missive = missive[0:256]
context_dict = {}
query_args = {
    'v': wit_version,
    'q': missive
}
if context_dict:
    query_args['context'] = context_dict
url_string = "%s?%s" % (wit_url, urlencode(query_args))
print(url_string)
get_request = Request(url=url_string, headers=headers)

# send request for intent inference
try:
    response = urlopen(get_request)
except:
    raise Exception('Oops... something went wrong.')

# return response as data format
response_dict = response.read()
json_dict = json.loads(response_dict.decode('utf-8'))
print(json_dict)


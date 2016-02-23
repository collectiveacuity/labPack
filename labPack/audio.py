__author__ = 'rcj1492'
__created__ = '2016.02'

'''
    Harmon Documentation

https://harmandeveloperdocs.readthedocs.org/en/latest/iOS/sdk-overview.html

## Harmon Speakers
- HK WHub App (iOS 8+)
- HKIoTCloud
- PubNub channel
- https://itunes.apple.com/us/app/hk-whub-app/id1057062847?mt=8

curl -X POST -H “Authorization: Basic Nzg0Y09BckxSWTZYZEVtdDpSUHFnU21FRW5QVE5ja2kzWURzT3hQNWhFM3hwMWU=” -d “grant_type=password&username=collectiveacuity&password=minutesbeforeDEADLINE” http://hkiotcloud.herokuapp.com/oauth/token
'''

from urllib.request import Request, urlopen
from urllib.parse import urlencode
from base64 import b64encode
import json
import time

class HarmonConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to HK IoT API with %s request.' % message
        super(HarmonConnectionError, self).__init__(text)
        self.errors = errors

class harmonAccessToken(object):

    '''
        a class of methods to request an access token from Harmon IoT API
    '''

    __name__ = 'harmonAccessToken'

    def __init__(self, access_token=None, harmon_credentials=None):

        if access_token:
            if isinstance(access_token, harmonAccessToken):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.tokenRefresh = ''
                self.endpoint = access_token.endpoint
                self.clientID = access_token.clientID
                self.clientSecret = access_token.clientSecret
            else:
                raise TypeError('access_token must be a %s object.' % self.__class__)

        elif harmon_credentials:
            if isinstance(harmon_credentials, dict):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.tokenRefresh = ''
                self.endpoint = 'http://hkiotcloud.herokuapp.com/oauth/token'
                self.clientID = harmon_credentials['appKey']
                self.clientSecret = harmon_credentials['appSecret']
            else:
                raise TypeError('harmon_credentials must be a dictionary.')

        else:
            raise Exception('harmonAccessToken.__init__() requires either an access_token or harmon_credentials input.')

    def request(self, username, password):

        title = self.__name__ + '.request()'

    # validate inputs
        if not isinstance(username, str):
            raise TypeError('%s user_name input must be a string.' % title)
        elif not isinstance(password, str):
            raise TypeError('%s pass_word input must be a string.' % title)

    # construct post request url and headers
        basic_id = '%s:%s' % (self.clientID, self.clientSecret)
        string_id = b64encode(basic_id.encode('utf-8')).decode()
        headers = {
            'Authorization': 'Basic %s' % string_id,
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_request = Request(url=self.endpoint, headers=headers)

    # construct post request data
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password
        }
        post_data = urlencode(data).encode('utf-8')

    # send request
        try:
            response = urlopen(post_request, post_data)
        except:
            raise HarmonConnectionError('%s urlopen(%s)' % (title, self.endpoint))

    # construct token methods from response
        token_data = json.loads(response.read().decode('utf-8'))
        self.accessToken = token_data['access_token']
        epoch_time = time.time()
        self.tokenExpiration = token_data['expires_in'] + epoch_time
        self.tokenType = token_data['token_type']
        self.tokenRefresh = token_data['refresh_token']
        return self

    def refresh(self):

        title = self.__name__ + '.refresh()'

    # validate inputs
        epoch_time = time.time()
        if not self.tokenRefresh:
            raise ValueError('%s method cannot be called without an initial request for an access token.' % title)
        elif epoch_time > self.tokenExpiration:
            raise ValueError('%s refresh_token has expired.' % title)

    # construct post request url and headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_request = Request(url=self.endpoint, headers=headers)

    # construct post request data
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.tokenRefresh,
            'client_id': self.clientID,
            'client_secret': self.clientSecret
        }
        post_data = urlencode(data).encode('utf-8')

    # send request
        try:
            response = urlopen(post_request, post_data)
        except:
            raise HarmonConnectionError('%s urlopen(%s)' % (title, self.endpoint))

    # construct token methods from response
        token_data = json.loads(response.read().decode('utf-8'))
        self.accessToken = token_data['access_token']
        epoch_time = time.time()
        self.tokenExpiration = token_data['expires_in'] + epoch_time
        self.tokenType = token_data['token_type']
        self.tokenRefresh = token_data['refresh_token']
        return self

class harmonSession(object):

    '''
        a class of methods to control audio on Harmon speakers
    '''

    __name__ = 'harmonSession'

    def __init__(self, access_token, sound_format=''):

        title = self.__name__ + '.__init__()'

    # validate inputs
        epoch_time = time.time()
        if not isinstance(access_token, harmonAccessToken):
            raise TypeError('%s access_token input must be a harmonAccessToken object.' % title)
        elif epoch_time > access_token.tokenExpiration:
            raise ValueError('%s access_token has expired.' % title)

    # add accessToken methods to class
        self.accessToken = access_token.accessToken

    # construct endpoints dictionary
        self.endpoints = {
            'init': 'http://hkiotcloud.herokuapp.com/api/v1/init_session'
        }

    # construct post request url and headers
        headers = {
            'Authorization': 'Bearer %s' % self.accessToken,
            'Accept': 'application/json'
        }
        post_request = Request(url=self.endpoints['init'], headers=headers)

    # send request
        try:
            response = urlopen(post_request)
        except:
            raise HarmonConnectionError('%s urlopen(%s)' % (title, self.endpoints['init']))

    # construct token methods from response
        token_data = json.loads(response.read().decode('utf-8'))
        self.sessionToken = token_data['SessionToken']

    # construct sound format method
        sound_list = ['audio/wav']
        self.soundFormat = 'audio/wav'
        if sound_format:
            if not isinstance(sound_format, str):
                raise TypeError('%s sound_format input must be a string.' % title)
            elif not sound_format in sound_list:
                raise ValueError('%s sound_format input must be one of %s values.' % (title, sound_list))
            self.soundFormat = sound_format

    def devices(self):
        return self

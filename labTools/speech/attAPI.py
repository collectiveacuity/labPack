__author__ = 'rcj1492'
__created__ = '2015.11'

from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import time

class ATTConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to ATT API with %s request.' % message
        super(ATTConnectionError, self).__init__(text)
        self.errors = errors

class attAccessToken(object):

    '''
        a class of methods to request an access token from ATT API
    '''

    __name__ = 'attAccessToken'

    def __init__(self, access_token=None, att_credentials=None):

        if access_token:
            if isinstance(access_token, attAccessToken):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.endpoint = access_token.endpoint
                self.clientID = access_token.clientID
                self.clientSecret = access_token.clientSecret
                self.scope = access_token.scope
            else:
                raise TypeError('access_token must be a %s object.' % self.__class__)

        elif att_credentials:
            if isinstance(att_credentials, dict):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.endpoint = 'https://api.att.com/oauth/v4/token'
                self.clientID = att_credentials['appKey']
                self.clientSecret = att_credentials['appSecret']
                self.scope = att_credentials['serviceScope']
            else:
                raise TypeError('att_credentials must be a dictionary.')

        else:
            raise Exception('attAccessToken.__init__() requires either an access_token or att_credentials input.')

    def request(self):

        title = self.__name__ + '.request()'

    # construct post request url and headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_request = Request(url=self.endpoint, headers=headers)

    # construct post request data
        data = {
            'client_id': self.clientID,
            'client_secret': self.clientSecret,
            'grant_type': 'client_credentials',
            'scope': self.scope
        }
        post_data = urlencode(data).encode('utf-8')

    # send request
        try:
            response = urlopen(post_request, post_data)
        except:
            raise ATTConnectionError('%s urlopen()' % title)

    # construct token methods from response
        token_data = json.loads(response.read().decode('utf-8'))
        self.accessToken = token_data['access_token']
        epoch_time = time.time()
        self.tokenExpiration = token_data['expires_in'] + epoch_time
        self.tokenType = token_data['token_type']
        return self

class attSpeech(object):

    '''
        a class of methods to convert text and speech through ATT API
    '''

    __name__ = 'attSpeech'

    def __init__(self, access_token, sound_format=''):

        title = self.__name__ + '.__init__()'

        if isinstance(access_token, attAccessToken):
            self.accessToken = access_token.accessToken
        else:
            raise TypeError('access_token input must be an accessToken object.')
        self.endpoints = {
            'TTS': 'https://api.att.com/speech/v3/textToSpeech',
            'STT': 'https://api.att.com/speech/v3/speechToText'
        }
        sound_list = ['audio/wav']
        self.soundFormat = 'audio/wav'
        if sound_format:
            if not isinstance(sound_format, str):
                raise TypeError('%s sound_format input must be a string.' % title)
            elif not sound_format in sound_list:
                raise ValueError('%s sound_format input must be one of %s values.' % (title, sound_list))
            self.soundFormat = sound_format

    def text2speech(self, text):

        title = self.__name__ + '.text2speech()'

    # validate inputs
        if not isinstance(text, str):
            raise TypeError('%s text input must be a string.' % title)

    # construct post request
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            'Accept': self.soundFormat,
            'Content-Type': 'text/plain',
            'X-Arg': 'VoiceName=crystal,Volume=100'
        }
        post_request = Request(url=self.endpoints['TTS'], headers=headers)
        post_data = text.encode('utf-8')

    # send request for text to speech
        try:
            response = urlopen(post_request, post_data)
        except:
            raise ATTConnectionError('%s urlopen(%s)' % (title, self.endpoints['TTS']))

    # return response as data format
        sound_data = response.read()
        return sound_data

    def speech2text(self, sound_data):

        title = self.__name__ + '.speech2text()'

    # validate inputs
        if not isinstance(sound_data, bytes):
            raise TypeError('%s sound_data input must be bytes.' % title)

    # construct post request
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            'Accept': 'application/json',
            'Content-Type': self.soundFormat
            # 'Transfer-Encoding': 'chunked'
        }
        post_request = Request(url=self.endpoints['STT'], headers=headers)
        post_data = sound_data

    # send request for text to speech
        try:
            response = urlopen(post_request, post_data)
        except:
            raise ATTConnectionError('%s urlopen(%s)' % (title, self.endpoints['STT']))

    # return recognition dictionary
        speech_analysis = json.loads(response.read().decode())
        return speech_analysis['Recognition']['NBest'][0]

    def unitTests(self):
        sound = self.text2speech('text analysis is fun')
        speech_analysis = self.speech2text(sound)
        assert speech_analysis['Hypothesis']
        return self

dummy = ''
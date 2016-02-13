__author__ = 'rcj1492'
__created__ = '2015.11'

'''
https://developer.clarifai.com/docs/requests
https://github.com/Clarifai/clarifai-python
'''

from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import time

class ClarifaiConnectionError(Exception):

    def __init__(self, message='', errors=None):
        text = '\nFailure connecting to Clarifai API with %s request.' % message
        super(ClarifaiConnectionError, self).__init__(text)
        self.errors = errors

class clarifaiAccessToken(object):

    '''
        a class of methods to request an access token from Clarifai API
    '''

    __name__ = 'clarifaiAccessToken'

    def __init__(self, access_token=None, clarifai_credentials=None):

        if access_token:
            if isinstance(access_token, clarifaiAccessToken):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.endpoint = access_token.endpoint
                self.clientID = access_token.clientID
                self.clientSecret = access_token.clientSecret
                self.scope = access_token.scope
            else:
                raise TypeError('access_token must be a %s object.' % self.__class__)

        elif clarifai_credentials:
            if isinstance(clarifai_credentials, dict):
                self.accessToken = ''
                self.tokenExpiration = 0
                self.tokenType = ''
                self.endpoint = 'https://api.clarifai.com/v1/token/'
                self.clientID = clarifai_credentials['clientID']
                self.clientSecret = clarifai_credentials['clientSecret']
                self.scope = clarifai_credentials['serviceScope']
            else:
                raise TypeError('clarifai_credentials must be a dictionary.')

        else:
            raise Exception('clarifaiAccessToken.__init__() requires either an access_token or clarifai_credentials input.')

    def request(self):

        title = self.__name__ + '.request()'

    # construct post request url and headers
    #     headers = {
    #         'Accept': 'application/json',
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
        post_request = Request(url=self.endpoint)

    # construct post request data
        data = {
            'client_id': self.clientID,
            'client_secret': self.clientSecret,
            'grant_type': 'client_credentials'
        }
        post_data = urlencode(data).encode('utf-8')

    # send request
        try:
            response = urlopen(post_request, post_data)
        except:
            raise ClarifaiConnectionError('%s urlopen()' % title)

    # construct token methods from response
        token_data = json.loads(response.read().decode('utf-8'))
        self.accessToken = token_data['access_token']
        epoch_time = time.time()
        self.tokenExpiration = token_data['expires_in'] + epoch_time
        self.tokenType = token_data['token_type']
        return self
    
class clarifaiImage(object):

    '''
        a class of methods to retrieve image recognition from Clarifai API
    '''

    __name__ = 'clarifaiImage'

    def __init__(self, access_token, mime_type=''):

        title = self.__name__ + '.__init__()'

        if not isinstance(access_token, clarifaiAccessToken):
            raise TypeError('access_token input must be an accessToken object.')
        self.accessToken = access_token.accessToken
        self.endpoints = {
            'Tagging': 'https://api.clarifai.com/v1/tag/',
            'Feedback': 'https://api.clarifai.com/v1/feedback/'
        }
        mime_list = ['image/jpg']
        self.mimeType = 'image/jpg'
        if mime_type:
            if not isinstance(mime_type, str):
                raise TypeError('%s mime_type input must be a string.' % title)
            elif not mime_type in mime_list:
                raise ValueError('%s mime_type input must be one of %s values.' % (title, mime_list))
            self.mimeType = mime_type

    def tagUrl(self, image_url):

        title = self.__name__ + '.tagUrl()'

    # validate inputs
        if not isinstance(image_url, str):
            raise TypeError('%s image_url input must be a string.' % title)

    # construct post request
        headers = {
            'Authorization': 'Bearer ' + self.accessToken,
            # 'Accept': 'application/json'
        }
        body = {
            'url': image_url
        }
        post_request = Request(url=self.endpoints['Tagging'], headers=headers)
        post_data = urlencode(body).encode('utf-8')

    # send request for text to speech
        try:
            response = urlopen(post_request, post_data)
        except:
            raise ClarifaiConnectionError('%s urlopen(%s)' % (title, self.endpoints['Tagging']))

    # return recognition dictionary
        response_dict = json.loads(response.read().decode())
        image_analysis = response_dict['results'][0]
        results = {
            'docID': image_analysis['docid'],
            'tags': []
        }
        tag_list = image_analysis['result']['tag']
        for i in range(len(tag_list['probs'])):
            details = {
                'class': tag_list['classes'][i],
                'conceptID': tag_list['concept_ids'][i],
                'confidence': tag_list['probs'][i]
            }
            results['tags'].append(details)
        return results

    def tagFile(self, image_data):
        return True

    def classFeedback(self, doc_id, tag_list):
        return True

    def unitTests(self):
        tags = self.tagUrl('http://cdn-static.tunein.com/201511121706/img/tunein-fm/station.jpg')
        print(tags)
        return self

dummy = ''
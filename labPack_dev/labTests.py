__author__ = 'rcj1492'
__created__ = '2015.11'

'''
a collection of test classes for testing other labTool classes

pip install pytest
https://pypi.python.org/pypi/pytest
'''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cred.credentialsGoogle import *
from oldTools.location.googleMapsAPI import *
from cred.credentialsATT import tinkerbellCredentials
from oldTools.speech.attSpeechAPI import *
from cred.credentialsClarifai import clarifaiCredentials
from oldTools.image.clarifaiImageAPI import *

class unitTests(object):

    def __init__(self):
        pass

    def attSpeechAPI(self):
        token = attAccessToken(att_credentials=tinkerbellCredentials).request()
        attSpeech(access_token=token).unitTests()
        return self

    def clarifaiImageAPI(self):
        token = clarifaiAccessToken(clarifai_credentials=clarifaiCredentials).request()
        clarifaiImage(access_token=token).unitTests()
        return self

    def googleMapsAPI(self):
        mapRules = json.loads(open('location/google-map-rules.json').read())
        googleMaps(app_key=googleMapsCred['appKey'], map_rules=mapRules).unitTests()
        return self

    def run(self):
        self.attSpeechAPI()
        self.clarifaiImageAPI()
        self.googleMapsAPI()
        return self

class performanceTests(object):
    pass

unitTests()




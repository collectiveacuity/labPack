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

from cred.credentialsATT import tinkerbellCredentials
from labTools.speech.attAPI import *

class unitTests(object):

    def __init__(self):
        pass

    def attAPI(self):
        token = attAccessToken(att_credentials=tinkerbellCredentials).request()
        attSpeech(access_token=token).unitTests()
        return self

    def run(self):
        self.attAPI()
        return self

class performanceTests(object):
    pass

unitTests().run()




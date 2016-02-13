__author__ = 'rcj1492'
__created__ = '2016.02'

from cred.credentialsMorphIO import morphIOCredentials
from labpack.webscrapers import labMorph

labMorph(morphIOCredentials).unitTests()


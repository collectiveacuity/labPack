__author__ = 'rcj1492'
__created__ = '2016.02'

from labPack.shorteners import bitlyAPI
from cred.credentialsBitly import bitlyToken
assert bitlyAPI('https://twitter.com/collectiveacuiT', bitlyToken)
__author__ = 'rcj1492'
__created__ = '2016.02'

from cred.credentialsBitly import bitlyToken
from dev.shorteners import bitlyAPI

assert bitlyAPI('https://twitter.com/collectiveacuiT', bitlyToken)
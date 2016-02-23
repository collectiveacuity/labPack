__author__ = 'rcj1492'
__created__ = '2016.02'

# Harmon API
from labPack.audio import harmonAccessToken
from cred.credentialsHarmon import harmonCredentials, harmonCredentialsCA
token = harmonAccessToken(harmon_credentials=harmonCredentials)
print(token.endpoint)
print(token.clientID)
print(token.clientSecret)
token.request(harmonCredentialsCA['user'], harmonCredentialsCA['pass'])
print(token.accessToken)
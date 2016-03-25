__author__ = 'rcj1492'
__created__ = '2016.02'

from cred.credentialsDBIP import dbIPAPIKey

from dev.dns import geoLocateByIP
assert geoLocateByIP(dbIPAPIKey).dbIP('4.35.25.132')['stateprov'] == 'Connecticut'
assert geoLocateByIP(dbIPAPIKey).dbIP('2001:db8:85a3:8d3:1319:8a2e:370:7348')['stateprov'] == 'Queensland'
assert geoLocateByIP(dbIPAPIKey).ipAPI('8.8.8.8')['regionName'] == 'California'
assert geoLocateByIP(dbIPAPIKey).ipAPI('2001:4860:4860::8888')['countryCode'] == 'US'

from dev.dns import localPublicIP
assert localPublicIP().httpBin()
assert localPublicIP().jsonIP()
assert localPublicIP().ip42()
assert localPublicIP().ipify()
print(localPublicIP().httpBin())

from dev.dns import localPrivateIP
print(localPrivateIP().askSocket())
print(localPrivateIP().socketHost())
print(localPrivateIP().pingHTTP('8.8.8.8'))

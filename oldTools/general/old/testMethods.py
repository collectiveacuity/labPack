__author__ = 'rcj1492'
__created__ = '2015'

import uuid
import netifaces
import pprint

# mac = ''
# test_mac = uuid.getnode()
# counter = 0
# while not test_mac == mac and counter < 20:
#     mac = test_mac
#     test_mac = uuid.getnode()
#     counter += 1
# m = hex(mac)[2:14]
# mac_address = m[0:2] + ':' + m[2:4] + ':' + m[4:6] + \
#               ':' + m[6:8] + ':' + m[8:10] + ':' + m[10:12]
# print(mac_address)
uuidList = netifaces.interfaces()
deviceList = []
testList = []
for i in uuidList:
    testList.append(netifaces.ifaddresses(i))
for i in uuidList:
    res = netifaces.ifaddresses(i)
    d = {}
    if -1000 in res.keys() and 2 in res.keys():
        if res[-1000][0]['addr'] and not res[-1000][0]['addr'] == '00:00:00:00:00:00:00:e0':
            d['mac'] = res[-1000][0]['addr']
            d['ip'] = res[2][0]['addr']
    if d:
        deviceList.append(d)
pprint.pprint(deviceList)

# from urllib.request import urlopen
# url = 'http://www.ucla.edu/'
# bytes = urlopen(url).read()
# string = bytes.decode('utf-8', 'ignore')
# print(string)

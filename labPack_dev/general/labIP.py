__author__ = 'rcj1492'
__created__ = '2015.09'

# pip install netifaces
# https://pypi.python.org/pypi/netifaces

import netifaces
import pprint

class labIP(object):

    def __init__(self):
        pass

    def ipv4(self):
        ip_address = ''
        return ip_address

    def ipv6(self):
        ip_address = ''
        return ip_address

    def unitTests(self):
        return self

def localMacs():
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

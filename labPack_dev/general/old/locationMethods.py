__author__ = 'rcj1492'
__created__ = '2015'


import re
import json
from urllib.request import urlopen
import socket
import uuid
import random
import codecs
import os
import hashlib
import sha3
from datetime import datetime
import time
from processor.methods.api.ipAPIMethods import *

class labLocate(dict):
    '''
        import uuid
        from urllib.request import urlopen
        import socket
        import re
        import json
    '''

    def __init__(self):
        '''
            methods to determine local information
        :return:
        '''
        # mac address
        try:
            mac = ''
            test_mac = uuid.getnode()
            counter = 0
            while not test_mac == mac and counter < 20:
                mac = test_mac
                test_mac = uuid.getnode()
                counter += 1
            m = hex(mac)[2:14]
            mac_address = m[0:2] + ':' + m[2:4] + ':' + m[4:6] + \
                          ':' + m[6:8] + ':' + m[8:10] + ':' + m[10:12]
            self['mac'] = mac_address
            print(time.perf_counter())
        except:
            raise Exception('cannot establish mac address')
        # private ip address
        # public ip address
        try:
            self['publicIP'] = localPublicIP.httpBin()
        except:
            try:
                self['publicIP'] = localPublicIP.jsonIP()
            except:
                raise Exception('cannot establish connection to internet')
        # geolocation by ip
        if 'publicIP' in self.keys():
            self['ipLocation'] = []
            try:
                ip = self['publicIP']
                d = geoLocateByIP.ipAPI(ip)
                self['ipLocation'].append(d)
                print(time.perf_counter())
            except:
                raise Exception('cannot establish connection to IP location API')
            try:
                ip = self['publicIP']
                d = geoLocateByIP.dbIP(ip)
                self['ipLocation'].append(d)
                print(time.perf_counter())
            except:
                raise Exception('cannot establish connection to IP location API')

print(labLocate())

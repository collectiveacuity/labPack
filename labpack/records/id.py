__author__ = 'rcj1492'
__created__ = '2015.09'
__license__ = 'MIT'

# pip install pytz
# pip install tzlocal

import uuid
import binascii
import os
import hashlib
import base64
from datetime import datetime
import pytz

class labID(object):

    ''' a class of methods for uniquely identifying objects

        build-in methods:
            self.uuid: uuid1 uuid object
            self.id12: 12 character base 64 url safe string of posix time
            self.id24: 24 character base 64 url safe string of md5 hash of uuid1
            self.id36: 36 character base 64 url safe string of sha1 hash of uuid1
            self.id48: 48 character base 64 url safe string of sha256 hash of uuid1
            self.mac: string of mac address of device
            self.epoch: current posix epoch timestamp with micro second resolution
            self.iso: current iso utc datetime string
            self.datetime: current python datetime
    '''

    def __init__(self):

        ''' a method to initialize a unique ID based upon the UUID1 method '''

    # retrieve UUID
        self.uuid = uuid.uuid1()

    # calculate micro second posix timestamp of uuid
        t = self.uuid.time
        t = t - 0x01b21dd213814000
        v = t / 1e7
        self.epoch = float(str(v)[0:17])
        self.datetime = datetime.utcfromtimestamp(self.epoch).replace(tzinfo=pytz.utc)
        self.iso = self.datetime.isoformat()


    # create byte ids of various lengths using hash of uuid
        self.bytes_9 = os.urandom(2) + bytes(binascii.unhexlify(format(int(t), 'x')))
        self.bytes_18 = os.urandom(2) + hashlib.md5(self.uuid.bytes).digest()
        self.bytes_27 = os.urandom(7) + hashlib.sha1(self.uuid.bytes).digest()
        self.bytes_36 = os.urandom(4) + hashlib.sha256(self.uuid.bytes).digest()

    # convert byte ids into base 64 url safe id strings
        self.id12 = base64.urlsafe_b64encode(self.bytes_9).decode()
        self.id24 = base64.urlsafe_b64encode(self.bytes_18).decode()
        self.id36 = base64.urlsafe_b64encode(self.bytes_27).decode()
        self.id48 = base64.urlsafe_b64encode(self.bytes_36).decode()

    # determine the mac address
        mac = 0
        test_mac = uuid.getnode()
        counter = 0
        while not test_mac == mac and counter < 5:
            mac = test_mac
            test_mac = uuid.getnode()
            counter += 1
        if counter < 5:
            m = hex(mac)[2:14]
            local_mac =  m[0:2] + ':' + m[2:4] + ':' + m[4:6] + \
                         ':' + m[6:8] + ':' + m[8:10] + ':' + m[10:12]
        else:
            local_mac = ''
        self.mac = local_mac

if __name__ == '__main__':
    print(labID().id12)
    print(labID().uuid)
    print(labID().epoch)




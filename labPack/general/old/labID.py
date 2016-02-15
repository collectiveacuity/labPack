__author__ = 'rcj1492'
__created__ = '2015.06'

# pip install pysha3

import uuid
import random
import binascii
import os
import hashlib
import sha3
from datetime import datetime

class labID(dict):
    '''
        methods to create and prove authorship of a unique alphanumeric identifier
        benefits of method include:
            1. hash function prohibits reverse engineering authorship details
            2. id is unique across all devices universally using method
            3. phase space is 10^60
            4. length is equivalent to existing UUID strings
            5. characters are human readable, url-safe
            6. work is preserved locally for claiming authorship
        dependencies:
        import random
        import binascii
        import os
        import uuid
        import hashlib
        import sha3 # pip install pysha3
        from datetime import datetime
    :return: dictionary with id string and (proof of) work dictionary
    '''
    def __init__(self):
        dict.__init__({})
        base_alpha = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
        utc_time = datetime.utcnow().isoformat() + 'Z'
        data = os.urandom(32)
        string = binascii.hexlify(data).decode()
        random_object = random.SystemRandom(string)
        rand_fraction = random_object.random()
        rand_float = str(rand_fraction)
        mac = 0
        test_mac = uuid.getnode()
        counter = 0
        while not test_mac == mac and counter < 10:
            mac = test_mac
            test_mac = uuid.getnode()
            counter += 1
        m = hex(mac)[2:14]
        local_mac =  m[0:2] + ':' + m[2:4] + ':' + m[4:6] + \
                     ':' + m[6:8] + ':' + m[8:10] + ':' + m[10:12]
        components = local_mac + utc_time + rand_float
        hex_string = hashlib.sha3_256(components.encode('utf-8')).hexdigest()
        i = int(hex_string, 16)
        base_len = len(base_alpha)
        s = ''
        while i:
            i, rem = divmod(i, base_len)
            s = base_alpha[rem] + s
        lab_id = s[0:36]
        self['id'] = lab_id
        self['work'] = {}
        self['work']['macAd'] = local_mac
        self['work']['timeStamp'] = utc_time
        self['work']['randFloat'] = rand_float

    @classmethod
    def proof(self, id='', work=None):
        '''
            runs proof of authorship of labID from work
        :param id: 36-digit alphanumeric string generated by labID class
        :param work: dictionary containing macID, timeStamp and randFloat generated by labID class
        :return: boolean
        '''
        if not isinstance(id, str) or not isinstance(work, dict):
            raise Exception ('method requires type string for id and dictionary for work')
        elif not len(id) == 36:
            raise Exception ('method requires 36-digit id generated by labID class')
        elif not 'macAd' in work.keys() or not 'timeStamp' in work.keys() or not 'randFloat' in work.keys():
            raise Exception ('method requires macAd, timeStamp and randFloat generated by labID class')
        else:
            base_alpha = tuple('23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ')
            components = work['macAd'] + work['timeStamp'] + work['randFloat']
            hex_string = hashlib.sha3_256(components.encode('utf-8')).hexdigest()
            i = int(hex_string, 16)
            base_len = len(base_alpha)
            s = ''
            while i:
                i, rem = divmod(i, base_len)
                s = base_alpha[rem] + s
            new_id = s[0:36]
            if new_id == id:
                return True
            else:
                return False

    @classmethod
    def unitTests(self):
        test = labID()
        assert labID.proof(test['id'],test['work'])
        return self

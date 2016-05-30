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
import re
from datetime import datetime
from tzlocal import get_localzone
from dateutil import parser as dTparser
from dateutil import tz
import pytz

class labID(object):

    '''
        a class of methods for uniquely identifying objects

        dependencies:
            import uuid
            import binascii
            import os
            import hashlib
            import base64
            import pytz
            from datetime import datetime

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

    __name__ = 'labID'

    def __init__(self):

        '''
            a method to initialize a unique ID based upon the UUID1 method
        '''

    # retrieve UUID
        self.uuid = uuid.uuid1()

    # calculate micro second posix timestamp of uuid
        t = self.uuid.time
        t = t - 0x01b21dd213814000
        v = t / 1e7
        self.epoch = float(str(v)[0:17])
        self.datetime = datetime.utcfromtimestamp(self.epoch).replace(tzinfo=pytz.utc)
        self.iso = self.datetime.isoformat().replace('+00:00', 'Z')


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

class labDT(datetime):

    '''
        a class of methods for datetime conversion

        for list of timezones:
            https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones
        for list of datetime directives:
            https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior

        dependencies:
            from datetime import datetime
            import re
            import pytz
            from tzlocal import get_localzone
            from dateutil import parser as dTparser
            from dateutil import tz
    '''

    __name__ = 'labDT'

    @classmethod
    def new(self):

        '''
            a method to generate the current datetime as a labDT object
        :return: labDT
        '''

        dT = datetime.utcnow().replace(tzinfo=pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    def iso(self):

        '''
            a method to report ISO UTC datetime string from a labDT object
        :return: string in ISO UTC format
        '''

    # construct ISO UTC string from labDT
        utc_dt = self.astimezone(pytz.utc)
        iso_dt = utc_dt.isoformat()
        return iso_dt.replace('+00:00', 'Z')

    def epoch(self):

        '''
            a method to report posix epoch timestamp from a labDT object
        :return: float with timestamp
        '''

    # construct epoch timestamp from labDT
        epoch_dt = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        delta_time = self - epoch_dt
        return delta_time.total_seconds()

    def pyLocal(self, time_zone=False):

        '''
            a method to report a python datetime from a labDT object
        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        get_tz = get_localzone()
        title = 'Timezone input for labDT.pyLocal'
        if time_zone:
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('\n%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)

    # construct python datetime from labDT
        dT = self.astimezone(get_tz)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    def jsLocal(self, time_zone=False):

        '''
            a method to report a javascript string from a labDT object
        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        js_format = '%a %b %d %Y %H:%M:%S.%f GMT%z (%Z)'
        title = 'Timezone input for labDT.jsLocal'
        get_tz = get_localzone()
        if time_zone:
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('\n%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)

    # construct javascript datetime from labDT
        dtLocal = self.astimezone(get_tz)
        return format(dtLocal, js_format)

    def humanFriendly(self, time_zone=False):

        '''
            a method to report a human friendly string from a labDT object
        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        zeroHourPattern = re.compile('\s0\d:')
        title = 'Timezone input for labDT.humanFriendly'
        human_format = '%A, %B %d, %Y %I:%M%p %Z'
        get_tz = get_localzone()
        if time_zone:
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('\n%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)

    # construct human friendly string from labDT
        dtLocal = self.astimezone(get_tz)
        dtString = format(dtLocal, human_format)
        zeroHour = zeroHourPattern.findall(dtString)
        if zeroHour:
            noZero = zeroHour[0].replace(' 0',' ')
            dtString = zeroHourPattern.sub(noZero,dtString)
        return dtString

    @classmethod
    def fromEpoch(self, epoch_time):

        '''
            a method for constructing a labDT object from epoch timestamp
        :param epoch_time: number with epoch timestamp info
        :return: labDT
        '''

    # validate input
        title = 'Epoch time input for labDT.fromEpoch'
        if not isinstance(epoch_time, float) and not isinstance(epoch_time, int):
            raise TypeError('\n%s must be an integer or float.' % title)

    # construct labDT from epoch time
        dT = datetime.utcfromtimestamp(epoch_time).replace(tzinfo=pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    @classmethod
    def fromISO(self, iso_string):

        '''
            a method for constructing a labDT object from a timezone aware ISO string
        :param iso_string: string with date and time info in ISO format
        :return: labDT
        '''

    # validate input
        title = 'ISO time input for labDT.fromISO'
        isopattern = re.compile('\d{4}-\d{2}-\d{2}T.*')
        if not isopattern.search(iso_string):
            raise ValueError('\n%s is not a valid ISO string.' % title)
        python_datetime = dTparser.parse(iso_string)
        if not python_datetime.tzinfo:
            raise ValueError('\n%s must have timezone info.' % title)

    # construct labDT from parsed string
        dT = python_datetime.astimezone(pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    @classmethod
    def fromPython(self, python_datetime):

        '''
            a method for constructing a labDT from a python datetime with timezone info
        :param python_datetime: datetime object with timezone info
        :return: labDT
        '''

    # validate inputs
        title = 'Python datetime input for labDT.fromPython'
        if not isinstance(python_datetime, datetime):
            raise TypeError('\n%s must be a valid %s object.' % (title, datetime.__class__))
        elif not python_datetime.tzinfo:
            raise ValueError('\n%s must have a timezone.' % title)

    # construct labDT from python datetime
        dT = python_datetime.astimezone(pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    @classmethod
    def fromJavascript(self, javascript_datetime):

        '''
            a method to construct labDT from a javascript datetime string
        :param javascript_datetime: string with datetime info in javascript formatting
        :return: labDT
        '''

    # validate inputs
        title = 'Javascript datetime string input for labDT.fromJavascript'
        jsDTpattern = re.compile('\s*\(.*\)$')
        jsGMTpattern = re.compile('GMT[-\+]\d{4}')
        if not jsGMTpattern.findall(javascript_datetime):
            raise Exception('\n%s must have a GMT timezone adjustment.' % title)

    # construct datetime from javascript string
        adj_input = jsDTpattern.sub('', javascript_datetime)
        if '-' in adj_input:
            adj_input = adj_input.replace('-','+')
        elif '+' in adj_input:
            adj_input = adj_input.replace('+','-')
        python_datetime = dTparser.parse(adj_input)
        dT = python_datetime.astimezone(pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )

    @classmethod
    def fromPattern(self, datetime_string, datetime_pattern, time_zone):

        '''
            a method for constructing labDT from a strptime pattern in a string
            https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            iso_pattern: '%Y-%m-%dT%H:%M:%S.%f%z'
            human_friendly_pattern: '%A, %B %d, %Y %I:%M:%S.%f%p'
        :param datetime_string: string with date and time info
        :param datetime_pattern: string with python formatted pattern
        :param time_zone: string with timezone info
        :return: labDT object with datetime
        '''

    # validate inputs
        title = 'input for labDT.fromPattern'
        dT_req = [['%Y','%y'],['%b','%B','%m'],['%d'],['%H','%I']]
        req_counter = 0
        for i in dT_req:
            for j in i:
                if j in datetime_pattern:
                    req_counter += 1
        if not req_counter == 4:
            raise Exception('Datetime pattern %s must contain at least year, month, day and hour.' % title)
        try:
            get_tz = tz.gettz(time_zone)
        except:
            raise ValueError('Timezone %s is not a valid timezone format.' % title)

    # decipher datetime
        python_datetime = datetime.strptime(datetime_string, datetime_pattern)
        python_datetime = python_datetime.replace(tzinfo=tz.gettz(time_zone))
        dT = python_datetime.astimezone(pytz.utc)
        return labDT(
            year=dT.year,
            month=dT.month,
            day=dT.day,
            hour=dT.hour,
            minute=dT.minute,
            second=dT.second,
            microsecond=dT.microsecond,
            tzinfo=dT.tzinfo
        )


if __name__ == '__main__':
    print(labID().id48)
    print(labID().epoch)




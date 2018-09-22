__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

# pip install pytz
# pip install tzlocal
    
import re
from datetime import datetime
from tzlocal import get_localzone
from dateutil import parser as dTparser
from dateutil import tz
import pytz

class labDT(datetime):

    ''' a class of methods for datetime conversion

    for list of timezones:
        https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones
    for list of datetime directives:
        https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    '''

    @classmethod
    def new(cls):

        ''' a method to generate the current datetime as a labDT object
        
        :return: labDT object
        '''

        dT = datetime.utcnow().replace(tzinfo=pytz.utc)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    def zulu(self):

        ''' a method to report ISO UTC datetime string from a labDT object

        NOTE: for timezone offset string use .isoformat() instead

        :return: string in ISO UTC format
        '''

    # construct ISO UTC string from labDT
        utc_dt = self.astimezone(pytz.utc)
        iso_dt = utc_dt.isoformat()
        return iso_dt.replace('+00:00', 'Z')

    def epoch(self):

        ''' a method to report posix epoch timestamp from a labDT object

        :return: float with timestamp
        '''

    # construct epoch timestamp from labDT
        epoch_dt = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        delta_time = self - epoch_dt
        return delta_time.total_seconds()

    def rfc2822(self):

        ''' 
            a method to report a RFC-2822 Compliant Date from a labDT object

            https://tools.ietf.org/html/rfc2822.html#page-14

        :return: string with RFC-2822 compliant date time
        '''

    # define format
        js_format = '%a, %d %b %Y %H:%M:%S GMT'
        utc_time = self.astimezone(pytz.utc)

        return format(utc_time, js_format)

    def pyLocal(self, time_zone=''):

        ''' a method to report a python datetime from a labDT object

        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        get_tz = get_localzone()
        title = 'Timezone input for labDT.pyLocal'
        if time_zone:
            # if time_zone.lower() in ('utc', 'uct', 'universal', 'zulu'):
            #     raise ValueError('time_zone cannot be UTC. %s requires a local timezone value. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('\n%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)

    # construct python datetime from labDT
        dT = self.astimezone(get_tz)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    def jsLocal(self, time_zone=''):

        ''' a method to report a javascript string from a labDT object

        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        js_format = '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
        title = 'Timezone input for labDT.jsLocal'
        get_tz = get_localzone()
        if time_zone:
            # if time_zone.lower() in ('utc', 'uct', 'universal', 'zulu'):
            #     raise ValueError('time_zone cannot be UTC. %s requires a local timezone value. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('\n%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)

    # construct javascript datetime from labDT
        dtLocal = self.astimezone(get_tz)
        return format(dtLocal, js_format)

    def humanFriendly(self, time_zone='', include_day=True, include_time=True):

        ''' a method to report a human friendly string from a labDT object

        :param time_zone: [optional] string with timezone to report in
        :return: string with date and time info
        '''

    # validate inputs
        zeroHourPattern = re.compile('\s0\d:')
        title = 'Timezone input for labDT.humanFriendly'
        human_format = ''
        if include_day:
            human_format += '%A, '
        human_format += '%B %d, %Y'
        if include_time:
            human_format += ' %I:%M%p %Z'
        get_tz = get_localzone()
        if time_zone:
            # if time_zone.lower() in ('utc', 'uct', 'universal', 'zulu'):
            #     raise ValueError('time_zone cannot be UTC. %s requires a local timezone value. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)
            try:
                get_tz = tz.gettz(time_zone)
            except:
                raise ValueError('%s is not a valid timezone format. Try:\nfor tz in pytz.all_timezones:\n  print tz' % title)
        
    # construct human friendly string from labDT
        dtLocal = self.astimezone(get_tz)
        dtString = format(dtLocal, human_format)
        zeroHour = zeroHourPattern.findall(dtString)
        if zeroHour:
            noZero = zeroHour[0].replace(' 0',' ')
            dtString = zeroHourPattern.sub(noZero,dtString)
        return dtString

    @classmethod
    def fromEpoch(cls, epoch_time):

        ''' a method for constructing a labDT object from epoch timestamp

        :param epoch_time: number with epoch timestamp info
        :return: labDT object
        '''

    # validate input
        title = 'Epoch time input for labDT.fromEpoch'
        if not isinstance(epoch_time, float) and not isinstance(epoch_time, int):
            raise TypeError('\n%s must be an integer or float.' % title)

    # construct labDT from epoch time
        dT = datetime.utcfromtimestamp(epoch_time).replace(tzinfo=pytz.utc)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    @classmethod
    def fromISO(cls, iso_string):

        ''' a method for constructing a labDT object from a timezone aware ISO string
        
        :param iso_string: string with date and time info in ISO format
        :return: labDT object
        '''

    # validate input
        title = 'ISO time input for labDT.fromISO'
        isopattern = re.compile('\d{4}-?\d{2}-?\d{2}[\s|T].*')
        if not isopattern.search(iso_string):
            raise ValueError('\n%s is not a valid ISO string.' % title)
        python_datetime = dTparser.parse(iso_string)
        if not python_datetime.tzinfo:
            raise ValueError('\n%s must have timezone info.' % title)

    # construct labDT from parsed string
        dT = python_datetime.astimezone(pytz.utc)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    @classmethod
    def fromPython(cls, python_datetime):

        ''' a method for constructing a labDT from a python datetime with timezone info
        
        :param python_datetime: datetime object with timezone info
        :return: labDT object
        '''

    # validate inputs
        title = 'Python datetime input for labDT.fromPython'
        if not isinstance(python_datetime, datetime):
            raise TypeError('\n%s must be a valid %s object.' % (title, datetime.__class__))
        elif not python_datetime.tzinfo:
            raise ValueError('\n%s must have a timezone.' % title)

    # construct labDT from python datetime
        dT = python_datetime.astimezone(pytz.utc)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    @classmethod
    def fromJavascript(cls, javascript_datetime):

        ''' a method to construct labDT from a javascript datetime string
        
        :param javascript_datetime: string with datetime info in javascript formatting
        :return: labDT object
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
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

    @classmethod
    def fromPattern(cls, datetime_string, datetime_pattern, time_zone, require_hour=True):

        '''
            a method for constructing labDT from a strptime pattern in a string
            https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
            iso_pattern: '%Y-%m-%dT%H:%M:%S.%f%z'
            human_friendly_pattern: '%A, %B %d, %Y %I:%M:%S.%f%p'
        :param datetime_string: string with date and time info
        :param datetime_pattern: string with python formatted pattern
        :param time_zone: string with timezone info
        :param require_hour: [optional] boolean to disable hour requirement
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
        if not req_counter == 4 and require_hour:
            raise Exception('Datetime pattern %s must contain at least year, month, day and hour.' % title)
        try:
            get_tz = tz.gettz(time_zone)
        except:
            raise ValueError('Timezone %s is not a valid timezone format.' % title)

    # decipher datetime
        python_datetime = datetime.strptime(datetime_string, datetime_pattern)
        python_datetime = python_datetime.replace(tzinfo=tz.gettz(time_zone))
        dT = python_datetime.astimezone(pytz.utc)
        dt_kwargs = {
            'year': dT.year,
            'month': dT.month,
            'day': dT.day,
            'hour': dT.hour,
            'minute': dT.minute,
            'second': dT.second,
            'microsecond': dT.microsecond,
            'tzinfo': dT.tzinfo
        }
        return labDT(**dt_kwargs)

if __name__ == '__main__':
    dt = labDT.new()
    print(dt.humanFriendly('US/Hawaii'))
    print(dt.rfc2822())
    print(dt.isoformat().replace('T', ' ')[0:19])
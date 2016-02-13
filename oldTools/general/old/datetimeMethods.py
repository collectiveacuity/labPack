__author__ = 'rcj1492'
__created__ = '2015'

# methods for conversion of datetime formats
# documentation: https://docs.python.org/2/library/datetime.html#
# pip install python-dateutil
# pip install pytz
# pip install tzlocal

from datetime import datetime
import re
import pytz
from tzlocal import get_localzone
from dateutil import parser as dTparser
from dateutil import tz

# from timeit import default_timer as timer
# t1 = timer()

class labDT(datetime):
    '''
        a persistent class for datetime conversion methods
        inherits from class datetime.datetime
        for list of timezones:
            https://stackoverflow.com/questions/13866926/python-pytz-list-of-timezones
        for list of datetime directives:
            https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        from datetime import datetime
        import re
        import pytz
        from tzlocal import get_localzone
        from dateutil import parser as dTparser
        from dateutil import tz
    '''

    @classmethod
    def new(self):
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

    def ISO(self):
        utc_dt = self.astimezone(pytz.utc)
        iso_dt = utc_dt.isoformat()
        return iso_dt.replace('+00:00', 'Z')

    def epoch(self):
        epoch_dt = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
        delta_time = self - epoch_dt
        return delta_time.total_seconds()

    def pyLocal(self, time_zone=False):
        get_tz = get_localzone()
        if time_zone:
            if not isinstance(time_zone, str):
                raise Exception('input is not the correct data type')
            elif not tz.gettz(time_zone):
                raise Exception('input is not a valid timezone format')
            else:
                get_tz = tz.gettz(time_zone)
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
        js_format = '%a %b %d %Y %H:%M:%S.%f GMT%z (%Z)'
        get_tz = get_localzone()
        if time_zone:
            if not isinstance(time_zone, str):
                raise Exception('input is not the correct data type')
            elif not tz.gettz(time_zone):
                raise Exception('input is not a valid timezone format')
            else:
                get_tz = tz.gettz(time_zone)
        dtLocal = self.astimezone(get_tz)
        return format(dtLocal, js_format)

    def humanFriendly(self, time_zone=False):
        zeroHourPattern = re.compile('\s0\d:')
        human_format = '%A, %B %d, %Y %I:%M%p %Z'
        get_tz = get_localzone()
        if time_zone:
            if not isinstance(time_zone, str):
                raise Exception('input is not the correct data type')
            elif not tz.gettz(time_zone):
                raise Exception('input is not a valid timezone format')
            else:
                get_tz = tz.gettz(time_zone)
        dtLocal = self.astimezone(get_tz)
        dtString = format(dtLocal, human_format)
        zeroHour = zeroHourPattern.findall(dtString)
        if zeroHour:
            noZero = zeroHour[0].replace(' 0',' ')
            dtString = zeroHourPattern.sub(noZero,dtString)
        return dtString

    @classmethod
    def fromEpoch(self, epoch_time):
        if not epoch_time:
            raise Exception('required parameters are missing')
        elif not isinstance(epoch_time, int) and not isinstance(epoch_time, float):
            raise Exception('input is not the correct data type')
        else:
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
        isopattern = re.compile('\d{4}-\d{2}-\d{2}T.*')
        if not iso_string:
            raise Exception('required parameters are missing')
        elif not isinstance(iso_string, str):
            raise Exception('input is not the correct data type')
        elif not isopattern.search(iso_string):
            raise Exception('input is not a valid ISO string')
        else:
            python_datetime = dTparser.parse(iso_string)
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
        if not python_datetime:
            raise Exception('required parameters are missing')
        elif not isinstance(python_datetime, datetime):
            raise Exception('input is not the correct data type')
        elif not python_datetime.tzinfo:
            raise Exception('datetime must have a timezone')
        else:
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
        jsDTpattern = re.compile('\s*\(.*\)$')
        jsGMTpattern = re.compile('GMT[-\+]\d{4}')
        if not javascript_datetime:
            raise Exception('required parameters are missing')
        elif not isinstance(javascript_datetime, str):
            raise Exception('input is not the correct data type')
        elif not jsGMTpattern.findall(javascript_datetime):
            raise Exception('datetime must have a GMT timezone adjustment')
        else:
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
            iso_pattern: '%Y-%m-%dT%H:%M:%S.%f%z'
            human_friendly_pattern: '%A, %B %d, %Y %I:%M:%S.%f%p'
        :param datetime_string:
        :param datetime_pattern:
        :param time_zone:
        :return:
        '''
        if not datetime_string or not datetime_pattern or not time_zone:
            raise Exception('required parameters are missing')
        elif not isinstance(datetime_string, str) or not isinstance(datetime_pattern, str) \
                or not isinstance(time_zone, str):
            raise Exception('inputs are not the correct data type')
        else:
            dT_req = [['%Y','%y'],['%b','%B','%m'],['%d'],['%H','%I']]
            req_counter = 0
            for i in dT_req:
                for j in i:
                    if j in datetime_pattern:
                        req_counter += 1
            if not req_counter == 4:
                raise Exception('datetime pattern must contain at least year, month, day and hour')
            elif not tz.gettz(time_zone):
                raise Exception('input is not a valid timezone format')
            else:
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

# Unit Test Method
def labDTUnitTests():
    '''
        a set of unit tests for the labDT class
    :return: True
    '''
# define variables
    epochDT = 1420167845.67891
    isoDT = '2015-01-01T22:04:05.678910-0500'
    pyDT = datetime(2015, 1, 2, 4, 4, 5, 678910, tzinfo=tz.gettz('Europe/Copenhagen'))
    jsDT = 'Thu Jan 01 2015 22:04:05.678910 GMT-0500 (Eastern Standard Time)'
    humanDT = 'Friday, January 2, 2015 12:04PM 5.67891sec' # Time in Palau
    pattern = '%A, %B %d, %Y %I:%M%p %S.%fsec'
# assertion tests
    assert labDT.new()
    assert labDT.fromEpoch(epochDT).pyLocal() == labDT.fromISO(isoDT).pyLocal()
    assert labDT.fromPython(pyDT).epoch() == labDT.fromJavascript(jsDT).epoch()
    assert labDT.fromPattern(humanDT, pattern, 'Pacific/Palau').ISO() == labDT.fromPython(pyDT).ISO()
    assert labDT.fromEpoch(epochDT).humanFriendly() == labDT.fromJavascript(jsDT).humanFriendly()
    assert labDT.fromPattern(humanDT, pattern, 'Pacific/Palau').jsLocal() == labDT.fromISO(isoDT).jsLocal()
    return True

labDTUnitTests()

# t2 = timer()
# print(str(t2 - t1) + ' seconds')

t = labDT.new()
print(t.ISO())
__author__ = 'rcj1492'
__created__ = '2015.09'

import pytz
from datetime import datetime

class dT(datetime):

    dt = datetime.utcnow().replace(tzinfo=pytz.utc)
    year = dt.year
    month = dt.month
    day = dt.day
    second = 12
    happy = 'yes'

    def __init__(self, year=datetime.utcnow().replace(tzinfo=pytz.utc)):
        dt = datetime.utcnow().replace(tzinfo=pytz.utc)
        super(dT, self).__init__(self, dt.year, dt.month, dt.day)

t = dT()
print(t)
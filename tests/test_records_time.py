__author__ = 'rcj1492'
__created__ = '2016.07'
__license__ = 'MIT'

try:
    import pytest
except:
    print('pytest module required to perform unittests. try: pip install pytest')
    exit()

from datetime import datetime
from dateutil import tz
from labpack.performance import labPerform
from labpack.records.time import labDT

class testlabDT(object):

    def __init__(self):
        pass

    def unitTests(self):

    # define variables
        epochDT = 1420167845.67891
        isoDT = '2015-01-01T22:04:05.678910-0500'
        pyDT = datetime(2015, 1, 2, 4, 4, 5, 678910, tzinfo=tz.gettz('Europe/Copenhagen'))
        jsDT = 'Thu Jan 01 2015 22:04:05.678910 GMT-0500 (Eastern Standard Time)'
        humanDT = 'Friday, January 2, 2015 12:04PM 5.67891sec'  # Time in Palau
        pattern = '%A, %B %d, %Y %I:%M%p %S.%fsec'

    # assertion tests
        assert labDT.new()
        assert labDT.fromEpoch(epochDT).pyLocal() == labDT.fromISO(isoDT).pyLocal()
        assert labDT.fromPython(pyDT).epoch() == labDT.fromJavascript(jsDT).epoch()
        assert labDT.fromPattern(humanDT, pattern, 'Pacific/Palau').iso() == labDT.fromPython(pyDT).iso()
        assert labDT.fromEpoch(epochDT).humanFriendly() == labDT.fromJavascript(jsDT).humanFriendly()
        assert labDT.fromPattern(humanDT, pattern, 'Pacific/Palau').jsLocal() == labDT.fromISO(isoDT).jsLocal()

    # exception tests
        with pytest.raises(ValueError):  # no timezone info in ISO datetime
            labDT.fromISO(isoDT[0:26])

        return self

    def performanceTests(self):

        labPerform.repeat(labDT.new(), 'labDT.new()', 10000)

        return self

if __name__ == '__main__':
    testlabDT().unitTests()
    testlabDT().performanceTests()
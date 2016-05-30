__author__ = 'rcj1492'
__created__ = '2016.05'
__license__ = 'MIT'

try:
    import pytest
except:
    print('pytest module required to perform unittests. try: pip install pytest')
    exit()

from labpack.records import labID, labDT
from labpack.performance import labPerform
from datetime import datetime
from dateutil import tz

class testlabID(labID):

    def __init__(self):
        labID.__init__(self)

    def unitTests(self):

    # assertion tests
        assert self.__name__ == 'labID'
        assert len(self.id12) == 12
        assert len(self.id24) == 24
        assert len(self.id36) == 36
        assert len(self.id48) == 48
        assert len(self.mac) == 17
        assert len(str(self.uuid)) == 36
        assert isinstance(self.epoch, float)
        assert isinstance(self.iso, str)
        assert isinstance(self.datetime, datetime)

        return self

    def performanceTests(self):

        labPerform(labID().id48, 'labID().id48', 10000)
        labPerform(labID().mac, 'labID().mac', 10000)
        labPerform(labID().datetime, 'labID().datetime', 10000)

        return self

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

        labPerform(labDT.new(), 'labDT.new()', 10000)

        return self

if __name__ == '__main__':
    testlabID().unitTests()
    testlabDT().unitTests()
    testlabID().performanceTests()
    testlabDT().performanceTests()


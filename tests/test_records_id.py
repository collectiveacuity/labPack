__author__ = 'rcj1492'
__created__ = '2016.05'
__license__ = 'MIT'

from datetime import datetime
from labpack.performance import performlab
from labpack.records.id import labID

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

        performlab.repeat(labID().id48, 'labID().id48', 10000)
        performlab.repeat(labID().mac, 'labID().mac', 10000)
        performlab.repeat(labID().datetime, 'labID().datetime', 10000)

        return self

if __name__ == '__main__':
    testlabID().unitTests()
    testlabID().performanceTests()


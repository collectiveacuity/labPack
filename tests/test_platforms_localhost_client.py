__author__ = 'rcj1492'
__created__ = '2016.03'

from labpack.performance import labPerform
from labpack.platforms.localhost_client import localhostClient

class testLocalhostClient(localhostClient):

    def __init__(self):
        localhostClient.__init__(self)

    def unitTests(self):

        os = self.os
        assert os
        username = self.username
        assert username
        ip = self.ip
        assert ip
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path
        self.os = 'Linux'
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path
        self.os = 'Mac'
        data_path = self.appData('Collective Acuity', 'pocketLab')
        assert data_path

        return self

    def performanceTests(self):

        index_root = '../../../'
        labPerform(self.index(index_root).files[45], 'localhostClient.fileList(../../../)', 10000)
        print('Number of files in fileList: %s'% len(self.files))

        return self

if __name__ == '__main__':
    testLocalhostClient().unitTests()
    testLocalhostClient().performanceTests()
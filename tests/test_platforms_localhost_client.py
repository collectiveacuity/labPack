__author__ = 'rcj1492'
__created__ = '2016.03'

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
        home = self.home
        assert home
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        file_query = self.query(key_query=['.py'], results=5, top_down=False, query_root='../')
        assert file_query
        print(file_query)
        self.os = 'Linux'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os = 'Mac'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path


        return self

    def performanceTests(self):

        return self

if __name__ == '__main__':
    testLocalhostClient().unitTests()
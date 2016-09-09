__author__ = 'rcj1492'
__created__ = '2016.03'

from labpack.platforms.localhost import localhostClient

class testLocalhostClient(localhostClient):

    def __init__(self):
        localhostClient.__init__(self)

    def unittests(self):

        os = self.os
        assert os
        username = self.username
        if os == 'Windows':
            assert username
        ip = self.ip
        assert ip
        home = self.home
        assert home
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os = 'Linux'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os = 'Mac'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path

    # test empty query returns 1 result from current folder
        file_query = self.find()
        assert len(file_query) == 1
        assert file_query[0].find('test_')

    # test query method with single query filter
        query_filters=[{'.file_name':{'must_not_contain':['localhost']}}]
        file_query = self.find(query_filters=query_filters)
        assert file_query

    # test query method with each valid record field in query criteria
        query_filters = [{'.file_name': {'discrete_values': ['__init__.py']}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        query_filters = [{'.file_size': {'max_value': 500}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        query_filters = [{'.file_path': {'must_contain': ['labpack']}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        query_filters = [{'.create_date': {'min_value': 1467334000.674533}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        query_filters = [{'.update_date': {'less_than': 1467334000.674533}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        query_filters = [{'.access_date': {'greater_than': 1467334000.674533}}]
        file_query = self.find(query_filters=query_filters, query_root='../')
        assert file_query
        print(file_query)

        return self

    def performanceTests(self):

        return self

if __name__ == '__main__':
    testLocalhostClient().unittests()
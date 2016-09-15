__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from labpack.platforms.localhost import localhostClient
from labpack.performance import labPerform

class testLocalhostClient(localhostClient):

    def __init__(self):
        localhostClient.__init__(self)

    def unittests(self):

        os = self.os.sysname
        assert os
        ip = self.ip
        assert ip
        home = self.home
        assert home
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os.sysname = 'Linux'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os.sysname = 'Darwin'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path

    # test empty list returns a list with 1 result from current folder
        file_list = self.list()
        assert len(file_list) == 1
        assert file_list[0].find('test_')

    # test list starting file returns a list with the next result from current folder
        file_list_a = self.list(max_results=3)
        file_list_b = self.list(previous_file=file_list_a[1])
        assert file_list_a[2] == file_list_b[0]

    # test list with higher max results, reverse order and previous results in sub directory
        file_list_c = self.list(walk_root='../', max_results=100, reverse_order=True)
        assert len(file_list_c) == 100
        file_list_d = self.list(walk_root='../', max_results=100, previous_file=file_list_c[96], reverse_order=True)
        assert file_list_c[99] == file_list_d[2]

    # test metadata of file list results
        print(self.metadata(file_list_a[0]))

    # test empty query returns a list with 1 result from current folder
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

        # import os
        # for current_dir, sub_dir, dir_files in os.walk('../', topdown=True):
        #     print(sub_dir)
        #     sub_dir.sort()
        #     sub_dir.reverse()
        #     print(sub_dir)
        #     if '.git' in sub_dir:
        #         sub_dir.remove('.git')
        #     for file in dir_files:
        #         print(os.path.join(current_dir, file))

        return self

    def performanceTests(self):

        labPerform.repeat(self.list(walk_root='../', max_results=1000, previous_file='/home/rcj/Dropbox/Lab/Dev/pyMod/labPack/labpack/compilers/drep.py'), 'localhost.list(max_results=1000)', 10000)

        return self

if __name__ == '__main__':
    testLocalhostClient().unittests()
    # testLocalhostClient().performanceTests()


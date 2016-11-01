__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

from labpack.platforms.localhost import localhostClient
from labpack.performance import performlab

class testLocalhostClient(localhostClient):

    def __init__(self):
        localhostClient.__init__(self)

    def unittests(self):

        from copy import deepcopy

        os_name = deepcopy(self.os.sysname)
        assert os_name
        ip = self.ip
        assert ip
        home = deepcopy(self.home)
        assert home
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path
        self.os.sysname = 'Linux'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path.find('.config')
        self.os.sysname = 'Darwin'
        self.home = '~/'
        data_path = self.appData('Collective Acuity', 'labpack')
        assert data_path.find('Library')
        self.os.sysname = os_name
        self.home = home
        assert 'file_path' in self.fileModel.schema.keys()

    # test walk generator and metadata
        for file_path in self.walk(walk_root='../'):
            assert file_path
            assert 'update_date' in self.metadata(file_path).keys()
            break

    # test empty list returns a list with 1 result from current folder
        file_list = self.list()
        assert len(file_list) == 1
        assert file_list[0].find('test_')

    # test list starting file returns a list with the next result from current folder
        file_list_a = self.list(max_results=3)
        file_list_b = self.list(previous_file=file_list_a[1])
        assert file_list_a[2] == file_list_b[0]

    # test list with higher max results, reverse order and previous results in sub directory
        file_list_c = self.list(list_root='../', max_results=10, reverse_order=True)
        assert len(file_list_c) == 10
        file_list_d = self.list(list_root='../', max_results=10, previous_file=file_list_c[6], reverse_order=True)
        assert file_list_c[9] == file_list_d[2]

    # test walk and list produce the same results
        file_list_e = self.list(list_root='../', max_results=20, reverse_order=True)
        file_list_f = self.list(list_root='../', max_results=10, reverse_order=True, previous_file=file_list_e[19])
        count = 0
        for file in self.walk(walk_root='../', reverse_order=True):
            count += 1
            if count > 20:
                assert file == file_list_f[count - 21]
            if count == 30:
                break

    # test filter function
        metadata_filters = [{'.file_name': {'must_not_contain': ['localhost']}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        assert filter_function(**{'file_name': 'test.json'})
        assert not filter_function(**{'file_name': 'localhost.py'})

    # test list method with filter functions
        filter_list = self.list(filter_function=filter_function)
        assert filter_list
        metadata_filters = [{'.file_name': {'discrete_values': ['__init__.py']}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        metadata_filters = [{'.file_size': {'max_value': 500}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        metadata_filters = [{'.file_path': {'must_contain': ['labpack']}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        metadata_filters = [{'.create_date': {'min_value': 1467334000.674533}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        metadata_filters = [{'.update_date': {'less_than': 1467334000.674533}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        metadata_filters = [{'.access_date': {'greater_than': 1467334000.674533}}]
        filter_function = self.conditionalFilter(metadata_filters=metadata_filters)
        filter_list = self.list(filter_function=filter_function, list_root='../')
        assert filter_list
        print(filter_list)

        return self

    def performanceTests(self):

        performlab.repeat(self.list(list_root='../', max_results=1000, previous_file='../labpack/compilers/drep.py'), 'localhost.list(max_results=1000)', 10000)

        return self

if __name__ == '__main__':
    testLocalhostClient().unittests()
    testLocalhostClient().performanceTests()


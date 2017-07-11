__author__ = 'rcj1492'
__created__ = '2016.03'
__license__ = 'MIT'

try:
    import pytest
except:
    print('pytest module required to perform unittests. try: pip install pytest')
    exit()

from labpack.storage.appdata import appdataClient
from labpack.performance import performlab
from jsonmodel.exceptions import InputValidationError

class testAppdataClient(appdataClient):

    def __init__(self):
        appdataClient.__init__(self, collection_name='Unit Tests')

    def unitTests(self):

        from time import time
        from copy import deepcopy
        testKey = 'lab/log/unittest'
        testDetails = { 'command': 'home', 'project': 'lab', 'verbose': True }
        seed_details = deepcopy(testDetails)
        seed_details['type'] = '.json'
        seed_details['time'] = time()
        seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
        self.create(record_key=seed_key, record_body=seed_details)
        file_types = [ 'json', 'json.gz', 'yaml', 'yaml.gz', 'drep' ]
        for type in file_types:
            test_dt = time()
            file_type = type.replace('_','.')
            test_details = deepcopy(testDetails)
            test_details['type'] = file_type
            test_details['time'] = test_dt
            test_key = '%s/%s.%s' % (testKey, str(test_details['time']), file_type)
            secret_key = ''
            if type == 'drep':
                secret_key = 'test-key'
            self.create(record_key=test_key, record_body=test_details, secret_key=secret_key)
            assert self.read(record_key=test_key, secret_key=secret_key)
            assert test_key in self.list(max_results=100, reverse_search=False)
            path_filters = [{0: {'must_contain': ['^lab']}, 2:{'discrete_values': ['unittest']}}]
            filter_function = self.conditional_filter(path_filters=path_filters)
            assert test_key in self.list(filter_function=filter_function, max_results=100)
            assert self.delete(record_key=test_key)
        self.delete(record_key=seed_key)
        self.remove()

    # test filter method
        path_segments = ['lab', 'unittests', '1473719695.2165067', '.json']
        path_filters = [ { 0: { 'must_contain': [ '^lab' ] } } ]
        filter_function = self.conditional_filter(path_filters=path_filters)
        assert filter_function(*path_segments)

    # test filter false results
        path_filters = [{0: {'must_not_contain': ['^lab']}}]
        filter_function = self.conditional_filter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{0: {'must_contain': ['^lab']}, 1:{'excluded_values': ['unittests']} }]
        filter_function = self.conditional_filter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{0: {'must_contain': ['^lab']}, 2: {'discrete_values': ['unittests']}}]
        filter_function = self.conditional_filter(path_filters=path_filters)
        assert not filter_function(*path_segments)
        path_filters = [{4: {'must_contain': ['^lab']}}]
        filter_function = self.conditional_filter(path_filters=path_filters)
        assert not filter_function(*path_segments)

    # test filter exceptions
        path_filters = [{ '0': {'must_contain': ['^lab']}}]
        with pytest.raises(TypeError):
            self.conditional_filter(path_filters=path_filters)
        path_filters = [{ 0: 'string' }]
        with pytest.raises(TypeError):
            self.conditional_filter(path_filters=path_filters)
        path_filters = [{ 0: {'must_contai': ['^lab']}}]
        with pytest.raises(InputValidationError):
            self.conditional_filter(path_filters=path_filters)

        return self

    def performanceTests(self):

        from time import time, sleep
        from copy import deepcopy
        testKey = 'lab/log/performancetest'
        testDetails = {'command': 'home', 'project': 'lab', 'verbose': True}
        count = 0
        last_key = ''
        while count < 100:
            seed_details = deepcopy(testDetails)
            seed_details['type'] = '.json'
            seed_details['time'] = time()
            seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
            self.create(record_key=seed_key, record_body=seed_details)
            count += 1
            sleep(.001)
            if count == 2:
                last_key = deepcopy(seed_key)
        path_filters = [{ 1:{'must_contain':['^log']}}]
        filter_function = self.conditional_filter(path_filters=path_filters)
        perform_kwargs = {
            'filter_function': filter_function, 
            'max_results': 100, 
            'previous_key': last_key
        }
        performlab.repeat(self.list, perform_kwargs, 'appdataClient.list(filter_function=self.conditional_filter(%s), max_results=100, previous_key=%s)' % (path_filters, last_key), 1000)
        self.remove()

        return self

if __name__ == '__main__':

# initialize client
    test_schema = { 'schema': {
        'dt': 1474505298.768161,
        'deviceID': 'ZeLPQ77bU3qnl5QI9ucwZyLK',
        'metric': 'temperature',
        'value': 34.5,
        'units': 'degrees Celsius'
    } }
    test_settings = {
        'enforce_schema': False,
        'index_fields': ['.deviceID', '.dt']
    }
    test_record = {
        'dt': 1474509314.419702,
        'deviceID': '2Pp8d9lpsappm8QPv_Ps6cL0'
    }
    test_client = testAppdataClient()

# test byte data
    from hashlib import md5
    test_data = open('../data/test_voice.ogg', 'rb').read()
    test_key = 'lab/voice/unittest.ogg'
    secret_key = 'upside'
    old_hash = md5(test_data).digest()
    test_client.create(test_key, test_data, secret_key=secret_key)
    test_filter = test_client.conditional_filter([{2:{'must_contain':['unittest\.ogg$']}}])
    test_search = test_client.list(test_filter)
    new_data = test_client.read(test_search[0], secret_key=secret_key)
    new_hash = md5(new_data).digest()
    assert old_hash == new_hash
    assert test_client.delete(test_search[0])

# test record data
    test_client.unitTests()
    test_client.performanceTests()
    # test_kwargs = { 'record_schema': test_schema, 'collection_settings': test_settings }
    # test_appdata_model = testAppdataModel(**test_kwargs)
    # testAppdataModel(appdata_model=test_appdata_model).unitTests()

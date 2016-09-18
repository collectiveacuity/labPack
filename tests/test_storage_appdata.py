__author__ = 'rcj1492'
__created__ = '2016.03'

from labpack.storage.appdata import appdataClient, appdataModel
from labpack.performance import labPerform

class testAppdataClient(appdataClient):

    def __init__(self):
        appdataClient.__init__(self)

    def unitTests(self):

        from time import time
        from copy import deepcopy
        testKey = 'lab/log/unittest'
        testDetails = { 'command': 'home', 'project': 'lab', 'verbose': True }
        seed_details = deepcopy(testDetails)
        seed_details['type'] = '.json'
        seed_details['time'] = time()
        seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
        self.create(seed_key, seed_details)
        file_types = set(self.ext.__dir__()) - set(self.ext.builtins)
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
            self.create(test_key, test_details, secret_key=secret_key)
            assert self.read(test_key, secret_key)
            assert test_key in self.list(max_results=100, reverse_order=False)
            assert test_key in self.find(path_filters=[{'0':{'must_contain':['^lab']}, '1':{'must_contain': ['^log']}}], max_results=3)
            assert self.delete(test_key)
        self.delete(seed_key)
        self.remove()

        return self

    def performanceTests(self):

        from time import time, sleep
        from copy import deepcopy
        testKey = 'lab/log/unittest'
        testDetails = {'command': 'home', 'project': 'lab', 'verbose': True}
        count = 0
        last_key = ''
        while count < 100:
            seed_details = deepcopy(testDetails)
            seed_details['type'] = '.json'
            seed_details['time'] = time()
            seed_key = '%s/%s%s' % (testKey, str(seed_details['time']), seed_details['type'])
            self.create(seed_key, seed_details)
            count += 1
            sleep(.001)
            if count == 2:
                last_key = deepcopy(seed_key)
        labPerform.repeat(self.list(max_results=100), 'appdataClient.list(max_results=100)', 10000)
        labPerform.repeat(self.find(path_filters=[{'1':{'must_contain':['^log']}}],max_results=100, previous_key=last_key), 'appdataClient.find(path_filters=[{"1":{"must_contain":["^log"]}}], max_results=100, previous_key=%s)' % last_key, 10000)
        self.remove()

        return self

class testAppdataModel(appdataModel):

    def __init__(self, record_schema=None, collection_settings=None, appdata_model=None):
        appdataModel.__init__(self, record_schema=record_schema, collection_settings=collection_settings, appdata_model=appdata_model)

    def unitTests(self):

        return self


if __name__ == '__main__':
    record_schema = {
        'schema': {
            'test': 'me'
        }
    }
    collection_settings = {
        'index_fields': []
    }
    testAppdataClient().unitTests()
    # testAppdataClient().performanceTests()
    # test_appdata_model = testAppdataModel(record_schema, collection_settings)
    # testAppdataModel(appdata_model=test_appdata_model).unitTests()

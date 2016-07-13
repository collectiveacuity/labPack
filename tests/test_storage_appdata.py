__author__ = 'rcj1492'
__created__ = '2016.03'

from labpack.storage.appdata import appdataClient, appdataModel

class testAppdataClient(appdataClient):

    def __init__(self):
        appdataClient.__init__(self)

    def unitTests(self):

        from time import time
        from copy import deepcopy
        testKey = 'lab-log-unittest'
        testDetails = { 'command': 'home', 'project': 'lab', 'verbose': True }
        for type in self.ext.types:
            test_dt = time()
            test_details = deepcopy(testDetails)
            test_details['type'] = type
            test_details['time'] = test_dt
            test_key = '%s-%s%s' % (testKey, str(test_details['time']), type)
            self.put(test_key, test_details)
            assert self.get(test_key)
            assert self.query(key_filters={'discrete_values': [test_key]})
            body_filter = { '.time': { 'min_value': test_dt } }
            assert self.query(body_filters=body_filter)
            assert self.delete(test_key)

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
    test_appdata_model = testAppdataModel(record_schema, collection_settings)
    testAppdataModel(appdata_model=test_appdata_model).unitTests()

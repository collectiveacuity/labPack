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
        file_types = set(self.ext.__dir__()) - set(self.ext.builtins)
        for type in file_types:
            test_dt = time()
            file_type = type.replace('_','.')
            test_details = deepcopy(testDetails)
            test_details['type'] = file_type
            test_details['time'] = test_dt
            test_key = '%s-%s.%s' % (testKey, str(test_details['time']), file_type)
            secret_key = ''
            if type == 'drep':
                secret_key = 'test-key'
            self.create(test_key, test_details, secret_key=secret_key)
            assert self.retrieve(test_key, secret_key)
            # assert self.query(key_filters={'discrete_values': [test_key]})
            # body_filter = { '.time': { 'min_value': test_dt } }
            # assert self.query(body_filters=body_filter)
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
